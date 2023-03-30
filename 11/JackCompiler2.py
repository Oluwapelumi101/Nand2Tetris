""" A program to translate Jack High level language into Jack VM code """

# Handling Directory inputs done
# Bug with string contants: done
# adjust output name
# Implementing parser

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

        "SYBOL":["(", ")", "{", "}", "[", "]", ".", ",", ";", "+", "-", "*", "&", "/", "|", "<", ">", "=", "~"]
    }

    SPECIAL_CHAR ={"<":"&lt;", ">":"&gt;", '"':"&quot;", "&":"&amp;" }

    def __init__(self, code_list):
        """ Stuff """
        self.input = code_list
        self.token_list = []
        self.temp_list = []
        self.output = []

    def temp_function(self, value):
        """ Parser that can handle strings """
        output_list = []
        if '"' in value:
            word_list = re.split(r'("[^"]*")', value)
            for obj in word_list:
                if obj[0] == '"' and obj[-1] == '"':
                        output_list.append(obj)
                if '"' not in obj:
                    temp = obj.strip().split(" ")
                    temp = list(filter(None, temp))
                    output_list = output_list + temp
        else:
            temp = value.strip().split(" ")
            temp = list(filter(None, temp))
            output_list = output_list + temp
        return output_list
            
    def parse_Line(self):
        for item in self.input:
            x = self.temp_function(item)
            self.temp_list.append(x)

    def is_keyword(self, value):
        """ Cheack if a code is a keyword and generate appropraite output """
        keywords = Tokenizer.LEXICAL_DICT["KEYWORD"]
        if value in keywords:
            xml = f"<keyword> {value} </keyword>"
            self.output.append(xml)
            return xml

    def is_symbol(self, value):
        """ Check if a value is a jack symbol and generate xml output """
        symbols = Tokenizer.LEXICAL_DICT["SYBOL"]
        special_char = Tokenizer.SPECIAL_CHAR.keys()
        if value in symbols:
            if value in special_char:
                xml = f"<symbol> {Tokenizer.SPECIAL_CHAR[value]} </symbol>"
            else:
                xml = f"<symbol> {value} </symbol>"
            self.output.append(xml)
            return xml

    def is_identifer(self, value):
        """ Checks is a value is an identifer and generates the xml output """
        if isinstance(value, str) and value[0] != '"' and not value.isdigit():
            xml = f"<identifier> {value} </identifier>"
            self.output.append(xml)
            return xml
  
    def is_strConstant(self, value):
        """ Checks is a value is a String Constant and generates the xml output """
        if isinstance(value, str) and value[0] == '"':
            no_quotes = value[1:-1]
            xml = f"<stringConstant> {no_quotes}  </stringConstant>"
            self.output.append(xml)
            return xml

    def is_intConstant(self, value):
        """ Checks is a value is an Int Constant and generates the xml output """
        # Dealing with trailing ;
        if value.isdigit():
            xml = f"<integerConstant> {value} </integerConstant>"
            self.output.append(xml)
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
        # handling string constant
        if value[0] == '"' and value[-1] == '"':
            self.token_list.append(value)
            return
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
        if self.is_keyword(value):
            # print(value)
            ...
        elif self.is_symbol(value):
            # print(value)
            ...
        elif self.is_identifer(value):
            # print(value)
            ...
        if self.is_intConstant(value):
            # print(value)
            ...
        if self.is_strConstant(value):
            # print(value)   
            ...
    
    def generateTokens(self):
        """ Tokenizing each command """
        for item in self.temp_list:
            for value in item:
                x = self.Tokenize(value)

        for token in self.token_list:
            self.get_XML(token)
        return self.output

# An object to represent the sybol table
class SymbolTable():

    def __init__(self):
        self.symbolTable = {}
        self.fieldCount = 0
        self.staticCount = 0
        self.varCount = 0
        self.argCount = 0

    def define(self, name, type, kind):
        """ Method for adding an identifier to the symbol table """
        #Determing the index value 
        if kind == "static":
            index = self.staticCount
            vm_segment = "static"
            self.staticCount += 1
        elif kind == "field":
            index = self.fieldCount
            vm_segment = "this"
            self.fieldCount += 1
        elif kind == "arg":
            index = self.argCount
            vm_segment = "argument"
            self.argCount += 1
        elif kind == "var":
            index = self.varCount
            vm_segment = "local"
            self.varCount += 1
        
        # Adding the identfier to 
        self.symbolTable.update({name: [type, kind, index, vm_segment]})

    # def indexCount(self, kind):
    #     """ Return the number of identifier of a given kind already defined in the symbol table """
    #     if kind == "STATIC":
    #         index = self.staticCount
    #         print(index)
    #     elif kind == "FIELD":
    #         index = self.fieldCount
    #         print(index)
    #     elif kind == "ARG":
    #         index = self.argCount
    #         print(index)
    #     elif kind == "var":
    #         index = self.varCount
    #         print(index)

    def kindOf(self, name):
        """ Return the kind of a identifier in the symbol table """
        if name in self.symbolTable:
            return self.symbolTable[name][1]
        else:
            return None

    def segmentOf(self, name):
        """ Return the ram segment of a identifier in the symbol table """
        if name in self.symbolTable:
            return self.symbolTable[name][3]
        else:
            return None

    def typeOf(self, name):
        """ Return the type of an identifier in the symbol table """
        if name in self.symbolTable:
            return self.symbolTable[name][0]
        else:
            return None

    def indexOf(self, name):
        """ Return the index of an identifier in the symbol table """
        if name in self.symbolTable:
            return self.symbolTable[name][2]
        else:
            return None        

    def checkRow(self, name, type, kind):
        """ Return the complete row of an identifer in the symbol table as a list """
        if name in self.symbolTable:
            return self.symbolTable[name]
        else:
            return None

    def reset(self):
        """ Reseting symbol table and counters """
        self.symbolTable.clear()
        self.fieldCount = 0
        self.staticCount = 0
        self.varCount = 0
        self.argCount = 0

class VWWriter():

    def __init__(self):
        self.my_list = []
    
    def writePush(segment, index):
        return f"push {segment} {index}"

    def writePop(segment, index):
        return f"pop {segment} {index}"

    def writeArithmetic(command, isUnary = False):
        # Jack commands and their equivalent VM commands
        commands = {"+":"add", "-":"sub", "*":"call Math.multiply 2", "/": "call Math.divide 2", "&amp;":"and", "|":"or", "&lt;":"lt", "&gt;":"gt", "=":"eq", "~":"not", "neg":"neg","&quot;": '"'}

        #Maps a VM unary op command. 
        unary_ops = {'~': 'not', '-': 'neg'}

        if isUnary:
            return f"{unary_ops[command]}"
        
        return f"{commands[command]}"
    
    def writeLabel(label):
        code = 'label ' + label
        return code

    def writeString(string):
        """ 
        Funcion to handle writing strings using the OS constructor String.new(length) and the OS method String.appendChar(nextChar). 
        """
        # A list to hold a commands 
        temp_list = []
        # Pushing  the lenth of the string to the stack
        temp_list.append('push constant ' + str(len(string)))

        # Calling string OS function
        temp_list.append('call String.new 1')
 
        # Pushing each letter in the string to the stack
        for char in string:
            temp_list.append('push constant ' + str(ord(char)))
            temp_list.append('call String.appendChar 2')
        return temp_list 

    def writeGoto(label):
        code = 'goto ' + label
        return code

    def writeIf(label):
        """ Writing if statements """
        code = 'if-goto ' + label
        return code

    def writeCall(class_name, func_name, nVars):
        code = 'call ' +  class_name + '.' + func_name + ' ' + nVars 
        return code

    def writeFunction(class_name, func_name, nVars):
        code = 'function ' +  class_name + '.' + func_name + ' ' + nVars
        return code

    def writeReturn():
        code = 'return'
        return code

    def writeTerm(command):
        temp_list = []
        terms = {'true': 'push constant 0\nnot', 
         'false': 'push constant 0', 
         'null': 'push constant 0', 
         'this': 'push pointer 0'}
        
        temp_list.append(terms[command])
        return temp_list 

class CompilationEngine():
    """ 
    # This class takes in a list of Tokenised Jack code in XML and formats it based on Grammer rules of the jack language
    # Output should be a list of XML statements
    """
    
    def __init__(self, input):
        """ Class initianlization """
        self.All_Tokens = input
        self.output = []
        self.count = 0
        self.current_token_str = self.getCurrentToken()[0]
        self.current_token_list = self.getCurrentToken()[1]
        self.classTable = SymbolTable()
        self.subroutineTable = SymbolTable()
        self.VM_Writer = VWWriter()
        self.VM_codes = []
        self.unary_op = False
        self.if_count = 0
        self._while_count = 0
           
    def compileClass(self):
        """ Compiling class token """
        # Checking that the first token is a valid class declaration
        if self.check("class"):
            self.Advance()

        # Checking the next token is a valid className declaration
        if self.check("className"):
            self.className = self.current_token_list[1] #getting the className
            self.Advance()
        # Checking the next value is a valid "{"
        if self.check("{"):
            self.Advance()
       
        while self.current_token_list[1] != "}":
            if self.check("classVarDec"):
                self.compileClassVarDec()
            elif self.check("subrountineDec"):
                self.compileSubroutine()

        # NB Last token is "}"
        # clearing the class symbol table
        self.classTable.reset()

        # # Development Code
        # print(len(self.VM_codes))
        # print(self.VM_codes)

    def compileClassVarDec(self):
        """ Compiling static variable declaration or field declaration """

        # Obtaining the kind of the identifier (static, field)
        kind = self.current_token_list[1]
        self.Advance()
        
        # Obtaining the type of the identifier (int, char, bool or className)
        if self.check("type"):
            type = self.current_token_list[1]
            self.Advance()

        # Obtaining the name of the identifier
        if self.check("varName"):
            name = self.current_token_list[1]             
            self.Advance()

        # appending identifier to symbol table
        self.classTable.define(name, type, kind)

        # Dealing with cases with several variale names
        while self.current_token_list[1] != ";":
            if self.check(","):
                self.Advance()
            if self.check("varName"):
                # Obtaining the name of the identifier
                name = self.current_token_list[1]

                # appending identifier to symbol table
                self.classTable.define(name, type, kind)
                self.Advance()

        # Consuming the end of line symbol 
        self.Advance()

    def compileSubroutine(self):
        """ 
        Compiling method, function, constructor 
        ('constructor' | 'function' | 'method') ('void' | type) 
        subroutineName '(' parameterList ')' subroutineBody   
        """
        # Getting subroutine type
        self.subroutine_type = self.current_token_list[1]

        # Pushing "this" if subroutine is a method
        if self.subroutine_type == "method":
            name, type, kind = "this", self.className, "arg"
            self.subroutineTable.define(name, type, kind)

        self.Advance()
        # comsuming type or void
        if self.check("type|void"):
            self.Advance()

        # Getting the subrountine name
        if self.check("varName"): 
            self.subroutineName = self.current_token_list[1]
            self.Advance()

        if self.check("("):
            self.Advance()
            self.compileParameterList()

        if self.check(")"):
            self.Advance()
          
        self.compileSubroutineBody()
        
        # Clearing the subroutine symbol table after each subroutine compilation
        self.subroutineTable.reset()
        self.Advance()
    
    def compileParameterList(self):
        """ Compiling parameter list not including parenthesis tokens """
        
        while self.current_token_list[1] != ")":
            if self.check("type"): # checking parameter type
                # Obtaining the type of the identifier (int, char, bool)
                type = self.current_token_list[1]
                self.Advance()
            if self.check("varName"): # checking parameter VarName
                # Obtaining the name of the identifier
                name = self.current_token_list[1]
                self.Advance()

            # Checking if it has been declared before and adding new to symbol table
            if not self.subroutineTable.typeOf(name):
                self.subroutineTable.define(name, type, kind= "arg")

            # Handling more than one parameter variable
            while self.current_token_list[1] != ")":
                if self.check(","):
                    self.Advance()
                if self.check("type"): # checking parameter type
                    # Obtaining the type of the identifier (int, char, bool)
                    type = self.current_token_list[1]
                    self.Advance()
                if self.check("varName"): # checking parameter VarName
                    # Obtaining the name of the identifier
                    name = self.current_token_list[1]  
                    self.Advance()
                # Checking if it has been declared before and adding new to symbol table
                if not self.subroutineTable.typeOf(name):
                    self.subroutineTable.define(name, type, kind= "arg")
        self.Advance()

    def compileSubroutineBody(self):
        """ Compiling the body of a subroutine """

        # consuming curly bracket on subroutine start
        if self.check("{"):
            self.Advance()

        while self.check("varDec"):
            self.compileVarDec()

        # Getting the number of local variables in the subroutine
        nVars = str(self.subroutineTable.varCount)

        # Writing the subroutine in VM Format
        code = VWWriter.writeFunction(self.className, self.subroutineName, nVars)
        self.VM_codes.append(code)

        # Pushing method conditioning code
        if self.subroutine_type == "method":
            code = VWWriter.writePush("argument", "0")
            self.VM_codes.append(code)
            code = VWWriter.writePop("pointer", "0")
            self.VM_codes.append(code)

        elif self.subroutine_type == "constructor":
            # Getting the number of local variables in the subroutine
            nVars = str(self.classTable.fieldCount)
            code = VWWriter.writePush("constant", nVars)
            self.VM_codes.append(code)
            code = VWWriter.writeCall("Memory", "alloc", '1')
            self.VM_codes.append(code)
            code = VWWriter.writePop("pointer", "0")
            self.VM_codes.append(code)

        self.compileStatements()

    def compileVarDec(self):
        """ Compiling var declarations """
        # obtaining the kind of the identifier (var)
        kind = self.current_token_list[1]
        self.Advance()

        if self.check("type"):
            # obtaining the type of the identifier (int, char, bool)
            type = self.current_token_list[1]
            self.Advance()
        if self.check("varName"):
            # obtaining the name of the identifier
            name = self.current_token_list[1]
            self.Advance()

        # appending identifier to symbol table
        self.subroutineTable.define(name, type, kind)

        # Dealing with cases with several variale names
        while self.current_token_list[1] != ";":
            # comsuming "," in multi variable declaration
            if self.check(","):
                self.Advance()
             # obtaining the name of the identifier
            if self.check("varName"):
                name = self.current_token_list[1]
                self.Advance()
            # appending identifier to symbol table
            self.subroutineTable.define(name, type, kind)

        # consuming the end of line symbol 
        self.Advance()

    def compileStatements(self):
        """ Compiling a sequence of statements """
        # Pushing one or more statements
        while self.current_token_list[1] != "}":
            # Handling let statements
            if self.check("let"):
                self.compileLet()

            # Handling do statements
            if self.check("do"):
                self.compileDo()

            # Handling while statements
            if self.check("while"):
                self.compileWhile()

            # Handling if statements
            if self.check("if"):
                self.compileIf()

            # Handling return statements
            if self.check("return"):
                self.compileReturn()                

    def compileLet(self):
        """ Compiling let statement """
        # Consume let keyword
        is_array = False
        self.Advance()

        # Let identifier
        if self.check("varName"):
            identifier_name = self.current_token_list[1]
            identifier_kind = self.getSegment(identifier_name)
            self.Advance()

        # Handling let statements with arrays
        if self.check("["):
            is_array = True
            self.Advance() #eat "["
            self.compileExpression() #expression in the array
            self.Advance()

            code = VWWriter.writePush(identifier_kind[0], identifier_kind[1])
            self.VM_codes.append(code)
            code = VWWriter.writeArithmetic("+")
            self.VM_codes.append(code)

        # Consume "="
        if self.check("="):
            self.Advance()
        
        self.compileExpression()
        
        self.Advance()  # Consume ";"
        
        # Procedure for handling array 
        if is_array:
            code = VWWriter.writePop('temp', '0')
            self.VM_codes.append(code)
            code = VWWriter.writePop('pointer', '1')
            self.VM_codes.append(code)
            code = VWWriter.writePush('temp', '0')
            self.VM_codes.append(code)
            code = VWWriter.writePop('that', '0')
            self.VM_codes.append(code)
        else:
            code = VWWriter.writePop(identifier_kind[0], identifier_kind[1])
            self.VM_codes.append(code)
            
    def compileIf(self):
        """ Compiling if statements """
        self.Advance() #consuming if token
        
        # Incrementing the number of if statments in the class
        if_count = str(self.if_count)
        self.if_count += 1 

        # Handling the condition of the if statement
        if self.check("("):
            self.Advance()
        self.compileExpression()
        if self.check(")"):
            self.Advance()

        # Converting if condition expression to VM 
        code = VWWriter.writeIf("IF_TRUE" + if_count)
        self.VM_codes.append(code)
        code = VWWriter.writeGoto("IF_FALSE" + if_count)
        self.VM_codes.append(code)
        code = VWWriter.writeLabel("IF_TRUE" + if_count)
        self.VM_codes.append(code)

        # Handling the body of the if statement
        if self.check("{"):
            self.Advance()
        self.compileStatements()
        if self.check("}"):
            self.Advance()
        
        # Handling else
        if self.check("else"):
            code = VWWriter.writeGoto("IF_END" + if_count)
            self.VM_codes.append(code)
            code = VWWriter.writeLabel('IF_FALSE' + if_count)
            self.VM_codes.append(code)

            self.Advance() # Cosume "else" token

            # Handling the body of the else statement
            if self.check("{"):
                self.Advance()
            self.compileStatements()
            if self.check("}"):
                self.Advance()

            code = VWWriter.writeLabel('IF_END' + if_count)
            self.VM_codes.append(code)
        else:
            code = VWWriter.writeLabel('IF_FALSE' + if_count)
            self.VM_codes.append(code)

    def compileWhile(self):
        """ Compiling while statements """
        while_count = str(self._while_count)
        self._while_count += 1     

        code = VWWriter.writeLabel('WHILE_EXP' + while_count)
        self.VM_codes.append(code)

        # Consuming the while Token 
        self.Advance()

        # Handling the condition of the while statement
        if self.check("("):
            self.Advance()
        self.compileExpression()
        if self.check(")"):
            self.Advance()

        code = VWWriter.writeArithmetic("~")
        self.VM_codes.append(code)
        code = VWWriter.writeIf('WHILE_END' + while_count)
        self.VM_codes.append(code)
    
        # Handling the body of the while statement
        if self.check("{"):
            self.Advance()
        self.compileStatements()
        if self.check("}"):
            self.Advance()

        code = VWWriter.writeGoto('WHILE_EXP' + while_count)
        self.VM_codes.append(code)
        code = VWWriter.writeLabel('WHILE_END' + while_count)
        self.VM_codes.append(code)

    def compileDo(self):
        """ Compiling do statements """
        # Comsuming Do token
        self.Advance()

        #.......... Subroutine call procedure..........#
        className =  self.className
        num_args = 0

        # Getting and consuming subroutine name
        if self.check("varName"):
            func_name = self.current_token_list[1]
            self.Advance()

        # Checking next is either "(" or "."   /erase() or screen.erase()
        if self.check("."):
            className = func_name

            # Handling object declared as variable
            if self.check_symbolTable(func_name):
                num_args += 1
                identifier_kind = self.getSegment(className)
                className = identifier_kind[2]
                code = VWWriter.writePush(identifier_kind[0], identifier_kind[1])
                self.VM_codes.append(code)
            self.Advance()

            # Getting and consuming method name
            if self.check("varName"): 
                func_name = self.current_token_list[1]
                self.Advance()
        else:
            num_args += 1
            code = VWWriter.writePush('pointer', '0')
            self.VM_codes.append(code)

        if self.check("("): #consume  parenthesis "
            self.Advance()

         # calling expression
        num_args += self.compileExpressionList()

        # Closing Bracket
        if self.check(")"):
            self.Advance()
        #........ End of subroutine procedure ............#

        # Comsuming Line end symbol
        if self.check(";"):
            self.Advance()

        code = VWWriter.writeCall(className, func_name, str(num_args))
        self.VM_codes.append(code)

        code = VWWriter.writePop('temp', '0')
        self.VM_codes.append(code)

    def compileReturn(self):
        """ Compiling return statements """
        # Consuming return token
        if self.check("return"):
            self.Advance()

        if not self.check(";"):
            self.compileExpression()
        else:
            code = VWWriter.writePush('constant', '0')
            self.VM_codes.append(code)

        self.Advance() # consuming ';'

        # Adding return to vm code
        code = VWWriter.writeReturn()
        self.VM_codes.append(code)

    def compileExpression(self):
        """ Compiling an expression statements """
        self.compileTerm()

        while self.check("op"):
            # Handling operation
            operation = self.current_token_list[1]
            self.Advance()
            self.compileTerm()

            # prefix to post fix conversion
            # Appending the operation to output list
            code = VWWriter.writeArithmetic(operation)
            self.VM_codes.append(code)

    def compileTerm(self):
        """ Compiling term  """        
        # Handling term in parenthesis
        if self.check("("):
            self.Advance()
            self.compileExpression() #expression in the parenthesis
            self.Advance()

        # previous = self.prev_token()[1]
        elif self.check("unary"):
            unary_op = self.current_token_list[1]
            self.Advance()
            self.compileTerm()

            operation_VM = VWWriter.writeArithmetic(unary_op, isUnary= True)
            self.VM_codes.append(operation_VM)
        else:
            next = self.next_token()[1]
            is_string = False
            is_term = False

            # Checking for subroutine syntax
            if next[1] == ".":
                #.......... Subroutine call procedure..........#
                className =  self.className
                num_args = 0
                # Getting and consuming subroutine name
                if self.check("varName"):
                    func_name = self.current_token_list[1]
                    self.Advance()

                # Checking next is either "(" or "."   /erase() or screen.erase()
                if self.check("."):
                    className = func_name

                    # Handling object declared as variable
                    if self.check_symbolTable(func_name):
                        num_args += 1
                        identifier_kind = self.getSegment(className)
                        className = identifier_kind[2]
                        code = VWWriter.writePush(identifier_kind[0], identifier_kind[1])
                        self.VM_codes.append(code)
                    self.Advance()

                    # Getting and consuming method name
                    if self.check("varName"): 
                        func_name = self.current_token_list[1]
                        self.Advance()
                else:
                    num_args += 1
                    code = VWWriter.writePush('pointer', '0')
                    self.VM_codes.append(code)

                if self.check("("): #consume  parenthesis "
                    self.Advance()

                # calling expression
                num_args += self.compileExpressionList()

                # Closing Bracket
                if self.check(")"):
                    self.Advance()

                code = VWWriter.writeCall(className, func_name, str(num_args))
                self.VM_codes.append(code)  
                #........ End of subroutine procedure ............#

            # Checking for terms with array expressions
            elif next[1] == "[":
                # Array handling procedure
                if self.check("varName"): 
                    # Getting array Name
                    array_name = self.current_token_list[1]
                    array_as_sysmbol = self.getSegment(array_name)

                    # Comsuming some tokens and compilling expression
                    self.Advance() # cosuming array name token
                    self.Advance() # comsume '['
                    self.compileExpression() #expression in the array
                    self.Advance()  # consume ']'

                    code = VWWriter.writePush(array_as_sysmbol[0], array_as_sysmbol[1])
                    self.VM_codes.append(code)
                    code = VWWriter.writeArithmetic('+')
                    self.VM_codes.append(code)
                    code = VWWriter.writePop('pointer', '1')
                    self.VM_codes.append(code)
                    code = VWWriter.writePush('that', '0') 
                    self.VM_codes.append(code)

            # Handling terms statements with terminal constants INT|STR|KEYWORD|VARNAME
            else:
                if self.check("constant") and next[1] not in [".", "["]:
                    #  Getting the term
                    term = self.current_token_list[1]
                    term_type = self.current_token_list[0]
                    if term_type == "<identifier>":
                        term_to_vm = self.getSegment(term)
                        term_as_vm = VWWriter.writePush(term_to_vm[0], term_to_vm[1])
                        self.Advance()
                    elif term_type == "<integerConstant>":
                        term_to_vm = ("constant", term)
                        term_as_vm = VWWriter.writePush(term_to_vm[0], term_to_vm[1])
                        self.Advance()
                    elif term_type == "<stringConstant>":
                        is_string = True
                        term = " ".join(self.current_token_list[1:-1])
                        term_as_vm = VWWriter.writeString(term)
                        self.Advance()
                    elif term in ['true', 'false', 'null', 'this']:
                        is_term = True
                        term_to_vm = ("constant", term)
                        term_as_vm = VWWriter.writeTerm(term)
                        self.Advance()
                if is_string or is_term:
                    self.VM_codes += term_as_vm
                else:
                    self.VM_codes.append(term_as_vm)

    def compileExpressionList(self):
        """ Compiling list of expressions statements """
        num_args = 0
        if not self.check(")"):
            self.compileExpression()
            num_args += 1
            while not self.check(")"):
                if self.check(","):
                    self.Advance() 
                self.compileExpression()  
                num_args += 1
        return num_args

    def check(self, type):
        """ Check if a value corresponds to ...... """
        if type == "class":
            try:
                if self.current_token_list[0] == "<keyword>" and self.current_token_list[1] == "class":
                    return True
            except:
                return False
        
        if type == "className":
            try:
                if self.current_token_list[0] == "<identifier>":
                    return True
            except:
                return False
        
        if type == "{":
            try:
                if self.current_token_list[0] == "<symbol>" and self.current_token_list[1] == "{":
                    return True
            except:
                return False

        if type == "}":
            try:
                if self.current_token_list[0] == "<symbol>" and self.current_token_list[1] == "}":
                    return True
            except:
                return False

        if type == "(":
            try:
                if self.current_token_list[0] == "<symbol>" and self.current_token_list[1] == "(":
                    return True
            except:
                return False

        if type == ")":
            try:
                if self.current_token_list[0] == "<symbol>" and self.current_token_list[1] == ")":
                    return True
            except:
                return False

        if type == ",":
            try:
                if self.current_token_list[0] == "<symbol>" and self.current_token_list[1] == ",":
                    return True
            except:
                return False

        if type == ";":
            try:
                if self.current_token_list[0] == "<symbol>" and self.current_token_list[1] == ";":
                    return True
            except:
                return False

        if type == "=":
            try:
                if self.current_token_list[0] == "<symbol>" and self.current_token_list[1] == "=":
                    return True
            except:
                return False

        if type == ".":
            try:
                if self.current_token_list[0] == "<symbol>" and self.current_token_list[1] == ".":
                    return True
            except:
                return False

        if type == "[":
            try:
                if self.current_token_list[0] == "<symbol>" and self.current_token_list[1] == "[":
                    return True
            except:
                return False
            
        if type == "op":
            try:
                if self.current_token_list[0] == "<symbol>" and self.current_token_list[1] in ["+", "-", "*", "/", "|", "=", "&lt;", "&gt;", "&amp;",]:
                    return True
            except:
                return False

        if type == "unary":
            try:
                if self.current_token_list[0] == "<symbol>" and self.current_token_list[1] in ["-", "~"]:
                    return True
            except:
                return False
            
        if type == "classVarDec":
            try:
                if self.current_token_list[0] == "<keyword>" and self.current_token_list[1] in ["field", "static"]:
                    return True
            except:
                return False   
        
        if type == "type":
            try:
                if self.current_token_list[0] == "<keyword>" and self.current_token_list[1] in ["int", "char", "boolean"]:
                    return True
                elif self.current_token_list[0] == "<identifier>":
                    return True
            except:
                return False   
        
        if type == "varName":
            try:
                if self.current_token_list[0] == "<identifier>":
                    return True
            except:
                return False

        if type == "subrountineDec":
            try:
                if self.current_token_list[0] == "<keyword>" and self.current_token_list[1] in ["constructor", "function", "method"]:
                    return True
                # elif self.current_token_list[0] == "<identifier>":
                #     return True
            except:
                return False   
 
        if type == "type|void":
            try:
                if self.current_token_list[0] == "<keyword>" and self.current_token_list[1] in ["int", "char", "boolean"]:
                    return True
                elif self.current_token_list[0] == "<identifier>":
                    return True
                elif self.current_token_list[1] == "void":
                    return True            
            except:
                return False   

        if type == "varDec":
            try:
                if self.current_token_list[0] == "<keyword>" and self.current_token_list[1] == "var":
                    return True
            except:
                return False            

        if type == "let":
            try:
                if self.current_token_list[0] == "<keyword>" and self.current_token_list[1] == "let":
                    return True
            except:
                return False    
            
        if type == "do":
            try:
                if self.current_token_list[0] == "<keyword>" and self.current_token_list[1] == "do":
                    return True
            except:
                return False               

        if type == "if":
            try:
                if self.current_token_list[0] == "<keyword>" and self.current_token_list[1] == "if":
                    return True
            except:
                return False    

        if type == "else":
            try:
                if self.current_token_list[0] == "<keyword>" and self.current_token_list[1] == "else":
                    return True
            except:
                return False   
            
        if type == "while":
            try:
                if self.current_token_list[0] == "<keyword>" and self.current_token_list[1] == "while":
                    return True
            except:
                return False    

        if type == "return":
            try:
                if self.current_token_list[0] == "<keyword>" and self.current_token_list[1] == "return":
                    return True
            except:
                return False    

        if type == "constant":
            try:
                constanta = ["<keyword>", "<stringConstant>", "<integerConstant>", "<identifier>"]
                if self.current_token_list[0] in constanta:
                    return True
            except:
                return False   

    def check_symbolTable(self, name):
        """ A function to check if an idenifier is in the symbol tables """
        if self.subroutineTable.typeOf(name):
            return True
        elif self.classTable.typeOf(name):
            return True
        else:
            return False
    
    def getSegment(self, name):
        """ Function to take an identifier and return its kind and index from the symbol table """
        if self.subroutineTable.kindOf(name):
            return (self.subroutineTable.segmentOf(name), self.subroutineTable.indexOf(name), self.subroutineTable.typeOf(name))
        elif self.classTable.typeOf(name):
            return (self.classTable.segmentOf(name), self.classTable.indexOf(name), self.classTable.typeOf(name))
        else:
            return False

    def getCurrentToken(self):
        """ Setting the value of the current token """
        self.current_token_str = self.All_Tokens[self.count] 
        self.current_token_list = self.current_token_str.split(" ")
        return(self.current_token_str, self.current_token_list)

    def Advance(self):
        """ Moving current value to the next term in the token list """
        if self.count < len(self.All_Tokens):
            self.count += 1
        self.getCurrentToken()
        return self.count

    def next_token(self):
        """ Getting the next token to use the term  """
        next_count = self.count + 1
        next_token_str = self.All_Tokens[next_count]
        next_token_list = next_token_str.split(" ")
        return(next_token_str, next_token_list)

    def prev_token(self):
        """ Getting the next token to use the term  """
        next_count = self.count - 1
        next_token_str = self.All_Tokens[next_count]
        next_token_list = next_token_str.split(" ")
        return(next_token_str, next_token_list)

    def compile(self):
        """ Driving the compilsion process """

        # Driving the compilation process
        self.compileClass()
        return(self.VM_codes)

def write_output(list, filename):
    # writing output
    with open(filename, 'w') as f:
        for line in list:
            f.write(f"{line}\n")

def main(directory):
    """ Loading file and directory and handling call from the command line """

    # Handing Directories inputs
    if os.path.isdir(directory):
        files = os.listdir(directory)

        for filename in files:
            if filename.endswith(".jack"):
                # Generating output directory and name
                filename_temp = filename.split(".jack")[0]
                output_name = os.path.basename(os.path.normpath(filename_temp)) + ".vm"
                output_dir = os.path.join(directory, output_name)  

                # Reconstructing file path
                file_path = os.path.join(directory, filename)
                jack_code = load(file_path)
                tokens = Tokenizer(jack_code)
                tokens.parse_Line()
                tokens = tokens.generateTokens()

                # Part 2
                compiled = CompilationEngine(tokens)
                all_xml = compiled.compile()
                write_output(all_xml, output_dir)

    # Handling single file input
    elif os.path.isfile(directory):
        filename = os.path.basename(directory)
        jack_code = load(directory)

        # Generating output name and directory
        output_name = filename.split(".jack")[0] + ".vm"
        path = os.path.dirname(os.path.abspath(directory))
        output_dir = os.path.join(path, output_name)  

        tokens = Tokenizer(jack_code)
        tokens.parse_Line()
        tokens = tokens.generateTokens()

        compiled = CompilationEngine(tokens)
        all_xml = compiled.compile()

        # wrting output 
        write_output(all_xml, output_dir)

if __name__ == "__main__" and len(sys.argv) == 2:
    vm_code_file = sys.argv[1]
    main(vm_code_file)

