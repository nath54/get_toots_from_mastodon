import os,loadnathmasto,codecs,time,requests

chem_dossier="/home/nathan/mastocorpus/"

#cette fonction calcule le temps restant d'un telechargement avec le nombre de toots restants
def calc_temps_restant(nb_tr):
    heures=nb_tr/3600
    hh=heures-int(heures)
    minutes=hh*60
    mm=minutes-int(minutes)
    secondes=mm*60
    return int(heures),int(minutes),int(secondes)

#regarde si de nouveaux toots ont étés rajoutés à l'instance et si oui, les télécharge.
def maj(inst):
    #verif_fichier(inst)
    print("regarde si des toots ont étés ajoutés a l'instance "+inst)
    hinst="https://"+inst
    chem_inst=chem_dossier+inst
    a=open(chem_inst,"r")
    n=loadnathmasto.queryInstance(hinst)
    for i in loadnathmasto.json_parse(a):
        try: oo=int(i["id"])
        except: print("error")
        break
    try: print(oo)
    except:
        print("le nombre de toots ne peut pas etre trouvé")
        oo=int(n)
    if int(oo) != int(n):
        print("le fichier "+inst+" a des toots qui ont étés ajoutés")
        print("mise à jour du fichier")
        id0=int(n)
        fich=chem_dossier+inst
        with open(fich,"r") as jkl: old_content=jkl.read()
        new_content=""
        
        print("nombre total de toots ",id0,"\nnombre de toots du fichier",oo)
        while id0 > oo:
            time.sleep(0.1)
            cmd = hinst+'/api/v1/statuses/'+str(id0)
            response = requests.get(cmd)
            if response.status_code!=404:
                o = response.text
                new_content+=o
            else:
                o = '{"id":"'+str(id0)+'"}'
                new_content+=o
            id0-=1
            h,m,s=calc_temps_restant(int(id0-oo))
            print("toots restants sur l'instance",inst," ="+str(int(id0)-int(oo)),"    temps restant estimé =",h,"heures",m,"minutes",s,"secondes")
            with codecs.open(fich,"w","utf-8") as f: f.write(new_content+old_content)
    else: print("l'instance",inst,"est à jour")
    #analyse_and_add_instance(inst)

dd=os.listdir(chem_dossier)
for d in dd: maj(d)
print("La mise a jour est finie :)")
