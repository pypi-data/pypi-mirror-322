from cherry_core import evm_decode_events, evm_event_signature_to_arrow_schema
import pyarrow

a = evm_event_signature_to_arrow_schema("Transfer(address indexed from, address indexed to, uint256 amount)")

print(a)
