# classroom-notifier
Classroom Notifier aims to send automated notification emails when any post in a Google Classroom is edited or deleted. This is because Google only sends email notifications for “added” posts.

***DISCLAIMER: The Google account language <ins>MUST</ins> be set to Korean, otherwise it will not work.**

## How to Use
#### 1. Download the required files.
Download `Classroom Notifier.py`, `mail_deleted.html`, and `mail_edited.html` and move them to a specific directory.

#### 2. Add a `.env` file to the directory where you put the other files and add the following code to the file.
* `google_id =` your Google account **(with @gmail.com)**
* `google_pw =` your Google account password
* `naver_id =` your NAVER account **(with @naver.com)**
* `naver_pw =` your NAVER account password
* `link =` link of your Google Classroom
* `file_path =` the directory of your file where your `.env` file is **[DO NOT end the directory with `/`]**

#### 3. Check your Google Chrome version and download chromedriver.
To check your Chrome version on your desktop, open Chrome and click the `⋮` button in the top right. Go to Help > About Google Chrome.

Visit https://chromedriver.chromium.org/downloads and download the chromedriver that matches your Chrome version and operating system. Add your downloaded chromedriver to the directory where you put the other files.

#### 4. Run the code.
You may need to quit the chromedriver windows after you stop executing the code. The chromedriver windows *do not* get closed automatically.

#### Note
You can edit line 33 to be `driver = uc.Chrome()` instead of downloading chromedriver manually. Note that this would lead to downloading chromedriver every time you execute the Python code; therefore this method is *not recommended for development purposes*.