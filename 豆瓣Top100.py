import requests
from bs4 import BeautifulSoup
import re
import pandas
import openpyxl

#url = "https://movie.douban.com/top250?start=25&filter="
header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}

def taklehtml(resp):
    soup =BeautifulSoup(resp.content,"html.parser",exclude_encodings="utf-8")
    #print(soup)
    #文件标题
    title = soup.find("title").string

    li_items = soup.find("ol", class_="grid_view").findAll("div",class_="item")
    #print(li_items)

    datas=[]
    for item in li_items:
        # 电影名称
        name = item.find("div",class_="hd").find("span",class_="title").get_text()
        # 电影排名
        rank =item.find("div",class_="pic").find("em").get_text()
        # 年代
        years =item.find("div",class_="bd").find("p").get_text()
        years = re.findall(r'\d+',years)
        # 电影评分
        rating_num = item.find("div",class_="bd").find("div",class_="star").findAll("span",class_="rating_num")[0].get_text()
        # 评论人数
        comments = item.find("div",class_="bd").find("div",class_="star").findAll("span")[3].get_text()
        datas.append({"rank":rank,"name":name,"years":years[0],"rating_num":rating_num,"comments":comments.replace("人评价","")})

    return datas

data_all =[]
for ide in range(0,250,25):
    url = f"https://movie.douban.com/top250?start={ide}&filter"
    resp = requests.get(url,headers=header)
    print("status_code:{}".format(resp.status_code))
    if(resp.status_code !=200):
        raise Exception("获取网站发生错误！")
    items =taklehtml(resp)
    for item in items:
        data_all.append(item)

#print(datas)
df = pandas.DataFrame(data_all)
print(df)
df.to_excel("top豆瓣电影.xlsx")




