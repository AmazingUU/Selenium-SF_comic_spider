import os

import requests
from selenium import webdriver

def get_proxy():
    return requests.get('http://127.0.0.1:5010/get/').content

def delete_proxy(proxy):
    requests.get('http://127.0.0.1:5010/delete/?proxy={}'.format(proxy))

def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def save_pic(url,filename):
    retry_count = 5
    proxy = get_proxy()
    print(proxy.decode('utf-8'))
    while retry_count > 0:
        try:
            r = requests.get(url,proxies={'http':'http://{}'.format(proxy.decode('utf-8'))},timeout=3)
            r.raise_for_status()
            pic = r.content
            with open(filename,'wb') as f:
                f.write(pic)
        except Exception as e:
            print(str(e))
            retry_count -= 1
    delete_proxy(proxy)

def get_chapter(url):
    brower = webdriver.PhantomJS('F:\Selenium\phantomjs-2.1.1\phantomjs-2.1.1-windows\\bin\phantomjs.exe')
    brower.get(url)
    brower.implicitly_wait(3)
    name = brower.find_element_by_xpath('/html/body/div[2]/h1').text
    base_dir = os.getcwd()
    comic_dir = base_dir + '\\' + name
    mkdir(comic_dir)
    a_list = brower.find_elements_by_xpath('/html/body/div[3]/div[1]/div[3]/div/a')
    # print(a_list)
    chapter_dirs = []
    chapter_urls = []
    for a in a_list:
        chapter = a.text
        chapter_dir = comic_dir + '\\' + chapter
        mkdir(chapter_dir)
        chapter_dirs.append(chapter_dir)
        link = a.get_attribute('href')
        chapter_urls.append(link)
    return chapter_urls,chapter_dirs


        # brower.get(link)
        # brower.implicitly_wait(3)
        # page_num = brower.find_element_by_xpath('//*[@id="TotalPage"]').text
        # for i in range(1,int(page_num) - 1):
        #     img_url = brower.find_element_by_xpath('//*[@id="curPic"]').get_attribute('src')
        #     save_pic(img_url,chapter_dir + '\\' + str(i) + '.png')
        #     next_page = brower.find_element_by_xpath('//*[@id="AD_j1"]/div/a[4]')
        #     next_page.click()

def get_content(urls,chapter_dirs):
    brower = webdriver.PhantomJS('F:\Selenium\phantomjs-2.1.1\phantomjs-2.1.1-windows\\bin\phantomjs.exe')
    for i in range(len(urls)):
        brower.get(urls[i])
        brower.implicitly_wait(3)
        page_num = brower.find_element_by_xpath('//*[@id="TotalPage"]').text
        for j in range(1,int(page_num) - 1):
            img_url = brower.find_element_by_xpath('//*[@id="curPic"]').get_attribute('src')
            save_pic(img_url,chapter_dirs[i] + '\\' + str(j) + '.png')
            next_page = brower.find_element_by_xpath('//*[@id="AD_j1"]/div/a[4]')
            next_page.click()

if __name__ == '__main__':
    chapter_urls,chapter_dirs = get_chapter('https://manhua.sfacg.com/mh/WLZWD/')
    get_content(chapter_urls,chapter_dirs)
