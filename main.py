from tokenize import StringPrefix

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
import time


#opening url
chrome_options=webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach",True)


driver=webdriver.Chrome(options=chrome_options)
url="https://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName=Bangalore&category=B&parameter=rel&hideviewed=N&ListingsType=I&filterCount=3&incSrc=Y&fromSrc=homeSrc"
driver.get(url)


#wait for load
WebDriverWait(driver,10).until(
    EC.presence_of_element_located((By.CLASS_NAME,"mb-srp__card__container"))
)

scroll_count = 0
max_scrolls = 5  # adjust based on how many cards you want
last_height = driver.execute_script("return document.body.scrollHeight")
while scroll_count < max_scrolls:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    scroll_count += 1

soup=BeautifulSoup(driver.page_source,"html.parser")

driver.quit()

container=soup.find_all(name="div",class_="mb-srp__card")
all_titles=[]
all_area_size=[]
all_prices=[]
area_type=[]
# print(f"Total cards found: {len(container)}")
# print(container[0].prettify())
# price=soup.find_all(name="div",class_="mb-srp__card__price--amount")
# for n in price:
#     all_prices.append(n.getText())
# print(all_prices)
for card in container:
    title=card.find(name="h2",class_="mb-srp__card--title")
    all_titles.append(title.getText(strip=True) if title else "N/A")

    price=card.find(name="div",class_="mb-srp__card__price--amount")
    all_prices.append(price.getText(strip=True) if price else "N/A")

    area_value=None
    area_label="N/A"
    carpet_div=card.find(name="div",attrs={'data-summary':"carpet-area"})
    if carpet_div:
        value=carpet_div.find(name="div",class_="mb-srp__card__summary--value")
        area_value=value.getText(strip=True) if value else None
        area_label="carpet area"


    if area_value is None:
        super_div=card.find(name="div",attrs={"data-summary":"super-area"})
        if super_div:
            val=super_div.find(name="div",class_="mb-srp__card__summary--value")
            area_value=val.getText(strip=True) if val else "N/A"
            area_label="super area"

    all_area_size.append(area_value)
    area_type.append(area_label)


print(all_prices)




df=pd.DataFrame({
    'title': all_titles,
    'area-size': all_area_size  ,
    'price':all_prices,
    'area-type':area_type
})
df.drop_duplicates(inplace=True)
print(df)

df.to_excel("real-estate.xlsx",index=False)
df.to_json("area.json")
df.to_csv("area.csv")

























































# title=soup.find_all(name="h2",class_="mb-srp__card--title")
#
# price=soup.find_all(name="div",class_="mb-srp__card__price--amount")
# # area=soup.find_all(name="div",class_="mb-srp__card__summary--value")
# all_title=[]
# all_price=[]
# all_area_size=[]
# for i in title:
#     all_title.append(i.getText())
# print(all_title)
#

#
# # for m in area:
# #     all_area_size.append(m.getText(strip=True) if m else 'N/A')
# # print(all_area_size)
# all_area_size = []
#
# # Loop through each property card
# for card in container:
#     carpet_div = card.find('div', attrs={'data-summary': 'carpet-area'})
#
#     if carpet_div:
#         value = carpet_div.find('div', class_='mb-srp__card__summary--value')
#         all_area_size.append(value.get_text(strip=True) if value else 'N/A')
#     else:
#         all_area_size.append('N/A')
#
# print(all_area_size)

