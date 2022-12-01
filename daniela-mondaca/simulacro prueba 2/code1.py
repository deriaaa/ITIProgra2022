#data format = y/m/d
#arrays = 6,6. 100,100.
#si una ubicación fuera a tener más de 100 items, se despachan inmediatamente 100 items, se conserva el excedente.



#import numpy
import numpy as np

#add functions
def addifnt(list, elm):
    if not elm in list:
        list.append(elm)
    return list.index(elm)

def add(list, elm):
    list.append(elm)
    return list.index(elm)

#zone with merged sectlor to zone and sector
def zAs(nStore):
    spls=nStore.split('-')
    zone=spls[0]; sector=spls[1]
    return(zone, sector)
        
        
#read from text and convert to list format    
def ship(): 
    date=[]; zone=[]; sector=[]; amt=[]
    arch=open('recibidos.txt', 'r')
    rline=arch.readline().strip()

    while rline != '':
        spl=rline.split(';')
        when=spl[0]; cInStore=spl[1]; ammt=int(spl[2])
        zoneR, sectorR=zAs(cInStore)
        add(date,when); add(zone,zoneR); add(sector,sectorR); add(amt,ammt)
        rline=arch.readline().strip()
    return(date,zone,sector,amt)



datext,zonext,sectext,amtext=ship(); inStore=np.zeros([6,6]); sentt=np.zeros([6,6])




#sent packages to secondary array
def snt(Wz,Ws,AWZ):
    sentt[Wz][Ws]=sentt[Wz][Ws]+100
    print("Se han enviado 100 paquetes a "+str(AWZ)+" - "+str(Ws))

#translate letter zone to numerical index
def trZ(zonetr,i):
    ztN=["A","B","C","D","E","F"]
    convt=0
    for c in range(0,5):        
        if ztN[c]==zonetr[i]:
            convt=c
    return(convt)
                
#translate to main storage array

def trsmtx(zone,sector,amt,date):
    for i in range(len(zone)):
        print(i)
        z=trZ(zone,i); s=int(sector[i])
        inStore[z][s]=inStore[z][s]+amt[i]
        if inStore[z][s]>=100:
            snt(z,s,zone)
            inStore[z][s]=inStore[z][s]-100
            print("100 paquetes fueron despachados el "+str(date)+" hacia "+str(zone)+" - "+str(s))


trsmtx(zonext,sectext,amtext,datext)
