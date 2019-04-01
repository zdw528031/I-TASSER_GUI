#!/usr/bin/python
import xml.etree.ElementTree as ET
import logging
import datetime
import os
import sys

# we mainly create a class here for the mainframe to modify and load config data
class xml_loader():
    def __init__(self):

        self.log_dir_path = os.path.join(os.path.dirname(__file__),'log')
        self.con_dir_path = os.path.join(os.path.dirname(__file__),'config')
        currentDT = datetime.datetime.now()
        log_file_name = currentDT.strftime("%Y_%m_%d_%H_%M_%S.log")
        #logging.basicConfig(filename = os.path.join(self.log_dir_path,log_file_name), level=logging.INFO)

        logging.info('logging module successfully create...')
        logging.info('loading config xml file...')

        self.config_file_name = "config.xml"
        try:
            self.tree = ET.parse(os.path.join(self.con_dir_path,self.config_file_name))
        except Exception:
            logging.error('fail to loading '+ os.path.join(self.con_dir_path,self.config_file_name) +' xml file')
            sys.exit(1)
        
        logging.info('finish vailadtion of xml file...')
        
        self.root = self.tree.getroot()
 
    def get_ITASSER_DIR(self):
        for child in self.root:
            if child.tag == "ITASSER_DIR":
                return child.text
        raise ValueError('cannot find ITASSER_DIR element in the xml')
    
    def get_LIBRARY_DIR(self):
        for child in self.root:
            if child.tag == "LIBRARY_DIR":
                return child.text
        raise ValueError('cannot find LIBRARY_DIR element in the xml')

    def get_OUTPUT_DIR(self):
        for child in self.root:
            if child.tag == "OUTPUT_DIR":
                return child.text
        raise ValueError('cannot find OUTPUT_DIR element in the xml')
    
    def get_CHIMERA_DIR(self):
        for child in self.root:
            if child.tag == "CHIMERA_DIR":
                return child.text
        raise ValueError('cannot find CHIMERA_DIR element in the xml')

    def set_ITASSER_DIR(self,ITASSER_DIR):
        for child in self.root:
            if child.tag == "ITASSER_DIR":
                child.text = ITASSER_DIR
                self.tree.write(os.path.join(self.con_dir_path,self.config_file_name))
                return
        raise ValueError('cannot find ITASSER_DIR element in the xml')

    def set_LIBRARY_DIR(self,LIBRARY_DIR):
        for child in self.root:
            if child.tag == "LIBRARY_DIR":
                child.text = LIBRARY_DIR
                self.tree.write(os.path.join(self.con_dir_path,self.config_file_name))
                return
        raise ValueError('cannot find LIBRARY_DIR element in the xml')
    
    def set_OUTPUT_DIR(self,OUTPUT_DIR):
        for child in self.root:
            if child.tag == "OUTPUT_DIR":
                child.text = OUTPUT_DIR
                self.tree.write(os.path.join(self.con_dir_path,self.config_file_name))
                return
        raise ValueError('cannot find OUTPUT_DIR element in the xml')

    def set_CHIMERA_DIR(self,CHIMERA_DIR):
        for child in self.root:
            if child.tag == "CHIMERA_DIR":
                child.text = CHIMERA_DIR
                self.tree.write(os.path.join(self.con_dir_path,self.config_file_name))
                return
        raise ValueError('cannot find CHIMERA_DIR element in the xml')