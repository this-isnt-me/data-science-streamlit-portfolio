import streamlit as st
import pandas as pd


st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded")


@st.cache_data
def load_csv_data(data_path):
    loaded_df = pd.read_csv(data_path)
    return loaded_df


header_cont = st.container()
hdr11, hdr12 = st.columns([1, 6])
hdr21, hdr22, hdr23 = st.columns([1, 4, 1])
logo_path = 'img/art_deco.png'
st.sidebar.image(logo_path)
hdr11.image(logo_path)
hdr22.markdown("<h1 style='text-align: center; color: white;'>Tim D. Clarke Data Science Portfolio</h1>",
               unsafe_allow_html=True)
hdr22.markdown("###")
hdr22.markdown("<h3 style='text-align: center; color: white;'>Profitability Analysis</h3>",
               unsafe_allow_html=True)
hdr22.markdown("Profitability analysis is the cornerstone of informed decision-making for businesses across industries. "
               "By meticulously examining revenues and costs, it unveils insights into the financial health and "
               "efficiency of operations, guiding strategic planning and resource allocation. Through a granular "
               "examination of profit margins, contribution margins, and cost structures, businesses can identify "
               "areas for improvement, optimize pricing strategies, trim unnecessary expenses, and ultimately enhance "
               "overall profitability. Moreover, profitability analysis enables businesses to evaluate the performance "
               "of different products, services, and segments, empowering them to focus resources on high-yield "
               "ventures while mitigating risks associated with underperforming areas. In essence, it serves as a "
               "compass for sustainable growth and competitive advantage in today's dynamic business landscape.")
hdr22.markdown("###")
hdr22.page_link("pages/1 Profitability Analysis.py", label="Link to Profitability Analysis Project")
hdr22.markdown("###")

hdr22.markdown("<h3 style='text-align: center; color: white;'>Customer Segmentation</h3>",
               unsafe_allow_html=True)
hdr22.markdown("Customer segmentation analysis is indispensable for businesses aiming to thrive in today's dynamic "
               "market landscape. By dividing customers into distinct groups based on shared characteristics such as "
               "demographics, behaviors, and preferences, businesses can tailor their marketing strategies, products, "
               "and services to meet the unique needs of each segment. This targeted approach enhances customer "
               "satisfaction, fosters loyalty, and maximizes profitability by allocating resources effectively and "
               "efficiently. Moreover, segmentation analysis enables businesses to identify untapped market "
               "opportunities, refine their value proposition, and stay ahead of competitors. Ultimately, it serves "
               "as a strategic compass guiding businesses towards sustainable growth and success in an increasingly "
               "competitive environment.")
hdr22.markdown("###")
hdr22.page_link("pages/2 Customer Clustering.py", label="Link to Customer Segmentation Project")
hdr22.markdown("###")

hdr22.markdown("<h3 style='text-align: center; color: white;'>Stockmarket Comparison Analysis</h3>",
               unsafe_allow_html=True)
hdr22.markdown("Stock market comparison analysis plays a pivotal role in providing investors, businesses, and analysts "
               "with valuable insights into the performance and relative strengths of various stocks, sectors, and "
               "markets. By meticulously examining and contrasting the performance metrics, trends, and financial "
               "indicators of different stocks or markets, analysts can identify opportunities, mitigate risks, and "
               "make informed investment decisions. This analytical approach not only aids in evaluating the "
               "competitiveness of individual companies within an industry but also facilitates strategic portfolio "
               "diversification and allocation of resources. Furthermore, stock market comparison analysis serves as a "
               "crucial tool for benchmarking, enabling stakeholders to gauge the overall health and efficiency of "
               "financial markets, thus contributing to prudent investment strategies and overall financial stability.")
hdr22.markdown("###")
hdr22.page_link("pages/3 Stockmarket Comparison Analysis.py", label="Link to Stockmarket Comparison Analysis Project")
hdr22.markdown("###")

hdr22.markdown("<h3 style='text-align: center; color: white;'>Eurovision Voting Analysis</h3>",
               unsafe_allow_html=True)
hdr22.markdown('''Utilizsing network analysis techniques like community detection and centrality analysis provides 
valuable insights into Eurovision voting patterns, considering the intricate dynamics influenced by political 
relationships across Europe. By representing participating countries as nodes and voting connections as edges, this 
approach uncovers underlying structures in voting behavior. It reveals regional alliances and cultural affinities 
through community detection, while identifying influential countries and strategic voting strategies with centrality 
analysis. Through these methods, Eurovision voting patterns are analyzed beyond the surface, offering concise yet 
nuanced perspectives on the complex interplay of cultural, political, and social factors defining this iconic 
international event.''')
hdr22.markdown("###")
hdr22.page_link("pages/4 Eurovision Voting Analysis.py", label="Link to Eurovision Voting Analysis Project")
hdr22.markdown("###")



