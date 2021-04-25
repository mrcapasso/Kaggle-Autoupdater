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
    unitsDict = {'B':1, 'KBs':3, 'MBs':6, 'GBs':9, 'TBs':12, 'PBs':15, 'EBs':18}
    for i in enumerate(unitsDict):
        exponent = unitsDict.get(i[1])
        if abs(sizeInBytes) < 1000:
            return str(sizeInBytes) + ' bytes'
        elif i[0]!=0 and abs(sizeInBytes)<10**(exponent+3):
            return str(round(sizeInBytes/10**exponent,2)) + ' ' + i[1]

if __name__ == '__main__':
    pass