import os

from resources import _read_parameters_store

param_names = ['POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_HOST', 'POSTGRES_PORT', 'POSTGRES_DB']
param_store_names = {
    'prod': 'sfigiel-prod-db-cred',
    'dev': 'sfigiel-dev-db-cred',
    'docker': 'sfigiel-docker-db-cred',
}

with open("database.conf", "w+") as file:
    param_store_name = param_store_names[os.environ['FLASK_ENV']]
    param_store = _read_parameters_store(param_store_name, True)
    if param_store:
        for name, value in zip(param_names, param_store):
            file.write(f'{name}={value}\n')
        print(f'database.conf file created')
