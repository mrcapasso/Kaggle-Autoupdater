def kaggleTokenExistence(drive: str='C:\\') -> bool:
    '''Checks for kaggle API token based on standard download configs.

    Args:
        mainStorageDrive (str): Main drive where user's 

    Returns:
        Tuple of strings where: 
        (Kaggle dataset's Name, Kaggle dataset's Author) 
    
    '''
    normalAPILocation = os.path.join(drive, 'Users', os.getlogin(), '.kaggle')
    kaggleToken = r'kaggle.json'
    if os.path.exists(os.path.join(drive, kaggleToken)):
        return True
    else:
        return False
