import os
import xml.etree.ElementTree as ET
from PIL import Image
import datetime

class ToVOCConverter(object):
    '''
    Parent class for all the converters
    '''

    def __init__(self,imageFolder,sourceLabelFolder,outputLabelFolder):
        '''
        imageFolder: folder where all the images are
        sourceLabelFolder: path to folder where source data is saved
        outputLabelFolder: path where ouptut files are to be saved
        '''
        assert os.path.isdir(imageFolder), "Image folder {:} does not exist!".format(imageFolder)
        assert os.path.isdir(sourceLabelFolder), "Source label folder {:} does not exist!".format(sourceLabelFolder)
        assert os.path.isdir(outputLabelFolder), "Output label folder {:} does not exist!".format(outputLabelFolder)

        self.imageFolder = imageFolder
        self.sourceLabelFolder = sourceLabelFolder
        self.outputLabelFolder = outputLabelFolder
        self.currentOutFile = None
        self.currentImageFile = None
        
        self.time = datetime.datetime.now().isoformat()

        self.imageFormat = None
        self.database = None

        self.currentImageShape = None

    def initializeXMLFile(self):
        '''
        Write the data that has nothing to do with the labels
        '''
        root = ET.Element("annotation")
        ET.SubElement(root,"folder").text = self.imageFolder
        ET.SubElement(root,"filename").text = self.currentImageFile

        source = ET.SubElement(root,"source")
        ET.SubElement(source,"database").text = self.database
        ET.SubElement(source,"annotation").text = self.database

        conversion = ET.SubElement(root,"conversion")
        ET.SubElement(conversion,"created").text = self.time
        ET.SubElement(conversion,"updated").text = self.time

        with Image.open(os.path.join(self.imageFolder,self.currentImageFile)) as img:
            width,height = img.size
            depth = img.mode
        assert depth=="RGB", "Colormode for image {} is not RGB, it is {}".format(self.currentImageFile,depth)
        depth = 3
        self.currentImageShape = (width,height,depth)
        
        imgSize = ET.SubElement(root,"size")
        ET.SubElement(imgSize,"width").text = str(width)
        ET.SubElement(imgSize,"height").text = str(height)
        ET.SubElement(imgSize,"depth").text = str(depth)

        return root

    def createXMLLabelFile(self,fileName):
        '''
        This method needs to be overridden in the child class
        '''
        assert False, "createXMLLabelFile needs to be implemented in the childClass"

    def createXMLLabel(self,line):
        '''
        Create a xml style label for the line that is passed in. Return the xml data.
        Must be implemented in the child class
        '''
        assert False, "createXMLLabel needs to be implemented in the childClass"

    def convertDataset(self):
        '''
        Convert all of the label files in self.sourceLabelFolder

        Need to catch any and all errors
            -image does not exist for label
            -label does not exist for an image
        '''
        assert False, "convertDataset needs to be implemented in the childClass"

