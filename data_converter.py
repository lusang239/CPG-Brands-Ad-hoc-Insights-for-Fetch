from datetime import datetime

def brands_data_converter(list):
    result = []
    for line in list:
        dict = {}
        dict["id"] = line.get("_id").get("$oid")
        dict["barcode"] = line.get("barcode")
        dict["brandCode"] = line.get("brandCode")
        dict["category"] = line.get("category")
        dict["categoryCode"] = line.get("categoryCode")
        dict["name"] = line.get("name")
        dict["topBrand"] = line.get("topBrand")
        dict["cpg"] = line.get("cpg").get("$id").get("$oid")
        result.append(dict)
    return result


def receipts_data_converter(list):
    result = []
    for line in list:
        dict = {}
        dict["id"] = line.get("_id").get("$oid")
        dict["bonusPointsEarned"] = line.get("bonusPointsEarned")
        dict["bonusPointsEarnedReason"] = line.get("bonusPointsEarnedReason")
        dict["createDate"] = datetime.fromtimestamp(int(line.get("createDate").get("$date")) / 1000)
        dict["dateScanned"] = datetime.fromtimestamp(int(line.get("dateScanned").get("$date")) / 1000)
        dict["finishedDate"] = datetime.fromtimestamp(int(line.get("finishedDate").get("$date")) / 1000) if line.get("finishedDate") != None else None
        dict["modifyDate"] = datetime.fromtimestamp(int(line.get("modifyDate").get("$date")) / 1000)
        dict["pointsAwardedDate"] = datetime.fromtimestamp(int(line.get("pointsAwardedDate").get("$date")) / 1000) if line.get("pointsAwardedDate") != None else None
        dict["pointsEarned"] = line.get("pointsEarned")
        dict["purchaseDate"] = datetime.fromtimestamp(int(line.get("purchaseDate").get("$date"))/ 1000) if line.get("purchaseDate") != None else None
        dict["purchasedItemCount"] = line.get("purchasedItemCount")
        dict["rewardsReceiptStatus"] = line.get("rewardsReceiptStatus")
        dict["totalSpent"] = line.get("totalSpent")
        dict["userId"] = line.get("userId")
        result.append(dict)
    return result

def users_data_converter(list):
    result = []
    for line in list:
        dict = {}
        dict["id"] = line.get("_id").get("$oid")
        dict["state"] = line.get("state")
        dict["createdDate"] = datetime.fromtimestamp(int(line.get("createdDate").get("$date")) / 1000)
        dict["lastLogin"] = datetime.fromtimestamp(int(line.get("lastLogin").get("$date")) / 1000) if line.get("lastLogin") != None else None
        dict["role"] = line.get("role")
        dict["active"] = line.get("active")
        dict["signUpSource"] = line.get("signUpSource")
        result.append(dict)
    return result

def items_data_converter(list):
    results = []
    for line in list:
        if line.get("rewardsReceiptItemList"):
            for item in line.get("rewardsReceiptItemList"):
                dict = {}
                dict["receiptId"] = line.get("_id").get("$oid")
                dict["barcode"] = item.get("barcode")
                dict["brandCode"] = item.get("brandCode") if item.get("brandCode") != None else None
                dict["description"] = item.get("description")
                dict["discountedItemPrice"] = item.get("discountedItemPrice")
                dict["finalPrice"] = item.get("finalPrice")
                dict["itemPrice"] = item.get("itemPrice")
                dict["needsFetchReview"] = item.get("needsFetchReview")
                dict["partnerItemId"] = item.get("partnerItemId")
                dict["preventTargetGapPoints"] = item.get("preventTargetGapPoints")
                dict["quantityPurchased"] = item.get("quantityPurchased")
                results.append(dict)
    return results

def convert(type, data):
    match type:
        case "receipts":
            return receipts_data_converter(data)
        case "users":
            return users_data_converter(data)
        case "brands":
            return brands_data_converter(data)
        case "items":
            return items_data_converter(data)
