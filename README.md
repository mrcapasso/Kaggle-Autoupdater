## Kaggle Autoupdater


### Abstract:

An archiving program to download new Kaggle dataset versions
once they are released -- done via Kaggle API and Kaggle python module. <br>Logging to file is included, and so are optional download status updates via console. Demo documents are provided for understanding.
<br><br>

_Note: Only tested for windows at this time._
<br><br>
### Requirements:

1. **Python3 v3.9.1** (or greater) 

2. **Kaggle Module v1.5.12** (or greater) 

    GitHub Documentation: https://github.com/Kaggle/kaggle-api

    Kaggle Documentation: https://www.kaggle.com/docs/api

    Action | Cmd 
    -------:|:--------
    Install:| ```pip install Kaggle```
    Check Version:| ```kaggle --version```
    Upgrade Version: | ```pip install kaggle --upgrade```

3. **Valid Kaggle API Token** (quick installation)

    Setup: https://www.kaggle.com/docs/api#authentication


4. **Requests v2.25.1** (or greater)

    Note: This is temporary, it will not be required
    once Kaggle fixes metadata retrieval issues. 

    Requests PyPi Docs: https://pypi.org/project/requests/

    Action | Cmd 
    -------:|:--------
    Install|```pip install requests```
    Check Version|```pip show requests```
    Upgrade Version|```pip install requests --upgrade```

<br>

### Run Guide:
1) Edit the configurations inside of [Source > \__main__.py], at the top of main(), 
to your desired settings. <br>This will also be the area where you plug in the Kaggle 
dataset URLs you want to track and auto-download.
2) Run \__main__.py from the CMD terminal, Python's IDLE, your IDE, or via daily CRON job.
3) Find your downloaded dataset in the Archive folder according to the latest version's date.
4) Check the Logs folder if you suspect any issues, or want to track time spent and data added amounts.