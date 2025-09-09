import panel as pn

#-----DESCRIÇÃO DAS ATIVIDADES-----
def create_activity_description(select_exp_id):

    activity_description = pn.panel('No activity selected', name='Activity Description')

    def update_activity_description(event):
        
        selected_activity = event.new
        
        if selected_activity == 'exp 1.1':
            description = """
            Material: 1,2KΩ, 10KΩ or 470Ω resistors, multimeter e dc power.

            Objetive: measure the current trough one resistor and compare it with the expected results of Ohm's Law.
            """
        elif selected_activity == 'exp 1.2':
            description = """
            Material: 1,2KΩ, 10KΩ and 470Ω resistors, multimeter e dc power.

            Objetive: measure the current at the circuit and, using the Ohm's Law, and calculate the equivalent resistance of the circuit. """
        elif selected_activity == 'exp 1.3':
            description = """
            Material: 1,2KΩ, 10KΩ and 470Ω resistors, multimeter e dc power.

            Objetive:  measure the voltage at each resistor, to understand how the voltage is “distributed” between the resistors.

            """
        else:
            description = 'No activity selected'
        
        activity_description.object = description

#-----DESCRIÇÃO DAS COMPETENCIAS-----
def create_kc_description(select_exp_id):
    kc_description = pn.panel('No activity selected', name='Competence Description')

    def update_activity_description(event):
        selected_kc = event.new
    
        if selected_kc == 'exp 1.1':
            description = """
                •  Properly select and operate the components.
                • Connect components.
                • Build the circuit in a clear structure.
                • Connect the DC power +6V. 
                • Choose the right voltage. 
                • Connect the multimeter 
                • Place the  measurement leads to mA 
                • Place the value of the  measurement spinner in A
                • Measure the current
            """
        elif selected_kc == 'exp 1.2':
            description = """
                •  Properly select and operate the components.
                • Connect components.
                • Build the circuit in a clear structure.
                • Connect the DC power +6V. 
                • Choose the right voltage. 
                • Connect the multimeter 
                • Place the  measurement leads to mA 
                • Place the value of the  measurement spinner in A
                • Measure the current
            """
        elif selected_kc == 'exp 1.3':
            description = """
                •  Properly select and operate the components.
                • Connect components.
                • Build the circuit in a clear structure.
                • Connect the DC power +6V. 
                • Choose the right voltage. 
                • Connect the multimeter 
                • Place the  measurement leads to V 
                • Place the value of the  measurement spinner in V
                • Measure the voltage
            """
        else:
            description = 'No activity selected'
        
        kc_description.object = description