#!/usr/bin/python

import sys
import argparse
import re
import os

def processPush(pushInst, fh):
    global fStr
    print("//VM inst: ", pushInst, file=fh)
    pushCmd=pushInst.strip("push")
    pushCmd=pushCmd.strip() #remove any trailing, leading spaces
    if re.match(r'constant', pushCmd):
        pushCmd=pushCmd.strip("constant")
        pushCmd=pushCmd.strip()
        print("@"+pushCmd, file=fh)
        print("D=A", file=fh)
        print("@SP", file=fh)
        print("A=M", file=fh)
        print("M=D", file=fh)
        print("@SP", file=fh)
        print("M=M+1", file=fh)
    elif re.match(r'local', pushCmd):
        pushCmd=pushCmd.strip("local")
        pushCmd=pushCmd.strip()
        print("@"+pushCmd, file=fh)
        print("D=A", file=fh)
        print("@LCL", file=fh)
        print("A=D+M", file=fh)
        print("D=M", file=fh)
        print("@SP", file=fh)
        print("A=M", file=fh)
        print("M=D", file=fh)
        print("@SP", file=fh)
        print("M=M+1", file=fh)
    elif re.match(r'argument', pushCmd):
        pushCmd=pushCmd.strip("argument")
        pushCmd=pushCmd.strip()
        print("@"+pushCmd, file=fh)
        print("D=A", file=fh)
        print("@ARG", file=fh)
        print("A=D+M", file=fh)
        print("D=M", file=fh)
        print("@SP", file=fh)
        print("A=M", file=fh)
        print("M=D", file=fh)
        print("@SP", file=fh)
        print("M=M+1", file=fh)
    elif re.match(r'this', pushCmd):
        pushCmd=pushCmd.strip("this")
        pushCmd=pushCmd.strip()
        print("@"+pushCmd, file=fh)
        print("D=A", file=fh)
        print("@THIS", file=fh)
        print("A=D+M", file=fh)
        print("D=M", file=fh)
        print("@SP", file=fh)
        print("A=M", file=fh)
        print("M=D", file=fh)
        print("@SP", file=fh)
        print("M=M+1", file=fh)
    elif re.match(r'that', pushCmd):
        pushCmd=pushCmd.strip("that")
        pushCmd=pushCmd.strip()
        print("@"+pushCmd, file=fh)
        print("D=A", file=fh)
        print("@THAT", file=fh)
        print("A=D+M", file=fh)
        print("D=M", file=fh)
        print("@SP", file=fh)
        print("A=M", file=fh)
        print("M=D", file=fh)
        print("@SP", file=fh)
        print("M=M+1", file=fh)
    elif re.match(r'static', pushCmd):
        pushCmd=pushCmd.strip("static")
        pushCmd=pushCmd.strip()
        print("@"+fStr+"."+pushCmd, file=fh)
        print("D=M", file=fh)
        print("@SP", file=fh)
        print("A=M", file=fh)
        print("M=D", file=fh)
        print("@SP", file=fh)
        print("M=M+1", file=fh)
    elif re.match(r'temp', pushCmd):
        pushCmd=pushCmd.strip("temp")
        pushCmd=pushCmd.strip()
        print("@"+pushCmd, file=fh)
        print("D=A", file=fh)
        print("@5", file=fh)
        print("A=D+A", file=fh)
        print("D=M", file=fh)
        print("@SP", file=fh)
        print("A=M", file=fh)
        print("M=D", file=fh)
        print("@SP", file=fh)
        print("M=M+1", file=fh)
    elif re.match(r'pointer', pushCmd):
        pushCmd=pushCmd.strip("pointer")
        pushCmd=pushCmd.strip()
        if pushCmd=="0":
            print("@THIS", file=fh)
            print("D=M", file=fh)
            print("@SP", file=fh)
            print("A=M", file=fh)
            print("M=D", file=fh)
            print("@SP", file=fh)
            print("M=M+1", file=fh)
        else:
            print("@THAT", file=fh)
            print("D=M", file=fh)
            print("@SP", file=fh)
            print("A=M", file=fh)
            print("M=D", file=fh)
            print("@SP", file=fh)
            print("M=M+1", file=fh)
    else:
        print("push cmd not supported yet", pushInst)
    return


def processPop(popInst, fh):
    print("//VM inst: ", popInst, file=fh)
    popCmd=popInst.strip("pop")
    popCmd=popCmd.strip() #remove any trailing, leading spaces
    if re.match(r'local', popCmd):
        popCmd=popCmd.strip("local")
        popCmd=popCmd.strip()
        print("@SP", file=fh)
        print("A=M-1", file=fh)
        print("D=M", file=fh)
        print("@R14", file=fh)
        print("M=D", file=fh) #SP-1 pointer value saved in R14
        print("@"+popCmd, file=fh)
        print("D=A", file=fh)
        print("@LCL", file=fh)
        print("D=D+M", file=fh)
        print("@R15", file=fh)
        print("M=D", file=fh) #local + index address saved in R15
        print("@R14", file=fh)
        print("D=M", file=fh)
        print("@R15", file=fh)
        print("A=M", file=fh)
        print("M=D", file=fh)
        print("@SP", file=fh)
        print("M=M-1", file=fh)
    elif re.match(r'argument', popCmd):
        popCmd=popCmd.strip("argument")
        popCmd=popCmd.strip()
        print("@SP", file=fh)
        print("A=M-1", file=fh)
        print("D=M", file=fh)
        print("@R14", file=fh)
        print("M=D", file=fh) #SP-1 pointer value saved in R14
        print("@"+popCmd, file=fh)
        print("D=A", file=fh)
        print("@ARG", file=fh)
        print("D=D+M", file=fh)
        print("@R15", file=fh)
        print("M=D", file=fh) #local + index address saved in R15
        print("@R14", file=fh)
        print("D=M", file=fh)
        print("@R15", file=fh)
        print("A=M", file=fh)
        print("M=D", file=fh)
        print("@SP", file=fh)
        print("M=M-1", file=fh)
    elif re.match(r'this', popCmd):
        popCmd=popCmd.strip("this")
        popCmd=popCmd.strip()
        print("@SP", file=fh)
        print("A=M-1", file=fh)
        print("D=M", file=fh)
        print("@R14", file=fh)
        print("M=D", file=fh) #SP-1 pointer value saved in R14
        print("@"+popCmd, file=fh)
        print("D=A", file=fh)
        print("@THIS", file=fh)
        print("D=D+M", file=fh)
        print("@R15", file=fh)
        print("M=D", file=fh) #local + index address saved in R15
        print("@R14", file=fh)
        print("D=M", file=fh)
        print("@R15", file=fh)
        print("A=M", file=fh)
        print("M=D", file=fh)
        print("@SP", file=fh)
        print("M=M-1", file=fh)
    elif re.match(r'that', popCmd):
        popCmd=popCmd.strip("that")
        popCmd=popCmd.strip()
        print("@SP", file=fh)
        print("A=M-1", file=fh)
        print("D=M", file=fh)
        print("@R14", file=fh)
        print("M=D", file=fh) #SP-1 pointer value saved in R14
        print("@"+popCmd, file=fh)
        print("D=A", file=fh)
        print("@THAT", file=fh)
        print("D=D+M", file=fh)
        print("@R15", file=fh)
        print("M=D", file=fh) #local + index address saved in R15
        print("@R14", file=fh)
        print("D=M", file=fh)
        print("@R15", file=fh)
        print("A=M", file=fh)
        print("M=D", file=fh)
        print("@SP", file=fh)
        print("M=M-1", file=fh)
    elif re.match(r'static', popCmd):
        popCmd=popCmd.strip("static")
        popCmd=popCmd.strip()
        print("@SP", file=fh)
        print("A=M-1", file=fh)
        print("D=M", file=fh)
        print("@"+fStr+"."+popCmd, file=fh)
        print("M=D", file=fh)
        print("@SP", file=fh)
        print("M=M-1", file=fh)
    elif re.match(r'temp', popCmd):
        popCmd=popCmd.strip("temp")
        popCmd=popCmd.strip()
        print("@"+popCmd, file=fh)
        print("D=A", file=fh)
        print("@5", file=fh)
        print("D=D+A", file=fh)
        print("@R14", file=fh)
        print("M=D", file=fh)
        print("@SP", file=fh)
        print("A=M-1", file=fh)
        print("D=M", file=fh)
        print("@R14", file=fh)
        print("A=M", file=fh)
        print("M=D", file=fh)
        print("@SP", file=fh)
        print("M=M-1", file=fh)
    elif re.match(r'pointer', popCmd):
        popCmd=popCmd.strip("pointer")
        popCmd=popCmd.strip()
        if popCmd=="0":
            print("@SP", file=fh)
            print("A=M-1", file=fh)
            print("D=M", file=fh)
            print("@THIS", file=fh)
            print("M=D", file=fh)
            print("@SP", file=fh)
            print("M=M-1", file=fh)
        else:
            print("@SP", file=fh)
            print("A=M-1", file=fh)
            print("D=M", file=fh)
            print("@THAT", file=fh)
            print("M=D", file=fh)
            print("@SP", file=fh)
            print("M=M-1", file=fh)
    else:
        print("pop cmd not supported yet", popCmd)
    return


def processArithlogic(alInst, instCnt, fh):
    global eqCallCnt
    global gtCallCnt
    global ltCallCnt

    print("//VM inst: ", alInst, file=fh)
    alCmd=alInst.strip()
    i=str(instCnt)
    if re.match(r'add', alCmd):
        print("@SP", file=fh)
        print("A=M-1", file=fh)
        print("D=M", file=fh) #value y, SP--
        print("A=A-1", file=fh)
        print("M=D+M", file=fh) #value x+y, SP--
        print("@SP", file=fh)
        print("M=M-1", file=fh)
        
    elif re.match(r'sub', alCmd):
        print("@SP", file=fh)
        print("A=M-1", file=fh)
        print("D=M", file=fh)
        print("A=A-1", file=fh)
        print("M=M-D", file=fh)
        print("@SP", file=fh)
        print("M=M-1", file=fh)

    elif re.match(r'and', alCmd):
        print("@SP", file=fh)
        print("A=M-1", file=fh)
        print("D=M", file=fh)
        print("A=A-1", file=fh)
        print("M=D&M", file=fh)
        print("@SP", file=fh)
        print("M=M-1", file=fh)

    elif re.match(r'or', alCmd):
        print("@SP", file=fh)
        print("A=M-1", file=fh)
        print("D=M", file=fh)
        print("A=A-1", file=fh)
        print("M=D|M", file=fh)
        print("@SP", file=fh)
        print("M=M-1", file=fh)

    elif re.match(r'neg', alCmd):
        print("@SP", file=fh)
        print("A=M-1", file=fh)
        print("M=-M", file=fh)

    elif re.match(r'not', alCmd):
        print("@SP", file=fh)
        print("A=M-1", file=fh)
        print("M=!M", file=fh)

    elif re.match(r'eq', alCmd):
        print("@SP", file=fh)
        print("A=M-1", file=fh)
        print("D=M", file=fh)
        print("A=A-1", file=fh)
        print("D=M-D", file=fh)
        print("@SET_EQ_TRUE"+str(eqCallCnt), file=fh)
        print("D;JEQ", file=fh)
        print("@SET_EQ_FALSE"+str(eqCallCnt), file=fh)
        print("0;JMP", file=fh)

        print("(SET_EQ_TRUE"+str(eqCallCnt)+")", file=fh)
        print("@SP", file=fh)
        print("A=M-1", file=fh)
        print("A=A-1", file=fh)
        print("M=-1", file=fh)
        print("@SP", file=fh)
        print("M=M-1", file=fh)
        print("@NEXT_"+i, file=fh)
        print("0;JMP", file=fh)

        print("(SET_EQ_FALSE"+str(eqCallCnt)+")", file=fh)
        print("@SP", file=fh)
        print("A=M-1", file=fh)
        print("A=A-1", file=fh)
        print("M=0", file=fh)
        print("@SP", file=fh)
        print("M=M-1", file=fh)
        print("@NEXT_"+i, file=fh)
        print("0;JMP", file=fh)

        print("(NEXT_"+i+")", file=fh)
        eqCallCnt=eqCallCnt+1

    elif re.match(r'gt', alCmd):
        print("@SP", file=fh)
        print("A=M-1", file=fh)
        print("D=M", file=fh)
        print("A=A-1", file=fh)
        print("D=M-D", file=fh)
        print("@SET_GT_TRUE"+str(gtCallCnt), file=fh)
        print("D;JGT", file=fh)
        print("@SET_GT_FALSE"+str(gtCallCnt), file=fh)
        print("0;JMP", file=fh)

        print("(SET_GT_TRUE"+str(gtCallCnt)+")", file=fh)
        print("@SP", file=fh)
        print("A=M-1", file=fh)
        print("A=A-1", file=fh)
        print("M=-1", file=fh)
        print("@SP", file=fh)
        print("M=M-1", file=fh)
        print("@NEXT_"+i, file=fh)
        print("0;JMP", file=fh)

        print("(SET_GT_FALSE"+str(gtCallCnt)+")", file=fh)
        print("@SP", file=fh)
        print("A=M-1", file=fh)
        print("A=A-1", file=fh)
        print("M=0", file=fh)
        print("@SP", file=fh)
        print("M=M-1", file=fh)
        print("@NEXT_"+i, file=fh)
        print("0;JMP", file=fh)

        print("(NEXT_"+i+")", file=fh)
        gtCallCnt=gtCallCnt+1

    elif re.match(r'lt', alCmd):
        print("@SP", file=fh)
        print("A=M-1", file=fh)
        print("D=M", file=fh)
        print("A=A-1", file=fh)
        print("D=M-D", file=fh)
        print("@SET_LT_TRUE"+str(ltCallCnt), file=fh)
        print("D;JLT", file=fh)
        print("@SET_LT_FALSE"+str(ltCallCnt), file=fh)
        print("0;JMP", file=fh)

        print("(SET_LT_TRUE"+str(ltCallCnt)+")", file=fh)
        print("@SP", file=fh)
        print("A=M-1", file=fh)
        print("A=A-1", file=fh)
        print("M=-1", file=fh)
        print("@SP", file=fh)
        print("M=M-1", file=fh)
        print("@NEXT_"+i, file=fh)
        print("0;JMP", file=fh)

        print("(SET_LT_FALSE"+str(ltCallCnt)+")", file=fh)
        print("@SP", file=fh)
        print("A=M-1", file=fh)
        print("A=A-1", file=fh)
        print("M=0", file=fh)
        print("@SP", file=fh)
        print("M=M-1", file=fh)
        print("@NEXT_"+i, file=fh)
        print("0;JMP", file=fh)

        print("(NEXT_"+i+")", file=fh)
        ltCallCnt=ltCallCnt+1

    else:
        print("Arith Logic cmd not supported", alInst)

    return

def processLabel(labelInst, fh):
    global funcName
    print("//VM inst: ", labelInst, file=fh)
    labelCmd=labelInst.strip("label")
    labelCmd=labelCmd.strip() #remove any trailing, leading spaces
    if funcName != "":
        print("("+funcName+"$"+labelCmd+")", file=fh)
    else:
        print("("+labelCmd+")", file=fh)

    return

def processGoto(gotoInst, fh):
    global funcName
    print("//VM inst: ", gotoInst, file=fh)
    gotoCmd=gotoInst.strip("goto")
    gotoCmd=gotoCmd.strip() #remove any trailing, leading spaces
    if funcName != "":
        print("@"+funcName+"$"+gotoCmd, file=fh)
        print("0;JMP", file=fh)
    else:
        print("@"+gotoCmd, file=fh)
        print("0;JMP", file=fh)

    return

def processIfgoto(ifgotoInst, fh):
    global funcName
    print("//VM inst: ", ifgotoInst, file=fh)
    ifgotoCmd=ifgotoInst.strip("if-goto")
    ifgotoCmd=ifgotoCmd.strip() #remove any trailing, leading spaces
    print("@SP", file=fh)
    print("A=M-1", file=fh)
    print("D=M", file=fh)
    print("@SP", file=fh)
    print("M=M-1", file=fh)
    if funcName != "":
        print("@"+funcName+"$"+ifgotoCmd, file=fh)
        print("D;JNE", file=fh)
    else:
        print("@"+ifgotoCmd, file=fh)
        print("D;JNE", file=fh)


    return

def processFunction(funcInst, fh):
    print("//VM inst: ", funcInst, file=fh)
    funcCmd=funcInst.strip() #remove any trailing, leading spaces
    fName=funcCmd.split()[1]
    print("("+fName+")", file=fh)
    funcVar=int(funcCmd.split()[2])
    for x in range(funcVar):
        print("@0", file=fh)
        print("D=A", file=fh)
        print("@SP", file=fh)
        print("A=M", file=fh)
        print("M=D", file=fh)
        print("@SP", file=fh)
        print("M=M+1", file=fh)

    return

def processCall(callInst, fh):
    global callCnt
    print("//VM inst: ", callInst, file=fh)
    callCmd=callInst.strip() #remove any trailing, leading spaces
    callFuncName=callCmd.split()[1]
    #print("@1111", file=fh)
    print("@"+callFuncName+"$ret."+str(callCnt), file=fh)
    print("D=A", file=fh)
    print("@SP", file=fh)
    print("A=M", file=fh)
    print("M=D", file=fh)
    print("@SP", file=fh)
    print("M=M+1", file=fh)
    print("@LCL", file=fh)
    print("D=M", file=fh)
    print("@SP", file=fh)
    print("A=M", file=fh)
    print("M=D", file=fh)
    print("@SP", file=fh)
    print("M=M+1", file=fh)
    print("@ARG", file=fh)
    print("D=M", file=fh)
    print("@SP", file=fh)
    print("A=M", file=fh)
    print("M=D", file=fh)
    print("@SP", file=fh)
    print("M=M+1", file=fh)
    print("@THIS", file=fh)
    print("D=M", file=fh)
    print("@SP", file=fh)
    print("A=M", file=fh)
    print("M=D", file=fh)
    print("@SP", file=fh)
    print("M=M+1", file=fh)
    print("@THAT", file=fh)
    print("D=M", file=fh)
    print("@SP", file=fh)
    print("A=M", file=fh)
    print("M=D", file=fh)
    print("@SP", file=fh)
    print("M=M+1", file=fh)
    callVar=int(callCmd.split()[2])
    print("@SP", file=fh)
    print("D=M", file=fh)
    print("D=D-1", file=fh)
    print("D=D-1", file=fh)
    print("D=D-1", file=fh)
    print("D=D-1", file=fh)
    print("D=D-1", file=fh)
    for x in range(callVar):
        print("D=D-1", file=fh)
    print("@ARG", file=fh)
    print("M=D", file=fh)
    print("@SP", file=fh)
    print("D=M", file=fh)
    print("@LCL", file=fh)
    print("M=D", file=fh)

    #print("@2222", file=fh)
    print("@"+callFuncName, file=fh)
    print("0;JMP", file=fh)

    print("("+callFuncName+"$ret."+str(callCnt)+")", file=fh)
    return

def processReturn(retInst, fh):
    print("//VM inst: ", retInst, file=fh)
    #print("@3333", file=fh)
    print("@LCL", file=fh)
    print("D=M", file=fh)
    print("@R15", file=fh) #LCL: endFrame
    print("M=D", file=fh)
    print("D=D-1", file=fh)
    print("D=D-1", file=fh)
    print("D=D-1", file=fh)
    print("D=D-1", file=fh)
    print("D=D-1", file=fh)
    print("A=D", file=fh)
    print("D=M", file=fh)
    print("@R14", file=fh) #LCL-5: retAddr
    print("M=D", file=fh)
    print("@SP", file=fh)
    print("A=M-1", file=fh)
    print("D=M", file=fh)
    print("@R13", file=fh) #pop value
    print("M=D", file=fh)
    print("@SP", file=fh)
    print("M=M-1", file=fh)
    print("@R13", file=fh) 
    print("D=M", file=fh)
    print("@ARG", file=fh)
    print("A=M", file=fh)
    print("M=D", file=fh)
    print("@ARG", file=fh)
    print("D=M", file=fh)
    print("D=D+1", file=fh)
    print("@SP", file=fh)
    print("M=D", file=fh)
    print("@R15", file=fh)
    print("D=M-1", file=fh)
    print("A=D", file=fh)
    print("D=M", file=fh)
    print("@THAT", file=fh)
    print("M=D", file=fh)
    print("@R15", file=fh)
    print("D=M-1", file=fh)
    print("D=D-1", file=fh)
    print("A=D", file=fh)
    print("D=M", file=fh)
    print("@THIS", file=fh)
    print("M=D", file=fh)
    print("@R15", file=fh)
    print("D=M-1", file=fh)
    print("D=D-1", file=fh)
    print("D=D-1", file=fh)
    print("A=D", file=fh)
    print("D=M", file=fh)
    print("@ARG", file=fh)
    print("M=D", file=fh)
    print("@R15", file=fh)
    print("D=M-1", file=fh)
    print("D=D-1", file=fh)
    print("D=D-1", file=fh)
    print("D=D-1", file=fh)
    print("A=D", file=fh)
    print("D=M", file=fh)
    print("@LCL", file=fh)
    print("M=D", file=fh)
    #print("@4444", file=fh)
    print("@R14", file=fh)
    print("D=M", file=fh)
    print("A=D", file=fh)
    print("0;JMP", file=fh)

    return

def processVmFile(vmFilePtr, asmFilePtr):
    global funcName
    global callCnt
    validInstCnt=-1
    instList=[]
    instType=''
  
    for line in vmFilePtr:
      if re.match(r'^\s*\/\/', line) or re.match(r'^\s*\n', line):
        line=line.strip('\n')
      else:
        line=re.sub(r'\s*\/\/.*', '', line) #removing trailing comment
        line=line.strip()
        if re.match(r'^\s*push.+', line):
          validInstCnt=validInstCnt+1
          line=line.strip('\n')
          instType='Push'
          instList.append((validInstCnt, instType, line))
        elif re.match(r'^\s*pop.+', line):
          validInstCnt=validInstCnt+1
          line=line.strip('\n')
          instType='Pop'
          instList.append((validInstCnt, instType, line))
        elif re.match(r'^\s*add|sub|neg|eq|gt|lt|and|or|not', line):
          validInstCnt=validInstCnt+1
          line=line.strip('\n')
          instType='Arithlogic'
          instList.append((validInstCnt, instType, line))
        elif re.match(r'^\s*function', line):
          validInstCnt=validInstCnt+1
          line=line.strip('\n')
          instType='Function'
          funcName=line.split()[1]
          instList.append((validInstCnt, instType, line))
        elif re.match(r'^\s*return', line):
          validInstCnt=validInstCnt+1
          line=line.strip('\n')
          instType='Return'
          instList.append((validInstCnt, instType, line))
        elif re.match(r'^\s*call', line):
          validInstCnt=validInstCnt+1
          line=line.strip('\n')
          instType='Call'
          instList.append((validInstCnt, instType, line))
        elif re.match(r'^\s*label.+', line):
          validInstCnt=validInstCnt+1
          line=line.strip('\n')
          instType='Label'
          instList.append((validInstCnt, instType, line))
        elif re.match(r'^\s*goto.+', line):
          validInstCnt=validInstCnt+1
          line=line.strip('\n')
          instType='Goto'
          instList.append((validInstCnt, instType, line))
        elif re.match(r'^\s*if-goto.+', line):
          validInstCnt=validInstCnt+1
          line=line.strip('\n')
          instType='Ifgoto'
          instList.append((validInstCnt, instType, line))
        else:
          print("Unrecognized VM Instruction: ", line)

    for i in range(len(instList)):
      if instList[i][1]=='Push':
          processPush(instList[i][2], asmFilePtr)
      elif instList[i][1]=='Pop':
          processPop(instList[i][2], asmFilePtr)
      elif instList[i][1]=='Arithlogic':
          processArithlogic(instList[i][2], instList[i][0], asmFilePtr)
      elif instList[i][1]=='Function':
          processFunction(instList[i][2], asmFilePtr)
      elif instList[i][1]=='Return':
          processReturn(instList[i][2], asmFilePtr)
      elif instList[i][1]=='Call':
          processCall(instList[i][2], asmFilePtr)
          callCnt=callCnt+1
      elif instList[i][1]=='Label':
          processLabel(instList[i][2], asmFilePtr)
      elif instList[i][1]=='Goto':
          processGoto(instList[i][2], asmFilePtr)
      elif instList[i][1]=='Ifgoto':
          processIfgoto(instList[i][2], asmFilePtr)
      else:
          print("shouldn't get here - strange - VM instruction not handled", instList[i][2])

    return

def addBootStrap(fh):
    global callCnt
    print("//Boot Strap Code: ", file=fh)
    print("@256", file=fh)
    print("D=A", file=fh)
    print("@SP", file=fh)
    print("M=D", file=fh)
    bsInst="call Sys.init 0"
    processCall(bsInst, fh)

    return


def main():
    global eqCallCnt
    global gtCallCnt
    global ltCallCnt
    global fStr
    global funcName
    global callCnt
    
    eqCallCnt=0
    gtCallCnt=0
    ltCallCnt=0
    callCnt=0
    funcName=''

    parser = argparse.ArgumentParser(description='VM to hack translator')
    parser.add_argument('file_or_dir', metavar='filename or dirname', help='input vm file or directory with vm files')
    
    args=parser.parse_args()

    if os.path.isdir(args.file_or_dir):
        #outputFile=re.sub(r'(.*\/*)(\w+)\/*', r'\1\2/\2.asm', args.file_or_dir)
        outputFile=re.sub(r'(\w+)\/*', r'\1.asm', args.file_or_dir)
        os.chdir(args.file_or_dir)
        asm=open(outputFile, 'w')
        addBootStrap(asm)
        for fileList in os.listdir('.'):
            if fileList.endswith(".vm"):
                vm=open(fileList)
                fStr=re.sub(r'(\w+)\.vm', r'\1', fileList)
                print("//***VM file: ", fileList, file=asm)
                processVmFile(vm, asm)
            else:
                pass
    else:
        outputFile=re.sub(r'(.*)\.vm', r'\1.asm', args.file_or_dir)
        asm=open(outputFile, 'w')
        fStr=re.sub(r'.*\/(\w+)\.vm', r'\1', args.file_or_dir)
        vm=open(args.file_or_dir)
        print("//***VM file: ", args.file_or_dir, file=asm)
        processVmFile(vm, asm)

    vm.close()
    asm.close()

main()


