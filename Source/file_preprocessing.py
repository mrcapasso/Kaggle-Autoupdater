########################(Dataset Parallelism Preparation)#######################
    #CSV Docs:
        #Module Contents: https://docs.python.org/3/library/csv.html#module-contents
        #Reader Objects: https://docs.python.org/3/library/csv.html#reader-objects
        #Writer Objects: https://docs.python.org/3/library/csv.html#writer-objects
        #Line by Line demo: https://docs.python.org/3/library/csv.html#id3
        #Cons: No append feature, no native parallelism, line by line only.
        #Pros: csv to dictionaries, popular
    #concurrent.futures
        #Docs: https://docs.python.org/3/library/concurrent.futures.html
        #Cons: Execution errors...?
        #Pros: Easy to use (subjective)
    #threading
        #Docs: https://docs.python.org/3/library/threading.html
    #multiprocessing: 
        #! Note: some functions exclusive to Unix OS
        #Docs: https://docs.python.org/3/library/multiprocessing.html

import os, multiprocessing, threading
#Goal: Redistribute files into smaller chunks optimized for system specs. 

#numOfFiles = f(vCPU)
#sizeOfFiles = f(DRAM, xVHD/HDD, time); note,

def preprocessPrecheck(outputFolderPath:str, workingDirName:str='working', incompleteSuffix:str='_incomplete', completeSuffix:str='_complete') -> str: #Return status code of preprocessing: 'incomplete', 'completed', 'outstanding'.
    '''
        Note: progress status of pre-processing is tracked via foldernames on working directory.
    '''
    for _,folderNameList,_ in os.walk(outputFolderPath):
        for i in folderNameList:
            if i == workingDirName + incompleteSuffix:
                return 'incomplete'
            elif i == workingDirName + completeSuffix:
                return 'completed'
            else:
                continue
    return 'outstanding'

def preprocessCreate(): #Creates/appends working environment
    pass

def preprocessCharacterHistogram() -> dict: #create histogram of file density
    pass

def preprocessFileDistributer(): #distribute files to output folder
    pass

def preprocessStatusUpdater(): #updates status text on folders
    pass

if __name__ == '__main__':

    #These are configurations, be sure to include in __main__.py once finished. 
    INPUT_FOLDER_LOCATION = 'path here to folder with files'
    OUTPUT_FOLDER_LOCATION = r'C:\Users\Matteo\Documents\YT-Archiver'
    OUTPUT_FOLDER_NAME = 'YT-Archiver'
    WORKING_DIRECTORY_SUBFOLDER = 'working'
    INCOMPLETE_STATUS_SUFFIX = '_incomplete'
    COMPLETED_STATUS_SUFFIX = '_completed'
    DISTRIBUTION_FILE_NAME = 'distribution.json'

    os.system('cls')
    print(preprocessPrecheck(OUTPUT_FOLDER_NAME))