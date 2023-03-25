
from tkinter import *

inp = open("SICInput.asm","r")
#For output of PASS ONE
out = open("IntermediateFile.mdt","w")

symtab = open("SymbolTab.txt","w")
# Initialize variables
SYMTAB = {}
LOCCTR = 0
PRGLTH = 0
PRGNAME = ""

symtab = open("SymbolTab.txt","w");
sym = {}
error=[]
littab = {}
 
#  SIC opcodes
optab = {
    "ADD": "3",
    "AND": "3",
    "COMP": "3",
    "DIV": "3",
    "J": "3",
    "JEQ": "3",
    "JGT": "3",
    "JLT": "3",
    "JSUB": "3",
    "LDA": "3",
    "LDCH": "3",
    "LDL": "3",
    "LDX": "3",
    "MUL": "3",
    "OR": "3",
    "RD": "3",
    "RSUB": "3",
    "STA": "3",
    "STCH": "3",
    "STL": "3",
    "STX": "3",
    "SUB": "3",
    "TD": "3",
    "TIX": "3",
    "WD": "3",
    "BYTE": "1",
    "WORD": "3",
    "RESB": "0",
    "RESW": "0",
    "START": "0",
    "END": "0"
}

#READING FIRST LINE
first = inp.readline()
if first[11:20].strip() == "START":
        LOCCTR =first[21:38].strip()
        start1 = LOCCTR    
        start =int(LOCCTR,16)
        PN=first[0:10].strip()
        out.write(LOCCTR+" "*6+first[0:38])
else:
    LOCCTR=0

for i in inp.readlines():
   
    n = i
    string=n[40:70]#to remove comments
    if (n[11:20].strip()!='END'):
        print(n[11:20].strip())
        if n[0]!='.':
            
            
            if len(string) == 0:
                if(n[11:20].strip() == "LTORG"): 
                    out.write(" "*10+n)

                else:
                   out.write(LOCCTR+" "*6+n)
               
            else:
                if(n[11:20].strip() == "LTORG"): 
                    out.write(" "*10+n)

                else:
                    out.write(LOCCTR+" "*6+n[0:38]+"\n")
                

            if n[0:10].strip()!="":
                if n[0:10].strip() in sym:

                    print("error:duplicate symbol : "+n[0:10].strip())
                    error.append("error:duplicate symbol : "+n[0:10].strip())
                    
                else:
                    space=18-len(n[0:10].strip())
                    symtab.write(n[0:10].strip()+" "*space+LOCCTR+"\n")
                    
                    sym[n[0:10].strip()] = LOCCTR
                    
            if n[11:19].strip() in optab.keys() or n[11:19].strip()=="WORD":
              LOCCTR = str(hex(int(LOCCTR,16)+(3)))[2:] 
            elif n[11:19].strip()=="RESW":
              temp = int(n[21:38].strip())
              LOCCTR = str(hex(int(LOCCTR,16)+(temp)*3))[2:]
            elif n[11:19].strip()=="RESB":
              LOCCTR = str(hex(int(LOCCTR,16)+int(n[21:38].strip())))[2:]
            elif n[11:19].strip()=="BYTE":
              if n[21:38].strip()[0]=="X":
                LOCCTR = str(hex(int(LOCCTR,16)+int((len(n[21:38].strip())-3)/2)))[2:]
              elif n[21:38].strip()[0]=="C":
                LOCCTR = str(hex(int(LOCCTR,16)+int((len(n[21:38].strip())-3))))[2:]
        
            elif n[11:19].strip()=="LTORG":
                for i in littab:
                    space=18-len(i)
                    out.write(LOCCTR+" "*6+"*"+" "*10+i+"\n")
                    symtab.write(i+" "*space+LOCCTR+"\n")
                    sym[i] = LOCCTR
                    
                    LOCCTR=str(hex(int(LOCCTR,16)+int(littab[i][0])))[2:]
                littab={} 
         


            if n[21:22] == '=':
                literal = n[21:38].strip()
                if literal[1]== 'X':
                     hexco = literal[3:-1]
                     
                     if literal not in littab:
                        littab[literal]=[len(hexco)/2]
                elif  literal[1]=='C':
                     hexco = literal[3:-1]
                     
                     if literal not in littab:
                        littab[literal]=[len(hexco)]
                else:
                    print("ُERROR: NOT Valid Literal : "+literal) 
                    error.append("ُERROR: NOT Valid Literal : "+literal)
    else:
        out.write(" "*10+n+'\n')
        if littab:
            for i in littab:
                space=18-len(i)
                out.write(LOCCTR+" "*6+"*"+" "*10+i+"\n")
                symtab.write(i+" "*space+LOCCTR+"\n")
                sym[i] = LOCCTR
                    
                LOCCTR=str(hex(int(LOCCTR,16)+int(littab[i][0])))[2:]
        else:
            print("error: invalid opcdce"+ n[11:19].strip())
            error.append("error: invalid opcdce : "+ n[11:19].strip())
            break
        
    
             
inp.close()
out.close()
symtab.close()

lastaddress=LOCCTR
programLength = int(lastaddress,16) - start
proglen = hex(int(programLength))[2:]

print("program name is : "+PN+"\n"+"pogram length: "+proglen+'\n')      
for i in sym:
    print(i+"  "+sym[i]+"\n")        
    
 


root =Tk()
root.title("Sic Assembler") 
text1 = open("SymbolTab.txt").read()
prognam = Label(root ,text = "Program Name :" + PN,font=('Sourse Code Pro',16), bg="pink")
prognam.pack(fill = BOTH)
blank= Label(root ,text = "" , bg="pink")
blank.pack(fill = BOTH)
programLength = Label(root ,text = " Program Langth :" + str(proglen),font=('Sourse Code Pro',16),bg='purple' ,fg='pink')
programLength.pack(fill = BOTH)
blank= Label(root ,text = "" , bg="pink")
blank.pack(fill = BOTH)
programLength = Label(root ,text = " Location Counter :" + str(LOCCTR),font=('Sourse Code Pro',16) , bg="pink")
programLength.pack(fill = BOTH)
blank= Label(root ,text = "" , bg="pink")
blank.pack(fill = BOTH)
symTit = Label(root, text=" Symbol Table:",font=('Sourse Code Pro',16),fg='pink',bg='purple')
symTit.pack(fill = BOTH)
sym1 = Label(root, text=text1,font=('Sourse Code Pro',16), bg="pink")
sym1.pack(fill = BOTH)


root.mainloop()
