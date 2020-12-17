#include<bits/stdc++.h>
using namespace std;

typedef long long LL;

double dis(vector<double>v1,vector<double>v2){
    double s=0;
    for(int i=0;i<(int)v1.size();i++)
        s+=(v1[i]-v2[i])*(v1[i]-v2[i]);
    return sqrt(s);
}

double dismax(vector<double>v1,vector<double>v2){
    double s=0;
    for(int i=0;i<(int)v1.size();i++)
        s=max(abs(v1[i]-v2[i]),s);
    return s;
}

vector<double> sub(vector<double>v1,vector<double>v2){
    vector<double>v;
    for(int i=0;i<(int)v1.size();i++)
        v.push_back(v1[i]-v2[i]);
    return v;
}
vector<double> add(vector<double>v1,vector<double>v2){
    vector<double>v;
    for(int i=0;i<(int)v1.size();i++)
        v.push_back(v1[i]+v2[i]);
    return v;
}
vector<double> concat(vector<double>v1,vector<double>v2){
    vector<double>v=v1;
    for(int i=0;i<(int)v2.size();i++)
        v.push_back(v2[i]);
    return v;
}


vector<double> rot(vector<double>y,int t){
    vector<double>x;
    if(t==-1){
        for(int i=0;i<y.size();i+=2){
            x.push_back((y[i]+y[i+1])/2);
            x.push_back((y[i]-y[i+1])/2);
        }
    }else{
        for(int i=0;i<y.size();i+=2){
            x.push_back(y[i]+y[i+1]);
            x.push_back(y[i]-y[i+1]);
        }
    }
    return x;
}
 

long long round(double y,long long a){
    long long x=round(y);
    long long m=(x%a+a)%a;
    if(m<a/2)
        return x-m;
    else
        return x-m+a;    
}

long long scale=1;

vector<double>decode(vector<double>y,int t){


    vector<double>x;

    if(t==1){
        return rot(decode(rot(y,-1),0),1);
    }

    if(y.size()==2){
        x.push_back(round(y[0],scale));
        x.push_back(round(y[1],scale));
        return x;
    }

    vector<double>y1,y2;
    for(int i=0;i<(int)y.size()/2;i++)
        y1.push_back(y[i]);
    for(int i=(int)y.size()/2;i<(int)y.size();i++)
        y2.push_back(y[i]);
    auto u1=decode(y1,t);
    auto u2=decode(y2,t);

    auto v1=decode(sub(y1,u2),t^1);
    auto v2=decode(sub(y2,u1),t^1);

    auto x1=concat(u1,add(u1,v2));
    auto x2=concat(add(u2,v1),u2);

    double d1=dis(x1,y);
    double d2=dis(x2,y);
    if(d1<d2)
        return x1;
    else
        return x2;
}

const int maxn=20000;
vector<double>vec[maxn];
vector<string>name;


bool cmp(vector<double>c1,vector<double>c2){
    for(int i=0;i<(int)c1.size();i++){
        if(fabs(c1[i]-c2[i])>1e-7){
            return false;
        }
    }
    return true;
}

int cnt[3010];

void output(vector<double>same){
    memset(cnt,0,sizeof(cnt));
    double sum=0;
    for(int i=0;i<(int)same.size();i++){
        double x=same[i];
        sum+=x;
        cnt[(int)(min(x,3.0)*1000)]++;
    }   
    double avg=sum/same.size();
    double sigma=0;
    for(auto x:same){
        sigma+=(x-avg)*(x-avg);
    }
    sigma=sqrt(sigma/same.size());

    //cout<<avg << " "<<sigma<<endl;

    for(int i=0;i<=3000;i++)
        cout<<1.0*cnt[i]/same.size()<<",";
    cout<<endl;
}

int main(){
    int n=128;
    double t=0.2;

    scale=t*(1LL<<31)/(sqrt(n)/2)+1;

    ifstream fin("caisa");
    string na;
    int cc=0;
    while(fin>>na){
        name.push_back(na.substr(0,na.size()-1));
        vec[cc].resize(128);
        for(int i=0;i<128;i++){
            double x;
            fin>>x;
            vec[cc][i]=x;//min(max(x+1,0.0),2.0)*(1LL<<31);
        }
        cc++;
    }


    int allyes=0,allno=0,falseP=0,falseN=0;

    int all=name.size()*(name.size()-1)/2;
    int cnt=0;

    vector<double>diff,same;
    vector<pair<string,string> >black;
    for(int i=0;i<(int)name.size();i++){
          //  auto v=decode(vec[i],0);
           // auto e=sub(v,vec[i]);
        for(int j=i+1;j<name.size();j++){

            bool flag;
            if(name[i]==name[j]){
                flag=true;
                allyes++;
            }else{
                flag=false;
                allno++;
            }

            //auto v2=decode(add(vec[j],e),0);

            
            if(flag){
                same.push_back(dis(vec[i],vec[j]));
            }else{
                diff.push_back(dis(vec[i],vec[j]));
            }
            
            if(dismax(vec[i],vec[j])<0.05/*cmp(v,v2)*/){
                if(!flag){
                    falseP++;
                    //cout<<name[i]<<" "<<name[j]<<endl;
                    black.push_back(make_pair(name[i],name[j]));
                }
            }else{
                if(flag)
                    falseN++;
            }

            if(++cnt%1000==0){
                fprintf(stderr,"%.5f\n",1.0*cnt/all*100);
                fprintf(stderr,"%.9f %.9f\n",1.0*falseP/allno*100,1.0*falseN/allyes*100);
            }
        }
    }


    for(auto p : black){
        cout<<p.first<<" "<<p.second<<endl;
    }

    //output(same);
    //output(diff);


    return 0;
}