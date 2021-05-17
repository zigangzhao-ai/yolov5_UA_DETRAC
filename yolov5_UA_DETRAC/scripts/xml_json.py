'''
code by zzg@2020/01/05
'''
#!/usr/bin/python

# pip install lxml
import sys
import os
import json
import glob
import xml.etree.ElementTree as ET
import pdb
from collections import defaultdict

START_BOUNDING_BOX_ID = 1
PRE_DEFINE_CATEGORIES = {}
# If necessary, pre-define category and its id
#  PRE_DEFINE_CATEGORIES = {"aeroplane": 1, "bicycle": 2, "bird": 3, "boat": 4,
                         #  "bottle":5, "bus": 6, "car": 7, "cat": 8, "chair": 9,
                         #  "cow": 10, "diningtable": 11, "dog": 12, "horse": 13,
                         #  "motorbike": 14, "person": 15, "pottedplant": 16,
                         #  "sheep": 17, "sofa": 18, "train": 19, "tvmonitor": 20}
def get(root, name):
    vars = root.findall(name)
    return vars

def get_and_check(root, name, length):
    vars = root.findall(name)
    if len(vars) == 0:
        raise NotImplementedError('Can not find %s in %s.'%(name, root.tag))
    if length > 0 and len(vars) != length:
        raise NotImplementedError('The size of %s is supposed to be %d, but is %d.'%(name, length, len(vars)))
    if length == 1:
        vars = vars[0]
    return vars

def get_filename_as_int(filename):
    try:
        filename = os.path.splitext(filename)[0]
        return filename
    except:
        raise NotImplementedError('Filename %s is supposed to be an integer.'%(filename))


#pdb.set_trace()
def convert(xml_dir, xml_basenames, json_file):
    #list_fp = open(xml_list, 'r')
    list_fp = xml_basenames
    #print(list_fp)
    json_dict = {"type": "instances", "annotations": []}

    bnd_id = START_BOUNDING_BOX_ID
    for line in list_fp:
        line = line.strip()
       # print(line)
        print("Processing %s"%(line))
        xml_f = os.path.join(xml_dir, line)
        # print(xml_f)
        tree = ET.parse(xml_f)
        root = tree.getroot()
        path = get(root, 'path')
        if len(path) == 1:
            filename = os.path.basename(path[0].text)
        elif len(path) == 0:
            filename = get_and_check(root, 'filename', 1).text
        else:
            raise NotImplementedError('%d paths found in %s'%(len(path), line))
        ## The filename must be a number
        image_id = get_filename_as_int(filename)
        size = get_and_check(root, 'size', 1)
        width = int(get_and_check(size, 'width', 1).text)
        height = int(get_and_check(size, 'height', 1).text)
        image = {'file_name': filename, 'height': height, 'width': width}
        # json_dict['annotations'].append(image)
        bbox = []
        for obj in get(root, 'object'):
            
            bndbox = get_and_check(obj, 'bndbox', 1)
            xmin = float(get_and_check(bndbox, 'xmin', 1).text) 
            ymin = float(get_and_check(bndbox, 'ymin', 1).text) 
            xmax = float(get_and_check(bndbox, 'xmax', 1).text)
            ymax = float(get_and_check(bndbox, 'ymax', 1).text)
          
            assert(xmax > xmin)
            assert(ymax > ymin)
            o_width = abs(xmax - xmin)
            o_height = abs(ymax - ymin)
            bbox.append([xmin, ymin, xmax, ymax])
            
        ann = {'bbox': bbox}
            
        image.update(ann)
       
        json_dict['annotations'].append(image)


    json_fp = open(json_file, 'w')
    json_str = json.dumps(json_dict, indent = 1)
    json_fp.write(json_str)
    json_fp.close()


if __name__ == '__main__':

    xml_dir = "train_xml"
    xml_list = glob.glob(xml_dir + '/*.xml')

    # print(xml_list)
    xml_basenames = []
    for item in xml_list:
        xml_basenames.append(os.path.basename(item))

    # f = open('xml_list.txt','w')
    # for xml in xml_basenames:
    #     f.write('\n'+xml)
    json_path = 'json'
    if not os.path.exists(json_path):
        os.makedirs(json_path)
    json_file = "json/train.json"
    convert(xml_dir, xml_basenames, json_file)

    print("finished!")