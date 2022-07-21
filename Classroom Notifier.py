from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from email.mime.text import MIMEText
from pytz import timezone
from datetime import datetime
import undetected_chromedriver as uc
import pyperclip
import smtplib
import time
import os

# ID/PW (.env 파일에 따로 보관)
load_dotenv()
google_id = os.getenv("google_id")
google_pw = os.getenv("google_pw")
naver_id = os.getenv("naver_id")
naver_pw = os.getenv("naver_pw")
linkstr = os.getenv("link")
file_path = os.getenv("file_path")


# 그래픽 자료형
imgdict = {
    "공지사항": "https://ci4.googleusercontent.com/proxy/lXfhTxxtlRo9jBByRra4CvV04HGPA1vh1Uy69rFI7Tx21qIUYebG3u-5hHb7GcAKaLP2LRTLQ3uAL_GJiwH5aO3KEXRIHCXxJfnH0V4RRRWEJmYoCnwnaoC3HuKMfKk7WOJ5Bjt3Eoi-WSfh6q4M7LGaZDG1BntyDfOOSopwlDhEf74sTAHhQhEdsK1bJHk=s0-d-e1-ft#https://fonts.gstatic.com/s/i/googlematerialicons/chat_bubble_outline/v7/white-48dp/2x/gm_chat_bubble_outline_white_48dp.png",
    "자료": "https://ci6.googleusercontent.com/proxy/KwZhwEdkmty0qJcCZZEZ1AgLPNQoi0gB3r7FLNj1-_YhlgY7AHrEcTybc31P1i0i2IFaXgN9Y_KiAoxtJUJcrqyyZn2hTYPOTSjhHqVT8k6KcZAHLZfmmF7mBFg5fpfzy3EotPxANHQGLtYCFlGtRZY=s0-d-e1-ft#https://fonts.gstatic.com/s/i/googlematerialicons/book/v8/white-48dp/2x/gm_book_white_48dp.png",
    "질문": "https://ci5.googleusercontent.com/proxy/uwmGFdeqaPUtThLULRQZIBqFlWtXXssiY-rIToedc4g9VKdjLmtRa0sj4Q-XUZNoUmwogKF9UcXA8xkFlEge5yHAoKj4DVnop7J4wEFnCX8lHoY7Jlh_tB_BaUjRQYhocipZ1ClyZRChfqa9f0Wq1ffbAyVxEHlpQnZz=s0-d-e1-ft#https://fonts.gstatic.com/s/i/googlematerialicons/live_help/v6/white-48dp/2x/gm_live_help_white_48dp.png",
    "과제": "https://ci3.googleusercontent.com/proxy/8nr0SU4M3K6mq9EASltstSjUrUfTv13LXLM_xIJr6oD-GyeiECMFXG3ze_-oG9P-EOU9MGJRgMQ_HknJ8by3ZuiZlF4EevHowhFySEamH6uWEg1ct-LbbVxkojI3fo0lTDWSscyay8IHOuSnKbtN-UxnHx1_D9n3QY8IyFo=s0-d-e1-ft#https://fonts.gstatic.com/s/i/googlematerialicons/assignment/v6/white-48dp/2x/gm_assignment_white_48dp.png",
}


# 구글 로그인 차단 우회
def init_driver():
    chromedriver_path = file_path + "/chromedriver"
    driver = uc.Chrome(driver_executable_path = chromedriver_path)
    driver.get(link)
    return driver


# 클래스룸 접속
def login(driver):
    driver.find_element(By.XPATH, '//*[@id="identifierId"]').send_keys(google_id)
    driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button').click()
    driver.implicitly_wait(5)
    driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(google_pw)
    driver.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button').click()
    driver.implicitly_wait(10)
    time.sleep(3)


# 끝까지 스크롤링 및 전체 게시글 수 체크
def Scroll():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height

    driver.execute_script("window.scrollTo(0, 0);")


# 경로 찾기 - 마지막으로 div가 있는 지점을 검색
def lastpathFinder(str1, str2, tofind, postmax):
    k = 2
    while True:
        try:
            if tofind == "text":
                result = driver.find_element(By.XPATH, str1 + str(k) + str2).text
            elif tofind == "HTML":
                result = driver.find_element(By.XPATH, str1 + str(k) + str2).get_attribute('innerHTML')
            driver.implicitly_wait(0.5)

        except:
            if 'result' in locals():
                break
            else:
                if k > postmax + 1:
                    break
                
        k = k + 1
        
    return result


# 게시물 종류 추출 (단, 공지사항은 제외)
def typeExtractor(postnum_str):
    title = driver.find_element(By.XPATH, "html/body/div[2]/div[1]/div[5]/div[2]/main/section/div/div[" + postnum_str + "]/div[1]/div/div[3]/div/div/span").text
    type = title[title.find("게시") - 3 : title.find("게시") - 1]
    return type


# 게시자 추출
def uploaderExtractor(postnum_str, type, postmax):
    if type == "공지사항":
        uploader = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[5]/div[2]/main/section/div/div[' + postnum_str + ']/div[1]/div[1]/div[1]/div/div/span').text
    
    elif type == "자료":
        uploader = lastpathFinder("/html/body/div[2]/div[", "]/div[4]/div[2]/div[1]/div[1]/div[2]/div[1]", "text", postmax)
        
    else:
        uploader = lastpathFinder("/html/body/div[2]/div[", "]/div[4]/div[2]/div[2]/div[1]/div[1]/div[2]/div[1]", "text", postmax)

    return uploader

# 최초 날짜 추출 (이를 활용하는 부분은 아직 개발이 안 됨)
def initialdateExtractor(postnum_str, type, postmax):
    end = "("

    if type == "공지사항":
        mod = driver.find_element(By.XPATH, "html/body/div[2]/div/div[5]/div[2]/main/section/div/div[" + postnum_str + "]/div[1]/div[1]/div[1]/span/span[2]").text
    
    elif type == "자료":
        mod = lastpathFinder("/html/body/div[2]/div[", "]/div[4]/div[2]/div[1]/div[1]/div[2]/div[3]", "text", postmax)

    else:
        mod = lastpathFinder("/html/body/div[2]/div[", "]/div[4]/div[2]/div[2]/div[1]/div[1]/div[2]/div[3]", "text", postmax)
    
    if end in mod:
        date = mod[0 : mod.find(end) -1]
    else:
        date = mod
    
    return date

# 게시/수정 날짜 추출
def finaldateExtractor(postnum_str, type, postmax):
    start = "("
    end = "에"

    if type == "공지사항":
        mod = driver.find_element(By.XPATH, "html/body/div[2]/div/div[5]/div[2]/main/section/div/div[" + postnum_str + "]/div[1]/div[1]/div[1]/span/span[2]").text
    
    elif type == "자료":
        mod = lastpathFinder("/html/body/div[2]/div[", "]/div[4]/div[2]/div[1]/div[1]/div[2]/div[3]", "text", postmax)

    else:
        mod = lastpathFinder("/html/body/div[2]/div[", "]/div[4]/div[2]/div[2]/div[1]/div[1]/div[2]/div[3]", "text", postmax)
    
    if end in mod:
        date = mod[mod.find(start) + 1 : mod.find(end)]
    else:
        date = mod

    return date


# 본문 추출
def bodyExtractor(postnum_str, type, encoding, postmax):
    if type == "공지사항":
        if encoding == "text":
            body = driver.find_element(By.XPATH, "html/body/div[2]/div/div[5]/div[2]/main/section/div/div[" + postnum_str + "]/div[1]/div[2]/div[1]/html-blob/span").text
        elif encoding == "HTML":
            body = driver.find_element(By.XPATH, "html/body/div[2]/div/div[5]/div[2]/main/section/div/div[" + postnum_str + "]/div[1]/div[2]/div[1]/html-blob/span").get_attribute('innerHTML')

    elif type == "자료":
        body1 = lastpathFinder("/html/body/div[2]/div[", "]/div[4]/div[2]/div[1]/div[1]/div[1]/h1/html-blob/span", encoding, postmax)
        try:
            body2 = lastpathFinder("/html/body/div[2]/div[", "]/div[4]/div[2]/div[1]/div[2]/html-blob/span", encoding, postmax)
        except:
            body2 = ""

        if body2 == "":
            body = body1
        else:
            body = body1 + "\n" + body2

    else:
        body1 = lastpathFinder("/html/body/div[2]/div[", "]/div[4]/div[2]/div[2]/div[1]/div[1]/div[1]/h1/html-blob/span", encoding, postmax)
        try:
            body2 = lastpathFinder("/html/body/div[2]/div[", "]/div[4]/div[2]/div[2]/div[1]/div[2]/html-blob/span", encoding, postmax)
        except:
            body2 = ""

        if body2 == "":
            body = body1
        else:
            body = body1 + "\n" + body2
    
    return body


# 첨부파일 경로 검색
def xpathFinder(postnum_str, type, divnum, j, postmax):
    if type == "공지사항":
        if divnum == "1":
            xpath = "html/body/div[2]/div/div[5]/div[2]/main/section/div/div[" + postnum_str + "]/div[1]/div[2]/div[2]/div[1]/div[1]/div[" + j + "]/a"
        if divnum == "2":
            xpath = "html/body/div[2]/div/div[5]/div[2]/main/section/div/div[" + postnum_str + "]/div[1]/div[2]/div[2]/div[1]/div[2]/div[" + j + "]/a"

    elif type == "자료":
        temp = "]/div[4]/div[2]/div[2]/div[1]/div/div[" + j + "]/div/a"
        xpath = lastpathFinder("/html/body/div[2]/div[", temp, "text", postmax)
        
    else:
        temp = "]/div[4]/div[2]/div[2]/div[2]/div[1]/div/div[" + j + "]/div/a"
        xpath = lastpathFinder("/html/body/div[2]/div[", temp, "text", postmax)
    
    return xpath


# 첨부파일 추출
def attachExtractor(postnum_str, type, postmax):
    attach = ()
    flg = False

    for divnum in ["1", "2"]:
        try:  # 첨부파일이 1개인 경우
            xpath = xpathFinder(postnum_str, type, divnum, "", postmax)
            id = driver.find_element(By.XPATH, xpath).get_attribute("href")
            driver.implicitly_wait(0.5)
            attach = attach + (id,)
            flg = True
        except:
            pass

    if flg == False:  # 첨부파일이 없거나 2개 이상인 경우
        if type == "공지사항":
            for divnum in ["1", "2"]:
                i = 1
                while True:
                    j = str(i)
                    try:  # 첨부파일이 2개 이상인 경우
                        xpath = xpathFinder(postnum_str, type, divnum, j, postmax)
                        id = driver.find_element(By.XPATH, xpath).get_attribute("href")
                        driver.implicitly_wait(0.5)
                        attach = attach + (id,)
                        i = i + 1
                    except:  # 첨부파일이 0개인 경우
                        break
        else:
            divnum = "1"
            i = 1
            while True:
                j = str(i)
                try:  # 첨부파일이 2개 이상인 경우
                    xpath = xpathFinder(postnum_str, type, divnum, j, postmax)
                    id = driver.find_element(By.XPATH, xpath).get_attribute("href")
                    driver.implicitly_wait(0.5)
                    attach = attach + (id,)
                    i = i + 1
                except:  # 첨부파일이 0개인 경우
                    break
                
    return attach


# 프로세스 실행
def Process():
    time.sleep(3)
    Scroll()

    # 총 게시글 수 세기
    postnum_int = 2
    while True:
        postnum_str = str(postnum_int)
        try:
            driver.find_element(By.XPATH, "/html/body/div[2]/div/div[5]/div[2]/main/section/div/div[" + postnum_str + "]")
            driver.implicitly_wait(0.5)

        except:
            postmax = postnum_int - 2
            break

        postnum_int = postnum_int + 1

    # 빈 딕셔너리 생성
    pdict = {}
    postnum_int = 2
    while True:
        postnum_str = str(postnum_int)
        errorchk = driver.find_element(By.XPATH, "html/body/div[2]/div/div[5]/div[2]/main/section/div/div[" + postnum_str + "]").get_attribute("jsaction")
        driver.implicitly_wait(0.5)

        if errorchk == None:
            post_type = "공지사항"
            post_uploader = uploaderExtractor(postnum_str, post_type, postmax)
            post_date = finaldateExtractor(postnum_str, post_type, postmax)
            post_body_HTML = bodyExtractor(postnum_str, post_type, "HTML", postmax)
            post_body_text = bodyExtractor(postnum_str, post_type, "text", postmax)
            post_attach = attachExtractor(postnum_str, post_type, postmax)
            plist = (post_type, post_uploader, post_date, post_body_HTML, post_body_text, post_attach)
            pdict.update({postnum_int: plist})

        else:
            post_type = typeExtractor(postnum_str)
            driver.find_element(By.XPATH, "html/body/div[2]/div/div[5]/div[2]/main/section/div/div[" + postnum_str + "]").click()
            time.sleep(3)
            post_uploader = uploaderExtractor(postnum_str, post_type, postmax)
            post_date = finaldateExtractor(postnum_str, post_type, postmax)
            post_body_HTML = bodyExtractor(postnum_str, post_type, "HTML", postmax)
            post_body_text = bodyExtractor(postnum_str, post_type, "text", postmax)
            post_attach = attachExtractor(postnum_str, post_type, postmax)
            plist = (post_type, post_uploader, post_date, post_body_HTML, post_body_text, post_attach)
            pdict.update({postnum_int: plist})

            driver.execute_script("window.history.go(-1)")
            driver.implicitly_wait(2)

        if postnum_int < postmax:
            postnum_int = postnum_int + 1

        else:
            break

    return pdict

# 메일 전송
def SendMsg(message, title):
    msg = MIMEText(message, "html")
    msg["Subject"] = title
    msg["From"] = naver_id
    msg["To"] = google_id

    with smtplib.SMTP_SSL("smtp.naver.com", 465) as smtp:
        smtp.login(naver_id, naver_pw)
        smtp.sendmail(naver_id, google_id, msg.as_string())


# 메일 전송 제어
def MsgEdited():
    post_room = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/div[2]/div/div[5]/div[1]/div/div[2]/h1').text
    set_before = set(pdict_before.items())
    set_after = set(pdict_after.items())
    diff = dict(set_after - set_before)
    for key, val in diff.items():
        key_str = str(key)
        post_type = val[0]
        post_uploader = val[1]
        post_date = val[2]
        post_body_HTML = val[3]
        post_body_text = val[4]
    
        # 주소 복사
        if post_type == "공지사항":
            driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[5]/div[2]/main/section/div/div[" + key_str + "]/div[1]/div[1]/div[4]/div/div/div").click()
            driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[5]/div[2]/main/section/div/div[" + key_str + "]/div[1]/div[1]/div[4]/div/div/div").send_keys(Keys.RETURN)
        else:
            driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[5]/div[2]/main/section/div/div[" + key_str + "]/div[1]/div/div[6]/div/div/div").click()
            driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[5]/div[2]/main/section/div/div[" + key_str + "]/div[1]/div/div[6]/div/div/div").send_keys(Keys.RETURN)
        
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/div[9]/div/div/span[1]').click()
        driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/div[9]/div/div/span[1]').send_keys(Keys.RETURN)
        post_postlink = pyperclip.paste()
        mailedit_path = file_path + "/mail_edited.html"
        message = open(mailedit_path, "r", encoding="utf-8").read()

        if post_type == "공지사항":
            message = message.replace("[[body]]", post_body_HTML)
            post_smalltext = '<tr height="0"></tr>'
        else:
            post_title = post_body_HTML.split('\n', 1)[0]   # \n을 기준으로 최대 1번 쪼갠 뒤 그 중 첫번째(0번째) 부분
            message = message.replace("[[body]]", post_title)
            post_smalltext = '<tr height="4px"></tr><tr><td style="color:#5f6368;font-size:14px;font-weight:400;line-height:20px;letter-spacing:0.2px">' + post_body_HTML.split('\n', 1)[1] + '</td></tr>'

        message = message.replace("[[google_id]", google_id)
        message = message.replace("[[roomlink]]", link)
        message = message.replace("[[room]]", post_room)
        message = message.replace("[[uploader]]", post_uploader)
        message = message.replace("[[type]]", post_type)
        message = message.replace("[[date]]", post_date)
        message = message.replace("[[postlink]]", post_postlink)
        message = message.replace("[[imgsrc]]", imgdict[post_type])
        message = message.replace("[[smalltext]]", post_smalltext)

        if post_type == "공지사항" or post_type == "질문":
            message = message.replace("[[postposition]]", "을")
        else:
            message = message.replace("[[postposition]]", "를")

        # 메일 제목
        if len(post_body_text) < 20:
            title = "수정된 " + post_type + ": '" + post_body_text + "'"
        else:
            title = "수정된 " + post_type + ": '" + post_body_text[0:20] + "...'"

        SendMsg(message, title)

def MsgRemoved():
    post_room = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/div[2]/div/div[5]/div[1]/div/div[2]/h1').text
    set_before = set(pdict_before.values())
    set_after = set(pdict_after.values())
    diff = list(set_before - set_after)
    for val in diff:
        post_type = val[0]
        post_uploader = val[1]
        post_date = val[2]
        post_body_HTML = val[3]
        post_body_text = val[4]
        del_date = datetime.now(timezone('Asia/Seoul')).strftime('%-m월 %-d일')
        maildel_path = file_path + "/mail_deleted.html"
        message = open(maildel_path, "r", encoding="utf-8").read()

        if post_type == "공지사항":
            message = message.replace("[[body]]", post_body_HTML)
            post_smalltext = '<tr height="0"></tr>'
        else:
            post_title = post_body_HTML.split('\n', 1)[0]   # \n을 기준으로 최대 1번 쪼갠 뒤 그 중 첫번째(0번째) 부분
            message = message.replace("[[body]]", post_title)
            post_smalltext = '<tr height="4px"></tr><tr><td style="color:#5f6368;font-size:14px;font-weight:400;line-height:20px;letter-spacing:0.2px">' + post_body_HTML.split('\n', 1)[1] + '</td></tr>'

        message = message.replace("[[google_id]", google_id)
        message = message.replace("[[roomlink]]", link)
        message = message.replace("[[room]]", post_room)
        message = message.replace("[[uploader]]", post_uploader)
        message = message.replace("[[type]]", post_type)
        message = message.replace("[[date]]", del_date)
        message = message.replace("[[imgsrc]]", imgdict[post_type])
        message = message.replace("[[smalltext]]", post_smalltext)

        if post_type == "공지사항" or post_type == "질문":
            message = message.replace("[[postposition]]", "을")
        else:
            message = message.replace("[[postposition]]", "를")

        # 메일 제목
        if len(post_body_text) < 20:
            title = "삭제된 " + post_type + ": '" + post_body_text + "'"
        else:
            title = "삭제된 " + post_type + ": '" + post_body_text[0:20] + "...'"

        SendMsg(message, title)

# main 함수
if __name__ == "__main__":
    linklst = linkstr.split(", ")
    print("Links: ", linklst)
    number = input("Select your desired link (nth item in list): ")
    link = linklst[int(number) - 1]
    driver = init_driver()
    login(driver)

    # 최초 딕셔너리
    pdict_before = Process()

    # 전후 비교
    while True:
        time.sleep(10)
        driver.refresh()
        while True:
            try:
                pdict_after = Process()
                break
            except:
                pass

        if pdict_before != pdict_after:
            if len(pdict_before) > len(pdict_after):
                print("삭제(또는 삭제 및 수정)된 게시물 감지.")
                MsgRemoved()
                print("메일 발신 완료.")

            elif len(pdict_before) == len(pdict_after):
                print("변경된 게시물 감지.")
                MsgEdited()
                print("메일 발신 완료.")

            else:
                print("새로운 게시물 감지. 클래스룸에서 발신된 메일을 확인하세요.")

        else:
            print("변경사항 없음.")

        pdict_before = pdict_after