# 仮想環境の作成
# python3 -m venv .venv
# 仮想環境への切り替え
# . .venv/bin/activate

# pip3 install requests beautifulsoup4 openpyxl

import openpyxl
import time
from excel_process import ExcelProcess
from research_product import ResearchProduct
from profit_calculator import Product

# Excelファイルの読み込み
wb = openpyxl.load_workbook("Amazon_research_temp.xlsx", data_only = True)
ws = wb["temp"]

# 始まりの行番号と終わりの行番号を指定
min_row = 2
max_row = 266

excel = ExcelProcess(worksheet = ws, min_row = min_row, max_row = max_row)
products_info = excel.getProductsInfo()

for i, item in enumerate(products_info):
    # 負荷がかからないように待機時間を設定
    if i != 0 : time.sleep(5)

    search_keyword = item["keyword"]
    purchase_price = item["price"]

    # max_pagesで検索結果の量を調整
    researchProduct = ResearchProduct(keyword = search_keyword, max_pages = 1)
    amazon_products = researchProduct.getAmazonProducts()
    asin_list = []
    for element in amazon_products:
        amazon_price = element["price"]
        asin = element["asin"]
        product = Product(purchase_price = purchase_price, amazon_prince = amazon_price)
        if product.judgeProfit() or product.amazon_price == -1:
            asin_list.append(asin)
        else:
            continue

    asin_list_str = str(asin_list).replace("[", "").replace("'", "").replace("]", "")

    ws.cell(row = min_row + i, column = 6).value = asin_list_str
    print(f"{i + 1} / {len(products_info)}")

# ファイルを保存
wb.save("out.xlsx")