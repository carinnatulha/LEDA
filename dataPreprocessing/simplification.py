import pandas as pd
import re

def simplificar_circuito(circuit):
    if circuit is None:
        return None
    if circuit == "":
        return ""

    circuit_prin = None

    components = circuit.split(",")
    connectors = [(component.split(" ")) for component in components]
    df = pd.DataFrame(components)

    #o circuito deve conter os cabos do multimetro
    valid = ("DMM_VLO" in circuit and "DMM_VHI" in circuit) or \
            ("DMM_ALO" in circuit and "DMM_AHI" in circuit) or \
            ("DMM_1_1" in circuit and "DMM_1_2" in circuit) or \
            ("IPROBE_1_1" in circuit and "IPROBE_1_2" in circuit) or \
            ("DMM_2_1" in circuit and "DMM_2_2" in circuit) or \
            ("IPROBE_2_1" in circuit and "IPROBE_2_2" in circuit)

    if not valid:
        return ""

    nodesf1 = None

    #nodo inicial do fragmento principal
    if "DMM_VLO" in circuit and "DMM_VHI" in circuit:
        nodesf1 = "DMM_VLO"
    elif "DMM_ALO" in circuit and "DMM_AHI" in circuit:
        nodesf1 = "DMM_ALO"
    elif "DMM_1_1" in circuit and "DMM_1_2" in circuit:
        nodesf1 = "DMM_1_1"
    elif "DMM_2_1" in circuit and "DMM_2_2" in circuit:
        nodesf1 = "DMM_2_1"
    elif "IPROBE_1_1" in circuit and "IPROBE_1_2" in circuit:
        nodesf1 = "IPROBE_1_1"
    elif "IPROBE_2_1" in circuit and "IPROBE_2_2" in circuit:
        nodesf1 = "IPROBE_2_1"

    if nodesf1 is None:
        return ""

    internal = pd.DataFrame({'V2': ["DMM_VHI","DMM_AHI","DMM_1_1","DMM_2_1","IPROBE_1_1","IPROBE_2_1"],
                             'V3': ["DMM_VLO","DMM_ALO","DMM_1_2","DMM_2_2","IPROBE_1_2","IPROBE_2_2"]})

    lista = [''] * df.shape[0]
    df = df.assign(V1=lista, V2=lista, V3=lista)
    for i in range(df.shape[0]):
        df.iloc[i, 1:4] = df.iloc[i, 0].split(" ")[0:3]

    df = pd.DataFrame({'V2': df['V2'].astype(str).tolist() + df['V3'].astype(str).tolist(),
                       'V3': df['V3'].astype(str).tolist() + df['V2'].astype(str).tolist()})

    df = pd.concat([df, internal])

    nodesf1_previous = ''

    lista = []

    while len(nodesf1) != len(nodesf1_previous):
        nodesf1_previous = nodesf1
        for i in range(df.shape[0]):
            if df.iloc[i,0] in nodesf1:
                lista.append(nodesf1)
                lista.append(df.iloc[i,1])
                nodesf1_lst = set(lista)

    y = 0
    for i in range(len(components)):
        if df.iloc[i,1] not in nodesf1:
            component = components[-(i - y)]
            y += 1

    circuito_prin = ",".join(components)

    #eliminar componentes curto circuitados
    components = circuito_prin.split(',')
    if components is None:
        return None
    if len(components) == 0:
        return None

    for i in range(len(components)):
        if components[i] != "":
            connectors = list(i.split(" ") for i in components)
        if connectors[0][1] == connectors[0][2]:
            components[i] = ''

    components = sorted(components, key=lambda x: re.sub(r'P[0-9][0-9]', 'Pxx', x))
    circuit_prin = ",".join(components)
    circuito_prin = re.sub("^,*","",circuito_prin)

    #circuit_prin = normalizar_circuito(circuit_prin)

    return circuit_prin