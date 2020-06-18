import os

app_dir = '/app'
supervisor_dir = '/opt/run/conf.d/'

port = 30000
prespawn_count = int(os.environ.get('KG_PRESPAWN_COUNT', '1'))

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

command=jupyter kernelgateway --debug --KernelGatewayApp.api='kernel_gateway.notebook_http' --KernelGatewayApp.port={port} --KernelGatewayApp.seed_uri='{path}' --KernelGatewayApp.prespawn_count={prespawn_count}
        '''.format(filebody=filebody, port=port, prespawn_count=prespawn_count,
                   path=os.path.join(app_dir, notebook_filename)))
    with open(os.path.join(app_dir, '.{}.kg.port'.format(filebody)), 'w') as f:
        f.write('{}'.format(port))
    port += 1
