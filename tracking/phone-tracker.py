import phonenumbers
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
import folium


def parse_phone_info(phone_number: str, region: str = "US") -> dict:
    parsed_number = phonenumbers.parse(phone_number, region)

    if not phonenumbers.is_valid_number(parsed_number):
        raise ValueError("Invalid phone number")

    location = geocoder.description_for_number(parsed_number, "en")
    phone_carrier = carrier.name_for_number(parsed_number, "en")

    return {
        "location": location,
        "carrier": phone_carrier,
        "number": phonenumbers.format_number(
            parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL
        ),
    }


def get_coordinates(api_key: str, location_name: str) -> tuple:
    geocoder = OpenCageGeocode(api_key)
    results = geocoder.geocode(location_name)

    if not results:
        raise ValueError("No coordinates found for the location")

    geometry = results[0]["geometry"]
    return geometry["lat"], geometry["lng"]


def create_map(lat: float, lng: float, label: str, output_file: str = "location_map.html") -> None:
    map = folium.Map(location=[lat, lng], zoom_start=10)
    folium.Marker([lat, lng], popup=label).add_to(map)
    map.save(output_file)


def main():
    region = "US"
    phone_number = "+14155238886"
    opencage_api_key = "YOUR_OPENCAGE_API_KEY"

    try:
        # Step 1: Get phone info
        phone_info = parse_phone_info(phone_number, region)
        print(f"Number: {phone_info['number']}")
        print(f"Location: {phone_info['location']}")
        print(f"Carrier: {phone_info['carrier']}")

        # Step 2: Convert location to coordinates
        lat, lng = get_coordinates(opencage_api_key, phone_info["location"])
        print(f"Coordinates: ({lat}, {lng})")

        # Step 3: Generate map
        create_map(
            lat, lng, f"{phone_info['number']} - {phone_info['carrier']}")
        print("Map saved as 'location_map.html'")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
