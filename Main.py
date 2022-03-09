#Karali Agoritsa Eirini dai17065

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance
from sklearn.metrics import mean_absolute_error
from scipy import stats
from random import randint
import statistics

#Class Movie
class Movie:
    def __init__(self, name):   # constructor
        self.name = name
        self.list = []
    
    def set_element(self, jList):
         self.list.append(jList)
    
    def get_list(self):
        return self.list


#Functions    

#define average calculation
def average(ar):
    array= ar.tolist()
    print(array)
    for i in range(99):
        avg = sum(array[i])/100
        for j in range(99):
            elem=(array[i][j]) - avg
            array.pop([i][j])
            array.insert([i][j], elem)
    return array

#define Create Set function
def createSet1(list):
    jlist = []
    for i in range(100):
        if list[i] != 0:
            jlist.append(1)
        else:
            jlist.append(0)
    return(jlist)
    
def createSet(list):
    jlist = []
    for i in range(100):
        if list[i] != 0:
            jlist.append(i)
    return(jlist)
    
#define Jaccard Similarity function
def jaccard(list1, list2):
    l1 = set(list1)
    l2 = set(list2)
    inter = l1.intersection(l2)
    union = l1.union(l2)
    return float("{:.2f}".format((len(inter)/len(union))))


#MAIN
#Create DataFrame from Excel
rating_data = pd.read_excel('rating_movies.xlsx', sheet_name='movie80')

#movies names
moviesName = pd.read_excel("rating_movies.xlsx", nrows=0)
m = list(moviesName) 
m.pop(0)

#calculate Jaccard Similarity for all movies
jMov = []
j = 0
for x in m:
    l3 = rating_data[x].tolist()
    l3 = createSet(l3)
    mo = Movie(x)
    for k in m:
        l4 = rating_data[k].tolist()
        l4 = createSet(l4)
        mo.set_element(jaccard(l3, l4))
    #print(mo.get_list())
    jMov.insert(j, mo.get_list())
    j = j + 1
print("Υπολογισμος του Jaccard Similarity για κάθε αντικείμενο" )  
print('------------------------------------------')
#print(jMov)

j=0
#Calculate Dice distance for all movies
dMov = []
for x in m:
    l1 = rating_data[x].tolist()
    l1 = createSet1(l1)
    mo = Movie(x)
    for k in m:
        l2 = rating_data[k].tolist()
        l2 = createSet1(l2)
        mo.set_element(float("{:.2f}".format(distance.dice(l1, l2))))
    #print(mo.get_list())
    dMov.insert(j, mo.get_list())
    j = j + 1
print("Υπολογισμος του Dice Similarity για κάθε αντικείμενο" )
print('------------------------------------------')
#print(dMov[99])

#Calculate Cosine Similarity distance for all movies
j=0
cMov = []
for x in m:
    l5 = rating_data[x].tolist()
    mo = Movie(x)
    for k in m:
        l6 = rating_data[k].tolist()
        mo.set_element(float("{:.2f}".format(distance.cosine(l5, l6))))
    #print(mo.get_list())
    cMov.insert(j, mo.get_list())
    j = j + 1
print("Υπολογισμος του Cosine Similarity για κάθε αντικείμενο" )
print('-----------------------------------------------')


#Calculate Adjusted Cosine Similarity distance for all movies
data = pd.read_excel('rating_movies.xlsx', sheet_name='movie80')
data["sum"] = data.mean(axis=1)

for k in m:
    data[k] = rating_data[k] - data["sum"]

j=0
acMov = []
for x in m:
    l7 = data[x].tolist()
    mo = Movie(x)
    for k in m:
        l8 = data[k].tolist()
        mo.set_element(float("{:.2f}".format(distance.cosine(l7, l8))))
    #print(mo.get_list())
    acMov.insert(j, mo.get_list())
    j = j + 1
print("Υπολογισμος του Adjusted Cosine Similarity για κάθε αντικείμενο" )
print('-----------------------------------------------')
#print(acMov[99])

#choose K max values from random user 
mAvg_jMov=[]
jacc_meanAvgEr=[]
avg_jMov=[]
jacc_AvgEr=[]

mAvg_dMov=[]
dice_meanAvgEr=[]
avg_dMov=[]
dice_AvgEr=[]

mAvg_cMov=[]
coss_meanAvgEr=[]
avg_cMov=[]
coss_AvgEr=[]

mAvg_acMov=[]
aCoss_meanAvgEr=[]
avg_acMov=[]
aCoss_AvgEr=[]
user_r = pd.read_excel("rating_movies.xlsx", sheet_name='movie80')
for T in range(10):
    mAvg_jMov.clear()
    avg_jMov.clear()
    mAvg_dMov.clear()
    avg_dMov.clear()
    mAvg_cMov.clear()
    avg_cMov.clear()
    mAvg_acMov.clear()
    avg_acMov.clear()
    print(str(T+1) +" επανάληψη...")
    
    #find user's ratings
    user = randint(1, 100)
    user_rate = list(rating_data.iloc[user])
    user_rate.pop(0)
    
    #Calculate mean Avg error with jaccard similarity
    listJ=[]
  
    j=0
    
    for j in range(100):
        user_rates1 = list(user_r.iloc[user])
        user_rates1.pop(0)
        sum_j=0
        prod=0
        listJ=jMov[j].copy()
        for k in range(19):
            max_value=0
            max_value=max(listJ)
            sum_j += max_value
            p=0
            while p <(len(listJ)):
                if max_value==listJ[p]:
                    prod+=max_value*float(user_rates1[p])
                    listJ.pop(p)
                    user_rates1.pop(p)
                    break
                p+=1
        if sum_j == 0:
            user= randint(1, 99)
        else:
            mAvg_jMov.append(float("{:.2f}".format(prod/sum_j)))
            avg_jMov.append(float("{:.2f}".format(prod/30)))
    jacc_meanAvgEr.append(float("{:.2f}".format(mean_absolute_error(user_rate, mAvg_jMov))))
    jacc_AvgEr.append(float("{:.2f}".format(mean_absolute_error(user_rate, avg_jMov))))

    #Calculate mean Avg error with dice similarity
    j=0
    for j in range(100):
        user_rates2 = list(user_r.iloc[user])
        user_rates2.pop(0)
        listD=dMov[j].copy()
        sum_j=0
        prod=0
        for k in range(19):
            max_value=max(listD)
            sum_j += max_value
            p=0
            while p <(len(listD)):
                if max_value==listD[p]:
                    prod+=max_value*float(user_rates2[p])
                    listD.pop(p)
                    user_rates2.pop(p)
                    break
                p+=1
        if sum_j == 0:
            user= randint(1, 99)
            
        else:
            mAvg_dMov.append(float("{:.2f}".format(prod/sum_j)))
            avg_dMov.append(float("{:.2f}".format(prod/30)))
    dice_meanAvgEr.append(float("{:.2f}".format(mean_absolute_error(user_rate, mAvg_dMov))))
    dice_AvgEr.append(float("{:.2f}".format(mean_absolute_error(user_rate, avg_dMov))))
    
    #Calculate mean Avg error with cossine similarity
    j=0
    
    for j in range(100):
        user_rates3 = list(user_r.iloc[user])
        user_rates3.pop(0)
        listC=cMov[j].copy()
        sum_j=0
        prod=0
        for k in range(19):
            max_value=max(listJ)
            sum_j += max_value
            p=0
            while p <(len(listC)):
                if max_value==listC[p]:
                    prod+=max_value*float(user_rates3[p])
                    listC.pop(p)
                    user_rates3.pop(p)
                    break
                p+=1
        if sum_j == 0:
            user= randint(1, 99)
        else:
            mAvg_cMov.append(float("{:.2f}".format(prod/sum_j)))
            avg_cMov.append(float("{:.2f}".format(prod/30)))
    coss_meanAvgEr.append(float("{:.2f}".format(mean_absolute_error(user_rate, mAvg_cMov))))
    coss_AvgEr.append(float("{:.2f}".format(mean_absolute_error(user_rate, avg_cMov))))
    
    #Calculate mean Avg error with Adjusted cossine similarity
    j=0
    for j in range(100):
        user_rates4 = list(user_r.iloc[user])
        user_rates4.pop(0)
        listAC=acMov[j].copy()
        sum_j=0
        prod=0
        for k in range(19):
            max_value=max(listAC)
            sum_j += max_value
            p=0
            while p <(len(listAC)):
                if max_value==listAC[p]:
                    prod+=max_value*float(user_rates4[p])
                    listAC.pop(p)
                    user_rates4.pop(p)
                    break
                p+=1
        if sum_j == 0:
            user= randint(1, 99)
            
        else:
            mAvg_acMov.append(float("{:.2f}".format(prod/sum_j)))
            avg_acMov.append(float("{:.2f}".format(prod/30)))
    aCoss_meanAvgEr.append(float("{:.2f}".format(mean_absolute_error(user_rate, mAvg_acMov))))
    aCoss_AvgEr.append(float("{:.2f}".format(mean_absolute_error(user_rate, mAvg_acMov))))
    
    listJ.clear()
    listD.clear()
    listC.clear()
    listAC.clear()

print("Μέσος όρος, του μέσου λάθος, υπολογισμένο με τους σταθμισμένους μέσους όρους (jaccard sim) απο 10 τυχαίους χρήστες" )
print(jacc_meanAvgEr)    
print(float("{:.2f}".format(statistics.mean(jacc_meanAvgEr))))
print("Μέσος όρος, του μέσου λάθος, υπολογισμένο με τους μέσους όρους (jaccard sim) απο 10 τυχαίους χρήστες" )
print(jacc_AvgEr) 
print(float("{:.2f}".format(statistics.mean(jacc_AvgEr))))
print("Μέσος όρος, του μέσου λάθος, υπολογισμένο με τους σταθμισμένους μέσους όρους (dice sim) απο 10 τυχαίους χρήστες" )
print(float("{:.2f}".format(statistics.mean(dice_meanAvgEr))))
print(dice_meanAvgEr)
print("Μέσος όρος, του μέσου λάθος, υπολογισμένο με τους μέσους όρους (dice sim) απο 10 τυχαίους χρήστες" )
print(float("{:.2f}".format(statistics.mean(dice_AvgEr))))
print(dice_AvgEr)
print("Μέσος όρος, του μέσου λάθος, υπολογισμένο με τους σταθμισμένους μέσους όρους (cossine sim) απο 10 τυχαίους χρήστες" )
print(float("{:.2f}".format(statistics.mean(coss_meanAvgEr))))
print(coss_meanAvgEr)
print("Μέσος όρος, του μέσου λάθος, υπολογισμένο με τους μέσους όρους (cossine sim) απο 10 τυχαίους χρήστες" )
print(float("{:.2f}".format(statistics.mean(coss_AvgEr))))
print(coss_AvgEr)
print("Μέσος όρος, του μέσου λάθος, υπολογισμένο με τους σταθμισμένους μέσους όρους (Adjusted cossine sim) απο 10 τυχαίους χρήστες" )
print(float("{:.2f}".format(statistics.mean(aCoss_meanAvgEr))))
print(aCoss_meanAvgEr)
print("Μέσος όρος, του μέσου  λάθος, υπολογισμένο με τους μέσους όρους (Adjusted cossine sim) απο 10 τυχαίους χρήστες" )  
print(float("{:.2f}".format(statistics.mean(aCoss_AvgEr))))
print(aCoss_AvgEr)
    
    






