import requests
from bs4 import BeautifulSoup
import re
import mysql.connector
from datetime import datetime
from mysql_connect import  connect

article_href = []
url = "https://www.ptt.cc/bbs/MacShop/search?q=Apple+Watch"
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
	db = connect('Ptt_Web_Crawler')
	cursor=db.cursor()
	# ptt article start from <div class= title>
	articles = request_parsing(url, "div.title")
	# print(articles)
	#get each article title
	for item in articles:
		# get each article's url
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
					product_type, product_spec, product_location, product_price, product_insurance = None, None, None, None, None
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
							print("paring error", content)
							print("https://www.ptt.cc", item_href)
				# Insert Multiple Records
				# print(product_price)
				find = "SELECT * from apple_watch WHERE url = %s"
				cursor.execute(find, ("https://www.ptt.cc" + item_href,))
				find_result = cursor.fetchall()
				# print(cursor.fetchall())
				if not find_result:
					try: 
						sqlStuff = "INSERT INTO apple_watch (name, type, spec, location, price, post_at, url, insurance, created_at) VALUES (%s,%s, %s, %s, %s, %s , %s, %s, %s)"
						# if use [(data)] need to use executemany else () use execute
						records = [(name, product_type, product_spec, product_location, product_price, post_at,  "https://www.ptt.cc" + item_href, product_insurance, datetime.now())]
						cursor.executemany(sqlStuff, records)
						db.commit()
						print(cursor.rowcount, "Record inserted successfully into Apple_Watch table")
					except mysql.connector.Error as error:
						print("Failed to insert into MySQL table {}".format(error))
				else:
					print("https://www.ptt.cc" + item_href, "have been added before")

	if (db.is_connected()):
		cursor.close()
		db.close()
		print("MySQL connection is closed")




main(url)