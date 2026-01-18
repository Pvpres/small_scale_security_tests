import os
from flask import Flask, request

app = Flask(__name__)

@app.route('/ping')
def ping():
    # EXTREMELY VULNERABLE: User input is passed directly to the shell
    hostname = request.args.get('hostname')
    response = os.popen(f"ping -c 1 {hostname}").read()
    return f"<pre>{response}</pre>"

if __name__ == '__main__':
    app.run(debug=True)
