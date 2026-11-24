import sys
import os

DEST_TABLE = {
    "": "000", "M": "001", "D": "010", "MD": "011",
    "A": "100", "AM": "101", "AD": "110", "AMD": "111"
}

JUMP_TABLE = {
    "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"
}

COMP_TABLE = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "!D": "0001101",
    "!A": "0110001", "-D": "0001111", "-A": "0110011",
    "D+1": "0011111", "A+1": "0110111", "D-1": "0001110",
    "A-1": "0110010", "D+A": "0000010", "D-A": "0010011",
    "A-D": "0000111", "D&A": "0000000", "D|A": "0010101",
    "M": "1110000", "!M": "1110001", "-M": "1110011",
    "M+1": "1110111", "M-1": "1110010", "D+M": "1000010",
    "D-M": "1010011", "M-D": "1000111", "D&M": "1000000",
    "D|M": "1010101"
}

def assemble(asm_file):
    symbols = {
        "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
        "SCREEN": 16384, "KBD": 24576
    }
    for i in range(16):
        symbols[f"R{i}"] = i

    custom_symbols = {}

    with open(asm_file, "r") as f:
        raw_lines = f.readlines()

    cleaned_lines = []
    for line in raw_lines:
        line = line.split("//")[0].strip()
        if line:
            cleaned_lines.append(line)

    instructions = []
    rom_address = 0
    for line in cleaned_lines:
        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1]
            symbols[label] = rom_address
            custom_symbols[label] = f"ROM {rom_address} (Label)"
        else:
            instructions.append(line)
            rom_address += 1

    next_var_ram = 16
    binary_output = []

    for inst in instructions:
        if inst.startswith("@"):
            symbol = inst[1:]
            if symbol.isdigit():
                val = int(symbol)
            else:
                if symbol not in symbols:
                    symbols[symbol] = next_var_ram
                    custom_symbols[symbol] = f"RAM {next_var_ram} (Variable)"
                    next_var_ram += 1
                val = symbols[symbol]
            binary_output.append(f"0{val:015b}")
        else:
            dest, comp, jump = "", inst, ""
            if "=" in comp:
                dest, comp = comp.split("=")
            if ";" in comp:
                comp, jump = comp.split(";")
            
            c_bits = COMP_TABLE[comp.strip()]
            d_bits = DEST_TABLE[dest.strip()]
            j_bits = JUMP_TABLE[jump.strip()]
            binary_output.append(f"111{c_bits}{d_bits}{j_bits}")

    out_file = os.path.splitext(asm_file)[0] + ".hack"
    with open(out_file, "w") as f:
        f.write("\n".join(binary_output) + "\n")

    with open("symbols.txt", "w") as f:
        f.write("Symbol Table (Labels & Variables) for K = 57\n")
        f.write("-" * 45 + "\n")
        for sym, addr in custom_symbols.items():
            f.write(f"{sym:<20} : {addr}\n")

    print(f"Assembled {asm_file} -> {out_file} (Saved symbols to symbols.txt)")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 assembler.py <file.asm>")
    else:
        assemble(sys.argv[1])