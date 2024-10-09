from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def authenticate():
    gauth = GoogleAuth()
    # Try to load saved client credentials
    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved credentials
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("mycreds.txt")
    return gauth

def upload_file(file_path, file_name):
    gauth = authenticate()
    drive = GoogleDrive(gauth)
    file = drive.CreateFile({'title': file_name,'parents': [{'id': '1uLkjciW_QEwml20foWh46jMKGEErpeP-'}]})
    file.SetContentFile(file_path)
    file.Upload()
    print('File uploaded: %s' % file['title'])

def download_file(file_id, save_to_path):
    gauth = authenticate()
    drive = GoogleDrive(gauth)
    file = drive.CreateFile({'id': file_id})
    file.GetContentFile(save_to_path)
    print('File downloaded to: %s' % save_to_path)

# Example usage
if __name__ == "__main__":
    # Upload file
   
    upload_file("","main.py")
    
   
