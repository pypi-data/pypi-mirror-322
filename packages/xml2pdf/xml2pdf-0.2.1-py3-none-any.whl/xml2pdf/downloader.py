import requests
import os

def download_xml_file(url, save_dir='downloads'):
    try:
        filename = url.split('f=')[-1]
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, filename)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            f.write(response.content)
            
        return save_path
    except Exception as e:
        print(f"Error downloading file: {str(e)}")
        return None