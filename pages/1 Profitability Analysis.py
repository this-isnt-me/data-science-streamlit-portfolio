import streamlit as st
import re
import io
import pandas as pd
import plotly.express as px


st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded")


@st.cache_data
def load_csv_data(data_path):
    loaded_df = pd.read_csv(data_path)
    return loaded_df


src_data_path = 'https://raw.githubusercontent.com/this-isnt-me/credit-card-fraud-network/main/dataset/food_orders_new_york.csv'

header_cont = st.container()
main_cont = st.container()

hdr1a, hdr1b = header_cont.columns([1, 6])
hdr2a, hdr2b, hdr2c = header_cont.columns([1, 4, 1])
logo_path = 'img/art_deco.png'
st.sidebar.image(logo_path)
hdr1a.image(logo_path)
hdr2b.markdown("<h1 style='text-align: center; color: white;'>Profitability Analysis Project</h1>",
               unsafe_allow_html=True)
header_cont.markdown('---')
hdr3a, hdr3b, hdr3c = header_cont.columns([1, 10, 1])
hdr3b.markdown('''Cost and Profitability Analysis, for this dataset, encompasses a comprehensive review of all expenses 
related to food order delivery, encompassing direct costs such as delivery fees and packaging, as well as indirect 
expenses like customer discounts and restaurant commission fees.   

By comparing these costs against the revenue generated, primarily derived from order values and commission fees, 
this analysis seeks to unveil the profitability of the food delivery service on a per-order basis.''')

orders_df = load_csv_data(src_data_path)
orders_df.columns = orders_df.columns.str.lower()
orders_df.columns = [re.sub(r'[^\w\s]', '_', col) for col in orders_df.columns]
orders_df.columns = [re.sub(r'\s+', '_', col) for col in orders_df.columns]

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
''')
tab1a.table(orders_df.head())

tab1b.markdown("<h3 style='text-align: center; color: white;'>View Overview of Data</h3>",
               unsafe_allow_html=True)
tab1b.markdown('''
By viewing details of the data columns we can get an idea of the type of data contained in each column and if any is 
missing. We can see the data is composed of 12 columns and 1000 rows, and is a mix of text, dates and numbers and that 
the majority of data is present. As we can see there is missing data in the "discounts_and_offers" column, but we can 
safely assume that where the data is missing no discount has been applied  

As part of the data cleaning process we will need to ensure the relevant date columns are in 
a datetime format and all monetary values are in a numeric format for performing calculations.   

###
''')
buffer = io.StringIO()
orders_df.info(buf=buffer)
orders_df_buffer = buffer.getvalue()
tab1b.text(orders_df_buffer)
missing_percent = orders_df.isnull().mean() * 100
missing_data_df = pd.DataFrame({'Percentage Missing': missing_percent}).sort_values(by='Percentage Missing',
                                                                                    ascending=False)
tab1b.markdown('###')
tab1b.table(missing_data_df.transpose())


tab1c.markdown("<h3 style='text-align: center; color: white;'>View Description of Numerical Data</h3>",
               unsafe_allow_html=True)
tab1c.markdown('''
By viewing basic statistical information about the numerical columns, in the table above, we obtain 
insights into the distribution and summary statistics of these numerical values. This will help helps us understand 
features in the data making it easier to identify trends, anomalies, or areas of interest.

###
''')
tab1c.table(orders_df.describe())


# DATA CLEANING
def extract_discount(discount_str):
    # Using regular expressions to extract discount
    try:
        match = re.search(r'(\d+(\.\d+)?)', str(discount_str))
        if match:
            return float(match.group(1))
        else:
            return 0.0
    except Exception as e:
        print("An error occurred:", e)
        print(discount_str)


orders_df['order_date_and_time'] = pd.to_datetime(orders_df['order_date_and_time'], format='%d/%m/%Y %H:%M')
orders_df['delivery_date_and_time'] = pd.to_datetime(orders_df['delivery_date_and_time'], format='%d/%m/%Y %H:%M')
orders_df['discount_percentage'] = orders_df['discounts_and_offers'].apply(lambda x: extract_discount(x))
orders_df['discount_amount'] = orders_df.apply(lambda x: (x['order_value'] * x['discount_percentage'] / 100)
                                               if x['discount_percentage'] > 1
                                               else x['discount_percentage'], axis=1)

orders_df['discount_amount'] = orders_df.apply(lambda x: x['discount_amount'] if x['discount_percentage'] <= 1
                                               else x['order_value'] * x['discount_percentage'] / 100, axis=1)

main_cont.markdown('---')
main_cont.markdown("<h2 style='text-align: center; color: white;'>Data Cleaning</h2>",
                   unsafe_allow_html=True)
main_cont.markdown('###')
mn2a, mn2b, mn2c = main_cont.columns([1, 10, 1])
mn2b.markdown("<h3 style='text-align: center; color: white;'>Initial Data Cleaning</h3>",
              unsafe_allow_html=True)
mn2b.markdown('''
The data has been through a cleaning process:   

*   the date columns have been converted to a datetme format.
*   Two new columns have been added that have numeric values for Discount Amount and Discount Percentage.

###
''')
mn2b.table(orders_df.head())

main_cont.markdown('---')
# Data Visualisation
main_cont.markdown("<h2 style='text-align: center; color: white;'>Data Visualisation</h2>",
                   unsafe_allow_html=True)
main_cont.markdown('###')
mn3a, mn3b, mn3c = main_cont.columns([1, 10, 1])

tab3a, tab3b, tab3c, tab3d = mn3b.tabs(["Cost Analysis", "Current Financial Distribution",
                                        "Current Financial Strategy", "Financial Modelling"])

tab3a.markdown("<h3 style='text-align: center; color: white;'>Cost Analysis - Overall Metrics</h3>",
               unsafe_allow_html=True)
tab3a.markdown('''
In our cost analysis, we will assess several expenses linked to each order:   

*   Delivery Fee: The charge incurred for delivering the order.
*   Payment Processing Fee: The cost associated with processing the payment.
*   Discount Amount: The deduction applied to the order.   

Our aim is to compute the total platform cost per order and subsequently analyze this data to gain insights into the 
overall cost composition.   

The primary revenue source for the platform is the Commission Fee. To determine the net profit, we will subtract the 
total costs, inclusive of discounts, from the revenue generated via commission fees.   

Upon review of the table below, it becomes apparent that the cumulative costs surpass the total revenue sourced from 
commission fees, leading to a net loss. This observation implies that the existing commission rates, delivery fees, 
and discount tactics may not be conducive to sustaining profitability.
''')

orders_df['total_costs'] = orders_df['delivery_fee'] + orders_df['payment_processing_fee'] + orders_df['discount_amount']
orders_df['revenue'] = orders_df['commission_fee']
orders_df['profit'] = orders_df['revenue'] - orders_df['total_costs']

total_orders = int(orders_df.shape[0])
total_revenue = orders_df['revenue'].sum()
total_costs = orders_df['total_costs'].sum()
total_profit = orders_df['profit'].sum()

overall_metrics_df = pd.DataFrame({
    'metric': ['Total Orders', 'Total Revenue', 'Total Costs', 'Total Profit'],
    'count': [total_orders, total_revenue, total_costs, total_profit]
})


tab3a.table(overall_metrics_df)

tab3b.markdown("<h3 style='text-align: center; color: white;'>Plot Current Financial Data</h3>",
               unsafe_allow_html=True)
tab3b.markdown('''
To gain deeper insights into the cost, revenue, and profit distribution, let's create visualizations for the following:

*   A histogram depicting profits per order, illustrating the spread between profitable and unprofitable orders.
*   A pie chart representing the proportion of total costs, encompassing delivery fees, payment processing fees, and 
discounts.
*   A bar chart for comparing total revenue, total costs, and total profit.

Looking at the histogram we can see the data has a long tail, that is to say The histogram illustrates a broad range 
of profit margins per order, with a significant portion of orders yielding negative returns (profits below 0). 
The presence of a red dashed line denotes the average profit, which falls within the negative range, emphasizing the 
prevailing scenario of losses.

###
''')
fig1 = px.histogram(orders_df, x='profit', nbins=50,
                    color_discrete_sequence=['skyblue'],
                    opacity=0.7,
                    height=600)

fig1.add_vline(x=orders_df['profit'].mean(), line_dash="dash", line_color="red",
               annotation_text=f'Mean: {orders_df["profit"].mean():.2f}',
               annotation_position="top right")

fig1.update_layout(title='Profit Distribution per Order',
                   xaxis_title='Profit ($)',
                   yaxis_title='Number of Orders')
tab3b.plotly_chart(fig1, use_container_width=True)
tab3b.markdown('###')

tab3b.markdown('''
The pie chart below demonstrates the distribution of total costs among various components, including delivery fees, 
payment processing fees, and discount amounts. Notably, discounts represent a substantial proportion of these costs, 
indicating that promotional strategies could significantly influence the overall profitability.

###
''')

costs_breakdown = orders_df[['delivery_fee', 'payment_processing_fee', 'discount_amount']].sum()
headers = ['name', 'count']
costs_breakdown = pd.DataFrame({headers[0]: costs_breakdown.index, headers[1]: costs_breakdown.values})
new_labels = {'delivery_fee': 'Delivery Fee',
              'payment_processing_fee': 'Payment Processing Fee',
              'discount_amount': 'Discount Amount'}
costs_breakdown['name'] = costs_breakdown['name'].map(new_labels)
fig2 = px.pie(costs_breakdown, values=costs_breakdown['count'], names=costs_breakdown['name'],
              title='Proportion of Total Costs',
              color_discrete_sequence=['#440154', '#2A788E', '#7AD151'],
              height=600)
tab3b.plotly_chart(fig2, use_container_width=True)
tab3b.markdown('###')

tab3b.markdown('''
The bar chart below illustrates the overall revenue, costs, and resulting profit. It vividly demonstrates the 
disparity between revenue and costs, highlighting that costs exceed revenue, resulting in a net loss.

###
''')
overall_metrics_df = overall_metrics_df[overall_metrics_df['metric'] != 'Total Orders']

colors = ['#440154', '#2A788E', '#7AD151']
fig3 = px.bar(overall_metrics_df, x="metric", y="count",
              color='metric',
              color_discrete_sequence=colors,
              height=600)

fig3.update_layout(title_font_size=20, legend_title='Metrics',
                   title='Total Revenue, Costs and Profit',
                   xaxis_title='Metric',
                   yaxis_title='Amount ($)',
                   template='plotly_white')
tab3b.plotly_chart(fig3, use_container_width=True)

tab3c.markdown("<h3 style='text-align: center; color: white;'>Extract Current Financial Strategy & Suggest Alternative</h3>",
               unsafe_allow_html=True)
tab3c.markdown('''
From our current analysis, it's evident that the discounts applied to food orders are resulting in substantial 
financial losses. Therefore, it's imperative to devise a new strategic approach to enhance profitability. This 
entails identifying an optimal balance between offering discounts and imposing commissions.

To achieve this, a thorough examination of the characteristics of profitable orders is necessary. Specifically, we 
aim to determine:

*   A revised average commission percentage based on profitable orders.
*   An updated average discount percentage for profitable orders, serving as a benchmark to gauge the level of discount 
that maintains profitability.   

By establishing these new benchmarks, we can propose adjustments that not only ensure the profitability of individual 
orders but also have a broad impact across all orders, thereby enhancing overall profitability.s

###
''')
orders_df['commission_percentage'] = (orders_df['commission_fee'] / orders_df['order_value']) * 100
orders_df['discount_percentage'] = (orders_df['discount_amount'] / orders_df['order_value']) * 100
current_avg_commission_percentage = orders_df['commission_percentage'].mean()
current_avg_discount_percentage = orders_df['discount_percentage'].mean()
profitable_orders = orders_df[orders_df['profit'] > 0]

new_avg_commission_percentage = profitable_orders['commission_percentage'].mean()
new_avg_discount_percentage = profitable_orders['discount_percentage'].mean()
tab3c.markdown(f'''
*   Current Average Commission : {current_avg_commission_percentage:.2f}%   
*   Current Average Discount : {current_avg_discount_percentage:.2f}%   
*   Profitable Average Commission : {new_avg_commission_percentage:.2f}%   
*   Profitable Average Discount : {new_avg_discount_percentage:.2f}%

After analyzing profitable orders, we've identified a new set of average values that could signify an optimal balance 
in commission and discount percentages.
The average commission percentage for profitable orders notably surpasses the overall average observed across all 
orders. This disparity suggests that higher commission rates could serve as a pivotal factor in achieving 
profitability. Conversely, the average discount percentage for profitable orders notably falls below the overall 
average, indicating that reducing discounts could potentially enhance profitability without significantly impacting 
order volume.   

Based on these findings, adopting a strategy that targets a commission rate near 30% and a discount rate 
around 6% may offer prospects for improving profitability.

###
''')

recommended_commission_percentage = 30.0
recommended_discount_percentage = 6.0

orders_df['simulated_commission_fee'] = orders_df['order_value'] * (recommended_commission_percentage / 100)
orders_df['simulated_discount_amount'] = orders_df['order_value'] * (recommended_discount_percentage / 100)

# recalculate total costs and profit with simulated values
orders_df['simulated_total_costs'] = (orders_df['delivery_fee'] +
                                      orders_df['payment_processing_fee'] +
                                      orders_df['simulated_discount_amount'])

orders_df['simulated_profit'] = (orders_df['simulated_commission_fee'] -
                                 orders_df['simulated_total_costs'])


fig4 = px.histogram(orders_df, x='simulated_profit', nbins=50,
                    color_discrete_sequence=['skyblue'],
                    opacity=0.7,
                    height=600)

fig4.add_vline(x=orders_df['simulated_profit'].mean(), line_dash="dash", line_color="red",
               annotation_text=f'Mean: {orders_df["simulated_profit"].mean():.2f}',
               annotation_position="top right")

fig4.update_layout(title='Simulated Profit Distribution per Order Using 30% Commission and 6% discount rates',
                   xaxis_title='Simulated Profit ($)',
                   yaxis_title='Number of Orders')
tab3c.plotly_chart(fig4, use_container_width=True)

tab3d.markdown("<h3 style='text-align: center; color: white;'>Model Different Financial Strategies</h3>",
               unsafe_allow_html=True)
tab3d.markdown('''
Here it is possible to model different scenarios by selecting different commission rates and discount rates.

###
''')
tab3d1, tab3d2, tab3d3, tab3d5 = tab3d.columns([1, 2, 2, 1])
tab3d12, tab3d22, tab3d32 = tab3d.columns([1, 4, 1])
com_number = tab3d2.number_input('Choose a Commission Percentage', min_value=0, max_value=100)
disc_number = tab3d3.number_input('Choose a Discount Percentage', min_value=0, max_value=100)
if tab3d22.button("Run Simulation", use_container_width=True):
    tab3d.markdown('###')
    tab3d.markdown(f"<h5 style='text-align: center; color: white;'>Simulated Profit Distribution - {com_number}% Commission and {disc_number}% discount</h5>",
                   unsafe_allow_html=True)
    tab3d.markdown('###')
    orders_df['simulated_commission_fee'] = orders_df['order_value'] * (com_number / 100)
    orders_df['simulated_discount_amount'] = orders_df['order_value'] * (disc_number / 100)
    # recalculate total costs and profit with simulated values
    orders_df['simulated_total_costs'] = (orders_df['delivery_fee'] +
                                          orders_df['payment_processing_fee'] +
                                          orders_df['simulated_discount_amount'])

    orders_df['simulated_profit'] = (orders_df['simulated_commission_fee'] -
                                     orders_df['simulated_total_costs'])

    fig5 = px.histogram(orders_df, x='simulated_profit', nbins=50,
                        color_discrete_sequence=['skyblue'],
                        opacity=0.7,
                        height=600)

    fig5.add_vline(x=orders_df['simulated_profit'].mean(), line_dash="dash", line_color="red",
                   annotation_text=f'Mean: {orders_df["simulated_profit"].mean():.2f}',
                   annotation_position="top right")

    fig5.update_layout(title=f'Simulated Profit Distribution per Order Using {com_number}% Commission and {disc_number}% discount rates',
                       xaxis_title='Simulated Profit ($)',
                       yaxis_title='Number of Orders')
    tab3d.plotly_chart(fig5, use_container_width=True)
    tab3d.markdown('###')
    tab3d.markdown(f"<h5 style='text-align: center; color: white;'>Current Profit Distribution</h5>",
                   unsafe_allow_html=True)
    tab3d.markdown('###')
    tab3d.plotly_chart(fig1, use_container_width=True)


