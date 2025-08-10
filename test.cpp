#include <bits/stdc++.h>
using namespace std;

struct comparitor{
    bool operator()(pair<int,int> a,pair<int,int> b){
        return a.second < b.second;
    }
};

int main(){
    priority_queue<pair<int,int>,vector<pair<int,int>>,comparitor> pq;

    pq.push({1,1});
    pq.push({1,2});
    pq.push({1,3});


    while(pq.size()){
        auto temp = pq.top();
        cout << temp.first << " " << temp.second << endl;
        pq.pop();
    }

}