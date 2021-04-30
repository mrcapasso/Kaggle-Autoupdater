## Kaggle Autoupdater

### Abstract

An archiving script to download new Kaggle dataset versions
once they are released -- done via Kaggle API and Kaggle module.

### Requirements
1. **Python3 v3.9.1 or greater**

2. **Kaggle Module** 

    GitHub Documentation: https://github.com/Kaggle/kaggle-api

    Kaggle Documentation: https://www.kaggle.com/docs/api

    ```pip install Kaggle```


3. **Valid Kaggle API Token** (very easy installation)

    Setup: https://www.kaggle.com/docs/api#authentication


4. **Requests and Regex Module**

    Note: These are temporary, they will not be required
    once Kaggle fixes metadata retrieval issues. 

    Requests PyPi Docs: https://pypi.org/project/requests/

    ```pip install requests```

    Regex PyPi Docs: https://pypi.org/project/regex/

    ```pip install regex```

### Run Guide
1) Edit the configurations inside of Source\__main__.py (at the top of file) to your desired settings, 
this will also be where you plug in the Kaggle dataset URLs you want to track and auto-download.
2) Run __main__.py from the CMD terminal, Python's IDLE, your IDE, or via daily CRON job.
3) Find your downloaded dataset in the Archive folder according to the latest version date.
4) Check the Logs folder if you suspect any issues.