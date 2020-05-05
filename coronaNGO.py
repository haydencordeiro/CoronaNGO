from selenium import webdriver
import time
import requests
from selenium.webdriver.chrome.options import Options
import pandas as pd 
from openpyxl.workbook import Workbook
from xlsx2html import xlsx2html
import os
chrome_options = Options()  
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=chrome_options)

r = requests.get('https://api.ipdata.co?api-key=6d67a0188fdfa81caecafb10882cb4c1b24c5ed970ec6c41d87987c7').json()
driver.get('https://www.covid19india.org/essentials')
driver.find_element_by_xpath('//button[@class="button is-purple search-button-mobile"]').click()
time.sleep(2)
driver.find_element_by_xpath('//input[@id="input-field-searchbar"]').send_keys(r['city']+'\n')
time.sleep(2)
rows=driver.find_elements_by_xpath('//tr[@role="row"]')
data=[]
maxt=0
colname=[]
for no,i in enumerate(rows):
	if(no==0):
		cols=i.text
		colname=cols.split(' ')
		
	else:
		cols=i.text
		cols=cols.split('\n')
		if(len(cols)>maxt):maxt=len(cols)
		data.append(cols)
colname=colname+['alternate']*(abs(len(colname)-maxt))
df=pd.DataFrame(data,columns=colname)
pd.set_option('display.max_columns', None)
print(df.head())
df.to_excel("Service.xlsx")


df.to_html('test.html')

os.system('firefox test.html')