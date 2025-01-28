import requests
from bs4 import BeautifulSoup
import time

class ResearchProduct(object) :
    # インスタンスの初期化
    def __init__(self, keyword: str, max_pages: int = 1):
        # キーワード検索の文字列を受け取る
        self.keyword = keyword
        # 検索結果ページの最大数を受け取る
        self.max_pages = max_pages

    def getAmazonHTML(self, page: int)->BeautifulSoup:
        # AmazonのURLを構築（日本の場合）
        base_url = "https://www.amazon.co.jp/s"
        # 検索クエリをURLエンコード
        query_params = {"k": self.keyword}
        query_params["page"] = page
        # リクエストヘッダー（Amazonのボット対策のため）
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        # HTMLを取得
        response = requests.get(url = base_url, params = query_params, headers = headers)
        print(response.url)
        soup = BeautifulSoup(response.content, "html.parser")

        return soup

    def getAmazonProducts(self):
        # 商品情報を入れるリストを作成
        result_list = []
        
        # 最大ページ数まで繰り返す
        for num in range(1, self.max_pages + 1):
            # サーバに負荷がかからないように指定の時間待機する
            if not num == 1:
                print("・・・待機中・・・")
                time.sleep(5)

            # 検索結果のページを指定
            soup = self.getAmazonHTML(page = num)

            # forループで一つずつ商品を取得
            for product in soup.find_all("div", class_ = "a-section a-spacing-base"):
                # 商品名を取得
                name_tag = product.find("h2", class_ = "a-size-base-plus a-spacing-none a-color-base a-text-normal")
                product_name = name_tag.text

                # 価格を取得
                price_tag = product.find("span", class_ = "a-price-whole")
                product_price = int(price_tag.text.replace(",", "").replace("￥", "").replace("¥", "").replace("円", "")) if not price_tag is None else -1
                
                # URLを取得
                product_url = "https://www.amazon.co.jp" + product.find("a", class_ = "a-link-normal s-no-outline")["href"]

                # ASINを取得
                asin_start = -1
                product_asin = None
                count_b0 = product_url.count("B0") # ASINの最初の文字(B0)の数を取得
                for i in range(count_b0): # count_b0の分だけループ
                    # asin_startを次のスタート地点で上書き
                    asin_start = product_url.find("B0", asin_start + 1)
                    # スタート地点からスライスで10文字分カット
                    asin = product_url[asin_start:asin_start+10]
                    # ASINではない文字列を除外し、ASINを更新
                    if asin != product_asin and not "%" in asin and not "-" in asin:
                        product_asin = asin

                # リストに商品名・価格・URLの情報を追加
                result_list.append({
                    "name": product_name,
                    "price": product_price,
                    "asin": product_asin,
                    "url": product_url
                })
        return result_list
