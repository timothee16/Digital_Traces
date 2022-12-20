from flask import Flask
import logging

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

@app.route('/logger', methods=["GET"])
def logger():
    script = """
    <script> console.log("logger") </script>"""
    return "There is the logger" + script