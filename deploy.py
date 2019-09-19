import os
import subprocess
import time

flask_env = os.environ.get('FLASK_ENV', False)
subprocess.run('pip --version')
subprocess.run('pipenv --version')

subprocess.run('pipenv shell')
if flask_env:
    subprocess.run('pipenv shell')
    subprocess.run('pipenv install -r requirements.txt')
    # subprocess.run('python deploy.py')

    subprocess.run('python gen_creds_for_db.py')
    subprocess.run('docker-compose down')

    if flask_env == 'docker':
        subprocess.run('docker-compose -f docker-compose-docker.yml up -d --force-recreate')
    elif flask_env == 'dev':
        subprocess.run('docker-compose up -d --force-recreate --remove-orphans')
        print('sleeping 3 sec')
        time.sleep(3)
        subprocess.run('python app.py')
    else:
        subprocess.run('docker-compose up -d')
        print('sleeping 3 sec')
        time.sleep(3)
        subprocess.run('python app.py')
else:
    raise KeyError('FLASK_ENV has not been set up :( ')