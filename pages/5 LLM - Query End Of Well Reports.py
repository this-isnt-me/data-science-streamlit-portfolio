import streamlit as st

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded")


header_cont = st.container()
main_cont = st.container()

hdr1a, hdr1b = header_cont.columns([1, 6])
hdr2a, hdr2b, hdr2c = header_cont.columns([1, 4, 1])
logo_path = 'img/art_deco.png'
hdr1a.image(logo_path)
st.sidebar.image(logo_path)
hdr2b.markdown(
    "<h1 style='text-align: center; color: white;'>LLM/RAG Project for querying Oil and Gas End of Well Reports</h1>",
    unsafe_allow_html=True)
header_cont.markdown('---')
hdr3a, hdr3b, hdr3c = header_cont.columns([1, 10, 1])
hdr3b.markdown('''Large language models, with a Retrieval-Augmented Generation (RAG) system offer significant 
advantages for engaging with End Of Well reports. Engineers can swiftly navigate complex technical documents, 
extracting precise information and insights with remarkable efficiency. RAG's unique retrieval mechanism allows for 
targeted access to vast knowledge repositories, ensuring the most relevant and up-to-date data is readily available. 
This accelerates decision-making processes and enhances problem-solving by providing contextually rich responses and 
generating clear, concise summaries tailored to specific queries. The fusion of large language models with RAG not 
only streamlines information retrieval but also empowers engineers to delve deeper into data making 
better informed decisions.''')
hdr3b.markdown('---')

hdr3b.video('https://youtu.be/UO1tQ4SfgKQ')



