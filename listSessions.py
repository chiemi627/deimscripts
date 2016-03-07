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

# セッション情報を生成する（PosTom用)
def generateSessionInfo(room,sessionID,sinfo,reviewer):
    session = [room,sessionID,sinfo["title"]]
    session.extend([slots[sessionID]["start"],slots[sessionID]["end"]])
    chair = reviewer["reviewers"][sinfo["chair"]]
    session.append(chair["name_last"]+" "+chair["name_first"])
    if chair["organization_abbr"] :
        session.append(chair["organization_abbr"])
    else:
        session.append(chair["organization"])
    comms = [reviewer["reviewers"][sinfo["comm1"]],reviewer["reviewers"][sinfo["comm2"]]]
    names = []; affrs = []
    for comm in comms:
        names.append(comm["name_last"]+" "+comm["name_first"])
        if(comm["organization_abbr"]):
            affrs.append(comm["organization_abbr"])
        else:
            affrs.append(comm["organization"])
    session.extend(['"'+",".join(names)+'"','"'+",".join(affrs)+'"'])
    return session

# main procedure
if __name__ == '__main__':
    data_program = 'http://db-event.jpn.org/deim2016/data_program.js'
    data_reviewer = 'http://db-event.jpn.org/deim2016/data_reviewers.js'

    program = loadProgramInfo(data_program,'var sessions =')
    reviewer = loadProgramInfo(data_reviewer,'var reviewers =')
    slots = getSlotInfo(program)

    for room in program["sessions"]:
        for sessionID in program["sessions"][room]:
            session = generateSessionInfo(room,sessionID,program["sessions"][room][sessionID],reviewer)
            print ",".join(session).encode('utf-8')