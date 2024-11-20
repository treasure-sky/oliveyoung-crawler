from pymongo import MongoClient

# MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")
db = client["cosmetic_db"]

brands_collection = db["brands"]
products_collection = db["products"]

def get_brand_id_by_name(brand_name):
  """DB에서 브랜드 ID 조회

  Args:
    brand_name (str): 브랜드 이름

  Returns:
    str: 브랜드 ID
  """
  brand = brands_collection.find_one({"name": brand_name})

  if brand:
    # 브랜드가 존재하면 _id 반환
    return brand["_id"]
  else:
    # 브랜드가 없으면 None 반환
    return None

def add_brand(brand_name):
  """DB에 새로운 브랜드 추가   

  Args:
    brand_name (str): 브랜드 이름

  Returns:
    str: 브랜드 ID
  """
  new_brand = {
    "name": brand_name,
    "website_url": None,
    "description": None,
  }
  brand_id = brands_collection.insert_one(new_brand).inserted_id
  print(f"added new brand: {new_brand}")
  return brand_id


def add_product(product_data):
  """제품 데이터를 데이터베이스에 저장

  Args:
    product_data (dict): 저장할 제품의 데이터
  """
  
  # 제품 데이터 삽입
  products_collection.insert_one(product_data)
  print(f"added new product: {product_data["product_name"]}")
  
def get_product_by_name(product_name):
  """제품 이름으로 제품 조회

  Args:
    product_name (str): 제품 이름

  Returns:
    dict: 제품 데이터
  """
  return products_collection.find_one({"product_name": product_name})

def update_product(product_id, update_data):
  """제품 데이터 업데이트

  Args:
    product_id (ObjectId): 업데이트할 제품의 ID
    update_data (dict): 업데이트할 데이터
  """
  products_collection.update_one(
    {"_id": product_id},
    {"$set": update_data}
  )
  print(f"updated product id: {product_id}")
