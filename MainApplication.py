# -*- coding: UTF-8 -*-

from PyQt5 import QtWidgets,QtCore
import sys

from PyQt5.QtCore import pyqtSignal

from mainwindow import Ui_MainWindow
import MediaProcessHandle
import os
import shutil
import re

#媒体文件夹处理类型
packageProcesType = 0
#协议生成类型
xmlProcesProtocolType = 0

class Runthread(QtCore.QThread):
    # python3,pyqt5与之前的版本有些不一样
    #  通过类成员对象定义信号对象
    _signal = pyqtSignal(str)

    def __init__(self, rootPath):
        super(Runthread, self).__init__()
        self.rootPath = rootPath

    def __del__(self):
        self.wait()

    def run(self):

        self._signal.emit("媒体资源下载，processing...")
        self._signal.emit("开始解析packageSource.xml!")
        try:
            medias = MediaProcessHandle.processMediaResourceDownload(self.rootPath)
            self._signal.emit("packageSource.xml解析完毕，共%d条记录" % len(medias))
            self._signal.emit("开始下载媒体资源...")
            index = 0
            for media in medias:
                index += 1
                self._signal.emit("(%d/%d)开始下载文件:%s" % (index,len(medias),media["url"]))
                MediaProcessHandle.httpDownload(media["url"], media["savePath"])
                self._signal.emit("保存到:%s" % (media["savePath"]))
            self._signal.emit("下载完成！")
        except BaseException:
            self._signal.emit("执行失败，请检查ctctecMedia包!")

    # def callback(self, msg):
        # self._signal.emit(msg);

class mywindow(QtWidgets.QMainWindow,Ui_MainWindow):

    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)

    def selectPackagePath(self):
        fileName = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                                    "选取文件",
                                                                    "")

        if(len(fileName) != 0):
            self.le_package_path.setText(fileName.replace("\\",os.path.sep).replace("/",os.path.sep))

    def selectLineXmlPath(self):
        fileName,type = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                    "选取文件",
                                                                    "","Xml Files (*.xml)")
        if(len(fileName) != 0):
            self.le_line_xml_path.setText(fileName.replace("\\",os.path.sep).replace("/",os.path.sep))

    def packageProcesStart(self):
        self.pte_log.clear()
        rootPath = self.le_package_path.text()

        if rootPath and len(rootPath)>0:
            if(os.path.basename(rootPath)=="cictecMedia"):
               self.packageProcesByType(rootPath)
            else:
               self.pte_log.appendPlainText("ERROR:根目录必须为：cictecMedia！")
        else:
            self.pte_log.appendPlainText("ERROR:文件路径不能为空!")

    def xmlProtocolProcesStart(self):
        self.pte_log.clear()
        rootPath = self.le_line_xml_path.text()
        print(xmlProcesProtocolType)
        if rootPath and len(rootPath)>0:
            self.xmlProtocolProcesByType(rootPath)
        else:
            self.pte_log.appendPlainText("ERROR:文件路径不能为空！")

    def changePackageProcesType(self):
        global packageProcesType
        packageProcesType = self.cb_proces_type.currentIndex()

    def changeLineXmlProtocolType(self):
        global xmlProcesProtocolType
        xmlProcesProtocolType = self.cb_protocol_type.currentIndex()

    def packageProcesByType(self,rootPath):
        #媒体资源下载
        if packageProcesType == 0:
            self.thread = Runthread(rootPath)
            self.thread._signal.connect(self.callbacklog)
            self.thread.start()
        #apk拷贝
        elif packageProcesType == 1:
            fileName, type = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                   "选取文件",
                                                                   "", "apk Files (*.apk)")
            self.pte_log.appendPlainText("APK拷贝，processing...")
            if (len(fileName) != 0):
                fileList = os.listdir(rootPath)
                for deviceDir in fileList:
                    if (deviceDir != "source"):
                        if re.match('^[0-9A-z]+$', deviceDir):
                            pathTmp = os.path.join(rootPath, deviceDir)+os.sep+"app"
                            if not os.path.exists(pathTmp):
                                os.mkdir(pathTmp)
                            shutil.copyfile(fileName,pathTmp+os.sep+os.path.basename(fileName))
                            self.pte_log.appendPlainText("设备【" + deviceDir + "】\tcopy\t [success]")
                        else:
                            self.pte_log.appendPlainText("[ERROR,目录: %s 名称不合法]" % deviceDir)
                self.pte_log.appendPlainText("拷贝完成！")

        elif packageProcesType == 2:
            self.pte_log.appendPlainText("媒体文件夹校验,processing...")

            fileList = os.listdir(rootPath)

            # 1.source文件夹校验
            if os.path.exists(rootPath + os.sep + "source"):

                result = "[pass]"
                failMsgs = []

                try:
                    medias = MediaProcessHandle.processMediaResourceDownload(rootPath)

                    for media in medias:
                        if not os.path.exists(media["savePath"]):
                            failMsgs.append("[ERROR: %s，not exists!]" % media["savePath"])
                            result = "[fail]"
                            continue
                    self.pte_log.appendPlainText("资源文件【source】\t\t\tchecked\t" + result)

                except BaseException:
                    result = "[fail]"
                    failMsgs.append("source文件夹校验失败！")
                if (result == "[fail]"):
                    for failMsg in failMsgs:
                        self.pte_log.appendPlainText(failMsg)
            else:
                self.pte_log.appendPlainText("资源文件【source】\t\t\tchecked\t[fail]")
                return

            # 2.设备文件夹校验
            for dirName in fileList:
                if (dirName != "source"):
                    if re.match('^[0-9A-z]+$', dirName):
                        packageCheck = MediaProcessHandle.MediaPackageCheck()
                        result,failMsgs = packageCheck.deviceDirCheck(rootPath+os.sep+dirName)
                        self.pte_log.appendPlainText("设备【"+dirName+"】\t\tchecked\t"+result)
                        if (result == "[fail]"):
                            for failMsg in failMsgs:
                                self.pte_log.appendPlainText(failMsg)
                    else:
                        self.pte_log.appendPlainText("[ERROR:目录 %s 文件名不合法！]" % dirName)

            self.pte_log.appendPlainText("FINISH!")
        elif packageProcesType in (3,4,5,6,7,8,9):
            self.pte_log.appendPlainText("待开发...")




    def callbacklog(self, msg):
        # 回调数据输出到文本框
        self.pte_log.appendPlainText(msg);

    def xmlProtocolProcesByType(self, rootPath):
        if(xmlProcesProtocolType in (0,1) ):
            self.pte_log.appendPlainText("processing...")
            self.pte_log.appendPlainText("开始解析文件!")
            try:
                MediaProcessHandle.processMedia485Protocol(rootPath, xmlProcesProtocolType)
                self.pte_log.appendPlainText("解析文件完成!")
                self.pte_log.appendPlainText("485协议文件路径："+rootPath.strip(".xml") + ".txt")
            except BaseException:
                self.pte_log.appendPlainText("解析失败，请检查线路xml!")
        else:
            self.pte_log.appendPlainText("待开发...")



app = QtWidgets.QApplication(sys.argv)
windows = mywindow()
windows.show()
sys.exit(app.exec_())



