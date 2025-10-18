import requests
from urllib.parse import quote_plus
from SPARQLWrapper import SPARQLWrapper, JSON

# HOUSE IMAGE
google_api_key = "AIzaSyBvPK89CPhKLyKppw19cjlzlzCmRsL0U88"

def geturl(house_number, street_name, postcode):
    full_address = f"{house_number} {street_name}, {postcode}"
    encoded_address = quote_plus(full_address)
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={encoded_address}&key={google_api_key}"
    response = requests.get(geocode_url)
    data = response.json()
    lat = data['results'][0]['geometry']['location']['lat']
    lng = data['results'][0]['geometry']['location']['lng']
    paidimage_url = f"https://maps.googleapis.com/maps/api/streetview?size=600x300&location={lat},{lng}&key={google_api_key}"
    livestreetview_image_url = f"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={lat},{lng}"

    return livestreetview_image_url

def getprice(house_number, postcode):  
    sparql = SPARQLWrapper("http://landregistry.data.gov.uk/landregistry/sparql")
    sparql.setQuery(f"""
    PREFIX lrppi: <http://landregistry.data.gov.uk/def/ppi/>
    PREFIX lrcommon: <http://landregistry.data.gov.uk/def/common/>

    SELECT ?pricePaid ?transactionDate ?postcode ?paon ?street ?town
    WHERE {{
      ?record a lrppi:TransactionRecord ;
              lrppi:pricePaid ?pricePaid ;
              lrppi:transactionDate ?transactionDate ;
              lrppi:propertyAddress ?addr .
      ?addr lrcommon:postcode ?postcode .
      OPTIONAL {{ ?addr lrcommon:paon ?paon . }}
      OPTIONAL {{ ?addr lrcommon:street ?street . }}
      OPTIONAL {{ ?addr lrcommon:town ?town . }}

      FILTER(STR(?postcode) = "{str(postcode)}")
      FILTER(STR(?paon) = "{str(house_number)}")
    }}
    LIMIT 5
    """)

    sparql.setReturnFormat(JSON)
    sparql.setTimeout(60)
    print("Querying... please wait")
    results = sparql.query().convert()

    prices = []
    street_name = None

    for result in results["results"]["bindings"]:
        pricepaid = result["pricePaid"]["value"]
        date = result["transactionDate"]["value"]
        street = result.get("street", {}).get("value", None)

        if not street_name and street:
            street_name = street

        prices.append(f"£{pricepaid} on {date}")

    if not prices:
        return ["No results found"], None

    return prices, street_name