# -*- coding: utf-8 -*-
#
# TARGET arch is: []
# WORD_SIZE is: 8
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 16
#
import ctypes


# if local wordsize is same as target, keep ctypes pointer function.
if ctypes.sizeof(ctypes.c_void_p) == 8:
    POINTER_T = ctypes.POINTER
else:
    # required to access _ctypes
    import _ctypes
    # Emulate a pointer class using the approriate c_int32/c_int64 type
    # The new class should have :
    # ['__module__', 'from_param', '_type_', '__dict__', '__weakref__', '__doc__']
    # but the class should be submitted to a unique instance for each base type
    # to that if A == B, POINTER_T(A) == POINTER_T(B)
    ctypes._pointer_t_type_cache = {}
    def POINTER_T(pointee):
        # a pointer should have the same length as LONG
        fake_ptr_base_type = ctypes.c_uint64 
        # specific case for c_void_p
        if pointee is None: # VOID pointer type. c_void_p.
            pointee = type(None) # ctypes.c_void_p # ctypes.c_ulong
            clsname = 'c_void'
        else:
            clsname = pointee.__name__
        if clsname in ctypes._pointer_t_type_cache:
            return ctypes._pointer_t_type_cache[clsname]
        # make template
        class _T(_ctypes._SimpleCData,):
            _type_ = 'L'
            _subtype_ = pointee
            def _sub_addr_(self):
                return self.value
            def __repr__(self):
                return '%s(%d)'%(clsname, self.value)
            def contents(self):
                raise TypeError('This is not a ctypes pointer.')
            def __init__(self, **args):
                raise TypeError('This is not a ctypes pointer. It is not instanciable.')
        _class = type('LP_%d_%s'%(8, clsname), (_T,),{}) 
        ctypes._pointer_t_type_cache[clsname] = _class
        return _class

c_int128 = ctypes.c_ubyte*16
c_uint128 = c_int128
void = None
if ctypes.sizeof(ctypes.c_longdouble) == 16:
    c_long_double_t = ctypes.c_longdouble
else:
    c_long_double_t = ctypes.c_ubyte*16




# values for enumeration 'c__Ea_EVMC_ABI_VERSION'
c__Ea_EVMC_ABI_VERSION__enumvalues = {
    7: 'EVMC_ABI_VERSION',
}
EVMC_ABI_VERSION = 7
c__Ea_EVMC_ABI_VERSION = ctypes.c_int # enum
class struct_evmc_bytes32(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('bytes', ctypes.c_ubyte * 32),
     ]

evmc_bytes32 = struct_evmc_bytes32
evmc_uint256be = struct_evmc_bytes32
class struct_evmc_address(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('bytes', ctypes.c_ubyte * 20),
     ]

evmc_address = struct_evmc_address

# values for enumeration 'evmc_call_kind'
evmc_call_kind__enumvalues = {
    0: 'EVMC_CALL',
    1: 'EVMC_DELEGATECALL',
    2: 'EVMC_CALLCODE',
    3: 'EVMC_CREATE',
    4: 'EVMC_CREATE2',
}
EVMC_CALL = 0
EVMC_DELEGATECALL = 1
EVMC_CALLCODE = 2
EVMC_CREATE = 3
EVMC_CREATE2 = 4
evmc_call_kind = ctypes.c_int # enum

# values for enumeration 'evmc_flags'
evmc_flags__enumvalues = {
    1: 'EVMC_STATIC',
}
EVMC_STATIC = 1
evmc_flags = ctypes.c_int # enum
class struct_evmc_message(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('PADDING_0', ctypes.c_ubyte),
     ]

class struct_evmc_tx_context(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('tx_gas_price', evmc_uint256be),
    ('tx_origin', evmc_address),
    ('block_coinbase', evmc_address),
    ('block_number', ctypes.c_int64),
    ('block_timestamp', ctypes.c_int64),
    ('block_gas_limit', ctypes.c_int64),
    ('block_difficulty', evmc_uint256be),
    ('chain_id', evmc_uint256be),
     ]

class struct_evmc_host_context(ctypes.Structure):
    pass

evmc_get_tx_context_fn = POINTER_T(ctypes.CFUNCTYPE(struct_evmc_tx_context, POINTER_T(struct_evmc_host_context)))
evmc_get_block_hash_fn = POINTER_T(ctypes.CFUNCTYPE(struct_evmc_bytes32, POINTER_T(struct_evmc_host_context), ctypes.c_int64))

# values for enumeration 'evmc_status_code'
evmc_status_code__enumvalues = {
    0: 'EVMC_SUCCESS',
    1: 'EVMC_FAILURE',
    2: 'EVMC_REVERT',
    3: 'EVMC_OUT_OF_GAS',
    4: 'EVMC_INVALID_INSTRUCTION',
    5: 'EVMC_UNDEFINED_INSTRUCTION',
    6: 'EVMC_STACK_OVERFLOW',
    7: 'EVMC_STACK_UNDERFLOW',
    8: 'EVMC_BAD_JUMP_DESTINATION',
    9: 'EVMC_INVALID_MEMORY_ACCESS',
    10: 'EVMC_CALL_DEPTH_EXCEEDED',
    11: 'EVMC_STATIC_MODE_VIOLATION',
    12: 'EVMC_PRECOMPILE_FAILURE',
    13: 'EVMC_CONTRACT_VALIDATION_FAILURE',
    14: 'EVMC_ARGUMENT_OUT_OF_RANGE',
    15: 'EVMC_WASM_UNREACHABLE_INSTRUCTION',
    16: 'EVMC_WASM_TRAP',
    -1: 'EVMC_INTERNAL_ERROR',
    -2: 'EVMC_REJECTED',
    -3: 'EVMC_OUT_OF_MEMORY',
}
EVMC_SUCCESS = 0
EVMC_FAILURE = 1
EVMC_REVERT = 2
EVMC_OUT_OF_GAS = 3
EVMC_INVALID_INSTRUCTION = 4
EVMC_UNDEFINED_INSTRUCTION = 5
EVMC_STACK_OVERFLOW = 6
EVMC_STACK_UNDERFLOW = 7
EVMC_BAD_JUMP_DESTINATION = 8
EVMC_INVALID_MEMORY_ACCESS = 9
EVMC_CALL_DEPTH_EXCEEDED = 10
EVMC_STATIC_MODE_VIOLATION = 11
EVMC_PRECOMPILE_FAILURE = 12
EVMC_CONTRACT_VALIDATION_FAILURE = 13
EVMC_ARGUMENT_OUT_OF_RANGE = 14
EVMC_WASM_UNREACHABLE_INSTRUCTION = 15
EVMC_WASM_TRAP = 16
EVMC_INTERNAL_ERROR = -1
EVMC_REJECTED = -2
EVMC_OUT_OF_MEMORY = -3
evmc_status_code = ctypes.c_int # enum
class struct_evmc_result(ctypes.Structure):
    pass

evmc_release_result_fn = POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_evmc_result)))
bool = ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_int32))
evmc_get_storage_fn = POINTER_T(ctypes.CFUNCTYPE(struct_evmc_bytes32, POINTER_T(struct_evmc_host_context), POINTER_T(struct_evmc_address), POINTER_T(struct_evmc_bytes32)))

# values for enumeration 'evmc_storage_status'
evmc_storage_status__enumvalues = {
    0: 'EVMC_STORAGE_UNCHANGED',
    1: 'EVMC_STORAGE_MODIFIED',
    2: 'EVMC_STORAGE_MODIFIED_AGAIN',
    3: 'EVMC_STORAGE_ADDED',
    4: 'EVMC_STORAGE_DELETED',
}
EVMC_STORAGE_UNCHANGED = 0
EVMC_STORAGE_MODIFIED = 1
EVMC_STORAGE_MODIFIED_AGAIN = 2
EVMC_STORAGE_ADDED = 3
EVMC_STORAGE_DELETED = 4
evmc_storage_status = ctypes.c_int # enum
evmc_set_storage_fn = POINTER_T(ctypes.CFUNCTYPE(evmc_storage_status, POINTER_T(struct_evmc_host_context), POINTER_T(struct_evmc_address), POINTER_T(struct_evmc_bytes32), POINTER_T(struct_evmc_bytes32)))
evmc_get_balance_fn = POINTER_T(ctypes.CFUNCTYPE(struct_evmc_bytes32, POINTER_T(struct_evmc_host_context), POINTER_T(struct_evmc_address)))
size_t = ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_int32))
evmc_get_code_hash_fn = POINTER_T(ctypes.CFUNCTYPE(struct_evmc_bytes32, POINTER_T(struct_evmc_host_context), POINTER_T(struct_evmc_address)))
evmc_copy_code_fn = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(struct_evmc_host_context), POINTER_T(struct_evmc_address), POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_int32))), POINTER_T(ctypes.c_ubyte), POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_int32)))))
evmc_selfdestruct_fn = POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_evmc_host_context), POINTER_T(struct_evmc_address), POINTER_T(struct_evmc_address)))
evmc_emit_log_fn = POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_evmc_host_context), POINTER_T(struct_evmc_address), POINTER_T(ctypes.c_ubyte), POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_int32))), POINTER_T(struct_evmc_bytes32), POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_int32)))))
struct_evmc_result._pack_ = True # source:False
struct_evmc_result._fields_ = [
    ('PADDING_0', ctypes.c_ubyte),
]

evmc_call_fn = POINTER_T(ctypes.CFUNCTYPE(struct_evmc_result, POINTER_T(struct_evmc_host_context), POINTER_T(struct_evmc_message)))
class struct_evmc_host_interface(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('PADDING_0', ctypes.c_ubyte),
     ]

class struct_evmc_vm(ctypes.Structure):
    pass

evmc_destroy_fn = POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_evmc_vm)))

# values for enumeration 'evmc_set_option_result'
evmc_set_option_result__enumvalues = {
    0: 'EVMC_SET_OPTION_SUCCESS',
    1: 'EVMC_SET_OPTION_INVALID_NAME',
    2: 'EVMC_SET_OPTION_INVALID_VALUE',
}
EVMC_SET_OPTION_SUCCESS = 0
EVMC_SET_OPTION_INVALID_NAME = 1
EVMC_SET_OPTION_INVALID_VALUE = 2
evmc_set_option_result = ctypes.c_int # enum
evmc_set_option_fn = POINTER_T(ctypes.CFUNCTYPE(evmc_set_option_result, POINTER_T(struct_evmc_vm), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)))

# values for enumeration 'evmc_revision'
evmc_revision__enumvalues = {
    0: 'EVMC_FRONTIER',
    1: 'EVMC_HOMESTEAD',
    2: 'EVMC_TANGERINE_WHISTLE',
    3: 'EVMC_SPURIOUS_DRAGON',
    4: 'EVMC_BYZANTIUM',
    5: 'EVMC_CONSTANTINOPLE',
    6: 'EVMC_PETERSBURG',
    7: 'EVMC_ISTANBUL',
    8: 'EVMC_BERLIN',
    8: 'EVMC_MAX_REVISION',
}
EVMC_FRONTIER = 0
EVMC_HOMESTEAD = 1
EVMC_TANGERINE_WHISTLE = 2
EVMC_SPURIOUS_DRAGON = 3
EVMC_BYZANTIUM = 4
EVMC_CONSTANTINOPLE = 5
EVMC_PETERSBURG = 6
EVMC_ISTANBUL = 7
EVMC_BERLIN = 8
EVMC_MAX_REVISION = 8
evmc_revision = ctypes.c_int # enum
evmc_execute_fn = POINTER_T(ctypes.CFUNCTYPE(struct_evmc_result, POINTER_T(struct_evmc_vm), POINTER_T(struct_evmc_host_interface), POINTER_T(struct_evmc_host_context), evmc_revision, POINTER_T(struct_evmc_message), POINTER_T(ctypes.c_ubyte), POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_int32)))))

# values for enumeration 'evmc_capabilities'
evmc_capabilities__enumvalues = {
    1: 'EVMC_CAPABILITY_EVM1',
    2: 'EVMC_CAPABILITY_EWASM',
    4: 'EVMC_CAPABILITY_PRECOMPILES',
}
EVMC_CAPABILITY_EVM1 = 1
EVMC_CAPABILITY_EWASM = 2
EVMC_CAPABILITY_PRECOMPILES = 4
evmc_capabilities = ctypes.c_int # enum
evmc_capabilities_flagset = ctypes.c_uint32
evmc_get_capabilities_fn = POINTER_T(ctypes.CFUNCTYPE(ctypes.c_uint32, POINTER_T(struct_evmc_vm)))
struct_evmc_vm._pack_ = True # source:False
struct_evmc_vm._fields_ = [
    ('abi_version', ctypes.c_int32),
    ('PADDING_0', ctypes.c_ubyte * 4),
    ('name', POINTER_T(ctypes.c_char)),
    ('version', POINTER_T(ctypes.c_char)),
    ('destroy', POINTER_T(ctypes.CFUNCTYPE(None, POINTER_T(struct_evmc_vm)))),
    ('execute', POINTER_T(ctypes.CFUNCTYPE(struct_evmc_result, POINTER_T(struct_evmc_vm), POINTER_T(struct_evmc_host_interface), POINTER_T(struct_evmc_host_context), evmc_revision, POINTER_T(struct_evmc_message), POINTER_T(ctypes.c_ubyte), POINTER_T(ctypes.CFUNCTYPE(ctypes.c_int32, POINTER_T(ctypes.c_int32)))))),
    ('get_capabilities', POINTER_T(ctypes.CFUNCTYPE(ctypes.c_uint32, POINTER_T(struct_evmc_vm)))),
    ('set_option', POINTER_T(ctypes.CFUNCTYPE(evmc_set_option_result, POINTER_T(struct_evmc_vm), POINTER_T(ctypes.c_char), POINTER_T(ctypes.c_char)))),
]

__all__ = \
    ['EVMC_ABI_VERSION', 'EVMC_ARGUMENT_OUT_OF_RANGE',
    'EVMC_BAD_JUMP_DESTINATION', 'EVMC_BERLIN', 'EVMC_BYZANTIUM',
    'EVMC_CALL', 'EVMC_CALLCODE', 'EVMC_CALL_DEPTH_EXCEEDED',
    'EVMC_CAPABILITY_EVM1', 'EVMC_CAPABILITY_EWASM',
    'EVMC_CAPABILITY_PRECOMPILES', 'EVMC_CONSTANTINOPLE',
    'EVMC_CONTRACT_VALIDATION_FAILURE', 'EVMC_CREATE', 'EVMC_CREATE2',
    'EVMC_DELEGATECALL', 'EVMC_FAILURE', 'EVMC_FRONTIER',
    'EVMC_HOMESTEAD', 'EVMC_INTERNAL_ERROR',
    'EVMC_INVALID_INSTRUCTION', 'EVMC_INVALID_MEMORY_ACCESS',
    'EVMC_ISTANBUL', 'EVMC_MAX_REVISION', 'EVMC_OUT_OF_GAS',
    'EVMC_OUT_OF_MEMORY', 'EVMC_PETERSBURG',
    'EVMC_PRECOMPILE_FAILURE', 'EVMC_REJECTED', 'EVMC_REVERT',
    'EVMC_SET_OPTION_INVALID_NAME', 'EVMC_SET_OPTION_INVALID_VALUE',
    'EVMC_SET_OPTION_SUCCESS', 'EVMC_SPURIOUS_DRAGON',
    'EVMC_STACK_OVERFLOW', 'EVMC_STACK_UNDERFLOW', 'EVMC_STATIC',
    'EVMC_STATIC_MODE_VIOLATION', 'EVMC_STORAGE_ADDED',
    'EVMC_STORAGE_DELETED', 'EVMC_STORAGE_MODIFIED',
    'EVMC_STORAGE_MODIFIED_AGAIN', 'EVMC_STORAGE_UNCHANGED',
    'EVMC_SUCCESS', 'EVMC_TANGERINE_WHISTLE',
    'EVMC_UNDEFINED_INSTRUCTION', 'EVMC_WASM_TRAP',
    'EVMC_WASM_UNREACHABLE_INSTRUCTION', 'bool',
    'c__Ea_EVMC_ABI_VERSION', 'evmc_address', 'evmc_bytes32',
    'evmc_call_fn', 'evmc_call_kind', 'evmc_capabilities',
    'evmc_capabilities_flagset', 'evmc_copy_code_fn',
    'evmc_destroy_fn', 'evmc_emit_log_fn', 'evmc_execute_fn',
    'evmc_flags', 'evmc_get_balance_fn', 'evmc_get_block_hash_fn',
    'evmc_get_capabilities_fn', 'evmc_get_code_hash_fn',
    'evmc_get_storage_fn', 'evmc_get_tx_context_fn',
    'evmc_release_result_fn', 'evmc_revision', 'evmc_selfdestruct_fn',
    'evmc_set_option_fn', 'evmc_set_option_result',
    'evmc_set_storage_fn', 'evmc_status_code', 'evmc_storage_status',
    'evmc_uint256be', 'size_t', 'struct_evmc_address',
    'struct_evmc_bytes32', 'struct_evmc_host_context',
    'struct_evmc_host_interface', 'struct_evmc_message',
    'struct_evmc_result', 'struct_evmc_tx_context', 'struct_evmc_vm']
