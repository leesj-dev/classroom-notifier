# classroom-notifier
Classroom Notifier aims to send automated notification emails when any post in a Google Classroom is edited or deleted.
This is because Google only sends email notifications for *added* posts.

***DISCLAIMER: The Google account language <ins>MUST</ins> be set to Korean, otherwise it will not work.**

## How to Use
### 1. Enable SMTP on your NAVER account.
Login to [NAVER Mail](https://mail.naver.com) and go to `환경설정 > POP3/SMTP 설정`. 
Set `POP3/SMTP 사용` to ‘**사용함**’ and click ‘**확인**’.

### 2. Download the files and install the required packages.
Download the entire repo as a .zip file, unzip it, and move the folder to a specific directory.

Open Terminal/Command Prompt, move to your directory by `cd "file path"` and type `pip install -r requirements.txt` to install the required packages. You should have Python 3 with pip installed to run this program.

### 3. Add a `.env` file to the directory where you put the other files.
On the `.env` file, add **every** email address and password you are going to use for logging in to your Google Classroom **and** for sending emails.

Please include the domain, such as `@gmail.com`, and remember to include both Google and NAVER emails.
You also have to add the line `file_path` and put the directory where the file is located.
* `"your email address 1" = "your password"`
* `"your email address 2" = "your password"`
* `"your email address 3" = "your password"`
* `file_path =` the directory of your file where your `.env` file is

For example, the result of the `.env` file would be:
```
123@gmail.com = qwerty
456@gmail.com = asdfg
789@naver.com = qwretyuiop
file_path = /Documents/VS Code/classroom-notifier
```

### 4. Check your Google Chrome version and download chromedriver.
To check your Chrome version on your desktop, open Chrome and click the `⋮` button in the top right.
Go to Help > About Google Chrome.

[Download chromedriver](https://chromedriver.chromium.org/downloads) that matches your Chrome version and operating system.
Add your downloaded chromedriver to the directory where you put the other files.

*Note: You can delete line No. 81 and edit line No. 88 & 91 to be `driver = uc.Chrome(options=options)` and `driver = uc.Chrome`, respectively, instead of downloading chromedriver manually.
Note that this would lead to downloading chromedriver every time you execute the Python code, and your Chrome browser should be updated to the latest version; therefore this method is **not recommended**.*

### 5. Add your configurations to `config.yaml`.
* `'headless'` is the option to whether enable headless mode or not; type `True` to enable, or `False` to disable.
* `'interval_time'` is the option to set an interval between refreshing Classrooms. If you type `10`, it means that the code will wait for 10 seconds before proceeding to the next loop.
* `'disable_before_months'` is the option to disable crawling Classroom posts that have been posted before a certain time period. If you type `12`, it does not crawl posts that are over 12 months old.
* `'disable_on_postnum'` is the option to crawl Classroom posts until the number of total posts has reached a  certain number. If you type `100`, it crawls posts until the 100th recent post. 

*Note: While you must type `True` or `False` on `'headless'`, options on the other three—`'interval_time'`, `'disable_before_months'`, and `'disable_on_postnum'`—are not mandatory, so you can just leave them as blanks.*

* `'1'`, `'2'`, `'3'`, ... are the main options regarding the login and email information. Remember that the **key**s *must* be `'1'`, `'2'`, `'3'`, and so forth.
  * In `link`, paste the Google Classroom links. You can add optional comments regarding the name of the classroom corresponding to the links if you'd like.
  * In `login`, type the Google account that you are going to crawl with.
  * In `sendfrom`, type your NAVER account to send the notification emails from.
  * In `sendto`, type your recipients of your notification emails as a list. 

```
---
'headless': False
'interval_time': 10
'disable_before_months': 12
'disable_on_postnum': 100
'1':
  link: https://classroom.google.com/c/123456789  # Mathematics
  login: 12345@gmail.com
  sendfrom: 23456@naver.com
  sendto:
    - abcd@gmail.com
'2': 
  link: https://classroom.google.com/c/abcdefgh  # Physics
  login: 12345@gmail.com
  sendfrom: 23456@naver.com
  sendto:
    - abcd@gmail.com
    - efgh@gmail.com
    - ijkl@gmail.com
```

### 6. Run `generator.py` to create a shell/batch script.
Open Terminal/Command Prompt, move to your file directory by `cd "file path"` and type `python3 src/generator.py`.
Every time you change `config.yaml`, you need to re-run `generator.py` in order to renew `run.sh` or `run.bat`.

### 7. Run `run.sh` or `run.bat`.
For Mac/Linux users, open Terminal, move to your directory and type `source src/run.sh`.

For Windows users, open Command Prompt, move to the directory, and type `src/run.bat`.

You may need to quit each Chrome window after you stop executing the code.
The chromedriver windows *do not* get closed automatically.
