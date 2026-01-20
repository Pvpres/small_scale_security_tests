import re
import subprocess
from flask import Flask, request

app = Flask(__name__)

def is_valid_hostname(hostname):
    if not hostname:
        return False
    if len(hostname) > 253:
        return False
    hostname_regex = re.compile(
        r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z0-9-]{1,63})*\.?$|'
        r'^(\d{1,3}\.){3}\d{1,3}$'
    )
    return hostname_regex.match(hostname) is not None

@app.route('/ping')
def ping():
    hostname = request.args.get('hostname')
    if not is_valid_hostname(hostname):
        return "<pre>Error: Invalid hostname provided</pre>", 400
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
