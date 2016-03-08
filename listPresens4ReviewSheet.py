#coding:utf-8

import deim,sys

def generatePresentationInfo(room,sessionID,paperID,presenOrder,papers,day):

    position = {u"B":u"学部生",
                u"M":u"博士前期課程（修士）",
                u"D":u"博士後期課程",
                u"D3":u"PhD取得後3年以内の社会人",
                u"W":u"それ以外の社会人",
                u"AD":u"社会人博士後期課程"}

    if paperID in papers["papers"]:
        presentation = papers["papers"][paperID]
        presen = [room+sessionID+"-"+str(presenOrder),room+sessionID,'"'+presentation["title"]+'"']
        authors = presentation["authors"]
        presen.extend([authors[0]["name_last"]+" "+authors[0]["name_first"],authors[0]["organization"],
                       position[authors[0]["position_title"]],day])
        for author in authors:
            presen.append(author["name_last"]+" "+author["name_first"]+"("+author["organization"]+")")
        return presen
    else:
        raise

# main procedure
if __name__ == '__main__':
    data_papers = 'http://cms.deim-forum.org/deim2016/list/papers.php?decode&pretty&jsonp=callback'
    papers = deim.getPaperInfo(data_papers)

    data_program = 'http://db-event.jpn.org/deim2016/data_program.js'
    program = deim.loadProgramInfo(data_program,'var sessions =')
    slots = deim.getSlotInfo(program)

    # list up oral presentations
    for room in program["oral"]:
        for sessionID in program["oral"][room]:
            i = 1
            for paperID in program["oral"][room][sessionID]:
                try:
                    print ','.join(generatePresentationInfo(room,sessionID,paperID, i, papers,slots[sessionID]["date"])).encode('utf-8')
                    i = i + 1
                except:
                    sys.stderr.write('ERROR: the paper (ID:'+paperID+") is not found. \n")
    # list up poster presentations
    for sessionID in program["interactive"]["P"]:
        i = 1
        for paperID in program["interactive"]["P"][sessionID]:
                try:
                    print ','.join(generatePresentationInfo("P",sessionID,paperID, i, papers, slots[sessionID]["date"])).encode('utf-8')
                    i = i + 1
                except:
                    sys.stderr.write('ERROR: the paper (ID:'+paperID+") is not found. \n")
