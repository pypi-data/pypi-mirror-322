from pyRustScraperApi import Client
from pyRustScraperApi.models import Order
import json


def main():
    client = Client(
        "http://185.204.2.206",
        "rs.ikxwaxvQfBCgLt9RcnNCaOB4c"
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
			"https://megamarket.ru/catalog/details/nabor-instrumentov-v-keyse-108-predmetov-100065768905/"
		],
		cookies=[],
  		proxy_pool=["2kpF3S:GP1FUb@147.44.62.127:8000"]
	)
    order_hash = client.send_order(order)
    for task in client.stream_task(order_hash):
        print(task)
    print(f"\n\n{json.dumps(task.result, ensure_ascii=False, indent=4)}")


if __name__ == "__main__":
    main()
