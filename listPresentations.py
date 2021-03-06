#coding:utf-8

import deim,sys

def generatePresentationInfo(room,sessionID,paperID,presenOrder,papers,slots):
    if paperID in papers["papers"]:
        presentation = papers["papers"][paperID]
        abstract = presentation["abstract"].replace("\r\n".decode('utf-8'),'').replace("\n".decode('utf-8'),'').replace("\"".decode('utf-8'),"'")
        title = presentation["title"].replace("\"".decode('utf-8'),"'")
        presen = [room,sessionID,str(presenOrder),str(slots[sessionID]["day"]),'"'+title+'"','"'+abstract+'"','"'+",".join(presentation["keywords"])+'"']
        names = []; affrs = []
        for author in presentation["authors"]:
            names.append(author["name_last"]+" "+author["name_first"])
            if author["organization_abbr"]:
                affrs.append(author["organization_abbr"].replace(",".decode('utf-8'),"/"))
            else:
                affrs.append(author["organization"].replace(",".decode('utf-8'),"/"))
        presen.extend(['"'+",".join(names)+'"','"'+",".join(affrs)+'"'])
        return presen
    else:
        raise

# main procedure
if __name__ == '__main__':
    data_papers = 'http://cms.deim-forum.org/deim2017/list/papers.php?decode&pretty&jsonp=callback'
    papers = deim.getPaperInfo(data_papers)

    data_program = 'http://db-event.jpn.org/deim2017/data_program.js'
    program = deim.loadProgramInfo(data_program,'var sessions =')
    slots = deim.getSlotInfo(program)

    # list up oral presentations
    for room in program["oral"]:
        for sessionID in program["oral"][room]:
            i = 1
            for paperID in program["oral"][room][sessionID]:
                try:
                    print ','.join(generatePresentationInfo(room,sessionID,paperID,i,papers,slots)).encode('utf-8')
                    i = i + 1
                except:
                    sys.stderr.write('ERROR: the paper (ID:'+paperID+") is not found. \n")
    # list up poster presentations
    for sessionID in program["interactive"]["P"]:
        i = 1
        for paperID in program["interactive"]["P"][sessionID]:
                try:
                    print ','.join(generatePresentationInfo("P",sessionID,paperID,i,papers,slots)).encode('utf-8')
                    i = i + 1
                except:
                    sys.stderr.write('ERROR: the paper (ID:'+paperID+") is not found. \n")
