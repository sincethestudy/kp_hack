import os
import json
from datetime import datetime


LOG_DIR = 'logs' # TBD
os.makedirs(LOG_DIR, exist_ok=True)


def log_messages(messages):
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
    save_path = os.path.join(LOG_DIR, timestamp + '.json')
    with open(save_path, 'w') as f:
        json.dump(messages, f, indent=4)