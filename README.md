# NLP-Browser-Extension

Initially, the user should enter the project’s folder from command line or PowerShell using the ‘cd‘ command. Then, ‘pip install -r requirements.txt’ command must be executed for the Python libraries to be installed. Additionally, tesseract must be downloaded from the following link: https://github.com/UB-Mannheim/tesseract/wiki. If an error is encountered this link might be helpful: https://stackoverflow.com/questions/50655738/how-do-i-resolve-a-tesseractnotfounderror. In order to run the back-end service, the following commands have to be executed:
```

·        cd /back-end
·        set FLASK_APP=server.py
·        set FLASK_ENV=development
·        flask run
```

The user should open the Chrome or Edge browser. Then, from the extensions tab, ‘Manage extensions’ button must be clicked. From the navigation bar, the developer mode should be turned on. ‘Load unpacked’ must be selected and ‘chrome-extension(front-end)’ folder must be uploaded. 
