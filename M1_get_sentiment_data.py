import pandas as pd
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager
# Modify line below using the path to your Chrome driver installation
driver = webdriver.Chrome("/path/to/chromedriver")
# For example:
# driver = webdriver.Chrome("/Users/aayala/.wdm/drivers/chromedriver/88.0.4324.96/mac64/chromedriver")

#%%

data = [] 
stock = "FB" # Define stock ticker 

#%%
# Scrape data 
while True:
    stock_url = "https://stocktwits.com/symbol/" + stock
    driver.get(stock_url) # Web scrapping
    sleep(1) # This holds before trying again, you can also use randint() for the number of seconds

    # Getting a readable source with BeautifulSoup
    html = driver.page_source 
    soup = BeautifulSoup(html)
    
    # Finding what we need 
    a = soup.findAll(class_ = "st_21nJvQl st_2h5TkHM st_8u0ePN3 st_2mehCkH")
    if(len(a)==3): # If stock does not have data
        break
    
#%%
# Save the signs of each value
sign_sent = []
for i in range(len(a)):
    if (str(a[i])[161:162] =='m'):
        sign_sent.append(1)
    else:
        sign_sent.append(-1)

# Get data with signs
i = 0
for z in a:
    try:
        z = float(str(z)[-13:-7])
    except:
        try:
            z = float(str(z)[-12:-7])
        except:
            try:
                z = float(str(z)[-11:-7])
            except:
                print("Scrapping failed for "+ stock)

    data.append(z*sign_sent[i])
    i += 1

# Close driver
driver.quit()

print( "Price change (%)          = ", data[0])
print( "Sentiment change (%)      = ", data[1])
print( "Message volume change (%) = ", data[2])