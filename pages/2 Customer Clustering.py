import pandas as pd
import streamlit as st
from sklearn.cluster import KMeans
import plotly.express as px
import io

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded")


@st.cache_data
def load_csv_data(data_path):
    loaded_df = pd.read_csv(data_path)
    return loaded_df


src_data_path = 'https://raw.githubusercontent.com/this-isnt-me/credit-card-fraud-network/main/dataset/online_retail.csv'

header_cont = st.container()
main_cont = st.container()

hdr1a, hdr1b = header_cont.columns([1, 6])
hdr2a, hdr2b, hdr2c = header_cont.columns([1, 4, 1])
logo_path = 'img/art_deco.png'
hdr1a.image(logo_path)
st.sidebar.image(logo_path)
hdr2b.markdown(
    "<h1 style='text-align: center; color: white;'>Customer Clustering and Segmentation Analysis Project</h1>",
    unsafe_allow_html=True)
header_cont.markdown('---')
hdr3a, hdr3b, hdr3c = header_cont.columns([1, 10, 1])
hdr3b.markdown('''This project uses RFM analysis and clustering techniques to identify different customer 
clusters in a dataset of online transactions from the UC Irvine Machine Learning Repository.   

Customer segmentation, which involves dividing customers into distinct groups based on shared characteristics and 
behaviors, can help businesses improve their marketing strategies and enhance customer satisfaction.   

Customer segmentation allows businesses to tailor their product offerings by understanding the unique needs and 
preferences of each customer group. By doing so, they can create more personalized and effective marketing campaigns, 
leading to higher customer retention and increased revenue.   

By combining RFM analysis, which evaluates customer behavior based on recency, frequency, and monetary factors, 
with K-Means clustering, a data-driven method for grouping customers, this notebook explores how to identify and 
target different customer segments effectively. RFM analysis helps in distinguishing the best customers and improving 
the spending habits of low-scoring customers, ultimately aiding in customer retention and revenue growth.''')

transaction_data = load_csv_data(src_data_path)


# EXPLORATORY DATA ANALYSIS
main_cont.markdown('---')
main_cont.markdown("<h2 style='text-align: center; color: white;'>Exploratory Data Analysis</h2>",
                   unsafe_allow_html=True)
main_cont.markdown('###')
mn1a, mn1b, mn1c = main_cont.columns([1, 10, 1])

tab1a, tab1b, tab1c, tab1d = mn1b.tabs(["All Data", "Data Overview", "Data Description", "Missing Data"])

tab1a.markdown("<h3 style='text-align: center; color: white;'>View All Data</h3>",
               unsafe_allow_html=True)
tab1a.markdown('''
In the table below we can see the top 5 rows of data contained within the dataset.   

###
''')
tab1a.table(transaction_data.head())

tab1b.markdown("<h3 style='text-align: center; color: white;'>View Overview of Data</h3>",
               unsafe_allow_html=True)
tab1b.markdown('''
By viewing details of the data columns we can get an idea of the type of data contained in each column and if any is 
missing. we can see the data is a mix of text, dates and numbers and that there is data missing in the "Description" 
and "CustomerID" columns.   

###
''')
buffer = io.StringIO()
transaction_data.info(buf=buffer)
transaction_data_buffer = buffer.getvalue()

tab1b.text(transaction_data_buffer)


tab1c.markdown("<h3 style='text-align: center; color: white;'>View Description of Numerical Data</h3>",
               unsafe_allow_html=True)
tab1c.markdown('''
By viewing basic statistical information about the numerical columns, in the table above, we obtain 
insights into the distribution and summary statistics of these numerical values. This will help helps us understand 
features in the data making it easier to identify trends, anomalies, or areas of interest.   

There are a few points to note, including customer ID's are stored with a decimal point, this would be better as whole 
numbers, also we can see that there are negative values in both the Quantity and UnitPrice columns. We will also drop 
rows where the Quantity and UnitPrice columns have negative values.   

###
''')
tab1c.table(transaction_data.describe())

tab1d.markdown("<h3 style='text-align: center; color: white;'>Identify Missing Data</h3>",
               unsafe_allow_html=True)
tab1d.markdown('''
 As we can see there is data missing in the Description and CustomerID columns, with approximately 1/4 missing in the 
 CustomerID Column. As we need the CustomerID to carry out the analysis effectively and identify unique customers to 
 cluster, we will drop all rows that are missing the CustomerID.   

###
''')
missing_percent = transaction_data.isnull().mean() * 100
missing_data_df = pd.DataFrame({'Percentage Missing': missing_percent}).sort_values(by='Percentage Missing',
                                                                                    ascending=False)
tab1d.table(missing_data_df.transpose())
tab1d.markdown('###')
missing_data_df = missing_data_df.reset_index()
fig1 = px.bar(missing_data_df,
              x='index', y='Percentage Missing',
              color='Percentage Missing', color_continuous_scale='Viridis')
fig1.update_layout(title='Percentage of Missing Data in Each Column',
                   xaxis_title='Column Name',
                   yaxis_title='Percentage Missing',
                   coloraxis_colorbar_title='Perc',
                   legend_title='Value')
tab1d.plotly_chart(fig1, use_container_width=True)


transaction_data = transaction_data.dropna(subset=['CustomerID'])
transaction_data = transaction_data[(transaction_data['Quantity'] > 0) &
                                    (transaction_data['UnitPrice'] > 0)]
transaction_data['CustomerID'] = transaction_data['CustomerID'].astype(int)


# DATA CLEANING
main_cont.markdown('---')
main_cont.markdown("<h2 style='text-align: center; color: white;'>Data Cleaning</h2>",
                   unsafe_allow_html=True)
main_cont.markdown('###')
mn2a, mn2b, mn2c = main_cont.columns([1, 10, 1])
tab2a, tab2b, tab2c = mn2b.tabs(["RFM Metrics", "RFM Scaled", "Data Clustering"])
tab2a.markdown("<h3 style='text-align: center; color: white;'>RFM Metrics</h3>",
               unsafe_allow_html=True)
tab2a.markdown('''
RFM Analysis serves as an effective technique for understanding and quantifying customer behavior. 
It assesses customers across three essential dimensions:

*   **Recency** (R): Reflects how recently a specific customer engaged in a purchase.
*   **Frequency** (F): Indicates how frequently they make purchases.
*   **Monetary Value** (M): Measures the amount of money they spend.

Utilising the processed dataset, we'll compute the recency, frequency, and monetary values for each customer. 
Subsequently, the values will be adapted to the a score scale ranging from 1 to 5.

For calculating Recency we are going to assume that the data was exported from the system the day after the most 
recent order.

Total spend also needs to be calculated we can do this using the quantity and unit price. We will then calculate how 
many days since spend, how many orders placed and total spend.   

###
''')

data_date = pd.Timestamp(max(transaction_data['InvoiceDate'])) + pd.DateOffset(days=1)

transaction_data['TotalSpend'] = transaction_data['Quantity'] * transaction_data['UnitPrice']
rfm_df = transaction_data.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (data_date - pd.Timestamp(x.max())).days,
    'InvoiceNo': 'nunique',
    'TotalSpend': 'sum'
})
rfm_df = rfm_df.rename(columns={'InvoiceDate': 'Recency',
                                'InvoiceNo': 'Frequency'})
tab2a.markdown('''In the Table Below we can see the number of days since most recent order (Recency), number of orders 
(Frequency) and amount of money spent by customer(TotalSpend).   

###
''')
tab2a.table(rfm_df.head())


tab2b.markdown("<h3 style='text-align: center; color: white;'>RFM Scaling</h3>",
               unsafe_allow_html=True)
tab2b.markdown('''
Next we will assign a scale of 1-5 to Recency, Frequency and TotalSpend, in order to do this we will need to know the 
maximum and minium value in each column of the three columns.   
We can assign the data to categories of 1 to 5, as per standard RFM practice. This also ensures the 3 metrics we are 
interested are on the same scale. For Recency most recent orders have a score of 5 while orders more than 250 days old 
get a score of 1.   

###
''')
recency_bins = [rfm_df['Recency'].min()-1, 20, 50, 150, 250,
                rfm_df['Recency'].max()]
frequency_bins = [rfm_df['Frequency'].min() - 1, 2, 3, 10, 100,
                  rfm_df['Frequency'].max()]
spend_bins = [rfm_df['TotalSpend'].min() - 3, 300, 600, 2000, 5000,
              rfm_df['TotalSpend'].max()]
# Calculate Recency score based on custom bins
rfm_df['R_Score'] = pd.cut(rfm_df['Recency'], bins=recency_bins,
                           labels=range(1, 6), include_lowest=True)

# Reverse the Recency scores so that higher values indicate more recent purchases
rfm_df['R_Score'] = 5 - rfm_df['R_Score'].astype(int) + 1

# Calculate Frequency and Monetary scores based on custom bins
rfm_df['F_Score'] = pd.cut(rfm_df['Frequency'], bins=frequency_bins,
                           labels=range(1, 6), include_lowest=True).astype(int)
rfm_df['M_Score'] = pd.cut(rfm_df['TotalSpend'], bins=spend_bins,
                           labels=range(1, 6), include_lowest=True).astype(int)
tab2b.table(rfm_df.head())


tab2c.markdown("<h3 style='text-align: center; color: white;'>Data Clustering</h3>",
               unsafe_allow_html=True)
tab2c.markdown('''
Now we move towards clustering the data, we will use the K-means clustering algorithm. In order to do this we need to 
identify the number of clusters, and we can use the elbow technique to do this, we will use the inertia value to do 
this (The sum of squared distance of samples to their closest cluster center).   

We can see in the chart below that the elbow sits about 3 or 4, we will plump for 4 clusters.   

###
''')

X = rfm_df[['R_Score', 'F_Score', 'M_Score']]
inertia = []
for k in range(2, 16):
    kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
    kmeans.fit(X)
    inertia.append(kmeans.inertia_)
inertia_data = {'Number of Clusters (k)': range(2, 16), 'Inertia': inertia}
inertia_df = pd.DataFrame(inertia_data)
fig2 = px.line(inertia_df, x='Number of Clusters (k)', y='Inertia', markers=True)

fig2.update_layout(
    title='Elbow Curve for K-means Clustering',
    xaxis_title='Number of Clusters (k)',
    yaxis_title='Inertia',
    showlegend=False,
    template='plotly_white'
)
tab2c.plotly_chart(fig2, use_container_width=True)


# KNN Clustering
kmeans_model = KMeans(n_clusters=4, n_init=10, random_state=42)
rfm_df['Cluster'] = kmeans_model.fit_predict(X)
rfm_df['Cluster'] += 1
rfm_df['Cluster'] = 'Cluster ' + rfm_df['Cluster'].astype(str)


# DATA VISUALISATION
main_cont.markdown('---')
main_cont.markdown("<h2 style='text-align: center; color: white;'>Cluster Visualisation</h2>",
                   unsafe_allow_html=True)
main_cont.markdown('###')
mn3a, mn3b, mn3c = main_cont.columns([1, 10, 1])
tab3a, tab3b = mn3b.tabs(["Classify Customers", "Customers in Each Cluster"])
tab3a.markdown("<h3 style='text-align: center; color: white;'>Classify Cluster by RFM Data</h3>",
               unsafe_allow_html=True)
tab3a.markdown('''
Looking at the chart below we can see that: 

*   Cluster 1 - has the lowest rates of RFM, they don’t spend often, and haven't bought recently. Customers in cluster 
3 can be considered to be At-Risk.
*   Cluster 2 - Has moderate rates of RFM, below cluster 1 and above clusters 3 and 4. We can classify them as Regular 
Customers.
*   Cluster 3 - has the highest rates of RFM and can be classified as Strong or Loyal Customers.
*   Cluster 4 - also has low rates of spending and buying less frequently, though they have made a purchase recently s
o potentially are Newly Acquired customers. 

The company may want to consider the following strategies tailored for different customer segments:

Loyal Customers: Extend exclusive privileges such as personalized discounts, early access to promotions, and premium 
perks to demonstrate appreciation for their loyalty.

Regular Customers: Launch appreciation campaigns, offer referral bonuses, and provide rewards as tokens of gratitude 
for their ongoing loyalty.

At-Risk Customers: Implement re-engagement initiatives featuring enticing discounts or promotions aimed at revitalizing 
their interest and encouraging repeat purchases.

Newly Acquired Customers: Develop targeted marketing campaigns focused on brand education and offer discounts for 
subsequent purchases to enhance brand familiarity and foster repeat business.   

###
''')

cluster_summary = rfm_df.groupby('Cluster').agg({
    'R_Score': 'mean',
    'F_Score': 'mean',
    'M_Score': 'mean'
}).reset_index()
cluster_melted_df = cluster_summary.melt(id_vars='Cluster',
                                         var_name='Metric',
                                         value_name='Score')

colors = ['#440154', '#2A788E', '#7AD151', '#FDE725']
fig3 = px.bar(cluster_melted_df, x="Cluster", y="Score",
              color='Metric', barmode='group',
              color_discrete_sequence=colors,
              height=800)

fig3.update_layout(title_font_size=20, legend_title='Clusters',
                   title='Average RFM Scores for Each Cluster',
                   xaxis_title='Cluster Number',
                   yaxis_title='Average Score',
                   template='plotly_white')
new = {'R_Score': 'Avg Recency',
       'F_Score': 'Avg Frequency',
       'M_Score': 'Avg Monetary'}
fig3.for_each_trace(lambda t: t.update(name=new[t.name]))
tab3a.plotly_chart(fig3, use_container_width=True)


tab3b.markdown("<h3 style='text-align: center; color: white;'>Customer Split by Cluster</h3>",
               unsafe_allow_html=True)
tab3b.markdown('''
We can see, looking at the chart below, that there is a relatively even split between the 4 clusters.   

###
''')

per_cluster = rfm_df['Cluster'].value_counts()
total = per_cluster.sum()
percentage_df = (per_cluster / total) * 100
labels = ['Loyal Customers', 'Regular Customers', 'At-risk Customers', 'Newly Acquired Customers']

# Create a pie chart
fig4 = px.pie(names=labels,
              values=percentage_df,
              title='Percentage of Customers in Each Cluster',
              color_discrete_sequence=colors,
              height=800)
fig4.update_traces(textposition='inside', textinfo='percent+label')


tab3b.plotly_chart(fig4, use_container_width=True)
