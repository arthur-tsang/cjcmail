import requests

"""
Edit the speaker information sheet by being a mod and going to:

https://docs.google.com/spreadsheets/d/1CNCQvy5NUVnJjnYjO9rD2sPp073cga-1gz8aNlXpzDc/edit#gid=0

"""

def download_speaker_csv():
    """
    Updates our local copy of the speaker csv file by downloading from the Google Docs sheet
    """

    
    # Sheet-specific details
    SHEET_ID = '1CNCQvy5NUVnJjnYjO9rD2sPp073cga-1gz8aNlXpzDc'
    SHEET_NAME = 'Sheet1'

    # Construct the URL for CSV export
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Save the content to a CSV file
        with open('speakers.csv', 'wb') as f:
            f.write(response.content)
        print("CSV file has been exported successfully.")
    else:
        raise RuntimeError(f'Failed to download CSV at {url} !! Status code {response.status_code}')



if __name__ == '__main__':
    download_speaker_csv()
