#!/user/bin/python3.9.1
import os, logging, time, csv
    #Logging Docs: https://docs.python.org/3/library/logging.html
    #CSV Docs: https://docs.python.org/3/library/csv.html
    #Time Docs: https://docs.python.org/3/library/time.html
from kaggle_API import kaggleDownloadCmd, kaggleRecentVersionDate

############################(Configurations - Start)############################
global KAGGLE_DATASETS_URL_LIST, KAGGLE_DATASETS_LOCATION, KAGGLE_REMOVE_JSON
KAGGLE_DATASETS_URL_LIST = [ 
        #Desc: These are the datasets you want to auto-download.
        #Note: Please ensure your URL list matches the same formatting.
        'https://www.kaggle.com/rsrishav/youtube-trending-video-dataset',
        'https://www.kaggle.com/gauravduttakiit/covid-19',
        'https://www.kaggle.com/paultimothymooney/coronavirus-in-italy',
        'https://www.kaggle.com/gpreda/all-covid19-vaccines-tweets',
        'https://www.kaggle.com/gpreda/pfizer-vaccine-on-reddit',
        'https://www.kaggle.com/shivamb/netflix-shows',
        'https://www.kaggle.com/gpreda/reddit-wallstreetsbets-posts',
        'https://www.kaggle.com/shivkumarganesh/politifact-factcheck-data',
        'https://www.kaggle.com/aaron7sun/stocknews',
        'https://www.kaggle.com/jealousleopard/goodreadsbooks',
        'https://www.kaggle.com/dhruvildave/wikibooks-dataset',
        #'https://www.kaggle.com/imsparsh/musicnet-dataset',
        'https://www.kaggle.com/datasnaek/chess',
        'https://www.kaggle.com/shivamb/netflix-shows',
        'https://www.kaggle.com/unsdsn/world-happiness',
        'https://www.kaggle.com/arashnic/hr-analytics-job-change-of-data-scientists',
        'https://www.kaggle.com/tencars/392-crypto-currency-pairs-at-minute-resolution',
        'https://www.kaggle.com/antgoldbloom/covid19-data-from-john-hopkins-university',
        'https://www.kaggle.com/new-york-state/nys-currently-licensed-real-estate-appraisers',
        'https://www.kaggle.com/new-york-state/nys-city-of-albany-building-permits-issued',
        'https://www.kaggle.com/sobhanmoosavi/us-accidents'
        ]
KAGGLE_DATASETS_LOCATION = r'Archive' #Relative file path to working directory.
UNZIP_DATASETS = True #Unzip AFTER downloading .zip file. Includes parallelism/concurrency. 
CONSOLE_OUTPUT = False
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
        
##ToDo:
# Finish logging. 
# Add feature to check if contained .zip was fully downloaded or interrupted
    #based off logging? based off posted file size online? 
# Add optional console output
# re-organize default list to sort by smallest file size
# print start and finish times & filesize
# check if works on linux
   
def main():
    logging.basicConfig(path=r'Source', filename=r'archive.log')
    #add console file handler
    #add file file handler
    







    #Converting config's URL list to convenient datastructure.
    trackedDatasets = []
    for i in KAGGLE_DATASETS_URL_LIST:
        trackedDatasets.append(extractURLData(i))

######################(CSV Version Control / Auto-Updater)######################    
    for datasetName, datasetAuthor in trackedDatasets:        
        individualDatasetLocation = os.path.join(KAGGLE_DATASETS_LOCATION,datasetName)
        #! Mark process start here

        #Note: Date naming convention is YYYY-MM-DD
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
            os.system(kaggleDownloadCmd(kaggleSourceName, newDateFolderPath, unzip=UNZIP_DATASETS)) 
        #! Mark process end here
        time.sleep(5) #Prevent API spam

if __name__ == '__main__':
    os.system('cls')
    main()
