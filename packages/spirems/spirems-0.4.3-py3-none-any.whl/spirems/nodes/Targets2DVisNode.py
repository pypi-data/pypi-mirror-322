#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: renjin@bit.edu.cn
# @Date  : 2025-01-20


import threading
import time
import cv2
import os
import json
import argparse
import numpy as np
from typing import Union
from queue import Queue
from spirems import Publisher, Subscriber, cvimg2sms, sms2cvimg
from spirems.nodes.BaseNode import BaseNode
import base64
try:
    from pycocotools import mask as pycoco_mask
except:
    pass


class Colors:
    def __init__(self):
        hexs = ('FF3838', 'FF9D97', 'FF701F', 'FFB21D', 'CFD231', '48F90A',
                '92CC17', '3DDB86', '1A9334', '00D4BB', '2C99A8', '00C2FF',
                '344593', '6473FF', '0018EC', '8438FF', '520085', 'CB38FF',
                'FF95C8', 'FF37C7')
        self.palette = [self.hex2rgb(f'#{c}') for c in hexs]
        self.n = len(self.palette)

    def __call__(self, i, bgr=False):
        c = self.palette[int(i) % self.n]
        return (c[2], c[1], c[0]) if bgr else c

    @staticmethod
    def hex2rgb(h):  # rgb order (PIL)
        return tuple(int(h[1 + i:1 + i + 2], 16) for i in (0, 2, 4))


def draw_rotated_box(img, center, size, angle, color=(0, 255, 0), thickness=2):
    """
    在图像上绘制旋转框
    :param img: 输入图像
    :param center: 旋转框中心点 (cx, cy)
    :param size: 旋转框的宽度和高度 (w, h)
    :param angle: 旋转角度（以度为单位，顺时针为正）
    :param color: 框的颜色 (B, G, R)
    :param thickness: 框的线宽
    :return: 绘制了旋转框的图像
    """
    # 获取旋转框的宽度和高度
    width, height = size

    # 计算旋转框的四个角点
    rect = ((center[0], center[1]), (width, height), angle)
    box = cv2.boxPoints(rect)  # 获取旋转框的四个角点
    box = np.int32(box)  # 将角点转换为整数

    # 在图像上绘制旋转框
    cv2.drawContours(img, [box], 0, color, thickness)

    return img


class Targets2DVisNode(threading.Thread, BaseNode):
    def __init__(
        self,
        job_name: str,
        specified_input_topic: str = None,
        ip: str = '127.0.0.1',
        port: int = 9094,
        param_dict_or_file: Union[dict, str] = None,
        sms_shutdown: bool = True,
        imshow: bool = True
    ):
        threading.Thread.__init__(self)
        BaseNode.__init__(
            self,
            self.__class__.__name__,
            job_name,
            ip=ip,
            port=port,
            param_dict_or_file=param_dict_or_file,
            sms_shutdown=sms_shutdown
        )
        input_topic = specified_input_topic if specified_input_topic else '/' + job_name + '/sensor/image_raw'

        self._image_reader = Subscriber(
            input_topic, 'sensor_msgs::CompressedImage', self.image_callback,
            ip=ip, port=port
        )
        self._image_writer = Publisher(
            '/' + job_name + '/detection_vis', 'sensor_msgs::CompressedImage',
            ip=ip, port=port
        )
        self.imshow = imshow

        self.score_threshold = self.get_param("score_threshold", 0.3)
        self.colors_obj = Colors()

        self.image_queue = Queue()
        self.queue_pool.append(self.image_queue)
        self.start()

    def release(self):
        BaseNode.release(self)
        self._image_reader.kill()
        self._image_writer.kill()

    def image_callback(self, msg):
        self.image_queue.put(msg)

    def run(self):
        while self.is_running():
            msg = self.image_queue.get(block=True)
            if msg is None:
                break

            img = sms2cvimg(msg)
            if 'spirecv_msgs::2DTargets' in msg:
                min_siz = min(msg['spirecv_msgs::2DTargets']['height'], msg['spirecv_msgs::2DTargets']['width'])
                if min_siz <= 720:
                    thickness = 1
                elif 720 < min_siz <= 1200:
                    thickness = 1
                else:
                    thickness = 2

                if 'rois' in msg['spirecv_msgs::2DTargets'] and len(msg['spirecv_msgs::2DTargets']['rois']) > 0:
                    roi = msg['spirecv_msgs::2DTargets']['rois'][0]
                    img_roi = img[roi[1]:roi[1] + roi[3], roi[0]:roi[0] + roi[2], :].copy()
                    img = cv2.addWeighted(img, 0.5, np.zeros_like(img, dtype=np.uint8), 0.5, 0)
                    img[roi[1]:roi[1] + roi[3], roi[0]:roi[0] + roi[2], :] = img_roi
                
                masks = []
                result_classid = []
                for obj in msg['spirecv_msgs::2DTargets']['targets']:
                    if 'score' not in obj or obj['score'] >= self.score_threshold:
                        if "segmentation" in obj:
                            obj['segmentation']['counts'] = base64.b64decode(obj['segmentation']['counts'])
                            mask = pycoco_mask.decode(obj['segmentation'])
                            masks.append(mask)
                            result_classid.append(obj['category_id'])

                if len(masks) > 0:
                    alpha = 0.5
                    colors_ = [self.colors_obj(x, True) for x in result_classid]
                    masks = np.asarray(masks, dtype=np.uint8)
                    masks = np.ascontiguousarray(masks.transpose(1, 2, 0))
                    masks = np.asarray(masks, dtype=np.float32)
                    colors_ = np.asarray(colors_, dtype=np.float32)
                    s = masks.sum(2, keepdims=True).clip(0, 1)
                    masks = (masks @ colors_).clip(0, 255)
                    img[:] = masks * alpha + img * (1 - s * alpha)

                for obj in msg['spirecv_msgs::2DTargets']['targets']:
                    if 'obb' in obj:
                        img = draw_rotated_box(
                            img, 
                            (int(round(obj['obb'][0])), int(round(obj['obb'][1]))),
                            (int(round(obj['obb'][2])), int(round(obj['obb'][3]))),
                            obj['obb'][4]
                        )
                    elif 'tracked_id' in obj:
                        cv2.rectangle(
                            img,
                            (int(obj['bbox'][0]), int(obj['bbox'][1])),
                            (int(obj['bbox'][0] + obj['bbox'][2]), int(obj['bbox'][1] + obj['bbox'][3])),
                            (0, 0, 255),
                            thickness,
                            cv2.LINE_AA
                        )
                        cv2.rectangle(
                            img,
                            (int(obj['bbox'][0]), int(obj['bbox'][1])),
                            (int(obj['bbox'][0] + len(str(obj['tracked_id'])) * 12), int(obj['bbox'][1] + 18)),
                            (0, 0, 0),
                            -1,
                            cv2.LINE_AA
                        )
                        cv2.putText(
                            img,
                            str(obj['tracked_id']),
                            (int(obj['bbox'][0]) + 2, int(obj['bbox'][1]) + 15),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (255, 255, 255),
                            1
                        )
                    elif 'score' not in obj or obj['score'] >= self.score_threshold:
                        cv2.rectangle(
                            img,
                            (int(obj['bbox'][0]), int(obj['bbox'][1])),
                            (int(obj['bbox'][0] + obj['bbox'][2]), int(obj['bbox'][1] + obj['bbox'][3])),
                            (0, 0, 255),
                            thickness,
                            cv2.LINE_AA
                        )
                        if obj['bbox'][3] < 50:  # pixel
                            cv2.rectangle(
                                img,
                                (int(obj['bbox'][0]), int(obj['bbox'][1])),
                                (int(obj['bbox'][0] + len(obj['category_name']) * 12), int(obj['bbox'][1] - 18)),
                                (0, 0, 0),
                                -1,
                                cv2.LINE_AA
                            )
                            cv2.putText(
                                img,
                                obj['category_name'],
                                (int(obj['bbox'][0]) + 2, int(obj['bbox'][1]) - 3),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.5,
                                (255, 255, 255),
                                1
                            )
                        else:
                            cv2.rectangle(
                                img,
                                (int(obj['bbox'][0]), int(obj['bbox'][1])),
                                (int(obj['bbox'][0] + len(obj['category_name']) * 12), int(obj['bbox'][1] + 18)),
                                (0, 0, 0),
                                -1,
                                cv2.LINE_AA
                            )
                            cv2.putText(
                                img,
                                obj['category_name'],
                                (int(obj['bbox'][0]) + 2, int(obj['bbox'][1]) + 15),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.5,
                                (255, 255, 255),
                                1
                            )
                        if 'keypoints' in obj:
                            kpt = np.array(obj['keypoints'], np.int32).reshape(-1, 3)
                            for i in range(len(kpt)):
                                cv2.circle(img, (kpt[i, 0], kpt[i, 1]), 2, (0, 0, 255), 2, lineType=cv2.LINE_AA)

                if "fei_cxcy" in msg['spirecv_msgs::2DTargets']:
                    cx = int(msg['spirecv_msgs::2DTargets']['fei_cxcy'][0])
                    cy = int(msg['spirecv_msgs::2DTargets']['fei_cxcy'][1])
                    cv2.circle(img, (cx, cy), 8, (154, 250, 0), 2)

            if self.imshow:
                cv2.imshow('img', img)
                cv2.waitKey(5)
            
            sms_img = cvimg2sms(img)
            self._image_writer.publish(sms_img)

        self.release()
        print('{} quit!'.format(self.__class__.__name__))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input_topic',
        help='SpireCV2 Image Topic')
    parser.add_argument(
        '--show',
        type=int,
        default=1,
        help='Show Detection Results Or NOT')
    parser.add_argument(
        '--job-name',
        type=str,
        default='live',
        help='SpireCV Job Name')
    parser.add_argument(
        '--ip',
        type=str,
        default='127.0.0.1',
        help='SpireMS Core IP')
    parser.add_argument(
        '--port',
        type=int,
        default=9094,
        help='SpireMS Core Port')
    args = parser.parse_args()
    print("input-topic:", args.input_topic)
    print("job-name:", args.job_name)
    im_show = True if args.show == 1 else False
    cam = Targets2DVisNode(args.job_name, specified_input_topic=args.input_topic, imshow=im_show)
    cam.join()


if __name__ == '__main__':
    main()
