import time,math,random,os
import pickle, hashlib
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *
from typing import List

jobsPerPage = 25
faster = 1
fast = 2
medium = 3
slow = 5 
botSpeed = fast
# Webdriver Elements 
totalJobs = "//small"
offersPerPage = "//li[@data-occludable-job-id]"
linkedinJobLinks = ["https://www.linkedin.com/jobs/search/?currentJobId=4012159218&f_WT=3%2C1&geoId=105773754&keywords=c%2B%2B&location=Bucharest%2C%20Romania&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true"]
timeframe=2
java=1
toate=1
outputFile = open("output_apply.txt", "r+")
logging.basicConfig(level=logging.WARNING)

browser = ["Chrome"]
headless = False
chromeProfilePath = r""
location = "Bucharest, Romania"
keywords = ["c++", "developer", "engineer", "c"]
experienceLevels = [ "Internship", "Entry level" , "Associate" , "Mid-Senior level" ]
datePosted = ["Any Time"]
jobType = ["Full-time"]
remote = ["Remote" , "Hybrid"]
salary = [ "$80,000+"]
sort = ["Recent"]
blacklistCompanies = ""
blacklistCompanies = ["luxoft", "rinf", "sii", "orion", "luxolis", "crossover", "randstad", "opentalent", "playrix", "amazon",
                      "consulting", "nagarro", "crowdstrike", "globallogic", "oasis", "techteamz", "xpert", "talent", 
                      "tlm", "kambi", "playtika", "mega image", "mpg", "avl", "von", "think-cell", "think", "smartchoice"];
blackListTitles = ""
blackListTitles = ["manager", "lead", "architect", "design", "devops", "devsecops", "security", "cyber", "crypto", "principal", "staff", "associate", "qa", 
                   "frontend", "fullstack", "backend", "web", "cisco", "reliability", "head", "machine learning", "angular", "ruby", "integrator", 
                   "angular", "react", "french", "mobile", "mac", "german", "spring", "java"]
blackListDescription = ""
#blackListDescription = ["game", "gaming", "unity", "unity3d", "unreal", "gameplay"]
#blackListDescription = ["devops", "devsecops", "cyber", "crypto", "principal", "associate", "game", "gaming", "gameplay", "java", "html", "web", "cisco", "cloud", "machine learning", "angular", "ruby", "statistical", "integrator", "animation", "sii", "node", "react", "french"]

# TODO: i have a feeling that not being logged in provides better search results on LinkedIn due to algorithm idiocy 
# and promoted jobs not respecting search terms. Make the script work logged out

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
            
def jobsToPages(numOfJobs: str) -> int:
  number_of_pages = 1

  if (' ' in numOfJobs):
    spaceIndex = numOfJobs.index(' ')
    totalJobs = (numOfJobs[0:spaceIndex])
    totalJobs_int = int(totalJobs.replace(',', ''))
    number_of_pages = math.ceil(totalJobs_int/jobsPerPage)
    if (number_of_pages > 40 ): number_of_pages = 40

  else:
      number_of_pages = int(numOfJobs)

  return number_of_pages

def getUrlDataFile():
    urlData = ""
    try:
        file = open('data/urlData.txt', 'r')
        urlData = file.readlines()
    except FileNotFoundError:
        text = "FileNotFound:urlData.txt file is not found"
        prRed(text)
    return urlData

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

    if(headless):
        options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    if(len(chromeProfilePath)>0):
        initialPath = chromeProfilePath[0:chromeProfilePath.rfind("/")]
        profileDir = chromeProfilePath[chromeProfilePath.rfind("/")+1:]
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

class Linkedin:
    def __init__(self):
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chromeBrowserOptions())
            self.driver.get("https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin")
            
            # uncomment these and put your own credentials
            #self.driver.find_element("id","username").send_keys("")
            #self.driver.find_element("id","password").send_keys("")    
            self.driver.find_element("xpath",'//button[@type="submit"]').click()
                  
            prYellow("Please log in to LinkedIn now, and then press ENTER.")
            input()
            
            # start application
            self.linkJobApply()

    def getHash(self, string):
        return hashlib.md5(string.encode('utf-8')).hexdigest()
  
    def isLoggedIn(self):
        self.driver.get('https://www.linkedin.com/feed')
        try:
            self.driver.find_element(By.XPATH,'//*[@id="ember14"]')
            return True
        except:
            pass
        return False 
    
    def generateUrls(self):
        global time,java, outputFile, linkedinJobLinks
        

    def linkJobApply(self):
        global timeframe,java, outputFile
        
        self.generateUrls()
        countApplied = 0
        countJobs = 0

        urlData = getUrlDataFile()

        for url in linkedinJobLinks:        
            self.driver.get(url)
            time.sleep(random.uniform(1, botSpeed))

            totalJobs = self.driver.find_element(By.XPATH,'//small').text 
            totalPages = jobsToPages(totalJobs)

            urlWords =  urlToKeywords(url)
            urlWords = ["none", "none"]
            lineToWrite = "\n Category: " + urlWords[0] + ", Location: " +urlWords[1] + ", Applying " +str(totalJobs)+ " jobs."
            self.displayWriteResults(lineToWrite)

            for page in range(totalPages):
                currentPageJobs = jobsPerPage * page
                url = url +"&start="+ str(currentPageJobs)
                self.driver.get(url)
                time.sleep(random.uniform(1, botSpeed))

                offersPerPage = self.driver.find_elements(By.XPATH, '//li[@data-occludable-job-id]')
                offerIds = [(offer.get_attribute(
                    "data-occludable-job-id").split(":")[-1]) for offer in offersPerPage]
                time.sleep(random.uniform(1, botSpeed))

                for offer in offersPerPage:
                    try:
                       offerId = offer.get_attribute("data-occludable-job-id")
                       offerIds.append(int(offerId.split(":")[-1]))
                    except Exception as e: 
                        continue            

                for jobID in offerIds:
                    offerPage = 'https://www.linkedin.com/jobs/view/' + str(jobID)
                    self.driver.get(offerPage)
                    time.sleep(random.uniform(1, botSpeed))

                    countJobs += 1
                    prYellow("Checking job at index " + str(countJobs))

                    jobProperties = self.getJobProperties(countJobs)
                    
                    jobDescription = self.getJobDescription()
                    
                    #first check if title and job description contain any of the goodTitles
                    goodTitles = [" c ", "c++", "java", "python", "c#", "embedded"]
                    goodDescriptions = ["c ", "c++", "java", "python", "c#", "embedded"]
                    
                    goodTitles = ["c++", "embedded", " c "]
                    goodDescriptions = ["c++", " c "]
                    badDescriptions = ["game", "gaming", "unity", "unity3d", "unreal", "gameplay"]
                    
                    checkTitle=1
                    checkDescription=0
                    checkBadDescription=0
                    
                    if checkTitle and not "blacklisted" in jobProperties.lower():                        
                        foundGoodTitle=False
                        for title in goodTitles:
                            if title in jobProperties.lower():
                                foundGoodTitle=True
                                break
                            
                        if foundGoodTitle is False:
                                lineToWrite = "No good title found in job title, skipping: " + str(offerPage)
                                self.displayWriteResults(lineToWrite)
                                continue
                                
                    if checkDescription and not "blacklisted" in jobDescription.lower():
                        foundGoodDesc=False
                        for desc in goodDescriptions:
                            if desc in jobDescription.lower():
                                foundGoodDesc=True
                                break  
                                
                        if foundGoodDesc is False:
                                lineToWrite = "No good description found in job description, skipping: " + str(offerPage)
                                self.displayWriteResults(lineToWrite)
                                continue    
                            
                    if checkBadDescription:
                        foundBadDesc = False;         
                        for title in badDescriptions:
                            if title in jobDescription.lower():
                                foundBadDesc = True
                                break
                                
                        if foundBadDesc is True:
                            lineToWrite = "Found bad title in jobDescription: " + title
                            self.displayWriteResults(lineToWrite)
                            continue      
                 
                    if "blacklisted" in jobProperties.lower():
                        lineToWrite = "Blacklisted Job, skipped: " +str(offerPage) + " reason: " + jobProperties
                        self.displayWriteResults(lineToWrite)
                        continue
                        
                    if "blacklisted" in jobDescription.lower():
                        lineToWrite = "Blacklisted Job description, skipped!: " +str(offerPage) + " reason: " + jobProperties
                        self.displayWriteResults(lineToWrite)
                        continue
                    
                    jobAlreadySaved = False
                    fileContent = outputFile.read()                
                    if str(jobID) in fileContent:
                        jobAlreadySaved = True
                        break
     
                    if not jobAlreadySaved:
                        prGreen("Saved job to File: " + offerPage)
                        outputFile.write(offerPage + "\n")
                        outputFile.flush()
                    else:
                        prGreen("Job already saved: " + offerPage)
                     
            prYellow("Category: " + urlWords[0] + "," +urlWords[1]+ " applied: " + str(countApplied) +
                  " jobs out of " + str(countJobs) + ".")

    def getJobProperties(self, count):
        textToWrite = ""
        jobTitle = ""
        jobLocation = ""
        
        time.sleep(5) # wait for page to load

        try:
            jobTitle = self.driver.find_element(By.XPATH, "//*[contains(@class, 'job-title')]").get_attribute("innerHTML").strip()
            res = [blItem for blItem in blackListTitles if (blItem.lower() in jobTitle.lower())]
            if (len(res) > 0):
                jobTitle = "(blacklisted title: " + ' '.join(res) + ")"
        except Exception as e:
            prYellow("Warning in getting jobTitle: " + str(e)[0:50])
            jobTitle = ""

        try:
            jobCompanyName = self.driver.find_element(By.XPATH, "//*[contains(@class, 'company-name')]").get_attribute("innerHTML").strip()
            res = [blItem for blItem in blacklistCompanies if (blItem.lower() in jobCompanyName.lower())]
            if (len(res) > 0):
                jobCompanyName = "(blacklisted company: " + ' '.join(res) + ")"
        except Exception as e:
            print(e)
            prYellow("Warning in getting jobDetail: " + str(e)[0:100])
            jobCompanyName = ""

        try:
            jobWorkStatusSpans = self.driver.find_elements(By.XPATH, "//span[contains(@class,'ui-label ui-label--accent-3 text-body-small')]//span[contains(@aria-hidden,'true')]")
            for span in jobWorkStatusSpans:
                jobLocation = jobLocation + " | " + span.text

        except Exception as e:
            print(e)
            prYellow("Warning in getting jobLocation: " + str(e)[0:100])
            jobLocation = ""

        if("blacklisted" in jobTitle):
            textToWrite = jobTitle
        elif("blacklisted" in jobCompanyName):
            textToWrite = jobCompanyName
        else:
            textToWrite = str(count) + " | " + jobTitle +" | " + jobCompanyName + jobLocation
        return textToWrite

    def getJobDescription(self):
        description = " "
        try:
            description= self.driver.find_element(By.ID,"job-details").get_attribute("innerHTML").strip()
            if(len(blackListDescription) > 0):
                res = [blItem for blItem in blackListDescription if(blItem.lower() in description.lower())]
                if (len(res)>0):
                    description += "(blacklisted description: "+ ' '.join(res)+ ")"
                    print("***** Blacklisted description: "+ ' '.join(res))
        except Exception as e:
            prYellow("Warning in getting job description: " +str(e)[0:50])
            description = ""
        return description
        
    def displayWriteResults(self,lineToWrite: str):
        try:
            print(lineToWrite)
            writeResults(lineToWrite)
        except Exception as e:
            prRed("Error in DisplayWriteResults: " +str(e))

    def element_exists(self, parent, by, selector):
        return len(parent.find_elements(by, selector)) > 0

start = time.time()
Linkedin().linkJobApply()
end = time.time()
prYellow("---Took: " + str(round((time.time() - start)/60)) + " minute(s).")
outputFile.close()