from flask import Flask, render_template
import logging
import requests

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