# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 20:35:47 2020

@author: sebtac

@title: ST's THOMPSON SAMPLING BASED BANDIT ALGORITHM for BEST MODEL SEARCH - MULTIPROCESSING EDITION

@objective: create TS based algorithm for best model search with multiprocessing implementation

@characteristics:
- for normally distributed objective (update STTS_sampler() otherwise)
- implementation for maximization objective (update # cond_index = np.argmin() otherwise)
- implemented with simple test case (update target = () to adjust to your use case)

@usage:

1.) Initalize trial_control table, one row per condition, count, each distribution paramter (example: norm(mu,sd))
2.) Initalize tiral_table to collect the measure of interst accross all runs
3.) Set max_count -- how many times each candidate model should be tested -- we do nto want to run best model idefinatively but rather test "thoroughly" couple best models
4.) Set top_count -- how many candidate models should be fully tested (with max_count runs)
5.) List Conditions (the model parameters) (COND1, COND2)
6.) Adjust target variable to your use case -- this is the traget objective.

"""

import multiprocessing as mp
import numpy as np
import random

mp_start_count = 0
np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

# ST's THOMPSON SAMPLING BASED BEST MODEL SEARCH - MULTIPROCESSING EDITION
random.seed(random.random())
np.random.seed(int(random.random()*100000))

def STTS_sampler(table, i, mu = 0, sd = 1):
    if table[2,i] == 0:
        mu = table[3,:].max()
        sd = table[4,:].max()
    elif table[2,i] == 1:
        mu = table[3,i]
        sd = table[4,:].max()
    else:
        mu = table[3,i]
        sd = table[4,i]#/np.sqrt(table[6,i])
    
    # assumes target variable disctributed normally -- adjust as needed
    return np.random.normal(mu, sd)
        
def executor(worker,
             lock,
             bandit_control_list,
             bandit_trial_list,
            stop_value):
             #cond_list,
             #cond_id_list):
    
    lock.acquire()
    while stop_value.value == 0:
        table = bandit_control_list[0]
        table_trial = bandit_trial_list[0]
        
        cond_samples = [STTS_sampler(table, i) for i in range(table.shape[1])]
        # identify the chosen element
        # consider only elements that were tested less than max_count times! for balanced exploration
        cond_index_mask = np.where(table[2,:]>=max_count,0,1)
        values = np.asarray(cond_samples)
        # np.random.random(values.shape) -- to break the ties! (otherwise only the first encountered will be used)
        # IF OBJECTIVE IS MAXIMUM
        cond_index = np.argmax(np.random.random(values.shape) * (values*cond_index_mask==(values*cond_index_mask).max()))
        # IF OBJECTIVE IS MINIMUM -- adjust to take care of ZEROs!
        # cond_index = np.argmin(np.random.random(values.shape) * (values*cond_index_mask==(values*cond_index_mask).max()))

        cond1_select = table[0,cond_index]
        cond2_select = table[1,cond_index]

        # current target value -- here put your measure of interst
        target = (np.random.random())*(cond1_select * cond2_select) #+ table[2,cond_index]

        # UPDATE TABLE

        run = int(table[2,cond_index])
        #print(run, cond_index)
        table_trial[run,cond_index] = target
        
        #n += 1
        table[2,cond_index] += 1

        # mu
        #print(np.average(table_trial[:run,cond_index]))
        table[3,cond_index] = np.average(table_trial[:run+1,cond_index])
        # sd
        #print(np.std(table_trial[:run,cond_index]))
        table[4,cond_index] = np.std(table_trial[:run+1,cond_index])
        
        if np.where(table[2,:]>=max_count,1,0).sum() >= top_count:
            stop_value.value = 1
            
        bandit_control_list[0] = table
        bandit_trial_list[0] = table_trial
        #print(worker, cond1_select,cond2_select,cond_index)
    lock.release()
    
if __name__ == '__main__':
    if mp_start_count == 0:
        mp.set_start_method('fork')
        mp_start_count += 1

    manager = mp.Manager()
    lock = mp.Lock()
    
    max_count = 16
    top_count = 10
        
    cond1 = [8,16,32,64,128] #[1,2,3,4,8,16,32,64,128] # LSTM Cells N
    cond2 = [3,4,5,6,7,8,9,10,15] #[2,3,4,5,6,7,8,9,10,15,20]#,30,40,60] # Input Length
    
    cond1_length = len(cond1)
    cond2_length = len(cond2)
    
    bandit_control_table = np.zeros([5,cond1_length*cond2_length])
    
    cond1_count = 0
    for i in cond1:
        cond2_count = 0
        for j in cond2:
            bandit_control_table[0,cond1_count*cond2_length+cond2_count] = i # COND 1
            bandit_control_table[1,cond1_count*cond2_length+cond2_count] = j # COND 2
            cond2_count+=1
        cond1_count+=1
    
    for i in range(cond1_length*cond2_length):
        bandit_control_table[2,i] = 1.0 # N
        bandit_control_table[3,i] = 1.0 # MU
        bandit_control_table[4,i] = 1.0 # SD
    
    #print(bandit_control_table)
    bandit_control_list = manager.list()
    bandit_control_list.append(bandit_control_table)
    
    bandit_trial_table = np.zeros([max_count,cond1_length*cond2_length])
    
    bandit_trial_list = manager.list()
    bandit_trial_list.append(bandit_trial_table)

    stop_value = mp.Value('i', 0)

    # MULTIPROCESSING
    executors_n = mp.cpu_count()
    print("executors_n", executors_n)

    jobs = []

    for worker in range(executors_n):
        p = mp.Process(target=executor, args = (worker,
                                                lock,
                                                bandit_control_list,
                                                bandit_trial_list,
                                                stop_value))
        jobs.append(p)
        p.start()

    for j in jobs: # Otherwise you need to run #time.sleep(1) next
        j.join()

    for j in jobs: # Otherwise you need to run #time.sleep(1) next
        j.close()
        
    print(bandit_control_list[0])
    print(np.argmax(bandit_control_list[0][3,:]))
    
