import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# LinkedIn API credentials
CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
PERSON_URN = os.getenv("LINKEDIN_PERSON_URN")
ORGANIZATION_URN = os.getenv("LINKEDIN_ORGANIZATION_URN")

# LinkedIn API URLs
API_BASE_URL = "https://api.linkedin.com/v2"
UPLOAD_API_URL = "https://api.linkedin.com/v2/assets?action=registerUpload"

# Function to register an image upload
def register_upload():
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    upload_request_data = {
        "registerUploadRequest": {
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
            "owner": f"urn:li:organization:{ORGANIZATION_URN}",
            "serviceRelationships": [
                {
                    "relationshipType": "OWNER",
                    "identifier": "urn:li:userGeneratedContent"
                }
            ]
        }
    }

    response = requests.post(UPLOAD_API_URL, headers=headers, data=json.dumps(upload_request_data))
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to register upload: {response.status_code} - {response.text}")
        return None

# Function to upload an image
def upload_image(upload_url, image_path):
    with open(image_path, 'rb') as image_file:
        response = requests.put(upload_url, headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}, data=image_file)
        if response.status_code == 201:
            print("Image uploaded successfully!")
            return True
        else:
            print(f"Failed to upload image: {response.status_code} - {response.text}")
            return False

# Function to create a LinkedIn post
def create_linkedin_post(text, asset_urns):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    post_data = {
        "author": f"urn:li:organization:{ORGANIZATION_URN}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": text
                },
                "shareMediaCategory": "IMAGE",
                "media": [{"status": "READY", "media": asset_urn} for asset_urn in asset_urns]
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    response = requests.post(f"{API_BASE_URL}/ugcPosts", headers=headers, data=json.dumps(post_data))
    if response.status_code == 201:
        print("Post created successfully!")
    else:
        print(f"Failed to create post: {response.status_code} - {response.text}")


# Main function to automate the entire process
def main():
    text = "Check out these awesome images from our organization!"
    image_paths = ["/home/polymorphisma/adex/ama/uploaded_image/0e64d04e-c32d-495a-83f8-9e0a27f9d36a.png", "/home/polymorphisma/adex/ama/uploaded_image/abc11c0a-17d6-41af-abd1-7308d4e510d8.png"]
    asset_urns = []

    for image_path in image_paths:
        upload_response = register_upload()
        if upload_response:
            upload_url = upload_response['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
            asset_urn = upload_response['value']['asset']
            if upload_image(upload_url, image_path):
                asset_urns.append(asset_urn)

    if asset_urns:
        create_linkedin_post(text, asset_urns)

if __name__ == "__main__":
    main()
