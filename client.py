import requests

# Replace with the actual URL your FastAPI server is running on
API_URL = "http://localhost:8000/analyze-clothing/"

# Path to the image file you want to send
IMAGE_PATH = "samples/F2.JPG"

def analyze_clothing(image_path: str, model: str = "llama3.2-vision:11b"):
    with open(image_path, "rb") as img_file:
        files = {"image": ("download.jpg", img_file, "image/jpeg")}
        data = {"model": model}
        response = requests.post(API_URL, files=files, data=data)

    if response.status_code == 200:
        print("✅ Analysis Result:")
        print(response.json())
    else:
        print(f"❌ Request failed with status code {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    analyze_clothing(IMAGE_PATH)
