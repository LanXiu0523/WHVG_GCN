from scipy.io import loadmat
import numpy as np
import os

##Data information init

#Data path init
load_path_NormalData = os.path.join(os.getcwd(),'data/Normal.mat')  
NormalData = loadmat(load_path_NormalData)
load_path_FaultData = os.path.join(os.getcwd(),'data/Fault_IR0.mat')  
FaultData_IR0 = loadmat(load_path_FaultData)
load_path_FaultData = os.path.join(os.getcwd(),'data/Fault_Ba0.mat')  
FaultData_Ba0 = loadmat(load_path_FaultData)
load_path_FaultData = os.path.join(os.getcwd(),'data/Fault_OR0.mat')  
FaultData_OR0 = loadmat(load_path_FaultData)
load_path_FaultData = os.path.join(os.getcwd(),'data/Fault_IR1.mat')  
FaultData_IR1 = loadmat(load_path_FaultData)
load_path_FaultData = os.path.join(os.getcwd(),'data/Fault_Ba1.mat')  
FaultData_Ba1 = loadmat(load_path_FaultData)
load_path_FaultData = os.path.join(os.getcwd(),'data/Fault_OR1.mat')  
FaultData_OR1 = loadmat(load_path_FaultData)
load_path_FaultData = os.path.join(os.getcwd(),'data/Fault_IR2.mat')  
FaultData_IR2 = loadmat(load_path_FaultData)
load_path_FaultData = os.path.join(os.getcwd(),'data/Fault_Ba2.mat')  
FaultData_Ba2 = loadmat(load_path_FaultData)
load_path_FaultData = os.path.join(os.getcwd(),'data/Fault_OR2.mat')  
FaultData_OR2 = loadmat(load_path_FaultData)

#Data number initialization(following for CWRU)
No_NormalData='X097'
No_Fault_IR0_Data='X105'
No_Fault_Ba0_Data='X118'
No_Fault_OR0_Data='X130'
No_Fault_IR1_Data='X106'
No_Fault_Ba1_Data='X119'
No_Fault_OR1_Data='X131'
No_Fault_IR2_Data='X107'
No_Fault_Ba2_Data='X120'
No_Fault_OR2_Data='X132'
FaultData_Label_NUM = 9
NormalDataset_size = 102400
FaultDataset_size = 102400
Data_size = 1024


#Sample condition init(following for CWRU)
NormalData = NormalData[(No_NormalData+'_DE_time')][0:NormalDataset_size]
FaultData_IR0 = FaultData_IR0[(No_Fault_IR0_Data+'_DE_time')][0:FaultDataset_size]
FaultData_Ba0 = FaultData_Ba0[(No_Fault_Ba0_Data+'_DE_time')][0:FaultDataset_size]
FaultData_OR0 = FaultData_OR0[(No_Fault_OR0_Data+'_DE_time')][0:FaultDataset_size]
FaultData_IR1 = FaultData_IR1[(No_Fault_IR1_Data+'_DE_time')][0:FaultDataset_size]
FaultData_Ba1 = FaultData_Ba1[(No_Fault_Ba1_Data+'_DE_time')][0:FaultDataset_size]
FaultData_OR1 = FaultData_OR1[(No_Fault_OR1_Data+'_DE_time')][0:FaultDataset_size]
FaultData_IR2 = FaultData_IR2[(No_Fault_IR2_Data+'_DE_time')][0:FaultDataset_size]
FaultData_Ba2 = FaultData_Ba2[(No_Fault_Ba2_Data+'_DE_time')][0:FaultDataset_size]
FaultData_OR2 = FaultData_OR2[(No_Fault_OR2_Data+'_DE_time')][0:FaultDataset_size]

NormalData_Graph_size = len(NormalData)//Data_size
FaultData_Graph_size = len(FaultData_IR0)//Data_size
FaultData_Graph_size_SUM = FaultData_Graph_size*FaultData_Label_NUM
Graph_size = NormalData_Graph_size + FaultData_Graph_size_SUM

NormalData_REG = NormalData.reshape(NormalData_Graph_size,Data_size)
FaultData_IR0_REG = FaultData_IR0.reshape(FaultData_Graph_size,Data_size)
FaultData_Ba0_REG = FaultData_Ba0.reshape(FaultData_Graph_size,Data_size)
FaultData_OR0_REG = FaultData_OR0.reshape(FaultData_Graph_size,Data_size)
FaultData_IR1_REG = FaultData_IR1.reshape(FaultData_Graph_size,Data_size)
FaultData_Ba1_REG = FaultData_Ba1.reshape(FaultData_Graph_size,Data_size)
FaultData_OR1_REG = FaultData_OR1.reshape(FaultData_Graph_size,Data_size)
FaultData_IR2_REG = FaultData_IR2.reshape(FaultData_Graph_size,Data_size)
FaultData_Ba2_REG = FaultData_Ba2.reshape(FaultData_Graph_size,Data_size)
FaultData_OR2_REG = FaultData_OR2.reshape(FaultData_Graph_size,Data_size)

Graph = [[[]for j in range(Data_size)] for i in range(Graph_size)]
Graph_index_CUR = 0


# NormalData
for Graph_index in range(Graph_index_CUR,NormalData_Graph_size):
    print("loading Graph_"+str(Graph_index)+" //...")
    for Va_index in range(Data_size):
        for Vb_index in range(Data_size):
            if Va_index==Vb_index:
                continue
            Visibility = True

            if Va_index < Vb_index:
                for Vc_index in range(Va_index+1,Vb_index):
                    if((NormalData_REG[Graph_index,Vc_index] >= NormalData_REG[Graph_index,Vb_index]
                        +(NormalData_REG[Graph_index,Va_index]-NormalData_REG[Graph_index,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) >= 0)
                        | (NormalData_REG[Graph_index,Vc_index] <= NormalData_REG[Graph_index,Vb_index]
                        +(NormalData_REG[Graph_index,Va_index]-NormalData_REG[Graph_index,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) <= 0)):
                        Visibility = False
                        break
                if Visibility:
                    Graph[Graph_index][Va_index].append(Vb_index)

            else:
                for Vc_index in range(Vb_index+1,Va_index):
                    if((NormalData_REG[Graph_index,Vc_index] >= NormalData_REG[Graph_index,Vb_index]
                        +(NormalData_REG[Graph_index,Va_index]-NormalData_REG[Graph_index,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) >= 0)
                        | (NormalData_REG[Graph_index,Vc_index] <= NormalData_REG[Graph_index,Vb_index]
                        +(NormalData_REG[Graph_index,Va_index]-NormalData_REG[Graph_index,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) <= 0)):
                        Visibility = False
                        break
                if Visibility:
                    Graph[Graph_index][Va_index].append(Vb_index)

Graph_index_CUR += NormalData_Graph_size


# FaultData_IR0
for Graph_index in range(Graph_index_CUR,Graph_index_CUR+FaultData_Graph_size):
    print("loading Graph_"+str(Graph_index)+" //...")
    for Va_index in range(Data_size):
        for Vb_index in range(Data_size):
            if Va_index==Vb_index:
                continue
            Visibility = True

            if Va_index < Vb_index:
                for Vc_index in range(Va_index+1,Vb_index):
                    if((FaultData_IR0_REG[Graph_index%FaultData_Graph_size,Vc_index] >= FaultData_IR0_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_IR0_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_IR0_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) >= 0)
                        | (FaultData_IR0_REG[Graph_index%FaultData_Graph_size,Vc_index] <= FaultData_IR0_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_IR0_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_IR0_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) <= 0)):
                        Visibility = False
                        break
                if Visibility:
                    Graph[Graph_index][Va_index].append(Vb_index)

            else:
                for Vc_index in range(Vb_index+1,Va_index):
                    if((FaultData_IR0_REG[Graph_index%FaultData_Graph_size,Vc_index] >= FaultData_IR0_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_IR0_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_IR0_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) >= 0)
                        | (FaultData_IR0_REG[Graph_index%FaultData_Graph_size,Vc_index] <= FaultData_IR0_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_IR0_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_IR0_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) <= 0)):
                        Visibility = False
                        break
                if Visibility:
                    Graph[Graph_index][Va_index].append(Vb_index)

Graph_index_CUR += FaultData_Graph_size


# FaultData_Ba0
for Graph_index in range(Graph_index_CUR,Graph_index_CUR+FaultData_Graph_size):
    print("loading Graph_"+str(Graph_index)+" //...")
    for Va_index in range(Data_size):
        for Vb_index in range(Data_size):
            if Va_index==Vb_index:
                continue
            Visibility = True

            if Va_index < Vb_index:
                for Vc_index in range(Va_index+1,Vb_index):
                    if((FaultData_Ba0_REG[Graph_index%FaultData_Graph_size,Vc_index] >= FaultData_Ba0_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_Ba0_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_Ba0_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) >= 0)
                        | (FaultData_Ba0_REG[Graph_index%FaultData_Graph_size,Vc_index] <= FaultData_Ba0_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_Ba0_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_Ba0_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) <= 0)):
                        Visibility = False
                        break
                if Visibility:
                    Graph[Graph_index][Va_index].append(Vb_index)

            else:
                for Vc_index in range(Vb_index+1,Va_index):
                    if((FaultData_Ba0_REG[Graph_index%FaultData_Graph_size,Vc_index] >= FaultData_Ba0_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_Ba0_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_Ba0_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) >= 0)
                        | (FaultData_Ba0_REG[Graph_index%FaultData_Graph_size,Vc_index] <= FaultData_Ba0_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_Ba0_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_Ba0_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) <= 0)):
                        Visibility = False
                        break
                if Visibility:
                    Graph[Graph_index][Va_index].append(Vb_index)

Graph_index_CUR += FaultData_Graph_size


# FaultData_OR0
for Graph_index in range(Graph_index_CUR,Graph_index_CUR+FaultData_Graph_size):
    print("loading Graph_"+str(Graph_index)+" //...")
    for Va_index in range(Data_size):
        for Vb_index in range(Data_size):
            if Va_index==Vb_index:
                continue
            Visibility = True

            if Va_index < Vb_index:
                for Vc_index in range(Va_index+1,Vb_index):
                    if((FaultData_OR0_REG[Graph_index%FaultData_Graph_size,Vc_index] >= FaultData_OR0_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_OR0_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_OR0_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) >= 0)
                        | (FaultData_OR0_REG[Graph_index%FaultData_Graph_size,Vc_index] <= FaultData_OR0_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_OR0_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_OR0_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) <= 0)):
                        Visibility = False
                        break
                if Visibility:
                    Graph[Graph_index][Va_index].append(Vb_index)

            else:
                for Vc_index in range(Vb_index+1,Va_index):
                    if((FaultData_OR0_REG[Graph_index%FaultData_Graph_size,Vc_index] >= FaultData_OR0_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_OR0_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_OR0_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) >= 0)
                        | (FaultData_OR0_REG[Graph_index%FaultData_Graph_size,Vc_index] <= FaultData_OR0_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_OR0_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_OR0_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) <= 0)):
                        Visibility = False
                        break
                if Visibility:
                    Graph[Graph_index][Va_index].append(Vb_index)

Graph_index_CUR += FaultData_Graph_size


# FaultData_IR1
for Graph_index in range(Graph_index_CUR,Graph_index_CUR+FaultData_Graph_size):
    print("loading Graph_"+str(Graph_index)+" //...")
    for Va_index in range(Data_size):
        for Vb_index in range(Data_size):
            if Va_index==Vb_index:
                continue
            Visibility = True

            if Va_index < Vb_index:
                for Vc_index in range(Va_index+1,Vb_index):
                    if((FaultData_IR1_REG[Graph_index%FaultData_Graph_size,Vc_index] >= FaultData_IR1_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_IR1_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_IR1_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) >= 0)
                        | (FaultData_IR1_REG[Graph_index%FaultData_Graph_size,Vc_index] <= FaultData_IR1_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_IR1_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_IR1_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) <= 0)):
                        Visibility = False
                        break
                if Visibility:
                    Graph[Graph_index][Va_index].append(Vb_index)

            else:
                for Vc_index in range(Vb_index+1,Va_index):
                    if((FaultData_IR1_REG[Graph_index%FaultData_Graph_size,Vc_index] >= FaultData_IR1_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_IR1_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_IR1_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) >= 0)
                        | (FaultData_IR1_REG[Graph_index%FaultData_Graph_size,Vc_index] <= FaultData_IR1_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_IR1_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_IR1_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) <= 0)):
                        Visibility = False
                        break
                if Visibility:
                    Graph[Graph_index][Va_index].append(Vb_index)

Graph_index_CUR += FaultData_Graph_size


# FaultData_Ba1
for Graph_index in range(Graph_index_CUR,Graph_index_CUR+FaultData_Graph_size):
    print("loading Graph_"+str(Graph_index)+" //...")
    for Va_index in range(Data_size):
        for Vb_index in range(Data_size):
            if Va_index==Vb_index:
                continue
            Visibility = True

            if Va_index < Vb_index:
                for Vc_index in range(Va_index+1,Vb_index):
                    if((FaultData_Ba1_REG[Graph_index%FaultData_Graph_size,Vc_index] >= FaultData_Ba1_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_Ba1_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_Ba1_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) >= 0)
                        | (FaultData_Ba1_REG[Graph_index%FaultData_Graph_size,Vc_index] <= FaultData_Ba1_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_Ba1_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_Ba1_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) <= 0)):
                        Visibility = False
                        break
                if Visibility:
                    Graph[Graph_index][Va_index].append(Vb_index)

            else:
                for Vc_index in range(Vb_index+1,Va_index):
                    if((FaultData_Ba1_REG[Graph_index%FaultData_Graph_size,Vc_index] >= FaultData_Ba1_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_Ba1_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_Ba1_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) >= 0)
                        | (FaultData_Ba1_REG[Graph_index%FaultData_Graph_size,Vc_index] <= FaultData_Ba1_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_Ba1_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_Ba1_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) <= 0)):
                        Visibility = False
                        break
                if Visibility:
                    Graph[Graph_index][Va_index].append(Vb_index)

Graph_index_CUR += FaultData_Graph_size


# FaultData_OR1
for Graph_index in range(Graph_index_CUR,Graph_index_CUR+FaultData_Graph_size):
    print("loading Graph_"+str(Graph_index)+" //...")
    for Va_index in range(Data_size):
        for Vb_index in range(Data_size):
            if Va_index==Vb_index:
                continue
            Visibility = True

            if Va_index < Vb_index:
                for Vc_index in range(Va_index+1,Vb_index):
                    if((FaultData_OR1_REG[Graph_index%FaultData_Graph_size,Vc_index] >= FaultData_OR1_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_OR1_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_OR1_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) >= 0)
                        | (FaultData_OR1_REG[Graph_index%FaultData_Graph_size,Vc_index] <= FaultData_OR1_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_OR1_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_OR1_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) <= 0)):
                        Visibility = False
                        break
                if Visibility:
                    Graph[Graph_index][Va_index].append(Vb_index)

            else:
                for Vc_index in range(Vb_index+1,Va_index):
                    if((FaultData_OR1_REG[Graph_index%FaultData_Graph_size,Vc_index] >= FaultData_OR1_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_OR1_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_OR1_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) >= 0)
                        | (FaultData_OR1_REG[Graph_index%FaultData_Graph_size,Vc_index] <= FaultData_OR1_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_OR1_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_OR1_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) <= 0)):
                        Visibility = False
                        break
                if Visibility:
                    Graph[Graph_index][Va_index].append(Vb_index)

Graph_index_CUR += FaultData_Graph_size


# FaultData_IR2
for Graph_index in range(Graph_index_CUR,Graph_index_CUR+FaultData_Graph_size):
    print("loading Graph_"+str(Graph_index)+" //...")
    for Va_index in range(Data_size):
        for Vb_index in range(Data_size):
            if Va_index==Vb_index:
                continue
            Visibility = True

            if Va_index < Vb_index:
                for Vc_index in range(Va_index+1,Vb_index):
                    if((FaultData_IR2_REG[Graph_index%FaultData_Graph_size,Vc_index] >= FaultData_IR2_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_IR2_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_IR2_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) >= 0)
                        | (FaultData_IR2_REG[Graph_index%FaultData_Graph_size,Vc_index] <= FaultData_IR2_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_IR2_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_IR2_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) <= 0)):
                        Visibility = False
                        break
                if Visibility:
                    Graph[Graph_index][Va_index].append(Vb_index)

            else:
                for Vc_index in range(Vb_index+1,Va_index):
                    if((FaultData_IR2_REG[Graph_index%FaultData_Graph_size,Vc_index] >= FaultData_IR2_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_IR2_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_IR2_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) >= 0)
                        | (FaultData_IR2_REG[Graph_index%FaultData_Graph_size,Vc_index] <= FaultData_IR2_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_IR2_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_IR2_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) <= 0)):
                        Visibility = False
                        break
                if Visibility:
                    Graph[Graph_index][Va_index].append(Vb_index)

Graph_index_CUR += FaultData_Graph_size


# FaultData_Ba2
for Graph_index in range(Graph_index_CUR,Graph_index_CUR+FaultData_Graph_size):
    print("loading Graph_"+str(Graph_index)+" //...")
    for Va_index in range(Data_size):
        for Vb_index in range(Data_size):
            if Va_index==Vb_index:
                continue
            Visibility = True

            if Va_index < Vb_index:
                for Vc_index in range(Va_index+1,Vb_index):
                    if((FaultData_Ba2_REG[Graph_index%FaultData_Graph_size,Vc_index] >= FaultData_Ba2_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_Ba2_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_Ba2_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) >= 0)
                        | (FaultData_Ba2_REG[Graph_index%FaultData_Graph_size,Vc_index] <= FaultData_Ba2_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_Ba2_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_Ba2_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) <= 0)):
                        Visibility = False
                        break
                if Visibility:
                    Graph[Graph_index][Va_index].append(Vb_index)

            else:
                for Vc_index in range(Vb_index+1,Va_index):
                    if((FaultData_Ba2_REG[Graph_index%FaultData_Graph_size,Vc_index] >= FaultData_Ba2_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_Ba2_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_Ba2_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) >= 0)
                        | (FaultData_Ba2_REG[Graph_index%FaultData_Graph_size,Vc_index] <= FaultData_Ba2_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_Ba2_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_Ba2_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) <= 0)):
                        Visibility = False
                        break
                if Visibility:
                    Graph[Graph_index][Va_index].append(Vb_index)

Graph_index_CUR += FaultData_Graph_size


# FaultData_OR2
for Graph_index in range(Graph_index_CUR,Graph_index_CUR+FaultData_Graph_size):
    print("loading Graph_"+str(Graph_index)+" //...")
    for Va_index in range(Data_size):
        for Vb_index in range(Data_size):
            if Va_index==Vb_index:
                continue
            Visibility = True

            if Va_index < Vb_index:
                for Vc_index in range(Va_index+1,Vb_index):
                    if((FaultData_OR2_REG[Graph_index%FaultData_Graph_size,Vc_index] >= FaultData_OR2_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_OR2_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_OR2_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) >= 0)
                        | (FaultData_OR2_REG[Graph_index%FaultData_Graph_size,Vc_index] <= FaultData_OR2_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_OR2_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_OR2_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) <= 0)):
                        Visibility = False
                        break
                if Visibility:
                    Graph[Graph_index][Va_index].append(Vb_index)

            else:
                for Vc_index in range(Vb_index+1,Va_index):
                    if((FaultData_OR2_REG[Graph_index%FaultData_Graph_size,Vc_index] >= FaultData_OR2_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_OR2_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_OR2_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) >= 0)
                        | (FaultData_OR2_REG[Graph_index%FaultData_Graph_size,Vc_index] <= FaultData_OR2_REG[Graph_index%FaultData_Graph_size,Vb_index]
                        +(FaultData_OR2_REG[Graph_index%FaultData_Graph_size,Va_index]-FaultData_OR2_REG[Graph_index%FaultData_Graph_size,Vb_index])
                        *(float(Vb_index-Vc_index)/(Vb_index-Va_index)) <= 0)):
                        Visibility = False
                        break
                if Visibility:
                    Graph[Graph_index][Va_index].append(Vb_index)

Graph_index_CUR += FaultData_Graph_size




f_HVG = open("HVG.txt","w")
f_HVG.write(str(Graph_size)+"\n")
for Graph_index in range(Graph_size):
    if Graph_index < NormalData_Graph_size:
        Label = 0
    #For this sample from CWRU,IR0 IR1 IR2 are the same label
    else:
        Label = (Graph_index-NormalData_Graph_size)//FaultData_Graph_size
        Label %= 3
        Label += 1
        
    f_HVG.write(str(Data_size)+" "+str(Label)+"\n")
    
    for Node_index in range(Data_size):
        f_HVG.write("0 "+str(len(Graph[Graph_index][Node_index])))
        for Edge_index in range(len(Graph[Graph_index][Node_index])):
            f_HVG.write(" "+str(Graph[Graph_index][Node_index][Edge_index]))
        f_HVG.write("\n")
f_HVG.close()


