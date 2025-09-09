from tempfile import template
import dataPreprocessing.preprocessing as pp
import dataPreprocessing.simplification as simp
import dataPreprocessing.normalization as norm
import dataTransformation.component as comp
import dataTransformation.errorClass as errorClass
import dataTransformation.espErrorClass as espErrorClass
import dataAnalysis.exploratory as expl

import dataVisualization.dataprep as dprep
import dataVisualization.widgets as widg
import dataVisualization.plots as plots
import dataVisualization.descriptions as desc
import dataVisualization.template as temp
import dataVisualization.pages as pages

import panel as pn
import pandas as pd

def main():

    df1 = pd.read_csv('dados.csv')
    df1 = df1.rename(columns={"Timestamp_before.1": "time_request", "Timestamp_after.1": "time_response", "Request": "user_request", "Response": "system_response"})
    df1 = df1.drop(['Timestamp_before', 'Timestamp_after', 'Link'], axis=1)

    #time_request: hora de execução pelo usuário
    #time_respose: hora de resposta do sistema
    #user_request: informações que o usuário envia para o VISIR (características da experimentação)
    #system_response: resposta do sistema à confifuração gerada pelo usuário

    # 2. Pré-processamento
    act_df, df2 = pp.create_tables(df1)
    act_df = pp.process_breadboard_column(act_df, column='breadboard')
    act_df = pp.cleaning(act_df, df2)
    act_df = pp.value_form(act_df, 'DMM_value')
    act_df = pp.value_form(act_df, 'DC6+_cur')
    act_df = pp.value_form(act_df, 'DC6+_volt')
    act_df = pp.value_form(act_df, 'DC25+_cur')
    act_df = pp.value_form(act_df, 'DC25+_volt')
    act_df = pp.value_form(act_df, 'DC25-_cur')
    act_df = pp.value_form(act_df, 'DC25-_volt')
    act_df = pp.remove_duplicates(act_df)            
    df3 = pp.norm_data(act_df)
    
    # 3. Normalization
    df3['breadboard'] = norm.prep_normalization(df3)
    act_df = act_df.drop(['breadboard'], axis=1)
    ordered_data = [[comp.split() for comp in circ.split(", ")] for circ in df3['breadboard_simp']]
    df3['breadboard_norm'] = norm.normalizar_circuito(ordered_data)
    df3['breadboard_norm'] = [', '.join(map(str, l)) for l in pp.df3['breadboard_norm']]

    # 4. Simplification
    df3['breadboard_simp'] = df3['breadboard_norm'].apply(lambda x: simp.simplificar_circuito(x))

    # 5. Components

    act_df = comp.component_features(act_df, df3)

    act_df['circuit'] = df3['breadboard'].apply(comp.circuite_type)

    act_df = comp.tolerance(act_df)

    # 6. Error Classification
    class_error = pd.DataFrame()
    class_error = errorClass.class_erro_comp(act_df, class_error)
    act_df = espErrorClass.class_erro_esp(act_df)
    act_df = errorClass.class_erro_geral(act_df)

    # 7. Exploratory Data Analysis
    act_df, total_exp, total_error, total_error_g, total_error_esp, total_error_esp_g = expl.error_analysis(act_df, class_error)
    act_df, class_errorFinal, calss_errorF_g = expl.score_calculation(act_df, class_error)  
    act_df = expl.score_calculation(act_df, class_error)
    act_df = expl.exec_count(act_df)
    manip = expl.manip_analysis(act_df, df1, df3)
    UserAtivFinal = expl.time_analysis(act_df)
    mean_executions_per_exp = expl.mean_time_per_experiment(UserAtivFinal)
    mean_time_per_exp = expl.mean_time_per_experiment(UserAtivFinal)
    UserAtivFinal, mean_executions_per_exp, mean_time_per_exp = expl.last_activity(UserAtivFinal)
    seq_rep, grupos = expl.sequence_analysis(df3)
    padroes_de_repeticao_por_usuario = expl.repetition_patterns(act_df)
    freq_df = expl.frequent_circuits_analysis(df3)    

    # 8. TCT
    tct_df = expl.tct_analysis(UserAtivFinal)

    # 9. Clustering
    inertia = expl.elbow_method(UserAtivFinal)
    result_df, cluster_sizes_k = expl.kmeans_clustering(act_df)

    # 10. Visualization
    # ---- widgets ----
    select_stud, select_exp_id = widg.create_widgets(data_dict["idf"].data)

    # ---- plots/tables ----
    exec_plot = plots.create_exec_line_plot(data_dict["idf"], select_stud, select_exp_id)
    score_plot = plots.create_score_line_plot(data_dict["idf"], select_stud, select_exp_id)
    error_table = plots.create_error_table(class_error, select_stud, select_exp_id)

    # ---- Montar páginas ----
    page1 = pages.Page1(exec_plot, score_plot, error_table, session_indicator="?", activity_description="?")
    page2 = pages.Page2(freq_plot="?", circ_uniq_indicator="?", error_bar_plot="?", heatmap_plot="?")
    page3 = pages.Page3(kc_description="?", number="?", plot_cluster_sizes_k="?", select_var="?", correlation_heatmap="?", display_rules="?")

    # ---- Template final ----
    template = temp.build_template(page1, page2, page3, select_exp_id, select_stud)
    error_table, error_bar = plots.create_error_panel(class_error, select_stud, select_exp_id)
    heatmap_panel = plots.create_heatmap_panel(AtivFinal, select_exp_id)
    corr_panel = plots.create_correlation_panel(act_dm, select_exp_id)
    session_ind, circ_ind = plots.create_indicators(manip, select_exp_id)
    cluster_bar, select_var, grouped_bar = plots.create_clustering_panel(cluster_sizes_k, result_df, select_exp_id)
    rules_panel = plots.create_rules_panel(act_ap)

if __name__ == "__main__":
    main()
    pn.extension()
    template.show()







