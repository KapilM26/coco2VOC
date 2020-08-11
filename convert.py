from KITTIConverter import KITTItoVOCConverter
import os, shutil
import tempfile

imageFolder = "/home/kapil/chess_data/train/" #path to images
anno_path = "/home/kapil/chess_data/train_anno/_annotations.coco.json" #path to annotations file
os.system('python coco2kitti.py --ann_file_path '+anno_path)
labelIn = tempfile.gettempdir()+'/labels'
try:
    os.mkdir("VOC_labels") #make folder to store labels
except FileExistsError:
    pass
labelOut = "VOC_labels" # path to output labels folder
converter = KITTItoVOCConverter(imageFolder,labelIn,labelOut)
converter.convertDataset(verbose=True)