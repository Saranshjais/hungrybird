import csv
import requests
import time

API_KEY = "AIzaSyAN1Y6DgLtlU24YTlp77O2gR_Lw4xiC03w"  
CITIES = {
    "Jaipur": (26.9124, 75.7873),
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777)
}
NUM_RESULTS = 20
RADIUS_METERS = 5000
QUERY = "street food"

def get_place_details(lat, lng, city):
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={QUERY}+in+{city}&location={lat},{lng}&radius={RADIUS_METERS}&key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data.get("results", [])

vendors = []

for city, (lat, lng) in CITIES.items():
    print(f"📍 Fetching street food places in {city}...")
    results = get_place_details(lat, lng, city)
    count = 0
    for place in results:
        if count >= NUM_RESULTS:
            break
        vendor = {
            "name": place.get("name"),
            "cuisine": "Street Food",
            "latitude": place["geometry"]["location"]["lat"],
            "longitude": place["geometry"]["location"]["lng"],
            "city": city,
            "rating": place.get("rating", 4.0),
            "image": "",
            "categories": ", ".join(place.get("types", []))  # ✅ Add types as categories
        }
        if "photos" in place:
            photo_ref = place["photos"][0]["photo_reference"]
            vendor["image"] = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_ref}&key={API_KEY}"
        vendors.append(vendor)
        count += 1
    time.sleep(2)

# ✅ Write to CSV
with open("google_places_vendors.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "cuisine", "latitude", "longitude", "city", "rating", "image", "categories"])
    writer.writeheader()
    writer.writerows(vendors)

print("✅ google_places_vendors.csv created successfully.")
