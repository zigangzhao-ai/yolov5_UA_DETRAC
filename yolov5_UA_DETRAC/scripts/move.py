'''
code by zzg@2021/05/11
'''

import os

train_file = os.listdir("/home/lj/zzg/fenghuo-zzg/DETRAC-dataset/Images/Insight-MVT_Annotation_Train/")
test_file = os.listdir("/home/lj/zzg/fenghuo-zzg/DETRAC-dataset/Images/Insight-MVT_Annotation_Test/")
print(len(train_file))

image_file = os.listdir("/home/lj/zzg/fenghuo-zzg/yolov5_zq_DETRAC/detrac-data-zzg/JPG/")
txt_file = os.listdir("/home/lj/zzg/fenghuo-zzg/yolov5_zq_DETRAC/detrac-data-zzg/ANO/")

src_image_file = "/home/lj/zzg/fenghuo-zzg/yolov5_zq_DETRAC/detrac-data-zzg/JPG"
src_txt_file = "/home/lj/zzg/fenghuo-zzg/yolov5_zq_DETRAC/detrac-data-zzg/ANO"

dst_image_train = "/home/lj/zzg/fenghuo-zzg/yolov5_zq_DETRAC/detrac-data-zzg/images/train"
dst_image_test = "/home/lj/zzg/fenghuo-zzg/yolov5_zq_DETRAC/detrac-data-zzg/images/test"

dst_txt_train = "/home/lj/zzg/fenghuo-zzg/yolov5_zq_DETRAC/detrac-data-zzg/labels/train"
dst_txt_test = "/home/lj/zzg/fenghuo-zzg/yolov5_zq_DETRAC/detrac-data-zzg/labels/test"


cnt = 0
for img in image_file:
    #print(img)
    if img in train_file:
        cnt += 1
        print(cnt)
        image_path = src_image_file + '/' + img 
        txt_path =src_txt_file + '/' + img 

        cmd = "mv {} {}".format(image_path, dst_image_train)
        print(cmd)
        os.system(cmd)
        cmd = "mv {} {}".format(txt_path, dst_txt_train)
        os.system(cmd)
  
    if img in test_file:
        image_path = src_image_file + '/' +img 
        txt_path = src_txt_file + '/' + img

        cmd = "mv {} {}".format(image_path, dst_image_test)
        print(cmd)
        os.system(cmd)
        cmd = "mv {} {}".format(txt_path, dst_txt_test)
        os.system(cmd)

print("finished move !!")