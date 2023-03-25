# Jakub Rada 28.2.2023
# encoding: utf-8

## Basic rules


# ! ráz
# @ šva


import re

BASIC_RULES = {'á':'A', 'y':'i', 'í':'I','ý':'I', 'é':'E','ó':'O','ů':'ú', 'ú':'U', 'š':'S', 'ř':'R',
'ť':'T', 'ď':'D', 'ň':'J', 'č':'C', 'ž':'Z', 'ou':'y', 'au':'Y', 'eu':'F', 'q':'kv', 'ch':'x', 'q':'kv' }

VOCALS = ['a', 'e', 'i', 'o', 'u', 'á', 'é', 'í', 'ó', 'ů', 'ú']

CONSTANT = ['b', 'c', 'č', 'd', 'ď', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'ň', 'p', 'q', 'r', 'ř', 's', 'š', 't', 'ť', 'v','w', 'x', 'y', 'z', 'ž'] 

DTN = ['d', 't', 'n']
DTN_tran = ['ď', 'ť', 'ň']


BPV = ['b', 'p', 'v']

RLM = {'r':'P', 'l':'L', 'm':'M'}


DTNM = ['d', 't', 'n', 'm']

SPLIT_ON = ['.', '?', '!', '-', '_']

VOICE_CONSTANT = {'b':'p', 'd':'t', 'ď':'ť', 'g' :'k', 'v':'f', 'z':'s', 'ž':'š', 'ř':'Q', 'dz':'c', 'dž':'č'}

VOICE_CONSTANTx = {'b':'p*', 'd':'t*', 'ď':'ť*', 'g' :'k*', 'v':'f*', 'z':'s*', 'ž':'š*', 'ř':'Q*', 'dz':'c*', 'dž':'č*'}
VOICE_CONSTANTxx = {'p*':'p', 't*':'t', 'ť*':'ť', 'k*' :'k', 'f*':'f', 's*':'s', 'š*':'š', 'x*':'x', 'Q*':'Q', 'c*':'c', 'č*':'č'}

VOICLESS_CONSTANT = {v: k for k, v in VOICE_CONSTANT.items()} # swap keys and vals in VOICE_CONSTANT

V_EXCEPTIONS = ['tv', 't|v', 'kv', 'k|v', 'sv', 's|v', 'šv', 'š|v', 'cv', 'c|v', 'čv']

UNIQUE_CONSTANT = ['m', 'n', 'ň', 'l', 'r', 'j']


EXCEPTIONS = {'nashle':'naschle', 'shora':'zhora', 'shůr':'zhůr', 'shluk':'zhluk', 'shod':'schod', 'jsme':'sme', 'jsem':'sem','jste':'ste', 'jsou':'sou', 'jsi':'si', 'dcer':'tcer','dceř':'tceř', 'srdce':'srtce', 'laik':'lajk', 'kofein':'kojefn', 'heroi':'heroji','poin':'pojin', 'naiv':'najiv', 'prozai':'prozaji'}


def preproces(text):
    splited = text.replace(' ', '|')
    for i in SPLIT_ON:
        splited = splited.replace(i, '|')
    splited = '|$|' + splited.replace(',', '|#')
    splited = splited + '$|'
    splited = splited.replace('\n', '')
    splited = splited.replace('vzb', 'zb')
    splited = splited.replace('w', 'v')
    splited = splited.replace('vzp', 'zp')
    for key in EXCEPTIONS.keys():
        splited = splited.replace(key, EXCEPTIONS[key])

    return splited


def basic_tran(text):
    for key in BASIC_RULES:
        text = text.replace(key, BASIC_RULES[key])

    return text

def vocal_tran(text):
    for i in VOCALS:
        for j in VOCALS:
            text = text.replace(i + '|' + j, i + '|!' + j)
            text = text.replace(i + '|#|' + j, i + '|#|!' + j)
        text = text.replace('|$|'+ i, '|$|!'+ i,)
    for i in CONSTANT:
        for j in VOCALS:
            text = text.replace(i + '|' + j, i + '|!' + j)
            text = text.replace(i + '|#|' + j, i + '|#|!' + j)

    for i in VOCALS:
        text = text.replace('i'+i, 'ij'+i)
    text = text.replace('x|#','ks|#')
    text = text.replace('x|!','ks|!')

    return text

def constant_tran(text):
    for i in range(len(DTN)):
        text = text.replace(DTN[i] + 'i', DTN_tran[i] + 'i')
        text = text.replace(DTN[i] + 'í', DTN_tran[i] + 'í')   # musím tam dát opět í protože BASIC_RULES budu používat až na konec, tak to nechci změnit
    for i in range(len(BPV)):
        text = text.replace(BPV[i] + 'ě', BPV[i] + 'je')
    for i in range(len(DTNM)):
        if DTNM[i] == 'm':
            text = text.replace(DTNM[i] + 'ě', DTNM[i] + 'ňe')
        else:
            text = text.replace(DTNM[i] + 'ě', DTN_tran[i] + 'e')

    return text

def voice_asimilation(text):

    for i in VOICE_CONSTANTx.keys():
        text = text.replace(i + '|v', VOICE_CONSTANTx[i]+'|v')
    # tady řeším ty základní srandy (rovnice 2.26)
    for i in VOICE_CONSTANTx.keys():
        for j in VOICLESS_CONSTANT.keys():
            text = text.replace(i + j, VOICE_CONSTANTx[i]+j)
            text = text.replace(i + '|' + j, VOICE_CONSTANTx[i]+ '|' + j)
            text = text.replace(i + '|$|', VOICE_CONSTANTx[i] + '|$|')
        for k in UNIQUE_CONSTANT:
            text = text.replace(i + '|' + k, VOICE_CONSTANTx[i]+ '|' + k)
        for q in VOCALS:
            text = text.replace(i + '|' + q, VOICE_CONSTANTx[i]+ '|' + q)

        # tady řeším ř na Q (rovnice 2.29)
        for z in VOICLESS_CONSTANT:
            text = text.replace(z + 'ř', z + 'Q')
        text = text.replace(i + '|#|', VOICE_CONSTANTx[i]+'|#|')

    # (rovnice 2.26 + rovnice 2.28)
    for i in VOICLESS_CONSTANT.keys():
        for j in VOICE_CONSTANT.keys():
            if i + j in V_EXCEPTIONS:
                continue
            else:
                text = text.replace(i + j, VOICLESS_CONSTANT[i]+j)
                text = text.replace(i + '|' + j, VOICLESS_CONSTANT[i] + '|' + j)

    # vifikundace, aby se mi to nepřepisovalo
    for key in VOICE_CONSTANTxx.keys():
        text = text.replace(key, VOICE_CONSTANTxx[key])
    
    text = text.replace('ch|', 'G|')

    return text

def articulation_asimilation(text):
    text = text.replace('mv', 'Mv')
    text = text.replace('mf', 'Mf')
    text = text.replace('nk', 'Nk')
    text = text.replace('ng', 'Ng')
    for i in range(len(DTN)):
        if DTN[i] == 'n':
            text = text.replace( DTN[i] + 'ť', DTN_tran[i] + 'ť')
            text = text.replace( DTN[i] + 'ď', DTN_tran[i] + 'ď')

        else:
            text = text.replace( DTN[i] + 'ň', DTN_tran[i] + 'ň')

    return text

def sylab_const_tran(text):
    for key in RLM.keys():
        for i in CONSTANT:
            for j in CONSTANT:
                    text = text.replace(i + key + j, i + RLM[key] + j)
                    text = text.replace(i + key + '|', i + RLM[key] + '|')
    

    return text

def x_trans(text):

# domyslet |! a |# a (ch)

# rovnice (2.84)
    for key in VOICE_CONSTANT.keys():
        text = text.replace('|ex' + key, '|egz' + key)

    text = text.replace('|exh','|egzh')
    
    for key in VOCALS:
        text = text.replace('|ex' + key, '|egz' + key)

    for key in VOICLESS_CONSTANT.keys():
        text = text.replace('|ex' + key, '|eks' + key)

    for key in UNIQUE_CONSTANT:
        text = text.replace('|ex' + key, '|eks' + key)

# rovnice (2.85)
    for key in VOICLESS_CONSTANT.keys():
        text = text.replace('x|' + key, 'ks'+ key)

    for key in VOICLESS_CONSTANT.keys():
        text = text.replace('x|' + key, 'ks|'+ key)

    for key in UNIQUE_CONSTANT:
        text = text.replace('x|' + key, 'ks|'+ key)

    for key in VOCALS:
        text = text.replace('x' + key, 'ks|'+ key)

    for key in VOICE_CONSTANT.keys():
        text = text.replace('x' + key, 'gz|'+ key)
    
    for i in VOCALS:
        for j in VOCALS:
            text = text.replace(i + 'x' + j, i + 'ks' + j)
        text = text.replace('|x' + i, '|ks'+ i)
    
    return text



