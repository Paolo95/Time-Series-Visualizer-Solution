import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=['date'])

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():

    # Draw line plot
    plt.figure(figsize=(15, 5)) 
    plt.plot(df.index, df.value, color='#8B0000')

    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')   

    plt.xlabel('Date')
    plt.ylabel('Page Views')

    fig = plt.gcf() 

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.groupby(by=[df.index, df.index.year.rename('Years'), df.index.month.rename('Months')]).mean()
    
    df_bar = df_bar.reset_index()

    df_bar['Years'] = [d.year for d in df_bar.date]
    df_bar['Months'] = [d.strftime('%B') for d in df_bar.date]

    month_order = ['January', 'February', 'March', 'April', 'May', 
                   'June', 'July', 'August', 'September', 'October', 
                   'November', 'December']

    df_bar['Months'] = pd.Categorical(df_bar['Months'], categories=month_order, ordered=True)

    df_pivot = df_bar.pivot_table(index='Years', columns='Months', values='value', aggfunc='mean')

    ax = df_pivot.plot(kind='bar', figsize=(12, 10), width=0.6)

    ax.set_xlabel("Years", fontsize=13)
    ax.set_ylabel("Average Page Views", fontsize=13)
    ax.set_xticklabels(df_pivot.index, rotation=90, fontsize=14)
    ax.legend(title='Years', fontsize=15, title_fontsize=15)

    plt.tight_layout() 

    fig = plt.gcf()
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():

    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_box['month'] = pd.Categorical(df_box['month'], categories=month_order, ordered=True)

    fig = plt.figure(figsize=(20, 7))

    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)

    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')

    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')

    sns.boxplot(x=df_box["year"], y=df_box["value"], ax=ax1, palette="Set2", hue=df_box["year"], legend=False, fliersize=3)
    
    sns.boxplot(x=df_box["month"], y=df_box["value"], ax=ax2, palette="Set2", hue=df_box["month"], legend=False, fliersize=3)

    fig.savefig('box_plot.png')

    return fig
