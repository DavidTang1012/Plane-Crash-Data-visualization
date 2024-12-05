import pandas as pd
import matplotlib.pyplot as plt

# Load the data
file_path = 'data.csv'  # Replace with your file path
data = pd.read_csv(file_path)

# Ensure proper datetime format and add decade
data['Year'] = pd.to_datetime(data['Date'], errors='coerce').dt.year
data['Decade'] = (data['Year'] // 10) * 10

# Replace missing or invalid numerical data with 0 for safety in plotting
data['Aboard'] = pd.to_numeric(data['Aboard'], errors='coerce').fillna(0)
data['Fatalities'] = pd.to_numeric(data['Fatalities'], errors='coerce').fillna(0)
data['Ground'] = pd.to_numeric(data['Ground'], errors='coerce').fillna(0)

# Create the scatter plot with improved layout
plt.figure(figsize=(14, 10))  # Increase figure size for better visibility

# Scatter plot with normalized and scaled sizes
scatter = plt.scatter(
    data['Aboard'],
    data['Fatalities'],
    c=data['Decade'],
    s=(data['Ground'] / data['Ground'].max()) * 300,  # Increased scaling for point size
    cmap='viridis',
    alpha=0.8,
    edgecolors='k',
    linewidth=0.5
)

# Title and axis labels
plt.title('Enhanced Fatalities vs. Aboard with Improved Readability', fontsize=18)
plt.xlabel('Total Aboard', fontsize=14)
plt.ylabel('Total Fatalities', fontsize=14)

# Add a colorbar for the decade
cbar = plt.colorbar(scatter, label='Decade', orientation='vertical', fraction=0.046, pad=0.04)
cbar.ax.tick_params(labelsize=12)  # Increase colorbar tick size

# Add a legend for point sizes
for size in [50, 100, 150]:  # Example sizes
    plt.scatter([], [], s=size, c='gray', alpha=0.6, edgecolors='k', label=f'Size {size}')

plt.legend(title='Ground Fatalities Scale', loc='upper right', fontsize=12, frameon=True)

# Grid and layout adjustments
plt.grid(alpha=0.3)
plt.tight_layout()

# Save the plot (optional)
plt.savefig('enhanced_fatalities_vs_aboard.png')

# Display the plot
plt.show()
