import os
import time
import urllib
from selenium import webdriver
from scrapy import Selector
import requests
import warnings
warnings.filterwarnings("ignore")

class GoogleImgCrawl:
    def __init__(self,word,max_pictures,img_path):

        self.url_lists = []
        self.count = 0
        self.proxy = {"https": "https://127.0.0.1:1080"}  # 初始化代理
        # self.bf = Bloom
        self.browser = webdriver.Chrome("chromedriver.exe")
        # self.browser.maximize_window()
        self.max_pictures = max_pictures
        self.key_world = word
        self.img_path = img_path
        if not os.path.exists(self.img_path):
            os.makedirs(self.img_path)

    def start_crawl(self):
        self.browser.get('https://www.google.com/search?q=%s' % self.key_world)
        self.browser.implicitly_wait(2)
        #self.browser.find_element_by_xpath('//a[@class="iu-card-header"]').click()
        self.browser.find_element_by_xpath('//a[contains(text(),"图片")]').click()  # 找到图片的链接点击进去.匹配一个属性值中包含的字符串。
                                                                                       #text()匹配的是显示文本信息，此处也可以用来做定位
                                                                                       #//a[contains(text(),"百度搜索")]匹配a标签中，显示的文本信息中，包含“百度搜索”的文本

        time.sleep(1)
        img_source = self.browser.page_source

        img_source = Selector(text=img_source)

        # self.img_down(img_source)  # 第一次下载图片
        self.slide_down()  # 向下滑动继续加载图片


    def slide_down(self):
        # for i in range(1,1):
        i = 0
        countt = 0
        while True:

            print(i)
            # pos = i * 800
            # js = "document.documentElement.scrollTop=%s" % pos
            # self.browser.execute_script(js)
            # for j in range(7):
            #     print(j)
            #     time.sleep(2)
            self.browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(2)
            # print(self.browser.find_element_by_xpath('//input[@value="显示更多结果")]'))
            img_source = Selector(text=self.browser.page_source)
            # datas = img_source.xpath("//*[@id='smb']")
            try:
                self.browser.find_element_by_xpath(".//*[@id='smbw']/input").click()
            except:
                print("未找到显示更多结果按钮")




            try:
                self.img_down(img_source)
            except BaseException as e:
                print("BaseException:",e)

            if self.count == countt and count_flag ==10:
                break
            elif self.count == countt:
                count_flag+=1
            else:
                countt = self.count
                count_flag = 0

            if self.count > self.max_pictures:
                break
            i += 1
            if i>100:
                break




    def img_down(self,img_source):
        #img_url_list = img_source.xpath('//div[@class="THL2l"]/../img/@src').extract()
        img_url_list = img_source.xpath('//a[@jsname="hSRGPd"]/@href').extract()
        # print("#########img_source.xpath###########")
        # print(img_source.xpath('//a[@jsname="hSRGPd"]/@href'))
        # print(img_url_list)

        for each_url in img_url_list:
            if "#" not in each_url:

                each_url = "https://www.google.com"+each_url
                if each_url in self.url_lists:
                    # print("已经下载过：",each_url)
                    pass
                else:

                    self.url_lists.append(each_url)
                    try:
                        response = requests.get(each_url, proxies=self.proxy, verify=False, timeout=1)  # 请求大图的网址
                    except BaseException as e:
                        print(e)
                    else:
                        img_info = Selector(text=response.content)

                        img_url = img_info.xpath('//div[@id="il_ic"]/img/@src').extract_first()  # 获取图片的网址

                        # print("##############div[id=il_ic]##############")
                        # print(img_info.xpath('//div[@id="il_ic"]/img/@src'))
                        # print(img_url)
                        try:
                            response = requests.get(img_url, proxies=self.proxy, verify=False, timeout=1)
                        except BaseException as e:
                            print(e)
                        else:
                            self.count += 1
                            print(self.count)
                            print('正在下载:',img_url)
                            with open('%s/%s.jpg' % (self.img_path, time.time()), 'wb')as f:
                                f.write(response.content)

def download(keyword,image_number,localPath):

    google_crawl = GoogleImgCrawl(keyword, image_number, localPath)
    google_crawl.start_crawl()

def main():
    aa = [800,300,100,300,200,300,200,100,800,300,200,300,300]

    # download(keyword="恐怖分子", image_number=aa[8], localPath="d:/img2/terrorist/")

if __name__ == '__main__':
    main()


