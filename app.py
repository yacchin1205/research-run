import json
import os
import subprocess
from tempfile import NamedTemporaryFile
import yaml
import requests
import traceback
from requests.exceptions import ConnectionError
import time

from flask import Flask, request

app = Flask(__name__)

ports = {}

def find_kg_port(notebook):
    port_path = os.path.join(os.environ.get('NOTEBOOK_DIR', '.'), '.' + notebook + '.kg.port')
    if not os.path.exists(port_path):
        return None
    with open(port_path) as f:
        port = f.read()
    return int(port.strip())

@app.route('/notebooks/<notebook>', methods=['GET', 'POST'])
def generate(notebook=None):
    notebook_path = os.path.join(os.environ.get('NOTEBOOK_DIR', '.'), notebook + '.ipynb')
    app.logger.info('request %s, %r', request.method, request.form)
    if request.method == 'GET' or not os.path.exists(notebook_path):
        return { 'exists': os.path.exists(notebook_path) }
    config_file = NamedTemporaryFile(delete=False, mode='w', suffix='.yaml')
    config_file.write(yaml.dump(dict(request.form.items())))
    config_file.close()
    result = json.loads(subprocess.check_output(['papermill', '-f', config_file.name, notebook_path, '-']))
    os.unlink(config_file.name)
    return { 'exists': True, 'output': result }

@app.route('/kg/<notebook>/<path:path>', methods=['GET', 'POST'])
def proxy(notebook=None, path=None):
    if notebook not in ports:
        port = find_kg_port(notebook)
        ports[notebook] = port
    else:
        port = ports[notebook]
    if port is None:
        return { 'exists': False }
    url = 'http://localhost:{}/{}'.format(port, path)
    retries = 3
    resp = None
    sleep_sec = 3
    while retries > 0:
        try:
            if request.method == 'POST':
                resp = requests.post(url, json=request.get_json())
            else:
                resp = requests.get(url)
            break
        except ConnectionError:
            traceback.print_exc()
            print('Retrying... sleep', sleep_sec)
            time.sleep(sleep_sec)
            sleep_sec *= 2
            retries -= 1
    if resp is None:
        return 'Cannot connect kernels', 500
    resp.raise_for_status()
    return resp.json()

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
