import requests
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import seaborn as sns
from matplotlib.gridspec import GridSpec
import mplcyberpunk
import matplotlib.dates as mdates
from scipy.stats import norm

class CryptoMarketSentimentAnalyzer:
    def __init__(self):
        plt.style.use('cyberpunk')
        self.colors = {
            'Extreme Fear': '#FF2700',
            'Fear': '#FF8E00',
            'Neutral': '#FFD700',
            'Greed': '#7CFF00',
            'Extreme Greed': '#00FF00'
        }
        
    def fetch_data(self, limit=365):
        """Fetch extended historical data"""
        url = f"https://api.alternative.me/fng/?limit={limit}"
        response = requests.get(url)
        return response.json()
    
    def process_data(self, raw_data):
        """Process raw data into pandas DataFrame"""
        data = []
        for entry in raw_data['data']:
            date = datetime.fromtimestamp(int(entry['timestamp']))
            data.append({
                'date': date,
                'value': int(entry['value']),
                'classification': entry['value_classification']
            })
        return pd.DataFrame(data)

    def create_gauge(self, value, classification, ax):
        """Create cyberpunk-styled gauge"""
        # Similar to before but with enhanced styling
        theta = np.linspace(3*np.pi/4, -3*np.pi/4, 100)
        r = 0.8
        
        # Create gradient effect
        for i in range(80):
            r_i = r - i*0.003
            x = r_i * np.cos(theta)
            y = r_i * np.sin(theta)
            alpha = 1 - i/80
            ax.plot(x, y, 'w-', alpha=alpha, linewidth=1)
        
        # Add value markers
        for value in [0, 25, 50, 75, 100]:
            angle = 3*np.pi/4 - (value/100) * (3*np.pi/2)
            marker_x = r * np.cos(angle)
            marker_y = r * np.sin(angle)
            ax.text(marker_x*1.1, marker_y*1.1, str(value), 
                   ha='center', va='center', color='cyan')
        
        # Add glowing needle
        needle_angle = 3*np.pi/4 - (value/100) * (3*np.pi/2)
        for i in range(5):
            alpha = 1 - i/5
            width = 3 - i*0.5
            ax.plot([0, r * np.cos(needle_angle)], 
                   [0, r * np.sin(needle_angle)], 
                   color='red', alpha=alpha, linewidth=width)

    def create_trend_analysis(self, df, ax):
        """Create advanced trend analysis plot"""
        # Plot main line
        ax.plot(df['date'], df['value'], color='cyan', linewidth=2)
        
        # Add moving averages
        df['MA7'] = df['value'].rolling(window=7).mean()
        df['MA30'] = df['value'].rolling(window=30).mean()
        ax.plot(df['date'], df['MA7'], '--', color='yellow', label='7-day MA')
        ax.plot(df['date'], df['MA30'], '--', color='magenta', label='30-day MA')
        
        # Add volatility bands
        df['Volatility'] = df['value'].rolling(window=20).std()
        ax.fill_between(df['date'], 
                       df['MA30'] - df['Volatility'],
                       df['MA30'] + df['Volatility'],
                       color='white', alpha=0.1)

    def create_visualization(self):
        """Create complete advanced dashboard"""
        # Fetch and process data
        raw_data = self.fetch_data()
        df = self.process_data(raw_data)
        
        # Create main figure
        fig = plt.figure(figsize=(20, 12))
        gs = GridSpec(3, 3, figure=fig)
        
        # 1. Main Gauge
        ax_gauge = fig.add_subplot(gs[0, 0])
        self.create_gauge(df.iloc[0]['value'], df.iloc[0]['classification'], ax_gauge)
        ax_gauge.set_title('Current Market Sentiment', color='cyan', pad=20)
        
        # 2. Trend Analysis
        ax_trend = fig.add_subplot(gs[0, 1:])
        self.create_trend_analysis(df, ax_trend)
        ax_trend.set_title('Sentiment Trend Analysis', color='cyan')
        ax_trend.grid(True, alpha=0.2)
        
        # 3. Distribution Analysis
        ax_dist = fig.add_subplot(gs[1, 0])
        sns.histplot(df['value'], ax=ax_dist, color='cyan', alpha=0.5)
        ax_dist.set_title('Sentiment Distribution', color='cyan')
        
        # 4. Classification Breakdown
        ax_class = fig.add_subplot(gs[1, 1])
        class_counts = df['classification'].value_counts()
        ax_class.pie(class_counts, labels=class_counts.index, 
                    colors=list(self.colors.values()),
                    autopct='%1.1f%%')
        ax_class.set_title('Classification Breakdown', color='cyan')
        
        # 5. Correlation with Price (placeholder)
        ax_corr = fig.add_subplot(gs[1, 2])
        ax_corr.text(0.5, 0.5, 'Correlation Analysis\n(Premium Feature)',
                    ha='center', va='center', color='cyan')
        ax_corr.set_title('Market Correlation', color='cyan')
        
        # 6. Statistics Panel
        ax_stats = fig.add_subplot(gs[2, :])
        stats_text = f"""
        Current Value: {df.iloc[0]['value']} ({df.iloc[0]['classification']})
        7-Day Average: {df['value'].head(7).mean():.1f}
        30-Day Average: {df['value'].head(30).mean():.1f}
        Volatility: {df['value'].std():.1f}
        Dominant Sentiment: {df['classification'].mode()[0]}
        Data Points Analyzed: {len(df)}
        """
        ax_stats.text(0.5, 0.5, stats_text, ha='center', va='center', 
                     color='white', fontsize=12)
        ax_stats.set_title('Market Statistics', color='cyan')
        ax_stats.axis('off')
        
        # Add main title
        fig.suptitle('Crypto Market Sentiment Analysis Dashboard', 
                    color='white', fontsize=24, y=0.95)
        
        # Add watermark
        fig.text(0.99, 0.01, 'Created by Your Name', 
                ha='right', color='gray', fontsize=8)
        
        plt.tight_layout()
        plt.show()
        
        # Save the visualization
        plt.savefig('crypto_sentiment_dashboard.png', 
                   dpi=300, bbox_inches='tight', facecolor='black')

if __name__ == "__main__":
    analyzer = CryptoMarketSentimentAnalyzer()
    analyzer.create_visualization()
