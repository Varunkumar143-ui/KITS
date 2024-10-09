import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload,MediaIoBaseDownload
import io
# Define the Google Drive API scopes and service account file path
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = "D:\\Downloads\\app-20240402T154822Z-001\\app\\sinuous-pact-384516-2badd46aa950.json"

# Create credentials using the service account file
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the Google Drive service
drive_service = build('drive', 'v3', credentials=credentials)

def create_folder(folder_name, parent_folder_id=None):
    """Create a folder in Google Drive and return its ID."""
    folder_metadata = {
        'name': folder_name,
        "mimeType": "application/vnd.google-apps.folder",
        'parents': [parent_folder_id] if parent_folder_id else []
    }

    created_folder = drive_service.files().create(
        body=folder_metadata,
        fields='id'
    ).execute()

    print(f'Created Folder ID: {created_folder["id"]}')
    return created_folder["id"]

def list_folder(parent_folder_id=None, delete=False):
    """List folders and files in Google Drive."""
    results = drive_service.files().list(
        q=f"'{parent_folder_id}' in parents and trashed=false" if parent_folder_id else None,
        pageSize=1000,
        fields="nextPageToken, files(id, name, mimeType)"
    ).execute()
    items = results.get('files', [])
    
    if not items:
        return None
        print("No folders or files found in Google Drive.")
    else:
        return items
        print("Folders and files in Google Drive:")
        for item in items:
            print(f"Name: {item['name']}, ID: {item['id']}, Type: {item['mimeType']}")
            if delete:
                delete_files(item['id'])

def delete_files(file_or_folder_id):
    """Delete a file or folder in Google Drive by ID."""
    try:
        drive_service.files().delete(fileId=file_or_folder_id).execute()
        print(f"Successfully deleted file/folder with ID: {file_or_folder_id}")
    except Exception as e:
        print(f"Error deleting file/folder with ID: {file_or_folder_id}")
        print(f"Error details: {str(e)}")

def download_file(file_id, destination_path):
    """Download a file from Google Drive by its ID."""
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.FileIO(destination_path, mode='wb')
    
    downloader = MediaIoBaseDownload(fh, request)
    
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")



def get_gdrive_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    # return Google Drive API service
    return build('drive', 'v3', credentials=creds)
def upload(file):
    file_metadata = {
        "name": file,
        "parents": ['1-L8y5jdChRWAKIgGC30-f9FvSRiPa69d']
    }
    # upload
    media = MediaFileUpload(file, resumable=True)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print("File created, id:", file.get("id"))
def is_check(file,parent_folder):
    fil = list_folder(parent_folder_id=parent_folder)
    if fil != None:
        for f in fil:
            if not f is None:
                print(f)
                if f['name'] == file:
                    return True
    return False
def upload_image(path,file):
    out = file[:-12]+".nii.gz"
    media = MediaFileUpload(path+file, resumable=True)
    file_metadata = {
        "name": file,
        "parents": ['1-L8y5jdChRWAKIgGC30-f9FvSRiPa69d']
    }
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print("Hello Upload")
    while(not is_check(out,'1-KDRcv015v3av-YGCp_G7iSsjNw4gI-5')):
        pass
    fil = list_folder(parent_folder_id='1-KDRcv015v3av-YGCp_G7iSsjNw4gI-5')
    if fil != None:
        for f in fil:
            if f['name'] == out:
                download_file(f['id'],'app\\templates\\uploads\output\\'+out)
    

if __name__ == '__main__':
    # Example usage:

    # Create a new folder
    # create_folder("MyNewFolder")
    
    # List folders and files
    
    upload_image("D:\\Downloads\\app-20240402T154822Z-001\\app\\uploads\\input\\","case_00006_0000_0000.nii.gz")
    # Delete a file or folder by ID
    # delete_files("your_file_or_folder_id")

    # Download a file by its ID
    # download_file("your_file_id", "destination_path/file_name.extension")