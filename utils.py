import math,constants,config,time
from typing import List

from selenium import webdriver

def chromeBrowserOptions():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-extensions")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    
    options.add_argument("--log-level=3")  
    options.add_argument("--disable-webrtc")
    options.add_argument("--disable-features=WebRTC")
    options.add_argument("--disable-features=WebRtcHideLocalIpsWithMdns")
    options.add_argument("--disable-webassembly")

    if(config.headless):
        options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    if(len(config.chromeProfilePath)>0):
        initialPath = config.chromeProfilePath[0:config.chromeProfilePath.rfind("/")]
        profileDir = config.chromeProfilePath[config.chromeProfilePath.rfind("/")+1:]
        options.add_argument('--user-data-dir=' +initialPath)
        options.add_argument("--profile-directory=" +profileDir)
    else:
        options.add_argument("--incognito")
    return options



def prRed(prt):
    print(f"\033[91m{prt}\033[00m")

def prGreen(prt):
    print(f"\033[92m{prt}\033[00m")

def prYellow(prt):
    print(f"\033[93m{prt}\033[00m")

def getUrlDataFile():
    urlData = ""
    try:
        file = open('data/urlData.txt', 'r')
        urlData = file.readlines()
    except FileNotFoundError:
        text = "FileNotFound:urlData.txt file is not found. Please run ./data folder exists and check config.py values of yours. Then run the bot again"
        prRed(text)
    return urlData

def jobsToPages(numOfJobs: str) -> int:
  number_of_pages = 1

  if (' ' in numOfJobs):
    spaceIndex = numOfJobs.index(' ')
    totalJobs = (numOfJobs[0:spaceIndex])
    totalJobs_int = int(totalJobs.replace(',', ''))
    number_of_pages = math.ceil(totalJobs_int/constants.jobsPerPage)
    if (number_of_pages > 40 ): number_of_pages = 40

  else:
      number_of_pages = int(numOfJobs)

  return number_of_pages

def urlToKeywords(url: str) -> List[str]:
    keywordUrl = url[url.index("keywords=")+9:]
    keyword = keywordUrl[0:keywordUrl.index("&") ] 
    locationUrl =  url[url.index("location=")+9:]
    location = locationUrl[0:locationUrl.index("&") ] 
    return [keyword,location]

def writeResults(text: str):
    timeStr = time.strftime("%Y%m%d")
    fileName = "Applied Jobs DATA - " +timeStr + ".txt"
    try:
        with open("data/" +fileName, encoding="utf-8" ) as file:
            lines = []
            for line in file:
                if "----" not in line:
                    lines.append(line)
                
        with open("data/" +fileName, 'w' ,encoding="utf-8") as f:
            f.write("---- Applied Jobs Data ---- created at: " +timeStr+ "\n" )
            f.write("---- Number | Job Title | Company | Location | Work Place | Posted Date | Applications | Result "   +"\n" )
            for line in lines: 
                f.write(line)
            f.write(text+ "\n")
            
    except:
        with open("data/" +fileName, 'w', encoding="utf-8") as f:
            f.write("---- Applied Jobs Data ---- created at: " +timeStr+ "\n" )
            f.write("---- Number | Job Title | Company | Location | Work Place | Posted Date | Applications | Result "   +"\n" )

            f.write(text+ "\n")

def printInfoMes(bot:str):
    prYellow("ℹ️ " +bot+ " is starting soon... ")