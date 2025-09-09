from mlxtend.frequent_patterns import apriori, association_rules

def association_data_prep(UserAtivFinal):
    act_ap = UserAtivFinal[:]
    act_ap = act_ap.drop(columns=['sessionkey', 'time_request', 'execution_count', 'DC6+_volt',
        'DC6+_cur', 'DC25+_volt', 'DC25+_cur', 'DC25-_volt', 'DC25-_cur', 'score', 'time_difference'])


    # List of columns to convert to boolean type
    columns_to_convert = ['R12K', 'R470K', 'R10K', 'DC+6V', 'DMM_v', 'DMM_mA', 'GND',
        'value_p11_470', 'value_p11_12', 'value_p11_10', 'value_p12',
        'value_p13_470', 'value_p13_12', 'value_p13_10', 'DC6+_volt_p1',
        'error_id', 'error_esp', 'circuit_0 resistor', 'circuit_1 resistor',
        'circuit_series', 'DMM_conf_0', 'DMM_conf_ac current',
        'DMM_conf_ac volt', 'DMM_conf_dc current', 'DMM_conf_dc volt',
        'DMM_conf_resistanc']

    # Convert each column to boolean type
    for col in columns_to_convert:
        act_ap[col] = act_ap[col].astype(bool)
    
    return act_ap

# Define a function to generate rules for a specific ID
def generate_rules_for_id(id_value, act_ap):
    subset = act_ap[act_ap['exp_id'] == id_value]
    frequent_itemsets = apriori(subset[['R12K', 'R470K', 'R10K', 'DC+6V', 'DMM_v', 'DMM_mA', 'GND',
    'value_p11_470', 'value_p11_12', 'value_p11_10', 'value_p12',
    'value_p13_470', 'value_p13_12', 'value_p13_10', 'DC6+_volt_p1',
    'error_id', 'error_esp', 'circuit_0 resistor', 'circuit_1 resistor',
    'circuit_series', 'DMM_conf_0', 'DMM_conf_ac current',
    'DMM_conf_ac volt', 'DMM_conf_dc current', 'DMM_conf_dc volt',
    'DMM_conf_resistanc']], min_support=0.5, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)

    return rules
