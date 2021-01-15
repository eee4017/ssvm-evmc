#!/usr/bin/env python

import ctypes
from binascii import unhexlify
from evmc import *
import os, signal
from Crypto.Util.number import *

handle = ctypes.cdll.LoadLibrary('./libsoll_runtime_test.so')

def int_to_address(x):
    return ctypes.c_buffer(long_to_bytes(x).rjust(20, b'\x00'), size=20)

def int_to_bytes32(x):
    return ctypes.c_buffer(long_to_bytes(x).rjust(32, b'\x00'), size=32)

def evmc_vm_execute(calldata:bytes, sender:int, destination:int, wasm:bytes):
    _evmc_vm_execute = handle.evmc_vm_execute
    
    sender = int_to_address(sender)
    destination = int_to_address(destination)
    
    result = struct_evmc_result()
    _evmc_vm_execute( 
                    ctypes.cast(calldata, ctypes.c_char_p), 
                    len(calldata), 
                    ctypes.pointer(sender),
                    ctypes.pointer(destination),
                    ctypes.cast(wasm, ctypes.c_char_p), 
                    len(wasm), 
                    ctypes.pointer(result))
    
    return evmc_status_code__enumvalues[result.status_code], result

def evmc_vm_deploy(deploy_wasm:bytes):
    _evmc_vm_deploy = handle.evmc_vm_deploy

    result = struct_evmc_result()
    _evmc_vm_deploy(ctypes.cast(deploy_wasm, ctypes.c_char_p), 
                    len(deploy_wasm), 
                    ctypes.pointer(result))
    
    return evmc_status_code__enumvalues[result.status_code], result

def evmc_get_storage(address:int, key:int):
    _evmc_get_storage = handle.evmc_get_storage
    
    address = int_to_address(address)
    key = int_to_bytes32(key)
    result = int_to_bytes32(0)

    _evmc_get_storage(
                    ctypes.pointer(address), 
                    ctypes.pointer(key), 
                    ctypes.pointer(result))
    
    return bytes(result.raw)


# In[34]:

test_base = sys.argv[1]

print("-------------------------------------------------------")
basic_sstore = open(f'{test_base}.wasm', 'rb').read()

calldata = unhexlify("")
sender = 0x0
destination = 0x7ffffffff
result_str, result = evmc_vm_execute(calldata, 0, destination, basic_sstore)
print("evmc vm execute result:", result_str)

print("-------------------------------------------------------")


# In[26]:


storage_dump = dict()
with open(f'{test_base}.yul', 'r') as f:
    storage_dump_flag = False
    for line in f:
        if storage_dump_flag:
            _, key, value = line.split()
            key, value = int(key[:-1], 16), int(value, 16)
            storage_dump[key] = value
        if line.find('Storage dump:') != -1:
            storage_dump_flag = True


# In[33]:


print(f"checking evmc storage with expected {len(storage_dump)} testcases:", storage_dump)

for i, p in enumerate(storage_dump.items()):
    k, v = p
    execute_result = bytes_to_long(evmc_get_storage(destination, k))
    print(f"testcase-{i}:", v == execute_result)

print("-------------------------------------------------------")

# In[ ]:




