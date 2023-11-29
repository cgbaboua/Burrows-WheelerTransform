#!/bin/python3

# M2BI
# antoine.bridier-nahmias@inserm.fr
# Rendu AVANT Le 2023/12/01
# Au choix
# 1) Ne pas stocker la matrice complète lors de la transformation
# 2) Gérer le 'maching'	pour qu'il tolère 1 'mismatch'
# 3) Générer une représentation graphique de l'alignement
# Objet du mail: '[M2BI_IPFB-BWT] .*'
# Nom du fichier: M2BI_IPFB-BWT-NOM1_NOM2.truc

import plotly.graph_objs as go
from plotly.offline import plot

def get_BWT(T):
    if not T.endswith("$"):
        T = T.upper() + "$"
        # print(f'0	{T}')
    L = len(T)
    rot = [None] * L
    rot[0] = T
    BWT = [None] * L
    for i in range(1, L):
        T = T[-1] + T[0:-1]
        rot[i] = T
        # print(f'{i}	{T}')
    rot.sort()
    # [print(f'{truc}') for truc in rot]
    for i in range(0, L):
        BWT[i] = rot[i][-1]
    return "".join(BWT)

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

##Allow mismatch##

def get_match_ignore_mismatch(pattern, FM, C, n_mismatch=1):
  stack = [(pattern[::-1].upper(), 0, n_mismatch, 0,0, len(FM)-1)]
  results = []
  while stack:
    print(len(stack[0]))
    print(stack)
    curr_pattern, curr_pos, allowed_mismatches, curr_mismatches, curr_top, curr_bot = stack.pop()
    if curr_mismatches > allowed_mismatches:
      continue
    if len(curr_pattern) == 0:
      results.append((curr_top, curr_bot))
      continue
    curr_char = curr_pattern[0]
    for char in C:
      if char != curr_char:
        updated_top = C[char] + FM[curr_top][char]
        updated_bot = C[char] + FM[curr_bot][char]
        if updated_top != updated_bot:
          stack.append((curr_pattern[1:], curr_pos+1, allowed_mismatches, curr_mismatches+1, updated_top, updated_bot))
      else:
        updated_top = C[curr_char] + FM[curr_top][curr_char]
        updated_bot = C[curr_char] + FM[curr_bot][curr_char]
        if updated_top != updated_bot:
          stack.append((curr_pattern[1:], curr_pos+1, allowed_mismatches, curr_mismatches, updated_top, updated_bot))
  return results

def n_match(match):
    tot=0
    for m in match:
        tot+= len(range(*m))
    return tot
 
def get_match_pos_mismatch(match, L, all_pos):
    l_range= n_match(match)
    if l_range==0:
        print('This is not a match')
        return()
    pos = [[-1,-1]] * l_range
    i=0
    for m_range in match:
        for m in range(*m_range):
            pos[i] = [all_pos[m], all_pos[m] + L - 1] 
            i += 1
    sorted_pos = sorted(pos, key=lambda x: x[0])
    return sorted_pos

## Plot the mapping ##

def plot_BWT_mapping(my_string_sorted, my_string, match_list, match_pos):
    match_pos = sorted(match_pos, key=lambda x: x[0])  # Tri des matchs
    match_counter = 1 
    y_values = []
    fig = go.Figure()
    x_values = my_string
    for pos in match_pos :
        fig.add_shape(type="line",
                      x0=pos[0], y0=match_counter, x1=pos[1],y1=match_counter,
                      line=dict(color="pink", width=2))
        for i in range(pos[0], pos[1]+1):
            fig.add_trace(go.Scatter(
                x=[i], y=[match_counter],
                mode='text',
                text='',
                textposition='bottom center',
                hoverinfo='text',
                hovertext=f'{my_string[i]}{i+1}',
                showlegend=False
            ))
            fig.add_annotation(x=i, y=match_counter, text=f"<b>{my_string[i]}</b>",
                               showarrow=False, font=dict(color='black', size=12))
        match_counter+= 1
    # Ajout des axes x et y
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black',
                     tickvals=list(range(len(my_string))),
                     ticktext=list(my_string),
                     range=[-1,71] if len(my_string) >= 70 else [-1,len(my_string)])
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black',range=[0, match_counter + 1])
    fig.update_layout(
        title={
            'text': "Mapping",
            'y':0.9,  # Position verticale du titre
            'x':0.5,  # Position horizontale du titre (0.5 pour le centrer)
            'xanchor': 'center',
            'yanchor': 'top',
            'font':dict(color='black')},
        xaxis=dict(title="Caractères de la séquence", color='black'),
        yaxis=dict(title="Numéro de match", color='black'),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    plot(fig, auto_open=True)

my_string = "AAACTAAATATATGTAAATGTGGAAATGTAAAGAGCCAAACAAAAAAAAAAAAAAAAAAAAACATTATCTAAAAAAATAAAACTAAATATATGTAAATGTGGAAATGTAAAGAGCCAAACAAAAAAAAAAAAAAAAAAAAACATTATCTAAAAAAATAAAACTAAATATATGTAAATGTGGAAATGTAAAGAGCCAAACAAAAAAAAAAAAAAAAAAAAACATTATCTAAAAAAATAAAACTAAATATATGTAAATGTGGAAATGTAAAGAGCCAAACAAAAAAAAAAAAAAAAAAAAACATTATCTAAAAAAATA"
#my_string = "BANANANA"
my_string_sorted = sorted("$" + my_string.upper())
my_pattern = "ATG"
BWT = get_BWT(my_string)
FM = get_FM(BWT)
C = get_C(FM)
I = get_I(BWT, FM)
all_pos = get_pos(BWT, I, C)
n_mismatch=1
match = get_match_ignore_mismatch(my_pattern, FM, C,n_mismatch)
match_pos = get_match_pos_mismatch(match, len(my_pattern), all_pos)
match_list = list(match)
print(my_string)
print(match)
print(f"There are {n_match(match)} match with the pattern '{my_pattern}' and allowing {n_mismatch} mismatchs")
print(f"Positions des matchs: {match_pos}")
#print(BWT)
#print(I)
#[print(f"{i} {my_string_sorted[i]}---{BWT[i]}") for i in range(len(BWT))]
#[print(f"{i} -- {FM[i]}") for i in range(len(FM))]
#print(match)
 
#print(all_pos)
#print(f"C = {C}")
plot_BWT_mapping(my_string_sorted,my_string,match_list,match_pos)




