import os
from flask import Flask, request, jsonify, render_template
import subprocess

app = Flask(__name__)


# Load the secret key from Render's environment variables
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

if not app.config['SECRET_KEY']:
    raise ValueError("SECRET_KEY is not set in the environment variables.")

# Serve the HTML form on the home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data received"}), 400

            key = app.config['SECRET_KEY']
            acl = data.get('acl')
            window_seconds = data.get('window_seconds')  # Extract variable 2

            # Debugging: Print received values
            print(f"Received key: {key}, acl: {acl}, window_seconds: {window_seconds}")

            result = subprocess.run(
                ['python', 'cms_edgeauth.py', "-k", key, "-a", acl, "-w", "500", "-s" "now"],  # Pass variables as arguments
                capture_output=True,
                text=True
            )
            print(result)
            return jsonify({"output": result.stdout, "error": result.stderr})
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return render_template('index.html')  # This renders the HTML form

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000, debug=True)
