import os
import time
import urllib
from selenium import webdriver
from scrapy import Selector
import requests

class GoogleImgCrawl:
    def __init__(self):
        self.proxy = {"https": "https://127.0.0.1:1080","http": "http://127.0.0.1:1080"}  # 初始化代理
        self.browser = webdriver.Chrome("chromedriver.exe")
        self.browser.maximize_window()
        self.key_world = "手"
        self.img_path = r"D:/img2"
        if not os.path.exists(self.img_path):
            os.makedirs(self.img_path)

    def start_crawl(self):
        self.browser.get('HTTP://www.google.com/search?q=%s' % self.key_world)
        self.browser.implicitly_wait(2)
        self.browser.find_element_by_xpath('//a[@class="iu-card-header"]').click()
        time.sleep(1)
        img_source = self.browser.page_source
        img_source = Selector(text=img_source)
        self.img_down(img_source)  # 第一次下载图片
        self.slide_down()   #向下滑动继续加载图片


    def img_down(self,img_source):
        img_url_list = img_source.xpath('//div[@class="THL2l"]/../img/@src').extract()
        for each_url in img_url_list:
            print("each_url:",each_url)
            if "https" not in each_url:
                print("each_url:", each_url)
                each_img_source = urllib.request.urlretrieve(each_url,'%s/%s.jpg' % (self.img_path, time.time()))
            else:

                response = requests.get(each_url, proxies=self.proxy, verify=False)
                with open('D:/img2\%s.jpg' % time.time(), 'wb')as f:
                    f.write(response.content)


    def slide_down(self):
        for i in range(1,2):
            pos = i * 500
            js = "document.documentElement.scrollTop=%s" % pos
            self.browser.execute_script(js)
            time.sleep(1)
            img_source = Selector(text=self.browser.page_source)
            self.img_down(img_source)


if __name__ == '__main__':
    google_crawl = GoogleImgCrawl()
    google_crawl.start_crawl()


