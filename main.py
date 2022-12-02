import json
import data_converter
import repository
from datetime import datetime

def main():
    file_list = ["data/brands.json", "data/users.json", "data/receipts.json"]
    # read data
    brands_raw_data = read_file(file_list[0])
    users_raw_data = read_file(file_list[1])
    receipts_raw_data = read_file(file_list[2])

    # convert data to db readable format
    brands_data = data_converter.convert("brands", brands_raw_data)
    users_data = data_converter.convert("users", users_raw_data)
    receipts_data = data_converter.convert("receipts", receipts_raw_data)
    items_data = data_converter.convert("items", receipts_raw_data)

    # store data in mysql
    rep = repository.Repository()
    # for brand in brands_data:
    #     rep.write_brands(brand)

    for receipts in receipts_data:
        rep.write_receipts(receipts)

    # for users in users_data:
    #     rep.write_users(users)

    # for item in items_data:
    #     rep.write_items(item)

def read_file(filename):
    file = open(filename, 'r')
    arr = []
    for line in file:
        arr.append(json.loads(line))
    return arr


if __name__ == '__main__':
    main()

