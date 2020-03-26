import requests
import json
import time
import os
import threading
from flask import Flask
from prometheus_client import Info, Gauge, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

# Create Flask app
app = Flask(__name__)

# Create Prometheus Metrics
NEXTCLOUD_VERSION = Info('nextcloud_version_info', 'The current version of the Nextcloud installation')
MEMORY_TOTAL = Gauge('nextcloud_memory_total_kibibytes', 'The total memory of the Nextcloud installation')
MEMORY_FREE = Gauge('nextcloud_memory_free_kibibytes', 'The free memory of the Nextcloud installation')
SWAP_TOTAL = Gauge('nextcloud_swap_total_kibibytes', 'The total swap of the Nextcloud installation')
SWAP_FREE = Gauge('nextcloud_swap_free_kibibytes', 'The free swap of the Nextcloud installation')
APPS_UPDATES_AVAILABLE = Gauge('nextcloud_app_updates_available_total', 'The number of apps which have updates available')
DATABASE_SIZE = Gauge('nextcloud_db_size_bytes', 'The size of the Nextcloud database')
ACTIVE_USERS = Gauge('nextcloud_active_users_1h_total', 'The active Nextcloud users 1h')
CPU_LOAD = Gauge('nextcloud_cpu_load_total', 'The Nextcloud CPU load')
FREE_DISK_SPACE = Gauge('nextcloud_free_space_bytes', 'The free Nextcloud disk space')
NUM_SHARES = Gauge('nextcloud_shares_total', 'The number of all Nextcloud shares')

# Pull data from nextcloud
def get_nextcloud_data():
    response = requests.get(os.getenv('NC_URL'), auth=(os.getenv('NC_USER'), os.getenv('NC_PASS')))
    data = response.json()
    return data['ocs']['data']

# Update Prometheus data
def update_prometheus_data():
    while(True):
        nc_data = get_nextcloud_data()

        NEXTCLOUD_VERSION.info({'version': nc_data['nextcloud']['system']['version']})
        MEMORY_TOTAL.set(nc_data['nextcloud']['system']['mem_total'])
        MEMORY_FREE.set(nc_data['nextcloud']['system']['mem_free'])
        SWAP_TOTAL.set(nc_data['nextcloud']['system']['swap_total'])
        SWAP_FREE.set(nc_data['nextcloud']['system']['swap_free'])
        APPS_UPDATES_AVAILABLE.set(nc_data['nextcloud']['system']['apps']['num_updates_available'])
        DATABASE_SIZE.set(nc_data['server']['database']['size'])
        ACTIVE_USERS.set(nc_data['activeUsers']['last1hour'])
        CPU_LOAD.set(nc_data['nextcloud']['system']['cpuload'][0])
        FREE_DISK_SPACE.set(nc_data['nextcloud']['system']['freespace'])
        NUM_SHARES.set(nc_data['nextcloud']['shares']['num_shares'])

        time.sleep(5) 

# Create the wsgi app
app_dispatch = DispatcherMiddleware(app, {
    '/metrics': make_wsgi_app()
})

version_updater = threading.Thread(target=update_prometheus_data)
version_updater.start()

