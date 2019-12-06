class Nibbles16Bit:
    def __init__(self, number: int):
        self._number = number

    def __getitem__(self, key: int) -> int:
        return (self._number >> (4 * (3 - key))) & 0xF


def parse_machine_instruction(instruction: int) -> str:
    if instruction == 0x00E0:
        return 'CLS'
    elif instruction == 0x00EE:
        return 'RET'

    nibbles = Nibbles16Bit(instruction)
    left = nibbles[0]

    if left == 1:
        return f'JP {hex(instruction & 0xFFF)}'
    elif left == 2:
        return f'CALL {hex(instruction & 0xFFF)}'
    elif left == 3:
        return f'SE V{nibbles[1]}, {hex(instruction & 0xFF)}'
    elif left == 4:
        return f'SNE V{nibbles[1]}, {hex(instruction & 0xFF)}'
    elif left == 5:
        return f'SE V{nibbles[1]}, V{nibbles[2]}'
    elif left == 6:
        return f'LD V{nibbles[1]}, {hex(instruction & 0xFF)}'
    elif left == 7:
        return f'ADD V{nibbles[1]}, {hex(instruction & 0xFF)}'
    elif left == 8:
        right = nibbles[3]
        if right == 0:
            return f'LD V{nibbles[1]}, V{nibbles[2]}'
        elif right == 1:
            return f'OR V{nibbles[1]}, V{nibbles[2]}'
        elif right == 2:
            return f'AND V{nibbles[1]}, V{nibbles[2]}'
        elif right == 3:
            return f'XOR V{nibbles[1]}, V{nibbles[2]}'
        elif right == 4:
            return f'ADD V{nibbles[1]}, V{nibbles[2]}'
        elif right == 5:
            return f'SUB V{nibbles[1]}, V{nibbles[2]}'
        elif right == 6:
            return f'SHR V{nibbles[1]} {{, V{nibbles[2]}}}'
        elif right == 7:
            return f'SUBN V{nibbles[1]}, V{nibbles[2]}'
        elif right == 15:
            return f'SHL V{nibbles[1]} {{, V{nibbles[2]}}}'
    elif left == 9:
        return f'SNE V{nibbles[1]}, V{nibbles[2]}'
    elif left == 10:
        return f'LD I, {hex(instruction & 0xFFF)}'
    elif left == 11:
        return f'JP V0, {hex(instruction & 0xFFF)}'
    elif left == 12:
        return f'RND V{nibbles[1]}, {hex(instruction & 0xFF)}'
    elif left == 13:
        return f'DRW V{nibbles[1]}, V{nibbles[2]}, {hex(instruction & 0xF)}'
    elif left == 14:
        right_two = instruction & 0xFF
        if right_two == 0x9E:
            return f'SKP V{nibbles[1]}'
        elif right_two == 0xA1:
            return f'SKNP V{nibbles[1]}'
    elif left == 15:
        right_two = right_two = instruction & 0xFF
        if right_two == 0x07:
            return f'LD V{nibbles[1]}, DT'
        elif right_two == 0x0A:
            return f'LD V{nibbles[1]}, K'
        elif right_two == 0x15:
            return f'LD DT, V{nibbles[1]}'
        elif right_two == 0x18:
            return f'LD ST, V{nibbles[1]}'
        elif right_two == 0x1E:
            return f'ADD I, V{nibbles[1]}'
        elif right_two == 0x29:
            return f'LD F, V{nibbles[1]}'
        elif right_two == 0x33:
            return f'LD B, V{nibbles[1]}'
        elif right_two == 0x55:
            return f'LD [I], V{nibbles[1]}'
        elif right_two == 0x65:
            return f'LD V{nibbles[1]}, [I]'
    else:
        return str(instruction)


def disassemble_file(filepath: str):
    instructions = []

    with open(filepath, 'rb') as f:
        chunk = f.read(2)
        while chunk:
            instructions.append(
                parse_machine_instruction(int.from_bytes(chunk, "big")))
            chunk = f.read(2)

    # Most Chip-8 programs get loaded into memory at this address.
    # This disassembler does not (currently) properly support ETI 660 Chip-8 programs.
    address = 512

    for instruction in instructions:
        print(f'[{hex(address)}] {instruction}')
        address += 2


if __name__ == '__main__':
    disassemble_file('Pong.ch8')
