import requests,json
def get_if_None(obj,fallBack):
    return obj if obj != None else fallBack
def get_rpc_payload(method,params=None,id=None,jsonrpc=None):
    if method == None:
        return None
    params=get_if_None(params,[])
    rpc_id=int(get_if_None(id,1))
    jsonrpc=str(get_if_None(jsonrpc,"2.0"))
    return {
            "jsonrpc": jsonrpc,
            "id": rpc_id,
            "method": method,
            "params": params
        }
def get_result(response):
    try:
        response = response.json()
        result = response.get('result',response)
    except:
        result = response.text
    return result
def make_rpc_call(method, params=[]):
    url = 'https://rpc.ankr.com/solana/c3b7fd92e298d5682b6ef095eaa4e92160989a713f5ee9ac2693b4da8ff5a370'
    headers = {'Content-Type': 'application/json'}
    payload = get_rpc_payload(method=method, params=params)
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    return response
def get_transaction(signature):
    transaction=None
    method='getTransaction'
    params=[signature,{"maxSupportedTransactionVersion": 0}]
    while True:
        response = make_rpc_call(method=method,params=params)
        transaction = get_result(response)
        if transaction:
            break
    return transaction
def get_signatures(address, until=None, limit=1000):
    method = 'getSignaturesForAddress'
    params = [address, {"limit": limit}]
    response = make_rpc_call(method=method,params=params)
    return get_result(response)
async def async_get_signatures(address, until=None, limit=1000):
    method = 'getSignaturesForAddress'
    params = [address, {"limit": limit}]
    response = make_rpc_call(method=method,params=params)
    return get_result(response)
