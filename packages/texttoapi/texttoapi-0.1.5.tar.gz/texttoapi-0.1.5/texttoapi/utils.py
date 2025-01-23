import json
import os
from . import env


# Configure the logger
logger = env.getLogger(os.path.basename(__file__))

def removeKeyFromList(data, key):
    return list(filter(lambda x: x.pop(key, None) or True, data))

def removeKeysFromList(data, keys):
    for key in keys:
       data = removeKeyFromList(data, key)
    return data

def removeKeyFromDict(data, key):
    return data.pop(key, None)

def removeKeysFromDict(data, keys):
    for key in keys:
        removeKeyFromDict(data, key)
    return data

def checkDataLimitAndRemoveKeys(data, keys):
    if json.dumps(data).__sizeof__() > env.data_limit:
        logger.info(f"Data size exceeds limit of {env.data_limit} bytes. Removing keys {keys} from data.")
        if isinstance(data, list):
            removeKeysFromList(data, keys)
        if isinstance(data, dict):
            removeKeysFromDict(data, keys)
    return data
