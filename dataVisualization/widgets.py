import panel as pn
import dataPreprocessing as pp

def create_widgets(act_df, act_ap, idf, last, freq, tct, acce, erro, cluster_sizes_k):
    #botao selecionar estudante
    select_stud = pn.widgets.Select(
        options = ['Select'] + act_df['sessionkey'].value_counts().index.tolist(),
        name = 'Session')

    #botao selecionar problema
    select_exp_id = pn.widgets.Select(
        options = ['Select'] + act_df['exp_id'].value_counts().index.tolist(),
        name = 'Experiment')

    # Create a Select widget for choosing the ID
    id_selector = pn.widgets.Select(name='Select ID', options=list(act_ap['exp_id'].unique()))

    return select_stud, select_exp_id, id_selector, 