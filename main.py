from urllib import request
from flask import Flask, render_template
import logging
import requests
from pytrends.request import TrendReq
from datetime import datetime
import random
import time
from collections import Counter
import json

app = Flask(__name__)

LOGGER = logging.getLogger(__name__)

@app.route('/', methods=["GET"])
def hello_world():
 prefix_google = """
 <!-- Google tag (gtag.js) -->
<script async 
src="https://www.googletagmanager.com/gtag/js?id=G-PNWR0TFW4H"></script>
<script>
 window.dataLayer = window.dataLayer || [];
 function gtag(){dataLayer.push(arguments);}
 gtag('js', new Date());
 gtag('config', 'G-PNWR0TFW4H');
</script>
 """
 return prefix_google + "Welcome to our page"

@app.route('/logger', methods=['GET'])
def Message():
    app.logger.warning('Warning log')
    app.logger.error('Error log')
    app.logger.info('Info log')

    return render_template('textbox.html')

@app.route('/getcookie')
def cookie():
    req = requests.get("https://www.google.com/")
    app.logger.info(req)
    return req.cookies.get_dict()

@app.route('/getcookie2')
def cookie2():
    req = requests.get('https://analytics.google.com/analytics/web/#/a250427860p344255484')
    app.logger.info(req)
    return req.text

if __name__=="__main__":
    app.run(debug=True)

#Google trend:

@app.route('/trend', methods=['GET', 'POST'])
def trends():
    if request.method == 'POST':
        pytrend = TrendReq()

        keywords = request.form['keywords']

        keywords_list = keywords.split(' ')

        timeframe = '2022-10-01 2023-01-01'

        pytrend.build_payload(kw_list=keywords_list, timeframe=timeframe)
        trend_data = pytrend.interest_over_time().drop(['isPartial'], axis=1)

        dates = [datetime.fromtimestamp(int(date / 1e9)).date().isoformat() for date in trend_data.index.values.tolist()]

        params = {
            'type': 'line',
            'data': {
                'labels': dates,
                'datasets': []
            },
            'options': {
                "title": {
                    "text": 'My chart'
                },
                "scales": {
                    "yAxes": [{
                        "ticks": {
                            "beginAtZero": 'true'
                        }
                    }]
                }
            }
        }

        for column in trend_data.columns:
            params['data']['datasets'].append({'label': column, 
                                            'data': trend_data[column].values.tolist(),
                                            "borderColor": "#"+''.join([random.choice('0123456789ABCDEF') for i in range(6)]),
                                            "fill": 'false',
                                        })


        template = f"""  
        <html>
            <head>
                <title>Trend Comparison</title>
            </head>
            <body>
                <h1>Trend Data</h1>
                <p>Keywords: {keywords}</p>    
                <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.5.0/Chart.min.js"></script>
                <div><canvas id="myChart" width="25" height="25"></canvas></div>
                <script>
                    var ctx = document.getElementById('myChart');
                    var myChart = new Chart(ctx, {params});
                </script>
            </body>
        </html>
        """

        return template
    else:
        return render_template('trends.html')

#Execution time


def log_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time} seconds")
        return result
    return wrapper

@log_execution_time
def count_words_dict(text):
    word_counts = {}
    for word in text.split():
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1

@log_execution_time
def count_words_counter(text):
    Counter(text.split())

@app.route('/execution_time', methods=['GET', 'POST'])
def execution_time():
    with open('shakespeare.txt', 'r') as f:
        text = f.read()
    
    execution_times = []
    counter_execution = []
    for i in range(100):
        start_time = time.time()
        word_count = count_words_dict(text)
        end_time = time.time()
        word_counter = count_words_counter(text)
        end_time_counter = time.time()
        execution_times.append(end_time - start_time)
        execution_times.append(end_time_counter - end_time)
    
    mean_time = sum(execution_times) / len(execution_times)
    variance = sum((x - mean_time) ** 2 for x in execution_times) / len(execution_times)

    counter_mean_time = sum(execution_times) / len(execution_times)
    counter_variance = sum((x - counter_mean_time) ** 2 for x in execution_times) / len(execution_times)
    

    mean_param = {'type': 'line', 
                'data':{
                    'datasets':[
                        {'label': 'Mean using a dictionary', 
                        'data': [mean_time],
                        "backgroundColor": "red",
                        },
                        {'label': 'Mean using the Counter function', 
                        'data': [counter_mean_time],
                        "backgroundColor": "blue",
                        }
                    ]
                },
                'options': {
                    "title": {
                        "text": 'Mean'
                        },
                }
            }

    variance_param = {'type': 'line', 
                'data':{
                    'datasets':[
                        {'label': 'Variance using a dictionary', 
                        'data': [variance],
                        "backgroundColor": "red",
                        },
                        {'label': 'Variance using the Counter function', 
                        'data': [counter_variance],
                        "backgroundColor": "blue",
                        }
                    ]
                },
                'options': {
                    "title": {
                        "text": 'Variance'
                        },
                }
            }

    template = f"""  
        <html>
            <head>
                <title>Execution time</title>
            </head>
            <body>
                <h1>Execution time for two different methods</h1>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.5.0/Chart.min.js"></script>
                <div><canvas id="myChart" width="400" height="400"></canvas></div>
                <div><script>
                    var ctx = document.getElementById('My_Chart');
                    new Chart(ctx, {mean_param});
                </script></div>
                <div><script>
                    var ctx = document.getElementById('My_Chart');
                    new Chart(ctx, {variance_param});
                </script></div>
            </body>
        </html>
        """
    return template

if __name__=="__main__":
    app.run(debug=True)