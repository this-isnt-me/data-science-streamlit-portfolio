import pandas as pd
import networkx as nx
import plotly.express as px
import json


hex_country_dict = {
    'Albania': '#ED1C24',
    'Andorra': '#D52B1E',
    'Armenia': '#D62612',
    'Australia': '#00008B',
    'Austria': '#FF0000',
    'Azerbaijan': '#3F9D2F',
    'Belarus': '#D52B1E',
    'Belgium': '#ED1C24',
    'Bosnia and Herzegovina': '#0D5EAF',
    'Bulgaria': '#00966E',
    'Croatia': '#FF0000',
    'Cyprus': '#FF0000',
    'Czechia': '#D7141A',
    'Denmark': '#C60C30',
    'Estonia': '#4891D9',
    'Finland': '#004FA3',
    'France': '#0055A4',
    'Georgia': '#FF0000',
    'Germany': '#000000',
    'Greece': '#0D5EAF',
    'Hungary': '#C21F2C',
    'Iceland': '#02529C',
    'Ireland': '#169B62',
    'Israel': '#13277A',
    'Italy': '#009246',
    'Latvia': '#9D2A28',
    'Lithuania': '#FDB913',
    'Luxembourg': '#D52B1E',
    'Malta': '#CF142B',
    'Moldova': '#FFD700',
    'Monaco': '#D52B1E',
    'Montenegro': '#C8102E',
    'Morocco': '#006233',
    'Netherlands': '#21468B',
    'North Macedonia': '#D2A429',
    'Norway': '#EF2B2D',
    'Poland': '#D52B1E',
    'Portugal': '#FF0000',
    'Romania': '#002B7F',
    'Russia': '#D52B1E',
    'San Marino': '#0033A0',
    'Serbia': '#D52B1E',
    'Serbia and Montenegro': '#D52B1E',
    'Slovakia': '#EE1C25',
    'Slovenia': '#007A2E',
    'Spain': '#C60B1E',
    'Sweden': '#0051BA',
    'Switzerland': '#FF0000',
    'Turkey': '#E30A17',
    'U.K.': '#00247D',
    'Ukraine': '#FFD500',
    'Yugoslavia': '#ED1C24'
}

def join_list(input_list):
    if len(input_list) == 1:
        return input_list[0]
    else:
        return ', '.join(input_list[:-1]) + ' & ' + input_list[-1]


def filter_data_frame(input_dataframe,
                      from_country=None,
                      to_country=None,
                      year=None,
                      full_name=False):
    ext = ''
    if full_name:
        ext ='_name'
    if year:
        input_dataframe = input_dataframe[input_dataframe['year'].isin(year)]
    if from_country and not to_country:
        input_dataframe = input_dataframe[input_dataframe['from_country_name'] == from_country]
        filter_col = f'to_country{ext}'
        input_dataframe = input_dataframe.groupby(filter_col)['total_points'].sum().reset_index(name='sum_value')
        input_dataframe['country'] = input_dataframe[filter_col].str.upper()
        title = f'Points Awarded by {from_country} in {join_list(year)}'
    if not from_country and to_country:
        input_dataframe = input_dataframe[input_dataframe['to_country_name'] == to_country]
        filter_col = f'from_country{ext}'
        input_dataframe = input_dataframe.groupby(filter_col)['total_points'].sum().reset_index(name='sum_value')
        input_dataframe['country'] = input_dataframe[filter_col].str.upper()
        title = f'Points Received by {to_country} in {join_list(year)}'
    if not from_country and not to_country:
        filter_col = f'to_country{ext}'
        input_dataframe = input_dataframe.groupby(filter_col)['total_points'].sum().reset_index(name='sum_value')
        input_dataframe['country'] = input_dataframe[filter_col].str.upper()
        title = f'Votes For Each Country in {join_list(year)}'
    return input_dataframe, title


def plot_votes_geo(input_dataframe,
                   from_country=None,
                   to_country=None,
                   year=None):
    if (from_country and to_country) or not year :
        return None
    input_dataframe, title = filter_data_frame(input_dataframe=input_dataframe,
                                               from_country=from_country,
                                               to_country=to_country,
                                               year=year,
                                               full_name=False)
    geojson_path = "data/europe.geojson"
    with open(geojson_path, 'r') as file:
        geojson_data = json.load(file)
    fig = px.choropleth(
        input_dataframe,
        geojson=geojson_data,
        locations='country',
        featureidkey="properties.ISO2",
        color='sum_value',
        color_continuous_scale='Viridis',
        title=title,
        scope='europe',
        labels={'sum_value': 'Votes'},
        height=1000
    )
    return fig


def plot_votes_bar(input_dataframe,
                   from_country=None,
                   to_country=None,
                   year=None):
    if (from_country and to_country) or not year:
        return None
    input_dataframe, title = filter_data_frame(input_dataframe=input_dataframe,
                                               from_country=from_country,
                                               to_country=to_country,
                                               year=year,
                                               full_name=True)
    input_dataframe = input_dataframe.sort_values(by=['sum_value'], ascending=False)
    fig = px.bar(input_dataframe,
                 x='country',
                 y='sum_value',
                 color='country')#,
                 # color_continuous_scale='viridis',
                 # height=1000)

    # Update layout for better readability (optional)
    fig.update_layout(
        title=title,
        xaxis_title='Country',
        yaxis_title='Points Awarded'
    )
    return fig


def plot_network(input_dataframe,
                 year=None):
    if not year:
        return None
    input_dataframe = input_dataframe[input_dataframe['year'].isin(year)]
    input_dataframe = input_dataframe.groupby(['from_country_name',
                                               'to_country_name',
                                               'from_country',
                                               'to_country'])['total_points'].sum().reset_index()
    input_dataframe['from_country'] = input_dataframe['from_country'].str.upper()
    input_dataframe['to_country'] = input_dataframe['to_country'].str.upper()
    country_name_list = list(input_dataframe['from_country_name']) + list(input_dataframe['to_country_name'])
    country_code_list = list(input_dataframe['from_country']) + list(input_dataframe['to_country'])
    result_dict = {k: v for k, v in zip(country_code_list, country_name_list)}
    grouped_df = input_dataframe.groupby(['to_country_name',
                                          'to_country']).agg(Total=('total_points', 'sum')).reset_index()
    grouped_df['colour'] = grouped_df['to_country_name'].map(hex_country_dict)
    node_list = [(row['to_country'], {'value': row['Total'],
                                           'label': row['to_country_name'],
                                           'color': row['colour']}) for _, row in grouped_df.iterrows()]
    G = nx.DiGraph()
    G.add_nodes_from(node_list)
    for _, row in input_dataframe.iterrows():
        G.add_edge(row['from_country'], row['to_country'], weight=row['total_points'], value=row['total_points'])
    centrality = nx.eigenvector_centrality(G)
    centrality_list = [result_dict[v] for v, c in sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:10]]
    page_rank = nx.pagerank(G)
    page_rank_list = [result_dict[v] for v, c in sorted(page_rank.items(), key=lambda x: x[1], reverse=True)[:10]]
    betweenness = nx.betweenness_centrality(G)
    betweenness_list = [result_dict[v] for v, c in sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:10]]
    importance_df = pd.DataFrame({'Centrality Algorithm Importance': centrality_list,
                                  'Page Rank Algorithm Importance': page_rank_list,
                                  'Betweenness Algorithm Importance': betweenness_list})
    communities = nx.community.greedy_modularity_communities(G, weight='weight', cutoff=3, best_n=5)
    community_list = []
    for index, community in enumerate(communities):
        cluster = str(index + 1)
        for country in sorted(list(community)):
            community_list.append((cluster, country))
    community_dataframe = pd.DataFrame(community_list, columns=['community', 'country'])

    geojson_path = "data/europe.geojson"
    with open(geojson_path, 'r') as file:
        geojson_data = json.load(file)
    fig = px.choropleth(
        community_dataframe,
        geojson=geojson_data,
        locations='country',
        featureidkey="properties.ISO2",
        color='community',
        color_discrete_map={'1': 'red',
                            '2': 'blue',
                            '3': 'green',
                            '4': 'yellow',
                            '5': 'pink'},
        title=f'Communities identified in voting patterns for {join_list(year)}',
        scope='europe',
        labels={'community': 'Community'},
        height=1000
    )
    return input_dataframe, fig, G, importance_df

'''
ARTS AND CULTURE
Craft and traditional arts
Creative youth development
Cultural awareness
Literary arts
Multidisciplinary arts
Museums
Performing arts
Public arts
Visual arts
DEMOCRATIC PROCESS
Civic and social engagement
Democracy
ECONOMIC SECURITY AND OPPORTUNITY
Access to housing and housing development
Agricultural development
Economic development
Financial inclusion
Livelihoods and workforce development
EDUCATION
Early learning
Elementary, secondary education
Postsecondary, tertiary education
Vocational education
Youth development
ENVIRONMENT
Biodiversity
Climate change
Environmental justice
Natural resources conservation
EQUITY AND JUSTICE
Aging
Caste
Disability
Faith and religion
Gender identity
Immigration or migration
Incarceration and justice system involvement
Race and ethnicity
Sexual orientation
FUNDING AND REGRANTING
Fund
Regrantor
HEALTH
Access to healthcare
Active living
Child development and welfare
Chronic diseases
Infectious and parasitic diseases
Maternal and perinatal health
Mental and behavioral health
Nutrition and food security
Public health, public health infrastructure
Sexual and gender-based violence
Sexual and reproductive health and justice
Water access, sanitation, and hygiene
NONPROFIT SECTOR
Nonprofit sector strengthening
Philanthropic sector strengthening
ADDITIONAL AREAS
Bridging divides
Human rights
Humanitarian assistance and relief
'''