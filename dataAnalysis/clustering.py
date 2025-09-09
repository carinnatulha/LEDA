import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.preprocessing import StandardScaler
import dataAnalysis.exploratory as exp

def elbow_method(UserAtivFinal):
    act_dm = UserAtivFinal[:]
    act_dm = act_dm.drop(columns=['sessionkey', 'time_request', 'execution_count', 'score',
                                'sessionkey', 'time_request', 'DC6+_volt', 'DC6+_cur', 
                                'DC25+_volt', 'DC25+_cur', 'DC25-_volt', 'DC25-_cur', 'time_difference',
                                'error_id', 'error_esp'
                                ])

    # Load your data
    elbow_df = act_dm[:]

    # Only discriminatory variables (with more than one value)
    elbow_df = elbow_df.drop(columns=['exp_id'])


    # Perform K-means clustering with different numbers of clusters
    inertia = []
    K = range(1,10)
    for k in K:
        kmeanModel = KMeans(n_clusters=k, n_init=10)
        kmeanModel.fit(elbow_df)
        inertia.append(kmeanModel.inertia_)

    return inertia

def kmeans_clustering(act_dm):
    # Initialize an empty DataFrame to store the results
    result_df = pd.DataFrame()

    act_k = act_dm[:]

    # Loop through unique 'exp_id' values
    for exp_id in act_k['exp_id'].unique():
        # Filter the DataFrame for the current 'exp_id'
        subset_df = act_k[act_k['exp_id'] == exp_id].copy()

        # Extract binary features for clustering
        binary_features = subset_df.drop(['exp_id'], axis=1)

        # Check if the number of samples is greater than or equal to the desired number of clusters
        if len(binary_features) >= 4:
            # Standardize the features
            scaler = StandardScaler()
            binary_features_scaled = pd.DataFrame(scaler.fit_transform(binary_features), columns=binary_features.columns)

            # Perform K-means clustering with n_clusters=4
            n_clusters = 3
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            subset_df['cluster_k'] = kmeans.fit_predict(binary_features_scaled)
                
            # Append the results to the main DataFrame
            result_df = pd.concat([result_df, subset_df], ignore_index=True)
            
        else:
            print(f"Skipping exp_id {exp_id} due to insufficient samples for clustering.")
            

    # Check the size of each cluster per exp_id
    cluster_sizes_k = result_df.groupby(['exp_id', 'cluster_k']).size().reset_index(name='cluster_sizes_k')

    # Set the style of seaborn for better aesthetics
    sns.set(style="whitegrid")

    # Create a directory to store the plots
    output_dir = "kmeans_exp"
    os.makedirs(output_dir, exist_ok=True)

    # Group the data by 'exp_id' and 'cluster_k', and calculate the size of each cluster
    cluster_sizes_k = result_df.groupby(['exp_id', 'cluster_k']).size().reset_index(name='cluster_sizes_k')

    return result_df, cluster_sizes_k



