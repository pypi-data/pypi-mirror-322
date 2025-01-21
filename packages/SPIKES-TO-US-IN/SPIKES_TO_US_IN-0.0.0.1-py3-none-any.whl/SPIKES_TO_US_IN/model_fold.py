import itertools

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from model_point import BiasLayer


# reference
# https://github.com/AnTao97/UnsupervisedPointCloudReconstruction/blob/b5896942c8/model.py

def local_maxpool(x, idx):
    batch_size = x.size(0)
    num_points = x.size(2)
    x = x.view(batch_size, -1, num_points)

    _, num_dims, _ = x.size()

    x = x.transpose(2, 1).contiguous()  # (batch_size, num_points, num_dims)
    x = x.view(batch_size * num_points, -1)[idx, :]  # (batch_size*n, num_dims) -> (batch_size*n*k, num_dims)
    x = x.view(batch_size, num_points, -1, num_dims)  # (batch_size, num_points, k, num_dims)
    x, _ = torch.max(x, dim=2)  # (batch_size, num_points, num_dims)

    return x


class FoldEncoder(nn.Module):
    def __init__(self, args, ch):
        super(FoldEncoder, self).__init__()

        argument = args['argument']

        if 'k' in argument.keys():
            self.k = argument['k']
        else:
            self.k = 16

        self.mlp1 = nn.Sequential(
            nn.Conv1d(ch, 64, 1),
            nn.ReLU(),
            nn.Conv1d(64, 64, 1),
            nn.ReLU(),
            nn.Conv1d(64, 64, 1),
            nn.ReLU(),
        )
        self.linear1 = nn.Linear(64, 64)
        self.conv1 = nn.Conv1d(64, 128, 1)
        self.linear2 = nn.Linear(128, 128)
        self.conv2 = nn.Conv1d(128, 256, 1)
        self.conv3 = nn.Conv1d(256, 64, 1)

        self.mlp2 = nn.Sequential(
            nn.Conv1d(256, 512, 1),
            nn.ReLU(),
            nn.Conv1d(512, 512, 1),
        )

    def graph_layer(self, x, idx):
        x = local_maxpool(x, idx)
        x = self.linear1(x)
        x = x.transpose(2, 1)
        x = F.relu(self.conv1(x))
        x = local_maxpool(x, idx)
        x = self.linear2(x)
        x = x.transpose(2, 1)
        x = self.conv2(x)
        return x

    def forward(self, pts, option=0):
        idx = knn(pts, k=self.k)
        x = local_cov(pts, idx)  # (batch_size, 3, num_points) -> (batch_size, 12, num_points])
        local_feature = self.mlp1(x)  # (batch_size, 12, num_points) -> (batch_size, 64, num_points])
        enc_result = self.graph_layer(local_feature,
                                      idx)  # (batch_size, 64, num_points) -> (batch_size, 1024, num_points)
        x = torch.max(enc_result, 2, keepdim=True)[0]  # (batch_size, 1024, num_points) -> (batch_size, 1024, 1)
        x = self    .mlp2(x)  # (batch_size, 1024, 1) -> (batch_size, feat_dims, 1)

        if option == 0:
            return x, local_feature  # (batch_size, feat_dims, 1), (batch_size, 64, num_points)
        else:
            return x, local_feature, enc_result


def knn(x, k):
    batch_size = x.size(0)
    num_points = x.size(2)

    inner = -2 * torch.matmul(x.transpose(2, 1), x)
    xx = torch.sum(x ** 2, dim=1, keepdim=True)
    pairwise_distance = -xx - inner - xx.transpose(2, 1)

    idx = pairwise_distance.topk(k=k, dim=-1)[1]  # (batch_size, num_points, k)

    if idx.get_device() == -1:
        idx_base = torch.arange(0, batch_size).view(-1, 1, 1) * num_points
    else:
        idx_base = torch.arange(0, batch_size, device=idx.get_device()).view(-1, 1, 1) * num_points
    idx = idx + idx_base
    idx = idx.view(-1)

    return idx


def local_cov(pts, idx):
    batch_size = pts.size(0)
    num_points = pts.size(2)
    pts = pts.view(batch_size, -1, num_points)  # (batch_size, 3, num_points)

    _, num_dims, _ = pts.size()

    x = pts.transpose(2, 1).contiguous()  # (batch_size, num_points, 3)
    x = x.view(batch_size * num_points, -1)[idx, :]  # (batch_size*num_points*2, 3)
    x = x.view(batch_size, num_points, -1, num_dims)  # (batch_size, num_points, k, 3)

    x = torch.matmul(x[:, :, 0].unsqueeze(3), x[:, :, 1].unsqueeze(
        2))  # (batch_size, num_points, 3, 1) * (batch_size, num_points, 1, 3) -> (batch_size, num_points, 3, 3)
    # x = torch.matmul(x[:,:,1:].transpose(3, 2), x[:,:,1:])
    x = x.view(batch_size, num_points, -1).transpose(2, 1)  # (batch_size, 9, num_points)

    x = torch.cat((pts, x), dim=1)  # (batch_size, 12, num_points)

    return x


class FoldDecoder(nn.Module):
    def __init__(self, args, seg_class=0):
        super(FoldDecoder, self).__init__()

        argument = args['argument']

        self.seg_class = seg_class
        self.m = 2025  # 45 * 45.
        self.shape = argument['shape']
        self.meshgrid = [[-0.3, 0.3, 45], [-0.3, 0.3, 45]]
        self.sphere = np.load("grid_npy/sphere.npy")
        self.gaussian = np.load("grid_npy/gaussian.npy")
        if self.shape == 'plane':
            self.folding1 = nn.Sequential(
                nn.Conv1d(argument['feat_dims'] + 2, argument['feat_dims'], 1),
                nn.ReLU(),
                nn.Conv1d(argument['feat_dims'], argument['feat_dims'], 1),
                nn.ReLU(),
                nn.Conv1d(argument['feat_dims'], 3, 1),
            )
        else:
            self.folding1 = nn.Sequential(
                nn.Conv1d(argument['feat_dims'] + 3, argument['feat_dims'], 1),
                nn.ReLU(),
                nn.Conv1d(argument['feat_dims'], argument['feat_dims'], 1),
                nn.ReLU(),
                nn.Conv1d(argument['feat_dims'], 3, 1),
            )
        self.folding2 = nn.Sequential(
            nn.Conv1d(argument['feat_dims'] + 3, argument['feat_dims'], 1),
            nn.ReLU(),
            nn.Conv1d(argument['feat_dims'], argument['feat_dims'], 1),
            nn.ReLU(),
            nn.Conv1d(argument['feat_dims'], 3 + seg_class, 1),
        )

    def build_grid(self, batch_size):
        if self.shape == 'plane':
            x = np.linspace(*self.meshgrid[0])
            y = np.linspace(*self.meshgrid[1])
            points = np.array(list(itertools.product(x, y)))
        elif self.shape == 'sphere':
            points = self.sphere
        elif self.shape == 'gaussian':
            points = self.gaussian
        points = np.repeat(points[np.newaxis, ...], repeats=batch_size, axis=0)
        points = torch.tensor(points)
        return points.float()

    def forward(self, x):
        x = x.repeat(1, 1, self.m)  # (batch_size, feat_dims, num_points)
        points = self.build_grid(x.shape[0]).transpose(1,
                                                       2)  # (batch_size, 2, num_points) or (batch_size, 3, num_points)
        if x.get_device() != -1:
            points = points.cuda(x.get_device())
        cat1 = torch.cat((x, points),
                         dim=1)  # (batch_size, feat_dims+2, num_points) or (batch_size, feat_dims+3, num_points)
        folding_result1 = self.folding1(cat1)  # (batch_size, 3, num_points)
        cat2 = torch.cat((x, folding_result1), dim=1)  # (batch_size, 515, num_points)
        x = self.folding2(cat2)  # (batch_size, 3, num_points)

        if self.seg_class == 0:
            return x
        else:
            recons = x[:, :3, :]
            seg = x[:, 3:, :].transpose(2, 1)
            seg = F.log_softmax(seg, dim=-1)

            return recons, seg


class FoldBiasDecoder(nn.Module):
    def __init__(self, args, seg_class=0):
        super(FoldBiasDecoder, self).__init__()

        argument = args['argument']

        self.seg_class = seg_class
        self.m = 2025  # args['parameter']['num_points']  # 45 * 45.
        self.shape = argument['shape']
        self.meshgrid = [[-0.3, 0.3, 45], [-0.3, 0.3, 45]]

        self.folding1 = nn.Sequential(
            nn.Conv1d(argument['feat_dims'] + 2, argument['feat_dims'], 1, bias=False),
            BiasLayer(argument['feat_dims'], self.m),
            nn.ReLU(),
            nn.Conv1d(argument['feat_dims'], argument['feat_dims'], 1, bias=False),
            BiasLayer(argument['feat_dims'], self.m),
            nn.ReLU(),
            nn.Conv1d(argument['feat_dims'], 3, 1, bias=False),
            BiasLayer(3, self.m),
        )

        self.folding2 = nn.Sequential(
            nn.Conv1d(argument['feat_dims'] + 3, argument['feat_dims'], 1, bias=False),
            BiasLayer(argument['feat_dims'], self.m),
            nn.ReLU(),
            nn.Conv1d(argument['feat_dims'], argument['feat_dims'], 1, bias=False),
            BiasLayer(argument['feat_dims'], self.m),
            nn.ReLU(),
            nn.Conv1d(argument['feat_dims'], 3 + seg_class, 1, bias=False),
            BiasLayer(3 + seg_class, self.m),
        )

    def build_grid(self, batch_size):
        if self.shape == 'plane':
            x = np.linspace(*self.meshgrid[0])
            y = np.linspace(*self.meshgrid[1])
            points = np.array(list(itertools.product(x, y)))
        elif self.shape == 'sphere':
            points = self.sphere
        elif self.shape == 'gaussian':
            points = self.gaussian
        points = np.repeat(points[np.newaxis, ...], repeats=batch_size, axis=0)
        points = torch.tensor(points)
        return points.float()

    def forward(self, x):
        x = x.repeat(1, 1, self.m)  # (batch_size, feat_dims, num_points)
        points = self.build_grid(x.shape[0]).transpose(1,
                                                       2)  # (batch_size, 2, num_points) or (batch_size, 3, num_points)
        if x.get_device() != -1:
            points = points.cuda(x.get_device())
        cat1 = torch.cat((x, points),
                         dim=1)  # (batch_size, feat_dims+2, num_points) or (batch_size, feat_dims+3, num_points)
        folding_result1 = self.folding1(cat1)  # (batch_size, 3, num_points)
        cat2 = torch.cat((x, folding_result1), dim=1)  # (batch_size, 515, num_points)
        x = self.folding2(cat2)  # (batch_size, 3, num_points)

        if self.seg_class == 0:
            return x
        else:
            recons = x[:, :3, :]
            seg = x[:, 3:, :].transpose(2, 1)
            seg = F.log_softmax(seg, dim=-1)

            return recons, seg
