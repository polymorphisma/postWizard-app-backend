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

# LinkedIn API URLs
API_BASE_URL = "https://api.linkedin.com/v2"
UPLOAD_API_URL = "https://api.linkedin.com/v2/assets?action=registerUpload"


class Linkedin:
    def __init__(self) -> None:
        pass

    def register_upload(self):
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }

        upload_request_data = {
            "registerUploadRequest": {
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                "owner": f"urn:li:person:{PERSON_URN}",
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
    def upload_image(self, upload_url, image_path):
        with open(image_path, 'rb') as image_file:
            response = requests.put(upload_url, headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}, data=image_file)
            if response.status_code == 201:
                print("Image uploaded successfully!")
                return True
            else:
                print(f"Failed to upload image: {response.status_code} - {response.text}")
                return False

    # Function to create a LinkedIn post
    def create_linkedin_post(self, text, asset_urns):
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }

        post_data = {
            "author": f"urn:li:person:{PERSON_URN}",
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
            return response.json()
        else:
            return {"success": False, "message": f"An error occurred: {response.text}"}

    # Main function to automate the entire process
    def entry_point(self, image_paths: list, text: str):
        asset_urns = []

        for image_path in image_paths:
            upload_response = self.register_upload()
            if upload_response:
                upload_url = upload_response['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
                asset_urn = upload_response['value']['asset']
                if self.upload_image(upload_url, image_path):
                    asset_urns.append(asset_urn)

        if asset_urns:
            value = self.create_linkedin_post(text, asset_urns)

            if 'id' in value: 
                value['message'] = "https://www.linkedin.com/feed/update/" + value['id']
                value['success'] = True

                del value['id']

            return value
        return {"success": False, "message": "Linkedin post didn't go through."}


if __name__ == "__main__":
    image_paths = ["/home/polymorphisma/adex/ama/uploaded_image/88d0faa0-66f0-494e-972f-b1a6f5af124b.jpg", "/home/polymorphisma/adex/ama/uploaded_image/4c3898c3-0194-4ebf-a46b-306594aa425e.png"]
    text = "testing testing"

    linked_obj = Linkedin()
    value = linked_obj.entry_point(image_paths=image_paths, text=text)
    print(value)
