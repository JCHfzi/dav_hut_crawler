
# %% First Part: Script to download driver binary

from selenium import webdriver
#from selenium.webdriver.chrome.service import Service
# Using this https://github.com/MarketSquare/webdrivermanager
#from webdrivermanager.chrome import ChromeDriverManager

from webdrivermanager import ChromeDriverManager

gdd = ChromeDriverManager()
gdd.download_and_install()

# ' C:/Users/julia/AppData/Local/rasjani/WebDriverManager/bin/chromedriver.exe'

#%% Seconc part to use driver. Path must be adapted in the data_collection script

from selenium import webdriver
driver = webdriver.Chrome('C:/Users/julia/AppData/Local/rasjani/WebDriverManager/bin/chromedriver.exe')

# %%
