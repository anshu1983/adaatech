from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException
import os
import sys
import time
import random
import csv
import subprocess

root = os.path.dirname(__file__)

def read_file(filename):
    try:
        with open(filename) as reader:
            data = reader.read().splitlines()

        return data

    except Exception as ex:
        print('Read file function: ',ex)
        sys.exit()

def save_link(link):
    with open('New Product Link.csv', mode='a' , newline='',encoding='utf-8') as csv_details:
        csv_writer = csv.writer(csv_details, quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([link])

def run_bat():
    try:
        path = root + '\CurlAFADiscord.bat'
     
        subprocess.call([r''+path+''])
    except Exception as ex:
        print('Run bat',ex)



def save_bat(link):
   
    pat =  '{\\"username\\":\\"Adaa\\", \\"content\\": \\"'+link+'\\"}'
    bat = """@echo off
    rem ...
    set errorlevel=
    D:\Curl\\bin\curl.exe -X POST -H "Content-Type: application/json" -d "{}" "https://discord.com/api/webhooks/758719012304715807/71co5w7Njb0Fvw0ntmuzL7YKiaPjPxuavw56HgQ83HpyD5BwonR49xsWBAdaL8etPQJq"
    D:\Downloads\\sound1.wav
    IF %errorlevel% ==0 GOTO SUCCESS
    IF %errorlevel% ==1 GOTO ERROR

    :SUCCESS
    echo Success!
    GOTO END

    :ERROR
    echo Error!
    GOTO END

    :END

    """.format(pat)

    myBat = open(r'CurlAFADiscord.bat','w+')

    myBat.write(bat)
    myBat.close()


def check_price(driver,link,our_price):
    try:
        driver.execute_script("window.open(arguments[0],'_blank');",link)
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[1])
        found = False
        count = 0
        while True:
            if count>1:
                break

            if driver.find_elements_by_css_selector('span#priceblock_dealprice'):
                price = driver.find_element_by_css_selector('span#priceblock_dealprice').text
                price = price.replace('£','').replace(' ','').replace('\n','')
                p  = price
                if '-' in p:
                    p = p.split('-')
                    price = min(float(p[0]),float(p[1]))
                
                else:    
                    price = float(price)
                    print(':> Deal price',price)
                if price > our_price:
                    print(price)
                    found = True
                break

            elif driver.find_elements_by_css_selector('span#priceblock_ourprice'):
                price = driver.find_element_by_css_selector('span#priceblock_ourprice').text
                price = price.replace('£','').replace(' ','').replace('\n','')
                p  = price
                if '-' in p:
                    p = p.split('-')
                    price = min(float(p[0]),float(p[1]))
                   
                else:
                    price = float(price)
                    print('our price',price)
                if price > our_price:
                    print(price)
                    found = True
                break

            elif driver.find_elements_by_id('price_inside_buybox'):
                price = driver.find_element_by_id('price_inside_buybox').text
                price = price.replace('£','').replace(' ','').replace('\n','')
                p  = price
                if '-' in p:
                    
                    p = p.split('-')
                    price = min(float(p[0]),float(p[1]))
                   

                else:
                    price = float(price)
                    print('inside deal box price',price)
                if price > our_price:
                    print(price)
                    found = True
                    
                break

            elif driver.find_elements_by_id('buyNewSection'):
                price = driver.find_element_by_id('buyNewSection').text
                price = price.replace('£','').replace(' ','').replace('\n','')
                p  = price
                if '-' in p:
                    p = p.split('-')
                    price = min(float(p[0]),float(p[1]))
                   

                else:
                    price = float(price)
                    print('inside deal box price',price)
                if price > our_price:
                    print(price)
                    found = True
                    
                break

            else:
                print('Price is lower')
                time.sleep(1)
                count = count + 1


    except Exception as ex:
        print(':> Check price:', ex)
    try:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except:
        pass
    return found


def request_product(driver):
    url = driver.current_url
    req_btn_count  = 0
    while True:
        if req_btn_count > 8:
            driver.execute_script("window.scrollTo(0,0);")
            break
        if driver.find_elements_by_id('vvp-product-details-modal--request-btn'):
            #Request Product
            try:
                btn = driver.find_element_by_id('vvp-product-details-modal--request-btn')
                if 'disable' in btn.get_attribute('class'):
                    break

                else:
                    #Check if btn displayed or not
                    c = 0
                    while True:
                        if c>8:
                            break
                        if btn.is_displayed():
                            try:
                                driver.execute_script('document.getElementById("vvp-product-details-modal--request-btn").click()')
                            except:
                                pass
                            time.sleep(1)
                            break
                        else:
                            c = c+1
                            time.sleep(1)
            except:
                pass

            #Click on Send to this address
            send_btn_count = 0
            while True:
                if send_btn_count >2:
                    driver.execute_script("window.scrollTo(0,0);")
                    break
                if driver.find_elements_by_id('vvp-shipping-address-modal--submit-btn'):
                    try:                       
                        #driver.find_element_by_id('vvp-shipping-address-modal--submit-btn').click()
                        #Check if btn displayed or not
                        btn = driver.find_element_by_id('vvp-shipping-address-modal--submit-btn')
                        x = 0
                        while True:
                            if x>3:
                                break
                            if btn.is_displayed():
                                try:
                              
                                    driver.execute_script('document.getElementById("vvp-shipping-address-modal--submit-btn").click()')
                                    print('Item Ordered')
                                except:
                                    pass
                                break
                            else:
                                x = x+1
                                time.sleep(1)
                        
                        time.sleep(1)
                        try:
                            #driver.execute_script("window.scrollTo(0,0);")
                            driver.get(url)
                        except:
                            pass
                        break
                    except:
                        pass
                else:
                    print('No Submit button')
                    time.sleep(1)
                    send_btn_count = send_btn_count + 1
            break
        else:
            print('No request btn found')
            time.sleep(1)
            req_btn_count = req_btn_count + 1



def get_products(driver,url,delay,filters,filt,our_price):

    try:
        
        driver.get(url)
        time.sleep(1)
        

        #Getting links of all the available product
        old_products = []
        new_products = []

        while True:
            try:
                products = []
                if driver.find_elements_by_css_selector('div.vvp-item-tile-content > div.vvp-item-product-title-container > a'):
                    #get product link
                    pl =  driver.find_elements_by_css_selector('div.vvp-item-tile-content > div.vvp-item-product-title-container > a')

                    #des
                    #desc = driver.execute_script("return document.querySelectorAll('div.vvp-item-product-title-container > a > span > span.a-truncate-full.a-offscreen')")
                    
                    #See details button
                    see_btn = driver.find_elements_by_css_selector('input.a-button-input')
                    
                    
                    
                    for i in range(len(pl)):
                        status= False
                        link = pl[i].get_attribute('href')
                        products.append(link)


                        #product descriptiom)
                        try:
                            des = driver.execute_script("return a = document.querySelectorAll('div.vvp-item-product-title-container > a > span > span.a-truncate-full.a-offscreen')[arguments[0]].innerText",i)
                            des = " " + des
                        except:
                            driver.refresh()
                            time.sleep(1)

                            try:
                                des = driver.execute_script("return document.querySelectorAll('div.vvp-item-product-title-container > a > span > span.a-truncate-full.a-offscreen')[arguments[0]].innerText",i)
                                des = " " + des
                            except:
                                pass
                        #print(link)
                        #print('des',des)
                        #print('\n')

                        #Check if new product link found or not
                        if len(old_products)>0:
                              
                            if link not in old_products and link not in new_products:
                                new_products.append(link)
                                print('New link -',link)
                                print(des)
                                save_bat(link)
                                time.sleep(1)
                                run_bat()
                                #print(filt)
                                #print(len(filt))
                                #If product link has specific kwd then buy
                                if len(filt)>0:
                                    #print('Descrption matching')
                                    count = 0
                                    for kwd in filt:
                                        #print(des.lower())
                                        #print(kwd)
                                        if kwd.lower() in des.lower():
                                            try:
                                                try:
                                                    driver.execute_script("document.querySelectorAll('input.a-button-input')[arguments[0]].click()", str(i))
                                                except Exception as ex:
                                                    print(ex)
                                                    
                                                time.sleep(1)
                                            
                                            except Exception as ex:
                                                print(ex)

                                            #Request product
                                            request_product(driver)
                                            time.sleep(1)
                                            count = count + 1
                                            print('Item Ordered')
                                            break
                                #print(count)

                                if count ==0:
                                    
                                    if len(filters)>0:
                                        #print('Descrption matching')
                                        count = 0
                                        for kword in filters:
                                            #print(des.lower())
                                            #print(kword)
                                            if kword.lower() in des.lower():
                                                count = count + 1
                                                print('Item Ignored due to Filter')
                                                break

                                if count ==0:                                            
                                    #If price match then order
                                    price = check_price(driver,link,our_price)
                                    if price:
                                        try:
                                            try:
                                                driver.execute_script("document.querySelectorAll('input.a-button-input')[arguments[0]].click()", str(i))
                                            except Exception as ex:
                                                print(ex)
                                                    
                                            time.sleep(1)
                                            
                                        except Exception as ex:
                                            print(ex)

                                        #Request product
                                        request_product(driver)
                                        time.sleep(1)
                                else:
                                    pass

                            else:
                                pass
         
                    old_products = products
                    #print('\n')
                        
                else:
                    print(':> No products available')
            except Exception as ex:
                print('Start: ',ex)
            try:
                driver.refresh()
            except Exception as ex:
                print('Refresh: ',ex)
            time.sleep(int(delay))

    except Exception as ex:
        print(ex)



def start():

    profile_path = root + '\Profile\Amazon'
    options = webdriver.ChromeOptions()
    options.add_argument("disable-infobars")
    options.add_argument("start-maximized")
    options.add_argument('ignore-certificate-errors')
    options.add_argument("test-type")
    options.add_experimental_option("useAutomationExtension", False);
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    options.add_argument('disable-blink-features=AutomationControlled')
    options.add_argument('user-data-dir=%s' % profile_path)
    driver = webdriver.Chrome('chromedriver.exe',options=options)

    url = read_file(root + '\Product Link.txt')
    url = url[0]

    delay = read_file(root + '\settings.txt')
    delay = delay[1]

    filters = read_file(root + '\Filters.txt')
    filt = read_file(root + '\Filters1.txt')
    price = float(filters[0])
    filters = filters[1:]
    filt = filt[0:]
    #print(filt)
    get_products(driver,url,delay,filters,filt,price)

start()