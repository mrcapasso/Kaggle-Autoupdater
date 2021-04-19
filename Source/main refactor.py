import os, logging, time, csv
    #Logging Docs: https://docs.python.org/3/library/logging.html
    #CSV Docs: https://docs.python.org/3/library/csv.html
    #Time Docs: https://docs.python.org/3/library/time.html
from kaggle_API import kaggleDownloadCmd, kaggleListsCmd, kaggleRecentVersionNum, kaggleRecentVersionDate

#Read More at: https://docs.python.org/3/tutorial/classes.html#inheritance
#Research: https://docs.python.org/3/tutorial/modules.html#packages

class kaggleMetadadata:
    #Classes Example: https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
    #Classes Docs: https://docs.python.org/3/tutorial/classes.html
    #Kaggle Metadata Ex: https://www.kaggle.com/rashikrahmanpritom/heart-attack-analysis-prediction-dataset/metadata

    def __init__(self,author,license,updateFrequency,dateCreated,lastOnlineUpdate,lastOfflineUpdate,currentOnlineVersion,currentOfflineVersion): 
        #__init__ is a constructor for new object creation specific to class
        #self is used to show variables belong to this class
        #instaces are like states for a group (e.g. water is LIQUId, water is SOLID)
        self.author = author
        self.license = license
        self.updateFrequency = updateFrequency
        self.dateCreated = dateCreated
        self.lastOnlineUpdate = lastOnlineUpdate
        self.lastOfflineUpdate = lastOfflineUpdate
        self.currentOnlineVersion = currentOnlineVersion
        self.currentOfflineVersion = currentOfflineVersion
    
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