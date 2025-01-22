import requests
import os
from datetime import datetime

def download_xml_file(url, save_dir='downloads'):
    """
    Download XML file from given URL and save it to specified directory.
    
    Args:
        url (str): URL of the XML file
        save_dir (str): Directory to save the downloaded file
        
    Returns:
        str: Path to the downloaded file if successful, None otherwise
    """
    try:
        filename = url.split('f=')[-1]
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, filename)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            f.write(response.content)
            
        return save_path
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {str(e)}")
        return None
    except IOError as e:
        print(f"Error saving file: {str(e)}")
        return None