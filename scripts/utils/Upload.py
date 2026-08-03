# 
# Generic script to upload assets to Roblox using the Open Cloud API
# Made by claude
#

import argparse
import os
import time
import requests
import json
import xml.etree.ElementTree as ET
import re

asset_type_map = {
    '.png': 'Decal',
    '.jpg': 'Decal',
    '.jpeg': 'Decal',
    '.gif': 'Decal',
    '.bmp': 'Decal',
    '.tga': 'Decal',
    '.mp3': 'Audio',
    '.ogg': 'Audio',
    '.wav': 'Audio',
    '.fbx': 'Model',
    '.obj': 'Model'
}

def upload_asset(file_path, name, description, auth_token, creator_id, creator_type="user"):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    file_ext = os.path.splitext(file_path)[1].lower()
    
    asset_type = asset_type_map.get(file_ext)
    if not asset_type:
        raise ValueError(f"Unsupported file type: {file_ext}")
    
    headers = {
        "x-api-key": auth_token,
    }
    
    # Uploading Asset
    creator_key = "userId" if creator_type.lower() == "user" else "groupId"
    request_data = {
        "assetType": asset_type,
        "displayName": name,
        "description": description,
        "creationContext": {
            "creator": {
                creator_key: str(creator_id)
            }
        }
    }
    
    with open(file_path, 'rb') as file:
        files = {
            'request': (None, json.dumps(request_data), 'application/json'),
            'fileContent': (os.path.basename(file_path), file, 'application/octet-stream')
        }
        
        try:
            response = requests.post("https://apis.roblox.com/assets/v1/assets", headers=headers, files=files)
            
            if response.status_code != 200:
                print(f"❌ Upload failed with status code: {response.status_code}")
                print(f"Response: {response.text}")
                return None
    
            result = response.json()
            operation_id = result.get('operationId')

            
            while True:
                time.sleep(0.25)
                status_url = f"https://apis.roblox.com/assets/v1/operations/{operation_id}"
                status_response = requests.get(status_url, headers=headers)
                
                if status_response.status_code == 200:
                    status_result = status_response.json()
                    if status_result.get('done') == True:
                        assetId = status_result["response"]["assetId"]
                        break
                else:
                    print(f"❌ Failed to check operation status: {status_response.status_code}")
                    return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None

    AssetDeliveryLocation = requests.get(f"https://apis.roblox.com/asset-delivery-api/v1/assetId/{assetId}", headers=headers)
    if AssetDeliveryLocation.status_code != 200:
        print(f"❌ Failed to get asset delivery location: {AssetDeliveryLocation.status_code}")
        return None
    
    XMLContentRequest = requests.get(AssetDeliveryLocation.json()["location"])
    ContentData = ET.fromstring(XMLContentRequest.content)

    url_element = ContentData.find(".//Content[@name='Texture']/url")

    if url_element is not None and url_element.text:
        # Extract the number using regex
        match = re.search(r"id=(\d+)", url_element.text)
        if match:
            asset_id = match.group(1)
            print(asset_id)
            return True
        else:
            print("❌ No ID found in URL text")
            return None
    else:
        print("❌  No <url> tag found")
        return None

    

def main():
    """Main function to handle command line arguments and execute upload"""
    parser = argparse.ArgumentParser(
        description="Upload assets to Roblox using Open Cloud API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python upload.py image.png --name "My Image" --description "A cool image" --auth "your_api_key" --creator-id "123456789"
  python upload.py sound.mp3 --name "Background Music" --description "Epic soundtrack" --auth "your_api_key" --creator-id "123456789" --creator-type "user"
  python upload.py model.fbx --name "3D Model" --description "Cool 3D model" --auth "your_api_key" --creator-id "987654321" --creator-type "group"
        """
    )
    
    parser.add_argument(
        'file_path',
        help='Path to the file to upload'
    )
    
    parser.add_argument(
        '--name',
        required=True,
        help='Name for the asset'
    )
    
    parser.add_argument(
        '--description',
        required=True,
        help='Description for the asset'
    )
    
    parser.add_argument(
        '--auth',
        required=True,
        help='Roblox Open Cloud API key'
    )
    
    parser.add_argument(
        '--creator-id',
        required=True,
        help='Creator ID (user ID or group ID)'
    )
    
    parser.add_argument(
        '--creator-type',
        choices=['user', 'group'],
        default='user',
        help='Creator type: user or group (default: user)'
    )
    
    args = parser.parse_args()
    
    try:
        result = upload_asset(args.file_path, args.name, args.description, args.auth, args.creator_id, args.creator_type)
        if result:
            exit(0)  # Success
        else:
            exit(1)  # Failure
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
