# 作者：欧楠青
# 2019年4月5日

import os
import cv2

image_path = r"VOCdevkit2\VOC2007\JPEGImages"  # 原始图片位置
new_image_path = r"VOCdevkit2\VOC2007\JPEGImages_00"  # 切割后图片位置
anno_path = r'2007_train.txt'  # 原始标注文件txt位置
w_path = r'2007_write_test.txt'  # 修改后的标注文件txt位置
test_img_path = r'VOCdevkit2\VOC2007\JPEGImages_t'  # 存放测试结果的路径
Ax1, Ay1, Ax2, Ay2 = 230, 4, 892, 666  # 要切割的部分的四个坐标xmin,ymin,xmax,ymax

'''
裁剪图片
输入：图片路径（文件夹），新路径（文件夹），裁剪部分的四个坐标
输出：无
'''


def cut_img(img_path, new_path, xmin, ymin, xmax, ymax):
    dirs = os.listdir(img_path)
    for file in dirs:
        right_path = img_path + "\\" + file
        img = cv2.imread(right_path)
        img = img[ymin:ymax, xmin:xmax]
        cv2.imwrite(new_path + "\\" + file, img)
    print('cut image in', new_path)


'''
修改标注的四个坐标值
输入：将要接受修改的box的四个坐标
接受Ax1, Ay1, Ax2, Ay2四个常值
输出：修改后的四个坐标和True/False（用于判断是否添加这个box）
'''


def scale(Bx1, By1, Bx2, By2):
    MAX_AX = max(Ax1, Ax2)
    MIN_AX = min(Ax1, Ax2)
    MAX_BX = max(Bx1, Bx2)
    MIN_BX = min(Bx1, Bx2)

    MAX_AY = max(Ay1, Ay2)
    MIN_AY = min(Ay1, Ay2)
    MAX_BY = max(By1, By2)
    MIN_BY = min(By1, By2)

    xshang = min(MAX_AX, MAX_BX) - max(MIN_AX, MIN_BX)
    yshang = min(MAX_AY, MAX_BY) - max(MIN_AY, MIN_BY)

    area = (MAX_BX - MIN_BX) * (MAX_BY - MIN_BY)

    if xshang <= 0 or yshang <= 0 or (xshang * yshang) / area < 0.25:
        print("不计入框内")
        return (Bx1, By1, Bx2, By2, False)
    else:
        Bx1, Bx2, By1, By2 = max(MIN_AX, MIN_BX) - Ax1, min(MAX_AX, MAX_BX) - Ax1, max(MIN_AY, MIN_BY) - Ay1, min(
            MAX_AY, MAX_BY) - Ay1
        print("边框修改为", Bx1, By1, Bx2, By2)
    return (Bx1, By1, Bx2, By2, True)


'''
裁剪txt文件的标注
输入：原标注路径，新标注路径，（都到txt）
输出：无
'''


def cut_anno(annotation_path, new_img_path, write_path):
    with open(annotation_path) as f:
        lines = f.readlines()
    for i in lines:
        i = i.split()
        img = i[0]
        general_box = i[1:]
        with open(write_path, 'a') as f:
            f.writelines([new_img_path + "/" + img[(img.rfind("/") + 1):], " "])
            for y in general_box:
                y = y.split(",")
                box = [int(x) for x in y]
                box[0], box[1], box[2], box[3], judge = scale(box[0], box[1], box[2], box[3])
                if judge == True:
                    for xman in box[0:4]:
                        f.writelines([str(xman), ","])
                    f.writelines([str(box[4]), " "])
                else:
                    pass
            f.write("\n")
    print('new annotation in', write_path)


'''
生成测试图片
输入：标注路径，保存路径
输出：无
'''


def t_anno(annotation_path, save_path):
    with open(annotation_path) as f:
        lines = f.readlines()
    for i in lines:
        i = i.split()
        img_path = i[0]
        general_box = i[1:]
        img = cv2.imread(img_path)
        for y in general_box:
            y = y.split(",")
            box = [int(x) for x in y]
            red = (0, 0, 255)
            cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), red, 3)
        cv2.imwrite(save_path + "/" + img_path[(img_path.rfind("/") + 1):], img)
    print('test image in', save_path)


def t_resize_main(img_path, new_img_path, annotation_path, write_path, test_image_path, xmin, ymin, xmax, ymax):
    cut_img(img_path, new_img_path, xmin, ymin, xmax, ymax)
    cut_anno(annotation_path, new_img_path, write_path)
    t_anno(write_path, test_image_path)


if __name__ == '__main__':
    t_resize_main(image_path, new_image_path, anno_path, w_path,
                  test_img_path, Ax1, Ay1, Ax2, Ay2)
