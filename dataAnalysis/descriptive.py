import matplotlib.pyplot as plt
import seaborn as sns
import dataAnalysis.clustering as clus

act_k = clus.act_dm[:] 

# Descriptive analysis
print('\nDescriptive Analysis: ', act_k.describe().round(2))

# Information about the variables
print('\nVariable´s Information: ', act_k.info())

# Visualization
# Histograms for each attribute
act_k.hist(figsize=(20, 20))
plt.show()

# Box and whisker plots for each attribute
act_k.plot(kind='box', subplots=True, layout=(11,4), sharex=False, sharey=False, figsize=(20,20))
plt.show()