import logging
import urllib3
import os
from tqdm import tqdm
from urllib3.util import Retry

class Transporter:
    def __init__(self):
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        self.http = urllib3.PoolManager(retries=retry_strategy)
        logging.getLogger("urllib3").setLevel(logging.WARNING)

    def download_file(self, url: str, path: str):
        """
        Download a file from a URL to a local path
        """
        try:
            response = self.http.request('GET', url, preload_content=False)
            total_length = int(response.headers.get('content-length', 0))

            with open(path, 'wb') as out_file, \
                 tqdm(desc=f"Downloading: {os.path.basename(path)}",
                      total=total_length,
                      unit='iB',
                      unit_scale=True) as progress_bar:
                
                for data in response.stream(1024 * 1024):
                    size = out_file.write(data)
                    progress_bar.update(size)

            response.release_conn()

            # Verify file was downloaded successfully
            if not os.path.exists(path):
                raise Exception("File not found after download")
            
            if os.path.getsize(path) != total_length and total_length > 0:
                raise Exception("Downloaded file size does not match expected size")

        except Exception as e:
            logging.error(f"Error downloading {url}: {type(e).__name__} - {str(e)}")

            try:
                if os.path.exists(path):
                    os.remove(path)
            except OSError as e:
                logging.error(f"Error removing file {path}: {str(e)}")
            return False
