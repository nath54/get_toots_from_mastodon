import loadnathmasto
#from prog import chem_dossier
chem_dossier="/home/nathan/mastocorpus"

def verif_doubles_toots(inst):
    ids=[]
    chem_inst=chem_dossier+inst
    a=open(chem_inst,"r")
    tab_acct=[]
    for i in loadnathmasto.json_parse(a):
        try:
            g=i['id']
            ids.append(g)
        except:
            print("error")
    print("len(ids) =",len(ids))
    print("len(set(ids)) =",len(set(ids)))
    if len(ids) == len(set(ids)):
        print("Il n'y a pas de doublons")
    else:
        print("il y a peut-etre des doublons")

verif_doubles_toots("instance.business")
