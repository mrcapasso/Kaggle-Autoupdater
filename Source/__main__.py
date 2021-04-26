#!/user/bin/python3.9.1
import os, sys, logging, time, csv
from kaggle_API import kaggleDownloadCmd, kaggleRecentVersionDate
from utility import elapsedTimeCalculator, extractURLData, folderSizeAmount, byteUnitConverter
        
##ToDo:
# create folder for logs based on date
# add datasets location pre-check
# documentation polish up
# check if works on linux
   
def main():
    startTime = time.time()

    ############################(Configurations - Start)############################
    KAGGLE_DATASETS_URL_LIST = [ 
            #Note: Please ensure your URL list matches the same formatting.
            #Format: https://www.kaggle.com/<author>/<datasetname>
            #'https://www.kaggle.com/rsrishav/youtube-trending-video-dataset', #CC0 1.0 Universal (CC0 1.0)
            #'https://www.kaggle.com/hgultekin/covid19-stream-data', #Database Contents License (DbCL) v1.0
            #'https://www.kaggle.com/cityofLA/los-angeles-parking-citations', #Open Data Commons Open Database License (ODbL) v1.0
            #'https://www.kaggle.com/chaibapat/slogan-dataset', #Database Contents License (DbCL) v1.0
            #'https://www.kaggle.com/camnugent/sandp500', #CC0 1.0 Universal (CC0 1.0)
            #'https://www.kaggle.com/dhruvildave/github-commit-messages-dataset' #Open Data Commons Attribution License (ODC-By) v1.0
            # 'https://www.kaggle.com/gauravduttakiit/covid-19',
            # 'https://www.kaggle.com/paultimothymooney/coronavirus-in-italy',
            # 'https://www.kaggle.com/gpreda/all-covid19-vaccines-tweets',
            # 'https://www.kaggle.com/gpreda/pfizer-vaccine-on-reddit',
            # 'https://www.kaggle.com/shivamb/netflix-shows',
            # 'https://www.kaggle.com/gpreda/reddit-wallstreetsbets-posts',
            # 'https://www.kaggle.com/shivkumarganesh/politifact-factcheck-data',
            # 'https://www.kaggle.com/aaron7sun/stocknews',
            # 'https://www.kaggle.com/jealousleopard/goodreadsbooks',
            # 'https://www.kaggle.com/dhruvildave/wikibooks-dataset',
            # 'https://www.kaggle.com/imsparsh/musicnet-dataset',
            # 'https://www.kaggle.com/datasnaek/chess',
            # 'https://www.kaggle.com/shivamb/netflix-shows',
            # 'https://www.kaggle.com/unsdsn/world-happiness',
            # 'https://www.kaggle.com/arashnic/hr-analytics-job-change-of-data-scientists',
            # 'https://www.kaggle.com/tencars/392-crypto-currency-pairs-at-minute-resolution',
            # 'https://www.kaggle.com/antgoldbloom/covid19-data-from-john-hopkins-university',
            # 'https://www.kaggle.com/new-york-state/nys-currently-licensed-real-estate-appraisers',
            # 'https://www.kaggle.com/new-york-state/nys-city-of-albany-building-permits-issued',
            # 'https://www.kaggle.com/sobhanmoosavi/us-accidents',
            # 'https://www.kaggle.com/gpreda/covid-world-vaccination-progress',
            'https://www.kaggle.com/arthurio/italian-vaccination',
            # 'https://www.kaggle.com/kaggle/meta-kaggle',
            # 'https://www.kaggle.com/dhruvildave/github-commit-messages-dataset',
            # 'https://www.kaggle.com/yamaerenay/spotify-dataset-19212020-160k-tracks',
            'https://www.kaggle.com/fireballbyedimyrnmom/us-counties-covid-19-dataset',
            # 'https://www.kaggle.com/dhruvildave/billboard-the-hot-100-songs',
            # 'https://www.kaggle.com/komalkhetlani/population-growth-annual',
            # 'https://www.kaggle.com/austinreese/craigslist-carstrucks-data',
            # 'https://www.kaggle.com/paultimothymooney/stock-market-data',
            # 'https://www.kaggle.com/brendan45774/hollywood-most-profitable-stories',
            # 'https://www.kaggle.com/dhruvildave/top-play-store-games',
            ]
    KAGGLE_DATASETS_LOCATION = r'Archive'
    UNZIP_DATASETS = False
    CONSOLE_TEXT_OUTPUT = True
    SLEEP_TIME = 10 #Do not recommend lowering below 10 seconds. 
    #############################(Configurations - End)#############################


    ###########################(Program Logging - Start)###########################
    #Logging Configurations
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('__main__')
    logger.propagate = CONSOLE_TEXT_OUTPUT
    logger.setLevel(logging.DEBUG)
    
    #File Specific Logging Configurations
    fh = logging.FileHandler(os.path.join('Source','__main__.log'))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    ##############################(Program Logging - End)###########################


    ###pre-check and pre-processing start
    #Changing rel file path from configs to abs file path for use in I/O operations.
    if os.path.isabs(KAGGLE_DATASETS_LOCATION) == False:
        KAGGLE_DATASETS_LOCATION = os.path.abspath(KAGGLE_DATASETS_LOCATION)

    startSize = folderSizeAmount(os.path.abspath(KAGGLE_DATASETS_LOCATION))
    logger.info('##############(Program Start)###########')

    #Converting config's URL list to convenient datastructure.
    try:
        trackedDatasets = []
        for i in KAGGLE_DATASETS_URL_LIST:
            trackedDatasets.append(extractURLData(i))
    except:
        logger.error(f"[Line: {sys.exc_info()[-1].tb_lineno}] [Problem: {sys.exc_info()[1]}]")
        logger.critical(f"Likely URL typo for: {i}")
    ###pre-check and pre-processing end


    ######################(CSV Version Control / Auto-Updater)######################    
    failedOnlineRetrivalCounter = 1
    failedOnlineRetrivalAttempts = 3
    timerPosition = 0
    for datasetName, datasetAuthor in trackedDatasets:        
        logger.debug(f"Initiating process: {datasetName}/{datasetAuthor}")

        try: #Checking online version's latest date.
            #Note: Date naming convention is YYYY-MM-DD
            kaggleOnlineVersion = kaggleRecentVersionDate(datasetAuthor,datasetName)
            onlineDate = int(kaggleOnlineVersion.replace('-',''))
            todaysDate = int(time.strftime("%Y%m%d"))
            if todaysDate - onlineDate > 1000: #'1000' is a year's time.
                logger.warning(f"Potential dataset depreciation: {datasetName}/{datasetAuthor}")
        except: #Robust error handling in case of network instability. 
            if failedOnlineRetrivalCounter <= failedOnlineRetrivalAttempts: 
                failedOnlineRetrivalCounter += 1
                logger.error(f"[Line: {sys.exc_info()[-1].tb_lineno}] [Problem: {sys.exc_info()[1]}]")
                logger.critical(f"Unable to retrieve online version: {datasetName}/{datasetAuthor}")
                time.sleep(5**failedOnlineRetrivalCounter)
                continue
            else: 
                logger.error(f"[Line: {sys.exc_info()[-1].tb_lineno}] [Problem: {sys.exc_info()[1]}]")
                logger.critical(f"Max online retrival attempts reached, exiting.")
                time.sleep(5)
                sys.exit()
        
        try: #Checking offline version's latest date.
            kaggleOfflineVersion = -1
            individualDatasetPath = os.path.join(KAGGLE_DATASETS_LOCATION,datasetName)
            #Case if dataset folder exists, but is empty.
            if os.listdir(KAGGLE_DATASETS_LOCATION) == []:
                logger.info(f"New dataset: {datasetName}/{datasetAuthor}")
            elif len(os.listdir(individualDatasetPath)) != 0: #Comparing sub-folder dates.
                #Note: Date naming convention is YYYY-MM-DD
                kaggleOfflineVersion = max(set(os.listdir(individualDatasetPath)))
        except:
            logger.critical(f"[Line: {sys.exc_info()[-1].tb_lineno}] [Problem: {sys.exc_info()[1]}]")

        try: #Comparing online and offline versions, then downloading via API if necessary.
            if kaggleOnlineVersion != kaggleOfflineVersion:
                logger.info(f"Outdated version: {datasetName}/{datasetAuthor}")
                newDateFolderPath = os.path.join(individualDatasetPath, kaggleOnlineVersion) 
                os.makedirs(newDateFolderPath)
                kaggleSourceName = datasetAuthor + '/' + datasetName
                logger.info(f"Starting download: {datasetName}/{datasetAuthor}")
                os.system(kaggleDownloadCmd(kaggleSourceName, newDateFolderPath,
                quiet=not(CONSOLE_TEXT_OUTPUT), unzip=UNZIP_DATASETS)) 
                logger.info(f"Finished download: {datasetName}/{datasetAuthor}")
            else:
                logger.info(f"Files up-to-date: {datasetName}/{datasetAuthor}")
        except:
            logger.critical(f"[Line: {sys.exc_info()[-1].tb_lineno}] [Problem: {sys.exc_info()[1]}]")
        
        logger.debug(f"Ending process: {datasetName}/{datasetAuthor}")        
        
        #Sleeping to prevent API spam.
        timerPosition += 1
        if timerPosition < len(trackedDatasets):
            logger.info(f"Sleeping: {SLEEP_TIME} seconds.")
            time.sleep(SLEEP_TIME)

    endTime = time.time()
    endSize = folderSizeAmount(os.path.abspath(KAGGLE_DATASETS_LOCATION))
    sizeDifference = endSize - startSize #These units are in bytes.
    logger.info('##############(Program End)#############')
    logger.info(f"Elapsed time: {elapsedTimeCalculator(startTime,endTime)}")
    logger.info(f"Added data: {byteUnitConverter(sizeDifference)}.")

if __name__ == '__main__':
    try: #Refreshs logs each run.
        os.unlink(os.path.join('Source','__main__.log'))
    except:
        pass
    os.system('cls')
    main()
