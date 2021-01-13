import ctypes
from binascii import unhexlify
from evmc import *
import os, signal


handle = ctypes.cdll.LoadLibrary('./libsoll_runtime_test.so')

def evmc_vm_execute(calldata:bytes, sender:bytes, wasm:bytes):
    _evmc_vm_execute = handle.evmc_vm_execute

    result = struct_evmc_result()
    _evmc_vm_execute( 
                    ctypes.cast(calldata, ctypes.c_char_p), 
                    len(calldata), 
                    ctypes.cast(sender, ctypes.c_char_p), 
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


_, result = evmc_vm_deploy(open('wasm/erc20-deploy.wasm', 'rb').read())
print(_)


erc20 = open('wasm/erc20.wasm', 'rb').read()
calldata = unhexlify("70a08231" + "000000000000000000000000000000000000000000000000000000007fffffff")
sender = unhexlify("000000000000000000000000000000007fffffff")

_, result = evmc_vm_execute(calldata, sender, erc20)
buffer = ctypes.cast(result.output_data, ctypes.POINTER(ctypes.c_byte * 32))
print(bytearray(buffer.contents))
