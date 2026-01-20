import os
from flask import Flask, request

app = Flask(__name__)

@app.route('/ping')
def ping():
    # EXTREMELY VULNERABLE: User input is passed directly to the shell
    # SECURITY ISSUE #1 (HIGH): Missing Input Validation
    # The hostname parameter is retrieved without any validation.
    # It could be None, empty, or contain malicious characters.
    # Remediation: Validate hostname format using regex or a validation library.
    hostname = request.args.get('hostname')
    # SECURITY ISSUE #2 (CRITICAL): Command Injection Vulnerability
    # User input is directly interpolated into a shell command via os.popen().
    # An attacker can execute arbitrary commands by injecting shell metacharacters.
    # Example attack: ?hostname=example.com;cat /etc/passwd
    # Remediation: Use subprocess.run() with shell=False and pass arguments as a list,
    # or use shlex.quote() to escape the input, or validate input against a whitelist.
    response = os.popen(f"ping -c 1 {hostname}").read()
    # SECURITY ISSUE #3 (LOW): Potential Cross-Site Scripting (XSS)
    # The response is embedded directly into HTML without escaping.
    # If an attacker controls the output (via command injection), they could inject JavaScript.
    # Remediation: Use proper HTML escaping (e.g., markupsafe.escape or flask.escape).
    return f"<pre>{response}</pre>"

if __name__ == '__main__':
    # SECURITY ISSUE #4 (MEDIUM): Debug Mode Enabled
    # Running Flask with debug=True in production exposes:
    # - Interactive debugger that can execute arbitrary Python code
    # - Detailed error messages with stack traces revealing internal code
    # - Auto-reload functionality
    # Remediation: Set debug=False or use environment variable to control (e.g., os.environ.get('FLASK_DEBUG', False))
    app.run(debug=True)
