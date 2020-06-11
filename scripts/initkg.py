import os

app_dir = '/app'
supervisor_dir = '/opt/run/conf.d/'

port = 30000

for notebook_filename in os.listdir(app_dir):
    if not notebook_filename.endswith('.kg.ipynb'):
        continue
    print('Preparing...', notebook_filename)
    filebody = notebook_filename[:-9]
    with open(os.path.join(supervisor_dir, '{}.conf'.format(filebody)), 'w') as f:
        f.write('''[program:{filebody}]
stdout_logfile = /dev/stdout
stdout_logfile_maxbytes = 0
stderr_logfile = /dev/stderr
stderr_logfile_maxbytes = 0

command=jupyter kernelgateway --KernelGatewayApp.api='kernel_gateway.notebook_http' --KernelGatewayApp.port={port} --KernelGatewayApp.seed_uri='{path}' --KernelGatewayApp.prespawn_count=5
        '''.format(filebody=filebody, port=port, path=os.path.join(app_dir, notebook_filename)))
    with open(os.path.join(app_dir, '.{}.kg.port'.format(filebody)), 'w') as f:
        f.write('{}'.format(port))
    port += 1
