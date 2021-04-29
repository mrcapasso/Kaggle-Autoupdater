#!/user/bin/python3.9.1

#     License Type: GNU General Public License v3.0
#     'Kaggle Autoupdater', automated file version control for Kaggle.
#     Copyright (C) 2021 Matteo Capasso (matteo@capasso.dev)

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os

def byteUnitConverter(sizeInBytes:int, roundDec:int=2) -> str: 
    '''Converts bytes integer to larger bytes-unit string.

    Args:
        sizeInBytes(int): The integer amount of bytes to re-label.
        roundDec(int): Decimal place to round numbers to.

    Returns:
        Small string with appropriate byte-unit label. 

    Examples: 
        190 -> '190 bytes'
        1898721 -> '1.9 MBs'
        9999999999999 -> '10.0 TBs'
    
    '''
    unitsDict = {'B':1, 'KBs':3, 'MBs':6, 'GBs':9, 'TBs':12, 'PBs':15, 'EBs':18}
    for i in enumerate(unitsDict):
        exponent = unitsDict.get(i[1])
        if abs(sizeInBytes) < 1000:
            return str(sizeInBytes) + ' bytes'
        elif i[0]!=0 and abs(sizeInBytes)<10**(exponent+3):
            #Note, for a better solution change (exponent+3) to the 
            #value pair from the ith+1 iteration. 3 was used for simplicity.
            return str(round(sizeInBytes/10**exponent,roundDec)) + ' ' + i[1]

def folderSizeAmount(absFolderPath:str) -> int:
    '''Finds byte size of specific folder by walking file tree.

    Args:
        absFolderPath (str): Absolute file path to directory.

    Returns:
        Integer value of designated directory in bytes.

    '''
    totalSize = 0
    for folderName, _, fileList in os.walk(absFolderPath):
        os.chdir(folderName)
        for file in fileList: 
            individalFilePath = os.path.abspath(file)
            totalSize += os.path.getsize(individalFilePath)
    return totalSize

def extractURLData(url:str) -> tuple: 
    '''Retrieves kaggle dataset author and name from kaggle URL string.

    Args:
        url (str): Kaggle URL of the following format:
        https://www.kaggle.com/<author>/<datasetname> 

    Returns:
        Tuple of strings where: 
        (Kaggle dataset's Name, Kaggle dataset's Author) 
    
    '''
    datasetName = []
    datasetAuthor = []
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

#Note, kaggle API & module allows for individual file type downloads.
def removeByFileExtension(extension:str, directory:str) -> None:
    '''Removes files in specifed directory based off file extension.

    Args:
        extension (str): Extension type to remove files by. (e.g. '.json')
        directory (str): Absolute file path to directory containing files.

    '''
    extractedFiles = os.listdir(directory)
    for file in extractedFiles:
        if file[-len(extension):] == extension:
            os.unlink(os.path.join(directory, file)) 

if __name__ == '__main__':
    raise AssertionError('Missguided call -- this is not the main function.')