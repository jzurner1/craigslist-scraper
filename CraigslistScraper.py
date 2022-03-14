from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from SQLConnection import *

def printList(plist):
    for iv in plist:
        print(iv)


# --------------- VARIABLES ---------------
ownerType = "owner"
doSearch = True
searchTerm = "datsun"
doPrice = True
minPrice = "0"
maxPrice = "50000000"
doMiles = True
minMiles = "0"
maxMiles = "10000000"
doYear = True
minYear = "1900"
maxYear = "2050"
avoidWords = ["part out", "parting out", "credit", "lease", "no title"]
goodWords = ["datsun"]

# --------------- SETUP ---------------
PATH = "(PATH TO CHROME WEBDRIVER)"
driver = webdriver.Chrome(PATH)
driver.get("https://baltimore.craigslist.org/")

# Go to the vehicles page
link = driver.find_element(By.CLASS_NAME, "cta")
link.click()
resultList = driver.find_elements(By.CLASS_NAME, "result-row")  # right side as list




# --------------- PREFERENCES ---------------
if doSearch:
    search = driver.find_element(By.ID, "query")
    search.send_keys(searchTerm)
    search.send_keys(Keys.RETURN)

# owner vs dealer
if ownerType == "owner":
    purveyor = driver.find_element(By.ID, "owner-purveyor")
    ownerButton = purveyor
    ownerButton.click()
    driver.implicitly_wait(1)
elif ownerType == "dealer":
    purveyor = driver.find_element(By.ID, "purveyor")
    ownerButton = purveyor.find_element(By.XPATH, 'ul/button[3]')
    ownerButton.click()
    driver.implicitly_wait(1)
else:
    purveyor = driver.find_element(By.ID, "purveyor")
    ownerButton = purveyor.find_element(By.XPATH, 'ul/button[1]')
    ownerButton.click()
    driver.implicitly_wait(1)
resultList = driver.find_elements(By.CLASS_NAME, "result-row")


# price
if doPrice:
    priceOption = driver.find_element(By.ID, "price")
    lowPrice = priceOption.find_element(By.XPATH, "input[1]")
    lowPrice.send_keys(minPrice)
    highPrice = priceOption.find_element(By.XPATH, "input[2]")
    highPrice.send_keys(maxPrice)

# miles
if doMiles:
    searchOptions = driver.find_element(By.CLASS_NAME, "search-options")
    milesOption = searchOptions.find_element(By.XPATH, "div[7]/div[2]")
    minMile = milesOption.find_element(By.XPATH, "input[1]")
    minMile.send_keys(minMiles)
    maxMile = milesOption.find_element(By.XPATH, "input[2]")
    maxMile.send_keys(maxMiles)

# year
if doYear:
    searchOptions = driver.find_element(By.CLASS_NAME, "search-options")
    yearOption = searchOptions.find_element(By.XPATH, "div[7]/div[1]")
    minYear_ = yearOption.find_element(By.XPATH, "input[1]")
    minYear_.send_keys(minYear)
    maxYear_ = yearOption.find_element(By.XPATH, "input[2]")
    maxYear_.send_keys(maxYear)

# update search options
searchOptions = driver.find_element(By.CLASS_NAME, "search-options")  # left side
update = searchOptions.find_element(By.XPATH, "div[11]/button")
update.click()

# --------------- PRINT ---------------
resultList = driver.find_elements(By.CLASS_NAME, "result-row")
badCars = []
notBadCars = []
goodCars = []
for i in resultList:
    title = i.find_element(By.CLASS_NAME, "result-heading")
    for n in avoidWords:
        if n in title.text:
            badCars.append(i.text)
            continue
    for m in goodWords:
        if m in title.text:
            goodCars.append(i.text)
    notBadCars.append(i.text)

priceList = []
locationList = []
titleList = []
dateList = []



for n in range(len(resultList)):

    # cleans up the prices and converts them to integers. If there is any error it sets it to -1
    pl = resultList[n].text.split("\n")[0]
    if pl[0] == "$":
        pl = pl.replace(",", "")
        pl = pl[1:]
        try:
            pl = int(pl)
            priceList.append(pl)
        except:
            priceList.append(-1)
    else:
        priceList.append(-1)


    locationList.append(resultList[n].text.split("(")[1][:-1].strip())

    title = resultList[n].text.split("\n")[-1].replace("'", "").split("(")[0].split("$")[0].strip().split(" ")[2:]
    titleList.append(" ".join(title))

    date = resultList[n].text.split("\n")[-1].split("(")[0].split("$")[0].strip().split(" ")[:2]
    dateList.append(" ".join(date))



for n in range(len(priceList)):
    locationList[n] = "'" + locationList[n] + "'"
    titleList[n] = "'" + titleList[n] + "'"
    dateList[n] = "'" + dateList[n] + "'"

    addCar(titleList[n], priceList[n], -1, -1, locationList[n], "''", dateList[n])
