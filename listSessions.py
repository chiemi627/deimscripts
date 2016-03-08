#coding=utf-8

import deim

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

    program = deim.loadProgramInfo(data_program,'var sessions =')
    reviewer = deim.loadProgramInfo(data_reviewer,'var reviewers =')
    slots = deim.getSlotInfo(program)

    for room in program["sessions"]:
        for sessionID in program["sessions"][room]:
            session = generateSessionInfo(room,sessionID,program["sessions"][room][sessionID],reviewer)
            print ",".join(session).encode('utf-8')