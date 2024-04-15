from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Åbn en webbrowser (f.eks. Google Chrome)
driver = webdriver.Chrome()

# Åbn websiden, du vil navigere på
driver.get("http://127.0.0.1:5000/beregn")

# Vent et par sekunder for at sikre, at siden er fuldt indlæst
time.sleep(2)

# Skift til næste side (for eksempel ved at klikke på en 'Next' knap eller lignende)
# Her antager vi, at der er en knap med teksten 'Next'. Du skal tilpasse dette efter dit specifikke websted.
next_button = driver.find_element_by_xpath("//button[text()='Next']")
next_button.click()

# Vent igen for at sikre, at den næste side er fuldt indlæst
time.sleep(2)

# Luk webbrowseren
driver.quit()
