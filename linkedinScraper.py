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

# TODO: i have a feeling that not being logged in provides better search results on LinkedIn due to algorithm idiocy
# and promoted jobs not respecting search terms. Make the script work logged out
# TODO: update script to look into the job description. It previously worked but needs checking and maintenance now
# TODO: try headless mode

# this is the link that the script uses for scraping, update with your own
linkedinJobLink = "https://www.linkedin.com/jobs/search/?currentJobId=4045708277&f_F=eng&f_T=9&f_WT=3%2C1&geoId=105773754&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R"

#linkedinJobLinks = "https://www.linkedin.com/jobs/search/?currentJobId=3958799969&f_F=eng%2Cit&f_TPR=r86400&f_WT=3%2C2&geoId=105773754&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R"

linkedinJobLink = "https://www.linkedin.com/jobs/search/?currentJobId=4049200552&f_C=82589639&geoId=105773754&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R"

checkTitle=0
checkDescription=1
checkBadDescription=0

goodTitles = ["c ", "c++", "embed"]
#goodTitles = ["embed"]
#goodTitles = ["unity", "unity3d", "unreal", "gam"]
#goodTitles = ["c++", "embedded", " c "]
#goodDescriptions = ["c ", "c++", "java", "python", "c#", "embedded"]
goodDescriptions = ["c++", " c "]
badDescriptions = ""
#badDescriptions = ["game", "gaming", "unity", "unity3d", "unreal", "gameplay"]

jobsPerPage = 25
botMinSpeed = 0.3
botMaxSpeed = 3
# Webdriver Elements 
totalJobs = "//small"
offersPerPage = "//li[@data-occludable-job-id]"
outputFile = open("output.txt", "w+")
logging.basicConfig(level=logging.WARNING)

headless = False
chromeProfilePath = r""

blacklistCompanies = ["luxoft", "rinf", "sii", "orion", "luxolis", "crossover", "randstad", "opentalent", "playrix", "amazon",
                      "consulting", "nagarro", "crowdstrike", "globallogic", "oasis", "techteamz", "xpert", "talent", 
                      "tlm", "kambi", "playtika", "mega image", "mpg", "avl", "von", "think-cell", "think", "smartchoice", "pentalog", "adc", "finastra"];
blacklistCompanies = "" # no blacklist for now

blackListTitles = ["manager", "lead", "architect", "design", "devops", "devsecops", "security", "cyber", "crypto", "principal", "staff", "associate", "qa", 
                  "frontend", "fullstack", "backend", "head", "machine learning", "angular", "ruby", "integrator", 
                   "react", "french", "mobile", "mac", "german", "spring", "java", "automation", "quality", "intern", "user", "sap", "administrator", 
                   "deutsch", "packaging", "erp", "oracle", "consult", "forensic"]
blackListTitles = ""    # no blacklist for now

blackListDescription = ""
#blackListDescription = ["game", "gaming", "unity", "unity3d", "unreal", "gameplay"]
#blackListDescription = ["devops", "devsecops", "cyber", "crypto", "principal", "associate", "game", "gaming", "gameplay", "java", "html", "web", "cisco", "cloud", "machine learning", "angular", "ruby", "statistical", "integrator", "animation", "sii", "node", "react", "french"]

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

def scrape():
    global outputFile
    countJobs = 0
    url = linkedinJobLink
    
    driver.get(url)
    time.sleep(random.uniform(botMinSpeed, botMaxSpeed))

    totalJobs = driver.find_element(By.XPATH,'//small').text 
    totalPages = jobsToPages(totalJobs)
    prYellow("Parsing " +str(totalJobs)+ " jobs.")

    for page in range(totalPages):
        currentPageJobs = jobsPerPage * page
        url = url +"&start="+ str(currentPageJobs)
        driver.get(url)
        time.sleep(random.uniform(botMinSpeed, botMaxSpeed))

        offersPerPage = driver.find_elements(By.XPATH, '//li[@data-occludable-job-id]')
        offerIds = [(offer.get_attribute(
            "data-occludable-job-id").split(":")[-1]) for offer in offersPerPage]
        time.sleep(random.uniform(botMinSpeed, botMaxSpeed))

        for offer in offersPerPage:
            try:
                offerId = offer.get_attribute("data-occludable-job-id")
                offerIds.append(int(offerId.split(":")[-1]))
            except Exception as e: 
                continue            

        for jobID in offerIds:
            offerPage = 'https://www.linkedin.com/jobs/view/' + str(jobID)
            driver.get(offerPage)
            time.sleep(random.uniform(botMinSpeed, botMaxSpeed))

            countJobs += 1
            prYellow("Checking job at index " + str(countJobs))

            jobProperties = getJobProperties(countJobs)
            jobDescription = getJobDescription()
            
            #first check if title and job description contain any of the goodTitles

            
            if checkTitle and not "blacklisted" in jobProperties.lower():                        
                foundGoodTitle=False
                for title in goodTitles:
                    if title in jobProperties.lower():
                        foundGoodTitle=True
                        break
                    
                if foundGoodTitle is False:
                    prYellow("No good title found in job title, skipping: " + str(offerPage))
                    continue
                        
            if checkDescription and not "blacklisted" in jobDescription.lower():
                foundGoodDesc=False
                for desc in goodDescriptions:
                    if desc in jobDescription.lower():
                        foundGoodDesc=True
                        break  
                        
                if foundGoodDesc is False:
                    prYellow("No good description found in job description, skipping: " + str(offerPage))
                    continue    
                    
            if checkBadDescription:
                foundBadDesc = False;         
                for title in badDescriptions:
                    if title in jobDescription.lower():
                        foundBadDesc = True
                        break
                        
                if foundBadDesc is True:
                    prYellow("Found bad title in jobDescription: " + title)
                    continue      
            
            if "blacklisted" in jobProperties.lower():
                prYellow("Blacklisted Job, skipped: " +str(offerPage) + " reason: " + jobProperties)
                continue
                
            if "blacklisted" in jobDescription.lower():
                prYellow("Blacklisted Job description, skipped!: " +str(offerPage) + " reason: " + jobProperties)
                continue
            
            jobAlreadySaved = False
            outputFile.seek(0, 0)
            fileContent = outputFile.read()                
            if str(jobID) in fileContent:
                jobAlreadySaved = True
                break

            if not jobAlreadySaved:
                outputFile.seek(0, 2)
                prGreen("Saved job to File: " + offerPage)
                outputFile.write(offerPage + "\n")
                outputFile.flush()
            else:
                prGreen("Job already saved: " + offerPage)

def getJobProperties(count):
    textToWrite = ""
    jobTitle = ""


    #driver.execute_script("return document.readyState") == "complete"
    
    time.sleep(botMaxSpeed) # wait for page to load
    # TODO try this: driver.execute_script("return document.readyState") == "complete"
    # or, checking for individual elements:     
    # element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'job-title')]"))

    try:
        jobTitle = driver.find_element(By.XPATH, "//*[contains(@class, 'job-title')]").get_attribute("innerHTML").strip()
        res = [blItem for blItem in blackListTitles if (blItem.lower() in jobTitle.lower())]
        if (len(res) > 0):
            jobTitle = "(blacklisted title: " + ' '.join(res) + ")"
    except Exception as e:
        prYellow("Warning in getting jobTitle: " + str(e)[0:50])
        jobTitle = ""

    try:
        jobCompanyName = driver.find_element(By.XPATH, "//*[contains(@class, 'company-name')]").get_attribute("innerHTML").strip()
        res = [blItem for blItem in blacklistCompanies if (blItem.lower() in jobCompanyName.lower())]
        if (len(res) > 0):
            jobCompanyName = "(blacklisted company: " + ' '.join(res) + ")"
    except Exception as e:
        print(e)
        prYellow("Warning in getting jobDetail: " + str(e)[0:100])
        jobCompanyName = ""

    if("blacklisted" in jobTitle):
        textToWrite = jobTitle
    elif("blacklisted" in jobCompanyName):
        textToWrite = jobCompanyName
    else:
        textToWrite = str(count) + " | " + jobTitle +" | " + jobCompanyName
    return textToWrite

def getJobDescription():
    description = " "
    try:
        description= driver.find_element(By.ID,"job-details").get_attribute("innerHTML").strip()
        if(len(blackListDescription) > 0):
            res = [blItem for blItem in blackListDescription if(blItem.lower() in description.lower())]
            if (len(res)>0):
                description += "(blacklisted description: "+ ' '.join(res)+ ")"
                print("***** Blacklisted description: "+ ' '.join(res))
    except Exception as e:
        prYellow("Warning in getting job description: " +str(e)[0:50])
        description = ""
    return description

# main
start = time.time()
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chromeBrowserOptions())
driver.get("https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin")
# uncomment these and put your own credentials
#driver.find_element("id","username").send_keys("")
#driver.find_element("id","password").send_keys("")
driver.find_element("xpath",'//button[@type="submit"]').click()       
prYellow("Please log in to LinkedIn now, and then press ENTER.")
input()    
scrape()
end = time.time()
prYellow("---Took: " + str(round((time.time() - start)/60)) + " minute(s).")
outputFile.close()