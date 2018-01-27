#*-coding:utf-8-*
import loadnathmasto,os,dateutil.parser,operator,collections
from collections import *
from decimal import *
chem_dossier="mastocorpus/"

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
            ac=i['account']['acct']
            # si ac contient un @, alors le user n'appartient pas a cette instance: il ne faut donc pas le compter dans les stats de l'instance
            # il ne faut comptabiliser QUE les toots des users sans @
            if "@" not in ac:
                #print(ac)
                accc=ac
                toot_account.append( accc )
                toot_language.append( i['language'] )
                dat=i['created_at']
                dat=dateutil.parser.parse(dat)
                toot_date.append( dat.year*100+dat.month )
                toot_id.append( i['id'] )
        except:
            #print("error : le programme n'arrive pas récuperer la date et le language du toot, il est peut-etre abimé")
            error=True
    assert len(toot_language)==len(toot_date)
    assert len(toot_language)==len(toot_account)
    assert len(toot_language)==len(toot_id)

    # Afficher le pourcentage des 5 langues les plus utilisees dans l'instance    
    coLang = Counter(toot_language)
    
    tot_lang=0
    for t in coLang.values(): tot_lang+=t
    
    langs=coLang.most_common(5)
    
    langg = []
    for n in langs:
        langg.append( [n[0],n[1]] )

    for l in langg:
        pc=int(l[1])/tot_lang*100
        l.append(pc)        
    lpu=0
    
    
    
    # TODO: afficher nb de toots dans l'instance pour les 6 derniers mois (en texte)
    
    
    
    coDate = Counter(toot_date)
    dates = OrderedDict(sorted(coDate.items()))
    
    ddates=[]    
    for a in dates.keys():
        ddates.append([a,dates[a]])   
    
    if len(ddates) < 6:
        ddates=ddates
    else:
        dddates=[]
        for x in range(6):
            dddates.append(ddates[x])
        ddates=dddates
    
    
    i="\nINSTANCE : "+inst+" / "
    m="\nles 6 mois (ou moin) les plus récents = "
    for mm in ddates:
        m+="le "+str(mm[0])+" il y a eu "+str(mm[1])+" toots  ,"
    m=m[0:len(m)-1]+" / " 
    
    l="\nles 5 langues les plus parlées = "
    for ll in langg:
        if ll[0] == None: ll[0] = "?"
        lll=Decimal(ll[2])
        l+="le "+ll[0]+" avec "+str(ll[1])+" utilisations soit "+str(lll.quantize(Decimal('.01'), rounding=ROUND_HALF_UP))+"%    ,"
    l=l[0:len(l)-1]
    #print(i)
    #print(m)
    #print(l)
    
    try:
        ra=i+m+l
        #print(ra)
        if len(ddates) > 0 and ra != None: return ra 
    except:
        error=True
        #return ("\n erreur inconnue dans l'instance",inst)
        #print("error")

def cree_page_html():
    texte=""
    a=os.listdir(chem_dossier)
    for b in a:
        p=calc_stats(b)
        if p != None: texte+="<li>"+p+"</li>"
    debut_page="""
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <link rel="stylesheet" href="style.css" />
        <title>Statistiques des instances</title>
    </head>
    <body>
        <h1>Statistiques des instances</h1>
        <nav>
            <ul>"""
    fin_page="""
            </ul>
        </nav>
    </body>
</html>
    
""" 
    milieu_page="\n"+texte
    #print(debut_page+milieu_page+fin_page)
    fichier=open("PAGE.html","w")
    fichier.write(debut_page+milieu_page+fin_page)

def main():
    a=os.listdir(chem_dossier)
    #a=["instance.business"]
    t=open("statistiques_instances.txt","w")
    for b in a:
        try:
            p=calc_stats(b)
            if p != "None" : t.write("\n"+str(p))
        except:
            print("erreur avec le fichier",b)
    cree_page_html()

main()

