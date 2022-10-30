# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
from mieanalyzer import Ui_MainWindow
import pandas as pd
import numpy as np
import scatteringDataFunctions as sdf

class MinimumVerticalLines(object):
    def __init__(self,vLinesDict={},parent=None):
        self.parent = parent
        self.vLines = vLinesDict
    def __getitem__(self,m):
        if str(m) in self.vLines.keys():
            return self.vLines[str(m)]
        else:
            return None
    def __setitem__(self,m,obj):
        self.vLines[str(m)] = obj
    def __call__(self):
        return list(self.vLines.values())
    def mRange(self):
        keys_int = [int(key) for key in self.vLines.keys()]
        m_min = min(keys_int)
        m_max = max(keys_int)
        return m_min,m_max
    def remove(self,m):
        vLine = self.vLines[str(m)]
        self.vLines.pop(str(m))
        if self.parent is not None:
            self.parent.removeItem(vLine)

class Ui(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.state = None
        self.wavelength = None
        self.screenZ = None
        self.diameter = None
        self.fraunDiameter = None
        self.relref = None

    def setupMeta(self):
        # self.graphWidget.keyPressEvent = self.graphWidget_onKeyPress
        # self.graphWidget.keyReleaseEvent = self.graphWidget_onKeyRelease
        self.graphWidget.setLabel("left","Intensity (%)")
        self.graphWidget.setLabel("bottom","x (mm)")
        self.graphWidget.vLines = MinimumVerticalLines(parent=self.graphWidget)
        self.mieScattering_radioButton.toggled.connect(self.refreshDiameter)
        self.fraunhoferApproximation_radioButton.toggled.connect(self.refreshDiameter)
        self.wavelength_lineEdit.textChanged.connect(self.refreshWavelength)
        self.screenDistance_lineEdit.textChanged.connect(self.refreshScreenZ)
        self.fibreDiameter_lineEdit.textChanged.connect(self.refreshDiameter)
        self.fraunhoferDiameter_lineEdit.textChanged.connect(self.refreshFraunDiameter)
        self.refractiveIndex_lineEdit.textChanged.connect(self.refreshRelref)
        self.extinctionCoefficient_lineEdit.textChanged.connect(self.refreshRelref)
        self.updateParameters()
    
    def refreshWavelength(self):
        self.wavelength = float(self.wavelength_lineEdit.text())
        self.updateVLinePositions()
        
    def refreshScreenZ(self):
        self.screenZ = float(self.screenDistance_lineEdit.text())
        self.updateVLinePositions()
    
    def refreshDiameter(self):
        self.diameter = float(self.fibreDiameter_lineEdit.text())
        self.updateVLinePositions()
        
    def refreshFraunDiameter(self):
        self.fraunDiameter = float(self.fraunhoferDiameter_lineEdit.text())
        self.updateVLinePositions()
        
    def refreshRelref(self):
        self.relref = (float(self.refractiveIndex_lineEdit.text()) +
                                float(self.extinctionCoefficient_lineEdit.text())*1j)
        self.updateVLinePositions()
        
    def updateParameters(self):
        self.refreshWavelength()
        self.refreshScreenZ()
        self.refreshDiameter()
        self.refreshFraunDiameter()
        self.refreshRelref()
    
    def addVLine(self,m,isFraun=False,cPos=None):
        if cPos is None: cPos = self.cPos
        pen = [(50,50,150),(150,150,150)][m==0]
        vLine = pg.InfiniteLine(pos=cPos,pen=pen,movable=True)
        vLine.m = m
        vLine.sigDragged.connect(lambda: self.vLine_onDragged(vLine))
        vLine.sigPositionChangeFinished.connect(self.vLine_onPositionChangeFinished)
        self.graphWidget.vLines[m] = vLine
        self.adjustVLine(m,isFraun,cPos)
        self.graphWidget.addItem(vLine)
    
    def adjustVLine(self,m,isFraun,cPos):
        if m==0:
            dx=0
        else:
            if isFraun:
                dx = np.sign(m)*self.screenZ*10/((1000*self.diameter/self.wavelength/m)**2-1)**0.5
            else:
                dtheta = sdf.getMieDThetaM(self.diameter,self.wavelength,self.relref,m)
                dx = self.screenZ*np.tan(dtheta)*10
        self.graphWidget.vLines[m].setValue(cPos+dx)
    
    def plot(self,x,y):
        self.graphWidget.plot(x,y)
        self.xdata = x
        self.ydata = y
        self.cPos = sdf.getCentreX(x,y)
        isFraun = self.fraunhoferApproximation_radioButton.isChecked()
        mMin, mMax = sdf.getMRange(x,self.screenZ,self.diameter,self.wavelength,self.cPos)
        for m in range(mMin,mMax+1):
            self.addVLine(m,isFraun,self.cPos)


    def updateVLinesExist(self):
        isFraun = self.fraunhoferApproximation_radioButton.isChecked()
        mMin, mMax = sdf.getMRange(self.xdata,self.screenZ,self.diameter,self.wavelength,self.cPos)
        mMin0, mMax0 = self.graphWidget.vLines.mRange()
        print((mMin,mMax,mMin0,mMax0))
        if mMin > mMin0:
            for i in range(mMin0,mMin): self.graphWidget.vLines.remove(i)
        elif mMin < mMin0:
            for i in range(mMin,mMin0): self.addVLine(i, isFraun)
        if mMax < mMax0:
            for i in range(mMax+1,mMax0+1): self.graphWidget.vLines.remove(i)
        elif mMax > mMax0:
            for i in range(mMax0+1,mMax+1): self.addVLine(i, isFraun)
        

    def updateDiameter(self,m=1):
        #updates diameter based on vLine[m] to reference vLine[0]   
        dx = self.graphWidget.vLines[m].value()-self.cPos
        dTheta = np.arctan(dx/10/self.screenZ)
        fraunhoferDiameter = sdf.getFraunDiameter(dTheta,self.wavelength,m)
        self.fraunhoferDiameter_lineEdit.setText(format(fraunhoferDiameter,'.2f'))
        if self.fraunhoferApproximation_radioButton.isChecked():
            diameter = fraunhoferDiameter
        else:
            diameter = sdf.getMieDiameter(dTheta,self.wavelength,self.relref,m)
        self.fibreDiameter_lineEdit.setText(format(diameter,'.2f'))
        return diameter

    def updateVLinePositions(self,ignoreM=[]):
        isFraun = self.fraunhoferApproximation_radioButton.isChecked()
        if type(ignoreM)==int: ignoreM = [ignoreM]
        for vLine in self.graphWidget.vLines():
            if vLine.m in ignoreM: continue
            self.adjustVLine(vLine.m,isFraun,self.cPos)
        

    def vLine_onDragged(self,vLine):
    # this function should be used with lambda function
        self.graphWidget.disableAutoRange()
        m = vLine.m
        if m==0:
            self.vLine0_onDragged()
            return
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ShiftModifier:
            #behaviour: move vLine[m], anchor vLine[0], move vLine[-m]
            if self.graphWidget.vLines[-m] is not None:
                self.graphWidget.vLines[-m].setValue(
                    2*self.graphWidget.vLines[0].value()-vLine.value())
        else:
            #default behaviour: move vLine[m], anchor vLine[-m], move vLine[0]
            if self.graphWidget.vLines[-m] is not None:
                self.graphWidget.vLines[0].setValue(
                    (vLine.value()+self.graphWidget.vLines[str(-m)].value())/2)
        self.cPos = self.graphWidget.vLines[0].value()
        self.updateDiameter(m)
        # self.updateVLinePositions(ignoreM=[-m,0,m])
        self.updateVLinesExist()
        
    def vLine0_onDragged(self):
        rPos_old = self.graphWidget.vLines[1].value()
        lPos_old = self.graphWidget.vLines[-1].value()
        cPos_new = self.graphWidget.vLines[0].value()
        self.cPos = cPos_new
        dx = cPos_new-0.5*(rPos_old+lPos_old)
        for vLine in self.graphWidget.vLines():
            vLine.setValue(vLine.value()+dx)
        self.updateVLinesExist()
        
    def vLine_onPositionChangeFinished(self):
        #self.graphWidget.enableAutoRange()
        pass
        
    # def leftLine_onDragged(self):
    #     modifiers = QtWidgets.QApplication.keyboardModifiers()
    #     if modifiers == QtCore.Qt.ShiftModifier:
    #         self.graphWidget.rightLine.setValue(
    #             2*self.graphWidget.centreLine.value()-self.graphWidget.leftLine.value())
    #     else:
    #         self.graphWidget.centreLine.setValue(
    #             (self.graphWidget.leftLine.value()+self.graphWidget.rightLine.value())/2)
    #     self.updateDiameter()
        
    # def rightLine_onDragged(self):
    #     modifiers = QtWidgets.QApplication.keyboardModifiers()
    #     if modifiers == QtCore.Qt.ShiftModifier:
    #         self.graphWidget.leftLine.setValue(
    #             2*self.graphWidget.centreLine.value()-self.graphWidget.rightLine.value())
    #     else:
    #         self.graphWidget.centreLine.setValue(
    #             (self.graphWidget.leftLine.value()+self.graphWidget.rightLine.value())/2)
    #     self.updateDiameter()

    
    # def graphWidget_onKeyPress(self,event):
    #     print(event.key())
    #     self.state = "SHIFT"
    
    # def graphWidget_onKeyRelease(self,event):
    #     self.state = None
    
# class dragLine(pg.InfiniteLine):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args,**kwargs)
    
#     def 

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui()
    ui.setupUi(MainWindow)
    ui.setupMeta()
    MainWindow.show()
    
    print(sys.argv)
    file=r'G:/My Drive/Msc. in Materials Engineering/Thesis/Tensile Specimens/Diffraction Files/621e55b6/257.csv'
    data = pd.read_csv(file).to_numpy()
    positions = data[:,0]
    intensities = data[:,1]
    data_length = data.shape[0]
    ui.plot(positions,np.log(intensities))

    sys.exit(app.exec_())
