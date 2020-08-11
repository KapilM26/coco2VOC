"""coco2kitti.py: Converts MS COCO annotation files to
                  Kitti format bounding box label files
__author__ = "Jon Barker"
"""

import os, shutil
from pycocotools.coco import COCO
import argparse
import tempfile

def coco2kitti(catNms, annFile):

    # initialize COCO api for instance annotations
    coco = COCO(annFile)

    # Create an index for the category names
    cats = coco.loadCats(coco.getCatIds())
    cat_idx = {}
    for c in cats:
        cat_idx[c['id']] = c['name']

    for img in coco.imgs:

        # Get all annotation IDs for the image
        catIds = coco.getCatIds(catNms=catNms)
        annIds = coco.getAnnIds(imgIds=[img], catIds=catIds)

        # If there are annotations, create a label file
        if len(annIds) > 0:
            # Get image filename
            img_fname = coco.imgs[img]['file_name']
            # open text file
            image_fname_ls = img_fname.split('.')
            image_fname_ls[-1] = 'txt'
            label_fname = '.'.join(image_fname_ls)
            with open(tempfile.gettempdir()+'/labels/' + label_fname,'w') as label_file:
                anns = coco.loadAnns(annIds)
                for a in anns:
                    bbox = a['bbox']
                    # Convert COCO bbox coords to Kitti ones
                    bbox = [bbox[0], bbox[1], bbox[2] + bbox[0], bbox[3] + bbox[1]]
                    bbox = [str(b) for b in bbox]
                    catname = cat_idx[a['category_id']]
                    # Format line in label file
                    # Note: all whitespace will be removed from class names
                    out_str = [catname.replace(" ","")
                               + ' ' + ' '.join(['0']*2)
                               + ' ' + ' '.join([b for b in bbox])
                               + ' ' + ' '.join(['0']*8)
                               +'\n']
                    label_file.write(out_str[0])

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='convert coco to kitti')
    parser.add_argument('--ann_file_path', help='path to annotation file')

    # These settings assume this script is in the annotations directory
    args = parser.parse_args()
    annFile = args.ann_file_path

    # If this list is populated then label files will only be produced
    # for images containing the listed classes and only the listed classes
    # will be in the label file
    # EXAMPLE:
    #catNms = ['person', 'dog', 'skateboard']
    catNms = []

    # Check if a labels file exists and, if not, make one
    # If it exists already, exit to avoid overwriting
    if os.path.isdir(tempfile.gettempdir()+'/labels'):
        shutil.rmtree(tempfile.gettempdir()+'/labels')
    os.mkdir(tempfile.gettempdir()+'/labels')
    coco2kitti(catNms, annFile)
