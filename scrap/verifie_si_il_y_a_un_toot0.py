import loadnathmasto
#from prog import chem_dossier
chem_dossier="/home/nathan/mastocorpus"

def verifie_toot0(inst):
    print("Vérifie le téléchargement de l'instance "+inst)
    hinst="https://"+inst
    chem_inst=chem_dossier+inst
    a=open(chem_inst,"r")
    tab_acct=[]
    for i in loadnathmasto.json_parse(a):
        try:
            o=i["id"]
            o=int(o)
        except:
            break
    print("o =",o)
    if o != 0:
        print("il n'y a pas de toot 0 dans l'instance",inst)

verifie_toot0("instance.business")
