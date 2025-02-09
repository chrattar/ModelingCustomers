import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error


#Selcect which columns you want
numeric_columns = ["Project-Size (sf)", "Price per Sq Ft", "Total Value ($)", "Sales Volume ($)"]

#minmax scaling
scaler = MinMaxScaler()
df_normalized = df.copy()
df_normalized[numeric_columns] = scaler.fit_transform(df[numeric_columns])

#plotting
plt.figure(figsize=(10,6))
for column in numeric_columns:
    plt.hist(df_normalized[column], bins=50, alpha =0.5, label = column)

#PLOT - Normal Distribution
plt.legend()
plt.title("Norm Dist of Prject Variables")
plt.xlabel("Normalized value 0-1")
plt.ylabel("Freq.")
plt.grid()
plt.show()

#PLOT - PROJECT SIZE VS VALUE
plt.figure(figsize=(8, 6))
plt.scatter(df_normalized["Project-Size (sf)"], df_normalized["Total Value ($)"], alpha=0.5)
plt.xlabel("Normalized Project Size")
plt.ylabel("Normalized Total Value")
plt.title("Project Size vs. Total Value (Normalized)")
plt.grid()
plt.show()

#--------------------------------------------------------
# Convert 'Classification' to numeric and put in dataframe
df_normalized["Classification"] = df_normalized["Classification"].astype("category").cat.codes

# ONly want numeric columns
numeric_df = df_normalized.select_dtypes(include=["number"])

correlation_matrix = numeric_df.corr()

#HEATMAP
plt.figure(figsize=(8,6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Correlation Matrix of Normalized Variables")
plt.show()


#----------------------------------------------------------

#Cluster Features
features = df_normalized[["Project-Size (sf)", "Total Value ($)", "Sales Volume ($)"]]

# Apply K-Means clustering (choose 3 clusters for A/B/C customers)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df_normalized["Cluster"] = kmeans.fit_predict(features)

# Scatter plot of clusters
plt.figure(figsize=(8, 6))
plt.scatter(df_normalized["Project-Size (sf)"], df_normalized["Total Value ($)"], c=df_normalized["Cluster"], cmap="viridis", alpha=0.5)
plt.xlabel("Normalized Project Size")
plt.ylabel("Normalized Total Value")
plt.title("Customer Clusters based on Spending & Project Size")
plt.colorbar(label="Cluster")
plt.show()


#------------------------------------------------------------------
#PLOT ACTUAL VS PREDICTED PRICE
# Select features & target variable
X = df_normalized[["Project-Size (sf)", "Sales Volume ($)"]]
y = df_normalized["Price per Sq Ft"]

# Split data into train & test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluate model
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error: {mae:.4f}")

plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.5)
plt.xlabel("Actual Price per Sq Ft")
plt.ylabel("Predicted Price per Sq Ft")
plt.title("Actual vs Predicted Price per Sq Ft")
plt.show()

