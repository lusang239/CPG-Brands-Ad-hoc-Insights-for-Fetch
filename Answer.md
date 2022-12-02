## Second Part: SQL

### Q1 : what are the top 5 brands by receipts scanned for most recent month?

**Answer** : BRAND, MISSION, and VIVA.

```sql
-- Find scanned receipts' ids for the most recent month from 2021-02-01 (included) to 2021-03-01 (included)
with MostRecentScannedReceipts AS (select id
                                   from receipts
                                   where dateScanned between "2021-02-01" and "2021-03-01"),

-- brandCode of items listed on the receipts
     itemsList AS (select brandCode
                   from items
                   where receiptId in (select id from MostRecentScannedReceipts)
                     and brandCode is not null)

select brandCode, count(*) as Numbers
from itemsList
group by 1
order by 2 desc
limit 5;
```

### Q2: How does the ranking of the top 5 brands by receipts scanned for the recent month compare to the ranking for the previous month?

**Answer**: HY-VEE, BEN AND JERRYS, PEPSI, KROGER, and KLEENEX

```sql
-- Find scanned receipts' ids for the previous month from 2021-01-01 (included) to 2021-01-30 (included)
with PreviousMonthScannedReceipts AS (select id
                                      from receipts
                                      where dateScanned between "2021-01-01" and "2021-01-30"),

-- brandCode of items listed on the receipts
     itemsList AS (select brandCode
                   from items
                   where receiptId in (select id from PreviousMonthScannedReceipts)
                     and brandCode is not null)

select brandCode, count(*) as Numbers
from itemsList
group by 1
order by 2 desc
limit 5;
```

### Q3: When considering average spend from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?

**Answer** : average spend of "Accepted" is greater than the "Rejected".

```sql
select round(avg(case when rewardsReceiptStatus = "FINISHED" then totalSpent end), 2) as average_spend_accepted,
       round(avg(case when rewardsReceiptStatus = "REJECTED" then totalSpent end), 2) as average_spend_rejected
from receipts;
```

### Q4: When considering total number of items purchased from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?

**Answer**: total number of items purchased from receipts with 'Accepted' is greater than the 'Rejected'.

```sql
select sum(case when rewardsReceiptStatus = "FINISHED" then purchasedItemCount end) as total_items_accepted,
       sum(case when rewardsReceiptStatus = "REJECTED" then purchasedItemCount end) as total_items_rejected
from receipts;
```

### Q5: Which brand has the most spend among users who were created within the past 6 months?

**Answer**: HEMPLER'S has the most spend among users who were created within the past 6 months.

```sql
-- Find the users who created within the past 6 months from 2020-09-01 to 2021-03-01
with newRegisteredUsers as (select id, min(createdDate) as earlist_createdDate
                            from users
                            group by 1
                            having earlist_createdDate between "2020-09-01" and "2021-03-01"),

-- Find the receipts scanned by those users' Id
     receiptsOfUsers as (select id
                  from receipts
                  where userId in (select id from newRegisteredUsers))

-- brandCode of items listed on the receipts
select brandCode, sum(finalPrice*quantityPurchased) as totalSpent
from items
where receiptId in (select id from receiptsOfUsers)
and brandCode is not null
group by 1
order by 2 desc
limit 1;
```

### Q6: Which brand has the most transactions among users who were created within the past 6 months?

**Answer**: HY-VEE has the most transactions among users who were created within the past 6 months.

```sql
with newRegisteredUsers as (select id, min(createdDate) as earlist_createdDate
                            from users
                            group by 1
                            having earlist_createdDate between "2020-09-01" and "2021-03-01"),

-- Find the receipts scanned by those users' Id
     receiptsOfUsers as (select id
                  from receipts
                  where userId in (select id from newRegisteredUsers))

select brandCode, count(*) as transactions
from items
where receiptId in (select id from receiptsOfUsers)
and brandCode is not null
group by 1
order by 2 desc
limit 1;
```

## Third Part : QA check

### Problem 1 : Barcode is used for two different brands.

Barcode = 511111704140 \
BrandCode = DIETCHRIS2 or PREGO

```sql
select distinct brandCode, name, barcode
from (select i.receiptId, i.barcode, b.brandCode, b.name
      from items i
               join brands b on i.barcode = b.barcode) t
order by 3;
```

### Problem 2: Total spend in receipts table doesn't match in items table.

ReceiptId = 60049d9d0a720f05f3000094

```sql
-- Total Spent amount in receipts table
select id, totalSpent, userId
from receipts
where id = "60049d9d0a720f05f3000094";

-- Each Price for this receipt
select receiptId, brandCode, discountedItemPrice, finalPrice, itemPrice, quantityPurchased
from items
where receiptId = "60049d9d0a720f05f3000094";

-- Calculated total spent amount in items table
select receiptId,
       round(sum(discountedItemPrice * quantityPurchased), 2) as discountedTotal,
       round(sum(finalPrice * quantityPurchased), 2)          as finalTotal,
       round(sum(itemPrice * quantityPurchased), 2)           as itemTotal
from items
where receiptId = "60049d9d0a720f05f3000094";
```

### Problem 3: Users Table has duplicated user ID, which cannot be considered as primary key.

```sql
select count(*) as rows from users;
select count(distinct id) as NumOfUserIds from users;
```

### Problem 4: Some barcodes in items table cannot be found in brands table.

```sql
select distinct barcode
from items
where barcode not in (select distinct barcode from brands);
```

### Problem 5: Some user Id in receipts table cannot be found in users table.

```sql
select distinct userId 
from receipts
where userId not in (select distinct id from users);
```

## Fourth Part: Communication

Hi, I found some data problems need clarification.
* First, a barcode is used to represent two different brands.
  For example, the brandCode DIETCHRIS2 or PREGO are both use the same barcode "511111704140".
* Second, the amount of "totalSpent" for some receipts doesn't match in items table.
  For example, the totalSpent for receiptId = "60049d9d0a720f05f3000094" is 743.79.
  While multiplying price by quantity purchased, we can't get this amount.
* Third, users data has many duplicated records, especially user ID. It can't be as a good primary key.
* Fourth, some barcodes in items table cannot be found in brands table, like 511111604037, 4060, etc.
* Fifth, some user ID in receipts table cannot be found in users table, like 5f9c74f7c88c1415cbddb839,
  5ff79459b3348b11c933736d, etc.
* Sixth, there are too much null / missing values in the tables. 

I discover the data quality issues based on three things:
  the logic behind the data,
  the relationship between different tables,
  and the foundation of better design a database.

To solve the data quality issues, I need to know how to perform data cleaning including removing duplicates data, 
filling in missing values, and data normalization.

To optimize the data assets, other information that I need to know are 
* Detail description of each column in the table.
* Understand the relationship between tables.
* Understand the dependency between columns.

I'm concerned about the items table because it was split from the receipts table, there was no primary key. 
In addition to that, we are constructing the relational database, which means it could be difficult for horizontal scale.
Therefore, the query performance may be quite slow if we put into production.










