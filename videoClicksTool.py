from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from pyvirtualdisplay import Display
import sys
import random
import threading
import json
userAgentArray = []
proxyIps = []
userAgentGlobal = {}
userAgentGlobal['userAgents'] = []
userAgentGlobal['usedIndexs'] = []

def readInfo(fileName):
    try:
        document = open(fileName, 'r', encoding='utf-8')
    except IOError:
        print('open %s error'% fileName)
        return {}
    else:
        data = document.read()
        document.close()
        if(data == ""):
            return {}
        else:
            return json.loads(data)

def getNewUserAgent():
  global userAgentGlobal
  userAgents = readInfo('./data/userAgentNew.json')
  userAgentGlobal['userAgents'] = userAgents

def getRandomUserAgentNew():
  global userAgentGlobal
  index = 0
  length = len(userAgentGlobal['userAgents'])
  mobile_emulation = {}
  while(index < length):
    index = random.randint(0, length-1)
    if(index not in userAgentGlobal['usedIndexs']):
      item = userAgentGlobal['userAgents'][index]
      mobile_emulation['deviceMetrics'] = item['deviceMetrics']
      mobile_emulation['userAgent'] = item['userAgent']
      userAgentGlobal['usedIndexs'].append(index)
      return mobile_emulation

def mobileEmulationBrowseNoDisPlay(chrome_options, intSleepTime, url):
  mobile_emulation = getRandomUserAgentNew()
  width = mobile_emulation['deviceMetrics']['width']
  height = mobile_emulation['deviceMetrics']['height']
  display = Display(visible=0, size=(width, height))
  display.start()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
  driver = webdriver.Chrome(chrome_options=chrome_options)
  driver.set_window_size(width, height)
  driver.get(url)
  try:
    youtubeVideo = driver.find_element_by_css_selector('ytm-compact-video-renderer.item:first-child')
  except Exception as error:
    print(error)
    driver.get(url)
    # 对特别版本的android
    youtubeVideo = driver.find_element_by_css_selector("div.cib[data-index='0']>div>div>a")

  ActionChains(driver).click(youtubeVideo).perform()
  # timeInt = random.randint(intSleepTime - 5, intSleepTime)
  time.sleep(intSleepTime)
  display.stop()
  driver.quit()

def searchAndClickVideo(chromeOptions, intSleepTime, url):
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
  # 查看本机ip，查看代理是否起作用
  browser.get(url)
  #定位到要单击的元素
  try:
    youtubeVideo = browser.find_element_by_css_selector('ytm-compact-video-renderer.item:first-child')
  except Exception as error:
    print(error)
    browser.get(url)
    # 对特别版本的android
    youtubeVideo = browser.find_element_by_css_selector("div.cib[data-index='0']>div>div>a")

  ActionChains(browser).click(youtubeVideo).perform()
  timeInt = random.randint(intSleepTime - 5, intSleepTime)
  time.sleep(timeInt)
  display.stop()
  # 退出，清除浏览器缓存
  browser.quit()

def runPyvirtualdisplayBrowser(chromeOptions, intSleepTime, videoUrl):
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
  # timeInt = random.randint(intSleepTime - 5, intSleepTime)
  time.sleep(intSleepTime)
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
    t = threading.Thread(target=searchAndClickVideo, args=(chromeOptions, intSleepTime, videoUrl))
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
  userAgentArray = read('./data/EssenceUserAgent.txt')

def getRandomUserAgent():
  global userAgentArray
  return random.choice(userAgentArray)

def clickVideosLoopThread(num, videoUrl, intSleepTime):
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
      timeInt = random.randint(110, 120)
      time.sleep(timeInt)
      i = i + 1
def clickVideosLoop(num, videoUrl, intSleepTime):
  # getUserAgentArray()
  getNewUserAgent()
  i = 0
  chromeOptions = webdriver.ChromeOptions()
  chromeOptions.binary_location='/usr/bin/chromium-browser'
  while(i < num):
    try:
      mobileEmulationBrowseNoDisPlay(chromeOptions, intSleepTime, videoUrl)
    except Exception as error:
      print(error)
    else:
      # 睡眠10s
      timeInt = random.randint(15, 20)
      time.sleep(timeInt)
      i = i + 1

if __name__ == '__main__':
  args = sys.argv
  num = int(args[1])
  intSleepTime = int(args[2])
  videoUrl = args[3]
  clickVideosLoop(num, videoUrl, intSleepTime)
