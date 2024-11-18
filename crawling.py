from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

# ChromeDriver 경로 설정
chrome_driver_path = "./chromedriver-mac-arm64/chromedriver"

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--headless")  # 브라우저 창을 띄우지 않음
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# 드라이버 설정
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# 웹페이지 열기
url = "{올리브영 검색 페이지 주소}"
driver.get(url)

# 페이지가 로드될 때까지 대기
wait = WebDriverWait(driver, 5)  # 최대 5초 대기
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "li_result")))

# 데이터 추출
products = driver.find_elements(By.CLASS_NAME, "li_result")
for product in products:
  # 브랜드 이름 추출
  brand = product.find_element(By.CLASS_NAME, "tx_brand").text
  # 제품명 추출
  name = product.find_element(By.CLASS_NAME, "tx_name").text

  # 원가 추출 (요소가 없을 경우 예외 처리)
  try:
    price = product.find_element(By.CSS_SELECTOR, ".tx_org .tx_num").text
  except NoSuchElementException:
    price = "N/A"  # 요소가 없을 경우 기본값 설정

  print(f"브랜드: {brand}, 제품명: {name}, 원가: {price}")

# 드라이버 종료
driver.quit()
