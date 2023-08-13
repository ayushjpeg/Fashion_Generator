from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time

insta = []
faceb = []
tweet = []
images = []
array_fashion = ['#iiest', '#capri', '#oneshouldertop', '#trouser', '#tanktop', '#tubetop', '#satindress','#bodycondress', '#halterneck', '#poloneck', '#bikershort', '#camisole', '#sweatshirt', '#highwaistjeans', '#sharara', '#bellbottom', '#bomberjacket', '#leggings', '#vintageshirt', '#kimonocardigan', '#boilersuit', '#puffsleeves', '#coldshoulder', '#croptop', '#joggers', '#buckethat', '#poloshirt', '#sweatpants', '#rippedjeans', '#kaftandress', '#gown', '#cargopants', '#denimjacket', '#miniskirt', '#bratop', '#ponchos', '#polkadotdress', '#meshtop', '#hoodie', '#pullover', '#stripedshirt', '#jeggings', '#trenchcoat', '#waistcoat', '#blazer', '#offshoulder', '#denimshorts', '#loungewear', '#chinos', '#pencilskirt', '#floraldress', '#dhotipants', '#skaterdress', '#harempants', '#tees', '#dungaree', '#corset', '#peplumtop', '#jumpsuit', '#anarkalidress', '#lehenga', '#maxidress', '#yogapants', '#sherwani', '#sequencedress']


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

    time.sleep(3)
    kwrd = array_fashion
    curr = []
    print("Started")
    keyword = kwrd[q_srch]
    driver.get("https://www.instagram.com/explore/tags/"+keyword[1:]+"/")
    n_scrolls = 1
    for j in range(0, n_scrolls):
        driver.execute_script("window.scrollTo(0, 0.01)")
        time.sleep(2)
    time.sleep(2)
    anchors = driver.find_elements(by=By.TAG_NAME, value="span")
    curr.append(keyword[1:])
    curr.append(anchors[3].text)
    curr.append("https://www.flipkart.com/search?q="+keyword[1:]+"&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off")
    
    return curr
    
        
        
  
    
for q_srch in range(0, len(array_fashion)):
    try:
        print(instagram(q_srch))
    except:
        continue