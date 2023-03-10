from backend.scraping import *
from backend.load import *
from backend.dataframes import results_to_dataframe
from backend.clip_functions import *
from backend.show import *
import streamlit as st


@st.cache_data
def get_bbc_headlines():
    config = load_yaml("config.yaml")  # get the unsplash image categories - this is cached
    bbc_categories = config['BBC_CATEGORIES']
    bbc_categories.sort()
    # get all the unsplash image category:url dictionary - this is cached
    bbc_headlines_dict = scrape_bbc_headlines('https://www.bbc.co.uk/news/', bbc_categories)
    return bbc_headlines_dict


def text_classification_loop(category, bbc_headlines_dict, tokeniser, model):

    c1, c2, c3 = st.columns((3, 2, 5))
    if 'text_keep' not in st.session_state:
        headlines = bbc_headlines_dict[category]
        headline = get_random_element(headlines)
        st.session_state['text_keep'] = headline
        c1.subheader(f'_"{headline}"_')
        st.markdown('#')
        st.markdown('#')

    else:

        c1.subheader(f'_"{st.session_state["text_keep"]}"_')
        st.markdown('#')
        st.markdown('#')

    text_input_string = st.text_input('Choose some labels for this text - seperate labels with a comma e.g. "business, sports"', 'dog, cat')
    labels = [i for i in text_input_string.split(",")]

    probs = classify_texts(labels, st.session_state['text_keep'], model, tokeniser)
    df = results_to_dataframe(probs, labels)
    c3.subheader('Predicted probabilities')
    c3.plotly_chart(plot_results(df, x_label='labels', y_label='probabilities'))

    more_headlines = st.empty()
    next_headline = more_headlines.button('Get new headline')
    if next_headline:
        st.session_state.pop('text_keep')
        more_headlines.empty()
        st.experimental_rerun()

    return
