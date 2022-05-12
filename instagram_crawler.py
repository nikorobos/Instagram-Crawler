from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service

import time
import os
import wget
import random

# Setup the ChromeWebDriver and open instagram
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
driver.get("https://www.instagram.com/")

# Click the essential cookies allowed in the pop up
cookies_essential = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[4]/div/div/button[1]')))
time.sleep(1)
cookies_essential.click()

# Username and password fields
username = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="loginForm"]/div/div[1]/div/label/input')))
password = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="loginForm"]/div/div[2]/div/label/input')))

username.clear()
password.clear()

user_name = input("Enter your username: \n>> ")
pass_word = input("Enter your password: \n>> ")
username.send_keys(user_name)
password.send_keys(pass_word)



# Click the login button
login_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div')))
time.sleep(2)
login_btn.click()

# Click the Not now on Save your info box
click_not_now = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="react-root"]/section/main/div/div/div/div/button')))
time.sleep(1)
click_not_now.click()

# Click the Don't turn on notification on the pop up
not_now_notifications_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".aOOlW.HoLwm")))
time.sleep(1)
not_now_notifications_btn.click()

# Search for a profile or a hashtag in the searchbar
keyword = input("Enter the name of a profile or a hashtag to continue: \n>> ")
keyword.strip()
search_bar = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')))
search_bar.clear()
search_bar.send_keys(keyword)
time.sleep(1)
search_bar.send_keys(Keys.ENTER)
time.sleep(1)
search_bar.send_keys(Keys.ENTER)
time.sleep(5)

# Scroll until the end of the page and targeting all the images
SCROLL_PAUSE_TIME = 3
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

images = driver.find_elements(By.TAG_NAME,'img')
images = [img.get_attribute('src') for img in images]
images = images[:-2]
print('Number of scraped images: ', len(images))

# Create a directory to Desktop with the name of the profile and check if already exists
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 
path = os.path.join(desktop, keyword)

dir_exists = os.path.exists(path)
if (dir_exists):
    random_num = random.randint(1,20)
    path = os.path.join(desktop, keyword + str(random_num))
    os.mkdir(path)
else:
    os.mkdir(path)
    
# Save images to the created directory
counter = 0
for image in images:
    save_as = os.path.join(path, keyword + str(counter)+ '.jpg')
    wget.download(image, save_as)
    counter += 1
