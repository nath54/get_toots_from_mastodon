import loadnathmasto,os
#from prog import chem_dossier
chem_dossier="/home/nathan/mastocorpus"

def calc_stats(inst):
    toot_id=[]
    toot_language=[]
    chem_inst=chem_dossier+inst
    a=open(chem_inst,"r")
    tab_acct=[]
    for i in loadnathmasto.json_parse(a):
        try:
            toot_language.append( i['language'] )
            toot_id.append( i['id'] )
        except:
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
    try: print("La langue la plus utilisée dans l'instance",inst,"est ''",languages[lp],"'' avec",nb_l[lp],"utilisation") 
    except: print("error")

a=os.listdir(chem_dossier)
for b in a:
    calc_stats(b)

