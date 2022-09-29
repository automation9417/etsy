import os
from time import sleep
from clicknium import clicknium as cc, locator, ui
import requests

search_key_word = 'mobile phone bag'

def main():
    # open the website
    tab = cc.chrome.open("https://www.etsy.com/sg-en/?ref=lgo")

    # input search keyword,and click the search button
    tab.find_element(locator.etsy.txt_search).set_text(search_key_word)
    tab.find_element(locator.etsy.btn_search).click()

    # wait 4 second to loading content
    sleep(4)

    # set sort by 
    tab.find_element(locator.etsy.btn_dropdown).click()
    tab.find_element(locator.etsy.dropdown_item_most_recent).click()
    sleep(4)

    # try get the top 5 pages 
    for page_count in range(0,5):
        similar_elements_img = tab.find_elements(locator.etsy.similar_img)
        print(f'page_count:{page_count}, similar_elements_img length:{len(similar_elements_img)}')

        index = 0
        for img in similar_elements_img:
            download_img(img,index)
            index+=1
        disabled = tab.find_element(locator.etsy.btn_next_page).get_property('disabled')
        if(disabled == 'true'):
            break
        else:
            tab.find_element(locator.etsy.btn_next_page).click()
            sleep(4)
    sleep(3)
    tab.close()
    

def download_img(img_obj,index):
    
    img_src = img_obj.get_property('src')
    print(f'index:{index},start download: {img_src}...')
    
    # img = requests.get(img_src, 
    #                 proxies=dict(http='socks5://127.0.0.1:10808',
    #                              https='socks5://127.0.0.1:10808'))

    img = requests.get(img_src)

    filepath = './download/'+img_src.split('/')[-1]
    i = 1
    while(os.path.exists(filepath)):
        filepath = f'./download/{img_src.split("/")[-1].split(".")[0]}-{i}.jpg'
        i+=1
    with open(filepath,'wb') as f:
        f.write(img.content)
    print(f'index:{index},download success!')

if __name__ == "__main__":
    main()
