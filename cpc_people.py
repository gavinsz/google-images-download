# coding=utf-8
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep  
import os
import codecs
import logging
from utils import download_img

logging.basicConfig(filename='logger.log', 
                    format='%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s', 
                    level = logging.INFO,
                    filemode='a',
                    datefmt='%Y-%m-%d %I:%M:%S %p')

class Uploader:
    def __init__(self):
        self.stars_set = set()
        self.img_count = 0
        self.img_set = set()

    def __del__(self):
        self.driver.close()

    def get_img_count(self):
        return self.img_count

    #chromeOptions = webdriver.ChromeOptions()
    #chromeOptions.add_argument('--proxy-server=http://127.0.0.1:12345')   
    #driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chromeOptions)
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    driver.set_window_size(1280, 1000) 
    
    driver.implicitly_wait(15)

    def get_all_provinces(self):
        provinces = dict()
        p4_con = self.driver.find_element_by_class_name('p4_con')
        if p4_con is None:
            return provinces

        fl = p4_con.find_element_by_class_name('fl')
        if fl:
            ul = fl.find_element_by_tag_name('ul')
            if ul:
                li_list = fl.find_elements_by_tag_name('li')
                for li in li_list:
                    link = li.find_element_by_tag_name('a')
                    if link:
                        href = link.get_attribute('href')
                        province_name = link.get_attribute('text')
                        if href != None and province_name != None:
                            provinces[province_name] = href
        
        return provinces

    def get(self, url, out_dir, layer_name):
        self.driver.get(url)

        #wait = WebDriverWait(self.driver, 60)
        #element = wait.until(EC.element_to_be_clickable((By.ID, 'copyright')))

        if 'top' == layer_name:
            p_tabs = self.driver.find_elements_by_class_name('p_tab')
            print('len(p_tabs)=', len(p_tabs))
            for i, p_tab in enumerate(p_tabs):
                '''
                if i == 10:
                    print(i, 'p_tab text=', p_tab.text)
                    self.process_p_tab(p_tab, out_dir)
                '''
                self.process_p_tab(p_tab, out_dir)

        if 'local' == layer_name:
            provinces = self.get_all_provinces()
            for k,v in provinces.items():
                self.process_providece_html(out_dir, k, v)
                print('province=%s|url=%s'%(k, v))


    def process_providece_html(self, out_dir, name, url):
        self.driver.get(url)
        p4_con = self.driver.find_element_by_class_name('p4_con')
        if p4_con:
            fr = p4_con.find_element_by_class_name('fr')
            if fr:
                box01 = fr.find_element_by_class_name('box01')
                if box01 == None:
                    return

                dls = box01.find_elements_by_class_name('clearfix')
                for dl in dls:
                    person_name = ''
                    img_src = None
                    links = dl.find_elements_by_tag_name('a')
                    for link in links:
                        imgs = dl.find_elements_by_tag_name('img')
                        for img in imgs:
                            img_src = img.get_attribute('src')
                            self.img_set.add(img_src)
                            self.img_count += 1
                        
                        if person_name == '':
                            person_name = link.get_attribute('text')
                        #print(person_name)

                    #if person_name != '' and img_src != '':
                    if img_src != '':
                        download_img(out_dir, person_name, img_src)
                    
                    if img_src != '' and person_name == '':
                        logging.error('no person name for img|img_url=%s'%(img_src))

                    '''
                    img = dl.find_element_by_tag_name('img')
                    if img:
                        img_src = img.get_attribute('src')

                    strong = dl.find_element_by_tag_name('strong')
                    if strong:
                        link = strong.find_element_by_tag_name('a')
                        if link:
                            person_name = link.get_attribute('text')
                    '''

    def process_p_tab(self, p_tab, out_dir):
        tds = p_tab.find_elements_by_tag_name('td')
        for td in tds:
            
            person_name, img_url = self.get_person_and_img(td)
            if img_url is not None:
                print('name=%s img_url=%s'%(person_name, img_url))
                self.img_set.add(img_url)
                if person_name != None and person_name != '':
                    download_img(out_dir, person_name, img_url)
                else:
                    logging.error('name=%s|img_url=%s'%(person_name, img_url))

            '''
            imgs = td.find_elements_by_tag_name('img')
            if len(imgs) == 0:
                continue

            img = td.find_element_by_tag_name('img')
            if img:
                img_src = img.get_attribute('src')
                print('img_src=%s'%(img_src))
            
            ps = td.find_elements_by_tag_name('p')
            for p in ps:
                links = p.find_elements_by_tag_name('a')
                if len(links) == 0:
                    name = p.text
                    if name == '':
                        name = p.get_attribute('text')
                else:
                    link = p.find_element_by_tag_name('a')
                    if link:
                        name = link.get_attribute('text')
                
                print('name=%s'%(name))
            '''

    def get_person_and_img(self, td):
        imgs = td.find_elements_by_tag_name('img')
        if len(imgs) == 0:
            return None, None

        img = td.find_element_by_tag_name('img')
        if img:
            img_src = img.get_attribute('src')
            #print('img_src=%s'%(img_src))
        
        person_name = self.get_person_name(td)
        
        return person_name, img_src

    def get_person_name(self, td):
        #print('td get_attribute(text)=%s text=%s'%(td.get_attribute('text'), td.text))
        #print('td text=', td.text)
        name = ''

        ps = td.find_elements_by_tag_name('p')
        for p in ps:
            #print('p=', p.get_attribute('innerHTML'))
            links = p.find_elements_by_tag_name('a')
            if len(links) == 0:
                name = p.text
                if name == '':
                    name = p.get_attribute('text')
                
                if name == None:
                    name = p.get_attribute('innerHTML')
            else:
                link = p.find_element_by_tag_name('a')
                if link:
                    if name == '':
                        name = link.get_attribute('text')
            #print('name=%s'%(name))

        if name != None:
            #name = name.replace('<br>', '')
            pos = name.find('<br>')
            if -1 != pos:
                name = name[pos+len('<br>'):]
            
            pos = name.find(':')
            if pos != -1:
                name = name[pos+1:]

            pos = name.find('：')
            if pos != -1:
                name = name[pos+1:]
            name = name.strip()

        return name

    def get_all_tabs(self):
        nav_div = self.driver.find_element_by_class_name('nav')
        if nav_div:
            ul = nav_div.find_element_by_tag_name('ul')
            if ul:
                tabs = ul.find_elements_by_tag_name('li')
                return tabs
        else:
            return None

    def save_stars_to_file(self, file_name):
        f = codecs.open(file_name, 'w', 'utf-8')
        for it in self.stars_set:
            #print(it)
            f.write(it + '\n')
        
        f.close()


if __name__ == "__main__":
    os.environ["http_proxy"] = 'http://web-proxy.tencent.com:8080'
    os.environ["https_proxy"] = 'http://web-proxy.tencent.com:8080'
    uploader = Uploader()
    out_dir = 'E:\workspace\\ai\\google-images-download-master\\cpc_images'
    #中央政要资料库
    uploader.get('http://cpc.people.com.cn/GB/64162/394696/index.html', out_dir, 'top')
    
    #out_dir = 'E:\workspace\\ai\\google-images-download-master\\local_government_images'
    #地方政府人物资料库
    #uploader.get('http://ldzl.people.com.cn/dfzlk/front/personProvince1.htm', out_dir, 'local')
    print('img count=', uploader.get_img_count())
    print('img_set count=', len(uploader.img_set))
    #uploader.save_stars_to_file('politicians.txt')