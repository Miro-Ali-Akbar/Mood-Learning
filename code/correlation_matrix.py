import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("data/data.csv")
corr_m = df.corr()
cmap = sns.diverging_palette(230, 0, as_cmap=True)
# Draw the heatmap with the mask and correct aspect ratio
fig, ax = plt.subplots(figsize=(15,10))  
sns.heatmap(corr_m, cmap=cmap, center=0, annot=True,annot_kws= {"size":10},
            square=True, linewidths=.5, fmt=".2f", cbar_kws={"shrink": .5}, ax=ax)
fig.savefig("finished/Corrfull.png", dpi=350, bbox_inches='tight')
