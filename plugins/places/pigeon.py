from base import *
import urllib2, json

# categorized tags
TYPES = [
  ["restaurant", "food", "bar", "night_club", "lodging", "meal_delivery", "meal_takeaway", "cafe", \
  "grocery_or_supermarket", "bakery"], 
  ["airport", "taxi_stand", "train_station", "taxi", "plane", "train", "transport", "subway_station", "bus_station"],
  ["store", "shoe_store", "shopping_mall", "mall", "clothing_store", "convenience_store", \
  "hardware_store", "home_goods_store", "bicycle_store", "book_store", "department_store", "electronics_store", \
  "furniture_store", "jewelry_store", "liquor_store", "pet_store"],
  ["church", "religion", "hindu_temple", "synagogue", "place_of_worship", "mosque"],
  ["police", "fire_station", "emergency", "hospital", "doctor", "dentist", "physiotherapist", "pharmacy", "veterinary_care"],
  ["car_dealer", "car_rental", "car_repair", "car_wash"],
  ["health", "gym"],
  ["local_government_office", "embassy", "city_hall", "courthouse"],
  ["school", "university"],
  ["accounting", "finance", "bank", "atm"],
  ["general_contractor", "plumber", "electrician", "locksmith"],
  ["art", "museum", "painter", "florist"],
  ["amusement_park"],
  ["aquarium"],
  ["art_gallery"],
  ["beauty_salon"],
  ["bowling_alley"],
  ["campground"],
  ["casino"],
  ["cemetery"],
  ["funeral_home"],
  ["gas_station"],
  ["hair_care"],
  ["insurance_agency"],
  ["laundry"],
  ["lawyer"],
  ["library"],
  ["movie_rental", "movie_theater"],
  ["moving_company"],
  ["park", "rv_park"],
  ["parking"],
  ["post_office"],
  ["real_estate_agency"],
  ["roofing_contractor"],
  ["spa"],
  ["stadium"],
  ["storage"],
  ["travel_agency"],
  ["zoo"]
]

# main class
class pigeonParser(Parser):

  def __init__(self, *args, **kwargs):
    super(pigeonParser, self).__init__(*args, **kwargs)

  def validate(self): 
    querystr = ' '.join(self.query)
    for cat in TYPES:
      for item in cat:
        if item.replace('_', ' ') in querystr:
          return cat

    return False

  # parse user's query
  def parse(self, parent):

    # get api key
    if self.info.has_key("key"):
      key = self.info["key"]
    else:
      raise InvalidKeyException, "Please enter a valid Google Places API key in Pigeon's info.json"

    # get our location
    qry = urllib2.urlopen("http://freegeoip.net/json")
    l = json.loads( qry.read() )
    pos_lat, pos_long = l["latitude"], l["longitude"]

    # test query
    qry = urllib2.urlopen(
      "https://maps.googleapis.com/maps/api/place/nearbysearch/json?key=%s&location=%s,%s&sensor=true&radius=5000" % 
      ( key, pos_lat, pos_long ))

    data = json.loads( qry.read() )

    # now, get all the places from the data
    places = []
    for p in data["results"]:
      place = {}
      # filter out whats not open
      if (p.has_key("opening_hours") and p["opening_hours"]["open_now"]) or not p.has_key("opening_hours"):
        place["name"] = p["name"]
        place["types"] = p["types"]
        places.append(place)


    # filter places depending on what user said
    tags = []
    items = []
    querystr = ' '.join(self.query)
    for cat in TYPES:
      for item in cat:
        # print item
        if item.replace('_', ' ') in querystr:
          tags.append(item)

          # get all items with that tag
          items.extend([i for i in places if item in i["types"]])

    # nicely stuff all items into text and return
    # also, present as list so the user can get more information
    self.resp["return"] = [i["name"] for i in items]
    self.resp["text"] = ", ".join( self.resp["return"] )
    self.resp["present"] = "AS_LIST"


    # return response packet
    self.resp["status"] = STATUS_OK
    return self.resp

