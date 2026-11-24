#include <bits/stdc++.h>
using namespace std;
int pc(int x){return __builtin_popcount((unsigned)x);}
vector<int> S;int si[4096];vector<int> bs;vector<int> in[4096];vector<int> contain[310], bsub[792], ext[310];int l[310],u[310],f[310];int Q[12];int n=310; // empty, 12 vertices, 66 pairs, 220 triples =299; index dynamic
long long checks=0;
struct Eq{int lhs, mult; vector<int> rhs;};vector<Eq> eq;
int ceildiv(int a,int b){return a<=0?a/b:(a+b-1)/b;}
bool propagate(vector<int>& F,int y, bool matching, vector<int>& opts){
 int z=0;for(int i=0;i<14;i++)if(i!=13&&i!=y)Q[z++]=i;assert(z==12);memset(f,0,sizeof f);
 for(int b:F){int m=0;for(int i=0;i<12;i++)if(b>>Q[i]&1)m|=1<<i;for(int i:in[m])f[i]++;}
 // exact budget and regular degrees; bounds on pair and triple multiplicity.
 for(int i=0;i<n;i++){int k=pc(S[i]);if(k==0)l[i]=u[i]=42-(int)F.size();else if(k==1)l[i]=u[i]=15-f[i];else if(k==2)l[i]=max(0,4-f[i]),u[i]=5-f[i];else l[i]=max(0,1-f[i]),u[i]=3-f[i];if(u[i]<l[i]||u[i]<0)return false;}
 // Full point codegree-6 matching: if fixed complete-root pair already uses double at x, cap all other pairs through x.
 if(matching){for(int x=0;x<12;x++){int c1=0,c2=0;for(int b:F)if(b>>Q[x]&1){c1+=b>>13&1;c2+=b>>y&1;}if(c1==6||c2==6)for(int i:ext[si[1<<x]])if(pc(S[i])==2)u[i]=min(u[i],5-f[i]);}}
 vector<unsigned char> active(bs.size(),1),selected(bs.size(),0);bool change=true;
 for(int j=0;j<(int)bs.size();j++){int real=0;for(int x=0;x<12;x++)if(bs[j]>>x&1)real|=1<<Q[x];if(find(F.begin(),F.end(),real)!=F.end())active[j]=0;}
 auto lower=[&](int i,int x){if(x>l[i])l[i]=x,change=true;};auto upper=[&](int i,int x){if(x<u[i])u[i]=x,change=true;};
 while(change){change=false;checks++;
  for(int i=0;i<n;i++)if(l[i]>u[i]||u[i]<0)return false;
  // Matching condition among pairs not touching roots: if a pair is forced at 6, cap its incident competitors.
  if(matching){for(int i=0;i<n;i++)if(pc(S[i])==2&&f[i]+l[i]==6){for(int j=0;j<n;j++)if(j!=i&&pc(S[j])==2&&(S[i]&S[j]))upper(j,5-f[j]);}}
  for(auto &e:eq){int a=0,b=0;for(int j:e.rhs)a+=l[j],b+=u[j];lower(e.lhs,ceildiv(a,e.mult));upper(e.lhs,b/e.mult);for(int j:e.rhs){lower(j,e.mult*l[e.lhs]-b+u[j]);upper(j,e.mult*u[e.lhs]-a+l[j]);}}
  for(int i=0;i<n;i++)if(l[i]>u[i]||u[i]<0)return false;
  // All selected candidates must satisfy every tuple upper bound.
  for(int b=0;b<(int)bs.size();b++)if(active[b]){bool ok=true;for(int i:bsub[b])if(!u[i]){ok=false;break;}if(!ok){active[b]=0;change=true;}}
  // With each sum relation, a chosen block spends mult slots; at most slack slots can go to zero-lower entries.
  for(auto &e:eq){int a=0;for(int j:e.rhs)a+=l[j];int slack=e.mult*u[e.lhs]-a;if(slack<0)return false;if(slack>=e.mult)continue;for(int b:contain[e.lhs])if(active[b]){int waste=0;for(int j:bsub[b])if(pc(S[j])==pc(S[e.rhs[0]])&&(S[j]&S[e.lhs])==S[e.lhs]&&!l[j])waste++;if(waste>slack){active[b]=0;change=true;}}}
  // Sum of each tuple's residual candidate variables; force blocks when every candidate is needed.
  vector<int> forced;for(int i=0;i<n;i++){int cnt=0;for(int b:contain[i])cnt+=active[b];upper(i,cnt);if(l[i]>u[i])return false;if(l[i]&&l[i]==cnt)for(int b:contain[i])if(active[b])forced.push_back(b);}
  sort(forced.begin(),forced.end());forced.erase(unique(forced.begin(),forced.end()),forced.end());
  for(int b:forced){assert(active[b]);active[b]=0;selected[b]=1;change=true;int real=0;for(int x=0;x<12;x++)if(bs[b]>>x&1)real|=1<<Q[x];F.push_back(real);for(int i:bsub[b]){l[i]=max(0,l[i]-1);u[i]--;f[i]++;}}
  // f includes newly selected residual blocks, and all l,u now refer to yet-unselected blocks. Equations remain homogeneous.
  // Strong lower count using available maximum number of mandatory triples per block containing each tuple.
  for(int i=0;i<n;i++){int k=pc(S[i]);if(k>2)continue;int need=0;for(int j:ext[i])if(pc(S[j])==3)need+=l[j];if(!need)continue;int best=0;for(int b:contain[i])if(active[b]){int v=0;for(int j:bsub[b])if(pc(S[j])==3&&(S[j]&S[i])==S[i]&&l[j])v++;best=max(best,v);}if(!best)return false;lower(i,ceildiv(need,best));}
 }
 int pivot=-1,best=100000;for(int i=0;i<n;i++)if(l[i]>0){int k=0;for(int b:contain[i])k+=active[b];if(k<best){pivot=i;best=k;}}
 opts.clear();if(pivot>=0)for(int b:contain[pivot])if(active[b]){int real=0;for(int x=0;x<12;x++)if(bs[b]>>x&1)real|=1<<Q[x];opts.push_back(real);}
 return true;
}
long long nodes=0;bool timeout=false;auto start=chrono::steady_clock::now();
bool search(vector<int> F,int y,bool matching){if((++nodes&127)==0&&false){timeout=true;return false;}vector<int> opts;if(!propagate(F,y,matching,opts))return false;if(F.size()==42){set<int>T;for(int b:F)for(int s=b;s;s=(s-1)&b)if(pc(s)==3)T.insert(s);assert(T.size()==364&&set<int>(F.begin(),F.end()).size()==42);cout<<"COVER";for(int b:F)cout<<' '<<b;cout<<'\n';return true;}assert(!opts.empty());for(int b:opts){auto FF=F;FF.push_back(b);if(search(FF,y,matching))return true;if(timeout)return false;}return false;}
int main(int argc,char**argv){bool matching=argc>1;for(int k=0;k<=3;k++)for(int s=0;s<4096;s++)if(pc(s)==k){si[s]=S.size();S.push_back(s);}n=S.size();assert(n==299);for(int b=0;b<4096;b++){for(int i=0;i<n;i++)if((b&S[i])==S[i])in[b].push_back(i);if(pc(b)==5){int j=bs.size();bs.push_back(b);bsub[j]=in[b];for(int i:in[b])contain[i].push_back(j);}}for(int i=0;i<n;i++){for(int j=0;j<n;j++)if(j!=i&&(S[i]&S[j])==S[i])ext[i].push_back(j);int k=pc(S[i]);for(int q=k+1;q<=3;q++){Eq e;e.lhs=i;int a=5-k,b=q-k;int v=1;for(int t=1;t<=b;t++)v=v*(a-t+1)/t;e.mult=v;for(int j:ext[i])if(pc(S[j])==q)e.rhs.push_back(j);assert(!e.rhs.empty());eq.push_back(e);}}
 string line;int ix=0,ex=0;while(getline(cin,line)){if(line.rfind("SURV ",0)!=0)continue;istringstream ss(line);string h;int rep,y;ss>>h>>rep>>y;vector<int> F(25);for(int &b:F)ss>>b;assert(ss);bool open=search(F,y,matching);if(timeout){cout<<"TIMEOUT at "<<ix<<" nodes "<<nodes<<"\n";break;}if(open)cout<<"OPEN "<<ix<<' '<<line<<'\n';else ex++;ix++;}cout<<"TOTAL "<<ix<<" excluded "<<ex<<" unresolved "<<ix-ex<<" iterations "<<checks<<" nodes "<<nodes<<" timed "<<timeout<<'\n';}
