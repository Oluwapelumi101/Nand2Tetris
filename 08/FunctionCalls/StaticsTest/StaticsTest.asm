// bootstrap code
@256
D=A
@SP
M=D
// call Sys.init 0
// Pushing return address onto the stack
@Sys.init$ret.0
D=A
@SP
A=M
M=D
@SP
M=M+1
//@LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
//@ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
//@THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
//@THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// ARG = SP-n-5
@SP
D=M
@0
D=D-A
@5
D=D-A
@ARG
M=D
// LCL = SP
@SP
D=M
@LCL
M=D
// goto f
@Sys.init
0;JMP
// (return-address)
(Sys.init$ret.0)
// function Class1.set 0
(Class1.set)
// push argument 0
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// pop static 0
@SP
M=M-1
A=M
D=M
@Class1.vm0
M=D
// push argument 1
@1
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// pop static 1
@SP
M=M-1
A=M
D=M
@Class1.vm1
M=D
// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// return
@LCL
D=M
@frame
M=D
@5
D=D-A
A=D
D=M
@return_address
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D 
@1
D=A
@frame
D=M-D
A=D
D=M
@THAT
M=D
@2
D=A
@frame
D=M-D
A=D
D=M
@THIS
M=D
@3
D=A
@frame
D=M-D
A=D
D=M
@ARG
M=D
@4
D=A
@frame
D=M-D
A=D
D=M
@LCL
M=D
@return_address
A=M
0;JMP
// function Class1.get 0
(Class1.get)
// push static 0
@Class1.vm0
D=M
@SP
A=M
M=D
@SP
M=M+1
// push static 1
@Class1.vm1
D=M
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
M=M-1
A=M
D=M
@6
M=D
@SP
M=M-1
A=M
D=M
@6
D=D-M
@SP
A=M
M=D
@SP
M=M+1
// return
@LCL
D=M
@frame
M=D
@5
D=D-A
A=D
D=M
@return_address
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D 
@1
D=A
@frame
D=M-D
A=D
D=M
@THAT
M=D
@2
D=A
@frame
D=M-D
A=D
D=M
@THIS
M=D
@3
D=A
@frame
D=M-D
A=D
D=M
@ARG
M=D
@4
D=A
@frame
D=M-D
A=D
D=M
@LCL
M=D
@return_address
A=M
0;JMP
// function Sys.init 0
(Sys.init)
// push constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 8
@8
D=A
@SP
A=M
M=D
@SP
M=M+1
// call Class1.set 2
// Pushing return address onto the stack
@Class1.set$ret.3
D=A
@SP
A=M
M=D
@SP
M=M+1
//@LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
//@ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
//@THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
//@THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// ARG = SP-n-5
@SP
D=M
@2
D=D-A
@5
D=D-A
@ARG
M=D
// LCL = SP
@SP
D=M
@LCL
M=D
// goto f
@Class1.set
0;JMP
// (return-address)
(Class1.set$ret.3)
// pop temp 0
@5
D=A
@0
D=D+A
@address_4
M=D
@SP
M=M-1
A=M
D=M
@address_4
A=M
M=D
// push constant 23
@23
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 15
@15
D=A
@SP
A=M
M=D
@SP
M=M+1
// call Class2.set 2
// Pushing return address onto the stack
@Class2.set$ret.7
D=A
@SP
A=M
M=D
@SP
M=M+1
//@LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
//@ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
//@THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
//@THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// ARG = SP-n-5
@SP
D=M
@2
D=D-A
@5
D=D-A
@ARG
M=D
// LCL = SP
@SP
D=M
@LCL
M=D
// goto f
@Class2.set
0;JMP
// (return-address)
(Class2.set$ret.7)
// pop temp 0
@5
D=A
@0
D=D+A
@address_8
M=D
@SP
M=M-1
A=M
D=M
@address_8
A=M
M=D
// call Class1.get 0
// Pushing return address onto the stack
@Class1.get$ret.9
D=A
@SP
A=M
M=D
@SP
M=M+1
//@LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
//@ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
//@THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
//@THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// ARG = SP-n-5
@SP
D=M
@0
D=D-A
@5
D=D-A
@ARG
M=D
// LCL = SP
@SP
D=M
@LCL
M=D
// goto f
@Class1.get
0;JMP
// (return-address)
(Class1.get$ret.9)
// call Class2.get 0
// Pushing return address onto the stack
@Class2.get$ret.10
D=A
@SP
A=M
M=D
@SP
M=M+1
//@LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
//@ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
//@THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
//@THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// ARG = SP-n-5
@SP
D=M
@0
D=D-A
@5
D=D-A
@ARG
M=D
// LCL = SP
@SP
D=M
@LCL
M=D
// goto f
@Class2.get
0;JMP
// (return-address)
(Class2.get$ret.10)
// label WHILE
(WHILE)
// goto WHILE
@WHILE
0;JMP
// function Class2.set 0
(Class2.set)
// push argument 0
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// pop static 0
@SP
M=M-1
A=M
D=M
@Class2.vm0
M=D
// push argument 1
@1
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// pop static 1
@SP
M=M-1
A=M
D=M
@Class2.vm1
M=D
// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// return
@LCL
D=M
@frame
M=D
@5
D=D-A
A=D
D=M
@return_address
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D 
@1
D=A
@frame
D=M-D
A=D
D=M
@THAT
M=D
@2
D=A
@frame
D=M-D
A=D
D=M
@THIS
M=D
@3
D=A
@frame
D=M-D
A=D
D=M
@ARG
M=D
@4
D=A
@frame
D=M-D
A=D
D=M
@LCL
M=D
@return_address
A=M
0;JMP
// function Class2.get 0
(Class2.get)
// push static 0
@Class2.vm0
D=M
@SP
A=M
M=D
@SP
M=M+1
// push static 1
@Class2.vm1
D=M
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
M=M-1
A=M
D=M
@6
M=D
@SP
M=M-1
A=M
D=M
@6
D=D-M
@SP
A=M
M=D
@SP
M=M+1
// return
@LCL
D=M
@frame
M=D
@5
D=D-A
A=D
D=M
@return_address
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D 
@1
D=A
@frame
D=M-D
A=D
D=M
@THAT
M=D
@2
D=A
@frame
D=M-D
A=D
D=M
@THIS
M=D
@3
D=A
@frame
D=M-D
A=D
D=M
@ARG
M=D
@4
D=A
@frame
D=M-D
A=D
D=M
@LCL
M=D
@return_address
A=M
0;JMP
