import torch.nn as nn
from .model_fold import FoldEncoder, FoldDecoder, FoldBiasDecoder
from .model_point import PointNetfeat, BiasDecoder, FCDecoder, PointDecoder, PointGridDecoder
from pytorch_lightning.core import LightningModule
from argparse import ArgumentParser
import torch

import torch_optimizer as opt
# import torch.optim as opt

import torch.nn.functional as F
from copy import deepcopy


def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def reorder_pts(recons, full_pts, obj_pts):
    cd_loss, _, idx2 = chamfer_loss(recons, full_pts)
    idx2 = idx2.long()
    reorder_obj = torch.stack([torch.index_select(oo, 0, ii)
                               for ii, oo in zip(idx2, obj_pts)], 0)
    reorder_obj = reorder_obj.transpose(2, 1)

    return reorder_obj, cd_loss


def chamfer_loss(recons_pts, gt_pts):
    gt_pts = gt_pts.float().transpose(1, 2)

    recons_pts = recons_pts.float().transpose(1, 2)

    dist1, dist2, idx1, idx2 = cham3D(gt_pts, recons_pts)

    loss = torch.mean(dist1) + torch.mean(dist2)
    return loss, idx1, idx2


def chamfer_loss6(recons_pts, gt_pts):
    gt_pts = gt_pts.float().transpose(1, 2)
    recons_pts = recons_pts.float().transpose(1, 2)

    dist1, dist2, idx1, idx2 = cham6D(gt_pts, recons_pts)

    loss = torch.mean(dist1) + torch.mean(dist2)
    return loss, idx1, idx2


def mse_loss(recons_pts, gt_pts):
    loss = F.mse_loss(recons_pts, gt_pts)
    return loss


def concat_feature(local_feature, glf, label, num_points):
    glf = torch.cat((glf, label), dim=1)
    glf = glf.repeat(1, 1, num_points)

    feature = torch.cat((local_feature, glf), dim=1)

    return feature


def to_full_glf(local1, local2):
    local = torch.cat((local1, local2), dim=2)
    glf = torch.max(local, 2, keepdim=True)[0]

    return glf


def build_association():
    return nn.Sequential(
        nn.Linear(525, 256),
        nn.ReLU(),
        nn.Linear(256, 128),
        nn.ReLU(),
        nn.Linear(128, 256),
        nn.ReLU(),
        nn.Linear(256, 512)
    )


class DenseCls(nn.Module):
    def __init__(self, k=2, feature_transform=False):
        super(DenseCls, self).__init__()
        self.fc1 = nn.Linear(1024, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, k)
        self.dropout = nn.Dropout(p=0.3)
        self.bn1 = nn.BatchNorm1d(256)
        self.bn2 = nn.BatchNorm1d(128)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = F.relu(self.bn1(self.fc1(x)))
        x = F.relu(self.bn2(self.dropout(self.fc2(x))))
        x = self.fc3(x)

        return x


class ReconstructionNet(nn.Module):
    def __init__(self, args0, seg_class=0, feat_dims=512, ch=12):
        super(ReconstructionNet, self).__init__()
        args = deepcopy(args0)
        self.args = args
        model_args = args['model']

        if model_args['encoder'] == 'graph':
            self.encoder = FoldEncoder(args, ch)
        elif model_args['encoder'] == 'point':
            self.encoder = PointNetfeat(args)

        if model_args['decoder'] == 'fold':
            self.decoder = FoldDecoder(args, seg_class)
        elif model_args['decoder'] == 'bias':
            self.decoder = BiasDecoder(args, seg_class, feat_dims)
        elif model_args['decoder'] == 'fc':
            self.decoder = FCDecoder(args, seg_class)
        elif model_args['decoder'] == 'point':
            self.decoder = PointDecoder(args, seg_class, feat_dims)
        elif model_args['decoder'] == 'bias-grid':
            self.decoder = PointGridDecoder(args, seg_class)
        elif model_args['decoder'] == 'fold-bias':
            self.decoder = FoldBiasDecoder(args, seg_class)

        print('Encoder Parameter', count_parameters(self.encoder) / 1024 / 1024, 'M')
        print('Decoder Parameter', count_parameters(self.decoder) / 1024 / 1024, 'M')

    def forward(self, input, option=0):
        if option == 0:
            # global_feature, local_feature = self.encoder(input, option)
            global_feature, local_feature = self.encoder(input)
        else:
            global_feature, local_feature, enc_result = self.encoder(input, option)

        if self.args['model']['decoder'] == 'point':
            output = self.decoder(global_feature, local_feature)
        else:
            output = self.decoder(global_feature)

        if option == 0:
            return output, global_feature
        else:
            return output, global_feature, enc_result

    def forward_glf(self, x, label, option=0):
        if option == 0:
            global_feature, local_feature = self.encoder(x)
        else:
            global_feature, local_feature, enc_result = self.encoder(x, option)

        global_feature2 = torch.cat((global_feature, label), dim=1)

        if self.args['model']['decoder'] == 'point':
            output = self.decoder(global_feature2, local_feature)
        else:
            output = self.decoder(global_feature2)

        if option == 0:
            return output, global_feature
        else:
            return output, global_feature, enc_result

    def forward_glf2(self, x, frame_glf):
        global_feature, local_feature = self.encoder(x)
        global_feature2 = torch.cat((global_feature, frame_glf), dim=1)

        if self.args['model']['decoder'] == 'point':
            output = self.decoder(global_feature2, local_feature)
        else:
            output = self.decoder(global_feature2)

        return output, global_feature

    def encoder_glf(self, x, label):
        global_feature, _ = self.encoder(x)
        global_feature = torch.cat((global_feature, label), dim=1)

        return global_feature

    def get_parameter(self):
        return list(self.encoder.parameters()) + list(self.decoder.parameters())


class FullAE(LightningModule):
    def __init__(
            self,
            args: dict,
            lr: float = 1e-4,
            b1: float = 0.5,
            b2: float = 0.999,
    ):
        super().__init__()

        self.save_hyperparameters()
        # self.seg_flag = args['model']['segment']
        self.seg_flag = False

        seg_class = args['parameter']['seg_class'] if self.seg_flag else 0

        self.seg_class = seg_class
        self.full_ae = ReconstructionNet(args, seg_class)
        self.args = args

    @staticmethod
    def add_argparse_args(parent_parser: ArgumentParser):
        parser = ArgumentParser(parents=[parent_parser], add_help=False)
        parser.add_argument("--lr", type=float, default=1e-4, help="adam: learning rate")
        parser.add_argument("--b1", type=float, default=0.5,
                            help="adam: decay of first order momentum of gradient")
        parser.add_argument("--b2", type=float, default=0.999,
                            help="adam: decay of second order momentum of gradient")

        return parser

    def forward(self, pts):
        return self.full_ae(pts)


class PartialRemainNet(LightningModule):
    def __init__(
            self,
            args: dict,
            lr: float = 1e-4,
            b1: float = 0.5,
            b2: float = 0.999,
    ):
        super().__init__()

        self.save_hyperparameters()

        remain_args = deepcopy(args)
        part_args = deepcopy(args)

        remain_args['parameter']['num_points'] = 1024
        part_args['parameter']['num_points'] = 2048

        dim_size = 16 + 512 + 50 + 512

        self.full_ae = ReconstructionNet(remain_args, feat_dims=dim_size, ch=12)
        self.vis_ae = ReconstructionNet(part_args, feat_dims=dim_size,
                                        ch=12)
        self.fc_p2f = build_association()

        self.args = args

    @staticmethod
    def add_argparse_args(parent_parser: ArgumentParser):
        parser = ArgumentParser(parents=[parent_parser], add_help=False)
        parser.add_argument("--lr", type=float, default=1e-4, help="adam: learning rate")
        parser.add_argument("--b1", type=float, default=0.5,
                            help="adam: decay of first order momentum of gradient")
        parser.add_argument("--b2", type=float, default=0.999,
                            help="adam: decay of second order momentum of gradient")

        return parser

    def forward(self, pts):
        part_glf = self.part_ae.encoder(pts)
        full_glf = self.fc_p2f(part_glf)
        full_pts = self.full_ae.decoder(full_glf)

        return full_pts

    def common_step(self, batch):
        obj_one, part_one, full_pts, full_part_pts, vis_pts, vis_part_pts = batch

        obj_one = torch.unsqueeze(obj_one, 2)
        part_one = torch.unsqueeze(part_one, 2)

        # encoder part
        full_glf, _ = self.full_ae.encoder(full_pts)
        full_part_glf, _ = self.full_ae.encoder(full_part_pts)

        vis_glf, _ = self.vis_ae.encoder(vis_pts)
        vis_part_glf, _ = self.vis_ae.encoder(vis_part_pts)

        full_feature = torch.cat((obj_one, full_glf, part_one, full_part_glf), dim=1)
        vis_feature = torch.cat((obj_one, vis_glf, part_one, vis_part_glf), dim=1)

        full_recons = self.full_ae.decoder(full_feature)
        vis_recons = self.vis_ae.decoder(vis_feature)

        print(full_recons.shape)

        # full_recons[:,:, 0] = [0]

        # cd loss only cam frame point
        full_loss, _, _ = chamfer_loss(full_recons, full_part_pts)
        part_loss, _, _ = chamfer_loss(vis_recons, vis_part_pts)

        # association network
        # pred_glf = self.fc_p2f(torch.squeeze(part_glf_label))
        # pred_full_label = self.full_class(pred_glf)
        # full_label_loss = self.criterion(pred_full_label, label)
        #
        # pred_full_glf = torch.unsqueeze(pred_glf, 2)
        # glf_loss = F.mse_loss(pred_full_glf, full_glf)
        # pred_full_glf = torch.cat((pred_full_glf, pred_label), dim=1)
        #
        # p2r_output = self.full_ae.decoder(pred_full_glf)
        # p2f_result = torch.cat((p2r_output[0], p2r_output[1]), dim=1)
        # p2f_loss, _, _ = chamfer_loss6(p2f_result, full_obj_pts)

        return {
            # AE Reconstruction Loss
            'full_cd': full_loss,
            'part_cd': part_loss,

            # # Association GLF Loss
            # 'p2f_glf_loss': glf_loss,
            #
            # # Association Reconstruction Loss
            # 'p2f_cd': p2f_loss,
            #
            # # Label Classification Loss
            # 'label_loss': label_loss,
            # 'label_full_loss': full_label_loss
        }

    def training_step(self, batch, batch_idx):
        loss_dict = self.common_step(batch)

        # log
        self.log('train_full_cd', loss_dict['full_cd'])
        self.log('train_part_cd', loss_dict['part_cd'])
        # self.log('train_glf_loss', loss_dict['p2f_glf_loss'])
        # self.log('train_p2f_cd', loss_dict['p2f_cd'])
        # self.log('train_label_loss', loss_dict['label_loss'])
        # self.log('train_label_full_loss', loss_dict['label_full_loss'])

        # loss = loss_dict['full_cd'] + loss_dict['part_cd'] + loss_dict['p2f_glf_loss'] + loss_dict['p2f_cd'] + \
        #        loss_dict['label_loss'] + loss_dict['label_full_loss']

        loss = loss_dict['full_cd'] + loss_dict['part_cd']

        return loss

    def validation_step(self, batch, batch_idx):
        loss_dict = self.common_step(batch)

        # log
        self.log('val_full_cd', loss_dict['full_cd'])
        self.log('val_part_cd', loss_dict['part_cd'])
        # self.log('val_glf_loss', loss_dict['p2f_glf_loss'])
        # self.log('val_p2f_cd', loss_dict['p2f_cd'])
        # self.log('val_label_loss', loss_dict['label_loss'])
        # self.log('val_label_full_loss', loss_dict['label_full_loss'])

        # loss = loss_dict['full_cd'] + loss_dict['part_cd'] + loss_dict['p2f_glf_loss'] + loss_dict['p2f_cd'] + \
        #        loss_dict['label_loss'] + loss_dict['label_full_loss']

        loss = loss_dict['full_cd'] + loss_dict['part_cd']

        return loss

    def configure_optimizers(self):
        lr = self.hparams.lr

        params = self.vis_ae.get_parameter() + self.full_ae.get_parameter()

        opt1 = opt.AdamP(
            params,
            lr=lr,
            weight_decay=1e-2,
        )

        return [opt1, ], []


class PartialRemainNet3(LightningModule):
    def __init__(
            self,
            args: dict,
            lr: float = 1e-4,
            b1: float = 0.5,
            b2: float = 0.999,
    ):
        super().__init__()

        self.save_hyperparameters()

        remain_args = deepcopy(args)
        part_args = deepcopy(args)

        remain_args['parameter']['num_points'] = 4096
        part_args['parameter']['num_points'] = 2048

        # part_args['model']['encoder'] = 'point'
        part_args['model']['decoder'] = 'point'

        self.full_ae = ReconstructionNet(remain_args, feat_dims=args['group']['remain_ae'] + 13,
                                         seg_class=3, ch=42)

        self.part_ae = ReconstructionNet(part_args, feat_dims=args['group']['part_ae'] + 13,
                                         ch=12)

        self.fc_p2f = build_association()

        self.args = args

    @staticmethod
    def add_argparse_args(parent_parser: ArgumentParser):
        parser = ArgumentParser(parents=[parent_parser], add_help=False)
        parser.add_argument("--lr", type=float, default=1e-4, help="adam: learning rate")
        parser.add_argument("--b1", type=float, default=0.5,
                            help="adam: decay of first order momentum of gradient")
        parser.add_argument("--b2", type=float, default=0.999,
                            help="adam: decay of second order momentum of gradient")

        return parser

    def forward(self, pts):
        part_glf = self.part_ae.encoder(pts)
        full_glf = self.fc_p2f(part_glf)
        full_pts = self.full_ae.decoder(full_glf)

        return full_pts

    def common_step(self, batch):
        full_gt, part_gt, obj_gt, label = batch

        full_obj_gt = torch.cat((full_gt, obj_gt), dim=1)

        # camera frame
        # full + xyz
        full_output, full_glf, _ = self.full_ae.forward_glf(full_obj_gt, label, 1)
        part_recons, part_glf, _ = self.part_ae.forward_glf(part_gt, label, 1)

        full_result = torch.cat((full_output[0], full_output[1]), dim=1)

        # cd loss only cam frame point
        full_loss, _, _ = chamfer_loss6(full_result, full_obj_gt)
        part_loss = mse_loss(part_recons, part_gt)

        # association network
        # occ to part
        part_glf_label = torch.cat((part_glf, label), dim=1)

        # part to remain
        pred_full_glf = torch.unsqueeze(self.fc_p2f(torch.squeeze(part_glf_label)), 2)
        p2f_glf_loss = F.mse_loss(pred_full_glf, full_glf)
        pred_full_glf = torch.cat((pred_full_glf, label), dim=1)

        p2f_output = self.full_ae.decoder(pred_full_glf)
        p2f_result = torch.cat((p2f_output[0], p2f_output[1]), dim=1)

        p2f_loss, _, _ = chamfer_loss6(p2f_result, full_obj_gt)
        # p2f_cam_loss, _, _ = chamfer_loss(p2f_output[0], full_gt)

        return {
            # AE Reconstruction Loss
            'full_cd': full_loss,
            # 'cam_cd': cam_loss,
            'part_cd': part_loss,

            # Association GLF Loss
            'p2f_glf_loss': p2f_glf_loss,

            # Association Reconstruction Loss
            'p2f_cd': p2f_loss,
            # 'p2f_cam_cd': p2f_cam_loss
        }

    def training_step(self, batch, batch_idx):
        loss_dict = self.common_step(batch)

        # log
        self.log('train_full_cd', loss_dict['full_cd'])
        # self.log('train_cam_cd', loss_dict['cam_cd'])
        self.log('train_part_cd', loss_dict['part_cd'])

        self.log('train_p2f_glf_loss', loss_dict['p2f_glf_loss'])
        self.log('train_p2f_cd', loss_dict['p2f_cd'])
        # self.log('train_p2f_cam_cd', loss_dict['p2f_cam_cd'])

        loss = (loss_dict['full_cd'] + loss_dict['part_cd']  # + loss_dict['cam_cd']
                + loss_dict['p2f_glf_loss'] + loss_dict['p2f_cd']  # + loss_dict['p2f_cam_cd']
                )

        return loss

    def validation_step(self, batch, batch_idx):
        loss_dict = self.common_step(batch)

        # log
        self.log('val_full_cd', loss_dict['full_cd'])
        self.log('val_part_cd', loss_dict['part_cd'])

        self.log('val_p2f_glf_loss', loss_dict['p2f_glf_loss'])
        self.log('val_p2f_cd', loss_dict['p2f_cd'])
        # self.log('val_p2f_cam_cd', loss_dict['p2f_cam_cd'])

        loss = (loss_dict['full_cd'] + loss_dict['part_cd']  # + loss_dict['cam_cd']
                + loss_dict['p2f_glf_loss'] + loss_dict['p2f_cd']  # + loss_dict['p2f_cam_cd']
                )

        return loss

    def configure_optimizers(self):
        lr = self.hparams.lr

        params = (self.part_ae.get_parameter() + self.full_ae.get_parameter()
                  + list(self.fc_p2f.parameters()))

        opt1 = opt.AdamP(
            params,
            lr=lr,
            weight_decay=1e-2,
        )

        return [opt1, ], []
