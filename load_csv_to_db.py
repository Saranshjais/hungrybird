import csv
import requests
import time

API_KEY = "AIzaSyAN1Y6DgLtlU24YTlp77O2gR_Lw4xiC03w"
CSV_FILE = "google_places_vendors.csv"

def get_photo_url(vendor_name, lat, lng, city):
    query = f"{vendor_name} {city}"
    url = (
        f"https://maps.googleapis.com/maps/api/place/textsearch/json"
        f"?query={query}&location={lat},{lng}&radius=2000&key={API_KEY}"
    )
    
    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        print(f"❌ Error fetching data from Google Places API: {e}")
        return ""

    results = data.get("results", [])
    if results and "photos" in results[0]:
        photo_ref = results[0]["photos"][0]["photo_reference"]
        return f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_ref}&key={API_KEY}"
    return ""

def is_valid_image_url(url):
    return url and "placeholder.com" not in url.lower() and "no+image" not in url.lower()

updated_vendors = []

with open(CSV_FILE, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Only update if image is missing or invalid
        if not is_valid_image_url(row["image"]):
            print(f"🔄 Fetching image for: {row['name']} ({row['city']})...")
            image_url = get_photo_url(row["name"], row["latitude"], row["longitude"], row["city"])
            if image_url:
                row["image"] = image_url
                print(f"✅ Found image.")
            else:
                row["image"] = "https://via.placeholder.com/400x300?text=No+Image"
                print(f"⚠️ No image found. Using placeholder.")
            time.sleep(1.5)  # API rate limit protection
        updated_vendors.append(row)

# Write updated CSV
with open(CSV_FILE, "w", newline='', encoding='utf-8') as f:
    fieldnames = ["name", "cuisine", "latitude", "longitude", "city", "rating", "image", "categories"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(updated_vendors)

print("✅ CSV updated with valid image URLs.")
