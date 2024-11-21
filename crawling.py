from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
from data_management_mongoDB import *

# 삽입할 데이터 받아올 주소
url = "https://www.oliveyoung.co.kr/store/search/getSearchMain.do?query=%EC%BF%A0%EC%85%98&giftYn=N&t_page=%ED%99%88&t_click=%EA%B2%80%EC%83%89%EC%B0%BD&t_search_name=%EC%BF%A0%EC%85%98"

# 삽입할 데이터 정보
new_features = {
  "moisturizing": True,
  "whitening": True,
  "soothing": True,
  "wrinkle_removal": False,
  "hypoallergenic": True
}
new_suitable_skin_types = {
  "oily": True,
  "dry": False,
  "combination": True,
  "dehydrated": True,
  "normal": True,
  "acne": True,
  "sensitive": True
}

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
  # 원가 추출
  try:
    price = product.find_element(By.CSS_SELECTOR, ".tx_org .tx_num").text
    price = int(price.replace(",", ""))
  except NoSuchElementException:
    price = "N/A"

  # 기존 제품 데이터 조회
  existing_product = get_product_by_name(name)

  # 기존 데이터 존재하면 정보 업데이트
  if existing_product:
    # 기존 features와 병합
    for key, value in new_features.items():
      if key in existing_product["features"]:
        existing_product["features"][key] = existing_product["features"][key] or value
      else:
        existing_product["features"][key] = value

    for key, value in new_suitable_skin_types.items():
      if key in existing_product["suitable_skin_types"]:
        existing_product["suitable_skin_types"][key] = existing_product["suitable_skin_types"][key] or value
      else:
        existing_product["suitable_skin_types"][key] = value

    # 제품 데이터 업데이트
    update_product(existing_product["_id"], {
      "price": price,
      "features": existing_product["features"],
      "suitable_skin_types": existing_product["suitable_skin_types"]
    })
  else:
    # 새로운 제품 데이터 저장
    crawled_data = {
      "product_name": name,
      "brand_name": brand,
      "type": "toner",
      "price": price,
      "features": new_features,
      "suitable_skin_types": new_suitable_skin_types
    }
    add_product(crawled_data)

# 드라이버 종료
driver.quit()
