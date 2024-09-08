from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import time

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors")
chrome_options.add_argument("--disable-web-security")
driver_path = "E:/chromdriver/chromedriver.exe"  # 你的chromedriver位置
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://www.kaoshibao.com/login"
driver.get(url)
input("登陆按下回车\n")
id = 'YOUR EXAM ID'

# 下一题按钮class <button>
XPATH_id_btn = '//button[@class="el-button el-button--primary el-button--small"]'
XPATH_id_ques = '//div[@class="qusetion-box"]'  # 题目class <div>
topic_type = "topic-type"  # 题目类型 <span>
options = 'option'  # 选项 <span>
# 正确选项 <span>
options_t = '//div[@class="option right"]/span[@class="before-icon"]'
options_duo = '//div[@class="option right right3"]'  # 多个正确选项 <span>
ai_answer = '//p[@class="answer-analysis"]'  # AI解析 <p>
beiti_btn = "/html/body/div[3]/div/div/section/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/p[2]/span[2]/div/span"
pic_xpath = '//img[@class="fr-fic fr-dib"]'
pic_xpath2 = '//img[@class="fr-fic fr-dib fr-fil"]'
ques_pic = '//img[@class="cursor-hover"]'


driver.get("https://www.kaoshibao.com/online/?paperId="+id)
driver.find_element(By.XPATH, beiti_btn).click()
input("准备完成|按下回车开始\n")


next = driver.find_elements(By.XPATH, XPATH_id_btn)
timer = 0
num = 0


with open("./data.txt", 'w', encoding="utf-8") as f:
    while next != []:
        timer += 1
        num += 1
        # frame=['类型',"题目","选项","答案","解析"]
        ques = driver.find_element(By.XPATH, XPATH_id_ques).text.strip()
        opts = driver.find_elements(By.CLASS_NAME, options)
        _topic_type = driver.find_element(By.CLASS_NAME, topic_type).text
        try:
            ques_p = driver.find_element(
                By.XPATH, ques_pic).get_attribute("src")
            if ques_p:
                ques += " "+ques_p
        except:
            pass

        opt = []
        for i in opts:
            a = i.text[1:].strip()
            if a != '':
                opt.append({i.text[0]: a})
            else:
                pic = driver.find_elements(By.XPATH, pic_xpath)
                if pic:
                    for i in range(len(opts)):
                        opt.append(
                            {opts[i].text[0]: pic[i].get_attribute('src')})
                else:
                    pic = driver.find_elements(By.XPATH, pic_xpath2)
                    if pic:
                        for i in range(len(opts)):
                            opt.append(
                                {opts[i].text[0]: pic[i].get_attribute('src')})
                break
        try:
            answer = driver.find_element(By.XPATH, options_t).text
        except:
            answer = driver.find_elements(By.XPATH, options_duo)
            if answer:
                t = ''
                for i in answer:
                    t += i.text[0]+' '
                answer = t
        try:
            jiexi = driver.find_element(By.XPATH, ai_answer).text
        except:
            jiexi = '暂无解析'
        frame = {"序号": num, "类型": _topic_type, "题目": ques,
                 "选项": opt, "答案": answer, "解析": jiexi}
        f.write(str(frame)+"\n")
        next[0].click()
        time.sleep(0.3)
        next = driver.find_elements(By.XPATH, XPATH_id_btn)
        if timer >= 50:
            timer = 0
            time.sleep(0.5)
    timer += 1
    num += 1
    # frame=['类型',"题目","选项","答案","解析"]
    ques = driver.find_element(By.XPATH, XPATH_id_ques).text.strip()
    opts = driver.find_elements(By.CLASS_NAME, options)
    _topic_type = driver.find_element(By.CLASS_NAME, topic_type).text
    try:
        ques_p = driver.find_element(By.XPATH, ques_pic).get_attribute("src")
        if ques_p:
            ques += " "+ques_p
    except:
        pass
    opt = []
    for i in opts:
        a = i.text[1:].strip()
        if a != '':
            opt.append({i.text[0]: a})
        else:
            pic = driver.find_elements(By.XPATH, pic_xpath)
            if pic:
                for i in range(len(opts)):
                    opt.append({opts[i].text[0]: pic[i].get_attribute('src')})
            else:
                pic = driver.find_elements(By.XPATH, pic_xpath2)
                if pic:
                    for i in range(len(opts)):
                        opt.append(
                            {opts[i].text[0]: pic[i].get_attribute('src')})
            break
    try:
        answer = driver.find_element(By.XPATH, options_t).text
    except:
        answer = driver.find_elements(By.XPATH, options_duo)
        if answer:
            t = ''
            for i in answer:
                t += i.text[0]+' '
            answer = t
    try:
        jiexi = driver.find_element(By.XPATH, ai_answer).text
    except:
        jiexi = '暂无解析'
    frame = {"序号": num, "类型": _topic_type, "题目": ques,
             "选项": opt, "答案": answer, "解析": jiexi}
    f.write(str(frame)+"\n")
    
    next[0].click()
    time.sleep(0.3)
    next = driver.find_elements(By.XPATH, XPATH_id_btn)
    if timer >= 50:
        timer = 0
        time.sleep(0.5)
f.close()
