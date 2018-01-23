#!/usr/bin/python3

import codecs
import json
import re

def tootIDprinter(tt):
    if 'id' in tt: print(tt['id'])

def getTootText(tt):
    s=""
    if 'content' in tt:
        s = tt['content']
        s = s.replace('<p>',' ').replace('</p>',' ').replace('<br>',' ')
        s = re.sub('<span[^>]*>','',s)
        s = s.replace("</span>","")
        s = re.sub('<a href=[^>]*>',' URL ',s)
        s = s.replace('</a>',' ')
        s = s.replace(u'＃','#')
        s = s.replace('&apos;',"'")
        s = s.replace('@ ','@')
        # les URL dans les hashtags ne sont pas vraiment des URL...
        s = s.replace('#  URL ','#')
        s = s.replace('# ','#')
        s = re.sub('https://[^ ]*'," ",s)
        s = re.sub('http://[^ ]*'," ",s)
        s = re.sub('  +',' ',s)
        s = s.strip()
    return s

def tootParent(tt):
    tid="-1"
    if 'id' in tt: tid = tt['id']
    if 'in_reply_to_id' in tt:
        pere = tt['in_reply_to_id']
        print(str(tid)+" <-- "+str(pere))


def tootTextPrinter(tt):
    s=getTootText(tt)
    print(s)

def tootPrinter(tt):
    print(tt)

def loadFile(handler,jsonfile):
    with codecs.open(jsonfile,"r","utf-8") as f:
        for l in f:
            if len(l)>0 and l[0]=='{':
                toot = json.loads(l)
                handler(toot)


