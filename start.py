import os, sys, time
from Source\precheck.py import *

pythonMajorVersion = a = 3
pythonMinorVersion = b = 9
pythonMicroVersion = c = 1
pythonVersion = f"{a}.{b}.{c}"

os.system('cls')
try:
    if approxProgramRuns() > 2: 
        main()
    else:
        #Display Information
        print(licenseDisplay())
        print('*Note: These messages will dissappear'
        + ' after a few program runs.*' + "\n")
        os.system('pause')
        os.system('cls')
        print(requirementsDisplay())
        os.system('pause')
        os.system('cls')

        #Precheck Process
        if pythonVersionValidate(pythonMajorVersion,
        pythonMinorVersion,pythonMicroVersion) == False:
            raise AssertionError('Invalid Python3 version.'
            + f" Requires v{pythonVersion} or greater.")
        try:
            if kaggleModuleAndTokenExistence == True:
                main()
        except:
            print('oof')
            
except: 
    print(f"Problem: {sys.exc_info()[1]}")
    os.system('pause')
    sys.exit()