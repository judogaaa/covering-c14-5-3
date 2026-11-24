// Second residual verifier. Independent state representation and branching.
// No numerical solver. All selected and forbidden candidates are retained in
// bitsets across recursion; the interval rules are derived from exact counts.
#include <algorithm>
#include <array>
#include <bitset>
#include <cassert>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
using namespace std;
constexpr int K=792, R=299;
using Bits=bitset<K>;
int pc(int m){return __builtin_popcount((unsigned)m);}
vector<int> tuplemask,blockmask;
int id[4096];
array<Bits,R> has;
array<vector<int>,K> sub;
struct Identity {int s, mult; vector<int> t;};
vector<Identity> identities;
array<vector<int>,R> triples;
long long nodes=0, rounds=0;
struct State {Bits possible,chosen; array<int,R> lo,hi;};
int choose(int n,int k){int v=1;for(int j=1;j<=k;j++)v=v*(n-j+1)/j;return v;}
void init(){
 for(int k=0;k<=3;k++)for(int m=0;m<4096;m++)if(pc(m)==k){id[m]=tuplemask.size();tuplemask.push_back(m);}
 assert(tuplemask.size()==R);
 for(int b=0;b<4096;b++)if(pc(b)==5){int j=blockmask.size();blockmask.push_back(b);for(int i=0;i<R;i++)if((b&tuplemask[i])==tuplemask[i]){has[i].set(j);sub[j].push_back(i);}}
 assert(blockmask.size()==K);
 for(int i=0;i<R;i++)for(int k=pc(tuplemask[i])+1;k<=3;k++){
   Identity e{i,choose(5-pc(tuplemask[i]),k-pc(tuplemask[i])),{}};
   for(int j=0;j<R;j++)if(pc(tuplemask[j])==k&&(tuplemask[j]&tuplemask[i])==tuplemask[i])e.t.push_back(j);
   if(k==3)triples[i]=e.t;
   identities.push_back(move(e));
 }
}
// Bounds refer to the ENTIRE residual solution, not only unselected blocks.
// This differs from the original program, which decrements counts on selection.
bool reduce(State &s,const array<int,R>& fixed,bool matching){
 while(true){++rounds;bool changed=false;
  auto lower=[&](int i,int v){if(v>s.lo[i]){s.lo[i]=v;changed=true;}};
  auto upper=[&](int i,int v){if(v<s.hi[i]){s.hi[i]=v;changed=true;}};
  if((s.chosen&~s.possible).any())return false;
  for(int i=0;i<R;i++){
   int a=(s.chosen&has[i]).count(), b=(s.possible&has[i]).count();
   lower(i,a);upper(i,b);if(s.lo[i]>s.hi[i])return false;
   if(s.hi[i]==a){Bits old=s.possible;s.possible&=~(has[i]&~s.chosen);changed|=(old!=s.possible);}
   if(s.lo[i]==b){Bits old=s.chosen;s.chosen|=s.possible&has[i];changed|=(old!=s.chosen);}
  }
  if((s.chosen&~s.possible).any())return false;
  // Each equation is propagated using a snapshot of its old bounds.
  for(const auto &e:identities){int L=0,U=0;for(int j:e.t){L+=s.lo[j];U+=s.hi[j];}
   lower(e.s,(L+e.mult-1)/e.mult);upper(e.s,U/e.mult);if(s.lo[e.s]>s.hi[e.s])return false;
   for(int j:e.t){int a=s.lo[j],b=s.hi[j];lower(j,e.mult*s.lo[e.s]-(U-b));upper(j,e.mult*s.hi[e.s]-(L-a));if(s.lo[j]>s.hi[j])return false;}
  }
  if(matching)for(int i=13;i<79;i++)if(fixed[i]+s.lo[i]==6){for(int j=13;j<79;j++)if(j!=i&&(tuplemask[i]&tuplemask[j])){upper(j,5-fixed[j]);if(s.lo[j]>s.hi[j])return false;}}
  Bits undecided=s.possible&~s.chosen;
  // Exact equation slack: additional selected blocks cannot spend too many
  // incidences on terms whose required lower bound is already satisfied.
  for(const auto &e:identities){int selected=(s.chosen&has[e.s]).count();int L=0;array<bool,R> done{};
   for(int j:e.t){int a=(s.chosen&has[j]).count();int req=max(0,s.lo[j]-a);L+=req;done[j]=req==0;}
   int slack=e.mult*(s.hi[e.s]-selected)-L;if(slack<0)return false;if(slack>=e.mult)continue;
   Bits test=undecided&has[e.s];for(int b=0;b<K;b++)if(test[b]){int waste=0;for(int j:sub[b])if(done[j])++waste;if(waste>slack){s.possible.reset(b);changed=true;}}
  }
  // A direct lower bound on the number of undecided blocks needed to
  // provide the outstanding required triple incidences.
  undecided=s.possible&~s.chosen;
  for(int i=0;i<79;i++){int need=0;array<bool,R> outstanding{};
   for(int j:triples[i]){int r=max(0,s.lo[j]-(int)(s.chosen&has[j]).count());need+=r;outstanding[j]=r>0;}
   if(!need)continue;
   int best=0;Bits test=undecided&has[i];for(int b=0;b<K;b++)if(test[b]){int v=0;for(int j:sub[b])v+=outstanding[j];best=max(best,v);}
   if(!best)return false;
   lower(i,(s.chosen&has[i]).count()+(need+best-1)/best);if(s.lo[i]>s.hi[i])return false;
  }
  if(!changed)return true;
 }
}
bool dfs(State s,const array<int,R>& fixed,bool matching){
 ++nodes;if(!reduce(s,fixed,matching))return false;
 if(s.chosen.count()==(size_t)s.lo[0]){
  for(int i=0;i<R;i++){int n=(s.chosen&has[i]).count();if(n<s.lo[i]||n>s.hi[i])return false;}
  return true;
 }
 Bits avail=s.possible&~s.chosen;int pivot=-1;size_t best=K+1;
 for(int i=0;i<R;i++)if((int)(s.chosen&has[i]).count()<s.lo[i]){size_t v=(avail&has[i]).count();if(v<best){best=v;pivot=i;}}
 assert(pivot>=0&&best>0);Bits cand=avail&has[pivot];
 // Disjoint branches: choose the first selected candidate in pivot order.
 // A solution must contain at least one of them.
 for(int j=0;j<K;j++)if(cand[j]){State t=s;t.chosen.set(j);if(dfs(t,fixed,matching))return true;s.possible.reset(j);}
 return false;
}
int main(int argc,char**argv){assert(argc==2);string mode=argv[1];assert(mode=="matching"||mode=="simple");bool matching=mode=="matching";int budget=matching?18:17;init();string line;int count=0;
 while(getline(cin,line)){if(line.rfind("SURV ",0)!=0)continue;istringstream ss(line);string tag;int rep,y;ss>>tag>>rep>>y;assert(y>=0&&y<13);vector<int> F(42-budget);for(auto &b:F){ss>>b;assert(b>0&&b<16384&&pc(b)==5&&(b&(1<<13|1<<y)));}assert(ss);string extra;assert(!(ss>>extra));auto copy=F;sort(copy.begin(),copy.end());assert(unique(copy.begin(),copy.end())==copy.end());
  // Independently verify both root links and all initial constraints.
  int deg[14]={},pair[14][14]={},tri[14][14][14]={};for(int b:F)for(int a=0;a<14;a++)if(b>>a&1){deg[a]++;for(int c=a+1;c<14;c++)if(b>>c&1){pair[a][c]++;for(int d=c+1;d<14;d++)if(b>>d&1)tri[a][c][d]++;}}
  assert(deg[13]==15&&deg[y]==15);
  for(int a=0;a<14;a++){assert(deg[a]<=15);for(int c=a+1;c<14;c++){assert(pair[a][c]<=(matching?6:5));if(a==y||c==y||c==13)assert(pair[a][c]>=4);for(int d=c+1;d<14;d++){assert(tri[a][c][d]<=(matching?4:3));if(d==13||a==y||c==y||d==y)assert(tri[a][c][d]>=1);}}}
  vector<int> q;for(int a=0;a<13;a++)if(a!=y)q.push_back(a);assert(q.size()==12);
  array<int,R> fixed{};for(int i=0;i<R;i++){int mask=0;for(int j=0;j<12;j++)if(tuplemask[i]>>j&1)mask|=1<<q[j];for(int b:F)fixed[i]+=(b&mask)==mask;}
  State s;s.possible.set();for(int i=0;i<R;i++){int k=pc(tuplemask[i]);int lo=k==0?42:k==1?15:k==2?4:1;int hi=k==0?42:k==1?15:k==2?(matching?6:5):(matching?4:3);s.lo[i]=max(0,lo-fixed[i]);s.hi[i]=hi-fixed[i];}
  if(matching)for(int i=0;i<12;i++){int a=q[i];if(pair[a][13]==6||pair[min(a,y)][max(a,y)]==6)for(int j=13;j<79;j++)if(tuplemask[j]>>i&1)s.hi[j]=min(s.hi[j],5-fixed[j]);}
  if(dfs(s,fixed,matching)){cout<<"UNRESOLVED case "<<count<<" rep "<<rep<<endl;return 1;}++count;
  if(count%100==0)cerr<<mode<<" checked "<<count<<" nodes "<<nodes<<endl;
 }
 cout<<"PASS "<<mode<<" cases "<<count<<" nodes "<<nodes<<" rounds "<<rounds<<endl;
}
