from selenium import webdriver
import os
import json
import requests


def create_folder(folder_name):
    if not os.path.exists("scraped-data/"+folder_name):
        os.makedirs('scraped-data/'+folder_name)

def download_image(url,image_type,counter,query):
    image = requests.get(url)
    image_name = 'scraped-data/'+query+'/'+query+'-'+str(counter)+'.'+image_type
    if image.ok:
        file = open(image_name,'wb')
        file.write(image.content)
        file.close()

#chrome driver path based on platform

DRIVER_PATH_WIN = "./chrome-driver/chromedriver-win.exe"
#DRIVER_PATH_LINUX = "./chrome-driver/chromedriver-linux"
#DRIVER_PATH_MAC = "./chrome-driver/chromedriver-mac"

browser_instance = webdriver.Chrome(executable_path=DRIVER_PATH_WIN)

print("\n\nWelcome to the google image downloader tool")
print("===========================================")

search_items = int(input("\n\nPlease input the number of unique items to search : "))

for item in range(search_items):
    counter = 0
    succounter = 0

    search_query = input("\n\nPlease input the search query "+str(item+1)+" : ")
    url = "https://www.google.co.in/search?q="+search_query+"&source=lnms&tbm=isch"

    create_folder(search_query)
    download_path = 'scraped-data/'+search_query
    browser_instance.get(url)

    for _ in range(500):
        browser_instance.execute_script("window.scrollBy(0,10000)")

    for image in browser_instance.find_elements_by_xpath('//div[contains(@class,"rg_meta")]'):
        counter = counter + 1
        print ("\n\nTotal Count:", counter)
        print ("Succsessful Count:", succounter)
        print ("URL:",json.loads(image.get_attribute('innerHTML'))["ou"])

        img = json.loads(image.get_attribute('innerHTML'))["ou"]
        imgtype = json.loads(image.get_attribute('innerHTML'))["ity"]
        try:
            download_image(img,imgtype,succounter,search_query)
            succounter = succounter + 1
        except:
                print("can't get img")

    print (succounter, "pictures succesfully downloaded")

browser_instance.close()
