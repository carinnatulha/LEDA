import numpy as np

#-----CLASSIFICAÇÃO DO ERRO ESPECIFICO-----
#Utilizando componentes protoboard e configurações das ferramentas de medição
def class_erro_esp(act_df):
    
    conditions_es = [
        {
            'condition_es': (
                (act_df['circuit'] == 'series') &
                (act_df['DC+6V'] == 1) &
                (act_df['DC6+_volt_p1'] == 1) &
                (act_df['DMM_v'] == 1) &
                (act_df['DMM_conf'] == 'dc volt') 
            ),
            'error_esp': 'error 1.0',
        },
        {
            'condition_es': (
                ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                (act_df['DC+6V'] == 1) &
                (act_df['DC6+_volt_p1'] == 1) &
                (act_df['DMM_mA'] == 1) &
                (act_df['DMM_conf'] == 'dc current') 
            ),
            'error_esp': 'error 1.0', #significa que é uma atividade conf certa
        },
        {
            'condition_es': (
                (act_df['circuit'] == 'series') &
                (act_df['DC+6V'] == 1) &
                (act_df['DC6+_volt_p1'] == 1) &
                (act_df['DMM_v'] == 1) &
                (act_df['DMM_conf'] == 'dc volt') 
            ),
            'error_esp': 'error 1.0', #significa que é uma atividade conf certa
        },
        {
            'condition_es': (
                act_df['circuit'] == '0 resistor'
            ),
            'error_esp': 'error 1.1', # sem resistor
        },
    # error 1.2 circuito montado errado
        {
            'condition_es': (
                ((act_df['circuit'] == 'parallel') | 
                (act_df['circuit'] == 'mist'))
            ),
            'error_esp': 'error 1.2', # circuito montado errado
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] == 'dc current') 
                ),
                'error_esp': 'error 1.2', #nenhum componente conectado e dc current
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] == 'dc volt')
                ),
                'error_esp': 'error 1.2', #nenhum componente conectado e dc volt
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] != 'dc current')
                ),
                'error_esp': 'error 1.2', #nenhum componente conectado e conf errada
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] != 'dc volt')
                ),
                'error_esp': 'error 1.2', #nenhum componente conectado e conf errada
        },
        {
            'condition_es': (
                (act_df['circuit'] == '1 resistor') &
                (act_df['DC+6V'] == 1) &
                (act_df['DC6+_volt_p1'] == 1) &
                (act_df['DMM_mA'] == 0) &
                (act_df['DMM_v'] == 1) &
                (act_df['DMM_conf'] == 'dc volt') 
            ),
                'error_esp': 'error 1.2', #nenhum componente conectado e conf errada
        },
        
    #erro 1.3 fonte nao conectada
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] == 'dc volt')
                ),
                'error_esp': 'error 1.3',  #volt
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] == 'dc current')
                ),
                'error_esp': 'error 1.3', #corrent
        }, 
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] == 'dc current') 
                ),
                'error_esp': 'error 1.3.1', #fonte valor errado
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] == 'dc volt')
                ),
                'error_esp': 'error 1.3.1',  #fonte valor errado
        },   
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] == 'dc current')
                ),
                'error_esp': 'error 1.3.2',  #multimetro nao conectado
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] == 'dc volt')
                ),
                'error_esp': 'error 1.3.2',  #multimetro nao conectado
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] != 'dc current')
                ),
                'error_esp': 'error 1.3.2',   #multimetro nao conectado
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] != 'dc volt')
                ),
                'error_esp': 'error 1.3.2',   #multimetro nao conectado
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] == 'dc current')
                ),
                'error_esp': 'error 1.3.3', #multimetro conetado errado 
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] == 'dc volt')
                ),
                'error_esp': 'error 1.3.3', #multimetro conetado errado 
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] != 'dc current')
                ),
                'error_esp': 'error 1.3.3', #multimetro conetado errado 
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] != 'dc volt')
                ),
                'error_esp': 'error 1.3.3', #multimetro conetado errado 
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] == 'dc current')
                ),
                'error_esp': 'error 1.3.4',  #multimetro conf errado
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] == 'dc volt')
                ),
                'error_esp': 'error 1.3.4',  #multimetro conf errado
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] != 'dc current')
                ),
                'error_esp': 'error 1.3.4',  #multimetro conf errado
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] != 'dc volt')
                ),
                'error_esp': 'error 1.3.4',  #multimetro conf errado
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] == 'dc current')
                ),
                'error_esp': 'error 1.3.5', #fonte valor errado, multimetro conectado errado
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] == 'dc volt')
                ),
                'error_esp': 'error 1.3.5', #fonte valor errado, multimetro conectado errado
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] != 'dc current')
                ),
                'error_esp': 'error 1.3.5', #fonte valor errado, multimetro conectado errado
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] != 'dc volt')
                ),
                'error_esp': 'error 1.3.5', #fonte valor errado, multimetro conectado errado
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] == 'dc current')
                ),
                'error_esp': 'error 1.3.6', #fonte valor errado, multimetro conf errado
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] == 'dc volt')
                ),
                'error_esp': 'error 1.3.6', #fonte valor errado, multimetro conf errado
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] != 'dc volt')
                ),
                'error_esp': 'error 1.3.6', #fonte valor errado, multimetro conf errado
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 0) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] != 'dc current')
                ),
                'error_esp': 'error 1.3.6', #fonte valor errado, multimetro conf errado
        },
        
    #erro 1.4 fonte valor errado
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] == 'dc current')
                ),
                'error_esp': 'error 1.4', #
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] == 'dc volt')
                ),
                'error_esp': 'error 1.4', #
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] == 'dc current')
                ),
                'error_esp': 'error 1.4.2', #multimetro nao conectado
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] == 'dc volt')
                ),
                'error_esp': 'error 1.4.2', #multimetro nao conectado
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] != 'dc current')
                ),
                'error_esp':'error 1.4.2', #multimetro nao conectado
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] != 'dc volt')
                ),
                'error_esp': 'error 1.4.2', #multimetro nao conectado
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] == 'dc current')
                ),
                'error_esp': 'error 1.4.2', #multimetro conectado errado
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] == 'dc volt')
                ),
                'error_esp':'error 1.4.3', #multimetro conectado errado
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] != 'dc current')
                ),
                'error_esp': 'error 1.4.3', #multimetro conectado errado
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] != 'dc volt')
                ),
                'error_esp': 'error 1.4.3', #multimetro conectado errado
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] == 'dc current')
                ),
                'error_esp': 'error 1.4.4', #multimetro conf errado
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] != 'dc volt')
                ),
                'error_esp': 'error 1.4.4', #multimetro conf errado
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 0) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] != 'dc current')
                ),
                'error_esp': 'error 1.4.4', #multimetro conf errado
        },

        
    #error 1.5 dmm nao conectado
    {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] == 'dc current')
                ),
                'error_esp': 'error 1.5', 
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] == 'dc volt')
                ),
                'error_esp': 'error 1.5', # 
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] != 'dc current')
                ),
                'error_esp': 'error 1.5', #
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] != 'dc volt')
                ),
                'error_esp': 'error 1.5', # 
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] == 'dc current')
                ),
                'error_esp': 'error 1.5.3', #dmm conectada errado
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] == 'dc volt')
                ),
                'error_esp': 'error 1.5.3', #dmm conectada errado
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  1) &
                    ((act_df['DMM_conf'] != 'dc current') | (act_df['DMM_conf'] != 'dc volt'))
                ),
                'error_esp': 'error 1.5.3', #dmm conectada errado
        },
        
    #erro 1.6 multímetro conf errado
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] == 'dc current')
                ),
                'error_esp': 'error 1.6', 
        },  
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 0) & 
                    (act_df['DMM_v'] ==  1) &
                    (act_df['DMM_conf'] != 'dc volt')
                ),
                'error_esp': 'error 1.6', 
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] == 'dc volt')
                ),
                'error_esp': 'error 1.6', 
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] != 'dc current')
                ),
                'error_esp': 'error 1.6', 
        },
        {
                'condition_es': (
                    ((act_df['circuit'] == '1 resistor') | (act_df['circuit'] == 'series')) &
                    (act_df['DC+6V'] == 1) &
                    (act_df['DC6+_volt_p1'] == 1) &
                    (act_df['DMM_mA'] == 1) & 
                    (act_df['DMM_v'] ==  0) &
                    (act_df['DMM_conf'] != 'dc volt')
                ),
                'error_esp': 'error 1.6', 
        },
    #dmm valor errado
        {
            'condition_es': (
                (act_df['circuit'] == '1 resistor') &
                (act_df['DC+6V'] == 1) &
                (act_df['DC6+_volt_p1'] == 1) &
                (act_df['DMM_mA'] == 1) &
                (act_df['DMM_v'] == 0) & 
                (act_df['DMM_conf'] == 'dc current') &
                ((act_df['value_p11_10'] == 0) | (act_df['value_p11_12'] == 0) | (act_df['value_p11_470'] == 0))
            ),
            'error_esp': 'error 1.7', # DMM valor errado
        },
        {
            'condition_es': (
                (act_df['circuit'] == 'series') &
                (act_df['DC+6V'] == 1) &
                (act_df['DC6+_volt_p1'] == 1) &
                (act_df['DMM_mA'] == 1) &
                (act_df['DMM_v'] == 0) &
                (act_df['DMM_conf'] == 'dc current') &
                (act_df['value_p12'] == 0)
            ),
            'error_esp': 'error 1.7', # DMM valor errado
        },
        {
            'condition_es': (
                (act_df['circuit'] == 'series') &
                (act_df['DC+6V'] == 1) &
                (act_df['DC6+_volt_p1'] == 1) &
                (act_df['DMM_mA'] == 0) &
                (act_df['DMM_v'] == 1) &
                (act_df['DMM_conf'] == 'dc volt') &
                ((act_df['value_p13_470'] == 0) | (act_df['value_p13_12'] == 0) | (act_df['value_p13_10'] == 0))
            ),
            'error_esp': 'error 1.7', # DMM valor errado
        },
            {
            'condition_es': (
                (act_df['circuit'] == '1 resistor') &
                (act_df['DC+6V'] == 1) &
                (act_df['DC6+_volt_p1'] == 1) &
                (act_df['DMM_mA'] == 1) &
                (act_df['DMM_v'] == 1) & 
                (act_df['DMM_conf'] == 'dc current') &
                ((act_df['value_p11_10'] == 0) | (act_df['value_p11_12'] == 0) | (act_df['value_p11_470'] == 0))
            ),
            'error_esp': 'error 1.7.3', #multimetro conectado errado
        },
        {
            'condition_es': (
                (act_df['circuit'] == 'series') &
                (act_df['DC+6V'] == 1) &
                (act_df['DC6+_volt_p1'] == 1) &
                (act_df['DMM_mA'] == 1) &
                (act_df['DMM_v'] == 1) &
                (act_df['DMM_conf'] == 'dc current') &
                (act_df['value_p12'] == 0)
            ),
            'error_esp': 'error 1.7.3', #multimetro conectado errado
        },
        {
            'condition_es': (
                (act_df['circuit'] == 'series') &
                (act_df['DC+6V'] == 1) &
                (act_df['DC6+_volt_p1'] == 1) &
                (act_df['DMM_mA'] == 1) &
                (act_df['DMM_v'] == 1) &
                (act_df['DMM_conf'] == 'dc volt') &
                ((act_df['value_p13_470'] == 0) | (act_df['value_p13_12'] == 0) | (act_df['value_p13_10'] == 0))
            ),
            'error_esp': 'error 1.7.3', #multimetro conectado errado
        },
        {
            'condition_es': (
                (act_df['circuit'] == '1 resistor') &
                (act_df['DC+6V'] == 1) &
                (act_df['DC6+_volt_p1'] == 1) &
                (act_df['DMM_mA'] == 0) &
                (act_df['DMM_v'] == 1) & 
                (act_df['DMM_conf'] == 'dc current') &
                ((act_df['value_p11_10'] == 0) | (act_df['value_p11_12'] == 0) | (act_df['value_p11_470'] == 0))
            ),
            'error_esp': 'error 1.7.3', #multimetro conf errado
        },
        {
            'condition_es': (
                (act_df['circuit'] == 'series') &
                (act_df['DC+6V'] == 1) &
                (act_df['DC6+_volt_p1'] == 1) &
                (act_df['DMM_mA'] == 0) &
                (act_df['DMM_v'] == 1) &
                (act_df['DMM_conf'] == 'dc current') &
                (act_df['value_p12'] == 0)
            ),
            'error_esp': 'error 1.7.3', #multimetro conf errado
        },
        {
            'condition_es': (
                (act_df['circuit'] == 'series') &
                (act_df['DC+6V'] == 1) &
                (act_df['DC6+_volt_p1'] == 1) &
                (act_df['DMM_mA'] == 1) &
                (act_df['DMM_v'] == 0) &
                (act_df['DMM_conf'] == 'dc volt') &
                ((act_df['value_p13_470'] == 0) | (act_df['value_p13_12'] == 0) | (act_df['value_p13_10'] == 0))
            ),
            'error_esp': 'error 1.7.3', #multimetro conf errado
        },
    {
            'condition_es': (
                (act_df['circuit'] == '1 resistor') &
                (act_df['DC+6V'] == 1) &
                (act_df['DC6+_volt_p1'] == 1) &
                (act_df['DMM_mA'] == 0) &
                (act_df['DMM_v'] == 0) & 
                (act_df['DMM_conf'] == 'dc current') &
                ((act_df['value_p11_10'] == 0) | (act_df['value_p11_12'] == 0) | (act_df['value_p11_470'] == 0))
            ),
            'error_esp': 'error 1.7.4', #multimetro nao conectado
        },
        {
            'condition_es': (
                (act_df['circuit'] == 'series') &
                (act_df['DC+6V'] == 1) &
                (act_df['DC6+_volt_p1'] == 1) &
                (act_df['DMM_mA'] == 1) &
                (act_df['DMM_v'] == 0) &
                (act_df['DMM_conf'] == 'dc current') &
                (act_df['value_p12'] == 0)
            ),
            'error_esp': 'error 1.7.4', #multimetro nao conectado
        },
        {
            'condition_es': (
                (act_df['circuit'] == 'series') &
                (act_df['DC+6V'] == 1) &
                (act_df['DC6+_volt_p1'] == 1) &
                (act_df['DMM_mA'] == 0) &
                (act_df['DMM_v'] == 0) &
                (act_df['DMM_conf'] == 'dc volt') &
                ((act_df['value_p13_470'] == 0) | (act_df['value_p13_12'] == 0) | (act_df['value_p13_10'] == 0))
            ),
            'error_esp': 'error 1.7.4', #multimetro nao conectado
        },
    ]

    act_df['error_esp'] = ''

    for cond in conditions_es:
        condition_mask_es = cond['condition_es']
        act_df['error_esp'] = np.where(condition_mask_es, cond['error_esp'], act_df['error_esp'])

    return act_df