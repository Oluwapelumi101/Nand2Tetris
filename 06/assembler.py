""" Implementing an assembler for the Hack CPU buit in the course NAND 2 tetris """

import sys
import re

# SYMBOLS_MAP = {"R0":"0", "R1":"1", "R2":"2", "R3":"3", "R4":"4", "R5":"5", "R6":"6", "R7":"7", "R8":"8", "R9":"9", "R10":"10", "R11":"11", "R12":"12", "R13":"31", "R14":"14", "R15":"15", "SCREEN":"16384", "KBD":"24576", "SP":"0", "LCL":"1", "ARG":"2", "THIS":"3", "THAT":"4"}


SYMBOLS_MAP = {"@R0":"@0", "@R1":"@1", "@R2":"@2", "@R3":"@3", "@R4":"@4", "@R5":"@5", "@R6":"@6", "@R7":"@7", "@R8":"@8", "@R9":"@9", "@R10":"@10", "@R11":"@11", "@R12":"@12", "@R13":"@13", "@R14":"@14", "@R15":"@15", "@SCREEN":"@16384", "@KBD":"@24576", "@SP":"@0", "@LCL":"@1", "@ARG":"@2", "@THIS":"@3", "@THAT":"@4"}



# Loading file
def load(file):
    try:
        with open(file, "r") as in_file:
            loaded_txt = list(line for line in (l.strip() for l in in_file) if line)
            return loaded_txt
    except IOError as e:
        print("{}\nError opening {}. Terminating program.".format(e, file),
            file=sys.stderr)
        sys.exit(1)

# Parsing file
def parse(loaded_txt):
    """ Parsing file to remove coments """
    # # Handling Comments
    parsed_txt = (line for line in loaded_txt if not (re.match("//", line)))
    parsed_txt = list(re.split("//", line)[0] for line in parsed_txt)
    parsed_txt = list(line.strip() for line in parsed_txt)        
    # print(parsed_txt)
    return(parsed_txt)

# x = load("Nand2Tetris/Pong.asm")
# x = parse(x)
# # print(x)

# Converting Decimal into binary
def decimalToBinary(num):
    value = num
    binary = []
    while True:
        if ( value % 2):
            binary.append(1)
        else:
            binary.append(0)
        value = value // 2
        if value == 0:
            base2 = ''.join(map(str, binary[::-1]))
            return base2

# x = decimalToBinary(40170)
# print(x)

# Handling symbols
def symbols(list):
    # adding (Labels to symbol table)
    pos = 0
    for instruction in list:
        if instruction[0] == "(":
            my_keys = re.split("\(([\w.$]+)\)", instruction)
            # print(my_keys)
            my_key = "@" + my_keys[1]
            # print(pos, instruction)
            val = "@" + str(pos)
            SYMBOLS_MAP[my_key] = val
        if instruction[0] != "(":
            pos += 1
    # updating label positions and adding variables
    N = 16
    for instruction in list:
        if (instruction[0] == "@") and not instruction[1::].isdigit():
            # Checking if instruction is in sybol table 
            val = SYMBOLS_MAP.get(instruction)
            if val == None:
                new_val= "@" + str(N)
                SYMBOLS_MAP[instruction] = new_val
                N += 1
    # print(SYMBOLS_MAP)


def Replace_Symbols(list):
    temp = list
    counter = 0
    for instruction in temp:
        if (instruction[0] == "@") and not instruction[1::].isdigit():
            # Checking if instruction is in sybol table 
            val = SYMBOLS_MAP.get(instruction)
            # Replacing symbol with instruction
            temp[counter] = val
        counter += 1

    def remove_labels(instruction):    
        if instruction[0] == "(":
            return False
        else:
            return True

    filtered_txt = filter(remove_labels, temp)
    return filtered_txt

# x = load("Nand2Tetris/Pong.asm")
# x = parse(x)
# symbols(x)
# edited = Replace_Symbols(x)
# print(list(edited))

# Converting a instruction to binary
def Convert_A_Instruction(instruction):
    num = int(instruction[1:])
    base2 = decimalToBinary(num)
    # converting to 15bit instruction
    x = str(base2)
    while True:
        x = "0" + x
        if len(x) == 16:
            return x

# print(Convert_A_Instruction("@10"))  

# Handlinf C instruuction
def Convert_C_Instruction(instruction):
    """ dest= comp;jump """
    # Compute tables
    C_instruct = ["111"]

    # Destination table
    dest_dict = {"null": "000", "M": "001", "D": "010", "MD": "011", "A": "100", "AM": "101", "AD" : "110", "ADM": "111" }
    
    # Comp table
    comp_dict = {"0":"0101010", "1":"0111111", "-1":"0111010", "D":"0001100", "A":"0110000", "M":"1110000", "!D":"0001101", "!A":"0110001", "!M" :"1110001", "-D":"0001111", "-A":"0110011", "-M":"1110011", "D+1":"0011111", "A+1":"0110111", "M+1":"1110111", "D-1":"0001110", "A-1":"0110010", "M-1":"1110010", "D+A":"0000010", "D+M":"1000010", "D-A":"0010011", "D-M":"1010011", "A-D":"0000111", "M-D":"1000111", "D&A":"0000000", "D&M":"1000000", "D|A":"0010101", "D|M":"1010101"}

    # jump table
    jump_dict = {"null":"000", "JGT":"001", "JEQ":"010", "JGE":"011", "JLT":"100", "JNE":"101", "JLE":"110", "JMP":"111"}

    # Parsing C-Instruction intob its components
    match = re.match("(\w*)=?([\w\-\+\&\!\|]+);?(\w*)", instruction) 
    # print(instruction)
    dest = match[1]
    comp = match[2]
    jump = match[3]
 
    # Handline comp
    comp_val = comp_dict[comp]
    C_instruct.append(comp_val)

    # Handling dest
    if dest:
        dest_val = dest_dict[dest]
        C_instruct.append(dest_val)
    else:
        dest_val = dest_dict["null"]
        C_instruct.append(dest_val)

    # Handling Jump
    if jump:
        jump_val = jump_dict[jump]
        C_instruct.append(jump_val)
    else:
        jump_val = jump_dict["null"]
        C_instruct.append(jump_val)

    C_instruct = ''.join(C_instruct)
    return C_instruct

# test = ["M=D", "D=M-1", "0;JMP", "DM=0;JMP", "D=D+A", "A=D-M"]
# for x in test:
#     print(x)
#     print(Convert_C_Instruction(x))

def main(file):
    Machine_Code = [] #holding output
    # Reading file into a list
    instructions = load(file)
    # Parsing the intructions
    paresed_instructions = parse(instructions)
    # updating symbol table 
    symbols(paresed_instructions)
    # print(SYMBOLS_MAP)
    paresed_instructions = Replace_Symbols(paresed_instructions)
    for instruction in paresed_instructions:
        if instruction[0] == "@":
            val = Convert_A_Instruction(instruction)
            Machine_Code.append(val)
        else:
            val = Convert_C_Instruction(instruction)
            Machine_Code.append(val)

    # writing output
    with open('Add.hack', 'w') as f:
        for line in Machine_Code:
            f.write(f"{line}\n")
        
    # print(Machine_Code)

main("Nand2Tetris/Add.asm")