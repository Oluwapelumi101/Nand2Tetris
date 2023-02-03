""" A program to tranlate VM code to Hack Assembly """

import sys
import re

""" 
RAM Addresses
0 - 15 : virtual resgisters
16- 255 static varables
256 - 2047 - stack

0 = SP
1 = LCL
2 = ARG
3 = THIS
4 = THAT
5 - 12 = TEMP
13 - 15 = 
"""

# CONTANT
EQ_ID = 0

# loading file with VM code
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
def parseOne(loaded_txt):
    """ Parsing file to remove coments and spaces"""
    # Handling Comments
    parsed_txt = (line for line in loaded_txt if not (re.match("//", line))) #header comments
    parsed_txt = list(re.split("//", line)[0] for line in parsed_txt) # inline coments
    # handling space
    parsed_txt = list([line.strip()] for line in parsed_txt)
    # converting each command to a list of lists
    output = []
    for list_item in parsed_txt:
       temp_list = ([word for item in list_item for word in item.split()])
       output.append(temp_list)       
    return(output)

# x = load("BasicTest.vm")
# x = parseOne(x)
# # print(x)

""" 
Index 1 = Push, Pop, ADD, Sub, eq, gt, lt, neg, and, or, not
"""
def get_commandType(command_Key):
    command_dict = {"add":"C_ARITHMETIC", "sub":"C_ARITHMETIC", "neg":"C_ARITHMETIC", "eq": "C_ARITHMETIC", "gt":"C_ARITHMETIC", "lt":"C_ARITHMETIC", "and":"C_ARITHMETIC", "or":"C_ARITHMETIC", "not":"C_ARITHMETIC", "push":"C_PUSH", "pop":"C_POP"}

    return(command_dict[command_Key])

""" 
# Sample One
push constant 7
@7
D = A
@SP
A = M
M = D
@SP
M = M + 1

# Sample Two
@3
D = A
push argument 3 (400) + 3
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1

# handling temp
@5
M = A Setting the temp to 5
... folwing standard procidure

"""
def write_C_PUSH(arg1, arg2, static_name):
    assembly_code = []

    # Handline Contants
    if arg1 == "constant":
        val = "@" + str(arg2)
        assembly_code.append(val)
        assembly_code.append("D=A")
    
    # handling local
    if arg1 == "local":
        val = "@" + str(arg2)
        assembly_code.append(val)
        assembly_code.append("D=A")
        assembly_code.append("@LCL")
        assembly_code.append("A=M+D")
        assembly_code.append("D=M")

    # handling argument
    if arg1 == "argument":
        val = "@" + str(arg2)
        assembly_code.append(val)
        assembly_code.append("D=A")
        assembly_code.append("@ARG")
        assembly_code.append("A=M+D")
        assembly_code.append("D=M")

    # handling this
    if arg1 == "this":
        val = "@" + str(arg2)
        assembly_code.append(val)
        assembly_code.append("D=A")
        assembly_code.append("@THIS")
        assembly_code.append("A=M+D")
        assembly_code.append("D=M")

    # handling that
    if arg1 == "that":
        val = "@" + str(arg2)
        assembly_code.append(val)
        assembly_code.append("D=A")
        assembly_code.append("@THAT")
        assembly_code.append("A=M+D")
        assembly_code.append("D=M")

    # handling temp
    if arg1 == "temp":
        val = "@" + str(arg2)
        assembly_code.append(val)
        assembly_code.append("D=A")
        assembly_code.append("@5")
        assembly_code.append("M=A")
        assembly_code.append("A=M+D")
        assembly_code.append("D=M")

    # handling Static
    if arg1 == "static":
        val = "@" + str(arg2)
        static_var = "@" + static_name + str(arg2)
        assembly_code.append(val)
        assembly_code.append("D=A")
        assembly_code.append(static_var)
        assembly_code.append("A=M+D")
        assembly_code.append("D=M")

    # handling pointer 0
    # Pushing the value at R3 to the stack
    if arg1 == "pointer" and arg2 == '0':
        assembly_code.append("@R3")
        assembly_code.append("D=M")

    # handling pointer 1
    # Pushing the value at R4 to the stack
    if arg1 == "pointer" and arg2 == '1':
        assembly_code.append("@R4")
        assembly_code.append("D=M")

    # Common commans
    assembly_code.append("@SP")
    assembly_code.append("A=M")
    assembly_code.append("M=D")
    assembly_code.append("@SP")
    assembly_code.append("M=M+1")
    return(assembly_code)


""" 
assume stack is 10
RAM O = 257
pop	argument 0

@2 (arg2) geting the argument index 
D = A
@ARG adding the index to argument starting location
A = M + D
D = A
@temp temporyry storying the needed arguement val
M = D
@SP
A = M-1
D = M   geting the value for the stack
@temp
A = M 
M = D setting the argurment index to the value in stack
@SP
M = M - 1 takins stack one value back

# Popping Pointer 0 (R3) //seeting R3 to stack value
@SP
A = M-1
D = M   geting the value for the stack
@R3
M=D
"""
def write_C_POP(arg1, arg2, static_name):
    assembly_code = []

    if arg1 != "pointer":
        val = "@" + str(arg2)
        assembly_code.append(val)
        assembly_code.append("D=A")
        if arg1 == "local":
            assembly_code.append("@LCL")
        if arg1 == "argument":
            assembly_code.append("@ARG")
        if arg1 == "this":
            assembly_code.append("@THIS")
        if arg1 == "that":
            assembly_code.append("@THAT")
        if arg1 == "temp":
            assembly_code.append("@5")
            assembly_code.append("M=A")
        if arg1 == "static":
            static_var = "@" + static_name + str(arg2)
            assembly_code.append(static_var)
        
        assembly_code.append("A=M+D")
        assembly_code.append("D=A")
        assembly_code.append("@6")
        assembly_code.append("M=D")
        assembly_code.append("@SP")
        assembly_code.append("M=M-1")
        assembly_code.append("A=M")
        assembly_code.append("D=M")
        assembly_code.append("@6")
        assembly_code.append("A=M")
        assembly_code.append("M=D")
        

    elif arg1 == "pointer" and arg2 == '0':
        assembly_code.append("@SP")
        assembly_code.append("M=M-1")
        assembly_code.append("A=M")
        assembly_code.append("D=M")
        assembly_code.append("@R3")
        assembly_code.append("M=D")

    elif arg1 == "pointer" and arg2 == '1':
        assembly_code.append("@SP")
        assembly_code.append("M=M-1")
        assembly_code.append("A=M")
        assembly_code.append("D=M")
        assembly_code.append("@R4")
        assembly_code.append("M=D")

    return(assembly_code)


""" 
256 = 7
257 = 8
sp = 258

@SP
A = M - 1
D = M  sets d to 8

@SP
M = M - 1 set sp to 257

@temp
M = D  sets m = 8

@SP
A = M -1
D = M dets D to 7

@SP
M = M - 1 set SP to 256

@temp
M = M + D | M = M-D
D = M

@SP
A = M
M = D

@SP
A = M
M = M + 1


# Computing not equal
... pop stack to M and D 
@temp
M = M-D
D = M
@OUTPUT_TRUE
D;JEQ


(INFINITE_LOOP)
   @INFINITE_LOOP 
   0;JMP      
"""
def write_C_ARITHMETIC(arg1):
    assembly_code = []
    global EQ_ID

    true_label_RAM = "@OUTPUT_TRUE" + "_" + str(EQ_ID)
    stack_label_RAM = "@OUTPUT_STACK" + "_" + str(EQ_ID)

    true_label = "(OUTPUT_TRUE" + "_" + str(EQ_ID) + ")"
    stack_label = "(OUTPUT_STACK" + "_" + str(EQ_ID) + ")"
    # Getting the top of the stack
    assembly_code.append("@SP")
    assembly_code.append("M=M-1")
    assembly_code.append("A=M")
    assembly_code.append("D=M")
    # Pushing the popped value to a temporary RAM[6] address
    assembly_code.append("@6")
    assembly_code.append("M=D")
    if arg1 == "not" or arg1 == "neg":
        # Negate
        if arg1 == "neg":
            assembly_code.append("D=-M")

        # not
        if arg1 == "not":
            assembly_code.append("D=!M")
    else:
        # Getting the next value in the Stack
        assembly_code.append("@SP")
        assembly_code.append("M=M-1")
        assembly_code.append("A=M")
        assembly_code.append("D=M")
        # Goint back to temp RAM[6]
        assembly_code.append("@6")

        # additon
        if arg1 == "add":
            assembly_code.append("D=M+D")

        # subtraction
        if arg1 == "sub":
            assembly_code.append("D=D-M")

        # equality
        # note D = first into the stack, M = second onto the stack 
        if arg1 == "eq":
            assembly_code.append("D=D-M")
            assembly_code.append(true_label_RAM)
            assembly_code.append("D;JEQ")
            assembly_code.append(stack_label_RAM)
            assembly_code.append("D=0")
            assembly_code.append("0;JMP")
            assembly_code.append(true_label)
            assembly_code.append("D=-1")
            assembly_code.append(stack_label)

        # Greater than
        if arg1 == "gt":
            assembly_code.append("D=D-M")
            assembly_code.append(true_label_RAM)
            assembly_code.append("D;JGT")
            assembly_code.append(stack_label_RAM)
            assembly_code.append("D=0")
            assembly_code.append("0;JMP")
            assembly_code.append(true_label)
            assembly_code.append("D=-1")
            assembly_code.append(stack_label)

        # Less than
        if arg1 == "lt":
            assembly_code.append("D=D-M")
            assembly_code.append(true_label_RAM)
            assembly_code.append("D;JLT")
            assembly_code.append(stack_label_RAM)
            assembly_code.append("D=0")
            assembly_code.append("0;JMP")
            assembly_code.append(true_label)
            assembly_code.append("D=-1")
            assembly_code.append(stack_label)

        # OR
        if arg1 == "or":
            assembly_code.append("D=D|M")

        # and
        if arg1 == "and":
            assembly_code.append("D=D&M")

    # pushing the result of the computation into the stack
    assembly_code.append("@SP")
    assembly_code.append("A=M")
    assembly_code.append("M=D")
    # Incrementing the stack
    assembly_code.append("@SP")
    assembly_code.append("M=M+1")
    EQ_ID += 1
    return(assembly_code)

def parseTwo(list, static_name):
    num_of_commands = len(list)
    final_assembly_code = []
    for current_command in list:
        comment = "// " + ' '.join(current_command)
        final_assembly_code.append(comment)
        commandType = get_commandType(current_command[0])
        
        # Handling Push Instructions
        if (commandType == "C_PUSH"):
            arg1 = current_command[1]
            arg2 = current_command[2]
            assembly_code = write_C_PUSH(arg1, arg2, static_name)
            [final_assembly_code.append(i) for i in assembly_code]
            # print(' '.join(assembly_code))
            # final_assembly_code.append(assembly_code)
        
        # Handling Pop Instructions
        if (commandType == "C_POP"):
            arg1 = current_command[1]
            arg2 = current_command[2]
            assembly_code = write_C_POP(arg1, arg2, static_name)
            [final_assembly_code.append(i) for i in assembly_code]
            # final_assembly_code.append(assembly_code)

        # Handling Arithemetic instructions
        if (commandType == "C_ARITHMETIC"):
            arg1 = current_command[0]
            assembly_code = write_C_ARITHMETIC(arg1)
            [final_assembly_code.append(i) for i in assembly_code]
            # final_assembly_code.append(assembly_code)

    return(final_assembly_code)

# parseTwo(x)

def write_output(list, filename):
    # writing output
    with open(filename, 'w') as f:
        for line in list:
            f.write(f"{line}\n")

def main(filename):
    # loading file 
    vm_code = load(filename)

    # spliting file name for static variable
    static_name = str(filename.split(".")[0].split("/")[-1])
    output_name = str(filename.split(".")[0]) + ".asm"

    # parsing out comments and spaces
    vm_code = parseOne(vm_code)

    # compiling file to assembly
    assembly_code = parseTwo(vm_code, static_name)

    # wrting output 
    write_output(assembly_code, output_name)

if __name__ == "__main__" and len(sys.argv) == 2:
    vm_code_file = sys.argv[1]
    main(vm_code_file)