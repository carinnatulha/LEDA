import pandas as pd
import numpy as np
import re

                           #--------PRE-PROCESSAMENTO--------
def create_tables(df1) -> pd.DataFrame:
    #----ACESSO-----
    df2 = df1.loc[df1['user_request'].str.contains(r'^(?=.*protocol)')]
    df2.reset_index(drop=True, inplace=True)
    act_df = df2.drop(['user_request', 'system_response', 'time_response'], axis=1)
    #----ID-------
    sessionkey_list= df2['user_request'].str.extract(r'(?s:.*sessionkey)([a-zA-Z0-9=!><#$&()\\-`.+,/\" :]+)')
    sessionkey_list.fillna(method='bfill', inplace=True)
    sessionkey_list = sessionkey_list[0].str.slice(start=6, stop=35).to_list()
    act_df.insert(0, "sessionkey", sessionkey_list, True)
    act_df['sessionkey'] = act_df['sessionkey'].replace('"', '', regex=True)

    #-----DATA-------
    act_df['time_request'] = pd.to_datetime(act_df['time_request'], errors='coerce')
    #act_df['date'] = act_df['time_request'].dt.date
    #act_df['time'] = act_df['time_request'].dt.time

    #-----BREADBOARD-----
    act_df['breadboard'] = df2['user_request'].str.extract(r'(?s:.+<circuitlist>)([a-zA-Z0-9=!#$&()\\-`.+,/\" ]+)(?:./circuitlist>)').fillna('')
    act_df['breadboard'] = act_df['breadboard'].replace(r'(\d+(?:\.\d+)?[kKMGTPEZY]?)_X\b', r'\1', regex=True)
    
    return act_df, df2

def process_breadboard_column(act_df, column='breadboard') -> pd.DataFrame:
    patterns = {
        "W_X": r'(W_X\s+\S+\s+\S+)',
        "R_X": r'(R_X\s+\S+\s+\S+\s+\S+)',
        "C_X": r'(C_X\s+\S+\s+\S+\s+\S+)',
        "DMM": r'(DMM_[12]\s+\S+\s+\S+)',
        "VDC": r'(VDC\+6V_1\s+\S+)',
        "PROBE": r'(IPROBE_[12]\s+\S+\s+\S+)'
    }

    def find_matches(row):
        matches = []
        for key, pattern in patterns.items():
            found = re.findall(pattern, row)
            if found:
                matches.append(', '.join(found))
        return ', '.join(matches)

    act_df[column] = act_df[column].apply(find_matches)

    return act_df

def cleaning(act_df, df2)-> pd.DataFrame:

    #LIMPEZA
    act_df['breadboard'] = act_df['breadboard'].replace(r'470', r'470k', regex=True)
    act_df['breadboard'] = act_df['breadboard'].replace(r'([A]\d{1})([A-Z]_X)\b', r'\1, \2', regex=True)
    act_df['breadboard'] = act_df['breadboard'].replace(r'([A]\d{2})([A-Z]_X)\b', r'\1, \2', regex=True)
    act_df['breadboard'] = act_df['breadboard'].replace(r'(\d+k)(\w+)',  r'\1, \2', regex=True)
    act_df['breadboard'] = act_df['breadboard'].replace(r'(DMM_1_[12])([A-Z])',  r'\1, \2', regex=True)
    act_df['breadboard'] = act_df['breadboard'].replace(r'(IPROBE_1_[12])([A-Z])',  r'\1, \2', regex=True)
    act_df['breadboard'] = act_df['breadboard'].replace(r'(25V_1_[12])([A-Z]_X)',  r'\1, \2', regex=True)
    act_df['breadboard'] = act_df['breadboard'].replace(r'(0)([A-Z])',  r'\1, \2', regex=True)
    act_df['breadboard'] = act_df['breadboard'].replace(r'(S)([A-Z])',  r'\1, \2', regex=True)
    act_df['breadboard'] = act_df['breadboard'].replace(r'(100)([A-Z])',  r'\1k, \2', regex=True)
    act_df['breadboard'] = act_df['breadboard'].replace(r'(100)',  r'\1k', regex=True)
    act_df['breadboard'] = act_df['breadboard'].replace(r'([F]\d{1})([A-Z]_X)\b', r'\1, \2', regex=True)
    act_df['breadboard'] = act_df['breadboard'].replace(r'([F]\d{2})([A-Z]_X)\b', r'\1, \2', regex=True)

    #substituir A para V
    act_df['breadboard'] = act_df['breadboard'].replace(r'DMM_AHI',  r'DMM_VHI', regex=True)
    act_df['breadboard'] = act_df['breadboard'].replace(r'DMM_ALO',  r'DMM_VLO', regex=True)

    #substituir identificação do aterramento de 0 para GND
    act_df['breadboard'] = act_df['breadboard'].replace(r"([^A-Z0-9])0([^A-Z0-9])",  r"\1GND\2 ", regex=True)
    act_df['breadboard'] = act_df['breadboard'].replace(r"([^A-Z0-9])0$",  r"\1GND", regex=True)

    #alterar registro de posição para um sistema único Axx
    act_df['breadboard'] = act_df['breadboard'].replace(r"A([0-9][^0-9])",  r"A0\1", regex=True)
    act_df['breadboard'] = act_df['breadboard'].replace(r"F1([0-9])",  r"A6\1", regex=True)
    act_df['breadboard'] = act_df['breadboard'].replace(r"F2([0-9])",  r"A7\1", regex=True)
    act_df['breadboard'] = act_df['breadboard'].replace(r"F3([0-9])",  r"A8\1", regex=True)
    act_df['breadboard'] = act_df['breadboard'].replace(r"F([0-9])",  r"A5\1", regex=True)
    act_df['breadboard'] = act_df['breadboard'].replace(r"([^A-Z0-9_])X([^A-Z0-9_])", r"\1 A90 \2", regex=True)
    act_df['breadboard'] = act_df['breadboard'].replace(r"([^A-Z0-9_])X$",  r"\1A90", regex=True)
    act_df['breadboard'] = act_df['breadboard'].replace(r"([^A-Z0-9_])Y([^A-Z0-9_])", r"\1 A91 \2", regex=True)
    act_df['breadboard'] = act_df['breadboard'].replace(r"([^A-Z0-9_])Y$",  r"\1A91", regex=True)
    act_df['breadboard'] = act_df['breadboard'].replace(r"([^A-Z0-9_])S([^A-Z0-9_])", r"\1 A92 \2", regex=True)
    act_df['breadboard'] = act_df['breadboard'].replace(r"([^A-Z0-9_])S$",  r"\1A92", regex=True)
    act_df['breadboard'] = act_df['breadboard'].replace(r"([^A-Z0-9_])T([^A-Z0-9_])", r"\1 A93 \2", regex=True)
    act_df['breadboard'] = act_df['breadboard'].replace(r"([^A-Z0-9_])T$",  r"\1 A93", regex=True)

    #-----FONTE-----

    act_df['DC'] = df2['system_response'].str.extract(r'(?s:.+<dc_outputs>)([a-zA-Z0-9=!><#$&()\\-`.+,_/\" V-]+)(?:.</dc_outputs>)').fillna(0)

    act_df['DC6+'] = act_df['DC'].str.extract(r'<dc_output channel="6V\+">(.*?)</dc_output>').fillna(0)
    act_df['DC6+_volt'] = act_df['DC6+'].str.extract(r' value="(.*?)/> <dc_current').fillna(0)
    act_df['DC6+_cur'] = act_df['DC6+'].str.extract(r'<dc_current value=(.*?)/> <dc_voltage_actual').fillna(0)
    act_df['DC6+_volt'] = act_df['DC6+_volt'].replace('"', '', regex=True)
    act_df['DC6+_cur'] = act_df['DC6+_cur'].replace('"', '', regex=True)

    act_df['DC25+'] = act_df['DC'].str.extract(r'<dc_output channel="25V\+">(.*?)</dc_output>').fillna(0)
    act_df['DC25+_volt'] = act_df['DC25+'].str.extract(r' value="(.*?)/> <dc_current').fillna(0)
    act_df['DC25+_cur'] = act_df['DC25+'].str.extract(r'<dc_current value=(.*?)/> <dc_voltage_actual').fillna(0)
    act_df['DC25+_volt'] = act_df['DC25+_volt'].replace('"', '', regex=True)
    act_df['DC25+_cur'] = act_df['DC25+_cur'].replace('"', '', regex=True)

    act_df['DC25-'] = act_df['DC'].str.extract(r'<dc_output channel="25V\-">(.*?)</dc_output>').fillna(0)
    act_df['DC25-_volt'] = act_df['DC25-'].str.extract(r' value="(.*?)/> <dc_current').fillna(0)
    act_df['DC25-_cur'] = act_df['DC25-'].str.extract(r'<dc_current value=(.*?)/> <dc_voltage_actual').fillna(0)
    act_df['DC25-_volt'] = act_df['DC25-_volt'].replace('"', '', regex=True)
    act_df['DC25-_cur'] = act_df['DC25-_cur'].replace('"', '', regex=True)

    act_df = act_df.drop(['DC'], axis=1)
    act_df = act_df.drop(['DC6+'], axis=1)
    act_df = act_df.drop(['DC25+'], axis=1)
    act_df = act_df.drop(['DC25-'], axis=1)

    #-----MULTIMETRO-----
    act_df['DMM_conf'] = df2['user_request'].str.extract(r'(?s:.+<dmm_function value=")([a-zA-Z0-9=!><#$&()\\-`.+,/\" ]+)(?:."></dmm_function)').fillna(0)
    act_df['DMM_conf'] = act_df['DMM_conf'].replace('curren', 'current', regex=True)
    act_df['DMM_conf']

    act_df['DMM_value'] = df2['system_response'].str.extract(r'(?s:.+<dmm_result value)([a-zA-Z0-9=!><#$&()\\-`.+,/\" ]+)(?:.</multimeter>)').fillna(0)
    #limpeza string valor multimetro
    act_df['DMM_value'] = act_df['DMM_value'].replace('"', '', regex=True)
    act_df['DMM_value'] = act_df['DMM_value'].replace('nan', np.nan, regex=True)
    act_df['DMM_value'] = act_df['DMM_value'].fillna(0)
    act_df['DMM_value'] = act_df['DMM_value'].replace('=', '', regex=True)
    act_df['DMM_value'] = act_df['DMM_value'].replace('/', '', regex=True)
    act_df['DMM_value'] = act_df['DMM_value'].replace('>', '', regex=True)
    act_df['DMM_value'] = act_df['DMM_value'].replace('#QNAN', '00000', regex=True)
    #act_df['DMM_value'] = act_df['DMM_value'].replace('1.#QNAN0e+000', '01', regex=True)

    return act_df

#-----FORMATAÇÃO VALOR 2 CASAS DECIMAIS-----
def value_form(act_df, column_name)-> pd.DataFrame:
    act_df[column_name] = act_df[column_name].apply(lambda x: "{:.2f}".format(float(x)) if x != '0.000000e+0' else 0.00)
    act_df[column_name] = act_df[column_name].astype(float)
    act_df = act_df.fillna(0)

    return act_df

#-----REMOÇÃO DUPLICADOS-----
def remove_duplicates(act_df)-> pd.DataFrame:
    act_df = act_df.drop_duplicates()
    act_df.reset_index(drop=True, inplace=True)

    act_df['breadboard'].replace('', np.nan, inplace=True)
    act_df = act_df.dropna(subset=['breadboard'])
    act_df.reset_index(drop=True, inplace=True)
    return act_df

#act_df.head(5)

def norm_data(act_df) -> pd.DataFrame:
    df3 = act_df[['sessionkey', 'time_request','breadboard']]
    return df3