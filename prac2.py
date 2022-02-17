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

        # Connecting API service
        self.service = build('drive', 'v3', credentials=self.creds)
        #Fetching list of files


        results = self.service.files().list(
            pageSize=100, fields="files(id, name)").execute()
        items = results.get('files', [])

        # printing files

        print("Here's a list of files: \n")
        print(*items, sep="\n", end="\n\n")

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
            self.file = self.service.files().get(fileId=file_id, fields='size,modifiedTime').execute()
            # True on success
            return True
        except:

            # False on fail
            print("Something went wrong.")
            return False


    #Test cases:
    def fileExistsAfterDownload(self,file_name):
        assert os.path.exists(f_name)
        print("The file download check completed")


    def fileSizecheckAfterDownload(self,file_name):
        file_size = os.path.getsize(f_name)
        assert file_size == int(self.file['size'])
        print("The size of file in Gdrive and file downloaded locally matches")
if __name__ == "__main__":
    obj = DriveAPI()
    i = int(input("Enter your choice:"
                  "1 - Download file, 2- Exit.\n"))

    if i == 1:
        f_id = input("Enter file id: ")
        f_name = input("Enter file name: ")
        obj.FileDownload(f_id, f_name)

    elif i == 2:
        f_path = input("Enter full file path: ")
        obj.FileUpload(f_path)

    else:
        exit()
    obj.fileExistsAfterDownload(f_name)
    obj.fileSizecheckAfterDownload(f_name)

