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
            # print(item)
            x = self.temp_function(item)
            # print(x)
            self.temp_list.append(x)
        # print(self.temp_list)

    def is_keyword(self, value):
        """ Cheack if a code is a keyword and generate appropraite output """
        keywords = Tokenizer.LEXICAL_DICT["KEYWORD"]
        if value in keywords:
            xml = f"<keyword> {value} </keyword>"
            # print(xml)
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
            # print(xml)
            self.output.append(xml)
            return xml

    def is_identifer(self, value):
        """ Checks is a value is an identifer and generates the xml output """
        if isinstance(value, str) and value[0] != '"' and not value.isdigit():
            xml = f"<identifier> {value} </identifier>"
            # print(xml)
            self.output.append(xml)
            return xml
  
    def is_strConstant(self, value):
        """ Checks is a value is a String Constant and generates the xml output """
        if isinstance(value, str) and value[0] == '"':
            no_quotes = value[1:-1]
            xml = f"<stringConstant> {no_quotes}  </stringConstant>"
            # print(xml)
            self.output.append(xml)
            return xml

    def is_intConstant(self, value):
        """ Checks is a value is an Int Constant and generates the xml output """
        # Dealing with trailing ;
        if value.isdigit():
            xml = f"<integerConstant> {value} </integerConstant>"
            # print(xml)
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
            # print(value)
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
        # print(self.temp_list)
        for item in self.temp_list:
            # print(len(item))
            for value in item:
                # print(value)
                x = self.Tokenize(value)
        # print(self.token_list)

        # self.output.append("<tokens>")
        for token in self.token_list:
            # print(token)
            self.get_XML(token)
        # self.output.append("</tokens>")
        # print((self.output))
        return self.output

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
           
    def compileClass(self):
        """ Compiling class token """
        # Checking that the first token is a valid class declaration
        if self.check("class"):
            self.output.append("<class>")
            self.output.append(self.current_token_str)
            self.Advance()
        # Checking the next token is a valid className declaration
        if self.check("className"):
            self.output.append(self.current_token_str)
            self.Advance()
        # Checking the next value is a valid "{"
        if self.check("{"):
            self.output.append(self.current_token_str)
            self.Advance()
       
        while self.current_token_list[1] != "}":
            if self.check("classVarDec"):
                self.compileClassVarDec()
            elif self.check("subrountineDec"):
                self.compileSubroutine()
        # Pushing close bracket and ending call
        self.output.append(self.current_token_str)
        self.output.append("</class>")

    def compileClassVarDec(self):
        """ Compiling static variable declaration or field declaration """
        # print("classVarDec")
        # Pushing <classVarDec> as class tag
        self.output.append("<classVarDec>")
        # Pushing current value (Static|Field)
        self.output.append(self.current_token_str)
        self.Advance()
        if self.check("type"):
            # print(self.current_token_str)
            self.output.append(self.current_token_str)
            self.Advance()
        if self.check("varName"):
            # print(self.current_token_str)
            self.output.append(self.current_token_str)
            self.Advance()
        # Dealing with cases with several variale names
        while self.current_token_list[1] != ";":
            if self.check(","):
                self.output.append(self.current_token_str)
                self.Advance()
            if self.check("varName"):
                # print(self.current_token_str)
                self.output.append(self.current_token_str)
                self.Advance()
        # Adding the end of line symbol 
        # if self.check(";"): 
        self.output.append(self.current_token_str)
        self.output.append("</classVarDec>")
        self.Advance()

    def compileSubroutine(self):
        """ Compiling method, function, constructor """
        # Adding class tag
        self.output.append("<subroutineDec>")
        self.output.append(self.current_token_str)
        # print(self.current_token_str)
        self.Advance()
        if self.check("type|void"):
            # print(self.current_token_str)
            self.output.append(self.current_token_str)
            self.Advance()
        if self.check("varName"): # checking subrountine name
            self.output.append(self.current_token_str)
            self.Advance()
        if self.check("("):
            self.output.append(self.current_token_str)
            self.Advance()
            self.compileParameterList()
        if self.check(")"):
            self.output.append(self.current_token_str)
            self.Advance()
            self.compileParameterList()
        self.compileSubroutineBody()
        self.output.append("</subroutineDec>")
        self.Advance()
    
    def compileParameterList(self):
        """ Compiling parameter list not including parenthesis tokens </parameterList>  """
        # print(self.current_token_str)
        self.output.append("<parameterList>")
        while self.current_token_list[1] != ")":
            if self.check("type"): # checking parameter type
                self.output.append(self.current_token_str)
                self.Advance()
            if self.check("varName"): # checking parameter VarName
                self.output.append(self.current_token_str)
                self.Advance()
            # Handling more than one parameter variable
            while self.current_token_list[1] != ")":
                if self.check(","):
                    self.output.append(self.current_token_str)
                    self.Advance()
                if self.check("type"): # checking parameter type
                    self.output.append(self.current_token_str)
                    self.Advance()
                if self.check("varName"): # checking parameter VarName
                    self.output.append(self.current_token_str)
                    self.Advance()
        self.output.append("</parameterList>")      
        # if self.check(")"):
        self.output.append(self.current_token_str)
        self.Advance()

    def compileSubroutineBody(self):
        """ Compiling the body of a subroutine """
        self.output.append("<subroutineBody>")
        if self.check("{"):
            self.output.append(self.current_token_str)
            self.Advance()
        while self.current_token_list[1] != "}":
            if self.check("varDec"):
                self.compileVarDec()
            else:
                self.compileStatements()
        self.output.append(self.current_token_str) #adding "}"
        # print(self.output)
        # print(self.current_token_str)
        self.output.append("</subroutineBody>")

    def compileVarDec(self):
        """ Compiling var declarations """
        # Pushing <varDec> as class tag
        self.output.append("<varDec>")
        # Pushing current value (var)
        self.output.append(self.current_token_str)
        self.Advance()
        if self.check("type"):
            # print(self.current_token_str)
            self.output.append(self.current_token_str)
            self.Advance()
        if self.check("varName"):
            # print(self.current_token_str)
            self.output.append(self.current_token_str)
            self.Advance()
        # Dealing with cases with several variale names
        while self.current_token_list[1] != ";":
            if self.check(","):
                self.output.append(self.current_token_str)
                self.Advance()
            if self.check("varName"):
                # print(self.current_token_str)
                self.output.append(self.current_token_str)
                self.Advance()
        # Adding the end of line symbol 
        # if self.check(";"): 
        self.output.append(self.current_token_str)
        self.output.append("</varDec>")
        self.Advance()

    def compileStatements(self):
        """ Compiling a sequence of statements """
        self.output.append("<statements>")
        # Pushing one or more statements
        while self.current_token_list[1] != "}":
            # Handling let statements
            if self.check("let"):
                # print(self.current_token_str)
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
        self.output.append("</statements>")

    def compileLet(self):
        """ Compiling let statement """
        # Pushing let tag 
        self.output.append("<letStatement>")
        # print(self.current_token_str)
        self.output.append(self.current_token_str)  #let keyword
        self.Advance()
        if self.check("varName"):
            # print(self.current_token_str)
            self.output.append(self.current_token_str)
            self.Advance()
        # handling expression 0 or one times
        if not self.check("="):
            self.compileExpression()
        if self.check("="):
            # print(self.current_token_str)
            self.output.append(self.current_token_str)
            self.Advance()
        self.compileExpression()
        self.output.append(self.current_token_str) # pushing ';' 
        self.output.append("</letStatement>")
        self.Advance() 

    def compileIf(self):
        """ Compiling if statements """
        # Pushing if tag 
        self.output.append("<ifStatement>")
        self.output.append(self.current_token_str) #pushing the if keyword
        self.Advance()
        
        # Handling the condition of the if statement
        if self.check("("):
            self.output.append(self.current_token_str)
            self.Advance()
        self.compileExpression()
        if self.check(")"):
            self.output.append(self.current_token_str)
            self.Advance()

        # Handling the body of the if statement
        if self.check("{"):
            self.output.append(self.current_token_str)
            self.Advance()
        self.compileStatements()
        if self.check("}"):
            self.output.append(self.current_token_str)
            self.Advance()
        
        # Handling else
        if self.check("else"):
            self.output.append(self.current_token_str)
            self.Advance()

            # Handling the body of the else statement
            if self.check("{"):
                self.output.append(self.current_token_str)
                self.Advance()
            self.compileStatements()
            if self.check("}"):
                self.output.append(self.current_token_str)
                self.Advance()
        self.output.append("</ifStatement>")

    def compileWhile(self):
        """ Compiling while statements """
        # Pushing while tag 
        self.output.append("<whileStatement>")
        self.output.append(self.current_token_str) #pushing the while keyword
        self.Advance()

        # Handling the condition of the while statement
        if self.check("("):
            self.output.append(self.current_token_str)
            self.Advance()
        self.compileExpression()
        if self.check(")"):
            self.output.append(self.current_token_str)
            self.Advance()

        # Handling the body of the while statement
        if self.check("{"):
            self.output.append(self.current_token_str)
            self.Advance()
        self.compileStatements()
        if self.check("}"):
            self.output.append(self.current_token_str)
            self.Advance()

        self.output.append("</whileStatement>")

    def compileDo(self):
        """ Compiling do statements """
        # Pushing <doStatement> tag
        self.output.append("<doStatement>")
        self.output.append(self.current_token_str) # do keyword
        self.Advance()
        # Subroutine call procedure
        if self.check("varName"): #Checking and Pushing subroutine Name or classname or varname
            self.output.append(self.current_token_str)
            self.Advance()

        # Checking next is either "(" or "."   /erase() or screen.erase()
        if self.check("."):
            self.output.append(self.current_token_str) #pushing "."
            self.Advance()
            if self.check("varName"): #Checking and Pushing classname or varname
                self.output.append(self.current_token_str)
                self.Advance()

        if self.check("("): #Checking if next is parenthesis 
            self.output.append(self.current_token_str) #pushing "("
            self.Advance()

         # calling expression
        self.compileExpressionList()
        # Closing Bracket
        if self.check(")"):
            self.output.append(self.current_token_str) #pushing ")"
            self.Advance()
        # Line end symbol
        if self.check(";"):
            self.output.append(self.current_token_str) #pushing ";"
            self.Advance()
        self.output.append("</doStatement>")

    def compileReturn(self):
        """ Compiling return statements """
        # Pushing retur tag 
        self.output.append("<returnStatement>")

        if self.check("return"):
            self.output.append(self.current_token_str) #pushing return keyword
            self.Advance()
        if not self.check(";"):
            self.compileExpression()
        self.output.append(self.current_token_str) 
        
        self.output.append("</returnStatement>")
        self.Advance()

    def compileExpression(self):
        """ Compiling an expression statements """
        self.output.append("<expression>")
        self.compileTerm()
        while self.check("op"):
            # Handling operation
            self.output.append(self.current_token_str)
            self.Advance()
            self.compileTerm()
        self.output.append("</expression>")
        # self.output.append(self.current_token_str)
        # self.Advance()

    def compileTerm(self):
        """ Compiling term  """
        # Term tag
        self.output.append("<term>")
        # Term value
        self.output.append(self.current_token_str)
        self.output.append("</term>")
        self.Advance()
  
    def compileExpressionList(self):
        """ Compiling list of expressions statements """
        # Expression list tag
        self.output.append("<expressionList>")
        if not self.check(")"):
            self.compileExpression
            while not self.check(")"):
                if self.check(","):
                    self.output.append(self.current_token_str) #pushing ","
                    self.Advance() 
                self.compileExpression()         
        self.output.append("</expressionList>")
        # self.Advance()

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

        if type == "op":
            try:
                if self.current_token_list[0] == "<symbol>" and self.current_token_list[1] in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
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

    def compile(self):
        """ Driving the compilsion process """
        """  
        # num_of_tokens = len(self.All_Tokens)
        # count = 0
        # while count < num_of_tokens:
        #     current_token = self.All_Tokens[count]
        #     print(current_token)
        #     self.check("class", current_token)
        #     count += 1 
        # for i in range(5):
        #     current_token = self.getCurrentToken()
        #     print(current_token)
        #     self.Advance()
        """
        
        # Step One Calling Compile method
        self.compileClass()
        return(self.output)


def write_output(list, filename):
    # writing output
    with open(filename, 'w') as f:
        for line in list:
            f.write(f"{line}\n")

def main(directory):
    """ Loading file and directory and handling call from the command line """

    # Handing Directories inputs
    print('######')
    if os.path.isdir(directory):
        files = os.listdir(directory)

        # # Generating output directory and name
        # output_name = os.path.basename(os.path.normpath(directory)) + "M.xml"
        # output_dir = os.path.join(directory, output_name)  

        for filename in files:
            if filename.endswith(".jack"):
                # Generating output directory and name
                output_name = os.path.basename(os.path.normpath(filename)) + "M.xml"
                output_dir = os.path.join(directory, output_name)  

                # Reconstructing file path
                file_path = os.path.join(directory, filename)
                # print(filename)
                jack_code = load(file_path)
                # print(jack_code)
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
        # print(filename)
        jack_code = load(directory)

        # Generating output name and directory
        output_name = filename.split(".vm")[0] + "M.xml"
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

