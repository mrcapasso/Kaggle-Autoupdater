#!/user/bin/python3.9.1
import os

#Note, key authentication exists natively in kaggle module. 
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

# class kaggleMetadadata:
#     #Classes Example: https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
#     #Classes Docs: https://docs.python.org/3/tutorial/classes.html
#     #Kaggle Metadata Ex: https://www.kaggle.com/rashikrahmanpritom/heart-attack-analysis-prediction-dataset/metadata

#     def __init__(self,author,license,updateFrequency,dateCreated,lastOnlineUpdate,lastOfflineUpdate,currentOnlineVersion,currentOfflineVersion): 
#         #__init__ is a constructor for new object creation specific to class
#         #self is used to show variables belong to this class
#         #instaces are like states for a group (e.g. water is LIQUId, water is SOLID)
#         self.author = author
#         self.license = license
#         self.updateFrequency = updateFrequency
#         self.dateCreated = dateCreated
#         self.lastOnlineUpdate = lastOnlineUpdate
#         self.lastOfflineUpdate = lastOfflineUpdate
#         self.currentOnlineVersion = currentOnlineVersion
#         self.currentOfflineVersion = currentOfflineVersion

if __name__ == '__main__':
    pass