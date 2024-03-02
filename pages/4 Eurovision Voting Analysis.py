import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from pyvis.network import Network
import helper_funcs.charts as pltchart
import helper_funcs.helper_funcs as helpf

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded")

replace_map = {
    'Moldova (the Republic of)': 'Moldova',
    'Netherlands (the)': 'Netherlands',
    'Russian Federation (the)': 'Russia',
    'United Kingdom of Great Britain and Northern Ireland (the)': 'U.K.',
    'Serbia and Montenegro': 'Serbia & Montenegro',
    'Bosnia and Herzegovina': 'Bosnia & Herzegovina'
}


@st.cache_data
def load_data(data_path):
    loaded_df = pd.read_csv(data_path, dtype={'year': str})
    loaded_df = loaded_df.drop(columns=['tele_points', 'jury_points'])
    loaded_df['from_country_name'] = loaded_df['from_country_name'].replace(replace_map)
    loaded_df['to_country_name'] = loaded_df['to_country_name'].replace(replace_map)
    return loaded_df


src_data_path = 'https://raw.githubusercontent.com/this-isnt-me/credit-card-fraud-network/main/dataset' \
                '/eurovision_votes_processed.csv'

header_cont = st.container()
main_cont = st.container()

hdr1a, hdr1b = header_cont.columns([1, 6])
hdr2a, hdr2b, hdr2c = header_cont.columns([1, 4, 1])
logo_path = 'img/art_deco.png'
hdr1a.image(logo_path)
st.sidebar.image(logo_path)
hdr2b.markdown(
    "<h1 style='text-align: center; color: white;'>Eurovision Voting Analysis Project</h1>",
    unsafe_allow_html=True)
header_cont.markdown('---')
hdr3a, hdr3b, hdr3c = header_cont.columns([1, 10, 1])
hdr3b.markdown('''It is often believed that the results of "the Eurovision Song Contest" final have a political 
element.   

This dashboard allows people to review the data to create an opinion. Analyzing Eurovision voting patterns through 
network analysis techniques such as community detection and centrality analysis offers a unique lens to understand 
the intricate dynamics of this iconic cultural event. By representing participating countries as nodes and voting 
connections as edges, network analysis unveils underlying structures and patterns in voting behavior. Community 
detection reveals clusters of countries with similar voting preferences, shedding light on regional alliances and 
cultural affinities. Centrality analysis identifies influential countries that play pivotal roles in shaping voting 
outcomes, providing insights into power dynamics and strategic voting strategies. Through these techniques, 
Eurovision voting patterns can be examined beyond the surface, uncovering the complex interplay of cultural, 
political, and social factors that define this celebrated international spectacle.   

For future analysis it would be interesting to take account of additional data, for example immigration which might 
have an effect on voting patterns.''')
header_cont.markdown('---')

eurovision_df = load_data(src_data_path)
mn1a, mn1b, mn1c = main_cont.columns([1, 10, 1])
mn1b.markdown(f'#### Filter Options')
mn1b.markdown('###### Select Options to Filter Chart Data Using Dropdowns Below')
mn1b.markdown('###')


mn2a, mn2b, mn2c, mn2d, mn2e = main_cont.columns([1, 2, 4, 4, 1])

year_list = sorted(eurovision_df['year'].unique())

chosen_year = mn2b.multiselect(label='Select Year of Competition',
                               options=year_list,
                               placeholder='Choose A Year',
                               key='year_dropdown')

from_country_list = helpf.filter_countries(input_dataframe=eurovision_df,
                                           filter_column='from_country_name',
                                           year=chosen_year)

to_country_list = helpf.filter_countries(input_dataframe=eurovision_df,
                                         filter_column='to_country_name',
                                         year=chosen_year)

chosen_country_from = mn2c.selectbox(label='Select Country Awarding Points',
                                     options=from_country_list,
                                     index=None,
                                     placeholder='Choose A Country',
                                     key='country_from_dropdown')

chosen_country_to = mn2d.selectbox(label='Select Country Receiving Points',
                                   options=to_country_list,
                                   index=None,
                                   placeholder='Choose A Country',
                                   key='country_to_dropdown')
mn3a, mn3b, mn3c = main_cont.columns([1, 10, 1])
if mn3b.button("Run Analysis", use_container_width=True):
    if len(chosen_year) == 0:
        chosen_year = year_list
    main_cont.markdown('###')
    geo_plt = pltchart.plot_votes_geo(input_dataframe=eurovision_df,
                                      from_country=chosen_country_from,
                                      to_country=chosen_country_to,
                                      year=chosen_year)

    bar_plt = pltchart.plot_votes_bar(input_dataframe=eurovision_df,
                                      from_country=chosen_country_from,
                                      to_country=chosen_country_to,
                                      year=chosen_year)

    network_df, network_plt, G, importance_df = pltchart.plot_network(input_dataframe=eurovision_df,
                                                                      year=chosen_year)
    if geo_plt or network_plt:
        geo_plt_expander = main_cont.expander("Expand To View Voting Maps", expanded=False)
        geo_plt_expander.markdown('###')
        if geo_plt and network_plt:
            gp1a, gp1b = geo_plt_expander.columns([1, 1])
        elif geo_plt and not network_plt:
            gp1a = geo_plt_expander.container()
        elif not geo_plt and network_plt:
            gp1b = geo_plt_expander.container()
        if geo_plt:
            gp1a.markdown('#### Map of Votes Received By Country')
            gp1a.plotly_chart(geo_plt, use_container_width=True)
        if network_plt:
            gp1b.markdown('#### Map of Communities Detectected in Voting Data')
            gp1b.plotly_chart(network_plt, use_container_width=True)

    if bar_plt or network_plt:
        voting_data_expander = main_cont.expander("Expand To View Voting Data Country by Country", expanded=False)
        voting_data_expander.markdown('###')
        if bar_plt and network_plt:
            bp1a, bp1b = voting_data_expander.columns([1, 1])
        elif bar_plt and not network_plt:
            bp1a = voting_data_expander.container()
        elif not bar_plt and network_plt:
            bp1b = voting_data_expander.container()
        if bar_plt is not None:
            bp1a.markdown('#### Votes By Country')
            bp1a.plotly_chart(bar_plt, use_container_width=True)

        if network_plt is not None:
            network_df = network_df.drop(
                columns=['from_country',
                         'to_country']).sort_values(
                by=['from_country_name',
                    'total_points'],
                ascending=[True, False]).rename(
                columns={"from_country_name": "From",
                         "to_country_name": "To",
                         "total_points": "Points Awarded"})
            bp1b.markdown('#### Table of Points Awarded')
            bp1b.dataframe(network_df,
                           hide_index=True,
                           use_container_width=True)
            voting_data_expander.markdown('###')
            voting_data_expander.markdown('#### Data on Most Influential Countries')
            voting_data_expander.dataframe(importance_df,
                                           hide_index=True,
                                           use_container_width=True)
        if G is not None:
            graph_net = Network(height='800px',
                                bgcolor='#222222',
                                font_color='white')
            graph_net.from_nx(G)
            graph_net.repulsion(node_distance=420, central_gravity=0.33,
                                spring_length=110, spring_strength=0.10,
                                damping=0.95)
            path = 'html_files'
            graph_net.save_graph(f'{path}/pyvis_graph.html')
            HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')
            with main_cont.expander("Expand To View Network Graph"):
                st.markdown(f'### Network Graph of Eurovision Voting in {pltchart.join_list(chosen_year)}')
                st.markdown(f'###')
                components.html(HtmlFile.read(), height=850)

main_cont.expander("Expand to View Complete Dataframe").dataframe(eurovision_df,
                                                                  hide_index=True,
                                                                  use_container_width=True)
st.markdown("""---""")