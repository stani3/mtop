from requests import get
from datetime import datetime
from decimal import Decimal
API_KEY = "XXGJPWPVY1QT7QIP7N21TWG2DI847YXQQF"
BASE_URL = "https://api-sepolia.etherscan.io/api"

# testnet usdt
USDT = '0x2e6bf640195b2E0A2e22D26Dd14bF9B25f88421a'
DECIMALS_USDT = 2
ETHER_VALUE = 10 ** 18


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
    response = get(balance_url)
    data = response.json()

    value = Decimal(data["result"]) / ETHER_VALUE
    return value


# always use with try
def get_token_balance(address, token):
    req = get_token_balance_req("account", "tokenbalance", token, address)
    data = get(req).json()
    return Decimal(data["result"]) / 10 ** DECIMALS_USDT


def get_token_transactions(address):
    transactions_url = get_token_balance_req("account", "tokentx", "0xD92E713d051C37EbB2561803a3b5FBAbc4962431",
                                             address, startblock=0, endblock=99999999, page=1, offset=10000,
                                             sort="asc")
    response = get(transactions_url)
    data = response.json()["result"]

    data.sort(key=lambda x: int(x['timeStamp']), reverse=True)
    # for tx in data:
    #     print(tx)
    current_balance = 0
    balances = []
    times = []
    value = 0
    time = None
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
    response = get(transactions_url)
    data = response.json()["result"]

    data.sort(key=lambda x: int(x['timeStamp']), reverse=True)
    # for tx in data:
    #     print(tx)
    current_balance = 0
    balances = []
    times = []
    value = 0
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

