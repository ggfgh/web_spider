import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning

url = 'https://www.cnblogs.com/AggSite/AggSitePostList'
json_list = [
    {"CategoryType":"SiteHome","ParentCategoryId":0,"CategoryId":808,"PageIndex":page,"TotalPostCount":4000,"ItemListActionName":"AggSitePostList"}
    for page in range(1,51)
]

headers = {
    'Cookie': 'Hm_lvt_866c9be12d4a814454792b1fd0fed295=1634929092; __gads=ID=40fb62362d389d3c:T=1634929094:S=ALNI_MawpTUVh5wwKkNwHQoA1zL84GQumg; _ga=GA1.2.461096539.1634929095; _gid=GA1.2.972441659.1634929096; _gat_gtag_UA_476124_1=1; Hm_lpvt_866c9be12d4a814454792b1fd0fed295=1634930373',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
}

def craw(json):
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    r = requests.post(url,headers=headers,json=json,verify=False)
    return r.text

def parse(html):
    # class = "post-item-title"
    soup = BeautifulSoup(html,"html.parser")
    links = soup.find_all("a",class_='post-item-title')
    return [ (link['href'], link.get_text()) for link in links]

if __name__ == "__main__":
    for result in parse(craw(json_list[3])):
         print(result)