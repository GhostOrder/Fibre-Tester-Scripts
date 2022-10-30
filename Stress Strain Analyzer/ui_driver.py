
from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
import pandas as pd
import numpy as np
from scipy.stats import linregress
from scipy.optimize import least_squares
from ui import Ui_MainWindow

UNSELECTED = 0
SELECTING_BACKGROUND = 1
SELECTING_SLOPE = 2

def __float__(val):
    try: return float(val)
    except: return None

class Ui(Ui_MainWindow):
    
    def __init__(self,xdata=None,ydata=None):
        super().__init__()
        self.gaugeLength = None
        self.correctedGaugeLength = None
        self.background = None
        self.maxStrength = None
        self.modulus = None
        self.offset = None
        self.slope = None
        self.interc = None
        self.status = UNSELECTED
        self.xValues = xdata
        self.yValues = ydata
    
    def setupMeta(self):
        self.graphWidget.setLabel("left","Stress (MPa)")
        self.graphWidget.setLabel("bottom","Strain (mm/mm)")
        self.graphWidget.plot(self.xValues,self.yValues,pen=pg.mkPen('w',width=0.5))
        self.graphWidget.mouseMoveProxy = None
        self.graphWidget.vBand_background = None
        self.graphWidget.vBand_slope = None
        self.selectBackground_pushButton.clicked.connect(self.selectBackground_pushButton_onClick)
        self.selectSlope_pushButton.clicked.connect(self.selectSlope_pushButton_onClick)
        self.gaugeLength = __float__(self.gaugeLength_lineEdit.text())
        
    
    def selectBackground_pushButton_onClick(self):
        active = self.selectBackground_pushButton.isChecked()
        if active:
            self.status = SELECTING_BACKGROUND
            if self.graphWidget.vBand_slope in self.graphWidget.items():
                self.graphWidget.removeItem(self.graphWidget.vBand_slope)
            self.graphWidget.scene().mousePressEvent = self.scene_background_onMousePress
            if self.graphWidget.vBand_background is not None:
                self.graphWidget.addItem(self.graphWidget.vBand_background)
            self.selectSlope_pushButton.setChecked(False)
        else:
            self.status = UNSELECTED
            self.graphWidget.scene().mousePressEvent = lambda ev: None
            self.graphWidget.removeItem(self.graphWidget.vBand_background)
            
    def selectSlope_pushButton_onClick(self):
        active = self.selectSlope_pushButton.isChecked()
        if active:
            self.status = SELECTING_SLOPE
            if self.graphWidget.vBand_background in self.graphWidget.items():
                self.graphWidget.removeItem(self.graphWidget.vBand_background)
            self.graphWidget.scene().mousePressEvent = self.scene_slope_onMousePress
            if self.graphWidget.vBand_slope is not None:
                self.graphWidget.addItem(self.graphWidget.vBand_slope)
            self.selectBackground_pushButton.setChecked(False)
        else:
            self.status = UNSELECTED
            self.graphWidget.scene().mousePressEvent = lambda ev: None
            self.graphWidget.removeItem(self.graphWidget.vBand_slope)
    
    def vBand_background_onRegionChangeFinished(self):
        bounds = self.graphWidget.vBand_background.getRegion()
        self.background = np.average(
            self.yValues[np.where((self.xValues>=bounds[0])&(self.xValues<=bounds[1]))])
        self.getResults()
        #self.selectBackground_pushButton.setChecked(False)
    
    def vBand_slope_onRegionChangeFinished(self):
        bounds = self.graphWidget.vBand_slope.getRegion()
        indices = np.where((self.xValues>=bounds[0])&(self.xValues<=bounds[1]))
        self.slope, self.interc, _, _, _ = linregress(self.xValues[indices],self.yValues[indices])
        self.getResults()
        #self.selectSlope_pushButton.setChecked(False)
        
    def scene_background_onMousePress(self,event):
        pos = event.scenePos()
        x0 = self.graphWidget.getPlotItem().vb.mapSceneToView(event.scenePos()).x()
        def mouseCoordinates(evt):
            pos = self.graphWidget.getPlotItem().vb.mapSceneToView(evt[0])
            return pos
        def mouseMoveProxy(evt):
            mousePoint = mouseCoordinates(evt)
            if self.graphWidget.vBand_background is not None:
                points = [x0,mousePoint.x()]
                self.graphWidget.vBand_background.setRegion((min(points),max(points)))
        if self.graphWidget.sceneBoundingRect().contains(pos):
            if self.graphWidget.vBand_background is None: 
                self.graphWidget.getPlotItem().vb.disableAutoRange()
                self.graphWidget.getPlotItem().vb.setMouseEnabled(False,False)
                self.graphWidget.vBand_background = pg.LinearRegionItem()
                self.graphWidget.vBand_background.setRegion((x0,x0))
                self.graphWidget.addItem(self.graphWidget.vBand_background)
                self.mouseMoveProxy = pg.SignalProxy(self.graphWidget.scene().sigMouseMoved,rateLimit=60,slot=mouseMoveProxy)
                self.graphWidget.scene().mouseReleaseEvent = self.scene_background_onMouseRelease
    
    def scene_background_onMouseRelease(self,event):
        pos = event.scenePos()
        if self.graphWidget.sceneBoundingRect().contains(pos):
            self.mouseMoveProxy.disconnect()
            self.vBand_background_onRegionChangeFinished()
            self.graphWidget.vBand_background.sigRegionChangeFinished.connect(self.vBand_background_onRegionChangeFinished)
            self.graphWidget.getPlotItem().vb.enableAutoRange()
            self.graphWidget.getPlotItem().vb.setMouseEnabled(True,True)
            self.graphWidget.scene().mouseReleaseEvent = lambda ev: None
            print(self.background)
            
    def scene_slope_onMousePress(self,event):
        pos = event.scenePos()
        x0 = self.graphWidget.getPlotItem().vb.mapSceneToView(event.scenePos()).x()
        def mouseCoordinates(evt):
            pos = self.graphWidget.getPlotItem().vb.mapSceneToView(evt[0])
            return pos
        def mouseMoveProxy(evt):
            mousePoint = mouseCoordinates(evt)
            if self.graphWidget.vBand_slope is not None:
                points = [x0,mousePoint.x()]
                self.graphWidget.vBand_slope.setRegion((min(points),max(points)))
        if self.graphWidget.sceneBoundingRect().contains(pos):
            if self.graphWidget.vBand_slope is None: 
                self.graphWidget.getPlotItem().vb.disableAutoRange()
                self.graphWidget.getPlotItem().vb.setMouseEnabled(False,False)
                self.graphWidget.vBand_slope = pg.LinearRegionItem()
                self.graphWidget.vBand_slope.setRegion((x0,x0))
                self.graphWidget.addItem(self.graphWidget.vBand_slope)
                self.mouseMoveProxy = pg.SignalProxy(self.graphWidget.scene().sigMouseMoved,rateLimit=60,slot=mouseMoveProxy)
                self.graphWidget.scene().mouseReleaseEvent = self.scene_slope_onMouseRelease
                
    def scene_slope_onMouseRelease(self,event):
        pos = event.scenePos()
        if self.graphWidget.sceneBoundingRect().contains(pos):
            self.mouseMoveProxy.disconnect()
            self.vBand_slope_onRegionChangeFinished()
            self.graphWidget.vBand_slope.sigRegionChangeFinished.connect(self.vBand_slope_onRegionChangeFinished)
            self.graphWidget.getPlotItem().vb.enableAutoRange()
            self.graphWidget.getPlotItem().vb.setMouseEnabled(True,True)
            self.graphWidget.scene().mouseReleaseEvent = lambda ev: None
            print(self.slope)
            
    def getResults(self):
        if self.background is not None and self.slope is not None:
            def estimator(xVals,params):
                cutoff = params[0]     
                y_est = np.empty_like(xVals)
                for i in range(xVals.size):
                    if xVals[i] <= cutoff: 
                        if xVals[i] < self.offset: y_est[i] = self.background
                        else: y_est[i] = self.interc + xVals[i]*self.slope
                    else: y_est[i] = self.background
                return y_est
            def residual(params, xVals, yVals):
                yVals_est = estimator(xVals,params)
                return yVals-yVals_est
            i_fit = np.where(self.xValues>=self.graphWidget.vBand_slope.getRegion()[0])
            xVals_fit = self.xValues[i_fit]
            yVals_fit = self.yValues[i_fit]
            self.offset = (self.background-self.interc)/self.slope
            i_maxStrength = np.where(self.yValues==max(self.yValues))[0][0]
            print(i_maxStrength)
            cutoff0 = self.xValues[i_maxStrength:][np.where(
                self.yValues[i_maxStrength:]<=0.5*(self.yValues[i_maxStrength]+self.background))][0]
            cutoff = least_squares(residual,cutoff0,args=(xVals_fit,yVals_fit)).x[0]
            self.maxStrength = self.interc + cutoff*self.slope - self.background
            self.correctedGaugeLength = self.gaugeLength*(1+self.offset)
            self.modulus = self.slope/1000/(1+self.offset)
            self.strength_value_label.setText('{:.2f} MPa'.format(self.maxStrength))
            self.modulus_value_label.setText('{:.2f} GPa'.format(self.modulus))
            self.correctedGaugeLength_value_label.setText('{:.2f} mm'.format(self.correctedGaugeLength))
            model_points = np.array([
                [self.offset,self.background],
                [cutoff,self.maxStrength+self.background],
                [cutoff,self.background],
                [self.xValues[-1],self.background]])
            if self.xValues[0] < self.offset:
                model_points = np.array([[self.xValues[0],self.background],*model_points])
            elif self.xValues[0] > self.offset:
                model_points[0,:] = np.array([self.xValues[0],self.interc+self.slope*self.xValues[0]])
            self.graphWidget.plot(model_points[:,0],model_points[:,1],pen=pg.mkPen('b',width=2))
    
    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    
    print(sys.argv)
    file=r'G:/My Drive/Msc. in Materials Engineering/Thesis/Tensile Specimens/Tensile Data/621e55b6/256.csv'
    data = pd.read_csv(file).to_numpy()
    strains = data[:,0]
    stresses = data[:,1]
    data_length = data.shape[0]
    ui = Ui(strains,stresses)
    ui.setupUi(MainWindow)
    ui.setupMeta()
    MainWindow.show()
    sys.exit(app.exec_())   
        
        
        