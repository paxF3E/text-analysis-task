from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

opt = Options()
opt.headless = True
driver = webdriver.Chrome(executable_path='chromedriver', options=opt)
with open('Input.csv', 'r') as f:
    input_urls = f.read().split('\n')[1:]
f.close()

for x in input_urls:
    fname = "Input/" + x.split(',')[0] + ".txt"
    url = x.split(',')[1]
    try:
        driver.get(url)
        head = driver.find_element(By.TAG_NAME, "h1").text + "\n"
        body = (driver.find_element(By.CLASS_NAME, "td-post-content").text.splitlines()[:-1])
        content = ""
        for i in body:
            content = content + i + "\n"
        with open(fname, 'w') as outf:
            outf.write(head)
            outf.write(content)
            outf.close()
        print(f"Article #{x.split(',')[0]} scraped and written to '{fname}'")
    except Exception as e:
        print(f"An error occured for article #{x.split(',')[0]}. {e}")

driver.quit()
