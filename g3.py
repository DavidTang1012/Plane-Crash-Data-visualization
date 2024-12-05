from wordcloud import WordCloud
import matplotlib.pyplot as plt

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
