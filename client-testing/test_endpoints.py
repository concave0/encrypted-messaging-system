import requests as r 
import json
import time 

token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZXN0aW5nIjoiQWNjb3VudCBjcmVhdGVkIG9uOiAyMDI0LTAzLTEzIDAzOjA2OjI5LjE1MTYyNSJ9.eAya9ONuYTHBLySZvGZF2-mAYJN35MTBx2MgppEQkeGccrdGLqkyVhr0g8BpiOLCw3MzXSF5MAFVp-p6onjBnUySl6_KjgNSfsp4FNVHYTSDtHYsD7iSq53nNXzlHBEMuUtK5IHUs4_4dyS3EQfSqVixEOQVHCt7W27SjAMZ959RRN_820TKtZ6nUZrvAVUADqN3pgXTzkqMQk1gScCQHB7-UncnzPSHF0EjX3CP-Ids7lZLKy7qspkEWAXUtIO_otPlNfhKp4Te5YtaHyg_tbxLCvpSvHDXKT2Rpb6tdR_To2ZUhx_RpvTNh76PbvVzH5gBRr88g1FiGXuNN8qs3aiJFzfo3e6qAl4TTmUX2h0gxTKJzqVvsRVWnuyEqqFf1YlocIAAiTaqryY4FFNQdUYstzhmbxEFuPf6vko01mc9PtsJXW2lnFxZQwQCxWSjZtev9Wh5pOlwirun2ea_8SxPLPivj6SNRAV3Wlqj9u-ygJORSOm0oo_C3r8lg8Jtuda1XmH9dvDjyhHXVaXq7eIcx7v0rQWt0R_S1C-Z-aMVZTwgLU3AUne--EviqK1SlwKpEEFgX99DhAX3NkPV2abxG9R6EzFFhI44__A1S05gXMXHXMOP1zV833L93xaIoUj4ptheFWDwyMz7PMPg-ctzLs5FJi41VMDdn7i8HEg"
testing_message_server_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZXN0aW5nX21lc3NhZ2Vfc2VydmVyIjoiQWNjb3VudCBjcmVhdGVkIG9uOiAyMDI0LTAzLTEzIDAzOjA3OjE0LjQ2NDEyNCJ9.QmZOp4Lp-_sgtXHJDNxIqMZ1MnHtc4mRCnKINp66FKXv9TloXDhVQVS-asctPkqHpSVoXdSgxtBvjaR2MvW1RQGFC8CHT81ui9CfPxSH9PHwc6JsOIbOpW2XxXuQJrJZ9g526RS4zs8kgli6Wj9TT2lNqJgwoAcl6BgDls6deHXzmeZA_wbkpKZC2IGfpSizNs2moS5YycQYe2UiXbdLChfcPQCpfdE02WlFtMTZ8V5utH_q-QVkTLOIXMo6cHTB9Hzu_gPtP3BlZ91tcpXu_S-w4jWztOxjKV6rr3VJmRGPgZ8fyp-XNLbAZZf7bMcHt4YkhmpKeyS2QUI9ONeUyJIHFi2xI6zmmbdN-3TSmLZvs-ILYBbtLzap_tzriuwzSLH2X-_H1fytOn5ReyBKHIV2WOcAl7cbmrxopV-pUfn1KL9FP-oKDEx6bjP_YfQgw80-fBAp7z-Lt7Mwb6DB1Xx746WD83PB3lM6CylnSSeoSXu3uMDDpfRc66RFS5U9E-v_ukulEX1eKsKj7oYd3OBvJLnoaQQhZmplU1jWRmJuPWWWCH4XBmim-t4AQ4uptzWdbAcYMeBArvND4fvYp93TiY_SOqFtrz_7Fvca2wQPVe_XJKHtSKwhBorUEisJhcPz5jeKPICCXwbZGJ5vHFCisY3ikGx4uPXKu64LA28"

headers = {
    "User" : "testing", 
    "Password" : "testing",
    "Authorization": token
}

headers_messaging = {
    "User" : "testing", 
    "Password": "testing", 
    "Token": token, 
    "TO": "testing_message_server", 
    "FROM": "testing", 
    "MESSAGE": "testing", 
}

headers_test_fetch_mail = {
    "User" : "testing_message_server", 
    "Password": "testing", 
    "Token": testing_message_server_token,
}

headers_testing_message_server = {
    "User" : "testing_message_server", 
    "Password": "testing", 
    "Token": testing_message_server_token,
}

headers_test_sync_mail =  {
    "User" : "testing_message_server", 
    "Password": "testing", 
    "Token": testing_message_server_token,
}

headers_test_test_user = {
    "User" : "testing", 
    "Password" : "testing",
    "Token": token
}

def test_fetch_mail(headers_maio:dict, url): 
    response = r.get(url,headers=headers_messaging)
    return response.text 
    
def test_messaging(headers_messaging:dict, url:str): 
    response = r.get(url,headers=headers_messaging)
    return response.text 


def test_authorize(headers: dict, url:str): 
    response = r.get(url,headers=headers)
    return response.text


def test_sync_mail(url): 
    response = r.get(url)
    return response.text

def test_add_users_batch_check_update(header:dict,url:str): 
    response = r.get(url, headers = header)
    return response.text
    
url_authorized =  "http://127.0.0.1:8000/authorize"
url_message = "http://127.0.0.1:8000/rerouting-message-to-designation"
url_fetch_mail = "http://127.0.0.1:8000/fetch-mailbox/testing_message_server"
sync_mail = "http://192.168.68.55:5000/sync-mail"
add_users_for_cache_url = "http://192.168.68.55:5000/users-to-cache"

""" Testing messaging services"""
# print(test_messaging(headers_messaging, url_message))
# print(test_fetch_mail(testing_message_server_token, url_fetch_mail))

""" Setting up config for messaging systems cache"""
print(test_add_users_batch_check_update(header=headers_testing_message_server, url=add_users_for_cache_url))
time.sleep(2)
print(test_add_users_batch_check_update(header=headers_test_test_user, url=add_users_for_cache_url))
time.sleep(2)

""" Testing the sync mail function"""
print(test_sync_mail(url = sync_mail))
