# -*- coding : UTF-8 -*-
import xml.sax
import urllib3
import os
import os.path
import Encode485Protocol
import platform
import json
from xml.dom.minidom import parse
import xml.dom.minidom


medias = []
lineDatas = []

class PackageSoueceHandle(xml.sax.ContentHandler):

    def __init__(self,rootPath):

        self.rootPath = rootPath
        self.objs = []

    def startElement(self, name, attrs):
        if name == "Source":

            obj = {}
            obj["savePath"] = (self.rootPath+os.sep+"source"+os.sep+attrs["savePath"]).replace("\\",os.path.sep).replace("/",os.path.sep)
            obj["url"] = attrs["url"].replace("\\",os.path.sep).replace("/",os.path.sep)

            self.objs.append(obj)

    def endDocument(self):
        global medias
        medias = self.objs



class Media485ProtocolHandle(xml.sax.ContentHandler):

    def __init__(self,filePath,protocolType):

        self.filePath = filePath
        self.protocolType = protocolType
        self.lineId = ""
        self.lineName = ""

        self.stationUpCount =0
        self.stationDownCount =0

        self.stationUpIndexs = []
        self.stationDownIndexs = []

    def startElement(self, name, attrs):
        if name == "LineInfo":
            self.lineId = attrs["lineId"]
            self.lineName = attrs["lineName"]

        elif name == "Station":
            #上行
            if ("1"==attrs["lineType"]) :
                self.stationUpIndexs.append(attrs["seq"])
                self.stationUpCount +=1
            elif ("2"== attrs["lineType"] ) :
                self.stationDownIndexs.append(attrs["seq"])
                self.stationDownCount +=1

    def endDocument(self):
        data = []

        if (self.protocolType == 0):
            data = Encode485Protocol.constructWZ485Protocol(self)
        elif (self.protocolType == 1):
            data = Encode485Protocol.constructXian485Protocol(self)

        savePath = self.filePath.strip(".xml") + ".txt"

        writeDataToFile(savePath, data)


class MediaPackageCheck:


    def deviceDirCheck(self,path):
        failMsgs = []
        result = "[pass]"
        cicDirPath = path+os.sep+"cictec"
        mediaDirPath = cicDirPath + os.sep + "media"
        configDirPath = cicDirPath + os.sep + "config"

        #cictec文件夹校验
        if( not os.path.exists(cicDirPath)):
            result = "[fail]"
            failMsgs.append("[ERROR: %s，not exists!]" % (cicDirPath))
        else:
            #author文件校验
            result = self.authorCheck(result,(cicDirPath + os.sep + "author"),failMsgs)

            #media文件夹校验
            if (not os.path.exists(mediaDirPath)):
                result = "[fail]"
                failMsgs.append("[ERROR: %s，not exists!]" % (mediaDirPath))
            else:
                #media.xml校验
                result = self.mediaXmlCheck(result,(mediaDirPath + os.sep + "media.xml"),failMsgs,path.strip(os.path.basename(path)))

            #config文件夹校验
            if (not os.path.exists(configDirPath)):
                result = "[fail]"
                failMsgs.append("[ERROR: %s，not exists!]" % (configDirPath))
            else:
                #configInfo.json校验
                result = self.configInfoJsonCheck(result,(configDirPath + os.sep + "configInfo.json"),failMsgs)

                #control.xml校验
                result = self.controlXmlCheck(result,(configDirPath + os.sep + "control.xml"),failMsgs)

                #lines.xml校验
                result = self.linesXmlCheck(result,(configDirPath + os.sep + "lines.xml"),failMsgs)

                #source.xml校验
                result = self.sourceXmlCheck(result,(configDirPath + os.sep + "source.xml"),failMsgs)

        return result,failMsgs

    def authorCheck(self,result,path,failMsgs):

        if (not os.path.exists(path)):
            result = "[fail]"
            failMsgs.append(
                "[ERROR: %s，not exists!]" % path)
        else:
            print()
            #TODO
        return result

    def linesXmlCheck(self,result,path,failMsgs):

        if (not os.path.exists(path)):
            result = "[fail]"
            failMsgs.append(
                "[ERROR: %s，not exists!]" % path)
        else:
            print()
            #TODO

        return result

    def sourceXmlCheck(self,result,path,failMsgs):

        if (not os.path.exists(path)):
            result = "[fail]"
            failMsgs.append(
                "[ERROR: %s，not exists!]" % path)
        else:
            print()
            # TODO
        return result



    def configInfoJsonCheck(self,result,path,failMsgs):

        if (not os.path.exists(path)):
            result = "[fail]"
            failMsgs.append(
                "[ERROR: %s，not exists!]" % path)
        else:
            with open(path, 'r') as f:
                data = json.load(f)

                keys = ["cityId","ip","operationalType","port","protocol"]

                for key in keys:
                    if not key in data :
                        result = "[fail]"
                        failMsgs.append("﻿[ERROR: file: %s 中缺少字段:%s]" % (path,key))
                    else:
                        if(len(data[key])==0):
                            result = "[fail]"
                            failMsgs.append("﻿[ERROR: file: %s 中缺少字段:%s]" % (path, key))
        return result


    def controlXmlCheck(self,result,path,failMsgs):

        if (not os.path.exists(path)):
            result = "[fail]"
            failMsgs.append(
                "[ERROR: %s，not exists!]" % path)
        else:
            DOMTree = xml.dom.minidom.parse(path)
            collection = DOMTree.documentElement
            #热点checked

            if len(collection.getElementsByTagName("BitmapResources")) != 2:
                result = "[fail]"
                failMsgs.append(
                    "[ERROR: %s，DefaultBitmap node size error!]" % path)

            #默认列表checked
            defaultProgramme = collection.getElementsByTagName("DefaultProgramme")
            if len(defaultProgramme)==1:
                defaultPlan =  defaultProgramme[0].getElementsByTagName("Plan")
                if len(defaultPlan)!=4:
                    result = "[fail]"
                    failMsgs.append(
                        "[ERROR: %s，DefaultProgramme Plan node size error!]" % path)
            else:
                result = "[fail]"
                failMsgs.append(
                    "[ERROR: %s，DefaultProgramme size error!]" % path)

            #播放列表checked
            # programme = collection.getElementsByTagName("Programme")

        return result

    def lineStationXmlCheck(self,result,path,failMsgs):

        if (not os.path.exists(path)):
            result = "[fail]"
            failMsgs.append(
                "[ERROR: %s，not exists!]" % path)
        else:
            print()
            # TODO
        return result


    def mediaXmlCheck(self,result,path,failMsgs,rootPath):

        if (not os.path.exists(path)):
            result = "[fail]"
            failMsgs.append(
                "[ERROR: %s，not exists!]" % path)
        else:
            # 使用minidom解析器打开 XML 文档
            DOMTree = xml.dom.minidom.parse(path)
            collection = DOMTree.documentElement
            mediaList = collection.getElementsByTagName("Media")
            for media in mediaList:
                if(
                        media.hasAttribute("id") and
                        media.hasAttribute("name") and
                        media.hasAttribute("path") and
                        media.hasAttribute("validateKey")):
                    filePath = (rootPath+os.sep+"source"+os.sep+media.getAttribute("path")).replace("\\",os.path.sep).replace("/",os.path.sep)
                    if not os.path.exists(filePath):
                        result = "[fail]"
                        failMsgs.append(
                            "[ERROR:%s 中, %s，not exists!]" % (path,filePath))
                    #文件校验码校验
                    else:
                        validateKey = media.getAttribute("validateKey")
                        print("path : %s ,vilidateKey: %s . checked" % (filePath,validateKey))
                        #TODO
        return result



def writeDataToFile(savePath,data):
    fileDir = os.path.dirname(savePath)
    if not os.path.exists(fileDir):
        os.makedirs(fileDir)
    file_object = open(savePath, 'w')
    for i in data:
        file_object.write(i)
        file_object.write("\n")
    file_object.close()
    openExplorerByFile(savePath)

def openExplorerByFile(filePath):
    dirPath = filePath.strip(os.path.basename(filePath))
    sysstr = platform.system()
    if (sysstr == "Windows"):
        os.system("explorer.exe %s" % dirPath)
    elif (sysstr == "Darwin"):
        os.system("open %s" % filePath)

def processMediaResourceDownload(rootPath):
    sourceHandle = PackageSoueceHandle(rootPath)
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    parser.setContentHandler(sourceHandle)
    parser.parse(rootPath + os.sep + "source" + os.sep + "packageSource.xml")
    return medias

def processMedia485Protocol(filePath,protocolType):
    handle = Media485ProtocolHandle(filePath,protocolType)
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    parser.setContentHandler(handle)
    parser.parse(filePath)


def httpDownload(url, savePath):
    http = urllib3.PoolManager()
    response = http.request("GET", url)
    fileDir = os.path.dirname(savePath)
    if not os.path.exists(fileDir):
        os.makedirs(fileDir)
    with open(savePath, 'wb') as fp:
        fp.write(response.data)
    response.release_conn()
    fp.close()



