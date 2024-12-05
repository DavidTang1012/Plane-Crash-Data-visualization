import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load the data
file_path = 'data.csv'  # Replace with your file path
data = pd.read_csv(file_path)

# Ensure proper datetime format and extract month and decade
data['Year'] = pd.to_datetime(data['Date'], errors='coerce').dt.year
data['Month'] = pd.to_datetime(data['Date'], errors='coerce').dt.month
data['Decade'] = (data['Year'] // 10) * 10

# Group data by month and decade, calculate total crashes
monthly_decade_stats = data.groupby(['Month', 'Decade']).agg(
    Total_Crashes=('Date', 'count')
).reset_index()

# Plot the data
plt.figure(figsize=(14, 8))
sns.lineplot(data=monthly_decade_stats, x='Month', y='Total_Crashes', hue='Decade', marker='o', palette='tab10')

# Add titles and labels
plt.title('Monthly Trends in Crashes by Decade', fontsize=18)
plt.xlabel('Month', fontsize=14)
plt.ylabel('Total Crashes', fontsize=14)
plt.xticks(ticks=range(1, 13), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], fontsize=12)
plt.yticks(fontsize=12)
plt.legend(title='Decade', fontsize=12, title_fontsize=14, bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(alpha=0.3)
plt.tight_layout()

# Save the plot (optional)
plt.savefig('monthly_trends_by_decade.png')

# Display the plot
plt.show()

# Combine all crash summaries into one text
summary_text = ' '.join(data['Summary'].dropna())

# Generate the word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(summary_text)

# Plot the word cloud
plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Crash Summaries', fontsize=18)
plt.tight_layout()

# Save and display
plt.savefig('wordcloud_crash_summaries.png')
plt.show()

plt.figure(figsize=(12, 6))
data['Fatalities'].dropna().plot(kind='hist', bins=30, alpha=0.7, color='skyblue', edgecolor='black')
plt.title('Distribution of Fatalities Per Crash', fontsize=18)
plt.xlabel('Fatalities', fontsize=14)
plt.ylabel('Frequency', fontsize=14)
plt.grid(alpha=0.3)

# Save and display
plt.tight_layout()
plt.savefig('fatalities_distribution_per_crash.png')
plt.show()

# Count the most frequent airplane types
type_counts = data['Type'].value_counts().head(10)

# Plot the pie chart for the top 10 types
plt.figure(figsize=(8, 8))
type_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140, cmap='tab10', legend=False)
plt.title('Top 10 Airplane Types in Crashes', fontsize=18)
plt.ylabel('')  # Remove default y-axis label for clarity

# Save and display
plt.tight_layout()
plt.savefig('top_10_airplane_types.png')
plt.show()

# Calculate the correlation matrix for numerical features
numerical_data = data[['Aboard', 'Fatalities', 'Ground']].dropna()
correlation_matrix = numerical_data.corr()

# Plot the heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', cbar_kws={'label': 'Correlation'})
plt.title('Correlation Matrix of Numerical Features', fontsize=18)

# Save and display
plt.tight_layout()
plt.savefig('correlation_matrix.png')
plt.show()

# Group data by decade and operator
decade_operator_stats = (
    data.groupby(['Decade', 'Operator']).size()
    .reset_index(name='Crashes')
    .sort_values(['Decade', 'Crashes'], ascending=[True, False])
    .groupby('Decade')
    .head(5)  # Select top 5 operators for each decade
)

# Plot the top operators by crashes per decade
plt.figure(figsize=(14, 10))
sns.barplot(data=decade_operator_stats, x='Crashes', y='Operator', hue='Decade', dodge=True, palette='tab10')
plt.title('Top Operators by Crashes per Decade', fontsize=18)
plt.xlabel('Crashes', fontsize=14)
plt.ylabel('Operator', fontsize=14)
plt.legend(title='Decade', fontsize=12, title_fontsize=14, bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(alpha=0.3)

# Save and display
plt.tight_layout()
plt.savefig('top_operators_by_decade.png')
plt.show()