# General bot settings to use Pro settings you need to download Pro version from: www.automated-bots.com

browser = ["Chrome"]
headless = False

# get Chrome profile path by typing following url: chrome://version/
chromeProfilePath = r""

# These settings are for running Linkedin job apply bot.
# location you want to search the jobs - ex : ["Poland", "Singapore", "New York City Metropolitan Area", "Monroe County"]
# continent locations:["Europe", "Asia", "Australia", "NorthAmerica", "SouthAmerica", "Africa", "Australia"]
location = "Bucharest, Romania"
# keywords related with your job search
keywords = ["c++", "developer", "engineer", "c"]	#job experience Level - ex:  ["Internship", "Entry level" , "Associate" , "Mid-Senior level" , "Director" , "Executive"]
experienceLevels = [ "Internship", "Entry level" , "Associate" , "Mid-Senior level" ]
#job posted date - ex: ["Any Time", "Past Month" , "Past Week" , "Past 24 hours"] - select only one
datePosted = ["Any Time"]
#job type - ex:  ["Full-time", "Part-time" , "Contract" , "Temporary", "Volunteer", "Intership", "Other"]
jobType = ["Full-time"]
#remote  - ex: ["On-site" , "Remote" , "Hybrid"]
remote = ["Remote" , "Hybrid"]
salary = [ "$80,000+"]
#sort - ex:["Recent"] or ["Relevent"] - select only one
sort = ["Recent"]
#Blacklist companies you dont want to apply - ex: ["Apple","Google"]
blacklistCompanies = ""
#blacklistCompanies = ["alten", "orion", "luxoft", "nxp"]
blacklistCompanies = ["luxoft", "rinf", "sii", "orion", "luxolis", "crossover", "randstad", "opentalent", "playrix", "amazon",
                      "consulting", "nagarro", "crowdstrike", "globallogic", "oasis", "techteamz", "xpert", "talent", 
                      "tlm", "kambi", "playtika", "mega image", "mpg", "avl", "von", "think-cell", "think", "smartchoice"];
#Blaclist keywords in title - ex:["manager", ".Net"]
blackListTitles = ""
blackListTitles = ["manager", "lead", "architect", "design", "devops", "devsecops", "security", "cyber", "crypto", "principal", "staff", "associate", "qa", 
                   "frontend", "fullstack", "backend", "web", "cisco", "reliability", "head", "machine learning", "angular", "ruby", "integrator", 
                   "angular", "react", "french", "mobile", "mac", "german", "spring", "java"]
blackListDescription = ""
#blackListDescription = ["game", "gaming", "unity", "unity3d", "unreal", "gameplay"]
#blackListDescription = ["devops", "devsecops", "cyber", "crypto", "principal", "associate", "game", "gaming", "gameplay", "java", "html", "web", "cisco", "cloud", "machine learning", "angular", "ruby", "statistical", "integrator", "animation", "sii", "node", "react", "french"]
#Follow companies after sucessfull application True - yes, False - no
followCompanies = False
#Below settings are for linkedin bot Pro, you can purchase monthly or yearly subscription to use them from me.

 # Testing & Debugging features
displayWarnings = True