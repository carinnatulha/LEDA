import re
from itertools import permutations

#https://github.com/vanessaserrano/visirTR/blob/master/dashboard/functions_VISIRDB.R

def prep_normalization(df3):
    #Split the representation for each component
    split_data = []
    for item in df3['breadboard']:
        components = item.split(', ')
        split_components = []
        for component in components:
            split_components.append(component.split(' '))
        split_data.append(split_components)

    # Lexicographically reorder the nodes and components
    ordered_data = []
    for components in split_data:
        ordered_components = []
        for component in components:
            ordered_component = sorted(component[1:], key=lambda x: x.split('_')[-1])
            ordered_components.append([component[0]] + ordered_component)
        ordered_components.sort(key=lambda x: x[0])
        ordered_data.append(ordered_components)

    #df2['breadboard_norm'] = ordered_data

#remove duplicates
def remove_duplicates(lst):
    seen = set()
    new_lst = []
    for item in lst:
        if tuple(item) not in seen and item != ['']:
            seen.add(tuple(item))
            new_lst.append(item)
    return new_lst

def normalizar_circuito(data):
    normr = []
    cont_norm = 0

    for circuito_list in data:
        normr_inner = []
        for circuito in circuito_list:
            x = " ".join(circuito)

            if x is None or x == "":
                continue

            circuito = x

            componentes = circuito.split("/")

            for i in range(len(componentes)):
                conectores = componentes[i].split()
                if len(conectores) >= 3:
                    if conectores[1] > conectores[2]:
                        conectores[1], conectores[2] = conectores[2], conectores[1]

                    if conectores[0] == "W_X" and conectores[1][0] == "A":
                        componentes = [re.sub(re.escape(conectores[1]), conectores[2], comp) if comp != componentes[i] else "" for comp in componentes]
                        cont_norm += 1
                    else:
                        componentes[i] = " ".join(conectores)
            componentes = sorted(componentes, key=lambda comp: re.sub(r"A[0-9][0-9]", "Axx", comp))
            circuito = "/".join(componentes)
            circuito = re.sub(r"^/*", "", circuito)

            componentes = circuito.split("/")
            for i in range(len(componentes)):
                conectores = componentes[i].split()
                if len(conectores) >= 3:
                    if conectores[1] > conectores[2]:
                        conectores[1], conectores[2] = conectores[2], conectores[1]
                    componentes[i] = " ".join(conectores)
            componentes = sorted(componentes, key=lambda comp: re.sub(r"A[0-9][0-9]", "Axx", comp))
            circuito = "/".join(componentes)

            nodos = re.findall(r"A[0-9][0-9]", circuito)
            nodos = list(set(nodos)) if nodos else []
            if 0 < len(nodos) < 9:
                nodos_unif = [f"P{str(i).zfill(2)}" for i in range(1, 10)] + [f"P{i}" for i in range(10, 100)]
                nodos_unif = nodos_unif[:len(nodos)]
                mat_nodos_unif = list(permutations(nodos_unif))
                r_circuitos = [re.sub("|".join(nodos), lambda m: mat_nodos_unif[i][nodos.index(m.group())], circuito) for i in range(len(mat_nodos_unif))]
                circuito = min(r_circuitos)

            normr_inner.append(circuito)
        normr_inner = remove_duplicates(normr_inner)
        normr.append(normr_inner)

    # Remove empty strings
    normr = [[c for c in inner if c] for inner in normr]

    return normr
