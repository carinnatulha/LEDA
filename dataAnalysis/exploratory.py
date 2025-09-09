import pandas as pd
import numpy as np
import dataPreprocessing.normalization as pp
from collections import Counter


def error_analysis(act_df, class_error):

    act_df.groupby('exp_id')['sessionkey'].nunique()

    total_exp = act_df.groupby('exp_id').size()
    total_error = act_df.groupby('error_id').size()
    total_error_g = act_df.groupby('error_id')['sessionkey'].nunique()
    total_error_esp = act_df.groupby('error_esp').size()
    total_error_esp_g = act_df.groupby('error_esp')['sessionkey'].nunique()

    class_errorFinal = class_error.groupby('Session').tail(1)
    class_errorFinal.reset_index(drop=True, inplace=True)
    calss_errorF_g = class_errorFinal.groupby('Experiment').sum()

    return act_df, total_exp, total_error, total_error_g, total_error_esp, total_error_esp_g, calss_errorF_g

#----SCORE-----
def score_calculation(act_df, class_error):
    act_df = pd.get_dummies(act_df, columns=['circuit', 'DMM_conf'])

    cols11 = ['R10K', 'R12K', 'R470K', 'DC6+_volt_p1', 'DC+6V', 'DMM_mA', 'DMM_conf_dc current']
    cols12 = ['R10K', 'R12K', 'R470K', 'DC6+_volt_p1', 'DC+6V', 'DMM_mA', 'DMM_conf_dc current']
    cols13 = ['R10K', 'R12K', 'R470K', 'DC6+_volt_p1', 'DC+6V','DMM_v', 'DMM_conf_dc volt']

    #act_df['score_float'] = 0.0
    act_df.loc[(act_df['exp_id'] == '0', 'score')] = 0
    act_df.loc[(act_df['exp_id'] == 'exp 1.1', 'score')] = np.round(act_df[cols11].sum(axis=1)/5, decimals = 2)
    act_df.loc[(act_df['exp_id'] == 'exp 1.2', 'score')] = np.round(act_df[cols12].sum(axis=1)/8, decimals = 2)
    act_df.loc[(act_df['exp_id'] == 'exp 1.3', 'score')] = np.round(act_df[cols13].sum(axis=1)/8, decimals = 2)
    act_df['score'] = act_df['score'].fillna(0) 

    class_errorFinal = class_error.groupby('Session').tail(1)
    class_errorFinal.reset_index(drop=True, inplace=True)

    class_errorFinal

    calss_errorF_g = class_errorFinal.groupby('Experiment').sum()
    
    return act_df, class_errorFinal, calss_errorF_g

#-----CONTAGEM DE EXECUÇÕES-----

def exec_count(act_df):
    session = act_df.sessionkey.eq(act_df.sessionkey.shift())

    count = 1
    exe = []

    #contagem de alterações (linhas) considerando sessão
    for row in session:
        if row == False:
            count = 1
            exe.append(count)
        elif row == True:
            count +=1
            exe.append(count)

    act_df.insert(2, "execution_count", exe, True)
    return act_df

#-----MANUPILAÇÕES-----
def manip_analysis(act_df, df1, df3):
    manip = pd.DataFrame()
    num_access = (df1['user_request'].str.contains('@@@initial::request@@@')).sum()
    manip['Session'] = act_df.groupby('exp_id')['sessionkey'].nunique()

    #----circuitos unicos
    df3['exp_id'] = act_df['exp_id'][:]
    manip['circ_uniq'] = df3.groupby('exp_id')['breadboard_simp'].nunique()

    manip = manip.reset_index()
    return manip

#-----TEMPO DE ATIVIDADE-----
def time_analysis(act_df):
    UserAtivFinal = act_df[:]

    UserAtivFinal['time_request'] = pd.to_datetime(UserAtivFinal['time_request'])

    UserAtivFinal['time_difference'] = UserAtivFinal.groupby(['sessionkey'])['time_request'].transform(lambda x: x.iloc[-1] - x.iloc[0])
    UserAtivFinal['time_difference'] = UserAtivFinal['time_difference'].astype(str).str[-8:]

    return UserAtivFinal

#------MÉDIA DE EXECUÇÃO DE EXECUÇÃO POR EXPERIMENTO-----
def mean_time_per_experiment(UserAtivFinal):
    mean_executions_per_exp = UserAtivFinal.groupby('exp_id')['execution_count'].mean()
    
    return mean_executions_per_exp


#-------MÉDIA DE TEMPO POR EXPERIMENTO-----
def mean_time_per_experiment(UserAtivFinal):
    UserAtivFinal['time_difference'] = pd.to_timedelta(UserAtivFinal['time_difference'])
    mean_time_per_exp = UserAtivFinal.groupby('exp_id')['time_difference'].mean()

    return mean_time_per_exp

#------ULTIMA ATIVIDADE-----
def last_activity(UserAtivFinal):
    UserAtivFinal = UserAtivFinal.groupby('sessionkey').tail(1)
    UserAtivFinal.reset_index(drop=True, inplace=True)

    mean_executions_per_exp = UserAtivFinal.groupby('exp_id')['execution_count'].mean()
    UserAtivFinal['time_difference'] = pd.to_timedelta(UserAtivFinal['time_difference'])
    mean_time_per_exp = UserAtivFinal.groupby('exp_id')['time_difference'].mean()

    return UserAtivFinal, mean_executions_per_exp, mean_time_per_exp

#-----ANÁLISE DE SEQUENCIAS----- 
def sequence_analysis(df3):
    grupos = df3.groupby(['sessionkey'])

    def identificar_sequencias_repetidas(grupo):
        sequencias = grupo['breadboard_norm'].str.split(',').tolist()
        sequencias_unicas = []
        sequencias_repetidas = []

        for sequencia in sequencias:
            if sequencia not in sequencias_unicas:
                sequencias_unicas.append(sequencia)
            else:
                sequencias_repetidas.append(sequencia)

        return sequencias_repetidas

    # Aplique a função de identificação de sequências repetidas a cada grupo de usuário
    seq_rep = grupos.apply(identificar_sequencias_repetidas)

    return seq_rep, grupos

#-----PADRÃO DE REPETIÇÃO-----

def repeat_pattern_analysis(grupos):
# Inicialize um dicionário para armazenar os padrões de repetição por usuário
    padroes_de_repeticao_por_usuario = {}

    # Itere sobre cada grupo (cada usuário)
    for student, grupo in grupos:
        acoes = grupo['breadboard_norm'].str.split(',')
        
        # Use o Counter para contar a frequência de cada sequência de ações
        contagem_acoes = Counter([tuple(acao) for acao in acoes])
        
        # Identifique as sequências de ações repetidas (com contagem maior que 1)
        padroes_de_repeticao = {acao: frequencia for acao, frequencia in contagem_acoes.items()}
        
        # Armazene os padrões de repetição para este usuário
        padroes_de_repeticao_por_usuario[student] = padroes_de_repeticao

    # Exiba os padrões de repetição por usuário
    for usuario, padroes in padroes_de_repeticao_por_usuario.items():
        print(f"Session: {student}")
        for acao, frequencia in padroes.items():
            print(f"   Sequência: {', '.join(acao)} - Frequência: {frequencia}")

    return padroes_de_repeticao_por_usuario
        
#-----CIRCUITOS MAIS FREQUENTES----
def frequent_circuits_analysis(df3):
    # Contar a frequência de breadboard_norm para cada problema
    freq_prob = df3.groupby(['exp_id', 'breadboard_norm']).size().reset_index(name='Frequency')

    freq_df = freq_prob.groupby('exp_id').apply(lambda x: x.nlargest(5, 'Frequency')).reset_index(drop=True)
    freq_df = freq_df.rename(columns={'breadboard_norm': 'Circuit'})

    return freq_df