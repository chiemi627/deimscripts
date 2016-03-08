#coding:utf-8

import csv,sys

# read presentations
def readPresentations(filename):
    presenList = {}
    with open(filename,'rb') as csvfile:
        reader = csv.reader(csvfile,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            presen = {}
            presen["presenID"]=row[0]
            presen["title"]=row[2]
            presen["author"]=row[3]
            presen["organization"]=row[4]
            presenList[row[0]]=presen
    csvfile.close()
    return presenList

# read participants
def readParticipants(filename):
    partList = {}
    with open(filename,'rb') as csvfile:
        reader = csv.reader(csvfile,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            person = {}
            person["id"]=row[0]
            person["name"]=row[1]+row[2]
            person["organization"]=row[3]
            partList[row[0]] = person
    csvfile.close()
    return partList

# read votes
def readVotes(filename,presenList,partList):
    votes = {}
    with open(filename,'rb') as csvfile:
        reader = csv.reader(csvfile,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            if row[0] not in partList:
                sys.stderr.write(row[0]+" is not in participant list.\n")
                continue
            if row[2] not in presenList:
                sys.stderr.write(row[2]+" is not in presen list.\n")
                continue
            if row[2] not in votes:
                votes[row[2]] = {}
                votes[row[2]]["id"] = row[2]
                votes[row[2]]["voters"]=[row[0]]
                votes[row[2]]["count"]=0
                votes[row[2]]["chair_count"]=0
            else:
                votes[row[2]]["voters"].append(row[0])
            if row[1] == "1":
                votes[row[2]]["count"] += 1
            else:
                votes[row[2]]["chair_count"] += 1
    csvfile.close()
    return votes

# main procedure
if __name__ == '__main__':
    presenList = readPresentations("presen.csv")
    partList = readParticipants("participants.csv")
    votes = readVotes("votes.csv",presenList,partList)
    for v in votes:
        presen =  presenList[v]
        result = [presen["presenID"],presen["author"],presen["organization"],presen["title"]]
        result.extend([str(votes[v]["chair_count"]),str(votes[v]["count"])])
        for p in votes[v]["voters"]:
            result.append(partList[p]["name"]+"("+partList[p]["organization"]+")")

        print ",".join(result)