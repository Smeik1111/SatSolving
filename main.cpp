#include <iostream>
#include <string>
#include <fstream>
#include <bits/stdc++.h>
#include <string.h>
using namespace std;

int main() 
{
  cout << "Enter Path and Name of col File: ";
  string fileName;
  string line;
  string subStr;
  int numEdges = 0;
  int numNodes = 0;
  getline(cin, fileName);
  ifstream myfile (fileName);
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
  }

  else cout << "Unable to open file"; 


  //void* s = ipasir_init();
}
