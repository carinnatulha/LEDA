import os
import matplotlib.pyplot as plt
import seaborn as sns
import dataAnalysis.clustering as clus
import panel as pn
import shutil

#--Elbow
plt.figure(figsize=(16,8))
plt.plot(clus.K, clus.inertia, 'bx-')
plt.xlabel('k')
plt.ylabel('Inertia')
plt.title('The Elbow Method showing the optimal k')
plt.show()

#---Cluster sizes for each 'exp_id'
for exp_id in clus.cluster_sizes_k['exp_id'].unique():
    exp_data = clus.cluster_sizes_k[clus.cluster_sizes_k['exp_id'] == exp_id]
    plt.figure(figsize=(8, 6))
    plt.bar(exp_data['cluster_k'], exp_data['cluster_sizes_k'])
    plt.title(f'Cluster Sizes for exp_id {exp_id}')
    plt.xlabel('Cluster')
    plt.ylabel('Size')
    plt.xticks(exp_data['cluster_k'])
    plt.show()
    
    output_file = os.path.join(clus.output_dir, f"kmeans{exp_id}.png")
    plt.savefig(output_file)

# Create a directory to store the plots
output_dir = "cluster_size_plots"
os.makedirs(output_dir, exist_ok=True)

#---Cluster sizes for each 'exp_id' and save them as image files
for exp_id in clus.cluster_sizes_k['exp_id'].unique():
    exp_data = clus.cluster_sizes_k[clus.cluster_sizes_k['exp_id'] == exp_id]
    plt.figure(figsize=(8, 6))
    plt.bar(exp_data['cluster_k'], exp_data['cluster_sizes_k'])
    plt.title(f'Cluster Sizes for exp_id {exp_id}')
    plt.xlabel('Cluster')
    plt.ylabel('Size')
    plt.xticks(exp_data['cluster_k'])
    
    # Save the plot to a file
    output_file = os.path.join(output_dir, f"cluster_size_plot_exp_{exp_id}.png")
    plt.savefig(output_file)
    plt.close()

# Generate download links for the saved plots
download_links = []
for exp_id in clus.cluster_sizes_k['exp_id'].unique():
    output_file = f"cluster_size_plot_exp_{exp_id}.png"
    download_links.append((f"Download Cluster Size Plot for exp_id {exp_id}", output_file))

# Display the download links
for link_text, file_name in download_links:
    display_link = pn.widgets.FileDownload(filename=file_name, label=link_text)
    display_link.servable()

# Set the style of seaborn for better aesthetics
sns.set(style="whitegrid")

# Loop through each variable and create a count plot for each variable per exp_id
for variable in clus.result_df.drop(['exp_id', 'cluster_k'], axis=1).columns:
    plt.figure(figsize=(10, 5))
    
    # Plot K-Means clusters
    sns.countplot(x='cluster_k', hue=variable, data=clus.result_df, palette='viridis', dodge=True)
    plt.title(f'Count of {variable} in K-Means Clusters')
    plt.xlabel('Cluster')
    plt.ylabel('Count')
    plt.legend(title=variable, loc='upper right')

    plt.tight_layout()
    plt.show()

    #------------PARA SALVAR OS GRAFICOS AUTOMATICO--------
# Set the style of seaborn for better aesthetics
sns.set(style="whitegrid")

# Create a directory to save plots if it doesn't exist
output_dir = 'plots'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Loop through each variable and create a bar plot for each cluster
for i, variable in enumerate(clus.result_df):
    plt.figure(figsize=(10, 5))
    
    # Plot K-Means clusters
    plt.subplot(1, 2, 1)
    sns.countplot(x='cluster_k', hue=variable, data=clus.result_df, palette='viridis')
    plt.title(f'Count of {variable} in K-Means Clusters')

    plt.tight_layout()
    
    # Save the plot
    filename = os.path.join(output_dir, f'plot_{i}.png')
    plt.savefig(filename)
    plt.close()  # Close the figure to release memory

# After generating all plots, you can compress them into a zip file for easier downloading

shutil.make_archive(output_dir, 'zip', output_dir)

# Set the style of seaborn for better aesthetics
sns.set(style="whitegrid")

# Loop through each exp_id and each variable, and create a count plot for each
for exp_id in clus.result_df['exp_id'].unique():
    exp_data = clus.result_df[clus.result_df['exp_id'] == exp_id]
    
    for variable in clus.result_df.drop(['exp_id', 'cluster_k'], axis=1).columns:
        plt.figure(figsize=(10, 5))

        # Plot K-Means clusters
        sns.countplot(x='cluster_k', hue=variable, data=exp_data, palette='viridis', dodge=True)
        plt.title(f'Count of {variable} in K-Means Clusters for exp_id {exp_id}')
        plt.xlabel('Cluster')
        plt.ylabel('Count')
        plt.legend(title=variable, loc='upper right')

        plt.tight_layout()
        plt.show()
        
#------------DOWNLOAD--------------

# Set the style of seaborn for better aesthetics
sns.set(style="whitegrid")

# Create a directory to store the plots
output_dir = "kmeans_plots"
os.makedirs(output_dir, exist_ok=True)

# Loop through each exp_id and each variable, and create a count plot for each
for exp_id in clus.result_df['exp_id'].unique():
    exp_data = clus.result_df[result_df['exp_id'] == exp_id]
    
    for variable in clus.result_df.drop(['exp_id', 'cluster_k'], axis=1).columns:
        plt.figure(figsize=(10, 5))

        # Plot K-Means clusters
        sns.countplot(x='cluster_k', hue=variable, data=exp_data, palette='viridis', dodge=True)
        plt.title(f'Count of {variable} in K-Means Clusters for exp_id {exp_id}')
        plt.xlabel('Cluster')
        plt.ylabel('Count')
        plt.legend(title=variable, loc='upper right')

        # Save the plot to a file
        output_file = os.path.join(output_dir, f"kmeans_plot_exp_{exp_id}_variable_{variable}.png")
        plt.savefig(output_file)
        plt.close()