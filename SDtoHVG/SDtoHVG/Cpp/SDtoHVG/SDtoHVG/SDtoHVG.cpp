#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <string.h>
#include <mat.h>

#include <windows.h>//t

using namespace std;

#define FaultData_Label_NUM  9
#define NormalDataset_size  102400
#define FaultDataset_size  102400
#define Dataset_size 102400
#define Data_size  1024

int Graph_index = 0;
int Graph_index_CUR = 0;
int EveryData_Graph_NUM = (NormalDataset_size / Data_size);
int Graph_index_total = ((NormalDataset_size + (FaultDataset_size * FaultData_Label_NUM)) / Data_size);
static bool Graph[((NormalDataset_size + (FaultDataset_size * FaultData_Label_NUM)) / Data_size)][Data_size][Data_size] = {false};
/*
 *Tips：
 *此处HVG图存储结构Graph为一个bool型1000*1024*1024容量的三维数组。
 *对应配置的[项目->属性->链接器->系统->堆栈保留大小]的值为[1,073,741,824]。
 *这种存储方法仅为了以空间换时间，在空间的角度上是十分不明智的。
 *若需要更大的HVG图容量或者受到运行系统的空间限制导致异常时，可考虑：
 *	1.采用稀疏矩阵、链表等存储结构实现HVG图的存储。(对于HVG图，其必定稀疏，但对于普通VG图，并不确定其是否稀疏)
 *	2.对Graph数组降维，并在完全生成每一个图后都进行一次文件写入然后清空Graph。
 */


void LoadMatData(string FilePath, string MatrixName, double Data_REG[]) {
    MATFile *pMatFile = NULL;
	mxArray *pMxArray = NULL;
	double *matdata;

    pMatFile = matOpen(FilePath.c_str(), "r");  
    if (pMatFile == NULL)
    {
        printf("FilePath is error!");
        return;
    }

    pMxArray = matGetVariable(pMatFile, MatrixName.c_str());
	matdata = (double*) mxGetData(pMxArray);
	matClose(pMatFile);

    for(int i=0; i<Dataset_size;i++){
		Data_REG[i] = double(matdata[i]);
    }

	mxDestroyArray(pMxArray);
	matdata = NULL;
	
	return;
}


void ToHVG(double Data_REG[]) {
	for (Graph_index = Graph_index_CUR; Graph_index < Graph_index_CUR + Dataset_size / Data_size; Graph_index++) {
		printf("loading Graph_[%d/%d]...\n", Graph_index + 1, Graph_index_total);

		int Va_index, Vb_index, Vc_index;
		bool Visibility;

		for (Va_index = 0; Va_index < Data_size; Va_index++) {
			for (Vb_index = 0; Vb_index < Data_size; Vb_index++) {
				if (Va_index == Vb_index) {
					continue;
				}

				Visibility = true;

				if ((abs(Data_REG[Va_index + ((Graph_index%EveryData_Graph_NUM)*Data_size)]) <= abs(Data_REG[Vb_index + ((Graph_index%EveryData_Graph_NUM)*Data_size)]))
					&& (Data_REG[Va_index + ((Graph_index%EveryData_Graph_NUM)*Data_size)] * Data_REG[Vb_index + ((Graph_index%EveryData_Graph_NUM)*Data_size)] > 0)) {
					if (Va_index < Vb_index) {
						for (Vc_index = Va_index + 1; Vc_index < Vb_index; Vc_index++) {
							if (((Data_REG[Vc_index + ((Graph_index%EveryData_Graph_NUM)*Data_size)] >= Data_REG[Va_index + ((Graph_index%EveryData_Graph_NUM)*Data_size)])
								&& (Data_REG[Va_index + ((Graph_index%EveryData_Graph_NUM)*Data_size)] > 0))
								|| ((Data_REG[Vc_index + ((Graph_index%EveryData_Graph_NUM)*Data_size)] <= Data_REG[Va_index + ((Graph_index%EveryData_Graph_NUM)*Data_size)])
								&& (Data_REG[Va_index + ((Graph_index%EveryData_Graph_NUM)*Data_size)] < 0))) {

								Visibility = false;
								break;
							}
						}
						if (Visibility) {
							Graph[Graph_index][Va_index][Vb_index] = true;
						}
					}

					else {
						for (Vc_index = Vb_index + 1; Vc_index < Va_index; Vc_index++) {
							if (((Data_REG[Vc_index + ((Graph_index%EveryData_Graph_NUM)*Data_size)] >= Data_REG[Va_index + ((Graph_index%EveryData_Graph_NUM)*Data_size)])
								&& (Data_REG[Va_index + ((Graph_index%EveryData_Graph_NUM)*Data_size)] > 0))
								|| ((Data_REG[Vc_index + ((Graph_index%EveryData_Graph_NUM)*Data_size)] <= Data_REG[Va_index + ((Graph_index%EveryData_Graph_NUM)*Data_size)])
								&& (Data_REG[Va_index + ((Graph_index %EveryData_Graph_NUM)*Data_size)] < 0))) {

								Visibility = false;
								break;
							}
						}
						if (Visibility) {
							Graph[Graph_index][Va_index][Vb_index] = true;
						}
					}
				}
			}
		}
	}
	Graph_index_CUR += Dataset_size / Data_size;
}


int Graph_Length(int index_CUR, int node_A, int node_B_Temp[]) {
	int Len = 0;
	for (int node_B = 0; node_B < Data_size; node_B++) {
		if (Graph[index_CUR][node_A][node_B]) {
			node_B_Temp[Len] = node_B;
			Len++;
		}
	}
	return Len;
}


void Output_HVGraph() {
	int Graph_index_CUR, Label;
	int Temp[Data_size];

	fstream file;
	file.open("HVG.txt", ios::out);
	file << Graph_index_total << endl;

	for (Graph_index_CUR = 0; Graph_index_CUR < Graph_index_total; Graph_index_CUR++) {
		if (Graph_index_CUR < (Dataset_size / Data_size)) {
			Label = 0;
		}
		else {
			Label = ((Graph_index_CUR - (Dataset_size / Data_size)) / (Dataset_size / Data_size));
			Label %= 3;
			Label += 1;
		}

		file << Data_size << " " << Label << endl;

		int Node_A, Node_B, Len;
		for (Node_A = 0; Node_A < Data_size; Node_A++) {
			Len = Graph_Length(Graph_index_CUR, Node_A, Temp);
			file << "0 " << Len;
			for (Node_B = 0; Node_B < Len; Node_B++) {
				file << " " << Temp[Node_B];
			}
			file << endl;
		}
	}

	file.close();

	return;
}



int main(){
	static double NormalData_REG[102400] = { 0 };
	static double FaultData_IR0_REG[102400] = { 0 };
	static double FaultData_Ba0_REG[102400] = { 0 };
	static double FaultData_OR0_REG[102400] = { 0 };
	static double FaultData_IR1_REG[102400] = { 0 };
	static double FaultData_Ba1_REG[102400] = { 0 };
	static double FaultData_OR1_REG[102400] = { 0 };
	static double FaultData_IR2_REG[102400] = { 0 };
	static double FaultData_Ba2_REG[102400] = { 0 };
	static double FaultData_OR2_REG[102400] = { 0 };

	LoadMatData("data/Normal.mat","X097_DE_time", NormalData_REG);
	LoadMatData("data/Fault_IR0.mat", "X105_DE_time", FaultData_IR0_REG);
	LoadMatData("data/Fault_Ba0.mat", "X118_DE_time", FaultData_Ba0_REG);
	LoadMatData("data/Fault_OR0.mat", "X130_DE_time", FaultData_OR0_REG);
	LoadMatData("data/Fault_IR1.mat", "X106_DE_time", FaultData_IR1_REG);
	LoadMatData("data/Fault_Ba1.mat", "X119_DE_time", FaultData_Ba1_REG);
	LoadMatData("data/Fault_OR1.mat", "X131_DE_time", FaultData_OR1_REG);
	LoadMatData("data/Fault_IR2.mat", "X107_DE_time", FaultData_IR2_REG);
	LoadMatData("data/Fault_Ba2.mat", "X120_DE_time", FaultData_Ba2_REG);
	LoadMatData("data/Fault_OR2.mat", "X132_DE_time", FaultData_OR2_REG);

	ToHVG(NormalData_REG);
	ToHVG(FaultData_IR0_REG);
	ToHVG(FaultData_Ba0_REG);
	ToHVG(FaultData_OR0_REG);
	ToHVG(FaultData_IR1_REG);
	ToHVG(FaultData_Ba1_REG);
	ToHVG(FaultData_OR1_REG);
	ToHVG(FaultData_IR2_REG);
	ToHVG(FaultData_Ba2_REG);
	ToHVG(FaultData_OR2_REG);
	
	Output_HVGraph();
	
	return 0;
}

