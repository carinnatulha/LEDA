import pandas as pd
import numpy as np
import dataPreprocessing.preprocessing as pp

#----CLASSIFICAÇÃO DO ERRO
#considerando os componentes e configurações das ferramentas de medição
def class_erro_comp(act_df, class_error):
    class_error['Session'] = act_df['sessionkey']
    class_error['Experiment'] = act_df['exp_id']
    class_error['Component'] = np.where((act_df['DC+6V'] == 0) | (act_df['DMM_mA'] == 0) | ((act_df['R470K'] == 0) | (act_df['R12K'] == 0) | (act_df['R10K'] == 0)), 1, 0)
    class_error['Electric Power'] = np.where((act_df['error_id'] == 'error 1.4'), 1, 0)
    class_error['Measument Tool Configuration'] = np.where((act_df['error_id'] == 'error 1.6'), 1, 0)
    class_error['Measument Tool Value'] = np.where((act_df['error_id'] == 'error 1.7'), 1, 0)
    class_error['Circuit'] = np.where((act_df['error_id'] == 'error 1.1') | (act_df['error_id'] == 'error 1.2'), 1, 0)
    class_error['Error_warning'] = pp.df2['system_response'].str.extract(r'^(.*?Either)').fillna(0)
    class_error['Error_warning'] = class_error['Error_warning'].replace('<protocol version="1.3"> <error> The circuit cannot be constructed. Either', 1)

    return class_error

#-----CLASSIFICAÇÃO DO ERRO GERAL-----
#Utilizando componentes protoboard e configurações das ferramentas de medição
def class_erro_geral(act_df):

    conditions_a = [
        {
            'condition_a': (
                (act_df['circuit'] == 'series') &
                (act_df['DC+6V'] == 1) &
                (act_df['DC6+_volt_p1'] == 1) &
                (act_df['DMM_mA'] == 0) &
                (act_df['DMM_v'] == 1) &
                (act_df['DMM_conf'] == 'dc volt') 
            ),
            'exp_id': 'exp 3',
        },
        {
            'condition_a': (
                (act_df['circuit'] == '1 resistor') &
                (act_df['DC+6V'] == 1) &
                (act_df['DC6+_volt_p1'] == 1) &
                (act_df['DMM_mA'] == 1) &
                (act_df['DMM_v'] == 0) &
                (act_df['DMM_conf'] == 'dc current') 
            ),
            'exp_id': 'exp 1', #significa que é uma atividade conf certa
        },
        {
            'condition_a': (
                (act_df['circuit'] == 'series') &
                (act_df['DC+6V'] == 1) &
                (act_df['DC6+_volt_p1'] == 1) &
                (act_df['DMM_mA'] == 1) &
                (act_df['DMM_v'] == 0) &
                (act_df['DMM_conf'] == 'dc current') 
            ),
            'exp_id': 'exp 2', #significa que é uma atividade conf certa
        },
        {
            'condition_a': (
                (act_df['circuit'] == '1 resistor') &
                (act_df['DC+6V'] == 1) &
                (act_df['DC6+_volt_p1'] == 1) &
                (act_df['DMM_mA'] == 0) &
                (act_df['DMM_v'] == 1) &
                (act_df['DMM_conf'] == 'dc volt') 
            ),
            'exp_id': 'exp 3',
        },
        {
            'condition_a': (
                act_df['circuit'] == '0 resistor'
            ),
            'exp_id': 'exp 0', # sem resistor
        },
    # error 1.2 circuito montado errado
        {
            'condition_a': (
                ((act_df['circuit'] == 'parallel') | 
                (act_df['circuit'] == 'mist'))
            ),
            'exp_id': 'exp 0', # circuito montado errado
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] == 'dc current') 
                ),
                'exp_id': 'exp 0', #nenhum componente conectado e dc current
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] == 'dc volt')
                ),
                'exp_id': 'exp 0', #nenhum componente conectado e dc volt
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] != 'dc current')
                ),
                'exp_id': 'exp 0', #nenhum componente conectado e conf errada
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] != 'dc volt')
                ),
                'exp_id': 'exp 0', #nenhum componente conectado e conf errada
        },
        
    #erro 1.3 fonte nao conectada
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] == 'dc current')
                ),
                'exp_id': 'exp 1.3',  #volt
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] == 'dc volt')
                ),
                'exp_id': 'exp 1.3',  #volt
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] == 'dc current')
                ),
                'exp_id': 'exp 1.1', #corrent
        },
        {
                'condition_a': (
                    (act_df['circuit'] == '1 resistor')  &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] == 'dc volt')
                ),
                'exp_id': 'exp 1.1', #volt
        },
        {
                'condition_a': (
                    (act_df['circuit'] == 'series') &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] == 'dc volt')
                ),
                'exp_id': 'exp 1.2', #volt
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] == 'dc current') 
                ),
                'exp_id': 'exp 1.3', #fonte valor errado
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] == 'dc volt') 
                ),
                'exp_id': 'exp 1.3', #fonte valor errado
        },
        {
                'condition_a': (
                    (act_df['circuit'] == '1 resistor') &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] == 'dc current')
                ),
                'exp_id': 'exp 1.1',  #fonte valor errado
        },
        {
                'condition_a': (
                    (act_df['circuit'] == 'series') &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] == 'dc current')
                ),
                'exp_id': 'exp 1.2',  #fonte valor errado
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] == 'dc volt')
                ),
                'exp_id': 'exp 1.2',  #fonte valor errado
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] == 'dc current')
                ),
                'exp_id': 'exp 1.2',  #multimetro nao conectado
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] == 'dc volt')
                ),
                'exp_id': 'exp 0',  #multimetro nao conectado
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] != 'dc current')
                ),
                'exp_id': 'exp 0',   #multimetro nao conectado
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] != 'dc volt')
                ),
                'exp_id': 'exp 0',   #multimetro nao conectado
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] == 'dc current')
                ),
                'exp_id': 'exp 2', #multimetro conetado errado 
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] == 'dc volt')
                ),
                'exp_id': 'exp 3', #multimetro conetado errado 
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] != 'dc current')
                ),
                'exp_id': 'exp 1.3', #multimetro conetado errado 
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] != 'dc volt')
                ),
                'exp_id': 'exp 1.2', #multimetro conetado errado 
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] == 'dc current')
                ),
                'exp_id': 'exp 1.3',  #multimetro conf errado
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] == 'dc volt')
                ),
                'exp_id': 'exp 1.2',  #multimetro conf errado
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] != 'dc current')
                ),
                'exp_id': 'exp 1.2',  #multimetro conf errado
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] != 'dc volt')
                ),
                'exp_id': 'exp 1.3',  #multimetro conf errado
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] == 'dc current')
                ),
                'exp_id': 'exp 1.2', #fonte valor errado, multimetro conectado errado
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] == 'dc volt')
                ),
                'exp_id': 'exp 1.3', #fonte valor errado, multimetro conectado errado
        },
        {
                'condition_a': (
                    (act_df['circuit'] == 'series') &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] != 'dc current')
                ),
                'exp_id': 'exp 1.3', #fonte valor errado, multimetro conectado errado
        },
        {
                'condition_a': (
                    (act_df['circuit'] == '1 resistor') &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] != 'dc current')
                ),
                'exp_id': 'exp 1.1', #fonte valor errado, multimetro conectado errado
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] != 'dc volt')
                ),
                'exp_id': 'exp 0', #fonte valor errado, multimetro conectado errado
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] == 'dc current')
                ),
                'exp_id': 'exp 1.3', #fonte valor errado, multimetro conf errado
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] == 'dc volt')
                ),
                'exp_id': 'exp 1.2', #fonte valor errado, multimetro conf errado
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] != 'dc volt')
                ),
                'exp_id': 'exp 1.3', #fonte valor errado, multimetro conf errado
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] != 'dc current')
                ),
                'exp_id': 'exp 1.2', #fonte valor errado, multimetro conf errado
        },
        
    #erro 1.4 fonte valor errado
        {
                'condition_a': (
                    (act_df['circuit'] == '1 resistor') &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] == 'dc current')
                ),
                'exp_id': 'exp 1.1', #
        },
        {
                'condition_a': (
                    (act_df['circuit'] == 'series') &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] == 'dc current')
                ),
                'exp_id': 'exp 1.2', #
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] == 'dc volt')
                ),
                'exp_id': 'exp 1.3', #
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] == 'dc current')
                ),
                'exp_id': 'exp 0', #multimetro nao conectado
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] == 'dc volt')
                ),
                'exp_id': 'exp 0', #multimetro nao conectado
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] != 'dc current')
                ),
                'exp_id':'exp 0', #multimetro nao conectado
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] != 'dc volt')
                ),
                'exp_id': 'exp 0', #multimetro nao conectado
        },
        {
                'condition_a': (
                    (act_df['circuit'] == '1 resistor') &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] == 'dc current')
                ),
                'exp_id': 'exp 1.1', #multimetro conectado errado
        },
        {
                'condition_a': (
                    (act_df['circuit'] == 'series') &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] == 'dc current')
                ),
                'exp_id': 'exp 1.2', #multimetro conectado errado
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] == 'dc volt')
                ),
                'exp_id':'exp 1.3', #multimetro conectado errado
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] != 'dc current')
                ),
                'exp_id': 'exp 1.2', #multimetro conectado errado
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] != 'dc volt')
                ),
                'exp_id': 'exp 1.3', #multimetro conectado errado
        },
        {
                'condition_a': (
                    (act_df['circuit'] == '1 resistor') &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] == 'dc current')
                ),
                'exp_id': 'exp 1.1', #multimetro conf errado
        },
        {
                'condition_a': (
                    (act_df['circuit'] == 'series') &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] == 'dc current')
                ),
                'exp_id': 'exp 1.2', #multimetro conf errado
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] != 'dc volt')
                ),
                'exp_id': 'exp 1.3', #multimetro conf errado
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] != 'dc current')
                ),
                'exp_id': 'exp 1.2', #multimetro conf errado
        },

        
    #error 1.5 dmm nao conectado
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  0) &
                    ((act_df['DMM_conf'] != 'dc current') | (act_df['DMM_conf'] != 'dc volt'))
                ),
                'exp_id': 'exp 0', #
        },
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  1) &
                    ((act_df['DMM_conf'] != 'dc current') | (act_df['DMM_conf'] != 'dc volt'))
                ),
                'exp_id': 'exp 0', #dmm conectada errado
        },
        
    #erro 1.6 multímetro conf errado
        {
                'condition_a': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] != 'dc volt')
                ),
                'exp_id': 'exp 1.3', 
        },
        {
                'condition_a': (
                    (act_df['circuit'] == '1 resistor') &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] != 'dc current')
                ),
                'exp_id': 'exp 1.1', 
        },
        {
                'condition_a': (
                    (act_df['circuit'] == 'series') &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] != 'dc current')
                ),
                'exp_id': 'exp 1.2', 
        },
    #dmm valor errado
        {
            'condition_a': (
                (act_df['circuit'] == '1 resistor') &
                (act_df['DC+6V'] == 1) &
                (act_df['DC6+_volt_p1'] == 1) &
                (act_df['DMM_mA'] == 1) &
                (act_df['DMM_v'] == 0) & 
                (act_df['DMM_conf'] == 'dc current') &
                ((act_df['value_p11_10'] == 0) | (act_df['value_p11_12'] == 0) | (act_df['value_p11_470'] == 0))
            ),
            'exp_id': 'exp 1.1', # DMM valor errado
        },
        {
            'condition_a': (
                (act_df['circuit'] == 'series') &
                (act_df['DC+6V'] == 1) &
                (act_df['DC6+_volt_p1'] == 1) &
                (act_df['DMM_mA'] == 1) &
                (act_df['DMM_v'] == 0) &
                (act_df['DMM_conf'] == 'dc current') &
                (act_df['value_p12'] == 0)
            ),
            'exp_id': 'exp 1.2', # DMM valor errado
        },
        {
            'condition_a': (
                (act_df['circuit'] == 'series') &
                (act_df['DC+6V'] == 1) &
                (act_df['DC6+_volt_p1'] == 1) &
                (act_df['DMM_mA'] == 0) &
                (act_df['DMM_v'] == 1) &
                (act_df['DMM_conf'] == 'dc volt') &
                ((act_df['value_p13_470'] == 0) | (act_df['value_p13_12'] == 0) | (act_df['value_p13_10'] == 0))
            ),
            'exp_id': 'exp 1.3', # DMM valor errado
        },
        {
            'condition_a': (
                (act_df['circuit'] == '1 resistor') &
                (act_df['DC+6V'] == 1) &
                (act_df['DC6+_volt_p1'] == 1) &
                (act_df['DMM_mA'] == 0) &
                (act_df['DMM_v'] == 0) & 
                ((act_df['DMM_conf'] == 'dc current') | (act_df['DMM_conf'] == 'dc volt')) &
                ((act_df['value_p11_10'] == 0) | (act_df['value_p11_12'] == 0) | (act_df['value_p11_470'] == 0))
            ),
            'exp_id': 'exp 1.2', #multimetro nao conectado
        },
        {
            'condition_a': (
                (act_df['circuit'] == 'series') &
                (act_df['DC+6V'] == 1) &
                (act_df['DC6+_volt_p1'] == 1) &
                (act_df['DMM_mA'] == 1) &
                (act_df['DMM_v'] == 0) &
                ((act_df['DMM_conf'] == 'dc current') | (act_df['DMM_conf'] == 'dc volt')) &
                (act_df['value_p12'] == 0)
            ),
            'exp_id': 'exp 1.2', #multimetro nao conectado
        },
        {
            'condition_a': (
                (act_df['circuit'] == 'series') &
                (act_df['DC+6V'] == 1) &
                (act_df['DC6+_volt_p1'] == 1) &
                (act_df['DMM_mA'] == 0) &
                (act_df['DMM_v'] == 0) &
                ((act_df['DMM_conf'] == 'dc current') | (act_df['DMM_conf'] == 'dc volt')) &
                ((act_df['value_p13_470'] == 0) | (act_df['value_p13_12'] == 0) | (act_df['value_p13_10'] == 0))
            ),
            'exp_id': 'exp 1.3', #multimetro nao conectado
        },
        {
            'condition_a': (
                (act_df['circuit'] == '1 resistor') &
                (act_df['DC+6V'] == 1) &
                (act_df['DC6+_volt_p1'] == 1) &
                (act_df['DMM_mA'] == 1) &
                (act_df['DMM_v'] == 1) & 
                ((act_df['DMM_conf'] == 'dc current') | (act_df['DMM_conf'] == 'dc volt')) &
                ((act_df['value_p11_10'] == 0) | (act_df['value_p11_12'] == 0) | (act_df['value_p11_470'] == 0))
            ),
            'exp_id': 'exp 1.1', #multimetro conectado errado
        },
        {
            'condition_a': (
                (act_df['circuit'] == 'series') &
                (act_df['DC+6V'] == 1) &
                (act_df['DC6+_volt_p1'] == 1) &
                (act_df['DMM_mA'] == 1) &
                (act_df['DMM_v'] == 1) &
                ((act_df['DMM_conf'] == 'dc current') | (act_df['DMM_conf'] == 'dc volt')) &
                (act_df['value_p12'] == 0)
            ),
            'exp_id': 'exp 1.2', #multimetro conectado errado
        },
        {
            'condition_a': (
                (act_df['circuit'] == 'series') &
                (act_df['DC+6V'] == 1) &
                (act_df['DC6+_volt_p1'] == 1) &
                (act_df['DMM_mA'] == 1) &
                (act_df['DMM_v'] == 1) &
                ((act_df['DMM_conf'] == 'dc current') | (act_df['DMM_conf'] == 'dc volt')) &
                ((act_df['value_p13_470'] == 0) | (act_df['value_p13_12'] == 0) | (act_df['value_p13_10'] == 0))
            ),
            'exp_id': 'exp 1.3', #multimetro conectado errado
        },
        {
            'condition_a': (
                (act_df['circuit'] == '1 resistor') &
                (act_df['DC+6V'] == 1) &
                (act_df['DC6+_volt_p1'] == 1) &
                (act_df['DMM_mA'] == 0) &
                (act_df['DMM_v'] == 1) & 
                ((act_df['DMM_conf'] == 'dc current') | (act_df['DMM_conf'] == 'dc volt')) &
                ((act_df['value_p11_10'] == 0) | (act_df['value_p11_12'] == 0) | (act_df['value_p11_470'] == 0))
            ),
            'exp_id': 'exp 1.1', #multimetro conf errado
        },
        {
            'condition_a': (
                (act_df['circuit'] == 'series') &
                (act_df['DC+6V'] == 1) &
                (act_df['DC6+_volt_p1'] == 1) &
                (act_df['DMM_mA'] == 0) &
                (act_df['DMM_v'] == 1) &
                ((act_df['DMM_conf'] == 'dc current') | (act_df['DMM_conf'] == 'dc volt')) &
                (act_df['value_p12'] == 0)
            ),
            'exp_id': 'exp 1.2', #multimetro conf errado
        },
        {
            'condition_a': (
                (act_df['circuit'] == 'series') &
                (act_df['DC+6V'] == 1) &
                (act_df['DC6+_volt_p1'] == 1) &
                (act_df['DMM_mA'] == 1) &
                (act_df['DMM_v'] == 0) &
                ((act_df['DMM_conf'] == 'dc current') | (act_df['DMM_conf'] == 'dc volt')) &
                ((act_df['value_p13_470'] == 0) | (act_df['value_p13_12'] == 0) | (act_df['value_p13_10'] == 0))
            ),
            'exp_id': 'exp 1.3', #multimetro conf errado
        },
    
    ]

    act_df['exp_id'] = ''

    for cond in conditions_a:
        condition_mask_es = cond['condition_a']
        act_df['exp_id'] = np.where(condition_mask_es, cond['exp_id'], act_df['exp_id'])

    return act_df