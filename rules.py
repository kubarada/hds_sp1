# Jakub Rada 28.2.2023
# encoding: utf-8

## Basic rules


# ! ráz
# @ šva


import re

BASIC_RULES = {'á':'A', 'y':'i', 'í':'I', 'é':'E','ó':'O','ů':'ú', 'ú':'U', 'š':'S', 'ř':'R',
'ť':'T', 'ď':'D', 'ň':'J', 'č':'C', 'ž':'Z', 'ou':'y', 'au':'Y', 'eu':'F'}

VOCALS = ['a', 'e', 'i', 'o', 'u', 'á', 'é', 'í', 'ó', 'ů', 'ú']

CONSTANT = ['b', 'c', 'č', 'd', 'ď', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'ň', 'p', 'q', 'r', 'ř', 's', 'š', 't', 'ť', 'v','w', 'x', 'y', 'z', 'ž'] 

DTN = ['d', 't', 'n']
DTN_tran = ['ď', 'ť', 'ň']

BPV = ['b', 'p', 'v']

DTNM = ['d', 't', 'n', 'm']

SPLIT_ON = ['.', '?', '!', '-', '_']

VOICE_CONSTANT = {'b':'p', 'd':'t', 'ď':'ť', 'g' :'k', 'v':'f', 'z':'s', 'ž':'š', 'ř':'Q', 'dz':'c', 'dž':'č'}

VOICE_CONSTANTx = {'b':'pp', 'd':'tt', 'ď':'ťť', 'g' :'kk', 'v':'ff', 'z':'ss', 'ž':'šš', 'ř':'QQ', 'dz':'cc', 'dž':'čč'}
VOICE_CONSTANTxx = {'pp':'p', 'tt':'t', 'ťť':'ť', 'kk' :'k', 'ff':'f', 'ss':'s', 'šš':'š', 'xx':'x', 'QQ':'Q', 'cc':'c', 'čč':'č'}

VOICLESS_CONSTANT = {v: k for k, v in VOICE_CONSTANT.items()} # swap keys and vals in VOICE_CONSTANT

UNIQUE_CONSTANT = ['m', 'n', 'ň', 'l', 'r', 'j']


def preproces(text):
    splited = text.replace(' ', '|')
    for i in SPLIT_ON:
        splited = splited.replace(i, '|')
    splited = '|$|' + splited.replace(',', '|#')
    splited = splited + '$|'
    splited = splited.replace('\n', '')
    splited = splited.replace('ch', 'x')
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

    # (rovnice 2.26)
    for i in VOICLESS_CONSTANT.keys():
        for j in VOICE_CONSTANTx.keys():
            text = text.replace(i + j, VOICLESS_CONSTANT[i]+j)
            text = text.replace(i + '|' + j, VOICLESS_CONSTANT[i] + '|' + j)

    # vifikundace, aby se mi to nepřepisovalo
    for key in VOICE_CONSTANTxx.keys():
        text = text.replace(key, VOICE_CONSTANTxx[key])


    return text


