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

def extractURLData(url:str) -> tuple: #Pulls author and dataset name from kaggle URL. 
    datasetName = []
    datasetAuthor = []
    #URL formatted as: www.kaggle.com/<datasetAuthor>/<datasetName>
    for i in reversed(url):
        if i != r'/':
            datasetName.append(i)
        else:
            datasetNameString = ''.join(datasetName[::-1])
            reducedURL = url.replace(r'/' + datasetNameString, '')
            break
    for j in reversed(reducedURL):
        if j != r'/':
            datasetAuthor.append(j)
        else:
            datasetAuthorString = ''.join(datasetAuthor[::-1])
            break
    return datasetNameString, datasetAuthorString

def elapsedTimeCalculator(startTime:float, endTime:float, decRound:int=2) -> str:
    elapsedTimeSecs = endTime - startTime
    elapsedTimeMins = elapsedTimeSecs/60
    elapsedTimeHours = elapsedTimeMins/60
    elapsedTimeDays = elapsedTimeHours/24
    if elapsedTimeDays >= 1: #Time as unit of days. 
        return str(round(elapsedTimeDays, decRound)) + ' days'
    elif elapsedTimeHours >= 1: #Time as unit of hours.
        return str(round(elapsedTimeHours, decRound)) + ' hours'
    elif elapsedTimeMins >= 1: #Time as unit of minutes.
        return str(round(elapsedTimeMins,decRound)) + ' minutes'
    else: #Time as unit of seconds.
        return str(round(elapsedTimeSecs,decRound)) + ' seconds'

def folderSizeAmount(absFolderPath:str):
    totalSize = 0
    for folderName, _, fileList in os.walk(absFolderPath):
        os.chdir(folderName)
        for file in fileList: 
            individalFilePath = os.path.abspath(file)
            totalSize += os.path.getsize(individalFilePath)
    return totalSize
    
def byteUnitConverter(sizeInBytes:int) -> str: 
    unitsDict = {'bytes':1, 'kilobytes':3, 'megabytes':6, 'gigabytes':9, 'terabytes':12, 'pedabytes':15}
    for i in unitsDict:
        exponent = unitsDict.get(i)
        if sizeInBytes <= 10**(exponent+3):
            unitConversion = round(sizeInBytes/(10**exponent),2)
            return  str(unitConversion) + ' ' + i

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