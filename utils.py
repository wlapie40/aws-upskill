# import sys
# import threading
import os

from resources import _read_parameters_store

param_names = ['POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_HOST', 'POSTGRES_PORT', 'POSTGRES_DB']
with open("database.conf", "w+") as file:
    print(f'current FLASK_ENV value : {os.environ["FLASK_ENV"]} !!!')
    if os.environ['FLASK_ENV'] == 'prod':
        param_store = _read_parameters_store('sfigiel-prod-db-cred', True)
    elif os.environ['FLASK_ENV'] == 'dev':
        param_store = _read_parameters_store('sfigiel-dev-db-cred', True)
    elif os.environ['FLASK_ENV'] == 'docker':
        param_store = _read_parameters_store('sfigiel-docker-db-cred', True)

    for name, value in zip(param_names, param_store):
        file.write(f'{name}={value}\n')


# class ProgressPercentage(object):
#
#     def __init__(self, filename):
#         self._filename = filename
#         self._size = float(os.path.getsize(filename))
#         self._seen_so_far = 0
#         self._lock = threading.Lock()
#
#     def __call__(self, bytes_amount):
#         # To simplify, assume this is hooked up to a single filename
#         with self._lock:
#             self._seen_so_far += bytes_amount
#             percentage = (self._seen_so_far / self._size) * 100
#             sys.stdout.write(
#                 "\r%s  %s / %s  (%.2f%%)" % (
#                     self._filename, self._seen_so_far, self._size,
#                     percentage))
#             sys.stdout.flush()
