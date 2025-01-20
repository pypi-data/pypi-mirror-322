from typing import List, Tuple
import pyarrow
from . import cherry_core as base

def cast(map: List[Tuple[str, str]], data: pyarrow.RecordBatch, allow_cast_fail: bool) -> pyarrow.RecordBatch:
    return base.cast(map, data, allow_cast_fail)

def cast_schema(map: List[Tuple[str, str]], schema: pyarrow.Schema) -> pyarrow.Schema:
    return base.cast_schema(map, schema)

def encode_hex(data: pyarrow.RecordBatch) -> pyarrow.RecordBatch:
    return base.encode_hex(data)

def encode_prefix_hex(data: pyarrow.RecordBatch) -> pyarrow.RecordBatch:
    return base.encode_prefix_hex(data)

def hex_encode_column(col: pyarrow.Array) -> pyarrow.Array:
    return base.hex_encode_column(col)

def prefix_hex_encode_column(col: pyarrow.Array) -> pyarrow.Array:
    return base.prefix_hex_encode_column(col)

def hex_decode_column(col: pyarrow.Array) -> pyarrow.Array:
    return base.hex_decode_column(col)

def prefix_hex_decode_column(col: pyarrow.Array) -> pyarrow.Array:
    return base.prefix_hex_decode_column(col)

def schema_binary_to_string(schema: pyarrow.Schema) -> pyarrow.Schema:
    return base.schema_binary_to_string(schema)

def u256_from_binary(col: pyarrow.Array) -> pyarrow.Array:
    return base.u256_from_binary(col)

def u256_to_binary(col: pyarrow.Array) -> pyarrow.Array:
    return base.u256_to_binary(col)

def evm_decode_call_inputs(signature: str, data: pyarrow.Array, allow_decode_fail: bool) -> pyarrow.RecordBatch:
    return base.evm_decode_call_inputs(signature, data, allow_decode_fail)

def evm_decode_call_outputs(signature: str, data: pyarrow.Array, allow_decode_fail: bool) -> pyarrow.RecordBatch:
    return base.evm_decode_call_outputs(signature, data, allow_decode_fail)

def evm_decode_events(signature: str, data: pyarrow.Array, allow_decode_fail: bool) -> pyarrow.RecordBatch:
    return base.evm_decode_events(signature, data, allow_decode_fail)

def evm_event_signature_to_arrow_schema(signature: str) -> pyarrow.Schema:
    return base.evm_event_signature_to_arrow_schema(signature)

def evm_transaction_signature_to_arrow_schemas(signature: str) -> Tuple[pyarrow.Schema, pyarrow.Schema]:
    return base.evm_transaction_signature_to_arrow_schemas(signature)

def evm_validate_block_data(blocks: pyarrow.RecordBatch, transactions: pyarrow.RecordBatch, logs: pyarrow.RecordBatch, traces: pyarrow.RecordBatch):
    base.evm_validate_block_data(blocks, transactions, logs, traces)

