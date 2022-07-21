# classroom-notifier
Classroom Notifier aims to send automated notification emails when any post in a Google Classroom is edited or deleted. This is because Google only sends email notifications for “added” posts.

***DISCLAIMER: The Google account language <ins>MUST</ins> be set to Korean, otherwise it will not work.**

## How to use
#### 1. Download the required files.
Download `Classroom Notifier.py`, `mail_deleted.html`, and `mail_edited.html` and put them to a specified directory.

#### 2. Add an `.env` file to the directory where you put the other files and add the following code to the file.
* `google_id =` your google account (with @gmail.com)
* `google_pw =` your google account password
* `naver_id =` your naver account (with @naver.com)
* `naver_pw =` your naver account password
* `link =` link of your Google Classroom

#### 3. Check your Google Chrome version and download chromedriver.
To check your Chrome version on your desktop, open Chrome and click the ⋮ button in the top right. Go to Help > About Google Chrome.

Visit https://chromedriver.chromium.org/downloads and download the chromedriver that matches your Chrome version and operating system. Add your downloaded chromedriver to the directory where you put the other files.

#### 4. Edit the code.
In line **33**, **349**, and **395**, replace `/Users/leesj/Documents/VS Code/classroom-notifier/` to your directory.

#### Note
You can edit line 33 to be `driver = uc.Chrome()` instead of downloading chromedriver. However, this would lead to downloading Chromedriver every time you execute the Python code, so this method is *not recommended for development purposes*.