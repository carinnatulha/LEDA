import hvplot.pandas 
import panel as pn
import pandas as pd
import holoviews as hv
from mlxtend.frequent_patterns import apriori, association_rules


#histograma execuções por sessão
def exec_line_plot(idf, select_stud, select_exp_id):
    return idf[(idf['sessionkey']==select_stud) & (idf['exp_id'] ==   select_exp_id)].hvplot.bar(
                                             x='sessionkey',
                                             y='execution_count')

#histograma notas por sessão
def attmp_line_plot(idf, select_stud, select_exp_id):
    return idf[(idf['sessionkey']==select_stud) & (idf['exp_id'] ==   select_exp_id)].hvplot.line(
                                             x='sessionkey',
                                             y='score')

#grafico em barra frequencia de circuitos
def freq_source_bar_plot(freq, select_exp_id):
    return freq[freq['exp_id']==  select_exp_id].hvplot.bar(
                                   x='Circuit',
                                   y='Frequency', height=300, width=1200)

#tabela de classificação de erros
def create_error_table(class_error, select_stud, select_exp_id):
    
    error_table = pn.panel(pd.DataFrame(columns=class_error.columns))

    def update_table(event):
        if select_stud.value == 'Select' or select_exp_id.value == 'Select':
            empty_df = pd.DataFrame(columns=class_error.columns)
            error_table.object = empty_df
        else:
            filtered_df = class_error[(class_error['Session'] == select_stud.value) & 
                                      (class_error['Experiment'] == select_exp_id.value)]
            error_table.object = filtered_df

    error_table = pn.panel(pd.DataFrame(columns=class_error.columns))
    select_stud.param.watch(update_table, 'value')
    select_exp_id.param.watch(update_table, 'value')

    # Frequência dos tipos de erro
    error_freq = class_error.drop(columns=['Session'])
    
    @pn.depends(select_exp_id.param.value)
    def generate_bar_plot(selected_problem):
        filtered = error_freq[error_freq['Experiment'] == selected_problem]
        numeric_cols = filtered.select_dtypes(include='number').columns
        freq = filtered[numeric_cols].sum()
        return freq.hvplot.bar(xlabel='Columns', ylabel='Frequency', height=300, width=1200)

    return error_table, generate_bar_plot

# Define the heatmap function
def create_heatmap_panel(AtivFinal, selected_exp_id, select_exp_id):

    def heatmap_plot(exp_id):
        selected_data = AtivFinal[AtivFinal['exp_id'] == selected_exp_id]
        plot = selected_data.set_index('sessionkey').iloc[:, 1:-1].transpose().hvplot.heatmap(
            cmap='Blues', height=300, width=1200, colorbar=False
        ).opts(shared_axes=False)
        return plot
    
    heatmap_panel = pn.panel(heatmap_plot(selected_exp_id.value))

    def update_heatmap(event):
        selected_exp_id = select_exp_id.value
        heatmap_panel.object = heatmap_plot(selected_exp_id.value)

    select_exp_id.param.watch(update_heatmap, 'value')
    return heatmap_panel


#matriz de correlação
def create_correlation(act_dm, select_exp_id):
    corr_df = act_dm[:]

    # Function to generate the correlation matrix heatmap based on selected exp_id
    @pn.depends(select_exp_id.param.value)
    def correlation_heatmap(selected_exp_id):
        # Filter data based on the selected exp_id
        if selected_exp_id == 'Select':
            selected_data = corr_df
        else:
            selected_data = corr_df[corr_df['exp_id'] == selected_exp_id]

        # Calculate correlation matrix
        correlation_matrix = selected_data.corr()

        # Create heatmap using hvplot
        return correlation_matrix.hvplot.heatmap(cmap='Blues', width=1200, height=800)

    return correlation_heatmap

def create_indicators(manip, select_exp_id):
    session_indicator = pn.indicators.Number(name='Session', value=manip.loc[0, 'Session'])
    circ_indicator = pn.indicators.Number(name='circ_uniq', value=manip.loc[0, 'circ_uniq'])

    def update_session(event):
        row = manip[manip['exp_id'] == select_exp_id.value].iloc[0]
        session_indicator.value = row['Session']
    select_exp_id.param.watch(update_session, 'value')

    def update_circ(event):
        row = manip[manip['exp_id'] == select_exp_id.value].iloc[0]
        circ_indicator.value = row['circ_uniq']
    select_exp_id.param.watch(update_circ, 'value')

    return session_indicator, circ_indicator

#Clustering
# Function to generate the bar plot based on selected exp_id
def create_clustering_panel(cluster_sizes_k, result_df, select_exp_id):

    @pn.depends(select_exp_id.param.value)
    def cluster_bar(selected_exp_id):
        # Filter data based on the selected exp_id
        if selected_exp_id == 'All':
            selected_data = cluster_sizes_k
        else:
            selected_data = cluster_sizes_k[cluster_sizes_k['exp_id'] == selected_exp_id]

        # Create bar plot using hvplot
        return  selected_data.hvplot.bar(
            x='cluster_k', y='cluster_sizes_k', stacked=True, 
            title=f'K-means Cluster Sizes per exp_id - Selected: {selected_exp_id}',
            xlabel='Cluster', ylabel='Cluster Size', width = 600, max_width = 800, height=500
        )

    cluster_result = result_df[:]
    result = cluster_result.groupby(['exp_id', 'cluster_k']).sum()
    
    select_var = pn.widgets.Select(options=['Select'] + cluster_result.columns[1:-1].tolist(),
                                   name='Variable')

    @pn.depends(select_exp_id.param.value, select_var.param.value)
    def grouped_bar(exp_id, variable):
        if exp_id == 'Select':
            return hv.Div('')
        return result.loc[exp_id, variable].hvplot.bar(by='cluster_k', stacked=False, width=800, height=400)

    return cluster_bar, select_var, grouped_bar

def create_rules_panel(act_ap):
    id_selector = pn.widgets.Select(name='Select ID', options=list(act_ap['exp_id'].unique()))
    
    def generate_rules(id_value):
        subset = act_ap[act_ap['exp_id'] == id_value]
        frequent_itemsets = apriori(subset, min_support=0.5, use_colnames=True)
        rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)
        return rules.head(10)

    @pn.depends(id_selector.param.value)
    def display_rules(id_value):
        return generate_rules(id_value)

    return pn.Column(id_selector, display_rules)