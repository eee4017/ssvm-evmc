#include <bits/stdc++.h>
#include "erc20.h"
using namespace std;

int main(){
  FILE *f = fopen("erc20.wasm", "wb");
  fwrite(erc20_wasm.data(), erc20_wasm.size(), 1, f);
  f = fopen("erc20-deploy.wasm", "wb");
  fwrite(erc20_deploy_wasm.data(), erc20_deploy_wasm.size(), 1, f);
}
