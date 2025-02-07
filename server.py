from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run-script', methods=['POST'])
def run_script():
    # Example of running a Python script
    result = subprocess.run(['python cms_edgeauth.py'], capture_output=True, text=True)
    return jsonify({"output": result.stdout, "error": result.stderr})

if __name__ == '__main__':
    app.run(debug=True)
