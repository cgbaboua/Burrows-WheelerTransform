#!/bin/python3

# M2BI
# antoine.bridier-nahmias@inserm.fr
# Rendu AVANT Le 2023/12/01
# Au choix
# 1) Ne pas stocker la matrice complète lors de la transformation
# 2) Gérer le 'maching' pour qu'il tolère 1 'mismatch'
# 3) Générer une représentation graphique de l'alignement
# Objet du mail: '[M2BI_IPFB-BWT] .*'
# Nom du fichier: M2BI_IPFB-BWT-NOM1_NOM2.truc

from visualization import plot_BWT_mapping
from bwt_no_matrix import get_BWT_simplified
from mismatches import get_match_ignore_mismatch, n_match, get_match_pos_mismatch

def get_BWT(T):
    if not T.endswith("$"):
        T = T.upper() + '$'
    L = len(T)
    rot = [None] * L
    BWT = [None] * L
    # Générer toutes les rotations de la chaîne T
    for i in range(L):
        rot[i] = T[i:] + T[:i]
        # print(f'{i}   {T}')
    # Trier les rotations
    rot.sort()
    # Construire la BWT en prenant le dernier caractère de chaque rotation triée
    for i in range(L):
        BWT[i] = rot[i][-1]
    return ''.join(BWT)


def get_alphab(T):
    dictio = {}
    for i in range(len(T)):
        dictio[T[i]] = 0
    alphab = list(dictio.keys())
    return sorted(alphab)

def get_FM(T):
    alphab = get_alphab(T)
    T = list(T)
    curr_dict = {}
    for chara in alphab:
        curr_dict.update({chara: 0})
    FM = []
    FM.append(curr_dict.copy())
    for i in range(0, len(T)):
        curr_dict[T[i]] += 1
        FM.append(curr_dict.copy())
    return FM

def get_C(FM):
    C = {}
    last_FM = FM[len(FM) - 1]
    keyz = list(last_FM.keys())
    C[keyz[0]] = 0
    C[keyz[1]] = 1
    curr_sum = 1
    for i in range(2, len(keyz)):
        curr_sum += last_FM[keyz[i - 1]]
        C[keyz[i]] = curr_sum
    return C

def get_match(pattern, FM, C):
    top = 0
    bot = len(FM) - 1
    pattern = pattern[::-1].upper()
    for i in range(len(pattern)):
        curr_char = pattern[i]
        top = C[curr_char] + FM[top][curr_char]
        bot = C[curr_char] + FM[bot][curr_char]
    return (top, bot)

def get_I(BWT, FM):
    dictio = FM[0].copy()
    I = []
    for i in range(len(BWT)):
        I.append(dictio[BWT[i]])
        dictio[BWT[i]] += 1
    return I

def get_pos(BWT, I, C):
    i = len(BWT)
    j = 0
    pos = [-1] * i
    while i > 0:
        i -= 1
        pos[j] = i
        j = C[BWT[j]] + I[j]
    return pos

def get_match_pos(match, L, all_pos):
    if not match[0] < match[1]:
        print("This is not a match")
        return ()
    l_range = len(range(match[0], match[1]))
    pos = [[-1, -1]] * l_range
    i = 0
    for m in range(match[0], match[1]):
        print(m)
        pos[i] = [all_pos[m], all_pos[m] + L - 1]
        i += 1
    return pos

# Main program #
#my_string = "AAACTAAATATATGTAAATGTGGAAATGTAAAGAGCCAAACAAAAAAAAAAAAAAAAAAAAACATTATCTAAAAAAATAAAACTAAATATATGTAAATGTGGAAATGTAAAGAGCCAAACAAAAAAAAAAAAAAAAAAAAACATTATCTAAAAAAATAAAACTAAATATATGTAAATGTGGAAATGTAAAGAGCCAAACAAAAAAAAAAAAAAAAAAAAACATTATCTAAAAAAATAAAACTAAATATATGTAAATGTGGAAATGTAAAGAGCCAAACAAAAAAAAAAAAAAAAAAAAACATTATCTAAAAAAATA"
my_string = "BANANA"
my_string_sorted = sorted("$" + my_string.upper())
my_pattern = "NA"
BWT = get_BWT_simplified(my_string)
FM = get_FM(BWT)
C = get_C(FM)
I = get_I(BWT, FM)
all_pos = get_pos(BWT, I, C)
n_mismatch = 1
match = get_match_ignore_mismatch(my_pattern, FM, C,my_string,n_mismatch)
match_pos = get_match_pos_mismatch(match, len(my_pattern), all_pos,my_string)
match_list = list(match)
print(f"The string is : {my_string}")
print(
    f"There are {n_match(match)} match with the pattern '{my_pattern}' and allowing {n_mismatch} mismatchs"
)
print(f"Positions des matchs: {match_pos}")
# print(BWT)
# print(I)
# [print(f"{i} {my_string_sorted[i]}---{BWT[i]}") for i in range(len(BWT))]
# [print(f"{i} -- {FM[i]}") for i in range(len(FM))]
# print(match)
# print(all_pos)
# print(f"C = {C}")
plot_BWT_mapping(my_string_sorted, my_string, match_list, match_pos)
