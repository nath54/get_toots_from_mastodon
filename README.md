
# Que fait ce programme ?

Ce programme télécharge des toots sur des instances différentes, avec ses toots là, il récupère de nouvelles instances puis télécharge les nouveaux toots de ses instances et ainsi de suite...
Il continue aussi les téléchargements des instances qui ont étés mal téléchargées.

Le programme calc_stats_ints.py crée une page_web (PAGE.html) avec des statistiques des instances déjà téléchargées.

# Comment executer ce programme ?

Pour lancer le programme, c'est très simple, il faut aller dans le dossier contenant les programmes, ils sont tous dans le dossier scrap, avec un terminal puis lancer la commande que vous trouverez ci-dessous. Il faut utiliser python3 car avec python2, il peut y avoir des problèmes d'encodage, c'est le programme prog.py qu'il faut lancer car c'est le programme principal 

```
python3 prog.py
```

IMPORTANT : avant de lancer le programme, il faut que vous changiez la variable chem_dossier qui se trouve au début du programme prog.py avec le chemin du dossier où vous voudriez télécharger toutes les instances. Si vous n'avez pas changé cette variable, le programme plantera. Il faut créer le dossier car si vous avez mis dans la variable un dossier qui n'existe pas, il plantera car le programme ne crée pas le dossier.

# Notes sur le programme

Vous pouvez l'arrêter en appuyant simultanément sur les touches Ctrl + c ou alors le programme finira de s'exécuter tout seul quand il aura fini de télécharger tous les toots de toutes les instances qu'il trouvera.
Si le programme était en train de télécharger lorsque vous l'avez arrêté, la prochaine fois que vous le relancerez, normalement, il va regarder toutes les instances qu'il a téléchargées et s'il y en a une incomplete, il va finir le téléchargement.

Toutefois, il se peut qu'il y ait une erreur : si le programme a mal écrit le dernier toot dans le fichier lorsque vous l'avez interrompu, il est censé s'arrêter automatiquement lors de la vérification du téléchargement, mais s'il ne s'est pas arrêté automatiquement et qu'il continue le téléchargement, le fichier complet de l'instance aura un problème. Si jamais c'est le cas, la meilleure solution reste de supprimer le fichier portant le nom de l'instance.

Si jamais il y a des bugs, veuillez m'en informer, merci.
