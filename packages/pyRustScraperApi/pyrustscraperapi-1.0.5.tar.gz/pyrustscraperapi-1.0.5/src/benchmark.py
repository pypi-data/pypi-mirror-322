from pyRustScraperApi import Client
from pyRustScraperApi.models import Order
import json


def main():
    client = Client(
        "rs.36rvCoQMLdojo9yC7gmtZz2Gn"
    )
    order = Order(
		products=[
			"oz/1596079870",
      		"ym/1732949807-100352880819-5997015",
			"wb/300365052",
			"mm/100028286032",
			"https://www.ozon.ru/product/nozhnitsy-kantselyarskie-21-sm-calligrata-nerzhaveyushchaya-stal-plastik-173091046/",
			"https://www.wildberries.ru/catalog/95979396/detail.aspx",
			"https://market.yandex.ru/product--igrovaia-pristavka-sony-playstation-5-slim-digital-edition-bez-diskovoda-1000-gb-ssd-2-geimpada-bez-igr-belyi/925519649?sku=103706885579&uniqueId=162025048",
			"https://megamarket.ru/catalog/details/nabor-instrumentov-v-keyse-108-predmetov-100065768905/",
   "https://market.yandex.ru/product--fitnes-braslet-xiaomi-smart-band-9-pro-chernyi/948965996?sku=103728231962&uniqueId=892410&do-waremd5=i6vEgCgmCV01xoT9otRL-Q"
		],
		cookies=[],
  		proxy_pool=[]
	)
    order_hash = client.send_order(order)
    for task in client.stream_task(order_hash):
        print(task)

    print(f"\n\n{json.dumps(task.result, ensure_ascii=False, indent=4)}")


if __name__ == "__main__":
    main()
