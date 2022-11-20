from itertools import islice

from typing import Generator, Tuple, List


LAYER_HEIGHTS = [62, 50, 38, 26]
STACK_POSITIONS = [779, 843, 907, 971]
STACK_START = 1260
BYTE_PER_STACK = 64
BYTE_PER_INSTRUCTION = 16
INSTRUCTIONS = 64


def addresses_gen() -> Generator[Tuple[int, int, int], None, None]:
	for stackPos in STACK_POSITIONS:
		for heights in LAYER_HEIGHTS:
			for i in range(0, BYTE_PER_STACK, 2):
				yield (stackPos, heights, STACK_START + i)


def get_position(iter: int, default = (0, 0, 0)) -> Tuple[int, int, int]:
    addresses = addresses_gen()
    return next(islice(addresses, iter, None), default)


def get_pos_for_instr(instr: int, step: int) -> Tuple[int, int, int]:
    if not (step in range(BYTE_PER_INSTRUCTION) and instr in range(INSTRUCTIONS)):
        raise IndexError
    instr_offset = instr * BYTE_PER_INSTRUCTION
    abs_addr = instr_offset + step
    return get_position(abs_addr)


def generate_command(bstr: str, i: int, index: Tuple[int, int, int]) -> str:
    bit = bstr[i]
    bit_state = "false" if bit == "1" else "true"

    block = f"{index[0] + (i * 2)} {index[1]} {index[2]}"
    return f"setblock {block} minecraft:lever[facing=south, powered={bit_state}] replace"


def generate_set_blocks(value: int, instr: int, step: int) -> List[str]:
    bstr = f"{'{0:b}'.format(value & 0xFF):0>8}"
    index = get_pos_for_instr(instr, step)

    return [generate_command(bstr, i, index) for i in range(8)]

