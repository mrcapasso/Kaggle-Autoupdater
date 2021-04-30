#     License Type: GNU General Public License v3.0
#     'Kaggle Autoupdater', automated file version control for Kaggle.
#     Copyright (C) 2021 Matteo Capasso (matteo@capasso.dev)

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os, sys

def requirementsDisplay(pythonVersion:str) -> str: 
    requirments = f'''
    REQUIRMENTS -- Kaggle Autoupdater: 
    1) Python3 v{pythonVersion} or greater.

    2) Kaggle Module Installation 

    3) Valid Kaggle API Token (very quick setup)
       https://www.kaggle.com/docs/api#authentication
    '''
    return requirments

def licenseDisplay() -> str: 
    license = '''
    Kaggle Autoupdater Copyright (C) 2021 Matteo Capasso
    Email: matteo@capasso.dev

    License: GNU General Public License v3.0
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under certain conditions. See source files for details.
    '''
    return license

def kaggleModuleAndTokenExistence() -> bool:
    try: 
        import kaggle
        return True
    except ModuleNotFoundError: #Happens with no module.
        return False
    except OSError: #Happens with invalid token.
        return False

#Note, same functionality included in the above function.
def kaggleTokenExistence(drive: str='C:\\') -> bool:
    '''Checks for kaggle API token based on standard download configs.

    Args:
        mainStorageDrive (str): Main drive where user's 

    Returns:
        Tuple of strings where: 
        (Kaggle dataset's Name, Kaggle dataset's Author) 
    
    '''
    APILocation = os.path.join(drive, 'Users', os.getlogin(), '.kaggle')
    kaggleToken = r'kaggle.json'
    if os.path.exists(os.path.join(APILocation, kaggleToken)):
        return True
    else:
        return False

def pythonVersionValidate(majorVersion:int, minorVersion:int, microVersion:int, moreRecent:bool=True) -> bool: 
    #E.g.: Python version 3.9.1 means: major=3, minor=9, micro=1
    #sys.version_info(major=3, minor=9, micro=1, releaselevel='final', serial=0)
    #moreRecent (bool): Accept versions coming after the required version.
    downloadedVersion = sys.version_info
    if moreRecent == True:
        if downloadedVersion[0] < majorVersion:
            return False
        if downloadedVersion[1] < minorVersion:
            return False
        if downloadedVersion[2] < microVersion:
            return False
        return True
    else: 
        if downloadedVersion[0] != majorVersion:
            return False
        if downloadedVersion[1] != minorVersion:
            return False
        if downloadedVersion[2] != microVersion:
            return False
        return True

def approxProgramRuns() -> int:
    logPath = os.path.abspath('Logs')
    if os.path.isdir(logPath) == True:
        logDir = os.listdir(logPath)
        demoFiles = 1
        return len(logDir) - demoFiles
    else:
        raise AssertionError('No log directory found.')

if __name__ == '__main__':
    raise AssertionError('Missguided call -- this is not the main function.')