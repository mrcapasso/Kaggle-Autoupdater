#! Note: This requires a current kaggle API token. See link below, very easy sign up. 
#! API Link: https://www.kaggle.com/docs/api

import kaggle, os, re, requests
    #pip install kaggle

def kaggleDownloadCmd(dataset, downloadPath, fileName: str=None, unzip: bool=False, force: bool=False, quiet: bool=False) -> str:
    #Reference URL: https://github.com/Kaggle/kaggle-api#download-dataset-files
    #Note, unzip feature conflicts with kaggle redundant file checking.
    if fileName == None: 
        i = False
    else: 
        i = True
    command = ('kaggle datasets download'
            + i*(' -f ' + str(fileName))
                #File name, all files downloaded if not provided
            + (' -p ' + str(downloadPath))
                #Folder where file(s) will be downloaded, defaults to current WD.
            + (' --unzip ')*unzip
                #Unzip the downloaded file. Will delete the zip file when completed.
            + (' -o ')*force
                #Skip check whether local version of file is up to date, force file download
            + (' -q ')*quiet
                #Suppress printing information about the upload/download progress
            + ' ' + str(dataset)
                #Dataset URL suffix in format <owner>/<dataset-name> (use "kaggle datasets list" to show options)
         )
    return command

def kaggleListsCmd(search: str, tags: list, sortBy=' ', fileSize=' ', fileType=' ', license=' ', user=' ', pageNum: int=' ', myItem: bool=False, csv: bool=False ) -> str:
    #Reference URL: https://github.com/Kaggle/kaggle-api#list-datasets
    sortByBool = fileSizeBool = fileTypeBool = licenseBool = tagBool = searchBool = userBool = pageBool = False 
    if search != ' ':
        searchBool = True
    if tags != ' ':
        tagBool = True
    if sortBy != ' ':
        sortByBool = True
    if fileSize != ' ':
        fileSizeBool = True
    if fileType != ' ':
        fileTypeBool = True
    if license != ' ':
        licenseBool = True
    if user != ' ':
        user = True
    if pageNum != ' ':
        pageNum = True

    command = ('kaggle datasets list' 
        + sortByBool*(' --sort-by ' + sortBy)
        + fileSizeBool*(' --size ' + fileSize) 
        + fileTypeBool*(' --file-type ' + fileType) 
        + licenseBool*(' --license ' + license) 
        + tagBool*(' --tags ' + (str(tags)).strip(r")(").replace(r"'",'').replace(' ','')
        + searchBool*(' -s ' + search) 
        + myItem*(' -m ') 
        + userBool*(' --user ' + user) 
        + pageBool*(' -p ' + str(pageNum)) )
        + csv*(' -v')
    )
    return command    

def kaggleRecentVersionNum(dataOwner: str='rsrishav', dataName: str='youtube-trending-video-dataset', proxy:dict='') -> int:
    #This method is intended to be temporary until the Kaggle metadata API retrival bug is fixed.
    metadataURL = r'https://www.kaggle.com/' + dataOwner + r'/' + dataName + r'/metadata'
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    pageRequest = requests.get(metadataURL, proxies=proxy, headers=headers)
    versionRegex = re.compile(r'Version (\d+)')
    versionList = versionRegex.findall(pageRequest.text)
    return max(set(versionList))

def kaggleRecentVersionDate(dataOwner: str='rsrishav', dataName: str='youtube-trending-video-dataset', proxy:dict='') -> str:
    #This method is intended to be temporary until the Kaggle metadata API retrival bug is fixed.
    #This function assumes the most recent date posted on metadata is the version's last update date.
    metadataURL = r'https://www.kaggle.com/' + dataOwner + r'/' + dataName + r'/metadata'
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    pageRequest = requests.get(metadataURL, proxies=proxy, headers=headers)
    dateRegex = re.compile(r'(\d{4})-(\d\d)-(\d\d)')
    dateList = dateRegex.findall(pageRequest.text)
    maxNumericDate = maxElement = -1
    for i in dateList: 
        numericDate = int(''.join(i))
        if numericDate > maxNumericDate:
            maxNumericDate = numericDate
            maxElement = i
    recentDate = '-'.join(maxElement)
    return recentDate

if __name__ == '__main__':
    pass