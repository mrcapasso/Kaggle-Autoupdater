#!/user/bin/python3.9.1
import os, logging, time, csv
from kaggle_API import kaggleDownloadCmd, kaggleRecentVersionDate

############################(Configurations - Start)############################
global KAGGLE_DATASETS_URL_LIST, KAGGLE_DATASETS_LOCATION, KAGGLE_REMOVE_JSON
global UNZIP_DATASETS, CONSOLE_TEXT_OUTPUT
KAGGLE_DATASETS_URL_LIST = [ 
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
KAGGLE_DATASETS_LOCATION = r'Archive'
UNZIP_DATASETS = True
CONSOLE_TEXT_OUTPUT = True
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
# re-organize default list to sort by smallest file size first
# make sure '/' at end of URL doesnt break program
# terminate program if too many failed online checks
# loop online check for program in case of network issue
# create folder for logs based on date
# check if works on linux
   
def main():
    ############################(Program Logging - Start)###########################
    #Logging Configs
    logger = logging.getLogger('__main__')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # File Logging
    fh = logging.FileHandler(os.path.join('Source','__main__.log'))
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # Console Logging
    if CONSOLE_TEXT_OUTPUT == True:
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    ##############################(Program Logging - End)###########################

    logging.info('Program start. UNZIP_DATASETS: ' + str(UNZIP_DATASETS))

    #Converting config's URL list to convenient datastructure.
    try:
        trackedDatasets = []
        for i in KAGGLE_DATASETS_URL_LIST:
            trackedDatasets.append(extractURLData(i))
    except:
        logging.critical(f"Invalid URL entry: {i}")

    ######################(CSV Version Control / Auto-Updater)######################    
    for datasetName, datasetAuthor in trackedDatasets:        
        logger.debug(f"Initiating process: {datasetName}/{datasetAuthor}")
        individualDatasetLocation = os.path.join(KAGGLE_DATASETS_LOCATION,datasetName)
        #! Mark process start here

        #Note: Date naming convention is YYYY-MM-DD
        try: #Checking online version's latest date.
            kaggleOnlineVersion = kaggleRecentVersionDate(datasetAuthor,datasetName)
        except:
            logger.critical(f"Unable to retrieve online version: {datasetName}/{datasetAuthor}")
            time.sleep(30)
            continue

        kaggleOfflineVersion = -1
        try: #Checking for existence of previous dataset installations.
            if len(os.listdir(individualDatasetLocation)) != 0:
                kaggleOfflineVersion = max(set(os.listdir(individualDatasetLocation)))
        except:
            logger.error(f"Unable to retrieve offline version: {datasetName}/{datasetAuthor}")
            pass

        if kaggleOnlineVersion != kaggleOfflineVersion:
            logger.info(f"Outdated version: {datasetName}/{datasetAuthor}")
            newDateFolderPath = os.path.join(individualDatasetLocation, kaggleOnlineVersion)
            os.makedirs(newDateFolderPath)
            kaggleSourceName = datasetAuthor + '/' + datasetName
            logger.info(f"Starting download: {datasetName}/{datasetAuthor}")
            os.system(kaggleDownloadCmd(kaggleSourceName, newDateFolderPath,
            quiet=CONSOLE_TEXT_OUTPUT, unzip=UNZIP_DATASETS)) 
            logger.info(f"Finished download: {datasetName}/{datasetAuthor}")
        else:
            logger.info(f"Files up-to-date: {datasetName}/{datasetAuthor}")
        logger.debug(f"Ending process: {datasetName}/{datasetAuthor}")
        time.sleep(15) #Prevent website spam.
    logging.info('Program end.')

if __name__ == '__main__':
    try: #Refreshs logs each run.
        os.unlink(os.path.join('Source','__main__.log'))
    except:
        pass
    os.system('cls')
    main()
