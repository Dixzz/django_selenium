import datetime

from django.http import HttpResponse
from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
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

    if i == 1:
        date = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%d-%m-%Y")
        print('## Working on Cleartrip ##')
        print(fro, to, date, ch, adu)
        #driver.get('https://www.cleartrip.com/')
        driver.find_element_by_xpath('//*[@id="FromTag"]').send_keys(fro)
        driver.find_element_by_xpath('//*[@id="ToTag"]').send_keys(to)
        driver.find_element_by_xpath('//*[@id="DepartDate"]').send_keys(date)
        driver.find_element_by_xpath('//*[@id="Adults"]').send_keys(adu)
        btn = driver.find_element_by_xpath('/html/body/section[2]/div/div[1]/div/form/div[6]/input[2]')
        driver.execute_script("arguments[0].click();", btn)
        return HttpResponse('Success')

    elif i == 2:
        print('## Working on EaseMyTrip ##')
        print(fro, to, date, ch, adu)
        '''e = driver.find_element_by_xpath('//*[@id="FromSector_show"]')
        e.clear()
        e.send_keys(fro)
        e = driver.find_element_by_id('fromautoFill')
        e.click()'''

        m = driver.find_element_by_xpath('//input[@id="Editbox13_show"]')
        m.click()
        driver.implicitly_wait(10)
        m.send_keys(to)
        #m.click()
        driver.implicitly_wait(20)
        m.send_keys(Keys.ARROW_DOWN, Keys.RETURN)
        driver.implicitly_wait(20)

        #m.send_keys(Keys.ARROW_DOWN)
        #m.send_keys(Keys.ENTER)
        #print(m.text, m.id)

        #WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="hdnAutoFill"]')))
        #e = driver.find_element_by_xpath('//*[@id="hdnAutoFill"]')
        #driver.execute_script('arguments[0].click();', e)


        e = driver.find_element_by_xpath('//*[@id="ddate"]')
        e.click()
        date = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")
        driver.find_element_by_xpath('//*[contains(@id,"_%s")]'%date).click()

        btn = driver.find_element_by_xpath('//*[@id="search"]/input')
        #driver.execute_script("arguments[0].click();", btn)
        return HttpResponse('Success')

    elif i == 3:
        print('## Working on Goibibo ##')
        print(fro, to, date, ch, adu)

        '''WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "react-autosuggest-1")))
        m = driver.find_element_by_id('react-autosuggest-1')
        text_contents = [el.text for el in driver.find_elements_by_xpath("//ul[@id='react-autosuggest-1']/li")]

        m = str([text_contents.__getitem__(0)])
        brack1 = m.find('(')
        brack2 = m.find(')')
        place = m[brack1:brack2+1]
        all1 = fro+" "+place
        e = driver.find_element_by_xpath('//*[@id="gosuggest_inputSrc"]')
        e.send_keys(all1)
        print(all1)

        e = driver.find_element_by_xpath('//*[@id="gosuggest_inputDest"]')
        e.send_keys(to)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "react-autosuggest-1")))
        m = driver.find_element_by_id('react-autosuggest-1')
        text_contents = [el.text for el in driver.find_elements_by_xpath("//ul[@id='react-autosuggest-1']/li")]

        m = str([text_contents.__getitem__(0)])
        brack1 = m.find('(')
        brack2 = m.find(')')
        place = m[brack1:brack2+1]
        all = to+" "+place
        e = driver.find_element_by_xpath('//*[@id="gosuggest_inputDest"]')
        print(all)

'''
        '''e = driver.find_element_by_xpath('//*[@id="gosuggest_inputSrc"]')
        e.send_keys(fro)

        e = driver.find_element_by_xpath('//*[@id="gosuggest_inputDest"]')
        e.send_keys(to)'''

        print(fro, to)

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
        driver.implicitly_wait(10)
        print(to)
        f = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "react-autosuggest-1")))
        #driver.find_element('react-autosuggest-1', )
        driver.find_element_by_xpath("//ul[@id='react-autosuggest-1']/li[@id='react-autosuggest-1-suggestion--0']").click()

        # Journey Date #
        e = driver.find_element_by_xpath('//*[@id="departureCalendar"]')
        e.click()

        date = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%Y%m%d")
        driver.find_element_by_xpath('//*[@id="fare_%s"]'%date).click()

        #btn = driver.find_element_by_xpath('//*[@id="gi_search_btn"]')
        #driver.execute_script("arguments[0].click();", btn)
        return HttpResponse('Success')

    elif i == 4:
        print('## Working on MMT ##')
        print(fro, to, date, ch, adu)

        month = int(datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%m"))
        day = int(datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%d"))

        month = datetime.date(1900, month, 1).strftime('%b')

        #Find element and enter From journey details
        e = driver.find_element_by_xpath('//*[@id="fromCity"]')
        e.send_keys(fro)

        #Find from element in autosuggestion
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='react-autowhatever-1']//p[contains(text(), '%s')]"%fro)))
        e = driver.find_element_by_xpath('//*[@id="react-autowhatever-1"]//p[contains(text(), "%s")]'%fro)
        print(e.text)
        e.click()

        # Find element and enter From journey details
        m = driver.find_element_by_xpath('//*[@id="toCity"]')
        print(m.text)
        m.send_keys(to)

        # Find from element in autosuggestion
        '''WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='react-autowhatever-1']//p[contains(text(), '%s')]"%to)))
        e = driver.find_element_by_xpath('//*[@id="react-autowhatever-1"]//p[contains(text(), "%s")]' % to)
        e.click()'''

        "//div[contains(@aria-label,'Mar 07 ')]"

        '''e = driver.find_element_by_xpath("//*[@class='lbl_input latoBold appendBottom10']")
        driver.execute_script("arguments[0].click();", e)

        m = WebDriverWait(driver, 10)
        m.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(@aria-label,'%s %d')]"%(month, day))))
        driver.find_element_by_xpath("//div[contains(@aria-label,'%s %d')]"%(month, day)).click()'''

        return HttpResponse('Success')