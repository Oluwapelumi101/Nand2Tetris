""" A program to translate Jack High level language into Jack VM code """

# Handling file and folder opening : done
# Handling parsing out junks
# Handling API comments : done
# inline comments: done

import sys
import os
import re


def load(file):
    """ Opening file and Cleaning for tokenization """
    try:
        with open(file, "r") as in_file:
            temp = []
            for x in in_file:
                line = x.strip()
                # Removing empty lines and simgle line comments
                if line and not re.match("//", line):
                    temp.append(line)

            # Handling Api Comments
            count = 0
            temp_2 = []
            # for count in range(len(temp)):
            while count < len(temp):
                line = temp[count]

                # Single line Api Comment
                if line.startswith("/**") and line.endswith("*/"):
                    count += 1

                # Multi line Api Comments
                if line.startswith("/**") and not line.endswith("*/"):
                    while not line.endswith("*/"):
                        count += 1
                        line = temp[count]
                    count += 1
                line = temp[count]
                temp_2.append(line)
                count += 1

            # Handling inline comments
            temp_2 = list(re.split("//", line)[0] for line in temp_2)  # inline coments
            return temp_2
    # Handling Error in file opening
    except IOError as e:
        print(
            "{}\nError opening {}. Terminating program.".format(e, file),
            file=sys.stderr,
        )
        sys.exit(1)

class Tokenizer():
    LEXICAL_DICT = {
        "KEYWORD":["class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"],

        "SYBOL":["(", ")", "{", "}", "[", "]", ".", ",", ";", "+", "-", "*", "&", "/", "|", "<", ">", "=", "~"], 

        "INT_CONSTANT":range(32767), 
        "STRING_CONSTANT":"", 
        "IDENTIFER":""
    }

    def __init__(self, code_list):
        """ Stuff """
        self.input = code_list
        self.token_list = []
        self.temp_list = []
        self.output = []

# Extrating Strings
# Check each item till you find a '"' 
# Split the item into three halfs 
    # A characters before the '"'
    # B chracters till the next '"'
    # C characters after
    # Recall function on all theree
# Base case 
# if no "
    # do norml
# if start with  " and end with "
    # do normal

    def temp_function(self, value):
        """ Parser that can handle strings """
        output_list = []
        # if value[0] == '"' and value[-1] == '"':
        #     print(value)
        #     return 
        # if '"' not in value:
        #     print(value)
        #     return value
        if '"' in value:
            # print(value)
            word_list = re.split(r'("[^"]*")', value)
            # print(word_list)
            for obj in word_list:
                if obj[0] == '"' and obj[-1] == '"':
                        print(obj)
                if '"' not in obj:
                    print(obj)
                    # return value
                # temp = obj.strip().split(" ")
                # print(temp)
                # self.temp_function(obj)

            
    def parse_Line(self):
        # print(self.input)
        for item in self.input:
            # print(item)
            x = self.temp_function(item)
            print(x)
        #     temp = item.strip().split(" ")
        #     temp = list(filter(None, temp))
        #     self.temp_list.append(temp)
        # print(self.temp_list)

    def is_keyword(self, value):
        """ Cheack if a code is a keyword and generate appropraite output """
        keywords = Tokenizer.LEXICAL_DICT["KEYWORD"]
        if value in keywords:
            xml = f"<keyword> {value} </keyword>"
            print(xml)
            return xml

    def is_symbol(self, value):
        """ Check if a value is a jack symbol and generate xml output """
        symbols = Tokenizer.LEXICAL_DICT["SYBOL"]
        if value in symbols:
            xml = f"<symbol> {value} </symbol>"
            print(xml)
            return xml

    def is_identifer(self, value):
        """ Checks is a value is an identifer and generates the xml output """
        ...
        # String
        # does not start with quotes
        # situations ending with ()
        # Situations ending without ()
        # ~exit
        # trailing ;
        #  Square.new(0, 0, 30);
        if isinstance(value, str) and value[0] != '"':
            if not value[0].isalpha():
                print("type A") 
                # value_one = value[0]
                # value_two = value[1:]
                # print(value_one, value_two)
                # Tokenizer.is_identifer(self, value_two)
            elif value[-1] == ")":
                print("tyoe B")
            elif value[-1] != ")":
                print("type C")
  
    def is_strConstant(self, value):
        """ Checks is a value is a String Constant and generates the xml output """
        if isinstance(value, str) and value[0] == '"':
            no_quotes = value[1:-1]
            xml = f"<stringConstant> {no_quotes}  </stringConstant>"
            print(xml)
            return xml

    def is_intConstant(self, value):
        """ Checks is a value is an Int Constant and generates the xml output """
        # Dealing with trailing ;
        if value.isdigit():
            xml = f"<integerConstant> {value} </integerConstant>"
            print(xml)
            return xml    

    def char_type(self, char):
        """ Determin if a character is an Alphabet, an Integer or a Symbol """
        if char.isalpha():
            return "alpha"
        elif char.isdigit():
            return "int"
        else:
            return "symbol"

    def Tokenize(self, value):
        """ Recursive function to seperate input to individual tokens"""
        constant = self.char_type(value[0])

        # if value[0] == '"' and value[-1] == '"':
        #     print(value)
        #     # self.token_list.append(value)
        # Base case for symbol tokens
        if constant == "symbol" and len(value) == 1:
            self.token_list.append(value)
            return
        # Handling symbols recursively
        if constant == "symbol" and len(value) > 1:
            first_half = value[:1]
            second_half = value[1:]
            self.Tokenize(first_half)
            self.Tokenize(second_half)
        # Handling non symbols (alphabets and digits)
        elif constant != "symbol":
            count = 0
            for char in value:
                if self.char_type(char) != constant:
                    first_half = value[:count]
                    second_half = value[count:]
                    self.Tokenize(first_half)
                    self.Tokenize(second_half)
                    return
                count += 1
            self.token_list.append(value)

    def get_XML(self, value):
        """ Tokeni´ying a command """
        """ Words in bracket, words with ; """
        # if self.is_keyword(value):
        #     # print(value)
            # ...
        # if self.is_symbol(value):
        #     # print(value)
        #     ...
        # # elif self.is_identifer(value):
        # #     print(value)
        # if self.is_intConstant(value):
        #     # print(value)
        #     ...
        if self.is_strConstant(value):
            print(value)   
            ...
    
    def generateTokens(self):
        """ Tokenizing each command """
        # print(self.temp_list)
        for item in self.temp_list:
            # print(len(item))
            for value in item:
                x = self.Tokenize(value)

        self.output.append("<tokens>")
        # print(self.token_list)
        # for token in self.token_list:
            # print(token)
            # self.get_XML(token)
            # ...
                # scaning each word and breaking it once a non alphabet chracter is spotted
                # for char in value:
                #     print(char)
                # self.Tokenize(value)
        self.output.append("</tokens>")

def main(directory):
    """ Loading file and directory and handling call from the command line """
    # Handing Directories
    if os.path.isdir(directory):
        files = os.listdir(directory)
        for filename in files:
            if filename.endswith(".jack"):
                # Reconstructing file path
                file_path = os.path.join(directory, filename)
                # print(filename)
                jack_code = load(file_path)
                print(jack_code)

    # Handling single file input
    elif os.path.isfile(directory):
        filename = os.path.basename(directory)
        # print(filename)
        jack_code = load(directory)
        # for i in jack_code:
        #     print(i)
        # print(jack_code)
        x = Tokenizer(jack_code)
        x.parse_Line()
        x.generateTokens()
        # x.is_keyword("null")
        # x.is_symbol("[")
        # x.is_strConstant('"Azeez"')
        # x.is_intConstant("44")
        # x.is_identifer('~Azeez("winner")')

#
if __name__ == "__main__" and len(sys.argv) == 2:
    vm_code_file = sys.argv[1]
    main(vm_code_file)

"""
# Take value
# Get type of the first character in value [alphabet or not alphabet]
# set contant to True if is alphabet
# set contant to False if otherwise
# For each character in value
# if character type is not equal to constant type
# Split value into two
# First half is Character before brekpoint
# Second half is brekpoint plus chareacters after
# call recursive function on both halves
# Base-Case: if all Character matches constant
# On Base-case tokenize and return

# dealing with contant and chaing symbools
# Dealing with a group of symbol
"""

""" 
# true;
# call comp("true;")
# first half is = true
# second hald is = ;
# call comp(true)
    leads to base case
    return tur as key word
# call comp(;)
 return ":" as symbol
"""






            # # Extracting strings 
            # if '"' in item:
            #     print(item)
            #     if item[0] == '"' and item[-1] == '"':
            #         # print(item)
            #         # return
            #         ...
            #     else:
            #         # temp = item.strip().split('"')
            #         # print(temp, len(temp))
            #         # print(item)
            #         count = 0
            #         for char in item:
            #             if char == '"':
            #                 print("in")
            #                 first_half = item[:count]
            #                 second_half = item[count:]
            #                 print(first_half, "FH")
            #                 print(second_half, "SH")
            #             # self.Tokenize(first_half)
            #             # self.Tokenize(second_half)
            #             return
            #         count += 1
            # # for char in item:
            # #     if char == '"':
            # #     #     while char != '"':
            # #     #         print(char)