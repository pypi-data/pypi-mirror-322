import numpy as np
from pyod.models.knn import KNN
import torch

def find_pixels(image, col_id):
    red_pixels = np.where((image[:, :, 0] == col_id))
    return list(zip(red_pixels[0], red_pixels[1]))


def remove_outlier(points):
    clf = KNN(n_neighbors=50)

    clf.fit(points)
    y_train_scores = clf.decision_scores_  # raw outlier scores

    remove_idx = np.where(y_train_scores > 0.05)[0]
    points = np.delete(points, remove_idx, axis=0)

    return points

def rigid_transform_3D(A, B):
    A = A.T
    B = B.T
    assert A.shape == B.shape

    num_rows, num_cols = A.shape
    if num_rows != 3:
        raise Exception(f"matrix A is not 3xN, it is {num_rows}x{num_cols}")

    num_rows, num_cols = B.shape
    if num_rows != 3:
        raise Exception(f"matrix B is not 3xN, it is {num_rows}x{num_cols}")

    # find mean column wise
    centroid_A = np.mean(A, axis=1)
    centroid_B = np.mean(B, axis=1)

    # ensure centroids are 3x1
    centroid_A = centroid_A.reshape(-1, 1)
    centroid_B = centroid_B.reshape(-1, 1)

    # subtract mean
    Am = A - centroid_A
    Bm = B - centroid_B

    H = Am @ np.transpose(Bm)

    # sanity check
    # if linalg.matrix_rank(H) < 3:
    #    raise ValueError("rank of H = {}, expecting 3".format(linalg.matrix_rank(H)))

    # find rotation
    U, S, Vt = np.linalg.svd(H)
    R = Vt.T @ U.T

    # special reflection case
    if np.linalg.det(R) < 0:
        print("det(R) < R, reflection detected!, correcting for it ...")
        Vt[2, :] *= -1
        R = Vt.T @ U.T

    t = -R @ centroid_A + centroid_B

    return R, t


def to_point_numpy(data):
    data = torch.transpose(data, 1, 2)
    return data.cpu().detach().numpy()
