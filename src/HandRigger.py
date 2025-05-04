import importlib
import MayaUtils
importlib.reload(MayaUtils)
from MayaUtils import GetMayaMainWindow, MayaWindow
from PySide2.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QSlider, QVBoxLayout
from PySide2.QtCore import Qt
import maya.cmds as mc 

class HandRigger:
    def __init__(self):
        self.wrist = ""
        self.thumbBase= ""
        self.thumbMid = ""
        self.thumbTip = ""
        self.indexBase = "" 
        self.indexMid = "" 
        self.indexTip = "" 
        self.middleBase = "" 
        self.middleMid = "" 
        self.middleTip = ""
        self.ringBase = ""
        self.ringMid = "" 
        self.ringTip = "" 
        self.pinkyBase = ""
        self.pinkyMid = "" 
        self.pinkyTip = "" 
        self.controllerSize = 5
        self.controllerColor = [0,0,0]

    def FindJointBasedOnSelection(self):
        try:
            self.wrist = mc.ls(sl = True, type ="joint")[0]
            self.thumbBase = mc.listRelatives(self.wrist, c = True, type = "joint")[0]
            self.thumbMid = mc.listRelatives(self.thumbBase, c = True, type = "joint")[0]
            self.thumbTip = mc.listRelatives(self.thumbMid, c = True, type = "joint")[0]
            self.indexBase = mc.listRelatives(self.wrist, c = True, type = "joint")[0]
            self.indexMid = mc.listRelatives(self.indexBase, c = True, type = "joint")[0]
            self.indexTip = mc.listRelatives(self.indexMid, c = True, type = "joint")[0]
            self.middleBase = mc.listRelatives(self.wrist, c = True, type = "joint")[0]
            self.middleMid = mc.listRelatives(self.middleBase, c = True, type = "joint")[0]
            self.middleTip = mc.listRelatives(self.middleMid, c = True, type = "joint")[0]
            self.ringBase = mc.listRelatives(self.wrist, c = True, type = "joint")[0]
            self.ringMid = mc.listRelatives(self.ringBase, c = True, type = "joint")[0]
            self.ringTip = mc.listRelatives(self.ringMid, c = True, type = "joint")[0]
            self.pinkyBase = mc.listRelatives(self.wrist, c = True, type = "joint")[0]
            self.pinkyMid = mc.listRelatives(self.pinkyBase, c = True, type = "joint")[0]
            self.pinkyTip = mc.listRelatives(self.pinkyMid, c = True, type = "joint")[0]
        except Exception as e:
            raise Exception(f"Wrong Selection, Plase select the wrist joint!")
        
    def CreateControllerForJoint(self, jntName): 
        ctrlName = "ac_l_" + jntName 
        ctrlGrpName = ctrlName + "_grp" 
        mc.circle(name = ctrlName, radius = self.controllerSize, normal = (1, 0, 0)) 
        mc.group(ctrlName, n = ctrlGrpName) 
        mc.matchTransform(ctrlGrpName, jntName)
        mc.orientConstraint(ctrlName, jntName)
        return ctrlName, ctrlGrpName 
        

    def RigHand(self):
        wristCtrl, wristCtrlGrp = self.CreateControllerForJoint(self.wrist)
        thumbBaseCtrl, thumbBaseCtrlGrp = self.CreateControllerForJoint(self.thumbBase)
        thumbMidCtrl, thumbMidCtrlGrp = self.CreateControllerForJoint(self.thumbMid)
        thumbTipCtrl, thumbTipCtrlGrp = self.CreateControllerForJoint(self.thumbTip)
        indexBaseCtrl, indexBaseCtrlGrp = self.CreateControllerForJoint(self.indexBase)
        indexMidCtrl, indexMidCtrlGrp = self.CreateControllerForJoint(self.indexMid)
        indexTipCtrl, indexTipCtrlGrp = self.CreateControllerForJoint(self.indexTip)
        middleBaseCtrl, middleBaseCtrlGrp = self.CreateControllerForJoint(self.middleBase)
        middleMidCtrl, middleMidCtrlGrp = self.CreateControllerForJoint(self.middleMid)
        middleTipCtrl, middleTipCtrlGrp = self.CreateControllerForJoint(self.middleTip)
        ringBaseCtrl, ringBaseCtrlGrp = self.CreateControllerForJoint(self.ringBase)
        ringMidCtrl, ringMidCtrlGrp = self.CreateControllerForJoint(self.ringMid)
        ringTipCtrl, ringTipCtrlGrp = self.CreateControllerForJoint(self.ringTip)
        pinkyBaseCtrl, pinkyBaseCtrlGrp = self.CreateControllerForJoint(self.pinkyBase)
        pinkyMidCtrl, pinkyMidCtrlGrp = self.CreateControllerForJoint(self.pinkyMid)
        pinkyTipCtrl, pinkyTipCtrlGrp = self.CreateControllerForJoint(self.pinkyTip)

        mc.parent(thumbBaseCtrlGrp, wristCtrl)
        mc.parent(thumbMidCtrlGrp, thumbBaseCtrl)
        mc.parent(thumbTipCtrlGrp, thumbMidCtrl)
        mc.parent(indexBaseCtrlGrp, wristCtrl)
        mc.parent(indexMidCtrlGrp, indexBaseCtrl)
        mc.parent(indexTipCtrlGrp, indexMidCtrl)
        mc.parent(middleBaseCtrlGrp, wristCtrl)
        mc.parent(middleMidCtrlGrp, middleBaseCtrl)
        mc.parent(middleTipCtrlGrp, middleMidCtrl)
        mc.parent(ringBaseCtrlGrp, wristCtrl)
        mc.parent(ringMidCtrlGrp, ringBaseCtrl)
        mc.parent(ringTipCtrlGrp, ringMidCtrl)
        mc.parent(pinkyBaseCtrlGrp, wristCtrl)
        mc.parent(pinkyMidCtrlGrp, pinkyBaseCtrl)
        mc.parent(pinkyTipCtrlGrp, pinkyMidCtrl)

class HandRigToolWidget(MayaWindow):
    def __init__(self):
        super().__init__()
        self.rigger = HandRigger()
        self.setWindowTitle("Hand Rigger")
        self.masterLayout = QVBoxLayout() 
        self.setLayout(self.masterLayout)

        toolTipLabel = QLabel("Select the wrist joint, and press the auto find button")
        self.masterLayout.addWidget(toolTipLabel)

        self.jntsListLineEdit = QLineEdit() 
        self.masterLayout.addWidget(self.jntsListLineEdit) 
        self.jntsListLineEdit.setEnabled(False)
        
        autoFindJntBtn = QPushButton("Auto Find") 
        autoFindJntBtn.clicked.connect(self.AutoFindJntButtonClicked) 
        self.masterLayout.addWidget(autoFindJntBtn)

        ctrlSizeSlider = QSlider()
        ctrlSizeSlider.setOrientation(Qt.Horizontal)
        ctrlSizeSlider.setRange(1, 30)
        ctrlSizeSlider.setValue(self.rigger.controllerSize)
        self.ctrlSizeLabel = QLabel(f"{self.rigger.controllerSize}")
        ctrlSizeSlider.valueChanged.connect(self.CtrlSizeSliderChanged)

        ctrlSizeLayout = QHBoxLayout()
        ctrlSizeLayout.addWidget(ctrlSizeSlider)
        ctrlSizeLayout.addWidget(self.ctrlSizeLabel)
        self.masterLayout.addLayout(ctrlSizeLayout)

        rigHandBtn = QPushButton("Rig Hand") 
        rigHandBtn.clicked.connect(lambda : self.rigger.RigHand()) 
        self.masterLayout.addWidget(rigHandBtn)

    def CtrlSizeSliderChanged(self,newValue):
        self.ctrlSizeLabel.setText(f"{newValue}")
        self.rigger.controllerSize = newValue

    def AutoFindJntButtonClicked(self): 
        try: 
            self.rigger.FindJointBasedOnSelection() 
            self.jntsListLineEdit.setText(f"{self.rigger.wrist},{self.rigger.thumbBase}, {self.rigger.thumbMid}, {self.rigger.thumbTip}, {self.rigger.indexBase}, {self.rigger.indexMid}, {self.rigger.indexTip}, {self.rigger.middleBase}, {self.rigger.middleMid}, {self.rigger.middleTip}, {self.rigger.ringBase}, {self.rigger.ringMid}, {self.rigger.ringTip}, {self.rigger.pinkyBase}, {self.rigger.pinkyMid}, {self.rigger.pinkyTip}") 
        except Exception as e: 
            QMessageBox.critical(self, "Error", f"{e}")

handRiggerWidget = HandRigToolWidget()
handRiggerWidget.show() 

GetMayaMainWindow()