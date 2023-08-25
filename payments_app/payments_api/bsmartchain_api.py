from requests import get
from datetime import datetime
from decimal import Decimal
API_KEY = "BU6CA1GEXCTTJJAEURG5UIHRITW78JTTBW"
BASE_URL = "https://api-testnet.bscscan.com/api"

# testnet usdt
USDT = '0x8E17b1E557844611De2872e9A5065449e60c072f'
DECIMALS_USDT = 18
ETHER_VALUE = 10 ** 18

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    "Upgrade-Insecure-Requests": "1", "DNT": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}

def make_api_url(module, action, address, **kwargs):
    url = BASE_URL + f"?module={module}&action={action}&address={address}&apikey={API_KEY}"

    for key, value in kwargs.items():
        url += f"&{key}={value}"

    return url


def get_token_balance_req(module, action, contractaddress, address, **kwargs):
    url = BASE_URL + f"?module={module}&action={action}&contractaddress={contractaddress}&address={address}&tag=latest&apikey={API_KEY}"

    for key, value in kwargs.items():
        url += f"&{key}={value}"

    return url


def get_account_balance(address):
    balance_url = make_api_url("account", "balance", address, tag="latest")

    response = get(balance_url, headers=headers)
    data = response.json()
    value = Decimal(data["result"]) / ETHER_VALUE
    return value


# always use with try
def get_token_balance(address, token):
    req = get_token_balance_req("account", "tokenbalance", token, address)
    data = get(req, headers=headers).json()
    return Decimal(data["result"]) / 10 ** DECIMALS_USDT


def get_token_transactions(address):
    transactions_url = get_token_balance_req("account", "tokentx", USDT,
                                             address, startblock=0, endblock=99999999, page=1, offset=10000,
                                             sort="asc")
    response = get(transactions_url, headers=headers)
    data = response.json()["result"]

    data.sort(key=lambda x: int(x['timeStamp']), reverse=True)
    # for tx in data:
    #     print(tx)
    current_balance = 0
    balances = []
    times = []

    for tx in data:
        to = tx["to"]
        from_addr = tx["from"]
        value = int(tx["value"]) / 10 ** DECIMALS_USDT

        time = datetime.fromtimestamp(int(tx['timeStamp']))
        # print("-------")
        # print("To:", to)
        # print("From: ", from_addr)
        # print("Value: ", value)
        # print("Time: ", time)

    current_balance += value

    balances.append(current_balance)
    times.append(time)


# ethereum transactions
def get_transactions(address):
    transactions_url = make_api_url("account", "txlist", address, startblock=0, endblock=99999999, page=1, offset=10000,
                                    sort="asc")
    response = get(transactions_url, headers=headers)
    data = response.json()["result"]

    data.sort(key=lambda x: int(x['timeStamp']), reverse=True)
    # for tx in data:
    #     print(tx)
    current_balance = 0
    balances = []
    times = []

    for tx in data:
        to = tx["to"]
        from_addr = tx["from"]
        value = int(tx["value"]) / ETHER_VALUE

        if "gasPrice" in tx:
            gas = int(tx["gasUsed"]) * int(tx["gasPrice"]) / ETHER_VALUE
        else:
            gas = int(tx["gasUsed"]) / ETHER_VALUE

        time = datetime.fromtimestamp(int(tx['timeStamp']))
        money_in = to.lower() == address.lower()
        # print("-------")
        # print("To:", to)
        # print("From: ", from_addr)
        # print("Value: ", value)
        # print("Time: ", time)

    if money_in:
        current_balance += value
    else:
        current_balance -= value + gas

    balances.append(current_balance)
    times.append(time)

#print(get_token_balance("0x4407440F86FBd1FE351639C37A1E9C64bA722731", USDT))

