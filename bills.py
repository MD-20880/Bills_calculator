import requests
import secret
import json
from pprint import pprint
import copy


def getDB():
    url = "https://api.notion.com/v1/databases/"+secret.database_id

    headers = {
        "Authorization": f"{secret.token}",
        "accept": "application/json",
        "Notion-Version": "2022-06-28"
    }

    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    # response.text
    pprint(data)
    print("END OF THE TASK")


def queryDB():


    url = f"https://api.notion.com/v1/databases/{secret.database_id}/query"

    payload = {"page_size": 100}
    headers = {
        "Authorization": f"{secret.token}",
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    return json.loads(response.text)



def getAmount(transaction) -> int:

    return transaction["properties"]["Amount"]['number']

def getBuyer(transaction) -> str:
    pay = transaction["properties"]["付款人"]["people"]
    if len(pay) == 0:
        return "NO BUYER"
    return pay[0]["name"]


def getMembers(transaction) -> list[str]:
    consumers = transaction["properties"]["参与者"]["people"]
    result = []
    for p in consumers:
        result.append(p["name"])
    return result

# The resultDict contains the value in resultDict[person1][person2] means person1 should pay person2 resultDict[From][To]
resultDict = {}
data = queryDB()
total = 0
# print(len(data["results"]))
for t in data["results"]:
    amount = getAmount(t)
    pay = getBuyer(t)
    consumers = getMembers(t)
    participants = set(consumers)
    participants.add(pay)

    if amount is not None:
        total += amount
        split = amount/(len(participants))
        # print( f"{pay} 付款 {amount}")
        for c in consumers:
            if c == pay:
                continue
            # print(f"{c} 付款 {split} 给 {pay}")
            if resultDict.get(c) is not None:
                if resultDict[c].get(pay) is None:
                    resultDict[c][pay] = split
                else:
                    resultDict[c][pay] += split
            else:
                resultDict[c] = {pay:split}       
    
intertransaction = copy.deepcopy(resultDict)
for p1 in resultDict.keys():
    if p1 == "伯涵 刘" or p1 == "NO BUYER":
        continue
    for p2 in resultDict[p1].keys():
        if p2 == "NO BUYER":
            continue
        intertransaction[p1][p2] = resultDict[p1][p2] - resultDict[p2][p1]



pprint(intertransaction)
pprint(total)