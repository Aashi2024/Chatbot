import requests

def get_flower_info(flower_name):
    url = "https://trefle.io/api/v1/plants"
    token = "q8DZmqk_sLr5wkNUfKAzgWdgoA_km8TalngY2YZ0-eg"
    params = {
        "q": flower_name,
        "token": token
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return f"❌ Error: {response.status_code}"

    try:
        data = response.json()["data"]
        if not data:
            return f"❌ No results found for '{flower_name}'."

        # Debug line to see what data is returned
        # print("DEBUG:", data)

        flower = next(
            (item for item in data if flower_name.lower() in item.get("common_name", "").lower()),
            None
        )

        if not flower:
            return f"❌ No flower found that matches '{flower_name}'."

        name = flower.get("common_name", "Unknown")
        scientific = flower.get("scientific_name", "N/A")
        image = flower.get("image_url", "")

        result = f"🌸 **{name}** ({scientific})"
        if image:
            result += f"\n🖼️ Image: {image}"
        return result

    except Exception as e:
        return f"❌ Failed to decode JSON: {e}"