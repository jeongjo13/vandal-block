# 차단하지 않을 사용자(또는 이미 차단한 사용자(중복 차단 방지)) 리스트
blocked = []# 차단하지 않을 사용자(또는 이미 차단한 사용자(중복 차단 방지)) 리스트
# 감지할 반달성 키워드
vandalism = ["은 뒤져라", "는 뒤져라", "정좆", "jeongjot", "Fuck_", "사퇴 기원", "sibal_", "No_", "Nono_", "NO_", "FUCK_", "satoehaseyo", "must resign", "해웃돈을", "혁명본부 만세", "wikiRevolution", "wikirevolution", "사퇴를 촉구합니다", "#redirect 개새끼", "#redirect 좆병신", "#redirect 좆", "#redirect 병신", "#넘겨주기 병신", "#넘겨주기 개새끼", "#넘겨주기 좆병신", "#넘겨주기 좆"]
# 자신의 위키 로그인 아이디
wiki_username = ''
# 자신의 위키 로그인 비밀번호
wiki_password = ''
# 위키 주소
wiki_url = ""
# 위키 이름
wiki_name = ""
# 긴급 정지 토론 발제 문서
emergency_stop_document = ""

from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support.ui import Select
from datetime import datetime
import random

now = datetime.now()

def emergency_stop() : #사용자 토론 긴급 정지 여부 확인
    try :
        driver.get("%s/discuss/%s" % (wiki_url, emergency_stop_document))
        try:
            time.sleep(1)
            element = driver.find_element(By.XPATH, '//*[@id="1"]')
            thread_topic_element = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/h2/a')
            thread_topic_element.click()
            time.sleep(2)
            thread_comment = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/form[4]/div[1]/div[1]/span/textarea')
            thread_comment.send_keys("[알림] 사용자 토론에 의해 봇을 긴급 정지합니다. (이 댓글은 봇에 의해 작성되었습니다.)")
            thread_comment_submit = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/form[4]/div[2]/button')
            thread_comment_submit.click()
            print("[알림] 사용자 토론에 의해 봇을 긴급 정지합니다.")
            return True
        except NoSuchElementException:
            return False
    except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
        print("[오류!] 사용자 토론 긴급 정지 여부를 검토할 수 없습니다.")
def block(document_, blocking, rev) : #문서 편집으로 인한 차단 시 차단하는 함수
    if blocking not in blocked :
        driver.get("%s/aclgroup?group=차단된 사용자" % wiki_url)
        option1 = driver.find_element(By.XPATH,'//*[@id="modeSelect"]') #ACLGroup 창의 아이피, 사용자 이름 여부 선택란
        dropdown1 = Select(option1)
        dropdown1.select_by_value("username")
        option2 = driver.find_element(By.XPATH,'//*[@id="usernameInput"]') #ACLGroup 창의 사용자 이름 입력란
        option2.send_keys(blocking)
        option3 = driver.find_element(By.XPATH,'//*[@id="noteInput"]') #ACLGroup 창의 메모 입력란
        option3.send_keys("%s r%d 긴급차단 | 자동 차단 (잘못된 경우 \'%s:차단 소명 게시판\'에 토론 발제 바랍니다. 오작동 시 \'%s\'에 토론 발제 바랍니다.)" % (block_memo(document_), rev, wiki_name, emergency_stop_document))
        option4 = driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/div[2]/div[2]/form[1]/div[3]/select') #ACLGroup 창의 기간 선택란
        dropdown2 = Select(option4)
        dropdown2.select_by_value("0")
        time.sleep(0.05)
        add_block = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/form[1]/div[4]/button') #ACLGroup 창의 추가 버튼
        add_block.click()
        blocked.append(blocking) #다른 사용자가 봇 오작동으로 보고 차단 해제했다면 다시 차단하는 것을 방지하기 위해 차단 제외 목록에 추가

def block_thread(thread, blocking, comment_number) : #토론으로 인한 차단 시 차단하는 함수
    if blocking not in blocked :
        driver.get("%s/aclgroup?group=차단된 사용자" % wiki_url)
        option1 = driver.find_element(By.XPATH,'//*[@id="modeSelect"]') #ACLGroup 창의 아이피, 사용자 이름 여부 선택란
        dropdown1 = Select(option1)
        dropdown1.select_by_value("username")
        option2 = driver.find_element(By.XPATH,'//*[@id="usernameInput"]') #ACLGroup 창의 사용자 이름 입력란
        option2.send_keys(blocking)
        option3 = driver.find_element(By.XPATH,'//*[@id="noteInput"]') #ACLGroup 창의 메모 입력란
        option3.send_keys("토론 %s #%d 긴급차단 | 자동 차단 (잘못된 경우 \'%s:차단 소명 게시판\'에 토론 발제 바랍니다. 오작동 시 \'%s\'에 토론 발제 바랍니다.)" % (thread, comment_number, wiki_name, emergency_stop_document))
        option4 = driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/div[2]/div[2]/form[1]/div[3]/select') #ACLGroup 창의 기간 선택란
        dropdown2 = Select(option4)
        dropdown2.select_by_value("0")
        time.sleep(0.05)
        add_block = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/form[1]/div[4]/button') #ACLGroup 창의 추가 버튼
        add_block.click()
        blocked.append(blocking) #다른 사용자가 봇 오작동으로 보고 차단 해제했다면 다시 차단하는 것을 방지하기 위해 차단 제외 목록에 추가

def block_edit_request(blocking, edit_request_url) :
    if blocking not in blocked :
        driver.get("%s/aclgroup?group=차단된 사용자" % wiki_url)
        option1 = driver.find_element(By.XPATH,'//*[@id="modeSelect"]') #ACLGroup 창의 아이피, 사용자 이름 여부 선택란
        dropdown1 = Select(option1)
        dropdown1.select_by_value("username")
        option2 = driver.find_element(By.XPATH,'//*[@id="usernameInput"]') #ACLGroup 창의 사용자 이름 입력란
        option2.send_keys(blocking)
        option3 = driver.find_element(By.XPATH,'//*[@id="noteInput"]') #ACLGroup 창의 메모 입력란
        option3.send_keys("%s 긴급차단 | 자동 차단 (잘못된 경우 \'%s:차단 소명 게시판\'에 토론 발제 바랍니다. 오작동 시 \'%s\'에 토론 발제 바랍니다.)" % (edit_request_url, wiki_name, emergency_stop_document))
        option4 = driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/div[2]/div[2]/form[1]/div[3]/select') #ACLGroup 창의 기간 선택란
        dropdown2 = Select(option4)
        dropdown2.select_by_value("0")
        time.sleep(0.05)
        add_block = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/form[1]/div[4]/button') #ACLGroup 창의 추가 버튼
        add_block.click()
        blocked.append(blocking) #다른 사용자가 봇 오작동으로 보고 차단 해제했다면 다시 차단하는 것을 방지하기 위해 차단 제외 목록에 추가

def get_doc_text() : #문서 RAW 읽어오는 함수
    doc_text_field = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/textarea')
    doc_text = doc_text_field.text #문서 RAW 란에 있는 내용 읽어오기
    return doc_text #문서 RAW 반환

def block_memo(name) : #차단 사유에 문서명을 문서:~~~, 하늘위키:~~~과 같이 들어갈 것을 지정해줌
    #만약 문서 이름공간에서의 반달이라면
    if not name.startswith("%s:" % wiki_name) :
        if not name.startswith("틀:") :
            if not name.startswith("분류:") :
                if not name.startswith("파일:") :
                    if not name.startswith("휴지통:") :
                        if not name.startswith("파일:") :
                            if not name.startswith("위키관리:") :
                                if not name.startswith("위키운영:") :
                                    if not name.startswith("가상위키:") :
                                        name = "문서:" + name #차단 사유의 문서명 앞에 문서:를 붙임
    return(name) #문서명 반환
def close_edit_request(edit_request) :
    driver.get(edit_request)
    close_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/div[5]/div/span/button')
    close_button.click()
    time.sleep(1)
    close_memo = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/div[4]/div/form/div/div[2]/input')
    close_memo.send_keys("반달 복구: 반달을 멈추시고 %s에 정상적으로 기여해 주시기 바랍니다. | 자동 편집 요청 닫기 (잘못된 경우 \'%s:문의 게시판\'에 토론 발제 바랍니다. 오작동 시 \'%s\'에 토론 발제 바랍니다." % (wiki_name, wiki_name, emergency_stop_document))
    close_submit = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/div[4]/div/form/div/div[3]/button[1]')
    close_submit.click()

def revert(doc, rev) : #반달성 편집 되돌리는 함수
    rev = rev - 1
    driver.get("%s/revert/%s?rev=%s" % (wiki_url, doc, rev)) #해당 문서의 정상적인 리비전으로 되돌리는 페이지에 접속
    try :
        time.sleep(0.5)
        revert_reason = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/form/input')
        revert_reason.send_keys("반달 복구: 반달을 멈추시고 %s에 정상적으로 기여해 주시기 바랍니다. | 자동 되돌리기 (잘못된 경우 \'%s:문의 게시판\'에 토론 발제 바랍니다. 오작동 시 \'%s\'에 토론 발제 바랍니다." % (wiki_name, wiki_name, emergency_stop_document)) #편집 요약
        revert_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/form/div/button')
        revert_button.click() #되돌리기 클릭
    except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
        print("[오류!] 반달성 편집을 되돌리지 못했습니다.")


def trash(doc) : #반달성 문서 휴지통화시키는 함수
    if "사용자:" not in doc :
        try :
            driver.get('%s/delete/%s' % (wiki_url, doc))
            delete_reason = driver.find_element(By.XPATH,'//*[@id="logInput"]') # 문서 삭제 시 편집 요약
            revert_reason.send_keys("반달 복구: 반달을 멈추시고 %s에 정상적으로 기여해 주시기 바랍니다. | 자동 삭제 (잘못된 경우 \'%s:문의 게시판\'에 토론 발제 바랍니다. 오작동 시 \'%s\'에 토론 발제 바랍니다." % (wiki_name, wiki_name, emergency_stop_document)) #편집 요약
            delete_check = driver.find_element(By.XPATH,'//*[@id="agreeCheckbox"]')
            delete_check.click()
            delete_button = driver.find_element(By.XPATH, '//*[@id="submitBtn"]')
            delete_button.click() #문서 삭제 버튼 클릭
        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
            print("[오류!] 문서를 삭제할 수 없습니다.")
        try :
            driver.get('%s/move/%s' % (wiki_url, doc))
            move_document = driver.find_element(By.XPATH,'//*[@id="titleInput"]') #문서 이동 시 사용할 휴지통 문서명
            move_document.send_keys('휴지통:%s' % trashname())
            move_document_memo = driver.find_element(By.XPATH,'//*[@id="logInput"]')
            revert_reason.send_keys("반달 복구: 반달을 멈추시고 %s에 정상적으로 기여해 주시기 바랍니다. | 자동 휴지통화 (잘못된 경우 \'%s:문의 게시판\'에 토론 발제 바랍니다. 오작동 시 \'%s\'에 토론 발제 바랍니다." % (wiki_name, wiki_name, emergency_stop_document)) #편집 요약
            move_button = driver.find_element(By.XPATH,'//*[@id="moveForm"]/div[4]/button')
            move_button.click() #문서 이동 버튼 클릭
        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
            print("[알림] 문서를 휴지통화할 수 없습니다.")

def trashname() : #휴지통화할 때 휴지통 문서명 반환해주는 함수
    a = random.randrange(1000000000, 9999999999) #랜덤한 10자리 수 지정 후
    return (a) #반환

def check_thread(thread) : #토론 주소에서 토론 ~~~의 부분만 반환
    thread = thread[27:] #https://위키주소/thread/부분은 자르고 나머지 부분만 남김 (다른 위키에서 사용 시 수정 필요)
    return(thread) #토론 주소 반환

def check_thread_user(thread) :
    driver.get(thread)
    time.sleep(10) #토론 로딩 완료까지 기다림
    try :
        thread_user_text = driver.find_element(By.XPATH, '//*[@id="res-container"]/div[1]/div/div[1]/a') #1번 댓글 작성자 식별
        thread_user = thread_user_text.text
        return(thread_user) #토론 발제자 값 반환
    except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) :
        print("[오류!] 토론 발제자를 식별하지 못했습니다.")

def close_thread(thread) : #토론 닫기 함수
    driver.get(thread)
    close_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/form[1]/button') #토론 상태 변경에서 '변경' 버튼
    close_button.click()
    time.sleep(1)
    new_document = driver.find_element(By.XPATH, '//*[@id="thread-document-form"]/input') #토론 문서 변경에서 토론 문서를 '휴지통:토론 휴지통'으로
    new_document.send_keys(Keys.CONTROL,'a', Keys.BACKSPACE)
    new_document.send_keys('휴지통:토론 휴지통')
    update_thread_document_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/form[2]/button')
    update_thread_document_button.click() #토론 문서 변경 버튼 클릭
    time.sleep(1)
    new_topic = driver.find_element(By.XPATH, '//*[@id="thread-topic-form"]/input')#토론 주제 변경 입력란
    new_topic.send_keys(Keys.CONTROL,'a', Keys.BACKSPACE)
    new_topic.send_keys('자동으로 휴지통화된 스레드') #새 토론 주제 (강제 조치와 같은 걸로 변경하고 싶으면 이걸 수정 바람)
    update_thread_topic_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/form[3]/button')
    update_thread_topic_button.click() # 토론 주제 변경 클릭

# Chrome WebDriver 초기화
driver = webdriver.Chrome()

# 크롬 드라이버에 URL 주소 넣고 실행
driver.get("{}/member/login?redirect=%2Faclgroup".format(wiki_url))
time.sleep(2.5)  # 페이지가 완전히 로딩되도록 2.5초 동안 기다림

# 아이디 입력
username = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/form/div[1]/input')
username.send_keys(wiki_username)
time.sleep(0.5)

# 비밀번호 입력
password = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/form/div[2]/input')
password.send_keys(wiki_password)
time.sleep(0.5)

auto_login_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/form/div[3]/label/input')
auto_login_button.click()

# 로그인 버튼 클릭
login_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/form/button')
login_button.click()
time.sleep(1)

document_names = []
while True :
    try :
        # RecentChanges 페이지로 이동
        driver.get('%s/RecentChanges?logtype=create' % wiki_url)
        time.sleep(0.4)

        # 페이지 소스 가져오기
        page_source = driver.page_source

        # BeautifulSoup을 사용하여 페이지 소스를 파싱
        soup = bs(page_source, 'html.parser')

        # 최근 변경된 문서 목록 추출
        links = soup.find_all('a', href=True)

        # 문서명 추출
        for link in links:
            href = link.get('href')
            if href.startswith('/w/') and link.text.strip():
                document_names.append(link.text.strip())
        try :
            document_names.remove("내 사용자 문서")
        except ValueError :
            print("[오류!] 리스트에서 사용자 문서를 제거할 수 없습니다.")
        print(document_names)

        edited_document = []
        edited_user = []

        for index, value in enumerate(document_names):
            if index % 2 == 0:
                edited_document.append(value)
            else:
                edited_user.append(value)

        print(edited_document)
        print(edited_user)

        for i,j in zip(edited_document,edited_user) :
            if any(v in i for v in vandalism):
                block(i, j, 1)
                trash(i)
    except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
        print("[오류!] 최근 변경의 새 문서 탭을 검토할 수 없습니다.")
    if emergency_stop() == True :
        break
    # 문서 변경사항 검토
    # RecentChanges 페이지로 이동
    try :
        driver.get('%s/RecentChanges' % wiki_url)
        time.sleep(0.4)

        # 페이지 소스 가져오기
        page_source = driver.page_source

        # BeautifulSoup을 사용하여 페이지 소스를 파싱
        soup = bs(page_source, 'html.parser')

        # 최근 변경된 문서 목록 추출
        links = soup.find_all('a', href=True)

        # 문서명 추출
        document_names.clear()
        for link in links:
            href = link.get('href')
            if href.startswith('/w/') and link.text.strip():
                document_names.append(link.text.strip())
        num = 0
        for i,j in zip(edited_document,edited_user) :
            driver.get('%s/history/%s' % (wiki_url, i))
            time.sleep(0.5)
            try :
                version = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/ul/li[1]/strong[1]')
                lastest_version = version.text  #해당 문서의 최신 리비전
                lastest_version = lastest_version[1:]
                lastest_version = int(lastest_version)
                if lastest_version > 1 :
                    driver.get("%s/raw/%s?rev=%d" % (wiki_url, i, lastest_version))
                    time.sleep(0.5)
                    lastest_doc = get_doc_text()
                    driver.get("%s/raw/%s?rev=%d" % (wiki_url, i, lastest_version-1))
                    time.sleep(0.5)
                    prev_doc = get_doc_text()
                    for k in vandalism :
                        if k in lastest_doc :
                            if k not in prev_doc :
                                block(i, j, lastest_version)
                                revert(i, lastest_version)
                                break
                else :
                    driver.get("%s/raw/%s?rev=%d" % (wiki_url, i, lastest_version))
                    time.sleep(0.5)
                    lastest_doc = get_doc_text()
                    for k in vandalism :
                        if k in lastest_doc :
                            block(i, j, lastest_version)
                            trash(i)
                            break
            except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
                print("error")
            num += 1;
            if num >= 11 :
                num = 0
                break
            time.sleep(0.01)
    except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
        print("[오류!] 최근 변경의 전체 탭을 검토할 수 없습니다.")
    if emergency_stop() == True :
        break
    #최근 토론에서 반달성 제목을 가진 토론 추출 및 차단
    try :
        driver.get("%s/RecentDiscuss" % wiki_url)
        time.sleep(0.4)

        # 페이지 소스 가져오기
        page_source = driver.page_source

        # BeautifulSoup을 사용하여 페이지 소스를 파싱
        soup = bs(page_source, 'html.parser')

        threads = []
        thread_url = []
        thread_text = []

        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if href.startswith('/thread/'):
                full_url = f"{wiki_url}{href}"
                text = a_tag.get_text(strip=True)
                thread_url.append(full_url)
                thread_text.append(text)
        print(thread_url)
        print(thread_text)

        for i,j in zip(thread_text,thread_url) :
            for k in vandalism :
                if k in i :
                    block_thread(check_thread(j), check_thread_user(j), 1)
                    close_thread(j)
    except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
        print("[오류!] 최근 토론을 검토할 수 없습니다.")
    #최근 편집 요청 검토
    try :
        driver.get(f"{wiki_url}/RecentDiscuss?logtype=open_editrequest")
        time.sleep(0.4)

        # 페이지 소스 가져오기
        page_source = driver.page_source

        # BeautifulSoup을 사용하여 페이지 소스를 파싱
        soup = bs(page_source, 'html.parser')

        edit_request_url = []
        edit_request_text = []

        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if href.startswith('/edit_request/'):
                full_url = f"{wiki_url}{href}"
                text = a_tag.get_text(strip=True)
                edit_request_url.append(full_url)
                edit_request_text.append(text)
        print(edit_request_url)
        print(edit_request_text)
        for i, j in zip(edit_request_url, edit_request_text):
            driver.get(i)
            edit_request_document_link = driver.find_element(By.XPATH, '//*[@id="main_title"]/a')
            edit_request_document = edit_request_document_link.text
            #해당 편집 요청의 기준판 알아내기
            version = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/div[2]')
            lastest_version = version.text  # 해당 문서의 최신 리비전
            lastest_version = lastest_version[6:]
            lastest_version = int(lastest_version)
            #해당 편집 요청의 기준 판 RAW 불러오기
            driver.get("%s/raw/%s?rev=%d" % (wiki_url, edit_request_document, lastest_version))
            time.sleep(0.5)
            lastest_doc = get_doc_text()

            driver.get(i)
            edit_request_diff_element = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/div[6]/div[1]/table/tbody')
            edit_request_diff = edit_request_diff_element.text

            edit_request_user_text = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[2]/h3/a')
            edit_request_user = edit_request_user_text.text

            for k in vandalism:
                if k in edit_request_diff:
                    if k not in lastest_doc :
                        block_edit_request(edit_request_user, j)
                        close_edit_request(i)
                        break
    except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
        print("[오류!] 최근 편집 요청을 검토할 수 없습니다.")
