from sklearn import datasets
import numpy as np
import random, math

def generate():
    """
    Inisialisasi populasi
    """
    for i in range(10):
        for j in range(12):
            individu[i][j] = random.uniform(0,5)

def fitness(anak):
    kluster1 = []
    kluster2 = []
    kluster3 = []
    jumlah_twcv = [0,0,0]
    for i in range(150):
        """
        Menghitung jarak tiap data ke kluster
        """
        jarak = [0,0,0]
        jarak[0] = math.sqrt((anak[0]-iris[i][0])**2 + (anak[1]-iris[i][1])**2 + (anak[2]-iris[i][2])**2 + (anak[3]-iris[i][2])**2)
        jarak[1] = math.sqrt((anak[4]-iris[i][0])**2 + (anak[5]-iris[i][1])**2 + (anak[6]-iris[i][2])**2 + (anak[7]-iris[i][2])**2)
        jarak[2] = math.sqrt((anak[8]-iris[i][0])**2 + (anak[9]-iris[i][1])**2 + (anak[10]-iris[i][2])**2 + (anak[11]-iris[i][2])**2)
        
        """
        1. Meng-assign data ke kluster
        2. Menghitung nilai fitness, yaitu total jarak data pada tiap kluster tempat dia di assign
        """
        smallest = jarak.index(min(jarak))
        if smallest == 0:
            kluster1.append((i, jarak[smallest]))
            jumlah_twcv[smallest] = jumlah_twcv[smallest] + jarak[smallest]
        elif smallest == 1:
            kluster2.append((i, jarak[smallest]))
            jumlah_twcv[smallest] = jumlah_twcv[smallest] + jarak[smallest]
        else:
            kluster3.append((i, jarak[smallest]))
            jumlah_twcv[smallest] = jumlah_twcv[smallest] + jarak[smallest] 

    return sum(jumlah_twcv)

def seleksi_parent(error):
    """
    Seleksi parent menggunakan Baker SUS n=6
    """
    n = 6
    parent = error
    total = sum(error)
    rws = [(lambda r: total/parent[r])(r) for r in range(10)]
    ratio = [(lambda q: rws[q]/sum(rws))(q) for q in range(10)]
    
    titik = [0]
    for i in range(10):
        titik.append(titik[i] + ratio[i])

    choosen = []
    sus = [random.uniform(0, 1/n)]
    for j in range(n):
        sus.append(sus[j]+round(1/n, 3))
        for k in range(10):
            if sus[j] >= titik[k] and sus[j] < titik[k+1]:
                choosen.append(k)
    return choosen

def crossover(orangtua):
    """
    Crossover menggunakan whole arithmetic crossover dengan a = 0.7 dan PC = 0.8
    """
    pc = 0.8
    a = 0.7
    b = 1 - a
    prob = [(lambda p: random.uniform(0,1))(p) for p in range(len(orangtua))]
    
    pool = []
    for i in range(len(prob)):
        if prob[i] < 0.8:
            pool.append(i)

    l = len(pool)
    hasil = []
    off = np.zeros((l, 12))
    for k in range(l-1):
        for j in range(12):
            off[k][j] = a * individu[pool[k]][j] + b * individu[pool[k+1]][j]
            off[k+1][j] = a * individu[pool[k+1]][j] + b * individu[pool[k]][j]
        hasil.append(off[k][:])
        hasil.append(off[k+1][:])
    return hasil

def mutasi(z):
    """
    Mutasi menggunakan mutasi uniform dengan menggunakan PM = 0.01
    """
    pm = 0.01
    prob = [(lambda p: random.uniform(0,1))(p) for p in range(len(z))]
    for i in range(len(z)):
        if prob[i]<pm:
            z[i][random.randint(0,11)] = random.uniform(0,5)
    return z

"""
Me-load dataset
"""
load = datasets.load_iris()
iris = np.array(load.data, dtype=float)

"""
Inisialisasi populasi
"""
individu = np.zeros((10,12))
generate()

error = np.zeros(10)

generation = 100
"""
Training
"""
for x in range(10):
    error[x] = fitness(individu[x][:]) #Menghitung nilai Fitness

choosen_parent = seleksi_parent(error) #Seleksi Parent
offspring = crossover(choosen_parent)  #Crossover
mutated = mutasi(offspring)            #Mutasi
survivor = mutated                     #Selesi Survivor - Metode Holland

while generation > 0:
    for kol in range(10):
        error[kol] = fitness(individu[x][:]) #Menghitung nilai Fitness

    choosen_parent = seleksi_parent(error) #Seleksi Parent
    offspring = crossover(choosen_parent)  #Crossover
    mutated = mutasi(offspring)            #Mutasi
    survivor = mutated                     #Selesi Survivor - Metode Holland
    print(survivor)                        #Output hasil
    kol, bar = np.shape(survivor)
    generation = generation -1
