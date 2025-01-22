import os
from copy import deepcopy
from typing import Union, Optional
import numpy as np
from numba import cuda
import math

from simba.utils.checks import check_file_exist_and_readable, check_if_dir_exists
from simba.utils.read_write import get_video_meta_data, read_df, read_img_batch_from_video_gpu
from simba.utils.errors import FrameRangeError
from simba.mixins.plotting_mixin import PlottingMixin
from simba.utils.data import create_color_palette

import cv2

# @cuda.jit(device=True)
# def find_pixels_within_euclidean(x0, y0, distance):
#     points =  cuda.local.array(shape=(512,), dtype=np.float32)
#     cnt = 0
#     for x1 in range(x0-distance[0], x0+distance[0]):
#         for y1 in range(y0-distance[0], y0+distance[0]):
#             b, c = (x1 - x0) ** 2, (y1 - y0) ** 2
#             if (b + c) <= distance[0] ** 2:
#                 points[cnt] = x1
#                 points[cnt][1] = y1
#                 cnt+=1
#     return points


@cuda.jit(max_registers=None)
def _pose_plot_kernel(imgs, data, circle_size, resolution, colors, results):
    bp_n, img_n = cuda.grid(2)
    if img_n < 0 or img_n > (imgs.shape[0] -1):
        return
    if bp_n < 0 or bp_n > (data[0].shape[0] -1):
        return

    img, bp_loc, color  = imgs[img_n], data[img_n][bp_n], colors[bp_n]
    # points =  cuda.local.array(shape=(1024,2), dtype=np.int32)
    # cnt = 0
    if bp_n == 8:
        print(bp_n, bp_loc[0], bp_loc[1])
    for blah in range(bp_loc[0]-circle_size[0], bp_loc[1]+circle_size[0]):
        if bp_n == 8:
            print(blah, bp_n, img_n)
    #     for y1 in range(bp_loc[1]-circle_size[0], bp_loc[1]+circle_size[0]):
    #         if (x1 > 0) and (x1 < resolution[0]):
    #             if (y1 > 0) and (y1 < resolution[1]):
    #
    #                 pass
    # print(x1, y1, bp_n, img_n)





    #         if (x1 > 0): points[cnt][0] = x1
    #         if (y1 > 0): points[cnt][1] = y1
    #         cnt += 1
    # cuda.syncthreads()
    # for point in points:
    #     if point[0] != 0 and point[1] != 0:
    #         results[n][point[0]][point[1]][0] = int(color[0])
    #         results[n][point[0]][point[1]][1] = int(color[1])
    #         results[n][point[0]][point[1]][2] = int(color[2])
   # print(n)





    #_ = find_pixels_within_euclidean(bp_loc[0], bp_loc[1], circle_size)
    # for px in pxls:
    #     print(px[0])




    #print(bp_loc[0], bp_loc[1])
    # for frame_bp in range(frame_pose.shape[0]):
    #     print(frame_pose[frame_bp][0])
    #
    #
    #
    #     pass


def pose_plotting(data: Union[str, os.PathLike, np.ndarray],
                  video_path: Union[str, os.PathLike],
                  save_path: Union[str, os.PathLike],
                  circle_size: Optional[int] = None,
                  colors: Optional[str] = 'Set1',
                  batch_size: int = int(0.001e+3)) -> None:

    THREADS_PER_BLOCK = (32, 32, 1)

    if isinstance(data, str):
        check_file_exist_and_readable(file_path=data)
        df = read_df(file_path=data, file_type='csv')
        cols = [x for x in df.columns if not x.lower().endswith('_p')]
        data = df[cols].values
        data = data.reshape(data.shape[0], int(data.shape[1] / 2), 2).astype(np.int32)

    video_meta_data = get_video_meta_data(video_path=video_path)
    n, w, h = video_meta_data['frame_count'], video_meta_data['width'], video_meta_data['height']
    check_if_dir_exists(in_dir=os.path.dirname(save_path))
    if data.shape[0] != video_meta_data['frame_count']:
        raise FrameRangeError(msg=f'The data contains {data.shape[0]} frames while the video contains {video_meta_data["frame_count"]} frames')

    if circle_size is None:
        circle_size = np.array([PlottingMixin().get_optimal_circle_size(frame_size=(w, h))]).astype(np.int32)
    else:
        circle_size = np.array([circle_size]).astype(np.int32)

    colors = np.array(create_color_palette(pallete_name=colors, increments=data[0].shape[0])).astype(np.int32)
    circle_size_dev = cuda.to_device(circle_size)
    colors_dev = cuda.to_device(colors)

    data = data[0:1]
    #print(data[0][8])

    resolution_dev = cuda.to_device(np.array([video_meta_data['width'], video_meta_data['height']]))
    for batch_cnt, l in enumerate(range(0, data.shape[0], batch_size)):
        r = min(data.shape[0], l + batch_size - 1)
        batch_data = np.ascontiguousarray(data[l:r + 1])
        batch_frms = read_img_batch_from_video_gpu(video_path=video_path, start_frm=l, end_frm=r, out_format='array').astype(np.int32)
        results = deepcopy(batch_frms)
        #results = cuda.device_array(batch_frms.shape, dtype=np.int32)
        results_dev = cuda.to_device(results)
        batch_n = batch_data.shape[0]
        grid_x = math.ceil(batch_frms.shape[0] / THREADS_PER_BLOCK[0])
        grid_z = math.ceil(batch_n / THREADS_PER_BLOCK[2])
        bpg = (grid_x, grid_z)
        img_dev = cuda.to_device(batch_frms)
        data_dev = cuda.to_device(batch_data)
    # #
    # #
        _pose_plot_kernel[bpg, THREADS_PER_BLOCK](img_dev, data_dev, circle_size_dev, resolution_dev, colors_dev, results_dev)
    #     results = results_dev.copy_to_host()
    #     cv2.imwrite('/mnt/c/troubleshooting/mitra/project_folder/frames/output/pose_ex/test.png', results[0].astype(np.uint8))
    # #
    #
    #
    #
    #
        #break


DATA_PATH = "/mnt/c/troubleshooting/mitra/project_folder/csv/outlier_corrected_movement_location/501_MA142_Gi_CNO_0514.csv"
VIDEO_PATH = "/mnt/c/troubleshooting/mitra/project_folder/videos/501_MA142_Gi_CNO_0514.mp4"
SAVE_PATH = "/mnt/c/troubleshooting/mitra/project_folder/frames/output/pose_ex/test.mp4"
CIRCLE_SIZE = np.array([50])


pose_plotting(data=DATA_PATH, video_path=VIDEO_PATH, save_path=SAVE_PATH, circle_size=5)




