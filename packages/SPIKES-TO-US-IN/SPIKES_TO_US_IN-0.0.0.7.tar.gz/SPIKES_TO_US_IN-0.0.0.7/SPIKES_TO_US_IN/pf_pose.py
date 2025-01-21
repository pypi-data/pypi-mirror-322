'''
    2023.12.07. EdgeBrain2 Panoptic Segmentation System from Lee Soojin
    1. YOLO: Objects detection in Scene Image
    2. YOLACT: Objects Segmentation of cropped images from YOLO
    3. YOLACT_Part: Part segmentation of Box, Pincers class
'''

import os
from sys import argv
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from .model import PartialRemainNet3


from .util_code import find_pixels, remove_outlier, rigid_transform_3D, to_point_numpy
from .point_util import view_pcd
import open3d as o3d
from copy import deepcopy
from glob import glob
# import zivid
import tkinter

_width = 3840
_height = 1400
_CLASS_LABEL = ['_background_', '01 Cat toy', '02 Can', '03 Coffee', '04 Cup Noodle', '05 Ketchup', '06 Milk',
                '07 Mouse', '08 Mug',
                '09 Plastic Cup', '10 Sweets Box', '11 Watering Can', '12 Pincers', '16 Tissue', '17 Box',
                '22 Eyeglasses Cloth Pouch']
_PART_CLASS_LABEL = ['_background_', '19 Box Body', '18 Box Wing', '20 Pincers Handle', '21 Pincers Head']
_PART_OBJ_LABEL = [-1, 14, 14, 12, 12]
p2f_class_names = ['', 'cat', 'can', 'coffee', 'cupnoodle', 'ketchup', 'milk', 'mouse', 'mug',
                   'plasticCup', 'sweetsbox', 'watering', 'pincers', 'tissue', 'box', 'glassescleaner']
COLUMNS = ['Trial number', 'Ground Truth Class', 'GT x', 'GT y', 'GT rot', 'Prediction Class', 'ADD']

_CLASS_COLOR = [[255, 255, 255], [255, 0, 0], [0, 255, 0], [150, 5, 61], [255, 0, 255], [31, 120, 230],
                [180, 230, 61], [255, 255, 0], [29, 190, 255], [5, 150, 61], [123, 12, 53], [135, 180, 0],
                [255, 0, 0], [0, 0, 255], [98, 6, 129], [199, 183, 0], [230, 23, 18], [9, 78, 11]]
_TEXT_COLOR = [[255, 255, 255], [255, 255, 255], [0, 0, 0], [255, 255, 255], [255, 255, 255], [0, 0, 0],
               [0, 0, 0], [0, 0, 0], [0, 0, 0], [255, 255, 255], [255, 255, 255], [0, 0, 0],
               [255, 255, 255], [255, 255, 255], [255, 255, 255], [0, 0, 0], [255, 255, 255], [255, 255, 255]]

checkboard_pose = np.array([[ 9.99231100e-01,  2.22457685e-02, -3.22853699e-02, -4.77271461],
                             [ 1.33444555e-02,  5.81323564e-01,  8.13563049e-01, -5.18204842],
                             [ 3.68665792e-02, -8.13368320e-01,  5.80579698e-01,  6.92002075e+01],
                             [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]])



device = 'cuda' if torch.cuda.is_available() else 'cpu'
window = tkinter.Tk()
window.geometry("640x400+100+100")
window.resizable(False, False)
camera = None

def init_models(weight_path):
    global p2f_model

    p2f_model = PartialRemainNet3.load_from_checkpoint(weight_path)
    p2f_model.eval()
    p2f_model.to(device)

def run(pts_path,weight_path):

    init_models(weight_path)
    pts2 = np.load(pts_path)

    sem_id = int(pts_path.split('.')[0].split('/')[-1])

    # view_pcd(pts2)
    pts2 = remove_outlier(pts2)
    # view_pcd(pts2)

    # Point Cloud 중에서 2048개를 random sampling
    obj_sample_idx = np.random.choice(np.arange(len(pts2)), 2048)
    result_pts = pts2[obj_sample_idx]

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(result_pts)
    center = pcd.get_center()
    partial_pcd = deepcopy(pcd)
    partial_pcd.paint_uniform_color((0, 1, 1))

    # o3d.visualization.draw_geometries([partial_pcd])

    pcd.translate(-center)  # center로 이동

    partial_pts = np.array(pcd.points)

    # Partial Point Cloud의 diameter 로 scale함
    norm_pts = partial_pts

    norm_pt_arr = []
    norm_pt_arr.append(norm_pts)

    obj_id = sem_id
    # print(obj_id)
    obj_id_ = sem_id
    if obj_id_ == 1:
        obj_id_ = 0
    if obj_id_ == 2:
        obj_id_ = 1
    if obj_id_ == 3:
        obj_id_ = 2
    # print("changed ", obj_id_)
    # label 생성 및 Point Cloud 변환
    non_outlier_pts_arr = np.array(norm_pt_arr)
    label_one_hot = np.zeros(13, dtype=np.float32)
    label_one_hot[obj_id_] = 1

    partial_input_pts = torch.from_numpy(np.array(non_outlier_pts_arr, dtype=np.float32))
    partial_input_pts = partial_input_pts.transpose(1, 2).to(device)

    label_batch = torch.unsqueeze(torch.from_numpy(np.array([label_one_hot])), -1).to(device)

    # 파셜 포인트 클라우드의 피쳐 뽑기
    # print(partial_input_pts.shape, label_batch.shape)
    part_recons, part_glf, _ = p2f_model.part_ae.forward_glf(partial_input_pts, label_batch, 1)
    part_glf_label = torch.cat((part_glf, label_batch), dim=1)

    # part to remain
    pred_full_glf = torch.unsqueeze(p2f_model.fc_p2f(torch.squeeze(part_glf_label, 2)), 2)
    pred_full_glf = torch.cat((pred_full_glf, label_batch), dim=1)

    p2f_output = p2f_model.full_ae.decoder(pred_full_glf)

    # 생성된 Point Cloud 를 Full model 의 diameter로 다시 scale 을 풀어줌
    cam_pts = to_point_numpy(p2f_output[0])[0]
    obj_pts = to_point_numpy(p2f_output[1])[0]

    cam_pcd = o3d.geometry.PointCloud()
    cam_pcd.points = o3d.utility.Vector3dVector(cam_pts)
    cam_pcd = cam_pcd.translate(center)  # center 정보를 이용하여 초기 위치로 복귀
    cam_pcd.paint_uniform_color((1, 0, 0))
    cam_pts = np.array(cam_pcd.points, dtype=np.float32)

    obj_pcd = o3d.geometry.PointCloud()
    obj_pcd.points = o3d.utility.Vector3dVector(obj_pts)
    obj_pcd.paint_uniform_color((0, 0, 0))

    obj_pts = np.array(obj_pcd.points)


    # Object Frame과 Camera Frame 사이의 Transforma matrix를 구함
    ret_R, ret_t = rigid_transform_3D(obj_pts, cam_pts)
    pred_pose = np.eye(4)
    pred_pose[:3, :3] = ret_R
    pred_pose[:3, 3] = ret_t.flatten() 
    coord_pose = pred_pose

    cam_coord = o3d.geometry.TriangleMesh.create_coordinate_frame(size=1, origin=[0, 0, 0])
    obj_coord = o3d.geometry.TriangleMesh.create_coordinate_frame(size=1, origin=[0, 0, 0])

    obj_coord.transform(coord_pose)
    pcd.translate(center)

    # 3D Visualization
    # o3d.visualization.draw_geometries([scene_pcd, obj_coord, model2_pcd])
    # o3d.visualization.draw_geometries([scene_pcd, obj_coord])
    # o3d.visualization.draw_geometries([pcd, cam_coord, obj_coord])

    return coord_pose





def _main():

    init_models()

    button = tkinter.Button(window, overrelief="solid", text='Pose Estimation', width=30, height=30, command=run)
    button.pack()

    window.mainloop()


if __name__ == '__main__':
    _main()
