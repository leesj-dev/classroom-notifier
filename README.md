# classroom-notifier
Classroom Notifier aims to send automated notification emails when any post in a Google Classroom is edited or deleted.
This is because Google only sends email notifications for *added* posts.

***DISCLAIMER: The Google account language <ins>MUST</ins> be set to Korean, otherwise it will not work.**

## How to Use
#### 1. Install the following packages.
```
pip install python-dotenv
pip install selenium
pip install email
pip install pytz
pip install datetime
pip install undetected_chromedriver
pip install pyclip
pip install smtplib
pip install pyyaml
```

#### 1. Enable SMTP on your NAVER account.
Login to [NAVER Mail](https://mail.naver.com) and go to `환경설정 > POP3/SMTP 설정`. 
Set `POP3/SMTP 사용` to ‘**사용함**’ and click ‘**확인**’.

#### 2. Download the files and install the required packages.
Download the entire repo as a .zip file and unzip it.
Open terminal and type `pip install -r requirements.txt` to install the required packages.
Open folder `src` and move every file to a specific directory.

#### 3. Add a `.env` file to the directory where you put the other files and add the following code to the file.
* `google_id =` your Google account **(with @gmail.com)**
* `google_pw =` your Google account password
* `naver_id =` your NAVER account **(with @naver.com)**
* `naver_pw =` your NAVER account password
* `file_path =` the directory of your file where your `.env` file is **[DO NOT end the directory with `/`]**

#### 4. Check your Google Chrome version and download chromedriver.
To check your Chrome version on your desktop, open Chrome and click the `⋮` button in the top right.
Go to Help > About Google Chrome.

[Download chromedriver](https://chromedriver.chromium.org/downloads) that matches your Chrome version and operating system.
Add your downloaded chromedriver to the directory where you put the other files.

#### 5. Put your Google Classroom links in `links.yaml`.
Replace "Google Classroom Link No. X" to the actual Google Classroom link. Remember that the **key**s *must* be `"1"`, `"2"`, `"3"`, and so forth.
You can add optional comments regarding the name of the classroom corresponding to the links.
```
---
'1': Google Classroom Link No. 1  # Classroom Name
'2': Google Classroom Link No. 2  # Classroom Name
'3': Google Classroom Link No. 3  # Classroom Name
```

#### 6. Run `execute.py` to create a shell/batch script.
Every time you change `links.json`, you need to re-run `execute.py` in order to renew `run.sh` / `run.bat`.

#### 7. Run `run.sh` or `run.batch`.
For Mac/Linux, open Terminal/Command Line and type `source "your file path"/run.sh`.
For example, if your files are located in `/Users/user/classroom-notifier`, then you need to type `source /Users/user/classroom-notifier/run.sh`.

For Windows, open Command Prompt and type `"your file path"\run.bat`.

You may need to quit each Chrome window after you stop executing the code.
The chromedriver windows *do not* get closed automatically.

#### Note
You can edit line No. 38 to be `driver = uc.Chrome()` instead of downloading chromedriver manually.
Note that this would lead to downloading chromedriver every time you execute the Python code; therefore this method is *not recommended*.
