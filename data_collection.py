### Solution that works in google Colab
#!pip install kora -q
#from kora.selenium import wd


### Solution for local
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

wd = webdriver.Chrome('C:/Users/julia/AppData/Local/rasjani/WebDriverManager/bin/chromedriver.exe')



import time

import pandas as pd

# Functions that work on the Meta Data
# Could be Work on the page ob the 
# Get meta data

def find_hut_name(wd):
  meta_info_raw = wd.find_element(By.CLASS_NAME, 'info')
  hut_name = meta_info_raw.find_element(By.TAG_NAME, 'h4').text
  return hut_name
  
def get_meta_data_colums(wd):
    data = []
    
    meta_info_raw = wd.find_element(By.CLASS_NAME, 'info')

    data.append("Hütten-Name")
    data.append("Hütte-ID")
  
    for meta_info in meta_info_raw.find_elements(By.TAG_NAME, 'span'):
       #print (meta_info.text)
       data.append(meta_info.text.split(":")[0])

    return data


# Get meta data

def get_meta_data(wd):
  data = []
  
  meta_info_raw = wd.find_element(By.CLASS_NAME, 'info')

  hut_name = find_hut_name(wd)

  data.append(hut_name)
  data.append(wd.current_url.split("=")[1])

  for meta_info in meta_info_raw.find_elements(By.TAG_NAME, 'span'):
    #print (meta_info.text)
    data.append(meta_info.text.split(":")[1])


  return data

#get_meta_data(wd)

## Select the Starting Date

def select_date(wd, selected_date):
  # Enter Data to start looking
  date_picker = wd.find_element(By.ID, 'fromDate')
  date_picker.clear()
  date_picker.send_keys(selected_date)

  date_picker.send_keys(Keys.RETURN)

# Function starts here

def get_free_beds(wd):
  dates_looked_up = []
  free_beds = []

  # Grenze Suche auf die Ergebnisse unten ein
  reservation_data = wd.find_elements(By.CLASS_NAME, 'cal-content')

  # Behandle jeden tag einzeln
  for day_data in reservation_data:

    date = day_data.find_element(By.CSS_SELECTOR, "input").get_attribute("value")

    dates_looked_up.append(date)
    #print(date)

    # Summiere Freie Plätze

    free_beds_info = day_data.find_elements(By.CLASS_NAME, "pull-right")

    zahl_freie_betten = 0

    for zimmer in free_beds_info:
      #print(zimmer)
      if zimmer.text == "":
        free_beds_in_this_room = 0
      else:
        free_beds_in_this_room = int(zimmer.text.split(" ")[0])
      
      zahl_freie_betten = free_beds_in_this_room + zahl_freie_betten

    free_beds.append(zahl_freie_betten)

  return dates_looked_up, free_beds
#print(dates_looked_up)
#print(free_beds)

dates_looked_up, free_beds = get_free_beds(wd)

# Loop through all huts
# Open each with a selemium webdriver
def collect_data(selected_date, list_of_huts):
  first_run = True


  for id in list_of_huts:

    try:
      url = "https://www.alpsonline.org/reservation/calendar?hut_id={}".format(id)
          
      wd.get(url)
      time.sleep(0.1)
      select_date(wd, selected_date)
      time.sleep(0.1)

      if first_run == True:
        # create database
        meta_data_df = pd.DataFrame(columns=get_meta_data_colums(wd))
        free_beds_data_df = pd.DataFrame(columns=["Hütten-Name","Datum","Freie Betten", "Hütten-ID"])
        first_run = False

      # Store Meta Data Results
      #new_data = get_meta_data(wd)
      meta_data_df = meta_data_df.append(pd.DataFrame([get_meta_data(wd)], columns=get_meta_data_colums(wd)), ignore_index=True)
      #meta_data_df = meta_data_df.concat(pd.DataFrame([get_meta_data(wd)], columns=get_meta_data_colums(wd)), ignore_index=True)

      # FIXME: Hier funktioniert die Abfrage nicht.
      time.sleep(1)
      dates_looked_up, free_beds = get_free_beds(wd)

      # Füge neue freie Betten hinzu
      temp_free_beds_data_df = pd.DataFrame(columns=["Hütten-Name","Datum","Freie Betten", "Hütten-ID"])
      temp_free_beds_data_df["Datum"]=dates_looked_up
      temp_free_beds_data_df["Freie Betten"]=free_beds
      temp_free_beds_data_df["Hütten-ID"] = id
      temp_free_beds_data_df["Hütten-Name"] = find_hut_name(wd)
      free_beds_data_df = free_beds_data_df.append(temp_free_beds_data_df, ignore_index=True)

    except:
      print("No data for hut_id={} found!".format(id))
      pass
  
  return meta_data_df, free_beds_data_df