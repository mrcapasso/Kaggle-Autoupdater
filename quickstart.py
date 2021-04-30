#!/user/bin/python3.9.1

#     License Type: GNU General Public License v3.0
#     'Kaggle Autoupdater', automated file version control for Kaggle.
#     Copyright (C) 2021 Matteo Capasso (matteo@capasso.dev)

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os, sys, time
sys.path.append("Source")
from Source.precheck import *

#Minimum Python3 version: 3.9.1
pythonMajorVersion = a = 3
pythonMinorVersion = b = 9
pythonMicroVersion = c = 1
pythonVersion = f"{a}.{b}.{c}"

try: #This process serves as a pre-check to ensure user has proper setup.
    os.system('cls')
    if approxProgramRuns() > 2: 
        from Source.__main__ import main
        main()
    else:
        #Display Information
        print(licenseDisplay())
        print('*Note: These messages will dissappear'
        + ' after a few program runs.*' + "\n")
        os.system('pause')
        os.system('cls')
        print(requirementsDisplay(pythonVersion))
        os.system('pause')
        os.system('cls')

        #Precheck Process
        if pythonVersionValidate(a,b,c) == False:
            raise AssertionError('Invalid Python3 version.'
            + f" Requires v{pythonVersion} or greater.")
        if kaggleModuleAndTokenExistence() == False:
            import kaggle #Intentionally breaking.

        #Passed Precheck Process
        from Source.__main__ import main
        main()

except: 
    print(f"Problem Type: {sys.exc_info()[0]}")
    print(f"Problem Value: {sys.exc_info()[1]}")
    os.system('pause')
    sys.exit()