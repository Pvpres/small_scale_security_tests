import subprocess
import re
from flask import Flask, request

app = Flask(__name__)

@app.route('/ping')
def ping():
    hostname = request.args.get('hostname')
    
    if not hostname:
        return "<pre>Error: hostname parameter is required</pre>", 400
    
    hostname_pattern = re.compile(
        r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z0-9-]{1,63})*$|'
        r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    )
    
    if not hostname_pattern.match(hostname):
        return "<pre>Error: Invalid hostname format</pre>", 400
    
    try:
        result = subprocess.run(
            ["ping", "-c", "1", hostname],
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
