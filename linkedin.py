import time,math,random,os
import utils,constants,config
import pickle, hashlib

import logging

from selenium import webdriver
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

from selenium.common.exceptions import *

DEBUG = True

linkedinJobLinks = ["https://www.linkedin.com/jobs/search/?currentJobId=4012159218&f_WT=3%2C1&geoId=105773754&keywords=c%2B%2B&location=Bucharest%2C%20Romania&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true"]

timeframe=2
java=1
toate=1
outputFile = open("output_apply.txt", "w")
logging.basicConfig(level=logging.WARNING)

def log(s):
    if DEBUG:
        print(s)
        
# TODO: i have a feeling that not being logged in provides better search results on LinkedIn due to algorithm idiocy 
# and promoted jobs not respecting search terms. Make the script work logged out
        
class Linkedin:
    def __init__(self):
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=utils.chromeBrowserOptions())
            self.driver.get("https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin")
            
            utils.prYellow("Please log in to LinkedIn now, and then press ENTER.")
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

        urlData = utils.getUrlDataFile()

        for url in linkedinJobLinks:        
            self.driver.get(url)
            time.sleep(random.uniform(1, constants.botSpeed))

            totalJobs = self.driver.find_element(By.XPATH,'//small').text 
            totalPages = utils.jobsToPages(totalJobs)

            urlWords =  utils.urlToKeywords(url)
            urlWords = ["none", "none"]
            lineToWrite = "\n Category: " + urlWords[0] + ", Location: " +urlWords[1] + ", Applying " +str(totalJobs)+ " jobs."
            self.displayWriteResults(lineToWrite)

            for page in range(totalPages):
                currentPageJobs = constants.jobsPerPage * page
                url = url +"&start="+ str(currentPageJobs)
                self.driver.get(url)
                time.sleep(random.uniform(1, constants.botSpeed))

                offersPerPage = self.driver.find_elements(By.XPATH, '//li[@data-occludable-job-id]')
                offerIds = [(offer.get_attribute(
                    "data-occludable-job-id").split(":")[-1]) for offer in offersPerPage]
                time.sleep(random.uniform(1, constants.botSpeed))

                for offer in offersPerPage:
                    try:
                       offerId = offer.get_attribute("data-occludable-job-id")
                       offerIds.append(int(offerId.split(":")[-1]))
                    except Exception as e: 
                        continue                    
                        
                for jobID in offerIds:
                    offerPage = 'https://www.linkedin.com/jobs/view/' + str(jobID)
                    self.driver.get(offerPage)
                    time.sleep(random.uniform(1, constants.botSpeed))

                    countJobs += 1

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
                    
                    if checkTitle:
                        foundGoodTitle=False
                        for title in goodTitles:
                            if title in jobProperties.lower():
                                foundGoodTitle=True
                                break;   
                            
                        if foundGoodTitle is False:
                                lineToWrite = "No good title found in job title, skipping: " + jobProperties
                                self.displayWriteResults(lineToWrite)
                                continue;   
                                
                    if checkDescription:  
                        foundGoodDesc=False
                        for desc in goodDescriptions:
                            if desc in jobDescription.lower():
                                foundGoodDesc=True
                                break;  
                                
                        if foundGoodDesc is False:
                                lineToWrite = "No good description found in job description, skipping: "
                                self.displayWriteResults(lineToWrite)
                                continue;      
                            
                    if checkBadDescription:
                        foundBadDesc = False;         
                        for title in badDescriptions:
                            if title in jobDescription.lower():
                                foundBadDesc = True
                                break;
                                
                        if foundBadDesc is True:
                            lineToWrite = "Found bad title in jobDescription: " + title
                            self.displayWriteResults(lineToWrite)
                            continue;       
                 
                    if "blacklisted" in jobProperties.lower():
                        lineToWrite = jobProperties + " | " + "* Blacklisted Job, skipped!: " +str(offerPage)
                        self.displayWriteResults(lineToWrite)
                        continue
                        
                    if "blacklisted" in jobDescription.lower():
                        lineToWrite = jobProperties + " | " + "* Blacklisted Job Description, skipped!: " +str(offerPage)
                        self.displayWriteResults(lineToWrite)
                        continue
                                                             
                    utils.prYellow("Saved job to File: " + offerPage + "\n")
                    outputFile.write(offerPage + "\n")
                    outputFile.flush()
 
                    lineToWrite = jobProperties + " | " + "* Saved job to " + str(outputFile) + ". " +str(offerPage)
                    self.displayWriteResults(lineToWrite)
                    
            utils.prYellow("Category: " + urlWords[0] + "," +urlWords[1]+ " applied: " + str(countApplied) +
                  " jobs out of " + str(countJobs) + ".")

    def getJobProperties(self, count):
        textToWrite = ""
        jobTitle = ""
        jobLocation = ""

        try:
            jobTitle = self.driver.find_element(By.XPATH, "//div[contains(@class, 'job-title')]").get_attribute("innerHTML").strip()
            res = [blItem for blItem in config.blackListTitles if (blItem.lower() in jobTitle.lower())]
            if (len(res) > 0):
                jobTitle += "(blacklisted title: " + ' '.join(res) + ")"
        except Exception as e:
            if (config.displayWarnings):
                utils.prYellow("Warning in getting jobTitle: " + str(e)[0:50])
            jobTitle = ""

        try:
            #time.sleep(5)
            jobDetail = self.driver.find_element(By.XPATH, "//div[contains(@class, 'job-details-jobs')]//div").text.replace("·", "|")
            res = [blItem for blItem in config.blacklistCompanies if (blItem.lower() in jobTitle.lower())]
            if (len(res) > 0):
                jobDetail += "(blacklisted company: " + ' '.join(res) + ")"
        except Exception as e:
            if (config.displayWarnings):
                print(e)
                utils.prYellow("Warning in getting jobDetail: " + str(e)[0:100])
            jobDetail = ""

        try:
            jobWorkStatusSpans = self.driver.find_elements(By.XPATH, "//span[contains(@class,'ui-label ui-label--accent-3 text-body-small')]//span[contains(@aria-hidden,'true')]")
            for span in jobWorkStatusSpans:
                jobLocation = jobLocation + " | " + span.text

        except Exception as e:
            if (config.displayWarnings):
                print(e)
                utils.prYellow("Warning in getting jobLocation: " + str(e)[0:100])
            jobLocation = ""

        textToWrite = str(count) + " | " + jobTitle +" | " + jobDetail + jobLocation
        return textToWrite

    def getJobDescription(self):
        description = " "
        try:
            description= self.driver.find_element(By.ID,"job-details").get_attribute("innerHTML").strip()
            if(len(config.blackListDescription) > 0):
                res = [blItem for blItem in config.blackListDescription if(blItem.lower() in description.lower())]
                if (len(res)>0):
                    description += "(blacklisted description: "+ ' '.join(res)+ ")"
                    print("***** Blacklisted description: "+ ' '.join(res))
        except Exception as e:
            if(config.displayWarnings):
                prYellow("Warning in getting job description: " +str(e)[0:50])
            description = ""

        return description


    def easyApplyButton(self):
        try:
            time.sleep(random.uniform(1, constants.botSpeed))
            button = self.driver.find_element(By.XPATH, "//div[contains(@class,'jobs-apply-button--top-card')]//button[contains(@class, 'jobs-apply-button')]")
            EasyApplyButton = button
        except: 
            EasyApplyButton = False

        return EasyApplyButton

    def applyProcess(self, percentage, offerPage):
        applyPages = math.floor(100 / percentage) - 2 
        result = ""
        for pages in range(applyPages):  
            self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Continue to next step']").click()

        self.driver.find_element( By.CSS_SELECTOR, "button[aria-label='Review your application']").click()
        time.sleep(random.uniform(1, constants.botSpeed))

        if config.followCompanies is False:
            try:
                self.driver.find_element(By.CSS_SELECTOR, "label[for='follow-company-checkbox']").click()
            except:
                pass

        self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Submit application']").click()
        time.sleep(random.uniform(1, constants.botSpeed))

        result = "* Just Applied to this job: " + str(offerPage)

        return result
        
    def saveOfferToFile(self, percentage, offerPage):
        applyPages = math.floor(100 / percentage) - 2 
        result = ""
        for pages in range(applyPages):  
            self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Continue to next step']").click()

        self.driver.find_element( By.CSS_SELECTOR, "button[aria-label='Review your application']").click()
        time.sleep(random.uniform(1, constants.botSpeed))

        if config.followCompanies is False:
            try:
                self.driver.find_element(By.CSS_SELECTOR, "label[for='follow-company-checkbox']").click()
            except:
                pass

        self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Submit application']").click()
        time.sleep(random.uniform(1, constants.botSpeed))

        result = "* Just Applied to this job: " + str(offerPage)

        return result        

    def displayWriteResults(self,lineToWrite: str):
        try:
            print(lineToWrite)
            utils.writeResults(lineToWrite)
        except Exception as e:
            utils.prRed("Error in DisplayWriteResults: " +str(e))

    def element_exists(self, parent, by, selector):
        return len(parent.find_elements(by, selector)) > 0

start = time.time()
Linkedin().linkJobApply()
end = time.time()
utils.prYellow("---Took: " + str(round((time.time() - start)/60)) + " minute(s).")
outputFile.close()
