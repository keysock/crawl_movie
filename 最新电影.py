import requests
from lxml import etree
import re
import pymysql

def get_movieInfo(url):
    response = requests.get(url=url, headers=headers)
    response.encoding = response.apparent_encoding
    page_text = response.text
    return page_text

if __name__=='__main__':
    db = pymysql.connect(host='localhost', user='root', password='20010617', database='moviedb', charset='utf8mb4')
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'
    }
    url='https://www.ygdy8.com'
    page_text=etree.HTML(get_movieInfo(url))
    movie_hrefs=page_text.xpath('//div[@class="co_content2"]/ul/a/@href')
    print(movie_hrefs)
    infos = []
    for href in movie_hrefs[1::]:
        url='https://www.ygdy8.com'+href
        pattern=re.compile('<div id="Zoom">.*?(译　　名|片　　名)　(.*?)<br />.*?上映日期　(.*?)<br />.*?(IMDb评分|豆瓣评分)　(.*?)<br />.*?<a href="(.*?)".*?</div>',re.S)
        # pattern=re.compile('<div id="Zoom">.*?</div>',re.S)

        m=pattern.findall(get_movieInfo(url))
        print(m)
        if m:
            info=(m[0][1],m[0][2],m[0][4],m[0][5])
            infos.append(info)
    sql = "INSERT INTO `moviedb`.`movie`(`名称`,`上映时间`,`豆瓣评分`,`下载地址`)VALUES (%s,%s,%s,%s)"
    db.cursor().executemany(sql,infos)
    db.commit()
    print('运行完毕！！！！')

