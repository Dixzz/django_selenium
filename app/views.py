import datetime

from django.http import HttpResponse
from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def index(request):
    return render(request, 'index.html')

def res(request):
    fro = request.POST.get('fromm')
    to = request.POST['To']
    date = request.POST['date']
    ch = request.POST['choice']
    adu = request.POST.get('adults')

    if ch == 'https://www.cleartrip.com':
        i = 1
    elif ch == 'https://www.easemytrip.com':
        i = 2
    elif ch == 'https://www.goibibo.com/':
        i = 3
    elif ch == "https://www.makemytrip.com/flights/":
        i = 4

    else:
        i = 0
    print(fro, to, date, ch, adu, i)
    a = open(fro, to, date, ch, adu, i)
    return a

def open(fro, to, date, ch, adu, i):
    driver = webdriver.Chrome('C:/Users/unknown/Desktop/Shit/chromedriver.exe')
    driver.maximize_window()
    driver.get(ch)
    try:
        if i == 1:
            date = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%d-%m-%Y")
            print('### Working on Cleartrip ###')

            # This was the easiest website to work, great thanks to web dev of ClearTrip
            driver.find_element_by_xpath('//*[@id="FromTag"]').send_keys(fro)
            driver.find_element_by_xpath('//*[@id="ToTag"]').send_keys(to)
            driver.find_element_by_xpath('//*[@id="DepartDate"]').send_keys(date)
            driver.find_element_by_xpath('//*[@id="Adults"]').send_keys(adu)

            btn = driver.find_element_by_xpath('/html/body/section[2]/div/div[1]/div/form/div[6]/input[2]')
            driver.execute_script("arguments[0].click();", btn)
            return HttpResponse('Success')

        elif i == 2:
            print('### Working on EaseMyTrip ###')

            #From Journey
            m = driver.find_element_by_xpath('//input[@id="FromSector_show"]')
            m.click()
            m.send_keys(fro)

            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//li[@class='ui-menu-item']//span[@class='ct'][contains(text(),'%s')]"%fro)))
            e = driver.find_element_by_xpath('//li[@class="ui-menu-item"]//span[@class="ct"][contains(text(),"%s")]'%fro)
            e.click()

            #To journey
            m = driver.find_element_by_xpath('//input[@id="Editbox13_show"]')
            m.click()
            m.send_keys(to)

            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//li[@class='ui-menu-item']//span[@class='ct'][contains(text(),'%s')]"%to)))
            e = driver.find_element_by_xpath('//li[@class="ui-menu-item"]//span[@class="ct"][contains(text(),"%s")]'%to)
            e.click()

            #Date
            e = driver.find_element_by_xpath('//*[@id="ddate"]')
            e.click()
            date = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")
            driver.find_element_by_xpath('//*[contains(@id,"_%s")]'%date).click()

            #Search
            btn = driver.find_element_by_xpath('//*[@id="search"]/input')
            driver.execute_script("arguments[0].click();", btn)
            return HttpResponse('Success')

        elif i == 3:
            print('### Working on Goibibo ###')

            # Journey Source #
            e = driver.find_element_by_xpath('//*[@id="gosuggest_inputSrc"]')
            e.clear()
            e.send_keys(fro)
            driver.implicitly_wait(10)
            f = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "react-autosuggest-1")))
            driver.find_element_by_xpath("//ul[@id='react-autosuggest-1']/li[@id='react-autosuggest-1-suggestion--0']").click()

            # Journey Destination #
            e = driver.find_element_by_xpath('//*[@id="gosuggest_inputDest"]')
            e.clear()
            e.send_keys(to)

            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "react-autosuggest-1")))
            driver.find_element_by_xpath("//ul[@id='react-autosuggest-1']/li[@id='react-autosuggest-1-suggestion--0']").click()

            # Journey Date
            e = driver.find_element_by_xpath('//*[@id="departureCalendar"]')
            e.click()

            date = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%Y%m%d")
            driver.find_element_by_xpath('//*[@id="fare_%s"]'%date).click()

            # Search
            btn = driver.find_element_by_xpath('//*[@id="gi_search_btn"]')
            driver.execute_script("arguments[0].click();", btn)
            return HttpResponse('Success')

        elif i == 4:
            print('### Working on MMT ###')

            month = int(datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%m"))
            day = int(datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%d"))

            month = datetime.date(1900, month, 1).strftime('%b')

            #Find element and enter From journey details
            e = driver.find_element_by_xpath('//*[@id="fromCity"]')
            e.send_keys(fro+"")

            #Find from element in autosuggestion
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='react-autowhatever-1']//p[contains(text(), '%s')]"%fro)))
            e = driver.find_element_by_xpath('//*[@id="react-autowhatever-1"]//p[contains(text(), "%s")]'%fro)
            e.click()

            # Find element and enter To journey details
            e = driver.find_element_by_xpath('//input[@id="toCity"]')
            driver.execute_script("arguments[0].click();", e)
            e.send_keys(to+"")

            # Select to autosuggestion partially
            # HACK to fix code, unable to find element
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//input[@class="react-autosuggest__input react-autosuggest__input--open"]')))
            e = driver.find_element_by_xpath('//input[@class="react-autosuggest__input react-autosuggest__input--open"]')
            e.send_keys(to+"")

            # Find from element in autosuggestion for to
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-autowhatever-1"]//p[contains(text(), "%s")]'%to)))
            e = driver.find_element_by_xpath('//*[@id="react-autowhatever-1"]//*[@class="react-autosuggest__suggestion react-autosuggest__suggestion--first"]//p[contains(text(), "%s")]'%to)
            driver.execute_script("arguments[0].click();", e)

            #Date
            #Find element which opens datepicker and click
            e = driver.find_element_by_xpath("//*[@class='lbl_input latoBold appendBottom10']")
            driver.execute_script("arguments[0].click();", e)

            #Dind date matching to label and click
            m = WebDriverWait(driver, 10)
            m.until(EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@aria-label,'%s %d')]"%(month, day))))
            driver.find_element_by_xpath("//div[contains(@aria-label,'%s %d')]"%(month, day)).click()

            #Search button
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]//*[@data-cy="submit"]//*[contains(text(), "Search")]')))
            driver.find_element_by_xpath('//*[@id="root"]//*[@data-cy="submit"]//*[contains(text(), "Search")]').click()
            return HttpResponse('Success')

    except TimeoutException as e:
        return HttpResponse(e.msg)

    except NoSuchWindowException as e:
        return HttpResponse(e.msg+"\nConnection closed")

    except:
        return HttpResponse("<h1>Something went wrong</h1>")