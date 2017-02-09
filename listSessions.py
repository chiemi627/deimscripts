#coding=utf-8

import deim

# フラグ：座長とコメンテータが決まってる時は1
reviewer_assigned = 0
# コメンテータの数
nofreviewers = 2

# セッション情報を生成する（PosTom用)
def generateSessionInfo(room,sessionID,sinfo,reviewer):
    session = [room,sessionID,sinfo["title"]]
    session.extend([str(slots[sessionID]["day"]),slots[sessionID]["start"],slots[sessionID]["end"]])
    if reviewer_assigned == 1:
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
    else:
        for i in range(1, nofreviewers+1):
            session.extend(["TBD","TBD"])
    return session

# main procedure
if __name__ == '__main__':
    data_program = 'http://db-event.jpn.org/deim2017/data_program.js'
    data_reviewer = 'http://db-event.jpn.org/deim2017/data_reviewers.js'

    program = deim.loadProgramInfo(data_program,'var sessions =')
    reviewer = deim.loadProgramInfo(data_reviewer,'var reviewers =')
    slots = deim.getSlotInfo(program)

    rooms = sorted(program["sessions"],key=lambda x:x[0])

    for room in rooms:
        sessions = sorted(program["sessions"][room],key=lambda x:x[0])
        for sessionID in sessions:
            session = generateSessionInfo(room,sessionID,program["sessions"][room][sessionID],reviewer)
            print ",".join(session).encode('utf-8')
