import os
import urllib
import requests
import re
import cv2
from scipy import misc
from os.path import join

def getPage(keyword,page,n):
    page=page*n
    keyword=urllib.parse.quote(keyword, safe='/')
    url_begin= "http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word="
    url = url_begin+ keyword + "&pn=" +str(page) + "&gsm="+str(hex(page))+"&ct=&ic=0&lm=-1&width=0&height=0"
    return url

def get_onepage_urls(onepageurl):
    try:
        html = requests.get(onepageurl).text
        # print(html)
    except Exception as e:
        print(e)
        pic_urls = []
        return pic_urls
    pic_urls = re.findall('"objURL":"(.*?)",', html, re.S)
    return pic_urls

def down_pic(pic_urls,localPath):
    """给出图片链接列表,下载所有图片"""
    i = 1
    for pic_url in pic_urls:

        string = localPath + str(i + 1) + '.jpg'
        while os.path.exists(string):
            i += 1
            string = localPath + str(i + 1) + '.jpg'
        try:
            pic = requests.get(pic_url, timeout=3)

            with open(string, 'wb') as f:
                f.write(pic.content)
                print('成功下载第%s张图片: %s' % (str(i + 1), str(pic_url)))
        except Exception as e:
            print('下载第%s张图片时失败: %s' % (str(i + 1), str(pic_url)))
            print(e)
            continue


def download(keyword ,image_number,localPath):

    if not os.path.exists(localPath):
        os.makedirs(localPath)
        print("创建文件成功")
    #keyword = '宿舍'  # 关键词, 改为你想输入的词即可, 相当于在百度图片里搜索一样
    page_begin = 0
    page_number = 30
    #image_number = 14
    all_pic_urls = []
    while 1:
        if page_begin > image_number:
            break
        print("第%d次请求数据", [page_begin])
        url = getPage(keyword, page_begin, page_number)
        print(url)
        onepage_urls = get_onepage_urls(url)
        print(onepage_urls)
        page_begin += 1

        all_pic_urls.extend(onepage_urls)
    down_pic(list(set(all_pic_urls)),localPath)

def main():

    # download(keyword="恐怖", image_number=10, localPath="d:/img1/horrible1/")
    # download(keyword="血腥", image_number=6, localPath="d:/img1/bloody/")
    # download(keyword="吓人", image_number=3, localPath="d:/img1/fearful/")
    # download(keyword="鬼片", image_number=3, localPath="d:/img1/ghost1/")
    # download(keyword="丧尸", image_number=4, localPath="d:/img1/ghost2/")
    # download(keyword="木乃伊", image_number=14, localPath="d:/img1/mummy/")
    # download(keyword="恐怖片", image_number=2, localPath="d:/img1/horrible2/")
    # download(keyword="惊悚", image_number=2, localPath="d:/img1/frightened/")
    download(keyword="恐怖分子", image_number=15, localPath="d:/img1/terrorist/")
    download(keyword="打架", image_number=8, localPath="d:/img1/fight/fight1/")
    download(keyword="斗殴", image_number=5, localPath="d:/img1/fight/fight2/")
    download(keyword="群架", image_number=3, localPath="d:/img1/fight/fight3/")
    download(keyword="恶心", image_number=8, localPath="d:/img1/awful/")


def main1():
    dir_name = "D:\img\sports/volleyball"
    localPath = "D:/img/sport"
    i = 1
    img_list= []
    for j in os.listdir(dir_name):
        img_name = join(dir_name,j)
        string = os.path.join(localPath , str(i + 1) + '.jpg')
        while os.path.exists(string):
            i += 1
            string = os.path.join(localPath , str(i + 1) + '.jpg')

        img = misc.imread(img_name,mode="RGB")

        misc.imsave(string,img)
        img_list.append(string)
        print(img_name,string)
def main2():
    dir_names = "D:\img/sports"
    img_list= []
    for i in os.listdir(dir_names):
        dir_name = join(dir_names,i)
        for j in os.listdir(dir_name):
            img_name = join(dir_name,j)

            try:
                misc.imread(img_name, mode="RGB")
                print(img_name)
            except:
                img_list.append(img_name)
    print("img_list",img_list)

if __name__ == '__main__':
    # localPath = "d:/img/bedroom/"
    main()




