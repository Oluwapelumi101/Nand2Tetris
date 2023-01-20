// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

// Put your code here.

(MAIN)  //infinite loops to monitor keyboard input
@n //monitoring keyboard
M=0

@KBD // Keyboard input
D=M

@WHITE
D;JEQ


// Handling screen blackout
(DARK)
@i 
M=0

@SCREEN //16384
D=A

(LOOP)
@KBD        // Keyboard input
D=M

@WHITE
D;JEQ

@SCREEN //16384
D=A

@i
A=D+M
M=-1

@i
M=M+1
D=M

@8192
D=D-A
@MAIN
D;JGT // if D is 0 goto end

@LOOP
0;JMP


// Handling screen whiten
(WHITE)
@w //ilterator
M=0

@SCREEN //16384
D=A

(WLOOP)
@KBD    // Ensuring empty keyboard on every loop
D=M

@DARK
D;JNE

@SCREEN //16384
D=A

@w
A=D+M
M=0

@w
M=M+1
D=M

@8192
D=D-A
@MAIN
D;JGT // if D is 0 goto end

@WLOOP
0;JMP


@MAIN //Keyboard infinti loop
0;JMP
