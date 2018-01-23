 #*-coding:utf-8-*
import loadnathmasto,os,time,codecs,requests,threading,toot
from threading import *

dejas_t=["mastodon.social"]
instance=[]

#fonction qui sauvegarde la liste des instances dans un fichier listeinstances.txt
def save_liste_instance():
    txti=""
    for k in instance:
        txti+=k+" "
    li=open("listeinstance.txt","w")
    li.write(txti)


#fonction qui récupere la liste des instances depuis le fichier listeinstance.txt
def get_liste_instance():
    try:
        f= open("listeinstance.txt","r")
        f=f.read()
        fd=f.split()
        for fg in fd:
            instance.append(fg)
        print("\n\n\n\n\n\n\n\n\n\n\n\n\nLA LISTE DES INSTANCES \n\n\n\n\n",instance)
    except:
        print("le fichier listeinstances.txt n'a pas ete trouve")

#cette fonction calcule le temps restant d'un telechargement avec le nombre de toots restants
def calc_temps_restant(nb_tr):
    heures=nb_tr/3600
    hh=heures-int(heures)
    minutes=hh*60
    mm=minutes-int(minutes)
    secondes=mm*60
    return int(heures),int(minutes),int(secondes)

#analyse l'instance qu'on lui donne, ajoute a la liste des instances de nouvelles instances
def analyse_and_add_instance(inst):
    global instance
    chem_inst="/home/nathan/mastocorpus/"+inst
    a=open(chem_inst,"r")
    tab_acct=[]
    for i in loadnathmasto.json_parse(a):
        try:
            g=i['id']
            gg=i['account']['acct']
            #print("id = ",g)
            #print("acct = ",gg)
            tab_acct.append(gg)
        except:
            print("error")
    #print("tab =",tab_acct)
    for t in tab_acct:
        tt=t.split("@")
        #print(tt)
        if len(tt) == 2:
            instance.append(tt[1])
        else:
            print(t,": Ne contient pas le nom de l'instance")  #les toots qui sont téléchargés et qui sont sur la meme instance qui est en train de se télécharger ne contiennent pas le nom de l'instance dans leur ['account]['acct']
    print()
    #print(instance)

#cette fonction verifie si le dernier toot a été coupé ou non en comparant la fin du dernier toot du fichier a la fin du dernier toot non coupé 
def verif_fichier(inst):
    a=open("/home/nathan/mastocorpus/"+inst,"r")
    a=a.read()
    b=a[len(a)-13:len(a)]
    print(b)
    if b == ',"emojis":[]}':
        print("normalement, le dernier toot n'a pas été coupé lorsque le téléchargement a été interrompu")
    else:
        b=a[len(a)-2:len(a)]
        print(b)
        if b == "]}":
            print("normalement, mais je suis moin sûr, le dernier toot n'a pas été coupé lorsque le téléchargement a été interrompu")
        else:
            b=a[len(a)-1]
            print(b)
            if b == "}":
                print("J'ai plus de doutes, mais normalement le dernier toot n'a pas été coupé lorsque le téléchargement a été interrompu")
            else:
                print("J'ai bien peur que le toot ai été coupé lors de l'arrêt téléchargement")
                exit()

#fonction qui verifie si une instance a bien été téléchargée et qui complete le fichier si mal telecharge
def verifie_telechargement(inst):
    verif_fichier(inst)
    print("Vérifie le téléchargement de l'instance "+inst)
    hinst="https://"+inst
    chem_inst="/home/nathan/mastocorpus/"+inst
    a=open(chem_inst,"r")
    tab_acct=[]
    for i in loadnathmasto.json_parse(a):
        try:
            o=i["id"]
            o=int(o)
        except:
            break
    if o > 0:
        print("le fichier "+inst+" a mal été téléchargé")
        print("reprise du téléchargement du fichier")
        id0=o-1
        fich="/home/nathan/mastocorpus/"+inst
        with codecs.open(fich,"a","utf-8") as f: 
            while id0>-1:
                time.sleep(0.1)
                cmd = hinst+'/api/v1/statuses/'+str(id0)
                response = requests.get(cmd)
                if response.status_code!=404:
                    o = response.text
                    f.write(o)
                else:
                    o = '{"id":"'+str(id0)+'"}'
                    f.write(o)
                id0-=1
                h,m,s=calc_temps_restant(int(id0))
                print("toots restants ="+str(id0),"    temps restant =",h,"heures",m,"minutes",s,"secondes")
    analyse_and_add_instance(inst)
    







#verifie si le fichier existe déjà, si "oui" retourné, le fichier n'existe pas
def verif_fichier(a):
    try:
        b=open(a,"r")
        return "oui"
    except: return "non"

#vérifie si le fichier est dans la liste des instances déjà téléchargées, si "oui" retourné, l'instance ne se trouve pas dans la liste des instances déjà téléchargées
def verif_tel(a):
    for x in dejas_t:
        if x == a:
            return "oui"
    return "non"

#telecharge l'instance qu'on lui donne
def download_instance(inst):
    print("TELECHAGEMENT DU FICHIER : "+inst)
    inst="https://"+inst
    n=loadnathmasto.queryInstance(inst)
    id0=n
    fich="/home/nathan/mastocorpus/"+inst[8:]
    with codecs.open(fich,"a","utf-8") as f: 
        while id0>-1:
            cmd = inst+'/api/v1/statuses/'+str(id0)
            response = requests.get(cmd)
            if response.status_code!=404:
                o = response.text
                f.write(o)
            else:
                    o = '{"id":"'+str(id0)+'"}'
                    f.write(o)
            id0-=1
            h,m,s=calc_temps_restant(int(id0))
            print("toots restants ="+str(id0),"    temps restant =",h,"heures",m,"minutes",s,"secondes")
            #input()
            time.sleep(0.1)



#fonction pour lancer les fonctions download_instance et analyse_and_add_instance ensembles
def download_analyse(inst):
    v=verif_tel(inst)
    if v == "oui":
        download_instance(inst)
        analyse_and_add_instance(inst)
    else: print("il a déjà été téléchargé")

#fonction principale
def main():
    dd=os.listdir("/home/nathan/mastocorpus/")
    for d in dd: dejas_t.append(d)
    dd=os.listdir("/home/nathan/mastocorpus/")
    for d in dd: verifie_telechargement(d)
    get_liste_instance()
    print(instance)
    while len(instance) != 0 :
        x=0
        #try: 
        din=instance[x]
        print("DIN =",din)
        if len(din) >= 5:
            del(instance[x])
            dejas_t.append(din)
            download_analyse(din)
        else:
            print("vide")
            break
        #except:
        #    print("vide")
        #    break
        

main()

save_liste_instance()


