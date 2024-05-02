import streamlit as st
import pandas as pd
import helper_funcs.helper_funcs as helpf
import plotly.express as px
import json


st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded")


@st.cache_data
def load_data(data_path):
    with open(data_path, 'r') as file:
        json_data = json.load(file)
    return json_data


geo_split_data = load_data('data/mackenzie_scott_gifts_geosplit.json')
geo_split_df = pd.DataFrame(geo_split_data)
geo_split_df['country'] = geo_split_df['country'].replace('United States of America', 'United States')

header_cont = st.container()
main_cont = st.container()

hdr1a, hdr1b = header_cont.columns([1, 6])
hdr2a, hdr2b, hdr2c = header_cont.columns([1, 4, 1])
logo_path = 'img/art_deco.png'
hdr1a.image(logo_path)
st.sidebar.image(logo_path)
hdr2b.markdown(
    "<h1 style='text-align: center;'>Mackenzie Scott Philanthropic Analysis Project</h1>",
    unsafe_allow_html=True)
header_cont.markdown('---')
main_cont.markdown('###')
mn1a, mn1b, mn1c = main_cont.columns([1, 10, 1])
mn1b.markdown('''In the past five years, MacKenzie Scott has risen to prominence in the US philanthropic community, 
becoming one of its most influential figures. Following her divorce from Amazon founder Jeff Bezos in 2019, she signed 
the Giving Pledge and expressed a desire to promptly distribute her wealth to empower charitable organizations. 
Unlike many other large donors, Scott has shown a willingness to relinquish control over her donations. Despite still 
ongoing giving, she has already granted over $15 billion to nearly 2,000 organizations through her organization Yield 
Giving, revealing distinctive patterns in her approach. This analysis delves into the unprecedented scale and rapid 
pace of her philanthropic endeavors by examining available donation information.''')
mn1b.markdown('''In this analysis we look at the geographic spread, and the interconnectedness of the focus area as 
declared by the organisation receiving the donation.''')
mn1b.markdown('###')

org_data = geo_split_df.drop(columns=['gift_year', 'gift_amount', 'state', 'state_code']).drop_duplicates()
country_counts = org_data.groupby(['alpha3',
                                   'country']).size().reset_index(name='count').sort_values(by='count',
                                                                                            ascending=False)
tab1a, tab1b, tab1c, tab1d = mn1b.tabs(["Organisations Supported - Global",
                                        "Money Donated - Global",
                                        "Focused Analysis of the US",
                                        "Network Analysis"])

tab1a.markdown('#### Organisations Supported - Global')
tab1a.markdown('These charts displays a count of the number of organisations given donations globally.')
tab1a.markdown('As we can see below MacKenzie Scott has funded organisations across the world, but has funded a '
               'disproportionate number of US charities compared to the rest of the world.')

tab1a1, tab1a2 = tab1a.tabs(["Map", "Bar Chart"])

fig = px.choropleth(country_counts,
                    locations='alpha3',
                    locationmode='ISO-3',
                    projection='natural earth',
                    color='count',
                    hover_name='country',
                    height=800,
                    color_continuous_scale=px.colors.sequential.Viridis)


tab1a1.plotly_chart(fig, use_container_width=True)

fig = px.bar(country_counts, x='country', y='count',
             height=800,
             color_continuous_scale=px.colors.sequential.Viridis)
fig.update_layout(
    xaxis_title='Country Name',
    yaxis_title='Organisation Count'
)
tab1a2.plotly_chart(fig, use_container_width=True)

tab1a.markdown('###')
tab1a.markdown('#### Organisations Supported - Global(ex USA)')
tab1a.markdown('These charts display a count of the number of organisations given donations globally, '
               'excluding the USA.')
tab1a.markdown('If we exclude the USA from the data the spread becomes more even, but with a focus in funding '
               'organisations in India, Brazil and Eastern Africa')

tab1a3, tab1a4 = tab1a.tabs(["Map", "Bar Chart"])

country_counts_no_usa = country_counts[country_counts['alpha3'] != 'USA']

fig = px.choropleth(country_counts_no_usa,
                    locations='alpha3',
                    locationmode='ISO-3',
                    projection='natural earth',
                    color='count',
                    hover_name='country',
                    height=800,
                    color_continuous_scale=px.colors.sequential.Viridis)

tab1a3.plotly_chart(fig, use_container_width=True)

fig = px.bar(country_counts_no_usa, x='country', y='count',
             height=800,
             color_continuous_scale=px.colors.sequential.Viridis)
fig.update_layout(
    xaxis_title='Country Name',
    yaxis_title='Organisation Count'
)
tab1a4.plotly_chart(fig, use_container_width=True)


tab1b.markdown('#### Money Donated - Global')
tab1b.markdown('This map displays the amount of money donated to each country globally in Millions of Dollars. '
               'Not all this data has been published.')
tab1b1, tab1b2 = tab1b.tabs(["Map", "Bar Chart"])

geo_split_spending_df = geo_split_df[geo_split_df['gift_amount'].notnull()]

geo_split_spending_df['gift_amount'] = geo_split_spending_df['gift_amount'].astype(int)
country_amount_sum = geo_split_spending_df.groupby(['alpha3',
                                                    'country'])['gift_amount'].sum().reset_index()
country_amount_sum = country_amount_sum.sort_values(by='gift_amount', ascending=False)
country_amount_sum['gift_amount'] = country_amount_sum['gift_amount'] / 1000000

fig = px.choropleth(country_amount_sum,
                    locations='alpha3',
                    locationmode='ISO-3',
                    projection='natural earth',
                    color='gift_amount',
                    hover_name='country',
                    height=800,
                    color_continuous_scale=px.colors.sequential.Magma)

tab1b1.plotly_chart(fig, use_container_width=True)

fig = px.bar(country_amount_sum, x='country', y='gift_amount',
             height=800,
             color_continuous_scale=px.colors.sequential.Viridis)
fig.update_layout(
    xaxis_title='Country Name',
    yaxis_title='Amount Gifted (Million USD)'
)
tab1b2.plotly_chart(fig, use_container_width=True)

tab1b.markdown('###')
tab1b.markdown('#### Money Donated - Global(ex USA)')
tab1b.markdown('This map displays the amount of money donated to each country globally, excluding the USA, in Millions '
               'of Dollars. Not all this data has been published.')
tab1b3, tab1b4 = tab1b.tabs(["Map", "Bar Chart"])

geo_split_no_usa_df = geo_split_spending_df[geo_split_spending_df['alpha3'] != 'USA']
country_amount_sum = geo_split_no_usa_df.groupby(['alpha3',
                                                  'country'])['gift_amount'].sum().reset_index()
country_amount_sum = country_amount_sum.sort_values(by='gift_amount', ascending=False)
country_amount_sum['gift_amount'] = country_amount_sum['gift_amount'] / 1000000

fig = px.choropleth(country_amount_sum,
                    locations='alpha3',
                    locationmode='ISO-3',
                    projection='natural earth',
                    color='gift_amount',
                    hover_name='country',
                    height=800,
                    color_continuous_scale=px.colors.sequential.Magma)
tab1b3.plotly_chart(fig, use_container_width=True)

fig = px.bar(country_amount_sum, x='country', y='gift_amount',
             height=800,
             color_continuous_scale=px.colors.sequential.Viridis)
fig.update_layout(
    xaxis_title='Country Name',
    yaxis_title='Amount Gifted (Million USD)'
)
tab1b4.plotly_chart(fig, use_container_width=True)


tab1b.markdown('###')
tab1b.markdown('#### Money Donated Per Organisation (Average) - Global')
tab1b.markdown('This map displays the average(mean) amount of money donated to each organisation in each country '
               'globally in Millions of Dollars. Not all this data has been published.')
tab1b5, tab1b6 = tab1b.tabs(["Map", "Bar Chart"])
grouped = geo_split_spending_df.groupby(['alpha3',
                                         'country',
                                         'organization'])['gift_amount'].sum().reset_index()
average_gift_per_org = grouped.groupby(['alpha3',
                                        'country'])['gift_amount'].mean().reset_index()
average_gift_per_org = average_gift_per_org.sort_values(by='gift_amount', ascending=False)
average_gift_per_org['gift_amount'] = average_gift_per_org['gift_amount'] / 1000000

fig = px.choropleth(average_gift_per_org,
                    locations='alpha3',
                    locationmode='ISO-3',
                    projection='natural earth',
                    color='gift_amount',
                    hover_name='country',
                    height=800,
                    color_continuous_scale=px.colors.sequential.Magma)
tab1b5.plotly_chart(fig, use_container_width=True)

fig = px.bar(average_gift_per_org, x='country', y='gift_amount',
             height=800,
             color_continuous_scale=px.colors.sequential.Viridis)
fig.update_layout(
    xaxis_title='Country Name',
    yaxis_title='Amount Gifted (Million USD)'
)
tab1b6.plotly_chart(fig, use_container_width=True)


tab1b.markdown('###')
tab1b.markdown('#### Organisation Count Where Gift Amount Unreported')
tab1b.markdown('This map displays the count of organisations in each country where the gift amount is unreported.')
tab1b7, tab1b8, tab1b9, tab1b10 = tab1b.tabs(["Map - Total Count", "Map - Percentage",
                                              "Bar Chart - Total Count", "Bar Chart - Percentage"])
geo_split_null_df = geo_split_df.query('gift_amount != gift_amount')
country_counts_null_df = geo_split_null_df.groupby(['alpha3',
                                                    'country']
                                                   ).size().reset_index(name='count'
                                                                        ).sort_values(by='count', ascending=False)
null_gift_count = geo_split_df[geo_split_df['gift_amount'].isnull()].groupby('alpha3').size()
total_count = geo_split_df.groupby('alpha3').size()
percentage_null = (null_gift_count / total_count) * 100
result_df = pd.DataFrame({
    'alpha3': percentage_null.index,
    'country': [geo_split_df[geo_split_df['alpha3'] == alpha3]['country'].iloc[0]
                for alpha3 in percentage_null.index],
    'percentage_null': percentage_null.values
})
result_df = result_df.sort_values(by='percentage_null', ascending=False)

fig = px.choropleth(country_counts_null_df,
                    locations='alpha3',
                    locationmode='ISO-3',
                    projection='natural earth',
                    color='count',
                    hover_name='country',
                    height=800,
                    color_continuous_scale=px.colors.sequential.Magma)
tab1b7.plotly_chart(fig, use_container_width=True)


fig = px.choropleth(result_df,
                    locations='alpha3',
                    locationmode='ISO-3',
                    projection='natural earth',
                    color='percentage_null',
                    hover_name='country',
                    height=800,
                    color_continuous_scale=px.colors.sequential.Magma)
tab1b8.plotly_chart(fig, use_container_width=True)

fig = px.bar(country_counts_null_df, x='country', y='count',
             height=800,
             color_continuous_scale=px.colors.sequential.Viridis)
fig.update_layout(
    xaxis_title='Country Name',
    yaxis_title='Organisation Count'
)
tab1b9.plotly_chart(fig, use_container_width=True)

fig = px.bar(result_df, x='country', y='percentage_null',
             height=800,
             color_continuous_scale=px.colors.sequential.Viridis)
fig.update_layout(
    xaxis_title='Country Name',
    yaxis_title='Organisation Percentage'
)
tab1b10.plotly_chart(fig, use_container_width=True)

tab1b11, tab1b12 = tab1b.tabs(["Total Spend per Year", "By Country Spend per Year"])
total_spend = geo_split_spending_df.groupby('gift_year')['gift_amount'].sum().reset_index()
total_spend['gift_amount'] = round(total_spend['gift_amount'] / 1000000, 2)
fig = px.line(total_spend, x='gift_year', y='gift_amount', height=800, markers=True)
fig.update_layout(
    xaxis=dict(
        tickmode='array',
        tickvals=sorted(list(total_spend['gift_year'].unique()))
    ),
    xaxis_title='Year',
    yaxis_title='Total Reported Spend (Million USD)'
)
tab1b11.plotly_chart(fig, use_container_width=True)
total_spend = geo_split_spending_df.groupby(['country', 'gift_year'])['gift_amount'].sum().reset_index()
total_spend['gift_amount'] = round(total_spend['gift_amount'] / 1000000, 2)
fig = px.line(total_spend, x='gift_year', y='gift_amount', color='country', height=800, markers=True)
fig.update_layout(
    xaxis=dict(
        tickmode='array',
        tickvals=sorted(list(total_spend['gift_year'].unique()))
    ),
    xaxis_title='Year',
    yaxis_title='Reported Spend By Country (Million USD)'
)
tab1b12.plotly_chart(fig, use_container_width=True)

usa_split_df = geo_split_df[geo_split_df['state_code'].notnull()]
state_counts = usa_split_df.groupby(['state',
                                     'state_code']).size().reset_index(name='count').sort_values(by='count',
                                                                                                 ascending=False)

tab1c.markdown('#### Analysis of the USA by State')
fig = px.choropleth(state_counts,
                    locations='state_code',
                    locationmode='USA-states',
                    color='count',
                    hover_name='state',
                    projection='albers usa',
                    height=800,
                    color_continuous_scale=px.colors.sequential.Viridis)

tab1c.markdown('#### Map of Organisations Supported - USA by State')
tab1c.markdown('This map displays a count of the number of organisations given donations in each state in the USA.')
tab1c.plotly_chart(fig, use_container_width=True)

usa_split_spending_df = usa_split_df[usa_split_df['gift_amount'].notnull()]
country_amount_sum = usa_split_spending_df.groupby(['state_code', 'state'])['gift_amount'].sum().reset_index()
country_amount_sum['gift_amount'] = country_amount_sum['gift_amount'] / 1000000

fig = px.choropleth(country_amount_sum,
                    locations='state_code',
                    locationmode='USA-states',
                    color='gift_amount',
                    hover_name='state',
                    projection='albers usa',
                    height=800,
                    color_continuous_scale=px.colors.sequential.Magma)

tab1c.markdown('#### Map of Money Donated - USA by State')
tab1c.markdown('This map displays the amount of money donated to each State in Millions of Dollars.'
               'Not all this data has been published.')
tab1c.plotly_chart(fig, use_container_width=True)

usa_split_spending_df = usa_split_df[usa_split_df['gift_amount'].notnull()]
grouped = usa_split_spending_df.groupby(['state', 'state_code', 'organization'])['gift_amount'].sum().reset_index()
average_gift_per_org = grouped.groupby(['state', 'state_code'])['gift_amount'].mean().reset_index()
average_gift_per_org['gift_amount'] = average_gift_per_org['gift_amount'] / 1000000

fig = px.choropleth(average_gift_per_org,
                    locations='state_code',
                    locationmode='USA-states',
                    color='gift_amount',
                    hover_name='state',
                    projection='albers usa',
                    height=800,
                    color_continuous_scale=px.colors.sequential.Magma)

tab1c.markdown('#### Map of Money Donated Per Organisation (Average) - USA by State')
tab1c.markdown('This map displays the average(mean) amount of money donated per organisation in each State in Millions '
               'of Dollars. Not all financial data has been published.')
tab1c.plotly_chart(fig, use_container_width=True)


# Network Analysis
body_container_one = st.container()
network_data = load_data('data/mackenzie_scott_gifts.json')

network_list = []
for document in network_data:
    focus_areas = document.get('org_reported_focus_areas', None)
    if len(focus_areas) > 1:
        network_list.append(sorted(focus_areas))

node_weight_list, edge_weight_list = helpf.generate_network_data(network_list)
network_graph = helpf.generate_network(node_weight_list, edge_weight_list)
communities = helpf.community_detection(network_graph)
cliques = helpf.clique_detection(network_graph)
tab1d.markdown('### Top 10 Most Influential Nodes by Algorithm')
tab1d.dataframe(helpf.centrality_detection(network_graph),
                hide_index=True,
                use_container_width=True)
tab1d.markdown('###')
tab1d.markdown(f'### Top {len(communities)} Node Sub Groups')
for index, community in enumerate(communities):
    tab1d.markdown(f'{index + 1}) {community}')
tab1d.markdown('###')
tab1d.markdown(f'### Top {len(cliques)} Largest Cliques')
for index, clique in enumerate(cliques):
    tab1d.markdown(f'{index + 1}) {clique}')
tab1d.markdown('###')

# graph_net = Network(height='1000px',
#                     bgcolor='#222222',
#                     font_color='white')
# graph_net.from_nx(network_graph)
# graph_net.repulsion(node_distance=750, central_gravity=0.1,
#                     spring_length=250, spring_strength=0.10,
#                     damping=0.95)
# try:
#     path = 'tmp'
#     graph_net.save_graph(f'{path}/pyvis_graph.html')
#     HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')
# except:
#     path = 'html_files'
#     graph_net.save_graph(f'{path}/pyvis_graph.html')
#     HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')
# with tab1d.expander("Expand To View Network Graph"):
#     components.html(HtmlFile.read(), height=1000)

