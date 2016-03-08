#coding=utf-8

import json,urllib2,os,re

# セッション情報を取得する
# header: jsonデータにするために不必要なphrase
def loadProgramInfo(url,header):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    data = response.read()
    lines = data.split(os.linesep)
    page = ""
    for line in lines:
        line = line.replace('	',' ')
        line = re.sub(r'<u.*</u>','',line)
        page = page + line
    jsonstr = page.replace(header,'')
    jsonstr = re.sub(r',(¥s|¥t| )*}','}',jsonstr)
    jsonstr = re.sub(r',(¥s|¥t| )*]',']',jsonstr)
    program = json.loads(jsonstr, "utf-8")
    return program

# 論文情報を取る
def getPaperInfo(url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    data = response.read().replace("callback(","")[:-1].replace("	"," ")
    data = data.decode('utf-8')
    # ゴミを取る
    for i in range(0,32):
        data = data.replace(unichr(i),'')
    papers = json.loads(data)
    return papers

# タイムスロットの情報を取得する
def getSlotInfo(program):
    dayno = 0
    curday = ""
    slots = {}
    for line in program["timetable"]:
        slot = {}
        slotinfo = re.match(u'セッション(.*)：(.*)月(.*)日（(.*)）(.*)〜(.*)',line)
        slot["session_no"] = slotinfo.group(1)
        if curday == "" or curday != slotinfo.group(2)+"/"+slotinfo.group(3):
            curday = slotinfo.group(2)+"/"+slotinfo.group(3)
            dayno = dayno + 1
        slot["day"] = dayno
        slot["start"] = slotinfo.group(5)
        slot["end"] = slotinfo.group(6)
        slots[slotinfo.group(1)]=slot
    return slots