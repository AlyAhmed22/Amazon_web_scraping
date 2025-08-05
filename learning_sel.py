from selenium.webdriver.common.by import By
from utils import start_driver
import time
import json

with open ("data.json","w") as f :
    json.dump([],f)

def write_json(new_data, filename="products.jsonl"):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(json.dumps(new_data, ensure_ascii=False) + "\n")

driver = start_driver()
driver.get('https://www.amazon.eg/-/en/s?k=headphones&i=electronics&rh=n%3A18018102031&dc&language=en&crid=1H8UG3IYZD6X8&qid=1753809199&sprefix=hea%2Caps%2C220&xpid=QmGI65tC-45bx&ref=sr_pg_1')
time.sleep(10)
page_counter=0

while True:
    element_list = driver.find_element(By.CSS_SELECTOR, "div.s-main-slot.s-result-list.s-search-results.sg-row")
    items = element_list.find_elements(By.XPATH, './/div[@data-component-type="s-search-result"]')

    for item in items:
        title = item.find_element(By.TAG_NAME, "h2").text
        try:
            currency_symbol = item.find_element(By.CSS_SELECTOR, 'span.a-price-symbol').text
            price_whole = item.find_element(By.CSS_SELECTOR, 'span.a-price-whole').text
            price_fraction = item.find_element(By.CSS_SELECTOR, 'span.a-price-fraction').text
            price = f"{currency_symbol}{price_whole}.{price_fraction}"
        except:
            price = "NO PRICE FOUND"

        try:
            img = item.find_element(By.CLASS_NAME, "s-image").get_attribute("src")
        except:
            img = "NO IMG FOUND"

        try:
            link = item.find_element(By.CLASS_NAME, "a-link-normal").get_attribute("href")
        except:
            link = "NO LINK FOUND"

        print("TITLE : " + title)
        print("price : " + price)
        print("IMG : " + img)
        print("LINK : " + link + "\n")
        
        write_json({ "title": title, "price": price,"image": img,"link": link })
    # المحاولة للضغط على زر "Next"
    try:
        next_button = driver.find_element(By.CLASS_NAME, "s-pagination-next")
        if 'disabled' in next_button.get_attribute('class'):
            print("No more pages.")
            break
        else:
            next_button.click()
            time.sleep(5)
            page_counter+=1
    except Exception as e:
        print("Next button not found or last page reached.")
        break

print(page_counter)
