# Python 3.8.10
# import matplotlib
# import matplotlib.pyplot as plt
import cv2
import os
import sys
import io
import time
# 场景文字检测 https://github.com/breezedeus/CnSTD
# 安装和启动server https://cnocr.readthedocs.io/zh/latest/install/
from cnstd import CnStd
from cnocr import CnOcr
# print 中文乱码问标题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

# 秒 2 时分秒
def deal_duration(duration: int) -> str:
    """
    处理时长 example: 90 --> 00:01:30
    :param duration: int 时长 单位s
    :return: str '00:01:30'
    """
    return time.strftime('%H:%M:%S', time.gmtime(duration))

# ret = deal_duration(3662)
# print(ret)

def video_to_frames(video_path, outPutDirName):
    # 初始化场景文字检测
    std = CnStd()
    cn_ocr = CnOcr()
    # 秒
    second = 0
    # 帧
    times = 0
    frame_frequency = 0
    # 检测路径没有则创建
    if not os.path.exists(outPutDirName):
        os.makedirs(outPutDirName)
    
    camera = cv2.VideoCapture(video_path)
    # 获取视频每秒帧率，每多少帧为1秒
    frame_frequency = int(camera.get(5))
    
    print('开始提取文字')
    # 提取文本容器
    text_list = []
    while True:
        times = times + 1
        res, image = camera.read()
        if not res:
            print('not res, not image')
            break
        if times % frame_frequency == 0:
            # cv2.imwrite(outPutDirName + '\\' + str(times)+'.jpg', image)
            # 秒计数
            second = second + 1
            # 每张图片的文本容器
            item_list = []
            # 检测图片的文字位置列表
            box_infos = std.detect(image)
            for box_info in box_infos['detected_texts']:
                cropped_img = box_info['cropped_img']
                # 识别指定位置的文本
                ocr_res = cn_ocr.ocr_for_single_line(cropped_img)
                # 识别指定位置的文本
                item_list.append(ocr_res['text'])
                # print('ocr result: %s' % str(ocr_res))
            # 如果识别得到文本的话打印时间
            if len(item_list):
                time_str = deal_duration(second)
                item_list.append(time_str)
                sys.stdout.write("\r")
                sys.stdout.write(time_str)
                sys.stdout.flush()
                # print(time_str, flush=True)
            # 检测前后的文本是否一致,一致去重
            is_same = 0
            if len(item_list) and len(text_list) and len(item_list) == len(text_list[-1]):
                for item_index, item_val,  in enumerate(text_list[-1]):
                    if item_list[item_index] == item_val:
                        is_same = is_same + 1
            # 小于两个一致的保存
            if is_same < 2:
                text_list.append(item_list)
                # print(item_list)
    print('图片提取完毕')
    camera.release()
    # 提取写入文件
    f = open('1.txt', mode='r+', encoding='utf-8')
    for item_val in text_list:
        # print(item_val)
        f.write(' '.join(item_val))
        f.write('\n')
    f.close()
    print('写入完毕')


video_to_frames("D:\\download\\sucheng_zexue.mp4", 
"D:\\software\\Python\\Project\\ship_handle\\imgs")

# img_path = './imgs/1820.jpg'
# std = CnStd()
# cn_ocr = CnOcr()
# box_infos = std.detect(img_path)
# for box_info in box_infos['detected_texts']:
#     cropped_img = box_info['cropped_img']
#     ocr_res = cn_ocr.ocr_for_single_line(cropped_img)
#     print('ocr result: %s' % str(ocr_res))
#     print(ocr_res['text'])
