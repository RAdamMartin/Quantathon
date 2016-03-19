#include <fstream>
#include <sstream>
#include <string>
#include <iostream>

std::string getword(std::string str, int ind){
    std::string ret = "";
    for (int i = ind; i < str.length(); i++){
        if (str[i] == ','){
            break;
        }
        ret += str[i];
    }
    return ret;
}

int main() {
    std::ifstream infile("data.csv");
    //FILE * dst = fopen("clean.csv", 'w');
    
    std::string line;
    std::string date = "";
    std::getline(infile, line);

    while (std::getline(infile, line))
    {
        date = getword(line, 0);
        int i = date.length()+1;
        int ind = i;
        int count = 0;
        int first = 1;
        int id = 0;
        std::cout << date << ',' << (id+1) << ',';
        id ++;
        
        for (;i < line.length(); i++){
            if (line[i] == ','){
                std::cout << getword(line,ind+1) <<',';
                ind = i;
                count = (count+1)%(6+first);
                if (count == 0){
                    std::cout << '\n';
                    std::cout << date << ',' << (id+1) << ',';
                    id = (id+1)%100;
                }
                first = 0;
            }
        }
        
        i = 0;
        count = 0;
        std::cout << '\n';
        
    } 
}