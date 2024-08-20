import os
import sys
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import zipfile
from google.cloud import storage

def create_bucket():
    """Creates a new bucket in Google Cloud Storage."""
    client = storage.Client()
    bucket = client.bucket('GDELT_event_files')
    bucket.storage_class = "STANDARD"
    new_bucket = client.create_bucket(bucket, location="US")
    print(f"Bucket {new_bucket.name} created.")

def download_files():
    URL = 'http://data.gdeltproject.org/events/index.html'
    response = requests.get(URL)
    bucket_path='/usr/local/airflow/dags/descargas'

    if response.status_code == 200:
        soup=BeautifulSoup(response.content, 'html.parser')
        links = [a['href'] for a in soup.find_all('a',href=True)]
        print(links[3])

        file_url = links[3]
        file_response = requests.get('http://data.gdeltproject.org/events/'+file_url)

        if file_response.status_code == 200:
            file_name = file_url.split('/')[-1]
            file_path=os.path.join(bucket_path,file_name)
            with open(file_name, 'wb') as file:
                file.write(file_response.content)
                print(f'File downloaded: {file_name}')

            # Decompress the ZIP file
            with zipfile.ZipFile(file_name, 'r') as zip_ref:
                zip_ref.extractall()
                print(f'File decompressed: {file_name}')

            # Assuming the ZIP file contains a single CSV file
            csv_file_name = zip_ref.namelist()[0]
            print(f'CSV file extracted: {csv_file_name}')



            # Delete the ZIP file
            os.remove(file_name)
            print(f'ZIP file deleted: {file_name}')
        else:
            print(f'Failed to download the file: {file_url}. Status code: {file_response.status_code}')     
    else:
        print(f'Failed to retrieve the URL: {URL}. Status code: {response.status_code}')

    return

'''URL = 'http://data.gdeltproject.org/events/index.html'
response = requests.get(URL)

if response.status_code == 200:
    soup=BeautifulSoup(response.content, 'html.parser')
    links = [a['href'] for a in soup.find_all('a',href=True)]
    print(links[3])

    file_url = links[3]
    file_response = requests.get('http://data.gdeltproject.org/events/'+file_url)

    if file_response.status_code == 200:
        file_name = file_url.split('/')[-1]
        with open(file_name, 'wb') as file:
            file.write(file_response.content)
            print(f'File downloaded: {file_name}')

    # Decompress the ZIP file
        with zipfile.ZipFile(file_name, 'r') as zip_ref:
            zip_ref.extractall()
            print(f'File decompressed: {file_name}')

        # Assuming the ZIP file contains a single CSV file
        csv_file_name = zip_ref.namelist()[0]
        print(f'CSV file extracted: {csv_file_name}')



        # Delete the ZIP file
        os.remove(file_name)
        print(f'ZIP file deleted: {file_name}')
    else:
        print(f'Failed to download the file: {file_url}. Status code: {file_response.status_code}')     
else:
    print(f'Failed to retrieve the URL: {URL}. Status code: {response.status_code}')


current_date=datetime.today().date()
target_date = datetime.strptime('20240815', '%Y%m%d').date()


# Iterate from current_date to target_date day by day
while current_date >= target_date:
    formatted_date = current_date.strftime('%Y%m%d')
    for link in links:
        if link.startswith(formatted_date):
            print(f"Link starting with {formatted_date}: {link}")
    current_date -= timedelta(days=1)'''