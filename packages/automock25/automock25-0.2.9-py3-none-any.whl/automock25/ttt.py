from DrissionPage import ChromiumPage
from DataRecorder import Recorder
from DrissionPage._configs.chromium_options import ChromiumOptions
from DrissionPage._configs.session_options import  SessionOptions
path = r'C:\Program Files (x86)\ChatAI Chrome\ChatAI_Chrome.exe'  # 请改为你电脑内Chrome可执行文件路径

#path = r'C:\Program Files\Mozilla Firefox\firefox.exe'
ChromiumOptions().set_browser_path(path).save()



# 创建页面对象
page = ChromiumPage()

# 访问网页
page.get('https://www.maoyan.com/board/4')

while True:
    # 遍历页面上所有 dd 元素
    for mov in page.eles('t:dd'):
        # 获取需要的信息
        num = mov('t:i').text
        score = mov('.score').text
        title = mov('@data-act=boarditem-click').attr('title')
        star = mov('.star').text
        time = mov('.releasetime').text
        # 写入到记录器
         # recorder.add_data((num, title, star, time, score))
        print(num, score, title, star, time)

    # 获取下一页按钮，有就点击
    btn = page('下一页', timeout=10)
    if btn:
        btn.click()
        page.wait.load_start()
    # 没有则退出程序
    else:
        break

