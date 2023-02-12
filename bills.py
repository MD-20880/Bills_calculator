import requests
import secret
import json
from pprint import pprint
import copy
import datetime




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


def queryDB() -> list:


    url = f"https://api.notion.com/v1/databases/{secret.database_id}/query"

    payload = { 
        "page_size": 1000,
        }
    headers = {
        "Authorization": f"{secret.token}",
        "accept": "application/json",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json",
       
    }

    response = requests.post(url, json=payload, headers=headers)
    result = json.loads(response.text)
    finalresult = [result]
    
    
    while result["has_more"] == True:
        payload["start_cursor"] = result["next_cursor"]
        response = requests.post(url,json=payload,headers=headers)
        result =json.loads(response.text)
        finalresult.append(result)
    
    return finalresult



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

def getDate(transaction) -> str:
    date = "None"
    try:   
        date = transaction["properties"]["Date"]["date"]["start"]
    except:
        pass
    
    return date

def getCategory(transaction) -> str:
    result = "None"
    try:
        result = transaction["properties"]["Category"]["multi_select"][0]["name"]
    except:
        pass
    
    return result 
    
def testGet():
    data = queryDB()
    for d in data:
        for t in d["results"]:
            getCategory(t)


def checkInRange(transaction) -> bool:
    pass 

def calculate():
    index = 0
    # The resultDict contains the value in resultDict[person1][person2] means person1 should pay person2 resultDict[From][To]
    resultDict = {}
    spendingDict ={}
    data = queryDB()
    total = 0
    rangeTotal = 0
    rangeIndex = 0
    # print(len(data["results"]))
    categoryTotal = {}
    for d in data:
        for t in d["results"]:
            
            #Try Get Date, Else None
            try:
                date = getDate(t)
            except:
                pprint(t)
                exit()
            
            #Get Amount of money for this transaction
            amount = getAmount(t)
            pay = getBuyer(t)
            consumers = getMembers(t)
            category = getCategory(t)
            participants = set(consumers)
            participants.add(pay)

            print(f"__________transaction {index}____________")
            if amount is not None:
                
                
                
                #Global Statistics
                #Total Amount ( For Double checking program correctness)
                total += amount
                
                #Check TransAction In Date Range
                if date == "None" or datetime.datetime.fromisoformat(date) < datetime.datetime.fromisoformat("2022-11-20"):
                    print(f"date {date} is before 2022-11-20. PASS")
                    continue
                
                #Range Statistics
                
                #Number Of Transactions in range ( For Mean Value Calculation )
                rangeIndex += 1
                
                #Range Total Amount ( For Double checking program correctness)
                rangeTotal += amount
                
                #Category Sum
                try:
                    categoryTotal[category] += amount
                except:
                    categoryTotal[category] = amount
                    
                    
                    
                    
                    
                split = amount/(len(participants))
                for c in participants:
                    try:
                        spendingDict[c] += split
                    except:
                        spendingDict[c] = split
                print( f"{pay} 付款 {amount}")
                for c in consumers:
                    if c == pay:
                        continue
                    print(f"{c} 付款 {split} 给 {pay}")
                    if resultDict.get(c) is not None:
                        if resultDict[c].get(pay) is None:
                            resultDict[c][pay] = split
                        else:
                            resultDict[c][pay] += split
                    else:
                        resultDict[c] = {pay:split}  
                    
            
            print(f"__________transaction {index} END____________\n\n\n")     
            index += 1
        
        
    #Calculate Intertransaction
    intertransaction = copy.deepcopy(resultDict)
    for p1 in resultDict.keys():
        if p1 == "伯涵 刘" or p1 == "NO BUYER":
            continue
        for p2 in resultDict[p1].keys():
            if p2 == "NO BUYER":
                continue
            intertransaction[p1][p2] = resultDict[p1][p2] - resultDict[p2][p1]





    #Print Statistics
    pprint(intertransaction)
    
    print ("STATISTICS: \n")
    pprint(f"MONEY FROM ENTIRE DB : {total}")
    print("")
    pprint(f"MONEY FROM RANGE: {rangeTotal}")
    print("")
    pprint(categoryTotal)
    print("")
    pprint(spendingDict)
    
    
if __name__ == "__main__":
    calculate()