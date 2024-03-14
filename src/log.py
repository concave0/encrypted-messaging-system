import datetime 
import json 

def log_ip(endpoint, status_code,ip_address): 
    record_ip = {}
    foriegn_key = {}
    now = datetime.datetime.now()
    record_ip["endpoint"] = str(endpoint)
    record_ip["status_code"] = str(status_code)
    record_ip["remote address"] = str(ip_address)

    foriegn_key[f"time stamp {str(now)}"] = record_ip

    with open("data/logs/ip_record.json",'r+') as log:
        file_data = json.load(log)
        file_data.update(foriegn_key)
        log.seek(0)
        new_data = json.dump(file_data, log, indent = 4)
    return new_data
