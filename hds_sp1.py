from rules import *  # import rules
import re  

INPUT_FILE = 'ukazka_HDS.ortho.txt'
OUTPUT_FILE = 'ukazka_HDS.phntrn.txt'
transcripted = list()

test = 'eunuch proběhl před tramvají po obědě přes celou evropu.'
with open(INPUT_FILE, 'r', encoding = 'UTF-8') as f:
    lines = f.readlines()
    for line in lines:
        line = basic_tran(constant_tran(vocal_tran(voice_asimilation(preproces(line)))))

        transcripted.append(line)


with open(OUTPUT_FILE, 'w', encoding = 'UTF-8') as f:
    for sentence in range(len(transcripted)):
        f.write(transcripted[sentence] + '\n')

print(transcripted)