import re
import subprocess
from flask import Flask, request

app = Flask(__name__)

HOSTNAME_PATTERN = re.compile(r'^[a-zA-Z0-9]([a-zA-Z0-9\-\.]{0,253}[a-zA-Z0-9])?$')

@app.route('/ping')
def ping():
    hostname = request.args.get('hostname')
    
    if not hostname:
        return "<pre>Error: hostname parameter is required</pre>", 400
    
    if not HOSTNAME_PATTERN.match(hostname):
        return "<pre>Error: Invalid hostname format</pre>", 400
    
    try:
        result = subprocess.run(
            ['ping', '-c', '1', hostname],
            capture_output=True,
            text=True,
            timeout=10
        )
        response = result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        response = "Error: Ping request timed out"
    except Exception as e:
        response = f"Error: {str(e)}"
    
    return f"<pre>{response}</pre>"

if __name__ == '__main__':
    app.run(debug=True)
