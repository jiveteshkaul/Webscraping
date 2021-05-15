from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from shutil import which
from selenium.webdriver.chrome.options import Options
import time

chrome_options=Options()
chrome_options.add_argument("--headless")
chrome_path=which("chromedriver")
driver=webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
print("Starting Driver!!")
driver.get(url="https://www.worldometers.info/coronavirus")
time.sleep(10)

table_rows=driver.find_elements_by_xpath("(//table[@id='main_table_countries_today']/tbody)[1]/tr[@role='row' and @class='even' or  @class='odd' ]")
#print(len(table_rows))
opfile="results.csv"
f=open(opfile,'w')
f.write("COUNTRY|TOTAL_CASES|NEW_CASES|TOTAL_DEATHS|NEW_DEATHS|TOTAL_RECOVERED|ACTIVE_CASES")
f.write("\n")


for item in  table_rows:
    try:
        country=item.find_element_by_xpath("(.//td)[2]/a").text
    except:
        country=''
    try:
        total_cases=item.find_element_by_xpath("(.//td)[3]").text
    except:
        total_cases=''
    try:
        new_cases=item.find_element_by_xpath("(.//td)[4]").text
    except:
        new_cases=''
    try:
        total_deaths=item.find_element_by_xpath("(.//td)[5]").text
    except:
        total_deaths=''
    try:
        new_deaths=item.find_element_by_xpath("(.//td)[6]").text
    except:
        new_deaths=''
    try:
        total_recovered=item.find_element_by_xpath("(.//td)[7]").text
    except:
        total_recovered=''
    try:
        active_cases=item.find_element_by_xpath("(.//td)[8]").text
    except:
        active_cases=''

    op_line=f'{country}|{total_cases}|{new_cases}|{total_deaths}|{new_deaths}|{total_recovered}|{active_cases}'
    f.write(op_line)
    f.write("\n")
    print("Fetched for Country : " + country)

f.close()
print("Done!!")

