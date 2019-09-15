import requests
from bs4 import BeautifulSoup
import re
import mysql.connector
from datetime import datetime
from mysql_connect import  connect
db = connect('Ptt_Web_Crawler')
cursor=db.cursor()
article_href = []
url = "https://www.ptt.cc/bbs/MacShop/search?q=macbook+pro+13"
# get response page from macshop
def request_parsing(url, tag, tag2 = None):
	# print(url, element)
	r = requests.get(url)
	# print(r.text)
	soup = BeautifulSoup(r.text, "html.parser")
	# print(soup)
	results = soup.select(tag)
	if tag2:
		a_tags = (soup.find_all('a', href=True))
		for a_tag in a_tags:
			a_tag.decompose()
		div_tags = (soup.select('div.richcontent'))

		for div_tag in div_tags:
			div_tag.decompose()
		# if url == "https://www.ptt.cc/bbs/MacShop/M.1568453004.A.88C.html":
		# 	print(soup)
		results2 = soup.select(tag2)
		return results, results2
	else:
		# print(results)
		return results
def main(url):

	articles = request_parsing(url, "div.title")
	# print(articles)
	#get each article title
	for item in articles:
		item_href = item.select_one("a").get("href")
		# print(item_href)
		if item_href:
			# print(item_href)
			titles, contents = request_parsing("https://www.ptt.cc" + item_href, "span.article-meta-value", "div.article-metaline")
			if titles and re.search("販售", titles[2].text):
				# print(re.search("販售", results2[2].text))
				name = titles[0].text
				post_at = datetime.strptime(titles[3].text, '%a %b %d %H:%M:%S %Y')
				# print('作者:', titles[0].text)
				# print('時間:', titles[3].text)
				# print(contents)
				for result in contents:
					product_type, product_spec, product_location, product_price = None, None, None, None
					# print(str(result.next_sibling))
					if str(result.next_sibling) and  (re.search("物品型號",str(result.next_sibling)) or re.search("交易價格",str(result.next_sibling))) :
						content = str(result.next_sibling)
						content = re.split("：|\n", content)
						content = list(filter(None, content))
						
						try:
							product_type = content[content.index('[物品型號]')+1] if '[物品型號]' in content else product_type
							product_spec = content[content.index('[物品規格]')+1] if '[物品規格]' in content else product_spec
							product_location = content[content.index('[交易地點]')+1] if '[交易地點]' in content else None
							product_price =  content[content.index('[交易價格]')+1] if '[交易價格]' in content else '0'

							product_insurance =  content[content.index('[保固日期]')+1] if '[保固日期]' in content else None
						except:
							print(content)
							print(item_href)
				# Insert Multiple Records
				# print(product_price)
				sqlStuff = "INSERT INTO MacBook_Pro (name, type, spec, location, price, post_at, url, insurance) VALUES (%s,%s, %s, %s, %s, %s , %s, %s)"
				records = [(name, product_type, product_spec, product_location, product_price, post_at,  "https://www.ptt.cc" + item_href, product_insurance)]
				cursor.executemany(sqlStuff, records)
				db.commit()



main(url)

# results = soup.select('div.article-metaline')
# for i in results:
# 	print("--------test")
# 	print(i.next_sibling)
# for result in results:
# 	print("-----------------------------------------")
# 	print(results)