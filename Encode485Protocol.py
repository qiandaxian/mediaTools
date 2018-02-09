# -*- coding: UTF-8 -*-



#网智协议start
def constructWZ485Protocol(self):

    data = []

    for index in self.stationUpIndexs:
        str1 = encodeWZ485(self.lineId, "00",  index, "00", self.stationUpCount)
        data.append(str1)
        str2 = encodeWZ485(self.lineId, "01",  index, "00", self.stationUpCount)
        data.append(str2)

    for index in self.stationDownIndexs:
        str1 = encodeWZ485(self.lineId, "00",  index, "01", self.stationDownCount)
        data.append(str1)
        str2 = encodeWZ485(self.lineId, "01",  index, "01", self.stationDownCount)
        data.append(str2)
    return data


def encodeWZ485(lineId,entryOutType,index,lineType,count):

    while len(lineId)<4:
        lineId = "0"+lineId

    head = "242424247F"
    lineId = bytes.hex(bytes((int(lineId),))).upper()
    msgLength = bytes.hex(bytes((17,)))
    lineNameHex =  bytes.hex(bytes(lineId, 'ascii')).upper()
    lineIndex = bytes.hex(bytes((int(index),))).upper()
    stationCount = bytes.hex(bytes((count,))).upper()

    str1 = head+lineId+msgLength+lineType+entryOutType+lineNameHex+stationCount+lineIndex+"1183"
    return str1
#网智协议end


#西安协议start
def constructXian485Protocol(self):
    data = []
    #上行
    initUpStr = encodeXian485Init(self.lineId,"30",self.stationUpCount)
    data.append(initUpStr)
    for index in self.stationUpIndexs:
        str1 = encodeXian485("31",  index, "30", self.stationUpCount)
        data.append(str1)
        str2 = encodeXian485("30",  index, "30", self.stationUpCount)
        data.append(str2)

    #下行
    initDownStr = encodeXian485Init(self.lineId,"31",self.stationDownCount)
    data.append(initDownStr)
    for index in self.stationDownIndexs:
        str1 = encodeXian485("31",  index, "31", self.stationDownCount)
        data.append(str1)
        str2 = encodeXian485("30",  index, "31", self.stationDownCount)
        data.append(str2)


    return data


def encodeXian485Init(lineId, lineType, count):
    while len(lineId) < 5:
        lineId = "0" + lineId

    head = "7E0003E50300299932AA00"
    lineIdHex = bytes.hex(bytes(lineId, 'ascii')).upper()
    serviceCode = "393900"

    stationCount = bytes.hex(bytes((count,))).upper()

    str1 = head + lineIdHex + serviceCode + lineType+ stationCount + "0102030405060708090A0B0C0D0E0F1011121314157F"
    return str1

def encodeXian485(entryOutType, index, lineType, count):
    head = "7E0003E00E002A00DC8D01"

    lineIndex = bytes.hex(bytes((int(index),))).upper()
    stationCount = bytes.hex(bytes((count,))).upper()

    str1 = head + entryOutType + lineType + stationCount + lineIndex + "CBAEB0B6B6ABB7BD00000000000000000000000000000000000000007F"
    return str1

#西安协议end