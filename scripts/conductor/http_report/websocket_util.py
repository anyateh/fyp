import struct

CONTINUATION  = 0x0
TEXT          = 0x1
BINARY        = 0x2
CONENCT_CLOSE = 0x8
PING          = 0x9
PONG          = 0xA

def is_last_frame(websocket_f:bytes) -> bool:
	return (websocket_f[0] & 0x80) == 0x80

# Reject any packet with a True inside the return value
def get_rsvs(frame:bytes) -> tuple[bool, bool, bool]:
	return (frame[0] & 0x40) == 0x40, \
		(frame[0] & 0x20) == 0x20, \
		(frame[0] & 0x10) == 0x10

def get_optcode(frame:bytes) -> int:
	return frame[0] & 0x0f

def is_frame_masked(frame:bytes) -> bool:
	return (frame[1] & 0x80) == 0x80

def get_payload_length(frame:bytes) -> int:
	len_7b = frame[1] & 0x7f

	if len_7b == 126:
		return struct.unpack("!H", frame[2:4])[0]

	if len_7b == 127:
		return struct.unpack("!Q", frame[2:6])[0]
	
	return len_7b

def gen_payload_len(l:int) -> bytes:
	if l < 126:
		return struct.pack("!B", l)

	if l < (1 << 16):
		return struct.pack("!B", 126) + struct.pack("!H", l)

	return struct.pack("!B", 127) + struct.pack("!Q", l)

def get_masking_bytes_start(frame:bytes) -> int:
	len_7b = frame[1] & 0x7f

	if len_7b == 126:
		return 4
	
	if len_7b == 127:
		return 10

	return 2

def get_payload_bytes_start(frame:bytes) -> int:
	if is_frame_masked(frame):
		return get_masking_bytes_start(frame) + 4

	return get_masking_bytes_start(frame)

def get_mask_bytes(frame:bytes) -> bytes:
	if is_frame_masked(frame):
		mask_start = get_masking_bytes_start(frame)
		return frame[mask_start:mask_start + 4]

	return b'\x00\x00\x00\x00'

def extract_payload(frame:bytes) -> bytes:
	payload_start = get_payload_bytes_start(frame)
	if not is_frame_masked(frame):
		return frame[payload_start:]

	return mask_unmask_payload(frame[payload_start:], get_mask_bytes(frame))

def mask_unmask_payload(payload:bytes, masking_key:bytes) -> bytes:
	return bytes(byte ^ masking_key[i % 4] for i, byte in enumerate(payload))

def is_valid_client_frame(frame:bytes) -> bool:
	if get_rsvs(frame) != ((False,) * 3):
		return False

	return is_frame_masked(frame)

def extract_text_frame(frame:bytes) -> str:
	assert get_optcode(frame) == TEXT, "The WebSocket frame is not of type \"text\""
	return extract_payload(frame).decode(encoding = 'utf-8')

def create_response_text_frame(payload:str) -> bytes:
	res_bytes = [
		bytes([TEXT | 0x80])
	]

	pl_bytes = payload.encode(encoding = 'utf-8')

	res_bytes.append(gen_payload_len(len(pl_bytes)))

	res_bytes.append(pl_bytes)

	return b''.join(res_bytes)
