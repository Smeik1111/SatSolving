#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <vector>
#include <signal.h>
#include <unistd.h>
#include <iostream>
#include <string>
#include <fstream>
#include <bits/stdc++.h>
#include <string.h>
#include <unistd.h> // For Unix-based systems
//#include <direct.h> // For Windows
using namespace std;

extern "C" {
	#include "ipasir.h"
}


int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <file_path>" << std::endl;
        return 1;
    }
	string relativeFilePath = argv[1];
	char currentDir[FILENAME_MAX];
    if (getcwd(currentDir, FILENAME_MAX) != nullptr) {
        string fullPath = string(currentDir) + "/" + relativeFilePath;
  	string line;
	string subStr;
	int numEdges = 0;
	int numNodes = 0;
	cout << fullPath << '\n';
	ifstream myfile (fullPath);
	if (myfile.is_open())
	{
    while (getline(myfile,line) && !line.rfind("p",0) == 0) 
    {
       cout << line << '\n';
    }
    stringstream ss(line);
    while (getline(ss,subStr , ' ')) {
        if(regex_match(subStr, std::regex("[(-|+)|][0-9]+"))) {
            if(numNodes == 0) {
                numNodes = stoi(subStr);
            } else {
                numEdges = stoi(subStr);
            }
        }
    }
    int edgesFrom[numEdges] = {0};
    int edgesTo[numEdges] = {0};
    for(int i = 0; i < numEdges;i++) {
        getline(myfile,line);
        stringstream ss(line);
        getline(ss,subStr , ' ');
        getline(ss,subStr , ' ');
        edgesFrom[i] = stoi(subStr);
        getline(ss,subStr , ' ');
        edgesTo[i] = stoi(subStr); 
    }
    cout << line << '\n';
    myfile.close();

	//solver (numNodes, edgesFrom, edgesTo):
	void *solver = ipasir_init();
	vector<int> assumptions;
	bool solved = false;
	int colors = 0;
	while(!solved) {
		//disable old assumptions
		for(uint i = 0; i < assumptions.size();i++) {
			ipasir_assume(solver, assumptions[i]);
		}
		//add color
		colors++;
		int assumption_literal = (numNodes+1)*colors;
		assumptions.push_back(assumption_literal);
		ipasir_assume(solver, -assumption_literal);
			//disallow all colors 0 per Nodes
		for(int node = 1; node <= numNodes; node++) {
			for(int color = 0; color < colors; color++) {
				int literal = -(node+((numNodes+1)*color));
				ipasir_add(solver, literal);
			}
			ipasir_add(solver, assumption_literal);
			ipasir_add(solver, 0);
		}
			//add edges for color
		for(int edge = 0; edge < numEdges;edge++) {
			ipasir_add(solver, edgesFrom[edge]+(numNodes+1)*(colors-1));
			ipasir_add(solver, edgesTo[edge]+(numNodes+1)*(colors-1));
			ipasir_add(solver, 0);
		}
		//solve
		int res = ipasir_solve(solver);
		if (res == 20) {
			solved = false;
		}else if (res == 0) {
			solved = false;
			//solver interupted
		}else {
			solved = true;
			printf("Ipasir returned %i\n", res);
			printf("Solved Graph with %i Colors\n", colors);
		}
	}
  }
  else cout << "Unable to open file\n"; 
}
}

