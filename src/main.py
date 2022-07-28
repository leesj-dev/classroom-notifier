from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from email.mime.text import MIMEText
from pytz import timezone
from datetime import datetime
from sys import platform
import undetected_chromedriver as uc
import pyclip
import smtplib
import yaml
import time
import sys
import os

# 운영체제 확인
if platform in ("linux", "darwin"):
    slash = "/"
elif platform == "win32":
    slash = "\\"

# .env 파일에서 파일 경로와 헤드리스 사용 여부를 불러옴
load_dotenv()
headless = os.getenv("headless")
file_path = os.getenv("file_path")
if file_path[-1] in ("/", "\\"):
    file_path = file_path[:-1]

# .yaml 파일에서 정보 불러옴
yaml_file = open(file_path + slash + "src" + slash + "config.yaml")
link_dict = yaml.safe_load(yaml_file)
number = sys.argv[1]
used_dict = link_dict[number]
link = used_dict["link"]
login_id = used_dict["login"]
login_pw = os.getenv(login_id)
sendfrom_id = used_dict["sendfrom"]
sendfrom_pw = os.getenv(sendfrom_id)
sendto = used_dict["sendto"]  # 자료형 list이므로 주의 필요

# 그래픽 자료형
imgdict = {
    "공지": "https://ci4.googleusercontent.com/proxy/lXfhTxxtlRo9jBByRra4CvV04HGPA1vh1Uy69rFI7Tx21qIUYebG3u-5hHb7GcAKaLP2LRTLQ3uAL_GJiwH5aO3KEXRIHCXxJfnH0V4RRRWEJmYoCnwnaoC3HuKMfKk7WOJ5Bjt3Eoi-WSfh6q4M7LGaZDG1BntyDfOOSopwlDhEf74sTAHhQhEdsK1bJHk=s0-d-e1-ft#https://fonts.gstatic.com/s/i/googlematerialicons/chat_bubble_outline/v7/white-48dp/2x/gm_chat_bubble_outline_white_48dp.png",
    "자료": "https://ci6.googleusercontent.com/proxy/KwZhwEdkmty0qJcCZZEZ1AgLPNQoi0gB3r7FLNj1-_YhlgY7AHrEcTybc31P1i0i2IFaXgN9Y_KiAoxtJUJcrqyyZn2hTYPOTSjhHqVT8k6KcZAHLZfmmF7mBFg5fpfzy3EotPxANHQGLtYCFlGtRZY=s0-d-e1-ft#https://fonts.gstatic.com/s/i/googlematerialicons/book/v8/white-48dp/2x/gm_book_white_48dp.png",
    "질문": "https://ci5.googleusercontent.com/proxy/uwmGFdeqaPUtThLULRQZIBqFlWtXXssiY-rIToedc4g9VKdjLmtRa0sj4Q-XUZNoUmwogKF9UcXA8xkFlEge5yHAoKj4DVnop7J4wEFnCX8lHoY7Jlh_tB_BaUjRQYhocipZ1ClyZRChfqa9f0Wq1ffbAyVxEHlpQnZz=s0-d-e1-ft#https://fonts.gstatic.com/s/i/googlematerialicons/live_help/v6/white-48dp/2x/gm_live_help_white_48dp.png",
    "과제": "https://ci3.googleusercontent.com/proxy/8nr0SU4M3K6mq9EASltstSjUrUfTv13LXLM_xIJr6oD-GyeiECMFXG3ze_-oG9P-EOU9MGJRgMQ_HknJ8by3ZuiZlF4EevHowhFySEamH6uWEg1ct-LbbVxkojI3fo0lTDWSscyay8IHOuSnKbtN-UxnHx1_D9n3QY8IyFo=s0-d-e1-ft#https://fonts.gstatic.com/s/i/googlematerialicons/assignment/v6/white-48dp/2x/gm_assignment_white_48dp.png",
}

# 색상 자료형 (클래스룸에서는 key 색상만 구할 수 있으므로 value 색상을 따로 구해야 함)
colordict = {
  # room & 열기 # 선 & 원
    "#174ea6": "#1967d2",  # Dark Blue
    "#137333": "#1e8e3e",  # Green 
    "#b80672": "#e52592",  # Pink 
    "#c26401": "#e8710a",  # Orange 
    "#007b83": "#129eaf",  # Mint 
    "#7627bb": "#9334e6",  # Purple 
    "#1967d2": "#4285f4",  # Light Blue 
    "#202124": "#5f6368",  # Grey 
}

# 구글 로그인 차단 우회 - undetected_chromedriver
def init_driver():
    chromedriver_path = file_path + slash + "chromedriver"

    if headless == "yes":
        options = uc.ChromeOptions()
        options.headless = True
        options.add_argument('--headless')
        driver = uc.Chrome(driver_executable_path=chromedriver_path, options=options)
    
    elif headless == "no":
        driver = uc.Chrome(driver_executable_path=chromedriver_path)

    driver.get(link)

    return driver


# 클래스룸 접속
def login(driver, login_id, login_pw):
    driver.implicitly_wait(10)
    driver.find_element(By.XPATH, '//*[@id="identifierId"]').send_keys(login_id)
    driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button').send_keys(Keys.RETURN)
    driver.implicitly_wait(5)
    driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(login_pw)
    driver.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button').send_keys(Keys.RETURN)
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


# 색상 추출
def colorExtractor():
    color_rgba = driver.find_element(By.XPATH, "(//*[@class='xHPsid'])[last()]/div[1]/a").value_of_css_property("color")
    color_rgba = color_rgba[color_rgba.find("(") + 1 : color_rgba.find(")")]
    color_list = color_rgba.split(', ')
    color_list = color_list[0:3]  # rgba -> rgb
    
    for i in range(0, len(color_list)):
        color_list[i] = int(color_list[i])

    color_tuple = tuple(color_list)
    color_hex = '#%02x%02x%02x' % color_tuple
    
    return color_hex


# xpath 경로 탐색
def elementFinder(number, type, path, tofind):
    if type in ("main", "공지"):
        total = "(//div[contains(@class, 'qhnNic LBlAUc Aopndd TIunU')])[" + number + "]" + path
    elif type == "link_copy":
        total = "(//*[@class='z80M1 FeRvI'])[last()-1]" + path
    else:
        total = "(//*[@class='fJ1Vac'])[last()]" + path

    if tofind == "self":
        result = driver.find_element(By.XPATH, total)
    elif tofind == "text":
        result = driver.find_element(By.XPATH, total).text
    elif tofind == "click":
        result = driver.execute_script("arguments[0].click()", driver.find_element(By.XPATH, total)) # visible한 영역이 아닐 때 클릭하도록 강제실행
    else:
        result = driver.find_element(By.XPATH, total).get_attribute(tofind)

    return result


# 게시물 종류 추출 (단, 공지는 제외)
def typeExtractor(postnum_str):
    title = elementFinder(postnum_str, "main", "/div[1]/div/div[3]/div/div/span", "text")
    type = title[title.find("게시") - 3 : title.find("게시") - 1]
    return type


# 게시자 추출
def uploaderExtractor(postnum_str, type):
    if type == "공지":
        uploader = elementFinder(postnum_str, type, "/div[1]/div[1]/div[1]/div/div/span", "text")
    else:
        uploader = elementFinder(postnum_str, type, "/div[2]/div[1]/div[1]/div[2]/div[1]", "text")

    return uploader


# 최초 날짜 추출 (이것을 활용하는 부분은 개발 예정)
def initialDateExtractor(postnum_str, type):
    end = "("

    if type == "공지":
        mod = elementFinder(postnum_str, type, "/div[1]/div[1]/div[1]/span/span[2]", "text")
    else:
        mod = elementFinder(postnum_str, type, "/div[2]/div[1]/div[1]/div[2]/div[3]", "text")

    if end in mod:
        date = mod[0 : mod.find(end) - 1]
    else:
        date = mod

    return date


# 게시/수정 날짜 추출
def finalDateExtractor(postnum_str, type):
    start = "("
    end = "에"

    if type == "공지":
        mod = elementFinder(postnum_str, type, "/div[1]/div[1]/div[1]/span/span[2]", "text")
    else:
        mod = elementFinder(postnum_str, type, "/div[2]/div[1]/div[1]/div[2]/div[3]", "text")

    if end in mod:
        date = mod[mod.find(start) + 1 : mod.find(end)]
    else:
        date = mod

    return date


# 본문 추출
def bodyExtractor(postnum_str, type, encoding):
    if type == "공지":
        body = elementFinder(postnum_str, type, "/div[1]/div[2]/div[1]/html-blob/span", encoding)

    else:
        body1 = elementFinder(postnum_str, type, "/div[2]/div[1]/div[1]/div[1]/h1/html-blob/span", encoding)
        try:
            body2 = elementFinder(postnum_str, type, "/div[2]/div[1]/div[2]/html-blob/span", encoding)
        except:
            body2 = ""
        body = body1 + "\n" + body2

    return body


# 첨부파일 경로 검색
def xpathFinder(type, divnum, j):
    if type == "공지":
        xpath = "/div[1]/div[2]/div[2]/div[1]/div[" + divnum + "]/div[" + j + "]/a"
    else:
        xpath = "/div[2]/div[2]/div[1]/div/div[" + j + "]/div/a"

    return xpath


# 첨부파일 추출
def attachExtractor(postnum_str, type):
    attach = ()
    flg = False

    for divnum in ["1", "2"]:
        try:  # 첨부파일이 1개인 경우
            xpath = xpathFinder(type, divnum, j)
            id = elementFinder(postnum_str, type, xpath, "href")
            driver.find_element(By.XPATH, xpath).get_attribute("href")
            driver.implicitly_wait(0.5)
            attach = attach + (id,)
            flg = True
        except:
            pass

    if flg is False:  # 첨부파일이 없거나 2개 이상인 경우
        if type == "공지":
            for divnum in ["1", "2"]:
                i = 1
                while True:
                    j = str(i)
                    try:  # 첨부파일이 2개 이상인 경우
                        xpath = xpathFinder(type, divnum, j)
                        id = elementFinder(postnum_str, type, xpath, "href")
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
                    xpath = xpathFinder(type, divnum, j)
                    id = elementFinder(postnum_str, type, xpath, "href")
                    driver.implicitly_wait(0.5)
                    attach = attach + (id,)
                    i = i + 1
                except:  # 첨부파일이 0개인 경우
                    break

    return attach


# 프로세스 실행
def Process():
    driver.implicitly_wait(10)
    time.sleep(3)
    Scroll()

    # 총 게시글 수 세기
    postnum_int = 1
    while True:
        postnum_str = str(postnum_int)
        try:
            elementFinder(postnum_str, "main", "", "self")
            driver.implicitly_wait(1)
        except:
            postmax = postnum_int - 1
            break

        postnum_int = postnum_int + 1

    # 빈 딕셔너리 생성
    pdict = {}
    postnum_int = 1

    while True:
        postnum_str = str(postnum_int)
        try:
            errorchk = elementFinder(postnum_str, "main", "", "jsaction")
            driver.implicitly_wait(1)
        except:  # 게시물이 삭제되었을 때 postmax에서 예외가 발생하기 때문
            break

        if errorchk is None:
            post_type = "공지"
            post_uploader = uploaderExtractor(postnum_str, post_type)
            post_date = finalDateExtractor(postnum_str, post_type)
            post_body_HTML = bodyExtractor(postnum_str, post_type, "innerHTML")
            post_body_text = bodyExtractor(postnum_str, post_type, "text")
            post_attach = attachExtractor(postnum_str, post_type)
            plist = (post_type, post_uploader, post_date, post_body_HTML, post_body_text, post_attach)
            pdict.update({postnum_int: plist})

        else:
            post_type = typeExtractor(postnum_str)
            elementFinder(postnum_str, "main", "", "click")
            time.sleep(2)
            post_uploader = uploaderExtractor(postnum_str, post_type)
            post_date = finalDateExtractor(postnum_str, post_type)
            post_body_HTML = bodyExtractor(postnum_str, post_type, "innerHTML")
            post_body_text = bodyExtractor(postnum_str, post_type, "text")
            post_attach = attachExtractor(postnum_str, post_type)
            plist = (post_type, post_uploader, post_date, post_body_HTML, post_body_text, post_attach)
            pdict.update({postnum_int: plist})

            driver.execute_script("window.history.go(-1)")
            driver.implicitly_wait(2)

        if postnum_int < postmax:
            postnum_int = postnum_int + 1

        else:
            break

    return pdict


# 메일 내용 가공 및 전송
def SendMsg(status, mail_path, room_name, room_color, post_type, post_uploader, post_postlink, post_or_del_date, post_body_HTML, post_body_text):
    message = open(mail_path, "r", encoding="utf-8").read()

    if post_type == "공지":
        message = message.replace("${body}", post_body_HTML)
        post_smalltext = '<tr height="0"></tr>'
    else:
        post_title = post_body_HTML.split("\n", 1)[0]  # \n을 기준으로 최대 1번 쪼갠 뒤 그 중 첫번째(0번째) 부분
        message = message.replace("${body}", post_title)
        post_smalltext = ('<tr height="4px"></tr><tr><td style="color:#5f6368;font-size:14px;font-weight:400;line-height:20px;letter-spacing:0.2px">' + post_body_HTML.split("\n", 1)[1] + "</td></tr>")

    if post_type == "질문":
        message = message.replace("${postposition}", "을")
    else:
        message = message.replace("${postposition}", "를")

    message = message.replace("${google_id]", login_id)
    message = message.replace("${roomlink}", link)
    message = message.replace("${room}", room_name)
    message = message.replace("${color1}", room_color)
    message = message.replace("${color2}", colordict[room_color])
    message = message.replace("${uploader}", post_uploader)
    message = message.replace("${type}", post_type)
    message = message.replace("${date}", post_or_del_date)  # 수정된 게시물: post_date, 삭제된 게시물: del_date
    message = message.replace("${postlink}", post_postlink)  # 수정된 게시물에만 존재
    message = message.replace("${imgsrc}", imgdict[post_type])
    message = message.replace("${smalltext}", post_smalltext)

    # 메일 제목
    if len(post_body_text) < 20:
        title = status + "된 " + post_type + ": '" + post_body_text + "'"
    else:
        title = status + "된 " + post_type + ": '" + post_body_text[0:20] + "...'"

    for address in sendto:
        # 메일 전송
        msg = MIMEText(message, "html")
        msg["Subject"] = title
        msg["From"] = sendfrom_id
        msg["To"] = address

        with smtplib.SMTP_SSL("smtp.naver.com", 465) as smtp:
            smtp.login(sendfrom_id, sendfrom_pw)
            smtp.sendmail(sendfrom_id, sendfrom_id, msg.as_string())


# 게시물 수정 시
def MsgEdited(pdict_before, pdict_after, room_name):
    room_color = colorExtractor()
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
        if post_type == "공지":
            elementFinder(key_str, "main", "/div[1]/div[1]/div[4]/div/div/div", "click")
        else:
            elementFinder(key_str, "main", "/div[1]/div/div[6]/div/div/div", "click")

        time.sleep(1)
        elementFinder(key_str, "link_copy", "", "click")
        post_postlink = pyclip.paste(text=True)
        pyclip.clear()
        mail_path = file_path + slash + "src" + slash + "mail_edited.html"
        SendMsg("수정", mail_path, room_name, room_color, post_type, post_uploader, post_postlink, post_date, post_body_HTML, post_body_text)


# 게시물 삭제 시
def MsgRemoved(pdict_before, pdict_after, room_name):
    room_color = colorExtractor()
    set_before = set(pdict_before.values())
    set_after = set(pdict_after.values())
    diff = list(set_before - set_after)
    for val in diff:
        post_type = val[0]
        post_uploader = val[1]
        post_body_HTML = val[3]
        post_body_text = val[4]
        del_date = datetime.now(timezone("Asia/Seoul")).strftime("%-m월 %-d일")
        mail_path = file_path + slash + "src" + slash + "mail_deleted.html"
        SendMsg("삭제", mail_path, room_name, room_color, post_type, post_uploader, "", del_date, post_body_HTML, post_body_text)


# main 함수
if __name__ == "__main__":
    driver = init_driver()
    login(driver, login_id, login_pw)

    # 최초 딕셔너리
    pdict_1 = Process()

    # 전후 비교
    while True:
        time.sleep(3)
        driver.refresh()
        pdict_2 = Process()

        if pdict_1 != pdict_2:
            time.sleep(3)
            driver.refresh()
            pdict_3 = Process()  # 모두 로딩될 때까지 기다려도 간혹 페이지 로딩이 끝까지 되지 않은 채로 크롤링될 때가 있음. 버그 예방을 위해 한 번 더 검증
            room_name = driver.find_element(By.XPATH, "//*[@class='tNGpbb YrFhrf-ZoZQ1 YVvGBb']").text

            if pdict_1 == pdict_3:
                print("'" + room_name + "'에서 버그 발견. [" + datetime.now().strftime("%H:%M:%S") + "]")
            
            else:
                if len(pdict_1) > len(pdict_3):
                    print("'" + room_name + "'에서 삭제된 게시물 감지. [" + datetime.now().strftime("%H:%M:%S") + "]")  # 삭제와 수정이 동시에 일어난 경우일 수도 있음. 이 경우, 둘 다 삭제된 게시물로 간주함. (버그 해결 예정)
                    MsgRemoved(pdict_1, pdict_3, room_name)
                    print("메일 발신 완료.")

                elif len(pdict_1) == len(pdict_3):
                    print("'" + room_name + "'에서 변경된 게시물 감지. [" + datetime.now().strftime("%H:%M:%S") + "]")
                    MsgEdited(pdict_1, pdict_3, room_name)
                    print("메일 발신 완료.")

                else:
                    print("'" + room_name + "'에서 새로운 게시물 감지. 클래스룸에서 발신된 메일을 확인하세요. [" + datetime.now().strftime("%H:%M:%S") + "]")
            
            pdict_1 = pdict_3

        else:
            room_name = driver.find_element(By.XPATH, "//*[@class='tNGpbb YrFhrf-ZoZQ1 YVvGBb']").text
            print("'" + room_name + "'에서 변경사항 없음. [" + datetime.now().strftime("%H:%M:%S") + "]")
            pdict_1 = pdict_2
