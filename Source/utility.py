#!/user/bin/python3.9.1
import os

def kaggleTokenExistence(mainStorageDrive: str='C:\\') -> bool: 
    normalAPILocation = os.path.join(mainStorageDrive, 'Users', os.getlogin(), '.kaggle')
    kaggleToken = r'kaggle.json'
    if os.path.exists(os.path.join(normalAPILocation, kaggleToken)):
        return True
    else:
        return False
    
def removeByFileExtension(extension:str, directory:str):
    extractedFiles = os.listdir(directory)
    for file in extractedFiles:
        if file[-len(extension):] == extension:
            os.unlink(os.path.join(directory, file)) 

if __name__ == '__main__':
    pass
    