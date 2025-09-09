import panel as pn
from panel.template import FastListTemplate


# Define pages as classes
class Page1:
    def __init__(self, exec_line_plot, score_line_plot, error_table, session_indicator, activity_description):
        self.content = pn.Column(
        #pn.Row('##Informações Gerais da Atividade', margin=(0, 500), sizing_mode="stretch_width"),
        pn.Row(
            pn.Column('# Activity Description', pn.layout.Divider(), activity_description, styles=dict(background='whitesmoke'), sizing_mode="stretch_width"),
            pn.Column(session_indicator),
        ),
        pn.Row(
            pn.Column('## Execution per Session', pn.widgets.TooltipIcon(value="This chart represents the "),exec_line_plot.panel(width_policy='min'), sizing_mode="stretch_width"),
            pn.Column('## Score by attemps', pn.widgets.TooltipIcon(value="This chart represents the "), attmp_line_plot.panel(width_policy='max'), sizing_mode="stretch_width")
        ),
        pn.Row(
            pn.Column('## Error Classification', pn.widgets.TooltipIcon(value="This table represents the "), error_table, sizing_mode="stretch_width")
        ),
    )

    def view(self):
        return self.content

    
class Page2:
    def __init__(self, freq_source_bar_plot, circ_uniq_indicator, update_bar_plot, heatmap_plot):
        self.content = pn.Column(
            pn.Row(
                pn.Column('## Most Frequent Circuit', pn.widgets.TooltipIcon(value="This table represents the "), sizing_mode="stretch_width"),
                pn.Column(circ_uniq_indicator),
            ),
            pn.Row(
                freq_source_bar_plot.panel(width_policy='max'), sizing_mode="stretch_width",
            ),
            pn.Row(
               "## Erros's frequency according to each error classification ", pn.widgets.TooltipIcon(value="This table represents the ")
            ),
            pn.Row(
               update_bar_plot, sizing_mode="stretch_width",
            ),
            pn.Row(
                "## Componets used per student ", pn.widgets.TooltipIcon(value="This table represents the ")
            ),
            pn.Row(
                heatmap_plot, sizing_mode="stretch_width"
            ),

            
    )

    def view(self):
        return self.content
    
    
class Page3:
    def __init__(self, kc_description, number, plot_cluster_sizes_k, select_var, correlation_heatmap, display_rules):
        self.content = pn.Column(
        pn.Row(
            pn.Column('# Competencies Description', pn.layout.Divider(), kc_description, styles=dict(background='whitesmoke'), sizing_mode="stretch_width"),
            pn.Column(number),
        ),
        #pn.Row(
        #        "## Learn Probability ", pn.widgets.TooltipIcon(value="This table represents the ")
        #),
       # pn.Row(
        #    pn.Column(bkt_source, bkt_source_bar_plot.panel(width_policy='max')),
        #),
        pn.Row(
            "## K-meas ", pn.widgets.TooltipIcon(value="This table represents the ")
        ),
        pn.Row(
            #pn.Column(number.clone(value=grau_df['Difficulty_Score'][0]), sizing_mode="stretch_width"),
            pn.Column(plot_cluster_sizes_k),
        ),
        pn.Row(
            "## Clustering per component ", pn.widgets.TooltipIcon(value="This table represents the ")
        ),
        pn.Row(
                select_var,
                #update_plot
        ),
        pn.Row(
            "## Correlation ", pn.widgets.TooltipIcon(value="This table represents the ")
        ),
        pn.Row(
            correlation_heatmap, sizing_mode="stretch_width"
        ),
        pn.Row(
            "## Association Rules ", pn.widgets.TooltipIcon(value="This table represents the ")
        ),
        pn.Row(
            display_rules
        )

    )

    def view(self):
        return self.content