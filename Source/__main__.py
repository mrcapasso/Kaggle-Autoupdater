#!/user/bin/python3.9.1
import os, sys, logging, time, csv
from kaggle_API import kaggleDownloadCmd, kaggleRecentVersionDate
from utility import elapsedTimeCalculator, extractURLData, folderSizeAmount, byteUnitConverter
        
def main():
    startTime = time.time()

    ############################(Configurations - Start)############################
    KAGGLE_DATASETS_URL_LIST = [
            'https://www.kaggle.com/jealousleopard/goodreadsbooks', 
            'https://www.kaggle.com/shivamb/netflix-shows'
            ]
        #URL Format (required): https://www.kaggle.com/<author>/<datasetname>
    KAGGLE_DATASETS_LOCATION = r'Archive'
        #Relative or absolute file paths accepted.
    UNZIP_DATASETS = True
        #Note: unzipping is done after file download.
    CONSOLE_TEXT_OUTPUT = True
    SLEEP_TIME = 10 
        #Sleeping between each download, do not lower below 10 seconds. 
    #############################(Configurations - End)#############################


    ###########################(Program Logging - Start)###########################
    #General Logging Configurations
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('__main__')
    logger.propagate = CONSOLE_TEXT_OUTPUT
    logger.setLevel(logging.DEBUG)
    
    #File Specific Logging Configurations
    currentDate = f"{time.strftime('%Y-%m-%d')}"
    fh = logging.FileHandler(os.path.join('Logs',f"{currentDate}.log"))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    #Console Specific Logging Configurations
    if CONSOLE_TEXT_OUTPUT == True: 
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    ##############################(Program Logging - End)###########################


    ######################(Precheck and Preprocessing - Start)######################
    #Changing rel file path from configs to abs file path for use in I/O operations.
    if os.path.isabs(KAGGLE_DATASETS_LOCATION) == False:
        KAGGLE_DATASETS_LOCATION = os.path.abspath(KAGGLE_DATASETS_LOCATION)

    startSize = folderSizeAmount(KAGGLE_DATASETS_LOCATION)
    logger.info('#'*23 + f"(Program Start (Date: {currentDate}))" + '#'*23)

    #Converting config's URL list to convenient datastructure.
    try:
        trackedDatasets = []
        for i in KAGGLE_DATASETS_URL_LIST:
            trackedDatasets.append(extractURLData(i))
    except:
        logger.error(f"Problem: {sys.exc_info()[1]}")
        logger.critical(f"Likely URL typo for: {i}")
    #######################(Precheck and Preprocessing - End)#######################


    ######################(Version Control & Updating - Start)######################  
    failedOnlineRetrivalAttempts = 2 #Acts as three attempts.
    timerPosition = failedOnlineRetrivalCounter = 0
    for datasetName, datasetAuthor in trackedDatasets:        
        logger.debug(f"Initiating process: {datasetName}/{datasetAuthor}")

        try: #Checking online version's latest date.
            #Note: Date naming convention is YYYY-MM-DD
            kaggleOnlineVersion = kaggleRecentVersionDate(datasetAuthor,datasetName)
            onlineDate = int(kaggleOnlineVersion.replace('-',''))
            todaysDate = int(time.strftime("%Y%m%d"))
            if todaysDate - onlineDate > 1000: #1000 is a year's time in .strftime notation
                logger.warning(f"Potential dataset depreciation: {datasetName}/{datasetAuthor}")
        except: #Robust error handling in case of network instability. 
            if failedOnlineRetrivalCounter <= failedOnlineRetrivalAttempts: 
                failedOnlineRetrivalCounter += 1
                logger.error(f"Problem: {sys.exc_info()[1]}")
                logger.critical(f"Unable to retrieve online version: {datasetName}/{datasetAuthor}")
                time.sleep(5**failedOnlineRetrivalCounter)
                continue
            else: 
                logger.error(f"Problem: {sys.exc_info()[1]}")
                logger.critical(f"Max online retrival attempts reached, exiting.")
                break
        
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
            logger.critical(f"Problem: {sys.exc_info()[1]}")

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
            logger.critical(f"Problem: {sys.exc_info()[1]}")
    
        logger.debug(f"Ending process: {datasetName}/{datasetAuthor}")        
        
        #Sleeping to prevent API spam.
        timerPosition += 1
        if timerPosition < len(trackedDatasets):
            logger.debug(f"Sleeping: {SLEEP_TIME} seconds.")
            time.sleep(SLEEP_TIME)
    #######################(Version Control & Updating - End)#######################


    ############################(Postprocessing - Start)############################
    endTime = time.time()
    endSize = folderSizeAmount(KAGGLE_DATASETS_LOCATION)
    sizeDifference = endSize - startSize #These units are in bytes.
    logger.info('#'*24 + f"(Program End (Date: {currentDate}))" + '#'*24)
    logger.info(f"Elapsed time: {elapsedTimeCalculator(startTime,endTime)}")
    logger.info(f"Added data: {byteUnitConverter(sizeDifference)}")
    #############################(Postprocessing - End)#############################


if __name__ == '__main__':
    os.system('cls')
    main()
