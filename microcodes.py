from typing import Tuple, List

from enum import Enum

from positions import generate_set_blocks


class LeftCodes(Enum):
	LD_D = 0x0
	D = 0x2
	LD_PORT_A = 0x1
	PORT_A = 0x8
	LD_IR = 0x3
	CLD_IR = 0x4
	LD_PORT_B = 0x5
	PORT_B = 0xC
	LD_A = 0x9
	LD_B = 0xB
	MAR = 0xF
	HALT = 0xA
	READ = 0x6
	WRITE = 0x7
	LD_MAR = 0xD
	INC_MAR = 0xE


class RightCodes(Enum):
	NOOP = 0x0
	D = 0x2
	LD_PORT_A = 0x1
	PORT_A = 0x8
	LD_IR = 0x3
	CLD_IR = 0x4
	LD_PORT_B = 0x5
	LD_OP = 0xC
	LD_A = 0x9
	LD_B = 0xB
	HALT = 0xA
	READ = 0x6
	WRITE = 0x7
	LD_MAR = 0xD
	INC_MAR = 0xE
	ACC = 0xF


def generate_instruction(codes: List[Tuple[LeftCodes, RightCodes]], instr: int) -> List[str]:
	values = [v[0].value << 4 | v[1].value for v in codes]

	code_blocks = [generate_set_blocks(v, instr, i) for i, v in enumerate(values)]

	return sum(code_blocks, [])


def test():
	stack = [
		(LeftCodes.HALT, RightCodes.NOOP),
		(LeftCodes.PORT_A, RightCodes.LD_A),

		(LeftCodes.HALT, RightCodes.NOOP),
		(LeftCodes.PORT_A, RightCodes.LD_B),
		
		(LeftCodes.HALT, RightCodes.NOOP),
		(LeftCodes.PORT_A, RightCodes.LD_OP),

		(LeftCodes.LD_PORT_A, RightCodes.ACC),
		(LeftCodes.HALT, RightCodes.NOOP),

		(LeftCodes.LD_IR, RightCodes.NOOP)
	]

	result = generate_instruction(stack, 0)

	for res in result:
		print(res)

