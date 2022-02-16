# import the required libraries
from __future__ import print_function
import pickle
import os.path
import io
import shutil
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from googleapiclient.http import MediaIoBaseDownload


class DriveAPI:
    global SCOPES

    #scopes
    SCOPES = ['https://www.googleapis.com/auth/drive']

    def __init__(self):

        # Variable to store the user access token.

        self.creds = None



        # Check if file token.pickle exists
        if os.path.exists('token.pickle'):

            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)

        # user to log in if credentials not available
        if not self.creds or not self.creds.valid:

            #new token will be created if it has expired
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        # Connect to the API service
        self.service = build('drive', 'v3', credentials=self.creds)



    def FileDownload(self, file_id, file_name):
        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()

        downloader = MediaIoBaseDownload(fh, request, chunksize=20000000)
        done = False

        try:
            # for data download
            while not done:
                status, done = downloader.next_chunk()

            fh.seek(0)

            # writing data to file
            with open(file_name, 'wb') as f:
                shutil.copyfileobj(fh, f)

            print("File Downloaded")
            # True on success
            return True
        except:

            # False on fail
            print("Something went wrong.")
            return False

    def test_download(self,file_name):
        assert file_name == "ChicagoCensusData.csv"

if __name__ == "__main__":
    obj = DriveAPI()
    obj.FileDownload("13qbs-X047d6i68ciKgdpM1aMLBY570di", "ChicagoCensusData.csv")
    obj.test_download("ChicagoCensusData.csv")

