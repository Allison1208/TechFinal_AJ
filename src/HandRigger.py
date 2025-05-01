import importlib
import MayaUtils
importlib.reload(MayaUtils)
from MayaUtils import GetMayaMainWindow, MayaWindow
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QColorDialog, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QSlider, QVBoxLayout, QWidget 
from PySide2.QtCore import Qt, Signal 
from maya.OpenMaya import MVector
import maya.mel as mel
import maya.cmds as mc 

class HandRigger:
    def __init__(self):
        self.wrist = ""
        self.fingerBase = ""
        self.fingerMiddle = ""
        self.fingerTip = ""
        self.controllerSize = 5
        self.controllerColor = [0,0,0]

    def FindJointBasedOnSelection(self):
        try:
            self.wrist = mc.ls(sl = True, type ="joint")[0]
            self.fingerBase = mc.listRelatives(self.wrist, c = True, type = "joint")[0]
            self.fingerMiddle = mc.listRelatives(self.fingerBase, c = True, type ="joint")[0]
            self.fingerTip = mc.listRelatives(self.fingerMiddle, c = True, type = "joint")[0]
        except Exception as e:
            raise Exception(f"Wrong Selection, Plase select the wrist joint!")
            

            

