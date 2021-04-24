#!/user/bin/python3.9.1
import os, logging, time, csv
from kaggle_API import kaggleDownloadCmd, kaggleRecentVersionDate
from utility import elapsedTimeCalculator, extractURLData, folderSizeAmount, byteUnitConverter

############################(Configurations - Start)############################
global KAGGLE_DATASETS_URL_LIST, KAGGLE_DATASETS_LOCATION, KAGGLE_REMOVE_JSON
global UNZIP_DATASETS, CONSOLE_TEXT_OUTPUT, SLEEP_TIME
KAGGLE_DATASETS_URL_LIST = [ 
        #Note: Please ensure your URL list matches the same formatting.
        #Format: https://www.kaggle.com/<author>/<datasetname>
        'https://www.kaggle.com/rsrishav/youtube-trending-video-dataset', #CC0 1.0 Universal (CC0 1.0)
        'https://www.kaggle.com/hgultekin/covid19-stream-data', #Database Contents License (DbCL) v1.0
        'https://www.kaggle.com/cityofLA/los-angeles-parking-citations', #Open Data Commons Open Database License (ODbL) v1.0
        'https://www.kaggle.com/chaibapat/slogan-dataset', #Database Contents License (DbCL) v1.0
        'https://www.kaggle.com/camnugent/sandp500', #CC0 1.0 Universal (CC0 1.0)
        'https://www.kaggle.com/dhruvildave/github-commit-messages-dataset' #Open Data Commons Attribution License (ODC-By) v1.0
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
        'https://www.kaggle.com/imsparsh/musicnet-dataset',
        'https://www.kaggle.com/datasnaek/chess',
        'https://www.kaggle.com/shivamb/netflix-shows',
        'https://www.kaggle.com/unsdsn/world-happiness',
        'https://www.kaggle.com/arashnic/hr-analytics-job-change-of-data-scientists',
        'https://www.kaggle.com/tencars/392-crypto-currency-pairs-at-minute-resolution',
        'https://www.kaggle.com/antgoldbloom/covid19-data-from-john-hopkins-university',
        'https://www.kaggle.com/new-york-state/nys-currently-licensed-real-estate-appraisers',
        'https://www.kaggle.com/new-york-state/nys-city-of-albany-building-permits-issued',
        'https://www.kaggle.com/sobhanmoosavi/us-accidents',
        'https://www.kaggle.com/gpreda/covid-world-vaccination-progress',
        'https://www.kaggle.com/arthurio/italian-vaccination',
        'https://www.kaggle.com/kaggle/meta-kaggle',
        'https://www.kaggle.com/dhruvildave/github-commit-messages-dataset',
        'https://www.kaggle.com/yamaerenay/spotify-dataset-19212020-160k-tracks',
        'https://www.kaggle.com/fireballbyedimyrnmom/us-counties-covid-19-dataset',
        'https://www.kaggle.com/dhruvildave/billboard-the-hot-100-songs',
        'https://www.kaggle.com/komalkhetlani/population-growth-annual',
        'https://www.kaggle.com/austinreese/craigslist-carstrucks-data',
        'https://www.kaggle.com/paultimothymooney/stock-market-data',
        'https://www.kaggle.com/brendan45774/hollywood-most-profitable-stories',
        'https://www.kaggle.com/dhruvildave/top-play-store-games',
        ]
KAGGLE_DATASETS_LOCATION = r'Archive'
UNZIP_DATASETS = True
CONSOLE_TEXT_OUTPUT = True
SLEEP_TIME = 10
#############################(Configurations - End)#############################
        
##ToDo:
# create folder for logs based on date
# documentation polish up
# amt of data added
# verify offline error logging is fixed
# check if works on linux
   
def main():
    startTime = time.time()
    ###########################(Program Logging - Start)###########################
    #Logging Configs
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('__main__')
    logger.propagate = CONSOLE_TEXT_OUTPUT
    logger.setLevel(logging.DEBUG)
    
    #File Logging
    fh = logging.FileHandler(os.path.join('Source','__main__.log'))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    ##############################(Program Logging - End)###########################

    startSize = folderSizeAmount(os.path.abspath(KAGGLE_DATASETS_LOCATION))
    logger.info('##############(Program Start)###########')

    #Converting config's URL list to convenient datastructure.
    try:
        trackedDatasets = []
        for i in KAGGLE_DATASETS_URL_LIST:
            trackedDatasets.append(extractURLData(i))
    except:
        logging.critical(f"Invalid URL entry: {i}")

    ######################(CSV Version Control / Auto-Updater)######################    
    failedOnlineRetrivalCounter = 1
    failedOnlineRetrivalAttempts = 3
    for datasetName, datasetAuthor in trackedDatasets:        
        logger.debug(f"Initiating process: {datasetName}/{datasetAuthor}")
        individualDatasetLocation = os.path.join(KAGGLE_DATASETS_LOCATION,datasetName)

        #Checking online version's latest date.
        try: #Note: Date naming convention is YYYY-MM-DD
            kaggleOnlineVersion = kaggleRecentVersionDate(datasetAuthor,datasetName)
            year = 1000
            onlineDate = int(kaggleOnlineVersion.replace('-',''))
            todaysDate = int(time.strftime("%Y%m%d"))
            if todaysDate - onlineDate > year:
                logger.warning(f"Potential dataset depreciation: {datasetName}/{datasetAuthor}")
        except:
            if failedOnlineRetrivalCounter <= failedOnlineRetrivalAttempts: 
                failedOnlineRetrivalCounter += 1
                logger.critical(f"Unable to retrieve online version: {datasetName}/{datasetAuthor}")
                time.sleep(5**failedOnlineRetrivalCounter)
                continue
            else: 
                logger.critical(f"Max online retrival attempts reached, exiting.")
                break
        
        #Checking for existence of previous dataset installations by dates.
        kaggleOfflineVersion = -1
        try: 
            #Case if dataset folder exists, but is empty.
            if os.listdir(individualDatasetLocation) == []: 
                logger.info(f"New dataset: {datasetName}/{datasetAuthor}")
            #Finding most recent offline version by date of existing dataset folders.
            elif len(os.listdir(individualDatasetLocation)) != 0:
                kaggleOfflineVersion = max(set(os.listdir(individualDatasetLocation)))
        except:
            logger.error(f"Unable to retrieve offline version: {datasetName}/{datasetAuthor}")
            pass

        #Comparing online and offline versions, then downloading if necessary.
        if kaggleOnlineVersion != kaggleOfflineVersion:
            logger.info(f"Outdated version: {datasetName}/{datasetAuthor}")
            newDateFolderPath = os.path.join(individualDatasetLocation, kaggleOnlineVersion)
            os.makedirs(newDateFolderPath)
            kaggleSourceName = datasetAuthor + '/' + datasetName
            logger.info(f"Starting download: {datasetName}/{datasetAuthor}")
            os.system(kaggleDownloadCmd(kaggleSourceName, newDateFolderPath,
            quiet=not(CONSOLE_TEXT_OUTPUT), unzip=UNZIP_DATASETS)) 
            logger.info(f"Finished download: {datasetName}/{datasetAuthor}")
        else:
            logger.info(f"Files up-to-date: {datasetName}/{datasetAuthor}")
        logger.debug(f"Ending process: {datasetName}/{datasetAuthor}")
        logger.info(f"Sleeping: {SLEEP_TIME} seconds.")
        time.sleep(SLEEP_TIME) #Prevent too many requests at once.
    endTime = time.time()
    endSize = folderSizeAmount(os.path.abspath(KAGGLE_DATASETS_LOCATION))
    sizeDifference = endSize - startSize #This is in bytes
    logger.info('##############(Program End)#############')
    logger.info(f"Elapsed time: {elapsedTimeCalculator(startTime,endTime)}")
    logger.info(f"Added data: {byteUnitConverter(sizeDifference)}.")

if __name__ == '__main__':
    # try: #Refreshs logs each run.
    #     os.unlink(os.path.join('Source','__main__.log'))
    # except:
    #     pass
    os.system('cls')
    main()
