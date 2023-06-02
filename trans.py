import requests
import json

def get_transaction_data(legal_entity_id):
    """Gets the historical transaction data for the given legal entity ID."""
    url = "https://api.tpex.com.tw/v1/transaction/history?legalEntityId={}".format(legal_entity_id)
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.content)
        return data
    else:
        raise Exception("Error getting transaction data: {}".format(response.status_code))

def main():
    """Gets the historical transaction data for the three major legal entities of the TPEx."""
    legal_entity_ids = [1, 2, 3]
    for legal_entity_id in legal_entity_ids:
        data = get_transaction_data(legal_entity_id)
        print("Legal entity ID: {} | Transactions: {}".format(legal_entity_id, data["transactions"]))

if __name__ == "__main__":
    main()
