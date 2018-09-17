# coding=utf-8
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait  
from time import sleep  
import os
import codecs


class Uploader:
    def __init__(self):
        self.stars_set = set()

    def __del__(self):
        self.driver.close()

    #option = webdriver.ChromeOptions()
    #option.add_argument('--start-fullscreen')
    #driver = webdriver.Chrome(executable_path='chromedriver.exe', options=option)
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    driver.set_window_size(1280, 1000) 
    driver.implicitly_wait(15)

    # 根据验证框的存在与否判断是否要输入验证码  
    def isVerifyCodeExist(self):  
        try:  # 如果成功找到验证码输入框返回true  
            self.driver.find_element_by_css_selector('input[name="verifycode"]')  
            return True  
        except:  # 如果异常返回false  
            return False  
  
    # 输入验证码部分，如果无需输入则直接返回，否则手动输入成功后返回          
    def inputVerifyCode(self):  
        input_verifycode = self.driver.find_element_by_css_selector('input[name="verifycode"]')  # 验证码输入框  
        bt_change = self.driver.find_element_by_css_selector('img[action-type="btn_change_verifycode"]')  # 验证码图片，点击切换  
        bt_logoin = self.driver.find_element_by_class_name('login_btn')  # 登录按钮  
        while self.isVerifyCodeExist():  
            print(u'请输入验证码……(输入"c"切换验证码图片)')  
            verifycode = input()  
            if verifycode == 'c':  
                bt_change.click()  
            else:  
                input_verifycode.send_keys(verifycode)  
                bt_logoin.click()  
                # 点击完登录以后判断是否成功  
                if self.driver.current_url.split('/')[-1] == 'home':  
                    print(u'登录成功')  
                    break  
                else:  
                    print(u'输入的验证码不正确')  
  
    # 打开微博首页进行登录的过程  
    def login(self, account, password):
        # 设置隐性等待时间，等待页面加载完成才会进行下一步，最多等待10秒
        url = 'https://weibo.com/login'
        chrome = self.driver
        self.driver.get(url)  
        # 输入账号密码并登录  
        WebDriverWait(self.driver, 5).until(lambda x: x.find_element_by_id('loginname')).send_keys(account)  
        self.driver.find_element_by_css_selector('input[type="password"]').send_keys(password)  
  
        bt_logoin = self.driver.find_element_by_class_name('login_btn')  
        bt_logoin.click()  
  
        # 如果存在验证码，则进入手动输入验证码过程
        if self.isVerifyCodeExist():
            self.inputVerifyCode()
        
        if "我的收藏" in chrome.page_source:
            #print("登录成功！")
            return True
        else:
            #print("登录失败！")
            return False
    def jump_month_rank(self):
        next_link = self.driver.find_element_by_class_name('next_link')
        next_link.click()
        #跳转到当月榜
        next_link.click()

    def click_calendar(self):
        #点击选择日历图标
        month_rank = self.driver.find_element_by_class_name('month_rank')
        if month_rank != None:
            #print(month_rank)
            data_link = month_rank.find_elements_by_tag_name('a')
            for link in data_link:
                link.click()
                
    def jump_rigth_rank(self, name):
        div = self.driver.find_element_by_class_name(name)
        if div != None:
            link = div.find_element_by_tag_name('a')
            if link != None:
                link.click()

    def get(self, url, name):
        #print('get', url)
        self.driver.get(url)

        #跳转到月排行榜
        self.jump_month_rank()
        #点击日历控件
        self.click_calendar()

        month_list = self.get_month_list()
        for month in month_list:
            print('rank:', name)
            self.goto_month(month)
            #print(month)
            self.process_month_star_ranks()
            #重新加载内地榜页面
            self.jump_rigth_rank(name)
            #sleep(5)
            #跳转到月排行榜
            self.jump_month_rank()
            #sleep(5)
            #点击日历控件
            self.click_calendar()

        '''
        #选择月份
        detail_month = self.driver.find_element_by_class_name('detail_month')
        if detail_month != None:
            links = detail_month.find_elements_by_tag_name('a')
            for link in links:
                print(link.get_attribute("text"))
                #if link.get_attribute("text") == '1月':
                #self.driver.implicitly_wait(10)
                #self.process_month_star_ranks()
                link.click()

        print('star ranks=', self.stars_set)

        #下一页
        changePages = self.driver.find_element_by_class_name('changePages')
        if changePages != None:
            links = changePages.find_elements_by_tag_name('a')
            for link in links:
                #print(link.get_attribute("text"))
                if link.get_attribute("text") == '2':
                    link.click()
                    break
        
        star_total_ranks = self.driver.find_elements_by_class_name('S_func1')
        for rank in star_total_ranks:
            links = rank.find_elements_by_tag_name('a')
            for link in links:
                print(link.get_attribute("text"))
        '''
    def save_stars_to_file(self, file_name):
        f = codecs.open(file_name, 'w', 'utf-8')
        for it in self.stars_set:
            #print(it)
            f.write(it + '\n')
        
        f.close()

    def jump_page_top(self):
        #js = "var q=document.getElementById('id').scrollTop=0"
        js = "var q=document.body.scrollTop=1"
        self.driver.execute_script(js) 

    def click_month_rank(self):
        month_rank = self.driver.find_element_by_class_name('month_rank')
        if month_rank != None:
            #print(month_rank)
            data_link = month_rank.find_elements_by_tag_name('a')
            for link in data_link:
                link.click()

    def goto_month(self, month):
        detail_month = self.driver.find_element_by_class_name('detail_month')
        if detail_month != None:
            links = detail_month.find_elements_by_tag_name('a')
            for link in links:
                #print(link.get_attribute("text"))
                if month == link.get_attribute("text"):
                    link.click()
                    
    def get_month_list(self):
        detail_month = self.driver.find_element_by_class_name('detail_month')
        s = []
        if detail_month != None:
            links = detail_month.find_elements_by_tag_name('a')
            for link in links:
                s.append(link.get_attribute("text"))
        return s

    def process_month_star_ranks(self):
        #抓取第一页排行榜
        self.get_stars()
        self.next_page()
        
        #抓取第二页排行榜
        self.get_stars()

    def next_page(self):
        #下一页
        changePages = self.driver.find_element_by_class_name('changePages')
        if changePages != None:
            links = changePages.find_elements_by_tag_name('a')
            for link in links:
                #print(link.get_attribute("text"))
                if link.get_attribute("text") == '2':
                    link.click()
                    break

    def get_stars(self):
        sleep(5)
        star_total_ranks = self.driver.find_elements_by_class_name('S_func1')
        for rank in star_total_ranks:
            links = rank.find_elements_by_tag_name('a')
            for link in links:
                print(link.get_attribute("text"))
                name = link.get_attribute("text")
                name = name.strip()
                self.stars_set.add(name)
    # 上传文字  
    def upload_txt(self, text):  
        input_w = self.driver.find_element_by_xpath('//div[@node-type="textElDiv"]/textarea[@class="W_input"]')  
        input_w.send_keys(text)  
        sleep(1)  
  
    # 运行上传图片脚步  
    def upload_img_script(self, time_bef, time_after, path):  # path参数需要前后带双引号  
        sleep(time_bef)  # 等待弹窗时间  
        os.system('C:/img/upload.exe ' + path)  
        sleep(time_after)  # 等待图片加载时间  
  
    # 上传文字和单图  
    def upload_txt_img(self, text, img_path):  
        self.upload_txt(text)  # 将文字上传  
        img = self.driver.find_element_by_css_selector('a[action-type="multiimage"]')  # 图片按钮  
        img.click()  # 点击图片按钮  
        sleep(1)  # 等待加载其他按钮  
  
        self.upload_img_script(1, 2, img_path)  
  
    # 上传文字和多图      
    def upload_txt_multiImg(self, text, img_path_list):  
        self.upload_txt_img(text, img_path_list[0])  # 将文字和第一张图片上传  
  
        len_imgs = len(img_path_list)  # 图片地址list的长度  
        bt_uploadimg = WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_xpath('//li[@node-type="uploadBtn"]/div'))  
        for i in range(len_imgs - 1):  # 将剩余图片上传  
            bt_uploadimg.click()  
            self.upload_img_script(1, 2, img_path_list[i + 1])  
  
    # 发布  
    def send(self):  
        self.driver.find_element_by_class_name('W_btn_a').click()  
        sleep(4)  # 等待发送成功字样消失  
  

if __name__ == "__main__":
    # 登录  
    uploader = Uploader()
    username = ''
    password = ''

    # 填写你的账号密码
    succ = uploader.login(username, password)
    if succ:
        print('login succ|username=%s'%(username))
    else:
        print('login failed|username=%s'%(username))

    #内地排行榜
    uploader.get('http://chart.weibo.com/chart?rank_type=5&version=v1', 'Korea')
    #港澳排行榜
    uploader.get('http://club.starvip.weibo.com/demo?rank_type=3&version=v1', 'macao')
    #新星
    #uploader.get('http://club.starvip.weibo.com/demo?rank_type=6&version=v1', 'smalrig')
    uploader.save_stars_to_file('明星.txt')

    '''
    count_img = 2;#自动获取图片多少张  
    text = "okokokokposfdfsdafsadfsadgsadfgsfgkjsfdajgkl;sajklgjsakgjsakljdgklsadjgkls;salkgjk"#填入你的内容  
    path_list = []  # 图片地址list  
    
    for i in range(count_img):  # 根据图片总数量生成所有图片地址  
        m = i+1  
        path_list.append('C:\\img\\'+str(m)+'.jpg')  
    # 上传内容  
    if count_img == 0:  # 没有图片  
        uploader.upload_txt(text)  
    elif count_img == 1:  # 单张图片  
        uploader.upload_txt_img(text, path_list[0])  
    else:  # 多张图片  
        uploader.upload_txt_multiImg(text, path_list)  
    
    uploader.send()
    '''