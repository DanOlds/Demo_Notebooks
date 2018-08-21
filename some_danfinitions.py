# A small and barely curated selection of python routines to make the education and initiation of students 
# into the wild world of total scattering just a little bit easier.  - Dan
#  
# Question --> oldsdp@ornl.gov

import numpy as np

def read_getN_file(filename,return_in_d = True):
    with open(filename,'r') as filein:
        all_lines = filein.readlines()
    
    tot_histos = int(all_lines[4].split()[1])
    #print (tot_histos)
    
    difc_list = np.zeros(tot_histos)
    line_on = 12

    all_banks_tof = []
    all_banks_int = []
    all_banks_d = []
    
    for cur_histo in range(tot_histos):
        difc_list[cur_histo] = float(all_lines[line_on].split()[-1])
        bank_length = int(all_lines[line_on+2].split()[2])
        #print ("bank length is "+str(bank_length))
        this_bank_tof = np.zeros(bank_length)
        this_bank_int = np.zeros(bank_length)
        
        line_on += 3
        is_on = 0
        while is_on < bank_length:
            this_bank_tof[is_on] = float(all_lines[line_on+is_on].split()[0])
            this_bank_int[is_on] = float(all_lines[line_on+is_on].split()[1])
            is_on += 1
            
        
        #print ('done')
        line_on += is_on
        all_banks_tof.append(this_bank_tof)
        all_banks_int.append(this_bank_int)
        all_banks_d.append(this_bank_tof/difc_list[cur_histo])
    
    if return_in_d:
        return np.array(all_banks_d), np.array(all_banks_int)
    else:
        return np.array(all_banks_tof), np.array(all_banks_int)
        
def read_nomad_sq(filename,junk=5,backjunk = 0):
    with open(filename,'r') as infile:
        datain = infile.readlines()
    if backjunk == 0:
        datain = datain[junk:]
    else:
        datain = datain[junk:-backjunk]
    
    xin = np.zeros(len(datain))
    yin = np.zeros(len(datain))
    print ('reading from file '+filename)
    #print ('length '+str(len(xin)))
    for i in range(len(datain)):
        xin[i]= float(datain[i].split()[0])
        yin[i]= float(datain[i].split()[1])
    return xin,yin
    
def pdf_transform(x,y,rmin=0,rmax=20,delr=.05, qmin=None, qmax=None):
    r = np.arange(rmin,rmax+delr/2.0,delr)
    gr = np.zeros(len(r))
    
    if qmin != None and qmax == None:
        x,y = cut_data(x,y,qmin,1000)
        print ('cutting qmin')
    if qmax != None and qmin == None:
        x,y = cut_data(x,y,0,qmax)
        print ('cutting qmax')
    if qmax != None and qmin != None:
        x,y = cut_data(x,y,qmin,qmax)
        print ('cutting both')
    
    for rvals in range(len(r)):
        for qvals in range(len(x)):
            gr[rvals] += x[qvals]*y[qvals]*np.sin(r[rvals]*x[qvals])
    gr = gr / (16.0*np.pi)
    gr = np.nan_to_num(gr)
    return r,gr
    
def cut_data(qt,sqt,qmin,qmax):
    qcut = []
    sqcut = []
    for i in range(len(qt)):
        if qt[i] >= qmin and qt[i] <= qmax:
            qcut.append(qt[i])
            sqcut.append(sqt[i])

    qcut = np.array(qcut)
    sqcut = np.array(sqcut)
    return qcut, sqcut      