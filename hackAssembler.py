#!/usr/bin/python

import sys
import argparse
import re

parser = argparse.ArgumentParser(description='Hack assembler')
parser.add_argument('file', metavar='filename', help='input hack asm file')

args=parser.parse_args()

#print(args.file)

asm=open(args.file)

validInstCnt=-1
instList=[]
instType=''
symTable={'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4, 'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5, 'R6': 6, 'R7': 7, 'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11, 'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15, 'SCREEN': 16384, 'KBD': 24576}

aLocation=""
lSymbol=""

for line in asm:
  if re.match(r'^\s*\/\/', line) or re.match(r'^\s*\n', line):
    line=line.strip('\n')
    #print("xxx ignoring comment or blank line", line)
  else:
    line=re.sub(r'\s*\/\/.*', '', line) #removing trailing comment
    #line=re.sub(r'^\s+', '', line) #removing initial whitespace
    #line=re.sub(r'(^.+)\s+', '\1', line) #removing trailing whitespace
    line=line.strip()
    if re.match(r'^\s*\@.+', line):
       validInstCnt=validInstCnt+1
       #print(validInstCnt)
       line=line.strip('\n')
       instType='Acmd'
       #print("A-cmd ", line)
       instList.append((validInstCnt, instType, line))
       #aLocation=re.split(r'\@', instList[i][2], maxsplit=1)[1]
       #if not re.match(r'^\d+', aLocation):
    elif re.match(r'^\s*\(.+\)', line):
       #print(validInstCnt)
       line=line.strip('\n')
       instType='Lcmd'
       #print("L-cmd ", line)
       instList.append((validInstCnt, instType, line))
       lSymbol=re.sub(r'\s*\((.+)\)', r'\1', line)
       symTable[lSymbol]=validInstCnt+1
       #print("pushed symbol: ", lSymbol,  symTable[lSymbol])
    else:
       validInstCnt=validInstCnt+1
       #print(validInstCnt)
       line=line.strip('\n')
       instType='Ccmd'
       #print("C-cmd ", line)    
       instList.append((validInstCnt, instType, line))

#print(symTable)

asm.close()

cDest=""
cComp=""
cJump=""
curFreeLoc=16

outputFile=re.sub(r'(.*)\.asm', r'\1.hack', args.file)
hack=open(outputFile, 'w')

for i in range(len(instList)):
    #print(instList[i])
    if instList[i][1]=='Acmd':
        #print("Acmd: ", instList[i][2])
        aLocation=re.split(r'\@', instList[i][2], maxsplit=1)[1]
        if not re.match(r'^\d+', aLocation):
            if aLocation in symTable.keys():
                #print("symbol found in symbol table: ", aLocation, symTable[aLocation])
                print(format(int(symTable[aLocation]), '016b'), file=hack)
            else:
                symTable[aLocation]=curFreeLoc
                print(format(int(symTable[aLocation]), '016b'), file=hack)
                curFreeLoc=curFreeLoc+1
                #print("symbol not found in symbol table: ", aLocation, symTable[aLocation])
        else:
            print(format(int(aLocation), '016b'), file=hack)

    elif instList[i][1]=='Lcmd':
        #lSymbol=re.sub(r'\s*\((.+)\)', r'\1', instList[i][2])
        #print("Lcmd: ", instList[i][2])
        #print("Symbol: ", lSymbol)
        pass

    else:
        #print("Ccmd: ", instList[i][2])
        if re.match(r'.+;', instList[i][2]):
            #print("; found", instList[i][2])
            cDestComp=re.split(r'\s*;\s*', instList[i][2], maxsplit=1)[0]
            cJump=re.split(r'\s*;\s*', instList[i][2], maxsplit=1)[1]
            #print("cJump: ", cJump)
            if re.match(r'.+=', cDestComp):
                cDest=re.split(r'\s*=\s*', cDestComp, maxsplit=1)[0]
                cComp=re.split(r'\s*=\s*', cDestComp, maxsplit=1)[1]
            else:
                cComp=cDestComp
                cDest=""
        else:
            #print("; not found", instList[i][2])
            cDest=re.split(r'\s*=\s*', instList[i][2], maxsplit=1)[0]
            cComp=re.split(r'\s*=\s*', instList[i][2], maxsplit=1)[1]

        if cDest=="AMD":
            cDest="111"
        elif cDest=="M":
            cDest="001"
        elif cDest=="D":
            cDest="010"
        elif cDest=="MD":
            cDest="011"
        elif cDest=="A":
            cDest="100"
        elif cDest=="AM":
            cDest="101"
        elif cDest=="AD":
            cDest="110"
        else:
            cDest="000"


        if cJump=="JMP":
            cJump="111"
        elif cJump=="JGT":
            cJump="001"
        elif cJump=="JEQ":
            cJump="010"
        elif cJump=="JGE":
            cJump="011"
        elif cJump=="JLT":
            cJump="100"
        elif cJump=="JNE":
            cJump="101"
        elif cJump=="JLE":
            cJump="110"
        else:
            cJump="000"

        
        if cComp=="0":
            cComp="0101010"
        if cComp=="1":
            cComp="0111111"
        if cComp=="-1":
            cComp="0111010"
        if cComp=="D":
            cComp="0001100"
        if cComp=="A":
            cComp="0110000"
        if cComp=="!D":
            cComp="0001101"
        if cComp=="!A":
            cComp="0110001"
        if cComp=="-D":
            cComp="0001111"
        if cComp=="-A":
            cComp="0110011"
        if cComp=="D+1":
            cComp="0011111"
        if cComp=="A+1":
            cComp="0110111"
        if cComp=="D-1":
            cComp="0001110"
        if cComp=="A-1":
            cComp="0110010"
        if cComp=="D+A":
            cComp="0000010"
        if cComp=="D-A":
            cComp="0010011"
        if cComp=="A-D":
            cComp="0000111"
        if cComp=="D&A":
            cComp="0000000"
        if cComp=="D|A":
            cComp="0010101"
        if cComp=="D|M":
            cComp="1010101"
        if cComp=="D&M":
            cComp="1000000"
        if cComp=="M-D":
            cComp="1000111"
        if cComp=="D-M":
            cComp="1010011"
        if cComp=="D+M":
            cComp="1000010"
        if cComp=="M-1":
            cComp="1110010"
        if cComp=="M+1":
            cComp="1110111"
        if cComp=="-M":
            cComp="1110011"
        if cComp=="!M":
            cComp="1110001"
        if cComp=="M":
            cComp="1110000"

        #print("cComp: ", cComp, "cDest: ", cDest, "cJump: ", cJump)
        print("111"+cComp+cDest+cJump, file=hack)

hack.close()
