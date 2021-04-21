#!/user/bin/python3.9.1
import os, logging, time, csv
    #Logging Docs: https://docs.python.org/3/library/logging.html
    #CSV Docs: https://docs.python.org/3/library/csv.html
    #Time Docs: https://docs.python.org/3/library/time.html
from kaggle_API import kaggleDownloadCmd, kaggleRecentVersionDate

############################(Configurations - Start)############################
global KAGGLE_DATASETS_URL_LIST, KAGGLE_DATASETS_LOCATION, KAGGLE_REMOVE_JSON
KAGGLE_DATASETS_URL_LIST = [ #Please ensure your URL list matches the same formatting.
        'https://www.kaggle.com/rashikrahmanpritom/heart-attack-analysis-prediction-dataset',
        'https://www.kaggle.com/ajaypalsinghlo/world-happiness-report-2021',
        'https://www.kaggle.com/iabhishekofficial/mobile-price-classification',
        'https://www.kaggle.com/gpreda/reddit-vaccine-myths'
        ]
KAGGLE_DATASETS_LOCATION = r'Archive' #Default is relative file path to working directory.
KAGGLE_REMOVE_JSON = False
#############################(Configurations - End)#############################

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
        
#! NOTE: Class use ommitted at time of creation b/c Kaggle metadata API is not fixed yet.
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
    #Converting config URL list to convenient datastructure.
    trackedDatasets = []
    for i in KAGGLE_DATASETS_URL_LIST:
        trackedDatasets.append(extractURLData(i))

######################(CSV Version Control / Auto-Updater)######################
    #Note: Date naming convention is YYYY-MM-DD
    for datasetName, datasetAuthor in trackedDatasets:        
        individualDatasetLocation = os.path.join(KAGGLE_DATASETS_LOCATION,datasetName)
        print('Individual dataset location: ' + individualDatasetLocation)#temp

        try: #Checking online version's latest date.
            kaggleOnlineVersion = kaggleRecentVersionDate(datasetAuthor,datasetName)
        except:
            print('Error encountered on retrieving online recent version date.')
            print('Moving to next kaggle dataset.')
            time.sleep(5)
            continue

        kaggleOfflineVersion = -1
        try: #Checking for existence of previous dataset installations.
            if len(os.listdir(individualDatasetLocation)) != 0:
                kaggleOfflineVersion = max(set(os.listdir(individualDatasetLocation)))
        except:
            pass

        if kaggleOnlineVersion != kaggleOfflineVersion:
            newDateFolderPath = os.path.join(individualDatasetLocation, kaggleOnlineVersion)
            os.makedirs(newDateFolderPath)
            kaggleSourceName = datasetAuthor + '/' + datasetName
            os.system(kaggleDownloadCmd(kaggleSourceName, newDateFolderPath, unzip=True))
            #Note: kaggle unzipping uses parrallelism/concurrency natively. 

        time.sleep(5) #Prevent API spam

if __name__ == '__main__':
    main()
