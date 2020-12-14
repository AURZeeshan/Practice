from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import urllib
import urllib.request
import time
import pandas as pd
import csv
import random
from os import name, system

# Current Working directory or root_dir
current = os.getcwd()
# image name and root_dir global var
direc =  "/ image"
global root_dir


# this ali express
# driver
browser = r'chromedriver.exe'

#  url of aliexpress
url = "https://www.aliexpress.com"
# url ="http://api.scraperapi.com?api_key=4b12245e29bfe1d452c932337876fc9e&url=https://www.aliexpress.com"
# url = "http://api.scraperapi.com?api_key=4b12245e29bfe1d452c932337876fc9e&url=https://www.aliexpress.com/wholesale?catId=0&initiative_id=SB_20201129104137&SearchText=Men+s+Fashion"
driver = webdriver.Chrome(executable_path=browser)



# Input from user 
find = input("input a category : ")

# get url
driver.get(url)
List_page_window = driver.current_window_handle





# Download Images and save in sub DIR
def download_img(url , address):
    name = random.randrange(1,1000)
    global full_name
    try:
        full_name = str(address) 
        full_name += str(name) + '.jpg'

        urllib.request.urlretrieve(url,full_name)
        print('\t Your image is downloaded and saved.')
    except:
        full_name = None




# function for directrys make two directory one root_directory and one sub directory with name category
def directry():
    global photospath
    root_dir = 'Ali express-  ' + str(find)
    os.mkdir(root_dir)
    os.chdir(root_dir)

    # change root dir to sub dir
    os.mkdir(find)
    os.chdir(find)

    sub_dir = os.getcwd()
    photospath = sub_dir + direc

# call directory function and one step back directory
directry()
os.getcwd()
os.chdir("..")
os.getcwd()







# Send Category for search 
InputField = driver.find_element_by_name('SearchText')
InputField.send_keys(find)
InputField.submit()
driver.minimize_window()
time.sleep(3)


# function for scroll of page
def Scroll():
    driver.execute_script("window.scroll(500,1500)")
    time.sleep(4)
    driver.execute_script("window.scroll(1500,2500)")
    time.sleep(4)
    driver.execute_script("window.scroll(2500,3500)")
    time.sleep(4)
    driver.execute_script("window.scroll(2500,4500)")
    time.sleep(4)
    driver.execute_script("window.scroll(4500,5200)")
    time.sleep(4)



# Scroll()
# # get Product Linkshoe
# cats = driver.find_elements_by_xpath('//*[@class="item-title"]')
driver.execute_script("window.scroll(4000,5000)")
Getpage = driver.find_elements_by_xpath('//*[@class="next-pagination-list"]/button')

for pageNo in range(len(Getpage)):
    key = 0
    print("\n\n \t Scraper Start...wait a few mint >>  PageNo : ", pageNo)
    if pageNo >= 0:
        # Empty dictionary key of dicsho
        D = {}
        Scroll()
        # # get Product Link
        cats = driver.find_elements_by_xpath('//*[@class="item-title"]')

        # Start of for loop -----------------------
        for c in cats:
            try:                      # Main try-cat
                cat = c.get_attribute('href')
                driver.execute_script("window.open('" + cat +"');")
                detail_page_window = driver.window_handles
                new_window = [x for x in detail_page_window if x != List_page_window][0]
                driver.switch_to.window(new_window)
                time.sleep(2)
                

                #driver1 = webdriver.Chrome(browser)
                #  driver.execute_script("window.open('" + my_href +"');")
                
                try:        # 1 try-title
                    Title = driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div/div/h1').text
                except:     #1 except -title
                    Title = None    
                try:       # 2 try-price
                    price = driver.find_element_by_xpath('//*[@class="product-price-current"]/span').text
                except:     # 2 except -price
                    price = None    
                try:    # 3 try-rating
                    rating = driver.find_element_by_xpath('//*[@class="product-reviewer-reviews black-link"]').text
                except:         # 3 except -rating
                    rating = None    
                
                
                try:        # 4 try-image
                    # Img = driver1.find_element_by_xpath('//*[@class="magnifier-image"]')
                    Img = driver.find_elements_by_xpath('//*[@class="images-view-item"]/img')
                    
                    for photo in Img:
                        image = photo.get_attribute('src')
                        download_img(image, photospath)
                        # print("\t {}\n {}\n {}\n {}\n {}\n ".format(Title, price, rating, full_name,cat))
                    D[key] = [Title,price,rating,full_name,cat]

                    
                    
                except:         # 4 except -image
                    image = None    
            

                

            except IndexError as e:     #except -Main
                print(e)

            
            # os.chdir(os.path.dirname(Main))
            time.sleep(2)
            key +=1 
            df = pd.DataFrame.from_dict(D,orient='index',columns=['Title','Price','rating','Image Path','Product URL']).drop_duplicates(keep=False)
            name = find + '.csv'
            if os.path.isfile(name):
                df.drop_duplicates(keep=False).to_csv(name,mode='w',header=True, index=True)
            else:
                df.drop_duplicates(keep=False).to_csv(name,mode='w', header=True,index=True)
            
            print("\t Get Detail NO {} from  ,  Page No << {} \n".format(key,pageNo))
            driver.close()
            driver.switch_to.window(List_page_window)
            

            # end of for loop-------------------------
        print("\t Completed Pages Are : ",pageNo)
        driver.execute_script("window.scroll(4000,5000)")
        time.sleep(2)
        driver.find_element_by_xpath('//*[@class="next-btn next-medium next-btn-normal next-pagination-item next-next"]').click()