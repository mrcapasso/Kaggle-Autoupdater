#     License Type: GNU General Public License v3.0
#     'Kaggle Autoupdater', automated file version control for Kaggle.
#     Copyright (C) 2021 Matteo Capasso (matteo@capasso.dev)

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with this program in the parent folder.
#     If not, see <https://www.gnu.org/licenses/>.

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
        #URL Format (REQUIRED): https://www.kaggle.com/<author>/<datasetname>
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
    absPathForLogDir = os.path.abspath('Logs')
    dateSpecificLogFile = os.path.join(absPathForLogDir,f"{currentDate}.log") #1 New / temp
    #Bug fix for inability to find log file? 
    if os.path.isfile(dateSpecificLogFile) == False: #! New / temp
        logFileToCreate = os.path.join(absPathForLogDir, dateSpecificLogFile) #! New / temp
        open(logFileToCreate, "x")
    #fh = logging.FileHandler(os.path.join('Logs',f"{currentDate}.log")) #previous 'working'
    fh = logging.FileHandler(dateSpecificLogFile) #! New / temp
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

    #Parsing config's URL list to list of dataset names and authors.
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
            #Note: Date naming convention is YYYY-MM-DD.
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
            if os.listdir(KAGGLE_DATASETS_LOCATION) == []: #Existent, but empty, folder.
                logger.info(f"New dataset: {datasetName}/{datasetAuthor}")
            elif len(os.listdir(individualDatasetPath)) != 0: #Comparing sub-folder dates.
                #Note: Directory subfolder naming convention is YYYY-MM-DD.
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
    print('''

        Kaggle Autoupdater Copyright (C) 2021 Matteo Capasso
        This program comes with ABSOLUTELY NO WARRANT.
        This is free software, and you are welcome to redistribute it
        under certain conditions. See source files for details.
        
        ''')
    sleepTime = 5
    for i in range(sleepTime):
        print(f"Sleeping {sleepTime-i} seconds...")
        time.sleep(1)
    os.system('cls')
    main()
