import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('final_dataset.csv', delimiter=';')

# Calculate Pearson's correlation coefficient for all features
corr_matrix = df.corr(method='pearson')

# Plot a heatmap of the correlation matrix
sns.set_theme(style="white")
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix of Features')
plt.show()

# Print the correlation coefficients for nat_demand in descending order
print(corr_matrix['nat_demand'].sort_values(ascending=False))

# Plot the feature importances
importances = rf.feature_importances_
std = np.std([tree.feature_importances_ for tree in rf.estimators_], axis=0)
indices = np.argsort(importances)[::-1]

plt.figure()
plt.title("Feature importances")
plt.bar(range(X.shape[1]), importances[indices],
        color="r", yerr=std[indices], align="center")
plt.xticks(range(X.shape[1]), X.columns[indices], rotation='vertical')
plt.xlim([-1, X.shape[1]])
plt.show()
