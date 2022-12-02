from sqlalchemy import create_engine
from sqlalchemy import insert
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime
import datetime


class Repository:

    def __init__(self):
        self.engine = create_engine(
            "mysql+pymysql://root:@localhost:3306/fetch",
        )
        metadata_obj = MetaData()
        self.brands = Table(
            "brands",
            metadata_obj,
            Column("id", String, primary_key=True),
            Column("barcode", String),
            Column("brandCode", String),
            Column("category", String),
            Column("categoryCode", String),
            Column("name", String),
            Column("topBrand", String),
            Column("cpg", String)
        )

        self.receipts = Table(
            "receipts",
            metadata_obj,
            Column("id", String, primary_key=True),
            Column("bonusPointsEarned", String),
            Column("bonusPointsEarnedReason", String),
            Column("createDate", String),
            Column("dateScanned", String),
            Column("finishedDate", String),
            Column("modifyDate", String),
            Column("pointsAwardedDate", String),
            Column("pointsEarned", String),
            Column("purchaseDate", String),
            Column("purchasedItemCount", String),
            Column("rewardsReceiptStatus", String),
            Column("totalSpent", String),
            Column("userId", String)
        )

        self.users = Table(
            "users",
            metadata_obj,
            Column("id", String),
            Column("state", String),
            Column("createdDate", DateTime),
            Column("lastLogin", DateTime),
            Column("role", String),
            Column("active", String),
            Column("signUpSource", String)
        )

        self.items = Table(
            "items",
            metadata_obj,
            Column("receiptId", String),
            Column("barcode", String),
            Column("brandCode", String),
            Column("description", String),
            Column("discountedItemPrice", String),
            Column("finalPrice", String),
            Column("itemPrice", String),
            Column("needsFetchReview", String),
            Column("partnerItemId", String),
            Column("preventTargetGapPoints", String),
            Column("quantityPurchased", String)
        )

    def write_brands(self, data):
        stmt = insert(self.brands).values(id=data["id"], barcode=data["barcode"], brandCode=data["brandCode"],
                                          category=data["category"],
                                          categoryCode=data["categoryCode"], name=data["name"],
                                          topBrand=data["topBrand"], cpg=data["cpg"])
        result = self.engine.execute(stmt)

    def write_receipts(self, data):
        stmt = insert(self.receipts).values(id=data["id"], bonusPointsEarned=data["bonusPointsEarned"],
                                            bonusPointsEarnedReason=data["bonusPointsEarnedReason"],
                                            createDate=data["createDate"], dateScanned=data["dateScanned"],
                                            finishedDate=data["finishedDate"], modifyDate=data["modifyDate"],
                                            pointsAwardedDate=data["pointsAwardedDate"],
                                            pointsEarned=data["pointsEarned"], purchaseDate=data["purchaseDate"],
                                            purchasedItemCount=data["purchasedItemCount"],
                                            rewardsReceiptStatus=data["rewardsReceiptStatus"],
                                            totalSpent=data["totalSpent"], userId=data["userId"])

        result = self.engine.execute(stmt)

    def write_users(self, data):
        stmt = insert(self.users).values(id=data["id"], state=data["state"], createdDate=data["createdDate"],
                                         finalPrice=data["finalPrice"],
                                         role=data["role"], active=data["active"],
                                         signUpSource=data["signUpSource"])

        result = self.engine.execute(stmt)

    def write_items(self, data):
        stmt = insert(self.items).values(receiptId=data["receiptId"], barcode=data["barcode"],
                                         brandCode=data["brandCode"], description=data["description"],
                                         discountedItemPrice=data["discountedItemPrice"],
                                         finalPrice=data["finalPrice"], itemPrice=data["itemPrice"],
                                         needsFetchReview=data["needsFetchReview"],
                                         partnerItemId=data["partnerItemId"],
                                         preventTargetGapPoints=data["preventTargetGapPoints"],
                                         quantityPurchased=data["quantityPurchased"])

        result = self.engine.execute(stmt)
