#!/bin/python3

import codecs
import json
import toot
import sys

from json import JSONDecoder
from functools import partial

# parse le fichier telecharge; utilise pour creer la base sqlite3
def json_parse(fileobj, decoder=JSONDecoder(), buffersize=65536):
    buffer = ''
    for chunk in iter(partial(fileobj.read, buffersize), ''):
        buffer += chunk
        # il peut y avoir du garbage entre 2 objets json
        if buffer[0]!='{':
            deb=buffer.find('{')
            if deb>=0:
                print("remove",buffer[0:deb])
                fixit = buffer[deb:]
                buffer=fixit
            else:
                buffer=""
                print("remove",chunk)
                continue
        while buffer:
            try:
                result, index = decoder.raw_decode(buffer)
                yield result
                buffer = buffer[index:]
            except ValueError:
                # Not enough data to decode, read more
                break

# recupere la liste des instances des tooters depuis le fichier. to be deprecated infavor of sqlite3
def getInstances():
    import langdetect
    allinst = set()
    with codecs.open("../mastocorpus/https:mastodon.social","r","utf-8") as f:
        for o in json_parse(f):
            # process object
            if 'id' in o.keys():
                s=toot.getTootText(o)
                lg='unk'
                if True:
                    try:
                        lg=langdetect.detect(s)
                    except:
                        lg='err'
                url = o['account']['url']
                j=url.rfind('/')
                instance = url[:j]
                allinst.add(instance)
                #print(instance+" "+str(o['id'])+" "+lg+" "+s)
    return allinst

# search dans le fichier directement telecharge. Sera deprecateed en faveur de la base sqlite3
def look4chars(lang,chars):
    import langdetect
    nfound=0
    with codecs.open("../mastocorpus/https:mastodon.social","r","utf-8") as f:
        for o in json_parse(f):
            # process object
            if 'id' in o.keys():
                s=toot.getTootText(o)
                lg='unk'
                if True:
                    try:
                        lg=langdetect.detect(s)
                    except:
                        lg='err'
                if lg==lang:
                    nfound+=1
                    s=s.lower()
                    if chars in s:
                        print(str(nfound)+" "+s)

def appendDB():
    import sqlite3
    db=sqlite3.connect("../mastocorpus/https:mastodon.social.db")
    c=db.cursor()
    c.execute('''SELECT id FROM toots''')
    res=c.fetchall()
    ids=[r[0] for r in res]
    print(min(ids),max(ids))
    db.close()

def createDB():
    import sqlite3
    import langdetect
    db=sqlite3.connect("../mastocorpus/https:mastodon.social.db")
    db.execute('''CREATE TABLE toots (toot text, id int, lang text, user text)''')
    with codecs.open("../mastocorpus/https:mastodon.social","r","utf-8") as f:
        for o in json_parse(f):
            # process object
            if 'id' in o.keys():
                id = int(o['id'])
                s=toot.getTootText(o)
                lg='unk'
                if True:
                    try:
                        lg=langdetect.detect(s)
                    except:
                        lg='err'
                url = o['account']['url']
                # url = url.replace('@',"_at_")
                cmd = "INSERT INTO toots VALUES (?,'"+str(id)+"','"+lg+"','"+url+"')"
                print("command",s)
                db.execute(cmd,(s,))
    db.commit()
    db.close()

def queryInstance(inst):
    # interroge une nouvelle instance pour connaitre le nb de toots qu'elle contient
    import requests
    cmd = inst+'/api/v1/instance'
    response = requests.get(cmd)
    if response.status_code==404: return 0
    o = response.json()
    n=int(o['stats']['status_count'])
    return n

def complete():
    # TODO used only for completing a single shot; must be generalized
    import requests
    inst="https://mastodon.social"
    id0=2220895
    with codecs.open("../mastocorpus/https:mastodon.social","a","utf-8") as f:
        while id0>0:
            cmd = inst+'/api/v1/statuses/'+str(id0)
            response = requests.get(cmd)
            if response.status_code!=404:
                o = response.text
                f.write(o)
            id0-=1

def queryDB(term):
    # cherche dans la DB les occurrences de ce term
    import sqlite3
    db=sqlite3.connect("../mastocorpus/https:mastodon.social.db")
    c=db.cursor()
    c.execute("SELECT toot FROM toots WHERE toot LIKE ?",('%'+term+'%',))
    res=c.fetchall()
    ids=[r[0] for r in res]
    for s in ids: print(s)

    c.execute("SELECT count(*) FROM toots")
    nrows=c.fetchone()
    print("nrows "+str(nrows))
    db.close()

def getText():
    import sqlite3
    db=sqlite3.connect("../mastocorpus/https:mastodon.social.db")
    c=db.cursor()
    c.execute("SELECT toot FROM toots")
    res=c.fetchall()
    ids=[r[0] for r in res]
    return ids

def punct():
    import sqlite3
    db=sqlite3.connect("../mastocorpus/https:mastodon.social.db")
    c=db.cursor()
    c.execute("SELECT toot FROM toots WHERE lang='fr'")
    res=c.fetchall()
    ss=[r[0] for r in res]
    print("got %d toots" % len(ss))
    pcts='?!.;,'
    x,y=[],[]
    translator = str.maketrans(pcts+"'-"," "*len(pcts)+"  ")
    for s in ss:
        # il me faut un contexte gauche assez grand quand meme
        for i in range(5,len(s)):
            if s[i] in pcts:
                # je supprime les ponctuations et les majuscules du contexte pour qu'il ne prenne pas des indices typographiques, mais semantiques
                ctxt=s[0:i].translate(translator).lower()
                ctxt=" ".join(ctxt.split())
                x.append(ctxt)
                y.append(s[i])
    return x,y

if __name__ == "__main__":
    if sys.argv[1]=="-s":
        # search dans le fichier (deprecated)
        lang = sys.argv[2]
        mot  = sys.argv[3]
        look4chars(lang,mot)
    elif sys.argv[1]=="-db": appendDB()
    elif sys.argv[1]=="-pct": punct()
    elif sys.argv[1]=="-q": queryDB(sys.argv[2])
    elif sys.argv[1]=="-qi": queryInstance('https://mastodon.social')
    elif sys.argv[1]=="-complete": complete()

