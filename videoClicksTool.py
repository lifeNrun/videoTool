from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from pyvirtualdisplay import Display
import sys
import random
import threading

userAgentArray = []
proxyIps = []

def runPyvirtualdisplayBrowser(chromeOptions, intSleepTime):
  display = Display(visible=0, size=(800, 600))
  display.start()
  userAgent = 'user-agent='+ getRandomUserAgent()
  print(userAgent)
  chromeOptions.add_argument(userAgent)
  chromeOptions.add_argument('--ignore-certificate-errors')
  chromeOptions.add_argument('--ignore-ssl-errors')
  chromeOptions.add_argument('--no-sandbox')
  browser = webdriver.Chrome(chrome_options=chromeOptions)
  browser.set_window_size(800,600)
  # 访问
  browser.get(videoUrl)
  #定位到要右击的元素
  youtubeVideo = browser.find_element_by_id("player")
  #对定位到的元素执行鼠标右键操作
  ActionChains(browser).click(youtubeVideo).perform()
  timeInt = random.randint(intSleepTime - 5, intSleepTime)
  time.sleep(timeInt)
  display.stop()
  # 退出，清除浏览器缓存
  browser.quit()

def clickVideoPyvirtualdisplayMoreWindow(videoUrl, intSleepTime):
  chromeOptions = webdriver.ChromeOptions()
  num = random.randint(3, 4)
  i = 0
  chromeOptions.binary_location='/usr/bin/chromium-browser'
  threads = []
  while i < num:
    t = threading.Thread(target=runPyvirtualdisplayBrowser, args=(chromeOptions, intSleepTime))
    threads.append(t)
    i = i + 1
  for s in threads: # 开启多线程爬取
    s.start()
  for e in threads: # 等待所有线程结束
    e.join()

# 读取文档
def read(path):
    with open(path, 'r', encoding='utf-8') as f:
        txt = []
        for s in f.readlines():
            txt.append(s.strip())
    return txt

def getUserAgentArray():
  global userAgentArray
  userAgentArray = read('./data/userAgent.txt')

def getRandomUserAgent():
  global userAgentArray
  return random.choice(userAgentArray)

def clickVideosLoop(num, videoUrl, intSleepTime):
  getUserAgentArray()
  i = 0
  # print(num)
  # 3*num 4*num 5*num
  while(i < num):
    try:
      clickVideoPyvirtualdisplayMoreWindow(videoUrl, intSleepTime)
    except Exception as error:
      print(error)
    else:
      # 睡眠10s
      timeInt = random.randint(5, 10)
      time.sleep(timeInt)
      i = i + 1

if __name__ == '__main__':
  args = sys.argv
  num = int(args[1])
  intSleepTime = int(args[2])
  videoUrl = args[3]
  clickVideosLoop(num, videoUrl, intSleepTime)


