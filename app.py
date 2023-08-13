# app.py
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# import time
import json
import requests
import re
from bs4 import BeautifulSoup
import plotly.graph_objs as go
from flask import Flask, request, send_file
from flask import Flask, request, jsonify, make_response
import io
import pandas as pd


service = Service('/home/uday/Chromedriver')
service.start()
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--headless')
browser = Chrome(service=service, options=options)

app = Flask(__name__)

@app.route('/generate_graph')
def generate_graph():
    # Get product URL from request
    product_url = request.args.get('product_url')
    # print(f"Product URL :- {product_url}")

    browser.get('https://www.pricebefore.com/')
    print("Ok") 

    search_box = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'search-box-home')))
    search_box.send_keys(product_url)
    search_box.send_keys(Keys.RETURN)

    # time.sleep(7)

    new_url = browser.current_url
    # print('New URL:', new_url)
            
    r = requests.get(new_url)
    htmlcontent = r.content

    soup = BeautifulSoup(htmlcontent,'html.parser')
    title = soup.title
    # print(title)

    paras = soup.find_all('canvas')

    paras1 = None
    scripts = soup.find_all('script')
    for script in scripts:
        if 'var data' in script.text:
            paras1 = script.text
            break
            
    if paras1:
        match = re.search(r'var\s+data\s*=\s*(.*?);', paras1)
        if match:
            data_str = match.group(1)
            # print(data_str)
            data = json.loads(data_str)
            dates_list = data["dates"]
            prices_list = data["prices"]
            df = pd.DataFrame({'col1': dates_list, 'col2': prices_list})
            df.to_csv('output.csv',index=False)

    return generate_and_return_graph(dates_list, prices_list)

def generate_and_return_graph(x_data, y_data):
    trace = go.Scatter(x=x_data, y=y_data, mode='lines+markers')
    fig = go.Figure(data=[trace])
    fig.update_layout(hovermode='x')

    # Generate the plot using plotly
    fig.show()

    # Save the plot to a PNG file
    buf = io.BytesIO()
    fig.write_image(buf, format='png')
    buf.seek(0)
    # Return the file as a Flask response
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run()
