import os, logging, time, csv
    #Logging Docs: https://docs.python.org/3/library/logging.html
    #CSV Docs: https://docs.python.org/3/library/csv.html
    #Time Docs: https://docs.python.org/3/library/time.html
from kaggle_API import kaggleDownloadCmd, kaggleListsCmd, kaggleRecentVersionNum, kaggleRecentVersionDate
    
def main():
    KAGGLE_DATASETS_LOCATION = r'Archive\youtube-trending-video-dataset'
    KAGGLE_SRC_NAME = r'rsrishav/youtube-trending-video-dataset'
    KAGGLE_REMOVE_JSON = True

######################(CSV Version Control / Auto-Updater)######################
    #Note: Date naming convention is YYYY-MM-DD
    try:
        kaggleOnlineVersion = kaggleRecentVersionDate()
    except:
        pass #! Log failure here.
    kaggleOfflineVersion = -1
    try: #Checking for existence of previous install
        if len(os.listdir(KAGGLE_DATASETS_LOCATION)) != 0:
            kaggleOfflineVersion = max(set(os.listdir(KAGGLE_DATASETS_LOCATION)))
    except:
        pass
    if kaggleOnlineVersion != kaggleOfflineVersion:
        newDateFolderPath = os.path.join(KAGGLE_DATASETS_LOCATION, kaggleOnlineVersion)
        os.makedirs(newDateFolderPath)
        os.system(kaggleDownloadCmd(KAGGLE_SRC_NAME, newDateFolderPath, unzip=True))
        if KAGGLE_REMOVE_JSON == True:
            extractedFiles = os.listdir(newDateFolderPath)
            for file in extractedFiles:
                if file[-5:] == r'.json':
                   os.unlink(os.path.join(newDateFolderPath, file)) 

########################(Dataset Parallelism Preparation)#######################
    #CSV Docs:
        #Module Contents: https://docs.python.org/3/library/csv.html#module-contents
        #Reader Objects: https://docs.python.org/3/library/csv.html#reader-objects
        #Writer Objects: https://docs.python.org/3/library/csv.html#writer-objects
        #Line by Line demo: https://docs.python.org/3/library/csv.html#id3
        #Cons: No append feature, no native parallelism, line by line only.
        #Pros: csv to dictionaries, popular
        
    #CSV? or RegEx for more general solution? 

if __name__ == '__main__':
    main()