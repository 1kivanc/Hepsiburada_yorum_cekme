import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def hepsiburada_yorum_cek(url):
    global_delay = 0.5
    driver = webdriver.Chrome()

    try:
        driver.get(url)
        time.sleep(5)  
        print('Ürünün yorum sayfasına gidildi')

        current_page_number = 1  
        while True:
            time.sleep(3)
            pagination_element = driver.find_element(By.XPATH, '/html/body/div[2]/main/div[2]/div/div/div/div/div/div/div[1]/div[2]/div[2]/div[6]/div[3]/div[2]/div/ul')
            page_elements = pagination_element.find_elements(By.TAG_NAME, 'li')
            total_pages = len(page_elements) - 1  

            print(f'Şu anki sayfa: {current_page_number}, Toplam sayfa: {total_pages}')

            for i in range(1, 11):
                try:
                    yorum = driver.find_element(By.XPATH, f'/html/body/div[2]/main/div[2]/div/div/div/div/div/div/div[1]/div[2]/div[2]/div[6]/div[3]/div[1]/div[{i}]/div[2]/div[2]/span').text
                    with open("yorumlar.txt", "a", encoding='utf-8') as yorum_file:
                        yorum_file.write(yorum + '\n')
                    time.sleep(global_delay)
                except Exception as e:
                    print(f'Yorum çekilirken hata oluştu: {str(e)}')

            if current_page_number < total_pages:
                current_page_number += 1
                next_page_url = url + f"?sayfa={current_page_number}"
                driver.get(next_page_url)
                print(f'Sonraki sayfa ({current_page_number}) yükleniyor...')
                time.sleep(3) 
                pagination_element = driver.find_element(By.XPATH, '/html/body/div[2]/main/div[2]/div/div/div/div/div/div/div[1]/div[2]/div[2]/div[6]/div[3]/div[2]/div/ul')
                page_elements = pagination_element.find_elements(By.TAG_NAME, 'li')
                total_pages = len(page_elements) - 1 

            else:
                break

    except Exception as e:
        print('Hata: ' + str(e))
    finally:
        print('Tüm yorumlar çekildi')
        driver.quit()

urun_url = input("Hepsiburada ürününün linkini giriniz: ")

if not urun_url.endswith("-yorumlari"):
    urun_url += "-yorumlari"

hepsiburada_yorum_cek(urun_url)
