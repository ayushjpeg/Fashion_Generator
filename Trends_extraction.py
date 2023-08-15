from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
from support import trend_check
insta = []
faceb = []
tweet = []
images = []
array_fashion = trend_check()

def instagram(q_srch):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    driver = webdriver.Chrome(options=options)

    driver.get("http://www.instagram.com")


    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

    username.clear()
    username.send_keys("grtidkumar.com")
    password.clear()
    password.send_keys("Grid@1304")

    button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    time.sleep(5)
    kwrd = array_fashion
    curr = []
    print("Started")
    keyword = kwrd[q_srch]
    driver.get("https://www.instagram.com/explore/tags/"+keyword[1:]+"/")
    n_scrolls = 1
    for j in range(0, n_scrolls):
        driver.execute_script("window.scrollTo(0, 0.01)")
        time.sleep(5)
    time.sleep(5)
    anchors = driver.find_elements(by=By.TAG_NAME, value="span")
    curr.append(keyword[1:])
    curr.append(anchors[3].text)
    
    return curr
    
