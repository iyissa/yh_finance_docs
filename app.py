import requests
import numpy as np 
import matplotlib.pyplot as plt
import streamlit as st




#---------------------------------#

st.set_option('deprecation.showfileUploaderEncoding', False)

#---------------------------------#
# Page layout
## Page expands to full width
st.set_page_config(layout="wide")

#---------------------------------#
# Title

st.title('Stock Comparison App')
st.markdown("""
This app uses API Dojo's API available on RapidAPI to perform quick and simple analysis on Stocks.

""")
#---------------------------------#
# About
expander_bar = st.expander("About")
expander_bar.markdown(""" 
* **API:** [YH Finance API](https://rapidapi.com/apidojo/api/yh-finance).
* **API Documentation:** [Documentation](https://ayomide-yissa.gitbook.io/yh-finance-docs/)
* **Webpage Credit:** Data Professsor Streamlit Freecodecamp [Tutorials](https://github.com/dataprofessor/streamlit_freecodecamp).
""")

symbols = st.text_input("Enter a comma-separated list of symbols:")
st.write("If there's an error, Please ensure there is no space within the comma-seperated list. e.g SPY,IWM,QQQ")
selected_keys = ['regularMarketPrice', 'regularMarketChangePercent', 'regularMarketVolume', 'averageDailyVolume3Month', 'fiftyDayAverage', 'twoHundredDayAverage', 'marketCap']

form = st.form(key='input_form')
selected_keys_input = form.multiselect('Select keys:', selected_keys, default=selected_keys)
submit_button = form.form_submit_button(label='Submit')

@st.cache_data
def get_data(symbols: list):
    url = "https://yh-finance.p.rapidapi.com/market/v2/get-quotes"
    querystring = {"region": "US", "symbols": ",".join(symbols)}
    headers = {
        "X-RapidAPI-Key": st.secrets["api_key"],
        "X-RapidAPI-Host": "yh-finance.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    response_data = response.json()
    json_data = response_data['quoteResponse']['result']
    return {data['symbol']: data for data in json_data}

def get_selected_data(symbols):
    data = get_data(symbols)
    selected_data = {}
    for symbol, symbol_data in data.items():
        selected_data[symbol] = {key: symbol_data[key] for key in selected_keys}
    return selected_data

def plot_data(symbols:list, selected_keys:list):
    selected_data = get_selected_data(symbols)
    symbol_vars = list(selected_data[symbols[0]].keys())
    symbol_values = []
    for symbol in symbols:
        symbol_values.append(list(selected_data[symbol].values()))

    # Define the bar positions
    bar_positions = np.arange(len(symbol_vars))

    # Create the figure and axis objects
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create the bar plots for each symbol
    width = 0.2
    for i in range(len(symbols)):
        ax.bar(bar_positions + width * (i - 0.5), symbol_values[i], width, label=symbols[i])

    # Set the axis labels, title, and legend
    ax.set_ylabel('Values')
    ax.set_title('Comparison of Selected Data for Symbols')
    ax.set_xticks(bar_positions)
    ax.set_xticklabels(symbol_vars, rotation=60, fontsize=7)
    ax.legend()

    # Set y-axis scale to logarithmic
    ax.set_yscale('log')

    # Return the plot
    return fig

if submit_button:
    fig = plot_data(symbols.split(','), selected_keys_input)
    st.pyplot(fig)
