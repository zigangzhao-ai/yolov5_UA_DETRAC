'''
code by zzg@2021/05/08
'''

import os
import glob
from PIL import Image
import pdb
import cv2

# the direction/path of Image,Label
classes = ['car']

FLAG = 1
if FLAG == 1:

    src_img_dir = "/workspace/zigangzhao/fenghuo-zzg/DETRAC-dataset/Annotations/data/images/train/"
    src_txt_dir = "/workspace/zigangzhao/fenghuo-zzg/DETRAC-dataset/Annotations/train_detrac_txt/"
    src_xml_dir = "train_xml/"

else:
    src_img_dir = "/workspace/zigangzhao/fenghuo-zzg/DETRAC-dataset/Annotations/data/images/test/"
    src_txt_dir = "/workspace/zigangzhao/fenghuo-zzg/DETRAC-dataset/Annotations/test_detrac_txt/"
    src_xml_dir = "test_xml/"

if not os.path.exists(src_xml_dir):
    os.makedirs(src_xml_dir)

img_Lists = glob.glob(src_txt_dir + '/*.txt')
print(len(img_Lists))

img_basenames = []
for item in img_Lists:
    img_basenames.append(os.path.basename(item))
    #print(img_basenames)

img_name = []
for item in img_basenames:
    temp1, temp2 = os.path.splitext(item)
    img_name.append(temp1)
    #print(img_name)
i = 0
j = 0
for img in img_name:
    # print(img)
    im = cv2.imread(src_img_dir + '/' + img + '.jpg')
    if im is None:
        i += 1

        print(i, img)
    if im is not None:
        j += 1
        print(j)
        # print(im.shape[::-1])
        channels, width, height = im.shape[::-1]  ##get w and h

        xml_file = open((src_xml_dir + '/' + str(img) + '.xml'), 'w')

        xml_file.write('<annotation>\n')
        xml_file.write('\t<folder>' + 'VOC2007' + '</folder>\n')
        xml_file.write('\t<filename>' + str(img) + '.jpg' + '</filename>\n')
        xml_file.write('\t<source>\n')
        xml_file.write('\t\t<database>Unknown</database>\n')
        xml_file.write('\t</source>\n')
        xml_file.write('\t<size>\n')
        xml_file.write('\t\t<width>'+ str(width) + '</width>\n')
        xml_file.write('\t\t<height>'+ str(height) + '</height>\n')
        xml_file.write('\t\t<depth>' + str(channels) + '</depth>\n')
        xml_file.write('\t</size>\n')
        xml_file.write('\t\t<segmented>0</segmented>\n')
        
        gt = open(src_txt_dir + '/' + img + '.txt').read().splitlines()
        # print(gt)
        for x in gt:
            spt = x.split()
            # print(spt[0])
            classlabel = classes[int(spt[0])]
            xmin = float(spt[1])
            ymin = float(spt[2])
            xmax = float(spt[3])
            ymax = float(spt[4])
            
            assert ymax > ymin and xmax > xmin

            ##[center_x, center_y, w, h]
            xml_file.write('\t<object>\n')
            xml_file.write('\t\t<name>'+ classlabel +'</name>\n')
            xml_file.write('\t\t<pose>Unspecified</pose>\n')
            xml_file.write('\t\t<truncated>1</truncated>\n')
            xml_file.write('\t\t<difficult>0</difficult>\n')
            xml_file.write('\t\t<bndbox>\n')
            xml_file.write('\t\t\t<xmin>' + str(xmin) + '</xmin>\n')
            xml_file.write('\t\t\t<ymin>' + str(ymin) + '</ymin>\n')  
            xml_file.write('\t\t\t<xmax>' + str(xmax) + '</xmax>\n')
            xml_file.write('\t\t\t<ymax>' + str(ymax) + '</ymax>\n')  
            xml_file.write('\t\t</bndbox>\n')
            xml_file.write('\t</object>\n')         
                    
        xml_file.write('</annotation>')


print("finished!")
print(i, j)
