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


# basic_sstore = open('wasm/basic_sstore.wasm', 'rb').read()
basic_sstore = open('wasm/comparison_lt.wasm', 'rb').read()
print("-------------------------------------------------------")

calldata = unhexlify("")
sender = 0x0
destination = 0x7ffffffff
result_str, result = evmc_vm_execute(calldata, 0, destination, basic_sstore)
print(result_str)

print("-------------------------------------------------------")


for i in range(15):
    print(bytes_to_long(evmc_get_storage(destination, i)))
