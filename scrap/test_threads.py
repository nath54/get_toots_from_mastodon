import time
from threading import *


def main():
    while True:
        def a():
            for x in range(5):
                time.sleep(1)
            #run
        td=[]
        for x in range(10):
            print("add a thread")
            td.append( Thread(target=a ) )
            td[x].start()
        for t in td:
            t.join()
        td=[]
        print()
        print("td =",td)
        print()
        

main()
