import os

def kaggleTokenExistence(mainStorageDrive: str='C:\\') -> bool: 
    normalAPILocation = os.path.join(mainStorageDrive, 'Users', os.getlogin(), '.kaggle')
    kaggleToken = r'kaggle.json'
    if os.path.exists(os.path.join(normalAPILocation, kaggleToken)):
        return True
    else:
        return False
    