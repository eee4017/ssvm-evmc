#include "evmc/evmc.hpp"
#include "evmc/loader.h"

#include "example_host.h"

#include <cassert>
#include <cstring>
#include <iostream>
#include <bits/stdc++.h>

typedef unsigned char * bytes;

const char *evmc_library = "./libssvm-evmc.so";
evmc_host_context *context;
const evmc_host_interface *host_interface;

extern "C"{

__attribute__((constructor))
void vm_constructor(){
  context = example_host_create_context(evmc_tx_context{});
  host_interface = example_host_get_interface();
}

void evmc_vm_deploy(bytes deploy_wasm, size_t deploy_wasm_size, evmc_result *result){
  enum evmc_loader_error_code err;
  struct evmc_vm *vm = evmc_load_and_create(evmc_library, &err);
  assert( (err == EVMC_LOADER_SUCCESS) && "Initialize evmc failed" );

  evmc::address sender({0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                        0x00, 0x00, 0x7f, 0xff, 0xff, 0xff});
  evmc::address destination = {};
  int64_t gas = 999999;
  evmc::uint256be value = {};
  evmc_bytes32 create2_salt = {};

  evmc_message msg{EVMC_CALL,
                   0,
                   0,
                   gas,
                   destination,
                   sender,
                   deploy_wasm,
                   deploy_wasm_size,
                   value,
                   create2_salt};
  *result =
      vm->execute(vm, host_interface, context, EVMC_MAX_REVISION, &msg,
                  deploy_wasm, deploy_wasm_size);

#ifdef DEBUG
  printf("%d, %lld, %p\n", result->status_code, result->gas_left, result->output_data);
  for(int i = 0;i < result->output_size; i++) printf("%x", result->output_data[i]); printf("\n");
#endif
}

evmc::address string_to_address(std::string SenderStr) {
  evmc::address address;
  std::vector<uint8_t> Sender;
  SSVM::Support::convertHexStrToBytes(SenderStr, Sender);
  for (int i = 0; i < 20; i++) {
    address.bytes[i] = Sender[i];
  }
  return address;
}

evmc::address bytes_to_address(bytes SenderStr) {
  evmc::address address;
  for (int i = 0; i < 20; i++) {
    address.bytes[i] = SenderStr[i];
  }
  return address;
}

void evmc_vm_execute(bytes calldata, size_t calldata_size, bytes SenderStr, bytes wasm, size_t wasm_size, evmc_result *result) {
#ifdef DEBUG
  printf("%p, %d, %p, %p, %d, %p\n", calldata, calldata_size, SenderStr, wasm, wasm_size, result);
  for(int i = 0;i < calldata_size; i++) printf("%x", calldata[i]); printf("\n");
  for(int i = 0;i < 32; i++) printf("%x", SenderStr[i]); printf("\n");
#endif

  evmc::address sender = bytes_to_address(SenderStr);

  enum evmc_loader_error_code err;
  struct evmc_vm *vm = evmc_load_and_create(evmc_library, &err);
  evmc::address destination = {};
  int64_t gas = 999999;
  evmc::uint256be value = {};
  evmc_bytes32 create2_salt = {};

  evmc_message msg{EVMC_CALL,
                   0,
                   0,
                   gas,
                   destination,
                   sender,
                   calldata,
                   calldata_size,
                   value,
                   create2_salt};
  *result =
      vm->execute(vm, host_interface, context, EVMC_MAX_REVISION, &msg,
                  wasm, wasm_size);

#ifdef DEBUG
  printf("%d, %lld, %p\n", result->status_code, result->gas_left, result->output_data);
  for(int i = 0;i < result->output_size; i++) printf("%x", result->output_data[i]); printf("\n");
#endif
}

}