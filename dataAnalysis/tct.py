import pandas as pd

#------------------------TEORIA CLASSICA DOS TESTES--------------
def tct_analysis(UserAtivFinal):
    error_ana = pd.DataFrame(columns=['Identification'])
    error_ana['Identification'] = UserAtivFinal.groupby('exp_id')['score'].value_counts()
    print(error_ana)

    # Calcular a média do score para cada exp_id
    tct_df = UserAtivFinal.groupby('exp_id')['score'].mean().reset_index()
    tct_df.rename(columns={'score': 'average_score'}, inplace=True)

    #verificação da média para classificação
    tct_df.loc[(tct_df['average_score'] <= 0.1, 'item_rating')] = 'very hard'
    tct_df.loc[(tct_df['average_score'] > 0.1, 'item_rating')] = 'hard'
    tct_df.loc[(tct_df['average_score'] > 0.3, 'item_rating')] = 'medium'
    tct_df.loc[(tct_df['average_score'] > 0.7, 'item_rating')] = 'easy'
    tct_df.loc[(tct_df['average_score'] >= 0.9, 'item_rating')] = 'very easy'
    tct_df = tct_df.round({'average_score': 2})

    return tct_df