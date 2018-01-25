#*-coding:utf-8-*
import loadnathmasto,os,dateutil.parser
#from prog import chem_dossier
chem_dossier="/home/nathan/mastocorpus/"

def calc_stats(inst):
    toot_id=[]
    toot_language=[]
    toot_account=[]
    toot_date=[]
    chem_inst=chem_dossier+inst
    a=open(chem_inst,"r")
    tab_acct=[]
    for i in loadnathmasto.json_parse(a):
        try:
            toot_language.append( i['language'] )
            toot_id.append( i['id'] )
            ac=i['account']['acct']
            acc=ac.split("@")
            accc=acc[0]
            toot_account.append( accc )
            dat=i['created_at']
            dat=dateutil.parser.parse(dat)
            toot_date.append( dat )
        except:
            #print("error : le programme n'arrive pas récuperer l'id et le language du toot, il est peut-etre abimé")
            error=True
    languages=[]
    nb_l=[]
    for l in toot_language:
         xx=0
         jj=0
         for ll in languages:
            if ll == l:
                nb_l[xx]+=1
                jj+=1
                break
         if jj == 0:
            languages.append( l )
            nb_l.append( 1 )
    lp=0
    for n in nb_l:
        if n > nb_l[lp]:
            lp = n
    nb_tot=0
    for n in nb_l:
        nb_tot+=n
    nb_fr=0
    for v in range(0,len(languages)-1):
        if languages[v] == "fr":
            nb_fr=nb_l[v]
            break
    account=[]
    ndfoalc=[]
    for h in list(set(toot_account)):
        account.append(h)
        ndfoalc.append(0)
        for g in toot_account:
            if h == g: ndfoalc[len(ndfoalc)-1]+=1
    
    cpa=0
    for x in range(0,len(ndfoalc)-1):
        if ndfoalc[x] > ndfoalc[cpa]:
            cpa = x

    ddate=[]
    nb_d=[]
    
    for t in list(set(toot_date)):
        ddate.append(t)
        nb_d.append(0)
        for g in toot_date:
            if t == g: nb_d[len(nb_d)-1]+=1

    dqaelpdt=0
    for x in range(0,len(nb_d)-1):
        if nb_d[x] > nb_d[dqaelpdt]:
            dqaelpdt = x
        
    
    try:
        ra="\nLa langue la plus utilisée dans l'instance "+str(inst)+" est ''"+str(languages[lp])+"'' avec "+str(nb_l[lp])+" utilisation, il y a "+str(nb_fr/nb_tot*100)+"% de utilisation de la langue francaise et le compte qui a publié le plus de toots dans cette instance est "+str(account[cpa])+" il y a eu le plus de toot le "+str(ddate[dqaelpdt])
        print(ra)
        return ra 
    except:
        return ("\n erreur inconnue dans l'instance",inst)
        print("error")

a=os.listdir(chem_dossier)
t=open("statistiques_instances.txt","w")
for b in a:
    try:
        p=calc_stats(b)
        t.write("\n"+str(p))
    except:
        print("erreur avec le fichier",b)
        
