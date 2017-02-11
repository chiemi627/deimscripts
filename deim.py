#coding=utf-8

import json,urllib2,os,re,string

# セッション情報をURLから取得する
# header: jsonデータにするために不必要なphrase
def loadProgramInfo(url,header):
    try:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        data = response.read()
    except:
        raise
    return loadProgramInfoFromJsonData(data,header)
    
# セッション情報をJSONファイルから取得
def loadProgramInfoFromJsonData(data,header):
    lines = data.split(os.linesep)
    page = ""
    for line in lines:
        line = line.replace('	',' ')
        line = re.sub(r'<u.*</u>','',line)
        page = page + line
    jsonstr = page.replace(header,'')
    jsonstr = re.sub(r',(¥s|¥t| )*}','}',jsonstr)
    jsonstr = re.sub(r',(¥s|¥t| )*]',']',jsonstr)
    try:
        program = json.loads(jsonstr, "utf-8")
    except ValueError, e:
        raise
    return program

# 論文情報を取る
def getPaperInfo(url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    papers = getPaperInfoFromJsonData(response.read())
    return papers
    
def getPaperInfoFromJsonData(data):
    data = data.replace("callback(","")[:-1].replace("	"," ")
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
        try:
            slot = {}
            slotinfo = re.match(u'セッション(.*)：(.*)月(.*)日[（\(](.*)[）\)](.*)〜(.*)',line)
            month = zen2han(slotinfo.group(2))
            day = zen2han(slotinfo.group(3))
            start = zen2han(slotinfo.group(5))
            end = zen2han(slotinfo.group(6))
            slot["session_no"] = slotinfo.group(1)
            if curday == "" or curday != month+"/"+day:
                curday = month+"/"+day
                dayno = dayno + 1
            slot["date"] = curday
            slot["day"] = dayno
            slot["start"] = string.replace(start,u' ', u'')
            slot["end"] = string.replace(end,u' ',u'')
            slots[slotinfo.group(1)]=slot            
        except:
            print "Description format may be changed. Check it."
            raise
    return slots
    
def zen2han(strnumber):
    transmap = {u'１':"1",u'２':"2",u'３':"3",u'４':"4",u'５':"5",u'６':"6",u'７':"7",u'８':"8",u'９':"9",u'０':"0",u'：':":"}
    for zen in transmap.keys():
        strnumber = strnumber.replace(zen, transmap[zen])
    return strnumber
