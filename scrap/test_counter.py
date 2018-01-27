import random
from collections import Counter

a=["en","en","fr","po","ch","es","jp","tu"]
b=[]

for x in range(random.randint(300,1000)):
    b.append(random.choice(a))

coLang=Counter(b)
print(coLang)   
print(coLang.keys())
print(coLang.values())

for x in coLang.keys():
    y=coLang[x]
    print(x,y)












