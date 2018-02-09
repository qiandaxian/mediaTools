# -*- coding : UTF-8 -*-
import xml.sax
import urllib3
import os
import os.path
import Encode485Protocol
import platform

medias = []
lineDatas = []

class PackageSoueceHandle(xml.sax.ContentHandler):

    def __init__(self,rootPath):

        self.rootPath = rootPath
        self.objs = []

    def startElement(self, name, attrs):
        if name == "Source":

            self.savePath = attrs["savePath"]
            self.url = attrs["url"]

            obj = {}
            obj["savePath"] = self.rootPath+os.sep+"source"+os.sep+attrs["savePath"]
            obj["url"] = attrs["url"]

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

        #cictec文件夹校验
        if( not os.path.exists(path+os.sep+"cictec")):
            result = "[fail]"
            failMsgs.append("[ERROR: %s，not exists!]" % (path+os.sep+"cictec"))
        else:
            #author文件校验
            result = self.authorCheck(result,(path + os.sep + "cictec" + os.sep + "author"),failMsgs)

            #media文件夹校验
            if (not os.path.exists(path + os.sep+ "cictec" + os.sep + "media")):
                result = "[fail]"
                failMsgs.append("[ERROR: %s，not exists!]" % (path + os.sep+ "cictec" + os.sep + "media"))
            else:
                #media.xml校验
                result = self.mediaXmlCheck(result,(path + os.sep + "cictec" + os.sep + "media" + os.sep + "media.xml"),failMsgs)

            #config文件夹校验
            if (not os.path.exists(path + os.sep + "cictec"+os.sep+"config")):
                result = "[fail]"
                failMsgs.append("[ERROR: %s，not exists!]" % (path + os.sep + "cictec"+os.sep+"config"))
            else:
                #configInfo.json校验
                result = self.configInfoJsonCheck(result,(path + os.sep + "cictec" + os.sep + "config" + os.sep + "configInfo.json"),failMsgs)

                #control.xml校验
                result = self.controlXmlCheck(result,(path + os.sep + "cictec" + os.sep + "config" + os.sep + "control.xml"),failMsgs)

                #lines.xml校验
                result = self.linesXmlCheck(result,(path + os.sep + "cictec" + os.sep + "config" + os.sep + "lines.xml"),failMsgs)

                #source.xml校验
                result = self.sourceXmlCheck(result,(path + os.sep + "cictec" + os.sep + "config" + os.sep + "source.xml"),failMsgs)

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
            print()
            # TODO
        return result


    def controlXmlCheck(self,result,path,failMsgs):

        if (not os.path.exists(path)):
            result = "[fail]"
            failMsgs.append(
                "[ERROR: %s，not exists!]" % path)
        else:
            print()
            # TODO
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


    def mediaXmlCheck(self,result,path,failMsgs):

        if (not os.path.exists(path)):
            result = "[fail]"
            failMsgs.append(
                "[ERROR: %s，not exists!]" % path)
        else:
            print()
            # TODO
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



