#data format = y/m/d
#arrays = 6,6. 100,100.
#si una ubicación fuera a tener más de 100 items, se despachan inmediatamente 100 items, se conserva el excedente.

################ initial data reading (textfile->list)##############

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
    zone=spls[0]; sector=int(spls[1]); sector-=1
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




########################################### secondary reading (list->array) and embedded processing (requests 1 and 2)


#sent packages to secondary array (part of req 2)
def snt(Wz,Ws,textZ,i):
    sentt[Wz][Ws]=sentt[Wz][Ws]+1
    print("Se han despachado 100 paquetes a "+str(textZ[i])+" - "+str(Ws+1),'\n')

#total sents calculation (part of req 2)
def totalsents(totalsents):
    dtotal=totalsents
    totalN=int()
    for z in range(6):
        for s in range(6):
            if dtotal[z][s]!=0:
                totalN=totalN+dtotal[z][s]
    return(totalN)

def cost(shipped):
    bySectorP=[125,325,198,635,312,185]; totalC=int()
    for s in range(6):
        temP=0
        for z in range(6):
            if shipped[z][s]!=0:
                temP=temP+shipped[z][s]*bySectorP[s]
        totalC=totalC+temP
    return(totalC)



#translate letter zone to numerical index (secondary processing list to array)
def trZ(zonetr,i):
    ztN=["A","B","C","D","E","F"]
    convt=int()
    for c in range(0,6):        
        if ztN[c]==zonetr[i]:
            convt=c
    return(convt)
                
#translate to main storage array (secondary processing list to array - main code, embedded processing (req 1 -determines when and where a shipment takes place- and 
# req 2 -determines how many shipments have been made and to where, shows said info via array))

def trsmtx(zone,sector,amt,date):
    for i in range(len(date)):
        z=trZ(zone,i); s=int(sector[i])
        inStore[z][s]=inStore[z][s]+amt[i]
        if inStore[z][s]>=100:
            print("100 paquetes fueron despachados el "+str(date[i])+" hacia "+str(zone[i])+" - "+str(s+1))
            snt(z,s,zone,i)
            inStore[z][s]=inStore[z][s]-100
    
    #total sents (minimal processing and output of req 2)
    totalN=int(totalsents(sentt)); totalN=totalN*100
    print("Se envio un total de "+str(totalN)+" paquetes durante este mes",'\n')
    print("Los paquetes fueron despachados a las direcciones que se muestran a continuación",'\n')
    print(sentt,'\n')

 
trsmtx(zonext,sectext,amtext,datext)
totalcost=cost(sentt)
print("El coste total de todos los despachos es: "+str(totalcost),'\n')


def indextozone_indextosect(zone_in,sect_in):
    toZone=["A","B","C","D","E","F"]; zone=str(); zone_in=zone_in+1
    sect=str(sect_in)
    for i in range(6):
        if i==zone_in:
            zone=toZone[i]
    index=str()
    index=str(zone+" - "+sect)
    return(index)
        
    


def determineBig(pendingZ,pendingS,item):
    tocomp=item[pendingZ][pendingS]; current=0; index=str()
    for col in range(6):
        for fil in range(6):
            current=item[col][fil]
            if current>tocomp:
                tocomp=current
                index=indextozone_indextosect(fil,col)
                
    return(tocomp,index)



def pending(items):
    for s in range(6):
        for z in range(6):
            if items[z][s]!=0:
                outBIG=determineBig(z,s,items)
    return(outBIG)

mostPendingItems, index=pending(inStore)
print("Las ubicaciones con la mayor cantidad de items pendientes son:"+'\n')
print(index+" con "+str(mostPendingItems),'\n'); 

def pendientes_despacho():
    


