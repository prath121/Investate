from realestate_apisv2 import geturl
from realestate_apisv2 import getprice


house_number = input("Please enter the house number: ").strip()
postcode = input("Please enter the postcode: ").strip().upper()

prices, street_name = getprice(house_number, postcode)
for p in prices:
    print(p)
    
url = geturl(house_number, street_name, postcode)
print(url)