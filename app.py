import json
import os
import subprocess
from tempfile import NamedTemporaryFile
import yaml

from flask import Flask, request

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
