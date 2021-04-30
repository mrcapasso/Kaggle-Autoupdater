#* Note: These function require a valid Kaggle API token and kaggle module.  
    #* API Token Link: https://www.kaggle.com/docs/api#authentication
    #* Kaggle Module Installation: 'pip install kaggle'
    #* Kaggle Module Documentation: https://github.com/Kaggle/kaggle-api
    
#     License Type: GNU General Public License v3.0
#     'Kaggle Autoupdater', automated file version control for Kaggle.
#     Copyright (C) 2021 Matteo Capasso (matteo@capasso.dev)

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

import kaggle, os, re, requests

def kaggleDownloadCmd(dataset, downloadPath, fileName: str=None, unzip: bool=False, force: bool=False, quiet: bool=False) -> str:
    '''Generates download CLI string for use with kaggle module and kaggle API.
    
    Args: 
        dataset (str): Name of the desired dataset to download. 
        downloadPath (str): Rel. or abs. file path for download location, defaults to working directory.
        fileName (str): Specific file in dataset to download, defaults to downloading all files.  
        unzip (bool): Unzips the downloaded file. Will delete the zip file when completed.
        force (bool): Forces file download regardless of local version redundancy.
        quiet (bool): Suppress console output of download status. 

    Returns: 
        CLI string to download kaggle datasets with designated parameters. 

    Reference: 
        https://github.com/Kaggle/kaggle-api#download-dataset-files

    Notes: 
        Unzip feature conflicts with kaggle module redundant file checking.
    
    '''
    if fileName == None: 
        i = False
    else: 
        i = True
    command = ('kaggle datasets download'
            + i*(' -f ' + str(fileName))
            + (' -p ' + str(downloadPath))
            + (' --unzip ')*unzip
            + (' -o ')*force
            + (' -q ')*quiet
            + ' ' + str(dataset)
         )
    return command

def kaggleListsCmd(search: str, tags: list, sortBy=' ', fileSize:str=' ', fileType:str=' ', license=' ', user=' ', pageNum: int=' ', myItem: bool=False, csv: bool=False ) -> str:
    '''Generates CLI string for listing kaggle datasets, used with kaggle module and kaggle API.
    
    Args:
        search (str): Parameter to search kaggle dataset archive by.
        tags (list): Kaggle tags to filter by -- ensure they are comma seperated.
        sortBy (str): Options to sort by: 'hottest', 'votes, 'updated', 'active'.
        fileSize (str): File sizes to filter by: 'all', 'small', 'medium', 'large'.
        fileType (str): File types to filter by: 'all', 'csv', 'sqlite', 'json', 'bigQuery'.
        license (str): Dataset licenses to filter by: 'all', 'cc', 'gpl', 'odb', 'other'.
        user (str): Kaggle user to search by.
        pagnum (int): Amount of page numbers to list, default is 20.
        myItem (bool): Only display my items.
        csv (bool): Print results in CSV, default is tabular format. 

    Returns:
        String to be used in CLI for listing kaggle datasets of provided filters.

    Reference: 
        https://github.com/Kaggle/kaggle-api#list-datasets

    Notes: 
        Big query datasets cannot be downloaded. 
    
    '''

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

def kaggleRecentVersionNum(dataOwner: str, dataName: str, proxy:dict='') -> int:
    '''Obtains Kaggle dataset version number via 'requests' and 'regex' modules.

    *This is a temporary solution until Kaggle's API metadata issue is fixed.*
    
    Args:
        dataOwner (str): Author of the desired dataset.
        dataName (str): Desired dataset's name.
        proxy (dict): Requires advance configuration, see notes below.

    Returns:
        Returns an int with kaggle dataset's specific version number.

    Notes: 
        Proxy: https://docs.python-requests.org/en/master/user/advanced/#proxies
    
    '''
    metadataURL = r'https://www.kaggle.com/' + dataOwner + r'/' + dataName + r'/metadata'
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    pageRequest = requests.get(metadataURL, proxies=proxy, headers=headers)
    versionRegex = re.compile(r'Version (\d+)')
    versionList = versionRegex.findall(pageRequest.text)
    return max(set(versionList))

def kaggleRecentVersionDate(dataOwner: str, dataName: str, proxy:dict='') -> str:
    '''Obtains Kaggle dataset version date via 'requests' and 'regex' modules.

    *This is a temporary solution until Kaggle's API metadata issue is fixed.*
    
    Args:
        dataOwner (str): Author of the desired dataset.
        dataName (str): Desired dataset's name.
        proxy (dict): Requires advance configuration, see notes below.

    Returns:
        Returns a str with kaggle dataset's latest version release date. 

    Notes: 
        Proxy: https://docs.python-requests.org/en/master/user/advanced/#proxies
        Function assumes latest date shown on webpage is the version's last update date.
    
    '''
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
    raise AssertionError('Missguided call -- this is not the main function.')