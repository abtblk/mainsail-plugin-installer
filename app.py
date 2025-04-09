from flask import Flask, render_template, request, jsonify
import subprocess
import os
import json

app = Flask(__name__)

with open("plugins.json", "r") as f:
    PLUGINS = json.load(f)

@app.route('/')
def index():
    return render_template('index.html', plugins=PLUGINS)

@app.route('/install', methods=['POST'])
def install():
    plugin_url = request.json['url']
    plugin_name = plugin_url.split("/")[-1].replace(".git", "")
    dest_path = os.path.expanduser(f"~/{plugin_name}")

    if os.path.exists(dest_path):
        return jsonify({"status": "already_installed"})

    try:
        subprocess.run(["git", "clone", plugin_url, dest_path], check=True)
        install_script = os.path.join(dest_path, "install.sh")
        if os.path.isfile(install_script):
            subprocess.run(["bash", install_script], check=True)
        return jsonify({"status": "installed"})
    except subprocess.CalledProcessError:
        return jsonify({"status": "error"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010)
