// Box.asm for K = 57
// Start row = 57 -> Base address = 16384 + (32 * 57) = 18208
// Height = 20 rows
// Width = 16 * ((57 mod 4) + 1) = 32 pixels = 2 words per row

(LOOP)
    @KBD
    D=M
    @SET_WHITE
    D;JEQ

    @color
    M=-1
    @DRAW
    0;JMP

(SET_WHITE)
    @color
    M=0

(DRAW)
    @18208
    D=A
    @addr
    M=D

    @20
    D=A
    @rows
    M=D

(ROW_LOOP)
    @rows
    D=M
    @LOOP
    D;JEQ

    @color
    D=M
    @addr
    A=M
    M=D

    @color
    D=M
    @addr
    A=M+1
    M=D

    @32
    D=A
    @addr
    M=D+M

    @rows
    M=M-1

    @ROW_LOOP
    0;JMP