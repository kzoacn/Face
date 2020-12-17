#include<bits/stdc++.h>
using namespace std;
const int maxn=20000;
vector<string>name;
vector<double>vec[maxn];


double dis(const vector<double>&vec1,const vector<double>&vec2){
    double s=0;
    for(int i=0;i<128;i+=4){
        double s1=abs(vec1[i]-vec2[i]);
        double s2=abs(vec1[i+1]-vec2[i+1]);
        double s3=abs(vec1[i+2]-vec2[i+2]);
        double s4=abs(vec1[i+3]-vec2[i+3]);

        s=max(s,max(max(s1,s2),max(s3,s4)));
    }
    return s;
}


double sqr(double x){return x*x;}
double dis2(const vector<double>&vec1,const vector<double>&vec2){
    double s=0;
    for(int i=0;i<128;i+=4){
        double s1=sqr(vec1[i]-vec2[i]);
        double s2=sqr(vec1[i+1]-vec2[i+1]);
        double s3=sqr(vec1[i+2]-vec2[i+2]);
        double s4=sqr(vec1[i+3]-vec2[i+3]);

        s+=s1;
        s+=s2;
        s+=s3;
        s+=s4;
    }
    return sqrt(s);
}

double dis1(const vector<double>&vec1,const vector<double>&vec2){
    double s=0;
    for(int i=0;i<128;i+=4){
        double s1=abs(vec1[i]-vec2[i]);
        double s2=abs(vec1[i+1]-vec2[i+1]);
        double s3=abs(vec1[i+2]-vec2[i+2]);
        double s4=abs(vec1[i+3]-vec2[i+3]);

        s+=s1;
        s+=s2;
        s+=s3;
        s+=s4;
    }
    return s;
}

string trim(string name){
    string n;
    for(int i=0;i<(int)name.length()-9;i++)
        n+=name[i];
    return n;
}



    double normalCDF(double x) // Phi(-∞, x) aka N(x)
{
    return std::erfc(-x/std::sqrt(2))/2;
}


 vector<double>same,diff;


void output(vector<double>s){
    static int cnt[6101];
    memset(cnt,0,sizeof(cnt));

    for(auto x:s){
        int t=(int)(min(max(x,0.0),100.0));
        //cout<<x<<" : "<<t<<" ";
        cnt[t]++;
    }
    for(int i=0;i<=100;i++)
        cout<<1.0*cnt[i]/s.size()<<",";
    cout<<endl;
}
int main(){
    ifstream fin("vec");
    string nm;
    int c=0;
    while(fin>>nm){
        name.push_back(trim(nm));
        vec[c].resize(128);
        for(int i=0;i<128;i++)
            fin>>vec[c][i];
        c++;
    }
 
    for(int j=0;j<128;j++){
        double sum=0,mean,std=0;
        for(int i=0;i<c;i++){
            sum+=vec[i][j];
        }
        sum/=c;
        for(int i=0;i<c;i++){
            vec[i][j]-=sum;
            std+=vec[i][j]*vec[i][j];
        }
        std=sqrt(std/c);
        for(int i=0;i<c;i++){
            vec[i][j]/=std;
        }
        //for(int i=0;i<c;i++){
        //    vec[i][j]=normalCDF(vec[i][j]);
        //}
    } 


    for(int T=0;T<1;T++){
        int all=0;
        int allyes=0,allno=0;
        int falseP=0,falseN=0;
        for(int i=0;i<c;i++)
        for(int j=i+1;j<c;j++){
            all++;
            bool flag=true;
            if(name[i]==name[j]){
                allyes++;
            }else{
                allno++;
                flag=false;
            }

            if(flag){
                same.push_back(dis2(vec[i],vec[j]));
            }else{
                diff.push_back(dis2(vec[i],vec[j]));

            }

            if(dis(vec[i],vec[j])<1.5){ 
                if(flag){

                }else{
                    falseP++;
                }
            }else{
                if(flag){
                    falseN++;
                }else{

                }
            }
            if(all % 100000==0){
                fprintf(stderr,"%d/%d falseP=%d/%d falseN=%d/%d\n",all,c*(c-1)/2,falseP,allno,falseN,allyes);
                fprintf(stderr,"%.8f%% %.8f%%\n",1.0*falseP/allno*100,1.0*falseN/allyes*100);
            }
        }
        fprintf(stderr,"%d/%d falseP=%d/%d falseN=%d/%d\n",all,c*(c-1)/2,falseP,allno,falseN,allyes);
        fprintf(stderr,"%.8f%% %.8f%%\n",1.0*falseP/allno*100,1.0*falseN/allyes*100);
    }
    output(same);
    output(diff);
}