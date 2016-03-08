#coding=utf-8

import svgwrite,urllib2,json,sys,re

posmappURL = sys.argv[1]

if len(sys.argv) == 2:
    posmappURL = sys.argv[1]
    xoffset = 0
    yoffset = 0
elif len(sys.argv) == 4:
    posmappURL = sys.argv[1]
    xoffset = int(sys.argv[2])
    yoffset = int(sys.argv[3])
else:
    print 'Usage: python generatePosterMap.py <URL> <xoffset> <yoffset>'
    quit()

urlparts = re.match('(.*)PosMapps/index/(.*)',posmappURL)
jsonURL = urlparts.group(1)+"json/"+urlparts.group(2)+".json"

req = urllib2.Request(jsonURL)
response = urllib2.urlopen(req)
data = response.read()
mapdata = json.loads(data,"utf-8")

positions = {}
for box in mapdata["position"]:
    positions[box["id"]]={"x":box["x"],"y":box["y"],"width":box["width"],"height":box["height"]}

posters = {}
for poster in mapdata["poster"]:
    if poster["date"] not in posters:
        posters[poster["date"]] = []
    position = positions[poster["posterid"]]
    p = {"x":position["x"],"y":position["y"],"width":position["width"],"height":position["height"]}
    p["posterid"] = poster["posterid"]
    p["presenid"] = poster["presenid"]
    posters[poster["date"]].append(p)

for day in posters:
    dwg = svgwrite.Drawing('day'+day+'.svg',size=(u'800',u'1000'),profile="tiny")
    dwg.add(dwg.image(urlparts.group(1)+"/img/bg/"+urlparts.group(2)+"_"+day+".png",insert=(0,0),size=(u'100%',u'100%')))
    for poster in posters[day]:
        dwg.add(dwg.rect((int(poster["x"])+xoffset,int(poster["y"])+yoffset),(poster["width"],poster["height"]),stroke='black', fill='white',stroke_width=1))
        dwg.add(dwg.text(poster["presenid"],insert=(int(poster["x"])+xoffset,int(poster["y"])+yoffset+20)))
    dwg.save()
    sys.stderr.write("File day"+day+".svg has been generated.\n")