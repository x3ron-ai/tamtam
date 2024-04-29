import json
import codecs
import os
import re
from bs4 import BeautifulSoup
import requests

def find_cite_web_links(text):
     pattern = r'\[\[Файл:.+?\]\]|\[\[.+?\]\]|\[\[Категория:.+?\]\]|<ref[^<]*?Cite\s*web[^<]*?</ref>|<ref[^<]*?cite\s*web[^<]*?</ref>'
      
     links = re.findall(pattern,text)
     
     return links

def find_category_names(text):
    category_pattern =  r'\[\[Категория:(.*?)\]\]'
    categories = re.findall(category_pattern, text)
    category_names = [category.split('|')[0].strip().replace(' ','_') for category in categories]
    return category_names


def find_files(directory):
    if not os.path.isdir(directory):
        print(f"Ошибка: {directory} не является директорией")
        return []
    found_files = []
     
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            found_files.extend(find_files(item_path))
        else:
            found_files.append(item_path)
           
            
    return found_files

def extract_url_info(url):

    if "title=" in url:
        parts = url.split("|")
        title = parts[1] 
        fixedUrl = url.split("|", 1)[0]

        print(fixedUrl)
    else:
        title = "-"
        fixedUrl = url
    try:
        response = requests.get(fixedUrl)
        soup = BeautifulSoup(response.content, "html.parser")
        

        author_tag = soup.find("meta", property="article:author")
        if author_tag:
            author = author_tag["content"]
        else:
            author = "-"

        date_tag = soup.find("meta", property="article:published_time")
        if date_tag:
            date = date_tag["content"]
        else:
            date = "-"

        website_tag = soup.find("meta", property="og:site_name")
        if website_tag:
            website = website_tag["content"]
        else:
            website = "-"

        publisher_tag = soup.find("meta", property="article:publisher")
        if publisher_tag:
            publisher = publisher_tag["content"]
        else:
            publisher = "-"
        return title, author, date, website, publisher, fixedUrl
    except Exception as e:
        print(f"Ошибка при запросе к ресурсу: {e}")     
        return "-", "-", "-", "-", "-", "-" 
     

def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8' ) as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print('Файл не найден')
        return None
    except json.JSONDecodeError:
        print("Ошибка декодирования JSON.")
        return None

def decode_unicode(data):
    try:
        decoded_data = codecs.decode(data, 'unicode-escape')
        return decoded_data
    except UnicodeDecodeError:
        print("Ошибка декодирования")
        return None

def process_json_file(file_path):
    
    json_data = read_json_file(file_path)
    json_title = json_data.get("title","-")
    print("ЗАГОЛОВОК: "+ json_title)
    file_data = {
        'urls':[],
        'categories':[]
    }
    if json_data:
       
        json_string = json.dumps(json_data)
         
        decoded_data = decode_unicode(json_string)
         
        web_links = find_cite_web_links(decoded_data)
        
        url_count = 0
        for link in web_links:
            if "url=" in link:
                url_count += 1   
                url_match = re.search(r'url=(https?://\S+)', link) 
                title_match = re.search(r'title=(.+?)(?=\||$)', link) 
                if (url_match):
                    url = url_match.group(1)
                     
                    titleOrig = title_match.group(1) if title_match else "-"        
                    title, author, date, website, publisher, fixedUrl = extract_url_info(url)
                    print(f"{url_count}. {titleOrig}")
                    print(f"   Ссылка: {fixedUrl}")
                    print(f"   Информация о ссылке: Автор - {author}, Дата - {date}, Веб-сайт - {website}, Издатель - {publisher}")
                    file_data['urls'].append((title, author, date, website, publisher, fixedUrl))
        categories = find_category_names(decoded_data)
        file_data['categories'] = categories
        print("Найденные категории:")
        for category in categories:
            print("https://ru.wikipedia.org/wiki/Категория:" + category)
        return file_data
    else:
        print("Цитаты не найдены")
        return None

def find_files(directory):
    if not os.path.isdir(directory):
        print(f"Ошибка: {directory} не является директорией.")
        return []

    found_files = []

    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            found_files.extend(find_files(item_path))
        else:
            found_files.append(item_path)

    return found_files

def console_main():
    print("1)Открыть один файл\n2)Открыть директорию")
    choice =  int(input())
    if choice == 1:
        file_path = input("Путь к JSON:\n")
        process_json_file(file_path)
    if choice == 2:
        directory_path = input("Укажите путь к директории:\n")
        json_files = find_files(directory_path)
        if json_files:
            for json_file in json_files:
                process_json_file(json_file)
        
        process_json_file(find_files(directory_path))

def work_main(file_path):
    return process_json_file(file_path)

if __name__ == "__main__":
    console_main()