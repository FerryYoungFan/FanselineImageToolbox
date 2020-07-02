"""
Fanseline Image Toolbox
by FerryYoungFan - Twitter @FanKetchup / @FanBuckle

Required Modules:
Python: Ver 3.7.4
Numpy: Ver 1.18.4
OpenCV (cv2: opencv-python): Ver 4.2.0.34
PyQt5: Ver 5.15.0


Project start: June 12, 2020
Ver 1.0.0: June 27, 2020
Ver 1.0.1: July 2, 2020
"""

version = "1.0.1"
##auto-py-to-exe##

from FansWheels import *
from PyQtWheels import *
import numpy as np
import os
import pickle

from FansDehairFilter import FDehair
from GrabCut import GCut
from MagicWand import MWand
from SkinSelect import SkinSelect
from CommonSelection import CSelect
from AdjustMask import MaskAdj
from AdjustImage import ImageAdj
from InPaint import InPaint
from FilterSets import FilterSets
from LanguagePack import *

lang = None


def cleanAll():
    global img_input, img_current, img_view, filepath, fdpack, gbcpack, mwdpack, sksepack, csepack, \
        madjpack, iadjpack, inptpack, filtpack, mask_current, mask_view, mask_check, drawMask, fastPreview, \
        HASMASK, lineColor, lineThick, maskUndoStack, imgUndoStack, maskUndoPtr, imgUndoPtr, maxUndoSize, \
        appMainWindow, tempfilepath, taskState
    taskState = 0
    img_input, img_current, img_view = None, None, None
    fdpack, gbcpack, mwdpack, sksepack, csepack = None, None, None, None, None
    madjpack, iadjpack, inptpack, filtpack = None, None, None, None
    mask_current, mask_view, mask_check = None, None, None
    drawMask, fastPreview = None, None
    HASMASK = False
    lineColor, lineThick = (255, 255, 255), 3
    maskUndoStack, imgUndoStack = [], []
    maskUndoPtr, imgUndoPtr = 0, 0
    appMainWindow.showMenuWindow()
    appMainWindow.viewer.stopDrawing()


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.windowName = lang["mainWindowName"]
        self.setWindowTitle(self.windowName)
        setWindowIcons(self)
        self.closeAll = False
        self.viewer = PhotoViewer(self)

        # UI Frame
        menuSize_L = 220
        menuSize_R = 180
        left = QtWidgets.QFrame(self)
        right = QtWidgets.QFrame(self)
        self.middle = QtWidgets.QFrame(self)
        self.middle.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.middle.setStyleSheet(viewerStyle)
        mainBox = QtWidgets.QHBoxLayout(self)
        mainBox.setSpacing(0)
        mainBox.setContentsMargins(0, 8, 0, 8)
        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(left)
        splitter.addWidget(self.middle)
        splitter.addWidget(right)
        QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create('Cleanlooks'))
        mainBox.addWidget(splitter)
        splitter.setStretchFactor(0, -1)
        splitter.setStretchFactor(1, 1)
        splitter.setStretchFactor(2, -1)
        splitter.setSizes([menuSize_L, 1, menuSize_R])

        self.window_menu_l = WindowMenu_L(self)
        self.window_menu_r = WindowMenu_R(self)

        # Small Windows
        self.window_msg = WindowMsg(self)
        self.window_help = WindowHelp(self)
        self.window_asksave = WindowAsksave(self)
        self.window_askresize = WindowAskresize(self)
        self.window_askquit = WindowAskquit(self)
        self.window_settings = WindowSettings(self)

        # Mask Tools
        self.window_gbcut_l = WindowGbcut_L(self)
        self.window_gbcut_r = WindowGbcut_R(self)
        self.window_mwd_l = WindowMwd_L(self)
        self.window_mwd_r = WindowMwd_R(self)
        self.window_skinselect_l = WindowSkinSelect_L(self)
        self.window_skinselect_r = WindowSkinSelect_R(self)
        self.window_cselect_l = WindowCSelect_L(self)
        self.window_cselect_r = WindowCSelect_R(self)
        self.window_adjm_l = WindowAdjMask_L(self)
        self.window_adjm_r = WindowAdjMask_R(self)

        # Image Processing Tools
        self.window_adji_l = WindowAdjImage_L(self)
        self.window_adji_r = WindowAdjImage_R(self)
        self.window_dehair_l = WindowDehair_L(self)
        self.window_dehair_r = WindowDehair_R(self)
        self.window_inpt_l = WindowInpaint_L(self)
        self.window_inpt_r = WindowInpaint_R(self)
        self.window_polish_l = WindowPolish_L(self)
        self.window_polish_r = WindowPolish_R(self)
        self.window_glow_l = WindowGlow_L(self)
        self.window_glow_r = WindowGlow_R(self)
        self.window_filters_l = WindowFilters_L(self)
        self.window_filters_r = WindowFilters_R(self)
        self.window_save_l = WindowSave_L(self)
        self.window_save_r = WindowSave_R(self)

        # Arrange layout
        VBlayout_l = QtWidgets.QVBoxLayout(left)
        VBlayout_l.setSpacing(0)
        VBlayout_l.setContentsMargins(0, 0, 0, 0)
        VBlayout_l.addWidget(self.window_menu_l)
        VBlayout_l.addWidget(self.window_gbcut_l)
        VBlayout_l.addWidget(self.window_mwd_l)
        VBlayout_l.addWidget(self.window_skinselect_l)
        VBlayout_l.addWidget(self.window_cselect_l)
        VBlayout_l.addWidget(self.window_adjm_l)

        VBlayout_l.addWidget(self.window_adji_l)
        VBlayout_l.addWidget(self.window_dehair_l)
        VBlayout_l.addWidget(self.window_inpt_l)
        VBlayout_l.addWidget(self.window_save_l)
        VBlayout_l.addWidget(self.window_polish_l)
        VBlayout_l.addWidget(self.window_glow_l)
        VBlayout_l.addWidget(self.window_filters_l)
        VBlayout_l.addWidget(self.window_settings)
        # ---------------------------------------------------------
        VBlayout_m = QtWidgets.QVBoxLayout(self.middle)
        VBlayout_m.setSpacing(0)
        VBlayout_m.setContentsMargins(0, 0, 0, 0)
        VBlayout_m.addWidget(self.viewer)
        # ---------------------------------------------------------
        VBlayout_r = QtWidgets.QVBoxLayout(right)
        VBlayout_r.setSpacing(0)
        VBlayout_r.setContentsMargins(0, 0, 0, 0)
        VBlayout_r.addWidget(self.window_menu_r)
        VBlayout_r.addWidget(self.window_gbcut_r)
        VBlayout_r.addWidget(self.window_mwd_r)
        VBlayout_r.addWidget(self.window_skinselect_r)
        VBlayout_r.addWidget(self.window_cselect_r)
        VBlayout_r.addWidget(self.window_adjm_r)

        VBlayout_r.addWidget(self.window_adji_r)
        VBlayout_r.addWidget(self.window_dehair_r)
        VBlayout_r.addWidget(self.window_inpt_r)
        VBlayout_r.addWidget(self.window_save_r)
        VBlayout_r.addWidget(self.window_polish_r)
        VBlayout_r.addWidget(self.window_glow_r)
        VBlayout_r.addWidget(self.window_filters_r)

        self.setStyleSheet(stylepack)

        self.showMenuWindow()
        self.undoButtonCheck()
        self.setAllButtons(False)

    def showMenuWindow(self):
        self.window_gbcut_l.hide()
        self.window_gbcut_r.hide()
        self.window_mwd_l.hide()
        self.window_mwd_r.hide()
        self.window_skinselect_l.hide()
        self.window_skinselect_r.hide()
        self.window_cselect_l.hide()
        self.window_cselect_r.hide()
        self.window_adjm_l.hide()
        self.window_adjm_r.hide()

        self.window_adji_l.hide()
        self.window_adji_r.hide()
        self.window_dehair_l.hide()
        self.window_dehair_r.hide()
        self.window_inpt_l.hide()
        self.window_inpt_r.hide()
        self.window_save_l.hide()
        self.window_save_r.hide()
        self.window_polish_l.hide()
        self.window_polish_r.hide()
        self.window_glow_l.hide()
        self.window_glow_r.hide()
        self.window_filters_l.hide()
        self.window_filters_r.hide()

        self.window_settings.hide()

        self.window_menu_l.show()
        self.window_menu_r.show()

        self.crosshairCursor(False)

    def loadImage(self, file_=None):
        global maskUndoStack, imgUndoStack
        if file_ is None:
            return
        if len(maskUndoStack) + len(imgUndoStack) > 0:
            self.window_asksave.show(file_)
        else:
            self.openImage(file_)

    def openImage(self, file_):
        try:
            img = cv_imread(file_)
            if img is None:
                raise FileNotFoundError
        except FileNotFoundError:
            self.window_msg.show(lang["Read File Error"], lang["not supported"])
        else:
            print("Loading Image")
            global filepath, tempfilepath
            filepath, tempfilepath = file_, file_

            if img.shape[0] * img.shape[1] > 3264 * 2448:
                self.window_askresize.show(img)
            self.initImage(img)

    def initImage(self, img=None):
        self.isBusy()
        global img_input, img_current, mask_current, mask_view
        cleanAll()
        self.window_menu_l.btn_dseall.setEnabled(False)
        self.window_menu_l.btn_adjm.setEnabled(False)
        self.window_menu_l.btn_showm.setEnabled(False)
        img_input = img
        img_current = blend_4c(img_input)
        mask_view = img_current.copy()
        mask_current = np.zeros(img_input.shape[:2], dtype=np.uint8)
        self.qt_imshow(img_current)
        self.viewer.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.viewer.fitInView()
        self.hist_show(img_current)
        self.undoButtonCheck()
        self.windowName = lang["mainWindowName"] + showSize(img_input)
        self.setWindowTitle(self.windowName)
        self.viewer.mode = 0
        self.viewer.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.setAllButtons(True)
        self.window_menu_l.btn_cmp.setEnabled(False)
        self.isBusy(False)

    def writeImage(self, img=None, savetype="jpg", jpgq=100, suffix="_FITB"):
        global img_current, filepath
        fpath, fname = os.path.split(filepath)
        fname = os.path.splitext(fname)[0]
        if img is None:
            img = img_current
        try:
            if savetype == "jpg":
                newpath = os.path.join(fpath, fname + suffix + ".jpg")
                file_, filetype = QtWidgets.QFileDialog.getSaveFileName(self,
                                                                        lang["Save as JPG"],
                                                                        newpath,
                                                                        lang["JPG Files (*.jpg)"])
                if file_:
                    cv_imsave(img, file_, jpgq)
            elif savetype == "png":
                newpath = os.path.join(fpath, fname + suffix + ".png")
                print(lang["Save as PNG"], newpath)
                file_, filetype = QtWidgets.QFileDialog.getSaveFileName(self,
                                                                        lang["Save as PNG"],
                                                                        newpath,
                                                                        lang["PNG Files (*.png)"])
                if file_:
                    cv_imsave(img, file_)
            elif savetype == "bmp":
                newpath = os.path.join(fpath, fname + suffix + ".bmp")
                file_, filetype = QtWidgets.QFileDialog.getSaveFileName(self,
                                                                        lang["Save as BMP"],
                                                                        newpath,
                                                                        lang["BMP Files (*.bmp)"])
                if file_:
                    cv_imsave(img, file_)
        except:
            self.window_msg.show(lang["File Save Error"], lang["Unable to save this image!"])
        else:
            if file_:
                self.window_msg.show(lang["File Saved"], lang["Your image has been saved."])

    def qt_imshow(self, img):
        self.viewer.setPhoto(cv2qtPhoto(img))

    def hist_show(self, img=None):
        result = getHist(img)
        if self.window_menu_r.isVisible():
            self.window_menu_r.hist_view.setPixmap(cv2qtPhoto(result))
        elif self.window_adji_r.isVisible():
            self.window_adji_r.hist_view.setPixmap(cv2qtPhoto(result))
        elif self.window_dehair_r.isVisible():
            self.window_dehair_r.hist_view.setPixmap(cv2qtPhoto(result))
        elif self.window_inpt_r.isVisible():
            self.window_inpt_r.hist_view.setPixmap(cv2qtPhoto(result))
        elif self.window_polish_r.isVisible():
            self.window_polish_r.hist_view.setPixmap(cv2qtPhoto(result))
        elif self.window_glow_r.isVisible():
            self.window_glow_r.hist_view.setPixmap(cv2qtPhoto(result))
        elif self.window_filters_r.isVisible():
            self.window_filters_r.hist_view.setPixmap(cv2qtPhoto(result))

    def resizeEvent(self, event):
        if self.middle.width() > 0:
            self.viewer.fitInView()
        super(Window, self).resizeEvent(event)

    def newMaskCanvas(self, mode=1):
        global img_current, img_view, drawMask, fastPreview, gbcpack
        drawMask = np.zeros([img_current.shape[0], img_current.shape[1]], np.uint8)
        fastPreview = img_view.copy()

    def drawMaskCanvas(self, oldx, oldy, newx, newy, x0=0, y0=0, mode=1):
        global img_current, img_view, drawMask, gbcpack, fastPreview, lineColor, lineThick, csepack, inptpack
        if mode == 1:  # Grabcut Rectangle
            fastPreview = img_view.copy()
            cv2.rectangle(fastPreview, (x0, y0), (newx, newy), (0, 0, 255, 255), self.viewer.getSelectBrushSize())
            self.qt_imshow(fastPreview)
        elif mode == 2:  # Grabcut Foreground
            cv2.line(drawMask, (oldx, oldy), (newx, newy), 255, lineThick)
            cv2.line(fastPreview, (oldx, oldy), (newx, newy), lineColor, lineThick)
            self.qt_imshow(fastPreview)
        elif mode == 3:  # Grabcut Background
            cv2.line(drawMask, (oldx, oldy), (newx, newy), 255, lineThick)
            cv2.line(fastPreview, (oldx, oldy), (newx, newy), lineColor, lineThick)
            self.qt_imshow(fastPreview)
        elif mode in [7, 8]:
            csepack.pushpoint(newx, newy)
            self.qt_imshow(csepack.getView())
        elif mode == 9:
            inptpack.drawPoint(newx, newy)
            self.qt_imshow(inptpack.getView())

    def showDrawMask(self, oldx, oldy, newx, newy, x0=0, y0=0, mode=1):
        global img_current, img_view, drawMask, gbcpack, mask_view, csepack, inptpack
        if mode == 1:
            gbcpack.setRect(x0, y0, newx, newy)
            if gbcpack.newrect:
                self.isBusy()
                gbcpack.update()
                if gbcpack.firstRun:
                    self.window_gbcut_l.disableButtons()
                    self.window_gbcut_r.disableButtons()
                else:
                    self.window_gbcut_l.enableButtons()
                    self.window_gbcut_r.enableButtons()
                self.isBusy(False)
        elif mode == 2:
            self.isBusy()
            gbcpack.addMask(drawMask)
            gbcpack.update()
            self.window_gbcut_l.enableButtons()
            self.window_gbcut_r.enableButtons()
            self.isBusy(False)
        elif mode == 3:
            self.isBusy()
            gbcpack.removeMask(drawMask)
            gbcpack.update()
            self.window_gbcut_l.enableButtons()
            self.window_gbcut_r.enableButtons()
            self.isBusy(False)
        if mode in [1, 2, 3]:
            self.isBusy()
            img_view = preview_mask(mask_view, gbcpack.getMask())
            self.qt_imshow(img_view)
            self.activateWindow()
            self.isBusy(False)
        elif mode in [7, 8]:
            self.isBusy()
            csepack.update()
            self.qt_imshow(csepack.getView())
            self.window_cselect_l.enableButtons()
            self.window_cselect_l.checkUndo()
            self.window_cselect_r.enableButtons()
            self.isBusy(False)
        elif mode == 9:
            self.isBusy()
            inptpack.update()
            self.window_inpt_r.enableButtons()
            self.window_inpt_l.checkUndo()
            self.qt_imshow(inptpack.getView())
            self.isBusy(False)

    def setMagicWand(self, x, y):
        global mask_view, mwdpack, taskState, img_view
        self.isBusy()
        if taskState in [4, 5]:
            mwdpack.update(x, y, self.window_mwd_l.sl_ldiff.value(), self.window_mwd_l.sl_udiff.value(), False)
            if taskState == 4:
                taskState = 5
                self.window_mwd_r.enableButtons()
        elif taskState == 6:
            mwdpack.update(x, y, self.window_mwd_l.sl_ldiff.value(), self.window_mwd_l.sl_udiff.value(), True)
        self.window_mwd_l.updateEdge()
        self.isBusy(False)

    def setColorRange(self, x, y):
        self.isBusy()
        self.window_skinselect_l.setPoint(x, y)
        self.isBusy(False)

    def startInpaint(self, x, y):
        global inptpack
        inptpack.startDrawing(x, y)
        self.qt_imshow(inptpack.view)

    def setCommonSelect(self, x, y):
        global csepack
        csepack.startpoint(x, y)
        self.qt_imshow(csepack.getView())
        self.viewer.startDrawing(7)
        if csepack.mode in [2,3,4]:
            csepack.lineThick = self.viewer.getSelectBrushSize()

    def updateImg(self, img):
        global imgUndoStack, img_current, mask_current, mask_view, imgUndoPtr
        imgUndoStack.append(img_current)
        imgUndoPtr += 1
        if imgUndoPtr > maxUndoSize:
            imgUndoPtr -= 1
            del imgUndoStack[0]
        del imgUndoStack[imgUndoPtr:]
        img_current = img
        mask_view = preview_mask(img_current, mask_current, (240, 32, 16), 0.35)
        self.undoButtonCheck()
        self.window_menu_l.btn_cmp.setEnabled(True)

    def updateMask(self, mask):
        global maskUndoStack, mask_current, mask_view, mask_check, maskUndoPtr, maxUndoSize
        maskUndoStack.append(mask_current)
        maskUndoPtr += 1
        if maskUndoPtr > maxUndoSize:
            maskUndoPtr -= 1
            del maskUndoStack[0]
        del maskUndoStack[maskUndoPtr:]
        mask_current = mask
        if len(mask_current[mask_current > 0]) > 0:
            mask_view = preview_mask(img_current, mask_current, (240, 32, 16), 0.35)
            self.window_menu_l.btn_dseall.setEnabled(True)
            self.window_menu_l.btn_adjm.setEnabled(True)
            self.window_menu_l.btn_showm.setEnabled(True)
        else:
            mask_view = img_current
            self.window_menu_l.btn_dseall.setEnabled(False)
            self.window_menu_l.btn_adjm.setEnabled(False)
            self.window_menu_l.btn_showm.setEnabled(False)
        mask_check = None
        self.qt_imshow(mask_view)
        self.undoButtonCheck()
        self.window_menu_l.btn_cmp.setEnabled(True)

    def isBusy(self, busyFlag=True):
        if busyFlag:
            self.setWindowTitle("".join([self.windowName, lang["Computing"]]))
            QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        else:
            QApplication.restoreOverrideCursor()
            self.setWindowTitle(self.windowName)

    def crosshairCursor(self, Flag=True):
        if Flag:
            self.viewer.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        else:
            self.viewer.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

    def hideMenuWindow(self):
        self.window_menu_l.hide()
        self.window_menu_r.hide()

    def undoButtonCheck(self):
        global imgUndoStack, imgUndoPtr, maskUndoStack, maskUndoPtr
        if imgUndoPtr <= 0:
            self.window_menu_r.btn_undo.setEnabled(False)
        else:
            self.window_menu_r.btn_undo.setEnabled(True)
        if imgUndoPtr >= len(imgUndoStack) - 1:
            self.window_menu_r.btn_redo.setEnabled(False)
        else:
            self.window_menu_r.btn_redo.setEnabled(True)

        if maskUndoPtr <= 0:
            self.window_menu_l.btn_undom.setEnabled(False)
        else:
            self.window_menu_l.btn_undom.setEnabled(True)
        if maskUndoPtr >= len(maskUndoStack) - 1:
            self.window_menu_l.btn_redom.setEnabled(False)
        else:
            self.window_menu_l.btn_redom.setEnabled(True)

    def closeEvent(self, event):
        global maskUndoStack, imgUndoStack
        if len(maskUndoStack) + len(imgUndoStack) > 0:
            if self.closeAll:
                self.closeAllWindows()
                event.accept()
            else:
                event.ignore()
                self.window_askquit.show()
        else:
            self.closeAllWindows()
            event.accept()

    def closeAllWindows(self):
        self.window_msg.close()
        self.window_help.close()
        self.window_asksave.close()
        self.window_askresize.close()
        self.window_askquit.close()

    def showHelloScreen(self):
        try:
            img = cv_imread(r"./GUI/Image/HelloScreen.png")
            if img is None:
                raise FileNotFoundError
        except FileNotFoundError:
            print("No Hello Screen Image")
        else:
            self.qt_imshow(img)
            self.viewer.fitInView()
            self.viewer.mode = -64
            self.viewer.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self.viewer.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
            self.hist_show(None)
            self.windowName = lang["mainWindowName"] + " - " + lang["Welcome!"]
            self.setWindowTitle(self.windowName)

    def setAllButtons(self, flag=True):
        self.window_menu_r.btn_dehair.setEnabled(flag)
        self.window_menu_r.btn_adjcolor.setEnabled(flag)
        self.window_menu_r.btn_inpt.setEnabled(flag)
        self.window_menu_r.btn_polish.setEnabled(flag)
        self.window_menu_r.btn_glow.setEnabled(flag)
        self.window_menu_r.btn_filters.setEnabled(flag)
        self.window_menu_r.btn_save.setEnabled(flag)
        self.window_menu_l.btn_cmp.setEnabled(flag)
        self.window_menu_l.btn_skinselect.setEnabled(flag)
        self.window_menu_l.btn_gbcut.setEnabled(flag)
        self.window_menu_l.btn_mwd.setEnabled(flag)
        self.window_menu_l.btn_cselect.setEnabled(flag)
        self.window_menu_l.btn_seinv.setEnabled(flag)
        if not flag:
            self.window_menu_l.btn_showm.setEnabled(flag)
            self.window_menu_l.btn_adjm.setEnabled(flag)
            self.window_menu_l.btn_dseall.setEnabled(flag)


class WindowMenu_L(QtWidgets.QWidget):
    def __init__(self, mainWindow):
        super(WindowMenu_L, self).__init__()
        self.mainWindow = mainWindow
        self.btn_setting = genButton(self, lang["Settings & Help"], None, self.btn_setting_release, "H")
        self.btn_cmp = genButton(self, lang["Compare"], self.show_input, self.show_output, None, style=2)
        self.btn_showm = genButton(self, lang["Show Mask"], self.show_mask, self.hide_mask, None, style=2)
        self.btn_skinselect = genButton(self, lang["Color Range"], None, self.btn_skinselect_release, None)
        self.btn_gbcut = genButton(self, lang["Grabcut"], None, self.btn_gbcut_release, None)
        self.btn_mwd = genButton(self, lang["Magic Wand"], None, self.btn_mwd_release, None)
        self.btn_cselect = genButton(self, lang["Select Tools"], None, self.btn_cselect_release, None)
        self.btn_adjm = genButton(self, lang["Adjust Selection"], None, self.btn_adjm_release, None)
        self.btn_dseall = genButton(self, lang["Deselect All"], None, self.btn_dseall_release, "Ctrl+D", style=3)
        self.btn_seinv = genButton(self, lang["Select Inverse"], None, self.btn_seinv_release, "Ctrl+I", style=5)
        self.btn_undom = genButton(self, lang["Undo Mask"], None, self.btn_undom_release, "Ctrl+Shift+Z", style=3)
        self.btn_redom = genButton(self, lang["Redo Mask"], None, self.btn_redom_release, "Ctrl+Shift+Y", style=4)

        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.setAlignment(QtCore.Qt.AlignTop)
        # VBlayout.addWidget(genLabel(self, "Select Tools"))
        VBlayout.addWidget(self.btn_setting)
        VBlayout.addWidget(genLabel(self, lang["Switch View"], 4))
        VBlayout.addWidget(self.btn_cmp)
        VBlayout.addWidget(self.btn_showm)
        VBlayout.addWidget(genLabel(self, lang["Create Local Mask"], 4))
        VBlayout.addWidget(self.btn_gbcut)
        VBlayout.addWidget(self.btn_skinselect)
        VBlayout.addWidget(self.btn_mwd)
        VBlayout.addWidget(self.btn_cselect)
        VBlayout.addWidget(genLabel(self, lang["Adjust Global Mask"], 4))
        VBlayout.addWidget(self.btn_adjm)
        VBlayout.addWidget(self.btn_seinv)
        VBlayout.addWidget(self.btn_dseall)

        HBlayout = QtWidgets.QHBoxLayout()
        HBlayout.addWidget(self.btn_undom)
        HBlayout.addWidget(self.btn_redom)
        VBlayout.addLayout(HBlayout)

    def show_input(self):
        global fdpack, img_input
        self.mainWindow.qt_imshow(img_input)
        self.mainWindow.hist_show(img_input)

    def show_output(self):
        global img_current
        self.mainWindow.qt_imshow(img_current)
        self.mainWindow.hist_show(img_current)

    def show_mask(self):
        global mask_current, img_current, mask_check
        if mask_check is None:
            mask_check = blend_4c(img_current, mask_current)
        self.mainWindow.qt_imshow(mask_check)

    def hide_mask(self):
        global mask_view
        self.mainWindow.qt_imshow(mask_view)

    def btn_skinselect_release(self):
        global taskState, sksepack, img_current, mask_view
        taskState = 10
        sksepack = SkinSelect(img_current)

        self.mainWindow.hideMenuWindow()
        self.mainWindow.window_skinselect_l.show()
        self.mainWindow.window_skinselect_r.show()
        self.mainWindow.viewer.startDrawing(mode=taskState)
        self.mainWindow.qt_imshow(mask_view)
        self.mainWindow.crosshairCursor()
        self.mainWindow.window_skinselect_r.enableButtons()

    def btn_gbcut_release(self):
        global gbcpack, img_current, img_view, mask_view, lineThick, taskState
        gbcpack = GCut(img_current)
        self.mainWindow.window_gbcut_l.updateEdge()
        taskState = 1
        img_view = mask_view.copy()

        lineThick = self.mainWindow.window_gbcut_l.sl_brush.value()
        self.mainWindow.hideMenuWindow()
        self.mainWindow.window_gbcut_l.disableButtons()
        self.mainWindow.window_gbcut_l.show()
        self.mainWindow.window_gbcut_r.disableButtons()
        self.mainWindow.window_gbcut_r.show()
        self.mainWindow.viewer.startDrawing(mode=taskState)
        self.mainWindow.qt_imshow(mask_view)
        self.mainWindow.window_gbcut_l.sl_iter_release()
        self.mainWindow.crosshairCursor()

    def btn_mwd_release(self):
        global taskState, mwdpack, img_current
        taskState = 4
        mwdpack = MWand(img_current, None, None,
                        self.mainWindow.window_mwd_l.sl_ldiff.value(),
                        self.mainWindow.window_mwd_l.sl_udiff.value())
        self.mainWindow.viewer.startDrawing(mode=taskState)
        self.mainWindow.window_mwd_r.enableButtons()
        self.mainWindow.hideMenuWindow()
        self.mainWindow.window_mwd_l.show()
        self.mainWindow.window_mwd_r.show()
        self.mainWindow.qt_imshow(mask_view)
        self.mainWindow.crosshairCursor()

    def btn_adjm_release(self):
        global madjpack, img_current, mask_current, mask_view
        madjpack = MaskAdj(img_current, mask_current)
        self.mainWindow.window_adjm_l.resetSliders()
        madjpack.edgeModify(self.mainWindow.window_adjm_l.sl_grow.value(),
                            self.mainWindow.window_adjm_l.sl_contract.value(),
                            self.mainWindow.window_adjm_l.sl_feather.value())
        self.mainWindow.qt_imshow(madjpack.getView())
        self.mainWindow.hideMenuWindow()
        self.mainWindow.window_adjm_l.show()
        self.mainWindow.window_adjm_r.show()

    def btn_seinv_release(self):
        global mask_current
        tempmask = mask_current.copy()
        tempmask = 255 - tempmask
        self.mainWindow.updateMask(tempmask)

    def btn_dseall_release(self):
        global mask_current, img_current
        if len(mask_current[mask_current > 0]) > 0:
            tempmask = np.zeros((mask_current.shape[0], mask_current.shape[1]), dtype=np.uint8)
            self.mainWindow.updateMask(tempmask)

    def btn_cselect_release(self):
        global csepack, mask_view, taskState,maxUndoSize
        csepack = CSelect(mask_view)
        csepack.maxUndoSize = maxUndoSize
        csepack.setMode(4)
        taskState = 7
        self.mainWindow.window_cselect_l.enableButtons()
        self.mainWindow.window_cselect_r.enableButtons()
        self.mainWindow.viewer.mode = taskState
        self.mainWindow.viewer.startDrawing(mode=taskState)
        self.mainWindow.qt_imshow(mask_view)
        self.mainWindow.hideMenuWindow()
        self.mainWindow.window_cselect_l.show()
        self.mainWindow.window_cselect_r.show()
        self.mainWindow.crosshairCursor()
        self.mainWindow.window_cselect_l.checkUndo(True)

    def btn_undom_release(self):
        global maskUndoStack, mask_current, mask_view, mask_check, maxUndoSize, maskUndoPtr
        if maskUndoPtr > 0:
            self.mainWindow.isBusy()
            if maskUndoPtr >= len(maskUndoStack):
                maskUndoStack.append(mask_current)
            else:
                maskUndoStack[maskUndoPtr] = mask_current
            maskUndoPtr -= 1
            mask_current = maskUndoStack[maskUndoPtr]
            mask_check = None
            if len(mask_current[mask_current > 0]) > 0:
                mask_view = preview_mask(img_current, mask_current, (240, 32, 16), 0.35)
                self.btn_dseall.setEnabled(True)
                self.btn_adjm.setEnabled(True)
                self.btn_showm.setEnabled(True)
            else:
                mask_view = img_current
                self.btn_dseall.setEnabled(False)
                self.btn_adjm.setEnabled(False)
                self.btn_showm.setEnabled(False)
            self.mainWindow.qt_imshow(mask_view)
            self.mainWindow.isBusy(None)
        self.mainWindow.undoButtonCheck()

    def btn_redom_release(self):
        global maskUndoStack, mask_current, mask_view, mask_check, maxUndoSize, maskUndoPtr
        if maskUndoPtr + 1 < len(maskUndoStack):
            self.mainWindow.isBusy()
            maskUndoPtr += 1
            mask_current = maskUndoStack[maskUndoPtr]
            mask_check = None
            if len(mask_current[mask_current > 0]) > 0:
                mask_view = preview_mask(img_current, mask_current, (240, 32, 16), 0.35)
                self.btn_dseall.setEnabled(True)
                self.btn_adjm.setEnabled(True)
                self.btn_showm.setEnabled(True)
            else:
                mask_view = img_current
                self.btn_dseall.setEnabled(False)
                self.btn_adjm.setEnabled(False)
                self.btn_showm.setEnabled(False)
            self.mainWindow.qt_imshow(mask_view)
            self.mainWindow.isBusy(None)
        self.mainWindow.undoButtonCheck()

    def btn_setting_release(self):
        self.mainWindow.hideMenuWindow()
        self.mainWindow.window_settings.show()


class WindowMenu_R(QtWidgets.QWidget):
    def __init__(self, mainWindow):
        super(WindowMenu_R, self).__init__()
        self.mainWindow = mainWindow

        self.btn_dehair = genButton(self, lang["Dehair"], None, self.btn_dehair_release, None)
        self.btn_adjcolor = genButton(self, lang["Adjust Color"], None, self.btn_adjcolor_release, "Ctrl+U")
        self.btn_inpt = genButton(self, lang["Inpaint"], None, self.btn_inpt_release, None)
        self.btn_polish = genButton(self, lang["Smooth Skin"], None, self.btn_polish_release, None)
        self.btn_glow = genButton(self, lang["Glow Blur"], None, self.btn_glow_release, None)
        self.btn_filters = genButton(self, lang["Classic Filters"], None, self.btn_filters_release, None)
        self.btn_load = genButton(self, lang["Load Image"], None, self.btn_load_release, "Ctrl+O", style=2)
        self.btn_save = genButton(self, lang["Save Image"], None, self.btn_save_release, "Ctrl+S", style=2)
        self.btn_undo = genButton(self, lang["Undo"], None, self.btn_undo_release, "Ctrl+Z", style=3)
        self.btn_redo = genButton(self, lang["Redo"], None, self.btn_redo_release, "Ctrl+Y", style=4)

        self.hist_view = genHist(self)  # Histogram

        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.setAlignment(QtCore.Qt.AlignTop)
        VBlayout.addWidget(self.hist_view)
        # VBlayout.addWidget(genLabel(self, "Process Tools"))
        VBlayout.addWidget(genLabel(self, lang["Filters"], 4))
        VBlayout.addWidget(self.btn_dehair)
        VBlayout.addWidget(self.btn_polish)
        VBlayout.addWidget(self.btn_glow)
        VBlayout.addWidget(self.btn_filters)
        VBlayout.addWidget(genLabel(self, lang["Tools"], 4))
        VBlayout.addWidget(self.btn_adjcolor)
        VBlayout.addWidget(self.btn_inpt)
        VBlayout.addWidget(genLabel(self, lang["Save & Load"], 4))
        VBlayout.addWidget(self.btn_load)
        VBlayout.addWidget(self.btn_save)
        HBlayout = QtWidgets.QHBoxLayout()
        HBlayout.addWidget(self.btn_undo)
        HBlayout.addWidget(self.btn_redo)
        VBlayout.addLayout(HBlayout)

    def btn_load_release(self):
        file_, filetype = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                lang["Select an Image"],
                                                                "",
                                                                lang["Image File Sets"])
        if not file_:
            print("No File!")
        else:
            self.mainWindow.loadImage(file_)

    def btn_save_release(self):
        self.mainWindow.hideMenuWindow()
        self.mainWindow.window_save_l.show()
        self.mainWindow.window_save_r.show()

    def btn_dehair_release(self):
        global fdpack, img_current, mask_current
        self.mainWindow.isBusy()
        fdpack = FDehair(img_current, mask_current)
        self.mainWindow.window_dehair_l.sl_mediank.reset(1, fdpack.max_mediank, 2, fdpack.mediank)
        self.mainWindow.window_dehair_r.btn_reset_release()
        self.mainWindow.qt_imshow(fdpack.result())
        self.mainWindow.hideMenuWindow()
        self.mainWindow.window_dehair_l.show()
        self.mainWindow.window_dehair_r.show()
        self.mainWindow.hist_show(fdpack.result())
        self.mainWindow.isBusy(False)

    def btn_polish_release(self):
        global img_current, filtpack, mask_current
        filtpack = FilterSets(img_current, mask_current)
        self.mainWindow.hideMenuWindow()
        self.mainWindow.window_polish_l.show()
        self.mainWindow.window_polish_r.show()
        self.mainWindow.window_polish_l.updateImg()

    def btn_glow_release(self):
        global img_current, filtpack, mask_current
        filtpack = FilterSets(img_current, mask_current)
        self.mainWindow.qt_imshow(filtpack.getImage())
        self.mainWindow.hideMenuWindow()
        self.mainWindow.window_glow_l.show()
        self.mainWindow.window_glow_r.show()
        self.mainWindow.window_glow_l.updateImg()

    def btn_filters_release(self):
        global img_current, filtpack, mask_current
        filtpack = FilterSets(img_current, mask_current)
        self.mainWindow.qt_imshow(filtpack.getImage())
        self.mainWindow.hideMenuWindow()
        self.mainWindow.window_filters_l.show()
        self.mainWindow.window_filters_r.show()
        self.mainWindow.hist_show(img_current)
        self.mainWindow.window_filters_l.resetAll()

    def btn_adjcolor_release(self):
        global img_current, mask_current, iadjpack
        iadjpack = ImageAdj(img_current, mask_current)
        self.mainWindow.window_adji_r.btn_reset_release()
        self.mainWindow.qt_imshow(iadjpack.getImage())
        self.mainWindow.hideMenuWindow()
        self.mainWindow.window_adji_l.show()
        self.mainWindow.window_adji_r.show()
        self.mainWindow.hist_show(img_current)

    def btn_inpt_release(self):
        global img_current, inptpack, taskState, maxUndoSize
        inptpack = InPaint(img_current)
        inptpack.maxUndoSize = maxUndoSize
        taskState = 9
        self.mainWindow.viewer.startDrawing(mode=taskState)
        self.mainWindow.qt_imshow(img_current)
        self.mainWindow.hideMenuWindow()
        self.mainWindow.window_inpt_l.show()
        self.mainWindow.window_inpt_l.enableButtons()
        self.mainWindow.window_inpt_l.checkUndo(True)
        self.mainWindow.window_inpt_r.show()
        self.mainWindow.window_inpt_r.enableButtons()
        self.mainWindow.hist_show(img_current)
        self.mainWindow.crosshairCursor()

    def btn_undo_release(self):
        global imgUndoStack, img_current, maxUndoSize, imgUndoPtr, mask_current, mask_view, mask_check
        if imgUndoPtr > 0:
            self.mainWindow.isBusy()
            if imgUndoPtr >= len(imgUndoStack):
                imgUndoStack.append(img_current)
            else:
                imgUndoStack[imgUndoPtr] = img_current
            imgUndoPtr -= 1
            img_current = imgUndoStack[imgUndoPtr]
            self.mainWindow.qt_imshow(img_current)
            self.mainWindow.hist_show(img_current)
            if len(mask_current[mask_current > 0]) > 0:
                mask_view = preview_mask(img_current, mask_current, (240, 32, 16), 0.35)
            else:
                mask_view = img_current
            mask_check = None
            self.mainWindow.isBusy(False)
        self.mainWindow.undoButtonCheck()

    def btn_redo_release(self):
        global imgUndoStack, img_current, maxUndoSize, imgUndoPtr, mask_current, mask_view, mask_check
        if imgUndoPtr + 1 < len(imgUndoStack):
            self.mainWindow.isBusy()
            imgUndoPtr += 1
            img_current = imgUndoStack[imgUndoPtr]
            self.mainWindow.qt_imshow(img_current)
            self.mainWindow.hist_show(img_current)
            if len(mask_current[mask_current > 0]) > 0:
                mask_view = preview_mask(img_current, mask_current, (240, 32, 16), 0.35)
            else:
                mask_view = img_current
            mask_check = None
            self.mainWindow.isBusy(False)
        self.mainWindow.undoButtonCheck()


# --------------------------------------------------------------
class WindowMsg(QtWidgets.QWidget):
    def __init__(self, mainWindow):
        super(WindowMsg, self).__init__()
        self.mainWindow = mainWindow
        self.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle(lang["Notice"])
        setWindowIcons(self)

        self.btn_OK = genButton(self, lang["OK"], None, self.btn_OK_release, "Return")

        self.wtitle = QtWidgets.QLabel("", self)
        self.wtitle.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
        self.wtitle.setProperty("fontset", 2)

        self.label = QtWidgets.QLabel("", self)
        self.label.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
        self.label.setProperty("fontset", 1)
        self.label.setWordWrap(True)

        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.addWidget(self.wtitle)
        VBlayout.addWidget(self.label, 2)
        VBlayout.addWidget(self.btn_OK)

        self.setStyleSheet(stylepack)

    def btn_OK_release(self):
        self.close()

    def show(self, title="", msg=""):
        self.wtitle.setText(title)
        self.label.setText(msg)
        self.resize(250, 180)
        sg = self.frameGeometry()
        mg = self.mainWindow.frameGeometry().center()
        sg.moveCenter(mg)
        self.move(sg.topLeft())
        self.mainWindow.setEnabled(False)
        super().show()

    def closeEvent(self, event):
        self.mainWindow.setEnabled(True)
        event.accept()


class WindowAsksave(QtWidgets.QWidget):
    def __init__(self, mainWindow):
        super(WindowAsksave, self).__init__()
        self.mainWindow = mainWindow
        self.setWindowTitle(lang["Notice"])
        setWindowIcons(self)
        self.file_ = None

        self.btn_yes = genButton(self, lang["YES"], None, self.btn_yes_release, "Y", style=2)
        self.btn_no = genButton(self, lang["NO"], None, self.btn_no_release, "N")

        self.wtitle = QtWidgets.QLabel(lang["Opening a new image..."], self)
        self.wtitle.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
        self.wtitle.setProperty("fontset", 2)

        self.label = QtWidgets.QLabel(lang["Would you like to discard"], self)
        self.label.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
        self.label.setProperty("fontset", 1)
        self.label.setWordWrap(True)

        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.addWidget(self.wtitle)
        VBlayout.addWidget(self.label, 2)
        HBlayout = QtWidgets.QHBoxLayout()
        HBlayout.addWidget(self.btn_yes)
        HBlayout.addWidget(self.btn_no)
        VBlayout.addLayout(HBlayout)

        self.setStyleSheet(stylepack)

    def btn_yes_release(self):
        self.mainWindow.openImage(self.file_)
        self.close()

    def btn_no_release(self):
        self.close()

    def show(self, file_):
        self.mainWindow.setEnabled(False)
        self.file_ = file_
        self.resize(250, 180)
        sg = self.frameGeometry()
        mg = self.mainWindow.frameGeometry().center()
        sg.moveCenter(mg)
        self.move(sg.topLeft())
        super().show()

    def closeEvent(self, event):
        self.mainWindow.setEnabled(True)
        event.accept()


class WindowAskquit(QtWidgets.QWidget):
    def __init__(self, mainWindow):
        super(WindowAskquit, self).__init__()
        self.mainWindow = mainWindow
        self.setWindowTitle(lang["Notice"])
        setWindowIcons(self)
        self.file_ = None

        self.btn_yes = genButton(self, lang["YES"], None, self.btn_yes_release, "Y", style=2)
        self.btn_no = genButton(self, lang["NO"], None, self.btn_no_release, "N")

        self.wtitle = QtWidgets.QLabel(lang["Quitting..."], self)
        self.wtitle.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
        self.wtitle.setProperty("fontset", 2)

        self.label = QtWidgets.QLabel(lang["Would you like to discard"], self)
        self.label.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
        self.label.setProperty("fontset", 1)
        self.label.setWordWrap(True)

        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.addWidget(self.wtitle)
        VBlayout.addWidget(self.label, 2)
        HBlayout = QtWidgets.QHBoxLayout()
        HBlayout.addWidget(self.btn_yes)
        HBlayout.addWidget(self.btn_no)
        VBlayout.addLayout(HBlayout)

        self.setStyleSheet(stylepack)

    def btn_yes_release(self):
        self.close()
        self.mainWindow.closeAll = True
        self.mainWindow.close()

    def btn_no_release(self):
        self.close()

    def show(self):
        self.mainWindow.setEnabled(False)
        self.resize(250, 180)
        sg = self.frameGeometry()
        mg = self.mainWindow.frameGeometry().center()
        sg.moveCenter(mg)
        self.move(sg.topLeft())
        super().show()

    def closeEvent(self, event):
        self.mainWindow.setEnabled(True)
        event.accept()


class WindowAskresize(QtWidgets.QWidget):
    def __init__(self, mainWindow):
        super(WindowAskresize, self).__init__()
        self.mainWindow = mainWindow
        self.setWindowTitle(lang["Notice"])
        setWindowIcons(self)
        self.img = None

        self.btn_yes = genButton(self, lang["YES"], None, self.btn_yes_release, "Y", style=2)
        self.btn_no = genButton(self, lang["NO"], None, self.btn_no_release, "N")

        self.wtitle = QtWidgets.QLabel(lang["Be Patient"], self)
        self.wtitle.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
        self.wtitle.setProperty("fontset", 2)

        self.label = QtWidgets.QLabel(lang["Large Image Notice"], self)
        self.label.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
        self.label.setProperty("fontset", 1)
        self.label.setWordWrap(True)

        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.addWidget(self.wtitle)
        VBlayout.addWidget(self.label, 2)
        HBlayout = QtWidgets.QHBoxLayout()
        HBlayout.addWidget(self.btn_yes)
        HBlayout.addWidget(self.btn_no)
        VBlayout.addLayout(HBlayout)

        self.setStyleSheet(stylepack)

    def btn_yes_release(self):
        self.img = resize_max(self.img, 3264)
        self.mainWindow.initImage(self.img)
        self.close()

    def btn_no_release(self):
        self.close()

    def show(self, img):
        self.mainWindow.setEnabled(False)
        self.img = img
        self.resize(350, 200)
        sg = self.frameGeometry()
        mg = self.mainWindow.frameGeometry().center()
        sg.moveCenter(mg)
        self.move(sg.topLeft())
        super().show()

    def closeEvent(self, event):
        self.img = None
        self.mainWindow.setEnabled(True)
        event.accept()


class WindowSettings(QtWidgets.QWidget):
    def __init__(self, mainWindow=None):
        super(WindowSettings, self).__init__()
        setWindowIcons(self)
        self.mainWindow = mainWindow
        if self.mainWindow is not None:
            global lang
            self.lang = lang
        else:
            self.lang = lang_cn_s

        self.setWindowTitle(self.lang["Welcome!"])

        self.setStyleSheet(stylepack)

        self.label_lang = genLabel(self, "Language")
        self.label_undo = genLabel(self, self.lang["Max Undo Steps"])
        self.label_lang_hint = genLabel(self, self.lang["Take Effect After Restart"], 1)

        self.combo_lang = QtWidgets.QComboBox(self)
        self.combo_lang.addItems(["简体中文", "English"])
        self.combo_lang.currentIndexChanged.connect(self.updateLang)
        self.combo_lang.setView(QtWidgets.QListView())

        self.sl_maxUndo = genSlider(self, self.lang["Steps"], 3, 30, 1, 5, changeEvent=self.showUndoSize)

        self.btn_help = genButton(self, self.lang["Help"], None, self.btn_help_release, "H")
        self.btn_about = genButton(self, self.lang["About"], None, self.btn_about_release)
        self.btn_apply = genButton(self, self.lang["Apply"], None, self.btn_apply_release, "Return", style=2)

        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.setAlignment(QtCore.Qt.AlignTop)
        VBlayout.addWidget(self.label_lang)
        VBlayout.addWidget(self.combo_lang)
        VBlayout.addWidget(self.label_lang_hint)
        VBlayout.addWidget(self.label_undo)
        VBlayout.addLayout(self.sl_maxUndo)
        VBlayout.addWidget(self.btn_help)
        VBlayout.addWidget(self.btn_about)
        VBlayout.addWidget(self.btn_apply)

        self.label_lang_hint.close()

    def btn_help_release(self):
        self.mainWindow.window_help.show("main")

    def btn_about_release(self):
        self.mainWindow.window_help.show("about")

    def btn_apply_release(self):
        global config, maxUndoSize
        if self.lang == lang_cn_s:
            config["language"] = "cn_s"
        elif self.lang == lang_en:
            config["language"] = "en"
        config["maxUndoSize"] = self.sl_maxUndo.value()
        config["version"] = version
        saveConfig()
        maxUndoSize = self.sl_maxUndo.value()
        if self.mainWindow is not None:
            self.close()
            self.mainWindow.showMenuWindow()
        else:
            global lang
            lang = self.lang
            startMain()
            self.close()

    def updateLang(self):
        if self.combo_lang.currentIndex() == 0:
            self.lang = lang_cn_s
        elif self.combo_lang.currentIndex() == 1:
            self.lang = lang_en
        if self.mainWindow is not None:
            self.label_lang_hint.show()
        self.label_undo.setText(self.lang["Max Undo Steps"])
        self.btn_help.setText(self.lang["Help"])
        self.btn_about.setText(self.lang["About"])
        self.btn_apply.setText(self.lang["Apply"])
        self.label_lang_hint.setText(self.lang["Take Effect After Restart"])
        self.setWindowTitle(self.lang["Welcome!"])
        self.showUndoSize()

    def showUndoSize(self):
        self.sl_maxUndo.setText(self.lang["Steps"] + ": " + str(self.sl_maxUndo.value()))

    def show(self):
        global config
        self.sl_maxUndo.setValue(config["maxUndoSize"])
        self.showUndoSize()
        if config["language"] == "cn_s":
            self.combo_lang.setCurrentIndex(0)
        elif config["language"] == "en":
            self.combo_lang.setCurrentIndex(1)
        if self.mainWindow is None:
            self.resize(300, 100)
        else:
            sg = self.frameGeometry()
            mg = self.mainWindow.frameGeometry().center()
            sg.moveCenter(mg)
            self.move(sg.topLeft())
        if self.mainWindow is None:
            self.btn_about.close()
            self.btn_help.close()
        super().show()


class WindowHelp(QtWidgets.QTextBrowser):
    def __init__(self, mainWindow):
        super(WindowHelp, self).__init__()
        setWindowIcons(self)
        self.setWindowTitle(lang["Help"])
        self.mainWindow = mainWindow
        self.setStyleSheet(stylepack)
        self.zoomIn(4)
        self.setViewportMargins(15,15,15,15)
        self.setOpenExternalLinks(True)
        self.path = u"./GUI/Help/"
        self.cdict={
            "cn_s":{
                "main":"main_cn_s.html",
                "Grabcut":"grabcut_cn_s.html",
                "MagicWand":"magic_wand_cn_s.html",
                "ColorRange":"color_range_cn_s.html",
                "SelectTools":"select_tools_cn_s.html",
                "AdjustSelection":"adjust_selection_cn_s.html",
                "Beeswax":"beeswax_cn_s.html",
                "about":"about_cn_s.html",
            },
            "en":{
                "main":"main_en.html",
                "Grabcut":"grabcut_en.html",
                "MagicWand":"magic_wand_en.html",
                "ColorRange":"color_range_en.html",
                "SelectTools":"select_tools_en.html",
                "AdjustSelection":"adjust_selection_en.html",
                "Beeswax":"beeswax_en.html",
                "about": "about_en.html",
            }
        }

    def show(self, content=None):
        global config
        try:
            docfile = self.path+self.cdict[config["language"]][content]
            self.setSource(QtCore.QUrl(docfile))
            if self.toPlainText() =="":
                raise FileNotFoundError
        except:
            self.mainWindow.window_msg.show(lang["Read File Error"], lang["Help document not found"])
        else:
            self.close()
            self.resize(800, 600)
            sg = self.frameGeometry()
            mg = self.mainWindow.frameGeometry().center()
            sg.moveCenter(mg)
            self.move(sg.topLeft())
            super().show()


# --------------------------------------------------------------

class WindowSave_L(QtWidgets.QWidget):
    def __init__(self, mainWindow):
        super(WindowSave_L, self).__init__()
        self.mainWindow = mainWindow

        self.btn_jpg = genButton(self, lang["JPG File"], None, self.btn_jpg_release, None, style=2)

        self.btn_cmp1 = genButton(self, lang["Save Comparison (Vertical)"], None, self.btn_cmp1_release, None)
        self.btn_cmp2 = genButton(self, lang["Save Comparison (Horizontal)"], None, self.btn_cmp2_release, None)
        self.sl_jpgq = genSlider(self, lang["JPG Quality"], 0, 100, 1, 100, changeEvent=self.showQuality)

        self.btn_savemask = genButton(self, lang["Save Masked Image as PNG"], None, self.btn_savemask_release, None)

        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.setAlignment(QtCore.Qt.AlignTop)
        VBlayout.addWidget(genLabel(self, lang["Save as JPG"]))
        VBlayout.addLayout(self.sl_jpgq)
        VBlayout.addWidget(self.btn_jpg)
        VBlayout.addWidget(genLabel(self, lang["Save Comparison"]))
        VBlayout.addWidget(self.btn_cmp1)
        VBlayout.addWidget(self.btn_cmp2)
        VBlayout.addWidget(genLabel(self, lang["Save Masked Image"]))
        VBlayout.addWidget(self.btn_savemask)

        self.setStyleSheet(stylepack)

    def btn_jpg_release(self):
        global img_current
        self.mainWindow.writeImage(img_current, "jpg", self.sl_jpgq.value())
        self.close()

    def btn_cmp1_release(self):
        global img_current, img_input
        img_cmp = cv2.vconcat([blend_3c(img_input), blend_3c(img_current)])
        self.mainWindow.writeImage(img_cmp, "jpg", self.sl_jpgq.value(), suffix="_FITB_Compare")
        self.close()

    def btn_cmp2_release(self):
        global img_current, img_input
        img_cmp = cv2.hconcat([blend_3c(img_input), blend_3c(img_current)])
        self.mainWindow.writeImage(img_cmp, "jpg", self.sl_jpgq.value(), suffix="_FITB_Compare")
        self.close()

    def btn_savemask_release(self):
        global img_current, mask_current
        maskedImage = blend_4c(img_current, mask_current)
        self.mainWindow.writeImage(maskedImage, "png", suffix="_FITB_Masked")

    def closeEvent(self, event):
        self.mainWindow.showMenuWindow()
        event.ignore()

    def showQuality(self):
        self.sl_jpgq.setText(lang["JPG Quality"] + ": " + str(self.sl_jpgq.value()) + "%")

    def show(self):
        global mask_current
        if len(mask_current[mask_current > 0]) == 0 or len(mask_current[mask_current < 255]) == 0:
            self.btn_savemask.setEnabled(False)
        else:
            self.btn_savemask.setEnabled(True)
        self.showQuality()
        super().show()


class WindowSave_R(QtWidgets.QWidget):
    def __init__(self, mainWindow):
        super(WindowSave_R, self).__init__()
        self.mainWindow = mainWindow

        self.btn_png = genButton(self, lang["PNG File"], None, self.btn_png_release, None)
        self.btn_bmp = genButton(self, lang["BMP File"], None, self.btn_bmp_release, None)
        self.btn_cancel = genButton(self, lang["Cancel"], None, self.btn_cancel_release, "Escape", style=3)

        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.setAlignment(QtCore.Qt.AlignTop)
        VBlayout.addWidget(genLabel(self, lang["Other Formats"]))
        VBlayout.addWidget(self.btn_png)
        VBlayout.addWidget(self.btn_bmp)
        VBlayout.addWidget(self.btn_cancel)

        self.setStyleSheet(stylepack)

    def btn_png_release(self):
        global img_current,img_input
        if len(img_input.shape)==3 and img_input.shape[2] == 4:
            print("test")
            self.mainWindow.writeImage(blend_4c(img_current,img_input[:, :, 3]), "png")
        else:
            self.mainWindow.writeImage(img_current, "png")
        self.close()

    def btn_bmp_release(self):
        global img_current
        self.mainWindow.writeImage(img_current, "bmp")
        self.close()

    def btn_cancel_release(self):
        self.close()

    def closeEvent(self, event):
        self.mainWindow.showMenuWindow()
        event.ignore()


class WindowGbcut_L(QtWidgets.QWidget):
    def __init__(self, mainWindow):
        super(WindowGbcut_L, self).__init__()
        self.mainWindow = mainWindow

        self.btn_roi = genButton(self, lang["ROI Select"], None, self.btn_roi_release, None)
        self.btn_fgd = genButton(self, lang["Add(+)"], None, self.btn_fgd_release, "=", style=4)
        self.btn_bgd = genButton(self, lang["Subtract(-)"], None, self.btn_bgd_release, "-", style=3)

        self.sl_iter = genSlider(self, lang["Grab Cut Iteration"], 1, 5, 1, 2, self.sl_iter_release)
        self.sl_brush = genSlider(self, lang["Brush Size"], 1, 100, 1, 15, self.sl_brush_release)

        self.sl_grow = genSlider(self, lang["Grow"], 0, 50, 2, 1, self.updateEdge)
        self.sl_contract = genSlider(self, lang["Contract"], 0, 50, 2, 1, self.updateEdge)
        self.sl_feather = genSlider(self, lang["Feather"], 1, 51, 2, 1, self.updateEdge)

        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.setAlignment(QtCore.Qt.AlignTop)
        VBlayout.addWidget(genLabel(self, lang["1. Frame Select"]))
        VBlayout.addWidget(self.btn_roi)
        VBlayout.addLayout(self.sl_iter)

        VBlayout.addWidget(genLabel(self, lang["2. Mark Manually"]))
        HBlayout1 = QtWidgets.QHBoxLayout()
        HBlayout1.addWidget(self.btn_bgd)
        HBlayout1.addWidget(self.btn_fgd)
        VBlayout.addLayout(HBlayout1)
        VBlayout.addLayout(self.sl_brush)

        VBlayout.addWidget(genLabel(self, lang["3. Edit Selection Edge"]))
        VBlayout.addLayout(self.sl_grow)
        VBlayout.addLayout(self.sl_contract)
        VBlayout.addLayout(self.sl_feather)

        self.setStyleSheet(stylepack)

    def btn_roi_release(self):
        global taskState, lineThick
        taskState = 1
        lineThick = 3
        self.mainWindow.viewer.startDrawing(mode=1)
        self.enableButtons()

    def btn_fgd_release(self):
        global taskState, lineColor, lineThick
        taskState = 2
        lineColor, lineThick = (0, 255, 255, 255), self.sl_brush.value()
        self.mainWindow.viewer.startDrawing(mode=2)
        self.enableButtons()

    def btn_bgd_release(self):
        global taskState, lineColor, lineThick
        taskState = 3
        lineColor, lineThick = (255, 0, 0, 255), self.sl_brush.value()
        self.mainWindow.viewer.startDrawing(mode=3)
        self.enableButtons()

    def sl_iter_release(self):
        global gbcpack
        gbcpack.setIter(self.sl_iter.value())

    def sl_brush_release(self):
        global lineThick
        lineThick = self.sl_brush.value()

    def updateEdge(self):
        global gbcpack, img_view, mask_view
        gbcpack.edgeModify(self.sl_grow.value(),
                           self.sl_contract.value(),
                           self.sl_feather.value())
        if not gbcpack.firstRun:
            img_view = preview_mask(mask_view, gbcpack.getMask())
            self.mainWindow.qt_imshow(img_view)

    def disableButtons(self):
        self.btn_roi.setEnabled(False)
        self.btn_fgd.setEnabled(False)
        self.btn_bgd.setEnabled(False)

    def enableButtons(self):
        global taskState
        if taskState == 0:
            self.btn_roi.setEnabled(True)
            self.btn_fgd.setEnabled(True)
            self.btn_bgd.setEnabled(True)
        if taskState == 1:
            self.btn_roi.setEnabled(False)
            self.btn_fgd.setEnabled(True)
            self.btn_bgd.setEnabled(True)
        elif taskState == 2:
            self.btn_roi.setEnabled(True)
            self.btn_fgd.setEnabled(False)
            self.btn_bgd.setEnabled(True)
        elif taskState == 3:
            self.btn_roi.setEnabled(True)
            self.btn_fgd.setEnabled(True)
            self.btn_bgd.setEnabled(False)


class WindowGbcut_R(QtWidgets.QWidget):
    def __init__(self, mainWindow):
        super(WindowGbcut_R, self).__init__()
        self.mainWindow = mainWindow

        self.btn_apply0 = genButton(self, lang["Replace All"], None, self.btn_apply0_release, "Return", style=2)
        self.btn_apply1 = genButton(self, lang["Add to(+)"], None, self.btn_apply1_release, "Shift+Return", style=4)
        self.btn_apply2 = genButton(self, lang["Subtract from(-)"], None, self.btn_apply2_release, "Alt+Return",
                                    style=3)
        self.btn_cancel = genButton(self, lang["Cancel"], None, self.btn_cancel_release, "Escape")
        self.btn_help = genButton(self, lang["Help"], None, self.btn_help_release, "H")

        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.setAlignment(QtCore.Qt.AlignTop)
        VBlayout.addWidget(self.btn_help)
        VBlayout.addWidget(genLabel(self, lang["Apply to Main Mask"]))
        VBlayout.addWidget(self.btn_apply0)
        VBlayout.addWidget(self.btn_apply1)
        VBlayout.addWidget(self.btn_apply2)
        VBlayout.addWidget(self.btn_cancel)

        self.setStyleSheet(stylepack)

    def btn_apply0_release(self):
        global gbcpack
        self.mainWindow.updateMask(gbcpack.getMask())
        self.close()

    def btn_apply1_release(self):
        global gbcpack, mask_current
        new_mask = cv2.add(mask_current, gbcpack.getMask())
        self.mainWindow.updateMask(new_mask)
        self.close()

    def btn_apply2_release(self):
        global gbcpack, mask_current
        new_mask = cv2.subtract(mask_current, gbcpack.getMask())
        self.mainWindow.updateMask(new_mask)
        self.close()

    def btn_cancel_release(self):
        self.close()

    def closeEvent(self, event):
        global mask_view, taskState, gbcpack
        taskState = 0
        self.mainWindow.viewer.stopDrawing()
        self.mainWindow.qt_imshow(mask_view)
        self.mainWindow.showMenuWindow()
        gbcpack = None
        event.ignore()

    def disableButtons(self):
        self.btn_apply0.setEnabled(False)
        self.btn_apply1.setEnabled(False)
        self.btn_apply2.setEnabled(False)

    def enableButtons(self):
        self.btn_apply0.setEnabled(True)
        self.btn_apply1.setEnabled(True)
        self.btn_apply2.setEnabled(True)

    def btn_help_release(self):
        self.mainWindow.window_help.show("Grabcut")


class WindowMwd_L(QtWidgets.QWidget):
    def __init__(self, mainWindow):
        super(WindowMwd_L, self).__init__()
        self.mainWindow = mainWindow

        self.sl_ldiff = genSlider(self, lang["Upper Difference"], 0, 150, 1, 40)
        self.sl_udiff = genSlider(self, lang["Lower Difference"], 0, 150, 1, 40)

        self.sl_grow = genSlider(self, lang["Grow"], 0, 50, 2, 1, self.updateEdge)
        self.sl_contract = genSlider(self, lang["Contract"], 0, 50, 2, 1, self.updateEdge)
        self.sl_feather = genSlider(self, lang["Feather"], 1, 51, 2, 1, self.updateEdge)

        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.setAlignment(QtCore.Qt.AlignTop)
        VBlayout.addWidget(genLabel(self, lang["Magic Wand Select"]))
        VBlayout.addLayout(self.sl_ldiff)
        VBlayout.addLayout(self.sl_udiff)
        VBlayout.addWidget(genLabel(self, lang["Edit Selection Edge"]))
        VBlayout.addLayout(self.sl_grow)
        VBlayout.addLayout(self.sl_contract)
        VBlayout.addLayout(self.sl_feather)

        self.setStyleSheet(stylepack)

    def updateEdge(self):
        global mwdpack, img_view, mask_view
        mwdpack.edgeModify(self.sl_grow.value(),
                           self.sl_contract.value(),
                           self.sl_feather.value())
        if not mwdpack.firstRun:
            img_view = preview_mask(mask_view, mwdpack.getMask())
            self.mainWindow.qt_imshow(img_view)

    def enableButtons(self):
        pass


class WindowMwd_R(QtWidgets.QWidget):
    def __init__(self, mainWindow):
        super(WindowMwd_R, self).__init__()
        self.mainWindow = mainWindow

        self.btn_apply0 = genButton(self, lang["Replace All"], None, self.btn_apply0_release, "Return", style=2)
        self.btn_apply1 = genButton(self, lang["Add to(+)"], None, self.btn_apply1_release, "Shift+Return", style=4)
        self.btn_apply2 = genButton(self, lang["Subtract from(-)"], None, self.btn_apply2_release, "Alt+Return",
                                    style=3)
        self.btn_cancel = genButton(self, lang["Cancel"], None, self.btn_cancel_release, "Escape")
        self.btn_help = genButton(self, lang["Help"], None, self.btn_help_release, "H")

        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.setAlignment(QtCore.Qt.AlignTop)
        VBlayout.addWidget(self.btn_help)
        VBlayout.addWidget(genLabel(self, lang["Apply to Main Mask"]))
        VBlayout.addWidget(self.btn_apply0)
        VBlayout.addWidget(self.btn_apply1)
        VBlayout.addWidget(self.btn_apply2)
        VBlayout.addWidget(self.btn_cancel)

        self.setStyleSheet(stylepack)

    def btn_apply0_release(self):
        global mwdpack
        self.mainWindow.updateMask(mwdpack.getMask())
        self.close()

    def btn_apply1_release(self):
        global mwdpack, mask_current
        new_mask = cv2.add(mask_current, mwdpack.getMask())
        self.mainWindow.updateMask(new_mask)
        self.close()

    def btn_apply2_release(self):
        global mwdpack, mask_current
        new_mask = cv2.subtract(mask_current, mwdpack.getMask())
        self.mainWindow.updateMask(new_mask)
        self.close()

    def btn_cancel_release(self):
        self.close()

    def closeEvent(self, event):
        global mask_view, taskState, mwdpack
        self.mainWindow.viewer.stopDrawing()
        self.mainWindow.qt_imshow(mask_view)
        self.mainWindow.showMenuWindow()
        mwdpack = None
        taskState = 0
        event.ignore()

    def enableButtons(self):
        global taskState
        if taskState == 4:
            self.btn_apply0.setEnabled(False)
            self.btn_apply1.setEnabled(False)
            self.btn_apply2.setEnabled(False)
        elif taskState in [5, 6]:
            self.btn_apply0.setEnabled(True)
            self.btn_apply1.setEnabled(True)
            self.btn_apply2.setEnabled(True)

    def btn_help_release(self):
        self.mainWindow.window_help.show("MagicWand")


class WindowSkinSelect_L(QtWidgets.QWidget):
    def __init__(self, mainWindow):
        super(WindowSkinSelect_L, self).__init__()
        self.mainWindow = mainWindow

        self.xpt, self.ypt = 0, 0

        self.sl_hdiff = genSlider(self, lang["H Tolerance"], 0, 255, 1, 127, self.setTolerance)
        self.sl_sdiff = genSlider(self, lang["S Tolerance"], 0, 255, 1, 20, self.setTolerance)
        self.sl_vdiff = genSlider(self, lang["V Tolerance"], 0, 255, 1, 20, self.setTolerance)
        self.sl_soft = genSlider(self, lang["Soft Select"], 0, 127, 1, 10, self.setTolerance)

        self.sl_grow = genSlider(self, lang["Grow"], 0, 50, 2, 1, self.updateMask)
        self.sl_contract = genSlider(self, lang["Contract"], 0, 50, 2, 1, self.updateMask)
        self.sl_feather = genSlider(self, lang["Feather"], 1, 51, 2, 1, self.updateMask)

        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.setAlignment(QtCore.Qt.AlignTop)
        VBlayout.addWidget(genLabel(self, lang["Manual Select"]))
        VBlayout.addLayout(self.sl_hdiff)
        VBlayout.addLayout(self.sl_sdiff)
        VBlayout.addLayout(self.sl_vdiff)
        VBlayout.addLayout(self.sl_soft)
        VBlayout.addWidget(genLabel(self, lang["Edit Selection Edge"]))
        VBlayout.addLayout(self.sl_grow)
        VBlayout.addLayout(self.sl_contract)
        VBlayout.addLayout(self.sl_feather)

        self.setStyleSheet(stylepack)

    def updateMask(self):
        global sksepack, img_view, mask_view
        sksepack.updateEdge(self.sl_grow.value(),
                            self.sl_contract.value(),
                            self.sl_feather.value())
        img_view = preview_mask(mask_view, sksepack.getMask())
        self.mainWindow.qt_imshow(img_view)

    def setTolerance(self):
        global sksepack, img_view, mask_view
        if sksepack.firstRun == False and sksepack.mode == 0:
            sksepack.colorRange(self.xpt, self.ypt,
                                hdiff=self.sl_hdiff.value(),
                                sdiff=self.sl_sdiff.value(),
                                vdiff=self.sl_vdiff.value(),
                                soft=self.sl_soft.value())
            sksepack.updateEdge()
            img_view = preview_mask(mask_view, sksepack.getMask())
            self.mainWindow.qt_imshow(img_view)

    def setPoint(self, x=0, y=0):
        global sksepack, img_view, mask_view
        self.xpt, self.ypt = x, y
        sksepack.colorRange(self.xpt, self.ypt,
                            hdiff=self.sl_hdiff.value(),
                            sdiff=self.sl_sdiff.value(),
                            vdiff=self.sl_vdiff.value(),
                            soft=self.sl_soft.value())
        sksepack.updateEdge()
        self.mainWindow.window_skinselect_r.enableButtons()
        img_view = preview_mask(mask_view, sksepack.getMask())
        self.mainWindow.qt_imshow(img_view)


class WindowSkinSelect_R(QtWidgets.QWidget):
    def __init__(self, mainWindow):
        super(WindowSkinSelect_R, self).__init__()
        self.mainWindow = mainWindow

        self.btn_otsu = genButton(self, lang["Otsu-Cr"], None, self.btn_otsu_release, None)
        self.btn_hsv1 = genButton(self, lang["HSV Auto"], None, self.btn_hsv1_release, None)
        self.btn_ycrcb1 = genButton(self, lang["YCrCb Auto"], None, self.btn_ycrcb1_release, None)
        self.btn_apply0 = genButton(self, lang["Replace All"], None, self.btn_apply0_release, "Return", style=2)
        self.btn_apply1 = genButton(self, lang["Add to(+)"], None, self.btn_apply1_release, "Shift+Return", style=4)
        self.btn_apply2 = genButton(self, lang["Subtract from(-)"], None, self.btn_apply2_release, "Alt+Return",
                                    style=3)
        self.btn_cancel = genButton(self, lang["Cancel"], None, self.btn_cancel_release, "Escape")
        self.btn_help = genButton(self, lang["Help"], None, self.btn_help_release, "H")

        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.setAlignment(QtCore.Qt.AlignTop)
        VBlayout.addWidget(self.btn_help)
        VBlayout.addWidget(genLabel(self, lang["Auto Select"]))
        VBlayout.addWidget(self.btn_otsu)
        VBlayout.addWidget(self.btn_hsv1)
        VBlayout.addWidget(self.btn_ycrcb1)

        VBlayout.addWidget(genLabel(self, lang["Apply to Main Mask"]))
        VBlayout.addWidget(self.btn_apply0)
        VBlayout.addWidget(self.btn_apply1)
        VBlayout.addWidget(self.btn_apply2)
        VBlayout.addWidget(self.btn_cancel)

        self.setStyleSheet(stylepack)

    def btn_hsv1_release(self):
        global sksepack, mask_view, img_view
        sksepack.HSVSelect()
        sksepack.updateEdge()
        self.mainWindow.window_skinselect_r.enableButtons()
        img_view = preview_mask(mask_view, sksepack.getMask())
        self.mainWindow.qt_imshow(img_view)

    def btn_ycrcb1_release(self):
        global sksepack, mask_view, img_view
        sksepack.YCrCbSelect()
        sksepack.updateEdge()
        self.mainWindow.window_skinselect_r.enableButtons()
        img_view = preview_mask(mask_view, sksepack.getMask())
        self.mainWindow.qt_imshow(img_view)

    def btn_otsu_release(self):
        global sksepack, mask_view, img_view
        sksepack.otsuSelect()
        sksepack.updateEdge()
        self.mainWindow.window_skinselect_r.enableButtons()
        img_view = preview_mask(mask_view, sksepack.getMask())
        self.mainWindow.qt_imshow(img_view)

    def btn_apply0_release(self):
        global sksepack
        self.mainWindow.updateMask(sksepack.getMask())
        self.close()

    def btn_apply1_release(self):
        global sksepack, mask_current
        new_mask = cv2.add(mask_current, sksepack.getMask())
        self.mainWindow.updateMask(new_mask)
        self.close()

    def btn_apply2_release(self):
        global sksepack, mask_current
        new_mask = cv2.subtract(mask_current, sksepack.getMask())
        self.mainWindow.updateMask(new_mask)
        self.close()

    def btn_cancel_release(self):
        self.close()

    def closeEvent(self, event):
        global mask_view, taskState, sksepack
        self.mainWindow.viewer.stopDrawing()
        self.mainWindow.qt_imshow(mask_view)
        self.mainWindow.showMenuWindow()
        sksepack = None
        taskState = 0
        event.ignore()

    def enableButtons(self):
        global sksepack
        if sksepack.firstRun:
            self.btn_apply0.setEnabled(False)
            self.btn_apply1.setEnabled(False)
            self.btn_apply2.setEnabled(False)
        else:
            self.btn_apply0.setEnabled(True)
            self.btn_apply1.setEnabled(True)
            self.btn_apply2.setEnabled(True)

    def btn_help_release(self):
        self.mainWindow.window_help.show("ColorRange")


class WindowCSelect_L(QtWidgets.QWidget):
    def __init__(self, mainWindow):
        super(WindowCSelect_L, self).__init__()
        self.mainWindow = mainWindow

        self.btn_fgd = genButton(self, lang["Add(+)"], None, self.btn_fgd_release, "=", style=4)
        self.btn_bgd = genButton(self, lang["Subtract(-)"], None, self.btn_bgd_release, "-", style=3)
        self.btn_brush = genButton(self, lang["Brush"], None, self.btn_brush_release, "B")
        self.sl_brsize = genSlider(self, lang["Brush Size"], 1, 200, 1, 3, self.sl_brsize_release)

        self.btn_rect = genButton(self, lang["Rectangle"], None, self.btn_rect_release, "S")
        self.btn_ellipse = genButton(self, lang["Ellipse"], None, self.btn_ellipse_release, "E")
        self.btn_marq = genButton(self, lang["Lasso"], None, self.btn_marq_release, "L")
        self.btn_undo = genButton(self, lang["Undo"], None, self.btn_undo_release, "Ctrl+Z", style=3)
        self.btn_redo = genButton(self, lang["Redo"], None, self.btn_redo_release, "Ctrl+Y", style=4)

        self.sl_grow = genSlider(self, lang["Grow"], 0, 200, 2, 0, self.updateEdge)
        self.sl_contract = genSlider(self, lang["Contract"], 0, 200, 2, 0, self.updateEdge)
        self.sl_feather = genSlider(self, lang["Feather"], 1, 201, 2, 1, self.updateEdge)

        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.setAlignment(QtCore.Qt.AlignTop)
        VBlayout.addWidget(genLabel(self, lang["Edit Current Selection"]))
        HBlayout1 = QtWidgets.QHBoxLayout()
        HBlayout1.addWidget(self.btn_bgd)
        HBlayout1.addWidget(self.btn_fgd)
        VBlayout.addLayout(HBlayout1)
        VBlayout.addWidget(self.btn_marq)
        VBlayout.addWidget(self.btn_rect)
        VBlayout.addWidget(self.btn_ellipse)
        VBlayout.addWidget(self.btn_brush)
        VBlayout.addLayout(self.sl_brsize)
        HBlayout2 = QtWidgets.QHBoxLayout()
        HBlayout2.addWidget(self.btn_undo)
        HBlayout2.addWidget(self.btn_redo)
        VBlayout.addLayout(HBlayout2)

        VBlayout.addWidget(genLabel(self, lang["Edit Selection Edge"]))
        VBlayout.addLayout(self.sl_grow)
        VBlayout.addLayout(self.sl_contract)
        VBlayout.addLayout(self.sl_feather)

        self.setStyleSheet(stylepack)

    def btn_fgd_release(self):
        global csepack
        csepack.INV = False
        self.enableButtons()

    def btn_bgd_release(self):
        global csepack
        csepack.INV = True
        self.enableButtons()

    def btn_brush_release(self):
        global csepack
        csepack.setMode(1)
        csepack.lineThick = self.sl_brsize.value()
        self.enableButtons()

    def btn_rect_release(self):
        global csepack
        csepack.setMode(2)
        csepack.lineThick = 3
        self.enableButtons()

    def btn_ellipse_release(self):
        global csepack
        csepack.setMode(3)
        csepack.lineThick = 3
        self.enableButtons()

    def btn_marq_release(self):
        global csepack
        csepack.setMode(4)
        csepack.lineThick = 3
        self.enableButtons()

    def sl_brsize_release(self):
        global csepack
        if csepack.mode == 1:
            csepack.lineThick = self.sl_brsize.value()

    def updateEdge(self):
        global csepack, img_view, mask_view
        csepack.edgeModify(self.sl_grow.value(),
                           self.sl_contract.value(),
                           self.sl_feather.value())
        self.mainWindow.qt_imshow(csepack.getView())

    def enableButtons(self):
        global csepack
        if csepack.mode == 1:
            self.btn_brush.setEnabled(False)
            self.btn_rect.setEnabled(True)
            self.btn_ellipse.setEnabled(True)
            self.btn_marq.setEnabled(True)
        elif csepack.mode == 2:
            self.btn_brush.setEnabled(True)
            self.btn_rect.setEnabled(False)
            self.btn_ellipse.setEnabled(True)
            self.btn_marq.setEnabled(True)
        elif csepack.mode == 3:
            self.btn_brush.setEnabled(True)
            self.btn_rect.setEnabled(True)
            self.btn_ellipse.setEnabled(False)
            self.btn_marq.setEnabled(True)
        elif csepack.mode == 4:
            self.btn_brush.setEnabled(True)
            self.btn_rect.setEnabled(True)
            self.btn_ellipse.setEnabled(True)
            self.btn_marq.setEnabled(False)

        if not csepack.INV:
            self.btn_fgd.setEnabled(False)
            self.btn_bgd.setEnabled(True)
        else:
            self.btn_fgd.setEnabled(True)
            self.btn_bgd.setEnabled(False)

    def btn_undo_release(self):
        global csepack
        self.mainWindow.isBusy()
        csepack.undo()
        self.mainWindow.qt_imshow(csepack.getView())
        self.checkUndo()
        self.mainWindow.isBusy(False)

    def btn_redo_release(self):
        global csepack
        self.mainWindow.isBusy()
        csepack.redo()
        self.mainWindow.qt_imshow(csepack.getView())
        self.checkUndo()
        self.mainWindow.isBusy(False)

    def checkUndo(self, flag=False):
        global csepack
        if not flag:
            self.btn_redo.setEnabled(csepack.redoCheck())
            self.btn_undo.setEnabled(csepack.undoCheck())
        else:
            self.btn_redo.setEnabled(False)
            self.btn_undo.setEnabled(False)


class WindowCSelect_R(QtWidgets.QWidget):
    def __init__(self, mainWindow):
        super(WindowCSelect_R, self).__init__()
        self.mainWindow = mainWindow

        self.btn_apply0 = genButton(self, lang["Replace All"], None, self.btn_apply0_release, "Return", style=2)
        self.btn_apply1 = genButton(self, lang["Add to(+)"], None, self.btn_apply1_release, "Shift+Return", style=4)
        self.btn_apply2 = genButton(self, lang["Subtract from(-)"], None, self.btn_apply2_release, "Alt+Return",
                                    style=3)
        self.btn_cancel = genButton(self, lang["Cancel"], None, self.btn_cancel_release, "Escape")
        self.btn_help = genButton(self, lang["Help"], None, self.btn_help_release, "H")

        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.setAlignment(QtCore.Qt.AlignTop)
        VBlayout.addWidget(self.btn_help)
        VBlayout.addWidget(genLabel(self, lang["Apply to Main Mask"]))
        VBlayout.addWidget(self.btn_apply0)
        VBlayout.addWidget(self.btn_apply1)
        VBlayout.addWidget(self.btn_apply2)
        VBlayout.addWidget(self.btn_cancel)

        self.setStyleSheet(stylepack)

    def btn_apply0_release(self):
        global csepack
        self.mainWindow.updateMask(csepack.getMask())
        self.close()

    def btn_apply1_release(self):
        global csepack, mask_current
        new_mask = cv2.add(mask_current, csepack.getMask())
        self.mainWindow.updateMask(new_mask)
        self.close()

    def btn_apply2_release(self):
        global csepack, mask_current
        new_mask = cv2.subtract(mask_current, csepack.getMask())
        self.mainWindow.updateMask(new_mask)
        self.close()

    def btn_cancel_release(self):
        self.close()

    def updateEdge(self):
        global csepack, img_view, mask_view
        csepack.edgeModify(self.sl_grow.value(),
                           self.sl_contract.value(),
                           self.sl_feather.value())
        self.mainWindow.qt_imshow(csepack.getView())

    def closeEvent(self, event):
        global mask_view, taskState, csepack
        self.mainWindow.viewer.stopDrawing()
        self.mainWindow.qt_imshow(mask_view)
        self.mainWindow.showMenuWindow()
        csepack = None
        taskState = 0
        event.ignore()

    def enableButtons(self):
        global csepack
        if csepack.firstRun:
            self.btn_apply0.setEnabled(False)
            self.btn_apply1.setEnabled(False)
            self.btn_apply2.setEnabled(False)
        else:
            self.btn_apply0.setEnabled(True)
            self.btn_apply1.setEnabled(True)
            self.btn_apply2.setEnabled(True)

    def btn_help_release(self):
        self.mainWindow.window_help.show("SelectTools")



class WindowAdjMask_L(QtWidgets.QWidget):
    def __init__(self, mainWindow):
        super(WindowAdjMask_L, self).__init__()
        self.mainWindow = mainWindow

        self.sl_grow = genSlider(self, lang["Grow"], 0, 50, 2, 0, self.updateEdge)
        self.sl_contract = genSlider(self, lang["Contract"], 0, 50, 2, 0, self.updateEdge)
        self.sl_feather = genSlider(self, lang["Feather"], 1, 201, 2, 1, self.updateEdge)
        self.sl_opacity = genSlider(self, lang["Opacity"], 0, 100, 1, 100, self.updateEdge)

        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.setAlignment(QtCore.Qt.AlignTop)
        VBlayout.addWidget(genLabel(self, lang["Edit Main Selection"]))
        VBlayout.addLayout(self.sl_grow)
        VBlayout.addLayout(self.sl_contract)
        VBlayout.addLayout(self.sl_feather)
        VBlayout.addLayout(self.sl_opacity)

        self.setStyleSheet(stylepack)

    def updateEdge(self):
        global madjpack
        madjpack.edgeModify(self.sl_grow.value(),
                            self.sl_contract.value(),
                            self.sl_feather.value(),
                            self.sl_opacity.value())
        self.mainWindow.qt_imshow(madjpack.getView())

    def resetSliders(self):
        self.sl_grow.setValue(0)
        self.sl_contract.setValue(0)
        self.sl_feather.setValue(1)
        self.sl_opacity.setValue(100)


class WindowAdjMask_R(QtWidgets.QWidget):
    def __init__(self, mainWindow):
        super(WindowAdjMask_R, self).__init__()
        self.mainWindow = mainWindow

        self.btn_apply = genButton(self, lang["Apply"], None, self.btn_apply_release, "Return", style=2)
        self.btn_cancel = genButton(self, lang["Cancel"], None, self.btn_cancel_release, "Escape")
        self.btn_help = genButton(self, lang["Help"], None, self.btn_help_release, "H")

        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.setAlignment(QtCore.Qt.AlignTop)
        VBlayout.addWidget(self.btn_help)
        VBlayout.addWidget(genLabel(self, lang["Apply to Main Mask"]))
        VBlayout.addWidget(self.btn_apply)
        VBlayout.addWidget(self.btn_cancel)

        self.setStyleSheet(stylepack)

    def btn_apply_release(self):
        global madjpack, mask_current
        self.mainWindow.updateMask(madjpack.getMask())
        self.close()

    def btn_cancel_release(self):
        self.close()

    def closeEvent(self, event):
        global mask_view, taskState, madjpack
        self.mainWindow.qt_imshow(mask_view)
        self.mainWindow.showMenuWindow()
        event.ignore()
        madjpack = None
        taskState = 0

    def btn_help_release(self):
        self.mainWindow.window_help.show("AdjustSelection")


# --------------------------------------------------------------
class WindowAdjImage_L(QtWidgets.QWidget):
    def __init__(self, mainWindow):
        super(WindowAdjImage_L, self).__init__()
        self.mainWindow = mainWindow

        self.sl_bright = genSlider(self, lang["Brightness"], -100, 100, 1, 0, self.updateImage)
        self.sl_contra = genSlider(self, lang["Contrast"], -100, 100, 1, 0, self.updateImage)
        self.sl_satur = genSlider(self, lang["Saturation"], -100, 100, 1, 0, self.updateImage, sl_type=5)
        self.sl_highlight = genSlider(self, lang["Highlight"], -100, 100, 1, 0, self.updateImage)
        self.sl_shadow = genSlider(self, lang["Shadow"], -100, 100, 1, 0, self.updateImage)
        self.sl_warm = genSlider(self, lang["Warm Color"], -100, 100, 1, 0, self.updateImage, sl_type=3)
        self.sl_magenta = genSlider(self, lang["Magenta Tone"], -100, 100, 1, 0, self.updateImage, sl_type=4)

        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.setAlignment(QtCore.Qt.AlignTop)
        VBlayout.addWidget(genLabel(self, lang["Basic Adjust"]))
        VBlayout.addLayout(self.sl_bright)
        VBlayout.addLayout(self.sl_contra)
        VBlayout.addLayout(self.sl_highlight)
        VBlayout.addLayout(self.sl_shadow)
        VBlayout.addWidget(genLabel(self, lang["Color Adjust"]))
        VBlayout.addLayout(self.sl_warm)
        VBlayout.addLayout(self.sl_magenta)
        VBlayout.addLayout(self.sl_satur)

        self.setStyleSheet(stylepack)

    def updateImage(self):
        global iadjpack
        self.mainWindow.isBusy()
        iadjpack.basicAdj(self.sl_bright.value(),
                          self.sl_contra.value(),
                          self.sl_satur.value(),
                          self.sl_warm.value(),
                          self.sl_magenta.value(),
                          self.sl_highlight.value(),
                          self.sl_shadow.value())
        self.mainWindow.qt_imshow(iadjpack.getImage())
        self.mainWindow.hist_show(iadjpack.getImage())
        self.mainWindow.isBusy(False)


class WindowAdjImage_R(QtWidgets.QWidget):
    def __init__(self, mainWindow):
        super(WindowAdjImage_R, self).__init__()
        self.mainWindow = mainWindow

        self.hist_view = genHist(self)

        self.btn_apply = genButton(self, lang["Apply"], None, self.btn_apply_release, "Return", style=2)
        self.btn_reset = genButton(self, lang["Reset"], None, self.btn_reset_release, "R", style=5)
        self.btn_cancel = genButton(self, lang["Cancel"], None, self.btn_cancel_release, "Escape")

        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.setAlignment(QtCore.Qt.AlignTop)
        VBlayout.addWidget(self.hist_view)
        VBlayout.addWidget(genLabel(self, lang["Apply to Image"]))
        VBlayout.addWidget(self.btn_apply)
        VBlayout.addWidget(self.btn_reset)
        VBlayout.addWidget(self.btn_cancel)

        self.setStyleSheet(stylepack)

    def btn_apply_release(self):
        global iadjpack, mask_current
        self.mainWindow.updateImg(iadjpack.getImage())
        self.close()

    def btn_cancel_release(self):
        self.close()

    def btn_reset_release(self):
        self.mainWindow.window_adji_l.sl_bright.setValue(0)
        self.mainWindow.window_adji_l.sl_contra.setValue(0)
        self.mainWindow.window_adji_l.sl_satur.setValue(0)
        self.mainWindow.window_adji_l.sl_warm.setValue(0)
        self.mainWindow.window_adji_l.sl_magenta.setValue(0)
        self.mainWindow.window_adji_l.sl_highlight.setValue(0)
        self.mainWindow.window_adji_l.sl_shadow.setValue(0)
        self.mainWindow.window_adji_l.updateImage()

    def closeEvent(self, event):
        global mask_view, taskState, img_current, iadjpack
        self.mainWindow.showMenuWindow()
        self.mainWindow.qt_imshow(img_current)
        self.mainWindow.hist_show(img_current)
        iadjpack = None
        event.ignore()
        taskState = 0


class WindowDehair_L(QtWidgets.QWidget):
    def __init__(self, mainWindow):
        super(WindowDehair_L, self).__init__()
        self.mainWindow = mainWindow

        self.sl_mediank = genSlider(self, lang["Median K-Size"], 3, 9, 2, 9, self.sl_mediank_release)
        self.sl_th_min = genSlider(self, lang["Dark Lower"], 0, 255, 1, 5, self.diffmap_update, sl_type=2)
        self.sl_th_max = genSlider(self, lang["Dark Upper"], 0, 255, 1, 255, self.diffmap_update, sl_type=1)
        self.sl_thi_min = genSlider(self, lang["Bright Lower"], 0, 255, 1, 5, self.diffmap_update, sl_type=2)
        self.sl_thi_max = genSlider(self, lang["Bright Upper"], 0, 255, 1, 255, self.diffmap_update, sl_type=1)
        self.sl_soft = genSlider(self, lang["Soft Transition"], 0, 127, 1, 0, self.diffmap_update, sl_type=1)

        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.setAlignment(QtCore.Qt.AlignTop)
        VBlayout.addWidget(genLabel(self, lang["Main Parameter"]))
        VBlayout.addLayout(self.sl_mediank)
        VBlayout.addWidget(genLabel(self, lang["Thresholds"]))
        VBlayout.addLayout(self.sl_th_min)
        VBlayout.addLayout(self.sl_th_max)
        VBlayout.addLayout(self.sl_thi_min)
        VBlayout.addLayout(self.sl_thi_max)
        VBlayout.addLayout(self.sl_soft)

        self.setStyleSheet(stylepack)

    def sl_mediank_release(self):
        global fdpack
        self.mainWindow.isBusy()
        fdpack.median(self.sl_mediank.value())
        self.mainWindow.qt_imshow(fdpack.result())
        self.mainWindow.hist_show(fdpack.result())
        self.mainWindow.isBusy(False)

    def diffmap_update(self):
        global fdpack
        self.mainWindow.isBusy()
        if self.sl_th_min.value() > self.sl_th_max.value():
            self.sl_th_max.setValue(self.sl_th_min.value())
        if self.sl_thi_min.value() > self.sl_thi_max.value():
            self.sl_thi_max.setValue(self.sl_thi_min.value())
        fdpack.diffmap(self.sl_th_min.value(), self.sl_th_max.value(),
                       self.sl_thi_min.value(), self.sl_thi_max.value(), self.sl_soft.value())
        self.mainWindow.qt_imshow(fdpack.result())
        self.mainWindow.hist_show(fdpack.result())
        self.mainWindow.isBusy(False)


class WindowDehair_R(QtWidgets.QWidget):
    def __init__(self, mainWindow):
        super(WindowDehair_R, self).__init__()
        self.mainWindow = mainWindow

        self.hist_view = genHist(self)
        self.btn_apply = genButton(self, lang["Apply"], None, self.btn_apply_release, "Return", style=2)
        self.btn_reset = genButton(self, lang["Reset"], None, self.btn_reset_release, "R", style=5)
        self.btn_cancel = genButton(self, lang["Cancel"], None, self.btn_cancel_release, "Escape")
        self.btn_help = genButton(self, lang["Help"], None, self.btn_help_release, "H")

        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.setAlignment(QtCore.Qt.AlignTop)
        VBlayout.addWidget(self.hist_view)
        VBlayout.addWidget(self.btn_help)
        VBlayout.addWidget(genLabel(self, lang["Apply to Image"]))
        VBlayout.addWidget(self.btn_apply)
        VBlayout.addWidget(self.btn_reset)
        VBlayout.addWidget(self.btn_cancel)

        self.setStyleSheet(stylepack)

    def btn_apply_release(self):
        global fdpack
        self.mainWindow.updateImg(fdpack.result())
        self.close()

    def btn_reset_release(self):
        global fdpack
        self.mainWindow.window_dehair_l.sl_mediank.setValue(fdpack.default_v[0])
        self.mainWindow.window_dehair_l.sl_th_min.setValue(fdpack.default_v[1])
        self.mainWindow.window_dehair_l.sl_th_max.setValue(fdpack.default_v[2])
        self.mainWindow.window_dehair_l.sl_thi_min.setValue(fdpack.default_v[3])
        self.mainWindow.window_dehair_l.sl_thi_max.setValue(fdpack.default_v[4])
        self.mainWindow.window_dehair_l.sl_soft.setValue(fdpack.default_v[5])
        self.mainWindow.isBusy()
        fdpack.setDefault()
        fdpack.start()
        self.mainWindow.qt_imshow(fdpack.result())
        self.mainWindow.hist_show(fdpack.result())
        self.mainWindow.isBusy(False)

    def btn_cancel_release(self):
        self.close()

    def closeEvent(self, event):
        global img_current, fdpack
        self.mainWindow.qt_imshow(img_current)
        self.mainWindow.showMenuWindow()
        self.mainWindow.hist_show(img_current)
        fdpack = None
        event.ignore()

    def btn_help_release(self):
        self.mainWindow.window_help.show("Beeswax")


class WindowInpaint_L(QtWidgets.QWidget):
    def __init__(self, mainWindow):
        super(WindowInpaint_L, self).__init__()
        self.mainWindow = mainWindow

        self.btn_method1 = genButton(self, lang["Telea"], None, self.btn_method1_release, "1")
        self.btn_method2 = genButton(self, lang["Navier-Stokes"], None, self.btn_method2_release, "2")
        self.sl_brush = genSlider(self, lang["Brush Size"], 1, 150, 1, 0, self.updateParam)
        self.sl_radius = genSlider(self, lang["Search Radius"], 1, 100, 1, 0, self.updateParam)
        self.btn_undo = genButton(self, lang["Undo"], None, self.btn_undo_release, "Ctrl+Z", style=3)
        self.btn_redo = genButton(self, lang["Redo"], None, self.btn_redo_release, "Ctrl+Y", style=4)

        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.setAlignment(QtCore.Qt.AlignTop)
        VBlayout.addWidget(genLabel(self, lang["Inpaint Method"]))
        VBlayout.addWidget(self.btn_method1)
        VBlayout.addWidget(self.btn_method2)
        VBlayout.addWidget(genLabel(self, lang["Brush Size"]))
        VBlayout.addLayout(self.sl_brush)
        VBlayout.addWidget(genLabel(self, lang["Compute Range"]))
        VBlayout.addLayout(self.sl_radius)
        HBlayout = QtWidgets.QHBoxLayout()
        HBlayout.addWidget(self.btn_undo)
        HBlayout.addWidget(self.btn_redo)
        VBlayout.addLayout(HBlayout)

        self.setStyleSheet(stylepack)

    def updateParam(self):
        global inptpack
        inptpack.setParam(linethick=self.sl_brush.value(),
                          radius=self.sl_radius.value())

    def btn_method1_release(self):
        global inptpack
        inptpack.setParam(method=0)
        self.enableButtons()

    def btn_method2_release(self):
        global inptpack
        inptpack.setParam(method=1)
        self.enableButtons()

    def btn_undo_release(self):
        global inptpack
        self.mainWindow.isBusy()
        inptpack.undo()
        self.mainWindow.qt_imshow(inptpack.getView())
        self.checkUndo()
        self.mainWindow.isBusy(False)

    def btn_redo_release(self):
        global inptpack
        self.mainWindow.isBusy()
        inptpack.redo()
        self.mainWindow.qt_imshow(inptpack.getView())
        self.checkUndo()
        self.mainWindow.isBusy(False)

    def enableButtons(self):
        global inptpack
        brush, rad, method = inptpack.getParam()
        self.sl_brush.setValue(brush)
        self.sl_radius.setValue(rad)
        if method == 0:
            self.btn_method1.setEnabled(False)
            self.btn_method2.setEnabled(True)
        else:
            self.btn_method1.setEnabled(True)
            self.btn_method2.setEnabled(False)

    def checkUndo(self, flag=False):
        global inptpack
        if not flag:
            self.btn_redo.setEnabled(inptpack.redoCheck())
            self.btn_undo.setEnabled(inptpack.undoCheck())
        else:
            self.btn_redo.setEnabled(False)
            self.btn_undo.setEnabled(False)


class WindowInpaint_R(QtWidgets.QWidget):
    def __init__(self, mainWindow):
        super(WindowInpaint_R, self).__init__()
        self.mainWindow = mainWindow

        self.hist_view = genHist(self)
        self.btn_apply = genButton(self, lang["Apply"], None, self.btn_apply_release, "Return", style=2)
        self.btn_reset = genButton(self, lang["Reset"], None, self.btn_reset_release, "R", style=5)
        self.btn_cancel = genButton(self, lang["Cancel"], None, self.btn_cancel_release, "Escape")

        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.setAlignment(QtCore.Qt.AlignTop)
        VBlayout.addWidget(self.hist_view)
        VBlayout.addWidget(genLabel(self, lang["Apply to Image"]))
        VBlayout.addWidget(self.btn_apply)
        VBlayout.addWidget(self.btn_reset)
        VBlayout.addWidget(self.btn_cancel)

        self.setStyleSheet(stylepack)

    def btn_apply_release(self):
        global inptpack
        self.mainWindow.updateImg(inptpack.getImage())
        self.close()

    def btn_reset_release(self):
        global inptpack, img_current, maxUndoSize
        inptpack = InPaint(img_current,
                           self.mainWindow.window_inpt_l.sl_brush.value(),
                           self.mainWindow.window_inpt_l.sl_radius.value(), )
        inptpack.maxUndoSize = maxUndoSize
        self.mainWindow.window_inpt_l.enableButtons()
        self.mainWindow.window_inpt_l.checkUndo(True)
        self.mainWindow.qt_imshow(inptpack.getImage())
        self.enableButtons()

    def btn_cancel_release(self):
        self.close()

    def closeEvent(self, event):
        global img_current, taskState, inptpack
        self.mainWindow.viewer.stopDrawing()
        self.mainWindow.crosshairCursor(False)
        self.mainWindow.showMenuWindow()
        self.mainWindow.qt_imshow(img_current)
        self.mainWindow.hist_show(img_current)
        inptpack = None
        taskState = 0
        event.ignore()

    def enableButtons(self):
        global inptpack
        self.mainWindow.hist_show(inptpack.getImage())
        if inptpack.firstRun:
            self.btn_apply.setEnabled(False)
            self.btn_reset.setEnabled(False)
        else:
            self.btn_apply.setEnabled(True)
            self.btn_reset.setEnabled(True)


class WindowPolish_L(QtWidgets.QWidget):
    def __init__(self, mainWindow):
        super(WindowPolish_L, self).__init__()
        self.mainWindow = mainWindow

        self.sl_sig = genSlider(self, lang["Strength"], 0, 100, 1, 80, self.updateImg)
        self.sl_dia = genSlider(self, lang["Blur Diameter"], 1, 100, 1, 30, self.updateImg)
        self.sl_white = genSlider(self, lang["Whiten"], 0, 100, 1, 0, self.updateImg2)
        self.sl_opacity = genSlider(self, lang["Opacity"], 0, 100, 1, 90, self.updateImg2)

        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.setAlignment(QtCore.Qt.AlignTop)
        VBlayout.addWidget(genLabel(self, lang["Skin Smooth"]))
        VBlayout.addLayout(self.sl_sig)
        VBlayout.addLayout(self.sl_dia)
        VBlayout.addWidget(genLabel(self, lang["Blend"]))
        VBlayout.addLayout(self.sl_opacity)
        VBlayout.addLayout(self.sl_white)

        self.setStyleSheet(stylepack)

    def updateImg(self):
        global filtpack
        self.mainWindow.isBusy()
        filtpack.skinPolish(v_d=self.sl_dia.value(),
                            v_s=self.sl_sig.value(),
                            opacity=self.sl_opacity.value(),
                            white=self.sl_white.value())
        self.mainWindow.qt_imshow(filtpack.getImage())
        self.mainWindow.hist_show(filtpack.getImage())
        self.mainWindow.isBusy(False)

    def updateImg2(self):
        global filtpack
        self.mainWindow.isBusy()
        filtpack.skinPolish(v_d=self.sl_dia.value(),
                            v_s=self.sl_sig.value(),
                            opacity=self.sl_opacity.value(),
                            white=self.sl_white.value(),
                            refresh=False)
        self.mainWindow.qt_imshow(filtpack.getImage())
        self.mainWindow.hist_show(filtpack.getImage())
        self.mainWindow.isBusy(False)


class WindowPolish_R(QtWidgets.QWidget):
    def __init__(self, mainWindow):
        super(WindowPolish_R, self).__init__()
        self.mainWindow = mainWindow

        self.hist_view = genHist(self)
        self.btn_apply = genButton(self, lang["Apply"], None, self.btn_apply_release, "Return", style=2)
        self.btn_reset = genButton(self, lang["Reset"], None, self.btn_reset_release, "R", style=5)
        self.btn_cancel = genButton(self, lang["Cancel"], None, self.btn_cancel_release, "Escape")

        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.setAlignment(QtCore.Qt.AlignTop)
        VBlayout.addWidget(self.hist_view)
        VBlayout.addWidget(genLabel(self, lang["Apply to Image"]))
        VBlayout.addWidget(self.btn_apply)
        VBlayout.addWidget(self.btn_reset)
        VBlayout.addWidget(self.btn_cancel)

        self.setStyleSheet(stylepack)

    def btn_apply_release(self):
        global filtpack
        self.mainWindow.updateImg(filtpack.getImage())
        self.close()

    def btn_reset_release(self):
        global filtpack
        self.mainWindow.window_polish_l.sl_sig.setValue(80)
        self.mainWindow.window_polish_l.sl_dia.setValue(30)
        self.mainWindow.window_polish_l.sl_opacity.setValue(90)
        self.mainWindow.window_polish_l.sl_white.setValue(0)
        self.mainWindow.window_polish_l.updateImg()

    def btn_cancel_release(self):
        self.close()

    def closeEvent(self, event):
        global img_current, filtpack
        self.mainWindow.qt_imshow(img_current)
        self.mainWindow.showMenuWindow()
        self.mainWindow.hist_show(img_current)
        filtpack = None
        event.ignore()


class WindowGlow_L(QtWidgets.QWidget):
    def __init__(self, mainWindow):
        super(WindowGlow_L, self).__init__()
        self.mainWindow = mainWindow

        self.sl_blurk = genSlider(self, lang["Blur Diameter"], 1, 100, 1, 20, self.updateImg)
        self.sl_opacity = genSlider(self, lang["Opacity"], 0, 100, 1, 50, self.updateImg)
        self.sl_glow = genSlider(self, lang["Glow"], 0, 100, 1, 10, self.updateImg)

        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.setAlignment(QtCore.Qt.AlignTop)
        VBlayout.addWidget(genLabel(self, lang["Blur Effect"]))
        VBlayout.addLayout(self.sl_blurk)
        VBlayout.addLayout(self.sl_opacity)
        VBlayout.addWidget(genLabel(self, lang["Glow Effect"]))
        VBlayout.addLayout(self.sl_glow)

        self.setStyleSheet(stylepack)

    def updateImg(self):
        global filtpack
        self.mainWindow.isBusy()
        filtpack.skinGlow(v_k=self.sl_blurk.value(),
                          opacity=self.sl_opacity.value(),
                          glow=self.sl_glow.value())
        self.mainWindow.qt_imshow(filtpack.getImage())
        self.mainWindow.hist_show(filtpack.getImage())
        self.mainWindow.isBusy(False)


class WindowGlow_R(QtWidgets.QWidget):
    def __init__(self, mainWindow):
        super(WindowGlow_R, self).__init__()
        self.mainWindow = mainWindow

        self.hist_view = genHist(self)
        self.btn_apply = genButton(self, lang["Apply"], None, self.btn_apply_release, "Return", style=2)
        self.btn_reset = genButton(self, lang["Reset"], None, self.btn_reset_release, "R", style=5)
        self.btn_cancel = genButton(self, lang["Cancel"], None, self.btn_cancel_release, "Escape")

        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.setAlignment(QtCore.Qt.AlignTop)
        VBlayout.addWidget(self.hist_view)
        VBlayout.addWidget(genLabel(self, lang["Apply to Image"]))
        VBlayout.addWidget(self.btn_apply)
        VBlayout.addWidget(self.btn_reset)
        VBlayout.addWidget(self.btn_cancel)

        self.setStyleSheet(stylepack)

    def btn_apply_release(self):
        global filtpack
        self.mainWindow.updateImg(filtpack.getImage())
        self.close()

    def btn_reset_release(self):
        global filtpack
        self.mainWindow.window_glow_l.sl_blurk.setValue(20)
        self.mainWindow.window_glow_l.sl_opacity.setValue(50)
        self.mainWindow.window_glow_l.sl_glow.setValue(10)
        self.mainWindow.window_glow_l.updateImg()

    def btn_cancel_release(self):
        self.close()

    def closeEvent(self, event):
        global img_current, filtpack
        self.mainWindow.qt_imshow(img_current)
        self.mainWindow.showMenuWindow()
        self.mainWindow.hist_show(img_current)
        filtpack = None
        event.ignore()


class WindowFilters_L(QtWidgets.QWidget):
    def __init__(self, mainWindow):
        super(WindowFilters_L, self).__init__()
        self.mainWindow = mainWindow

        self.filterTitle = genLabel(self, "")
        self.filterTitle.setAlignment(QtCore.Qt.AlignCenter)

        self.sl_blurk = genSlider(self, lang["Kernel Size"], 1, 100, 1, 20, self.updateImg)
        self.sl_sigcolor = genSlider(self, lang["Sigma-Color"], 0, 120, 1, 100, self.updateImg)
        self.sl_sigspace = genSlider(self, lang["Sigma-Space"], 0, 120, 1, 100, self.updateImg)
        self.sl_sigma = genSlider(self, lang["Sigma"], 0, 100, 1, 0, self.updateImg)
        self.sl_sharpen = genSlider(self, lang["Sharpen"], -100, 100, 1, -100, self.updateImg)
        self.sl_sharpens = genSlider(self, lang["Sharpen"], 0, 100, 1, 25, self.updateImg)
        self.sl_pixel = genSlider(self, lang["Pixelation"], 0, 100, 1, 50, self.updateImg)
        self.sl_vig = genSlider(self, lang["Vignette"], -100, 100, 1, 50, self.updateImg)
        self.sl_denoise = genSlider(self, lang["Luminance Denoise"], 0, 100, 1, 50, self.updateImg)
        self.sl_denoisec = genSlider(self, lang["Color Denoise"], 0, 100, 1, 50, self.updateImg)

        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        VBlayout.addWidget(self.filterTitle)
        VBlayout.addLayout(self.sl_blurk)
        VBlayout.addLayout(self.sl_sigcolor)
        VBlayout.addLayout(self.sl_sigspace)
        VBlayout.addLayout(self.sl_sigma)
        VBlayout.addLayout(self.sl_sharpen)
        VBlayout.addLayout(self.sl_sharpens)
        VBlayout.addLayout(self.sl_pixel)
        VBlayout.addLayout(self.sl_vig)
        VBlayout.addLayout(self.sl_denoise)
        VBlayout.addLayout(self.sl_denoisec)

        self.setStyleSheet(stylepack)
        self.hideAllSliders()

    def updateImg(self):
        global filtpack
        self.mainWindow.isBusy()
        if filtpack.mode == 1:
            filtpack.bilateral(self.sl_blurk.value(), self.sl_sharpen.value())
        elif filtpack.mode == 2:
            filtpack.bilateral2(self.sl_blurk.value(), self.sl_sigcolor.value(),
                                self.sl_sigspace.value(), self.sl_sharpen.value())
        elif filtpack.mode == 3:
            filtpack.median(self.sl_blurk.value(), self.sl_sharpen.value())
        elif filtpack.mode == 4:
            filtpack.Gaussian(self.sl_blurk.value(), self.sl_sigma.value(), self.sl_sharpen.value())
        elif filtpack.mode == 5:
            filtpack.boxBlur(self.sl_blurk.value(), self.sl_sharpen.value())
        elif filtpack.mode == 6:
            filtpack.simpleSharpen(self.sl_sharpens.value())
        elif filtpack.mode == 7:
            filtpack.pixelation(self.sl_pixel.value())
        elif filtpack.mode == 8:
            filtpack.vignette(self.sl_vig.value())
        elif filtpack.mode == 9:
            filtpack.denoise(self.sl_denoise.value(), self.sl_denoisec.value())
        self.mainWindow.qt_imshow(filtpack.getImage())
        self.mainWindow.hist_show(filtpack.getImage())
        self.mainWindow.isBusy(False)

    def showSliders(self):
        global filtpack
        self.hideAllSliders()
        if filtpack.mode in [1, 3, 5]:
            self.sl_blurk.show()
            self.sl_sharpen.show()
        elif filtpack.mode == 2:
            self.sl_blurk.show()
            self.sl_sigcolor.show()
            self.sl_sigspace.show()
            self.sl_sharpen.show()
        elif filtpack.mode == 4:
            self.sl_blurk.show()
            self.sl_sigma.show()
            self.sl_sharpen.show()
        elif filtpack.mode == 6:
            self.sl_sharpens.show()
        elif filtpack.mode == 7:
            self.sl_pixel.show()
        elif filtpack.mode == 8:
            self.sl_vig.show()
        elif filtpack.mode == 9:
            self.sl_denoise.show()
            self.sl_denoisec.show()

    def hideAllSliders(self):
        self.sl_blurk.close()
        self.sl_sharpen.close()
        self.sl_sigcolor.close()
        self.sl_sigspace.close()
        self.sl_sigma.close()
        self.sl_sharpens.close()
        self.sl_pixel.close()
        self.sl_vig.close()
        self.sl_denoise.close()
        self.sl_denoisec.close()

    def resetAll(self):
        self.filterTitle.setText(lang["Select a Filter"])
        self.hideAllSliders()
        self.sl_blurk.setValue(20)
        self.sl_sharpen.setValue(-100)
        self.sl_sigcolor.setValue(100)
        self.sl_sigspace.setValue(100)
        self.sl_sigma.setValue(0)
        self.sl_sharpens.setValue(25)
        self.sl_pixel.setValue(50)
        self.sl_vig.setValue(50)
        self.sl_denoise.setValue(40)
        self.sl_denoisec.setValue(40)
        self.mainWindow.window_filters_r.enableAll()


class WindowFilters_R(QtWidgets.QWidget):
    def __init__(self, mainWindow):
        super(WindowFilters_R, self).__init__()
        self.mainWindow = mainWindow

        self.hist_view = genHist(self)
        # self.btn_bila1 = genButton(self, lang["Bilateral Simple"], None, self.btn_bila1_release)
        self.btn_bila2 = genButton(self, lang["Bilateral Full"], None, self.btn_bila2_release)
        self.btn_median = genButton(self, lang["Median Filter"], None, self.btn_median_release)
        self.btn_Gaussian = genButton(self, lang["Gaussian Filter"], None, self.btn_Gaussian_release)
        self.btn_boxBlur = genButton(self, lang["Box Filter"], None, self.btn_boxBlur_release)
        self.btn_sharps = genButton(self, lang["Simple Sharpen"], None, self.btn_sharps_release)
        self.btn_pixel = genButton(self, lang["Pixelation"], None, self.btn_pixel_release)
        self.btn_vig = genButton(self, lang["Vignette"], None, self.btn_vig_release)
        self.btn_denoise = genButton(self, lang["Denoise (Slow)"], None, self.btn_denoise_release,style=6)

        self.btn_apply = genButton(self, lang["Apply"], None, self.btn_apply_release, "Return", style=2)
        self.btn_cancel = genButton(self, lang["Cancel"], None, self.btn_cancel_release, "Escape")

        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.setAlignment(QtCore.Qt.AlignTop)
        VBlayout.addWidget(self.hist_view)
        VBlayout.addWidget(genLabel(self, lang["Classic Filters"]))
        VBlayout.addWidget(self.btn_Gaussian)
        VBlayout.addWidget(self.btn_median)
        VBlayout.addWidget(self.btn_boxBlur)
        # VBlayout.addWidget(self.btn_bila1)
        VBlayout.addWidget(self.btn_bila2)
        VBlayout.addWidget(self.btn_denoise)
        VBlayout.addWidget(self.btn_sharps)
        VBlayout.addWidget(self.btn_pixel)
        VBlayout.addWidget(self.btn_vig)

        VBlayout.addWidget(genLabel(self, lang["Apply to Image"]))
        VBlayout.addWidget(self.btn_apply)
        VBlayout.addWidget(self.btn_cancel)

        self.setStyleSheet(stylepack)

    def enableAll(self):
        # self.btn_bila1.setEnabled(True)
        self.btn_bila2.setEnabled(True)
        self.btn_median.setEnabled(True)
        self.btn_Gaussian.setEnabled(True)
        self.btn_boxBlur.setEnabled(True)
        self.btn_sharps.setEnabled(True)
        self.btn_pixel.setEnabled(True)
        self.btn_vig.setEnabled(True)
        self.btn_denoise.setEnabled(True)

    def btn_bila1_release(self):
        global filtpack
        self.enableAll()
        self.btn_bila1.setEnabled(False)
        filtpack.mode = 1
        self.mainWindow.window_filters_l.filterTitle.setText(self.btn_bila1.text())
        self.mainWindow.window_filters_l.showSliders()
        self.mainWindow.window_filters_l.updateImg()

    def btn_bila2_release(self):
        global filtpack
        self.enableAll()
        self.btn_bila2.setEnabled(False)
        filtpack.mode = 2
        self.mainWindow.window_filters_l.filterTitle.setText(self.btn_bila2.text())
        self.mainWindow.window_filters_l.showSliders()
        self.mainWindow.window_filters_l.updateImg()

    def btn_median_release(self):
        global filtpack
        self.enableAll()
        self.btn_median.setEnabled(False)
        filtpack.mode = 3
        self.mainWindow.window_filters_l.filterTitle.setText(self.btn_median.text())
        self.mainWindow.window_filters_l.showSliders()
        self.mainWindow.window_filters_l.updateImg()

    def btn_Gaussian_release(self):
        global filtpack
        self.enableAll()
        self.btn_Gaussian.setEnabled(False)
        filtpack.mode = 4
        self.mainWindow.window_filters_l.filterTitle.setText(self.btn_Gaussian.text())
        self.mainWindow.window_filters_l.showSliders()
        self.mainWindow.window_filters_l.updateImg()

    def btn_boxBlur_release(self):
        global filtpack
        self.enableAll()
        self.btn_boxBlur.setEnabled(False)
        filtpack.mode = 5
        self.mainWindow.window_filters_l.filterTitle.setText(self.btn_boxBlur.text())
        self.mainWindow.window_filters_l.showSliders()
        self.mainWindow.window_filters_l.updateImg()

    def btn_sharps_release(self):
        global filtpack
        self.enableAll()
        self.btn_sharps.setEnabled(False)
        filtpack.mode = 6
        self.mainWindow.window_filters_l.filterTitle.setText(self.btn_sharps.text())
        self.mainWindow.window_filters_l.showSliders()
        self.mainWindow.window_filters_l.updateImg()

    def btn_pixel_release(self):
        global filtpack
        self.enableAll()
        self.btn_pixel.setEnabled(False)
        filtpack.mode = 7
        self.mainWindow.window_filters_l.filterTitle.setText(self.btn_pixel.text())
        self.mainWindow.window_filters_l.showSliders()
        self.mainWindow.window_filters_l.updateImg()

    def btn_vig_release(self):
        global filtpack
        self.enableAll()
        self.btn_vig.setEnabled(False)
        filtpack.mode = 8
        self.mainWindow.isBusy()
        filtpack.setVignette()
        self.mainWindow.isBusy(False)
        self.mainWindow.window_filters_l.filterTitle.setText(self.btn_vig.text())
        self.mainWindow.window_filters_l.showSliders()
        self.mainWindow.window_filters_l.updateImg()

    def btn_denoise_release(self):
        global filtpack
        self.enableAll()
        self.btn_denoise.setEnabled(False)
        filtpack.mode = 9
        self.mainWindow.window_filters_l.filterTitle.setText(self.btn_denoise.text())
        self.mainWindow.window_filters_l.showSliders()
        self.mainWindow.window_filters_l.updateImg()

    def btn_apply_release(self):
        global filtpack
        self.mainWindow.updateImg(filtpack.getImage())
        self.close()

    def btn_cancel_release(self):
        self.close()

    def closeEvent(self, event):
        global img_current, filtpack
        self.mainWindow.qt_imshow(img_current)
        self.mainWindow.showMenuWindow()
        self.mainWindow.hist_show(img_current)
        filtpack = None
        event.ignore()


def loadConfig():
    global config, lang, maxUndoSize
    try:
        with open('GUI/config.pickle', 'rb') as handle:
            config = pickle.load(handle)
            print(config)
    except:
        print("no config")
        return False
    else:
        maxUndoSize = config["maxUndoSize"]
        if config["language"] == "cn_s":
            lang = lang_cn_s
        else:
            lang = lang_en
        return True


def saveConfig():
    global config
    try:
        with open('GUI/config.pickle', 'wb') as handle:
            pickle.dump(config, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print("save config")
    except:
        print("Cannot Save Config")


if __name__ == '__main__':
    maxUndoSize = 5
    taskState = 0
    """
    0: no task, viewing
    1: Grabcut - ROI
    2: Grabcut - foreground
    3: Grabcut - background
    4: Magic Wand - init
    5: Magic Wand - foreground
    6. Magic Wand - background
    7. Common Selection - init
    8. Common Selection - run
    9. Inpaint
    10. Color Range Selection
    """
    img_input, img_current, img_view = None, None, None  # Input image, current image, temp image for viewer
    filepath, tempfilepath = None, None
    fdpack, gbcpack, mwdpack, sksepack, csepack = None, None, None, None, None
    madjpack, iadjpack, inptpack, filtpack = None, None, None, None
    mask_current, mask_view, mask_check = None, None, None
    drawMask, fastPreview = None, None
    HASMASK = False

    lineColor, lineThick = (255, 255, 255), 3
    maskUndoStack, imgUndoStack = [], []
    maskUndoPtr, imgUndoPtr = 0, 0

    appMainWindow = None
    app = QtWidgets.QApplication(sys.argv)


    def startMain():
        global appMainWindow
        appMainWindow = Window()
        appMainWindow.resize(1080, 640)
        appMainWindow.show()
        appMainWindow.showHelloScreen()
        #appMainWindow.loadImage(r"./Sample/香菇腿子原图.jpg")


    config = {
        "version": version,
        "firstRun": False,
        "language": "cn_s",
        "maxUndoSize": 8,
    }

    if not loadConfig():
        helloWindow = WindowSettings()
        helloWindow.resize(800, 600)
        helloWindow.show()
    else:
        startMain()

    sys.exit(app.exec_())
