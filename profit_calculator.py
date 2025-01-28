# 利益計算をするプログラム

# Productクラスを定義
class Product(object):
    # インスタンスの初期化
    def __init__(self, purchase_price: int, amazon_prince: int, postage: int = 500, commission_rate: int = 10):
        # 仕入価格
        self.purchase_price = purchase_price
        # Amazon価格
        self.amazon_price = amazon_prince
        # 送料
        self.postage = postage
        # 手数料率
        self.commission_rate = commission_rate / 100
        
    # 販売手数料を取得するメソッド
    def getSalesCommission(self)->int:
        result = self.amazon_price * self.commission_rate * 1.1
        return round(result)
    
    # 利益を計算するメソッド
    def getProfit(self)->int:
        sales_commission = self.getSalesCommission()
        result = self.amazon_price - self.purchase_price - self.postage - sales_commission
        return result
    
    # 利益が出るか判定するメソッド
    def judgeProfit(self)->bool:
        return self.getProfit() > 100
    
    # 結果を出力するメソッド
    def outputResult(self)->str:
        return "仕入価格は" + format(self.purchase_price, ",") + "円です\n" + \
        "Amazon価格は" + format(self.amazon_price, ",") + "円です\n" + \
        "送料は" + format(self.postage, ",") + "円です\n" + \
        "手数料率は" + "{:.1f}".format(self.commission_rate * 100) + "％です\n" + \
        "販売手数料は" + format(self.getSalesCommission(), ",") + "円です\n" + \
        ("利益は" + format(self.getProfit(), ",") + "円です\n" if self.judgeProfit() else "利益は出ません\n")
