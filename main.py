from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support.ui import Select

def block(document_, blocking) :
    if blocking not in blocked :
        driver.get('https://haneul.wiki/aclgroup?group=차단된 사용자')
        time.sleep(2)
        option1 = driver.find_element(By.XPATH,'//*[@id="modeSelect"]') #ACLGroup 창의 아이피, 사용자 이름 여부 선택란
        dropdown1 = Select(option1)
        dropdown1.select_by_value("username")
        time.sleep(0.7)
        option2 = driver.find_element(By.XPATH,'//*[@id="usernameInput"]') #ACLGroup 창의 사용자 이름 입력란
        option2.send_keys(blocking)
        time.sleep(0.7)
        option3 = driver.find_element(By.XPATH,'//*[@id="noteInput"]') #ACLGroup 창의 메모 입력란
        option3.send_keys("%s r0 긴급차단 | 자동 차단 (차단이 잘못된 경우 하늘위키:차단 소명 게시판에 토론 발제 바람)" % block_memo(document_))
        time.sleep(2)
        add_block = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[3]/form[1]/div[4]/button') #ACLGroup 창의 추가 버튼
        add_block.click()
        time.sleep(2)
def block_memo(name) : #차단 사유에 문서명을 문서:~~~, 하늘위키:~~~과 같이 들어갈 것을 지정해줌
    if "하늘위키" not in name :
        if "틀" not in name :
            if "분류" not in name :
                if "파일" not in name :
                    if "휴지통" not in name :
                        name = "문서:" + name
    return(name)

# 차단하지 않을 사용자(또는 이미 차단한 사용자(중복 차단 방지)) 리스트
blocked = []

# Chrome WebDriver 초기화
driver = webdriver.Chrome()

# 크롬 드라이버에 URL 주소 넣고 실행
driver.get('https://haneul.wiki/member/login?redirect=%2Faclgroup')
time.sleep(2.5)  # 페이지가 완전히 로딩되도록 2.5초 동안 기다림

# 아이디 입력
username = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[3]/form/div[1]/input')
username.send_keys('') #여기에 자신의 아이디
time.sleep(1)

# 비밀번호 입력
password = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[3]/form/div[2]/input')
password.send_keys('') #여기에 자신의 비밀번호
time.sleep(1)

# 로그인 버튼 클릭
login_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[3]/form/button')
login_button.click()
time.sleep(1)
while True :
    # RecentChanges 페이지로 이동
    driver.get('https://haneul.wiki/RecentChanges')
    time.sleep(1)

    # 페이지 소스 가져오기
    page_source = driver.page_source

    # BeautifulSoup을 사용하여 페이지 소스를 파싱
    soup = bs(page_source, 'html.parser')

    # 최근 변경된 문서 목록 추출
    links = soup.find_all('a', href=True)

    # 문서명 추출
    document_names = []
    for link in links:
        href = link.get('href')
        if href.startswith('/w/') and link.text.strip():
            document_names.append(link.text.strip())

    document_names.remove("내 사용자 문서")
    print(document_names)

    edited_document = []
    edited_user = []

    vandalism = ["사퇴하세요", "뒤져라","Fuck_","사퇴 기원"] #반달 문서 키워드를 여기에 추가

    for index, value in enumerate(document_names):
        if index % 2 == 0:
            edited_document.append(value)
        else:
            edited_user.append(value)

    print(edited_document)
    print(edited_user)

    for i,j in zip(edited_document,edited_user) :
        if any(v in i for v in vandalism):
            block(i, j)
    time.sleep(10)
