from DrissionPage import ChromiumPage
from DataRecorder import Recorder
from DrissionPage._configs.chromium_options import ChromiumOptions
from DrissionPage._configs.session_options import  SessionOptions
path = r'C:\Program Files (x86)\ChatAI Chrome\ChatAI_Chrome.exe'  # 请改为你电脑内Chrome可执行文件路径

#path = r'C:\Program Files\Mozilla Firefox\firefox.exe'
ChromiumOptions().set_browser_path(path).save()



co = ChromiumOptions()
print(co.browser_path)
