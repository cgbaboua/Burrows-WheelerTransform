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

#Import other functions 
from visualization import plot_BWT_mapping
from bwt_no_matrix import get_BWT_simplified
from mismatches import get_match_ignore_mismatch, n_match, get_match_pos_mismatch
import argparse

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

# Main program

def read_pattern_from_file(file_path):
    """Reads a pattern from a specified file."""
    with open(file_path, 'r') as file:
        return file.read().strip().replace(" ","").replace("\n","")

def print_help():
    """Prints help information for using the script."""
    print("Usage: python3 BWT.py --string [string or file] --pattern [pattern] --mismatch [mismatch]")
    print("--string: The string to process (default an ATP8 Seq)")
    print("--pattern: The pattern to match or path to file containing pattern (default 'AATC')")
    print("--mismatch: Number of allowed mismatches (default 1)")
    print("Example: python3 BWT.py --string APPLE --pattern PL --mismatch 0 or python3 BWT.py --string ../apple.txt --pattern PL --mismatch 0")

def main(my_string, my_pattern, n_mismatch):
    """Main function that processes the string, pattern, and mismatch count."""
    my_string_sorted = sorted("$" + my_string.upper())
    BWT = get_BWT_simplified(my_string)
    FM = get_FM(BWT)
    C = get_C(FM)
    I = get_I(BWT, FM)
    all_pos = get_pos(BWT, I, C)
    match = get_match_ignore_mismatch(my_pattern, FM, C, my_string, n_mismatch)
    match_pos = get_match_pos_mismatch(match, len(my_pattern), all_pos, my_string)
    match_list = list(match)
    print(f"The string is : {my_string}")
    print(f"There are {n_match(match)} matches with the pattern '{my_pattern}' allowing {n_mismatch} mismatches")
    print(f"Match positions: {match_pos}")
    plot_BWT_mapping(my_string_sorted, my_string, match_list, match_pos)


if __name__ == "__main__":
# Default values
    my_string = "ATGCCCCAACTAAATACTACCGTATGGCCCACCATAATTACCCCCATACTCCTTACACTATTCCTCATCACCCAACTAAAAATATTAAACACAAACTACCACCTACCTCCCTCACCAAAGCCCATAAAAATAAAAAATTATAACAAACCCTGAGAACCAAAATGAACGAAAATCTGTTCGCTTCATTCATTGCCCCCACAATCCTAG"
    my_pattern = "AATC"
    n_mismatch = 1
    parser = argparse.ArgumentParser(
        description="Process a string with BWT algorithm.",
        epilog="Example usage: python3 python/BWT.py --string APPLE --pattern PL --mismatch 0\n"
               "Or: python3 python/BWT.py --string examples/seq.txt --pattern TTGC --mismatch 0\n"
               "Note: --string and --pattern should be used together. You can use --mismatch alone."
    )
    parser.add_argument("--string", help="The string to process or path to file containing the string", default=f"{my_string}")
    parser.add_argument("--pattern", help="The pattern to match", default="AATC")
    parser.add_argument("--mismatch", help="Number of allowed mismatches", type=int, default=1)
    args = parser.parse_args()
    # Validate that both --string and --pattern are provided if one is given
    if args.string != f"{my_string}" and args.pattern == "AATC":
        parser.error("Both --string and --pattern must be provided together.")
    if args.pattern != "AATC" and args.string == f"{my_string}":
        parser.error("Both --string and --pattern must be provided together.")
    # Check if the string or pattern are file paths and read from files if necessary
    if args.string.endswith(".txt"):
        args.string = read_pattern_from_file(args.string)
    main(args.string, args.pattern, args.mismatch)
   
  

