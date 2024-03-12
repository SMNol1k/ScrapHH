# # Нужно выбрать те вакансии, у которых в описании есть ключевые слова "Django" и "Flask".
# # Записать в json информацию о каждой вакансии - ссылка, вилка зп, название компании, город.
# #
# # статья
# # <div class="serp-item vacancy-serp-item_clickme serp-item_link"
# # data-qa="vacancy-serp__vacancy vacancy-serp__vacancy_standard">
# # id="a11y-main-content"
# # class="vacancy-serp-item__layout"
#
# import lxml
# # Заголовок
# # h3 data-qa="bloko-header-3" class="bloko-header-section-3"
#
# # Ссылка
# # <a class="bloko-link" target="_blank" href="https://adsrv.hh.ru/click?b=932728&amp;place=35&amp;meta=j7
#
# # Вилка ЗП
# # <span data-qa="vacancy-serp__vacancy-compensation" class="bloko-header-section-2"
#
# # Название компании
# # <div class="bloko-v-spacing-container bloko-v-spacing-container_base-2">
#
# # Город
# # <div data-qa="vacancy-serp__vacancy-address" class="bloko-text">Москва</div>
# # <div data-qa="vacancy-serp__vacancy-address" class="bloko-text">Санкт-Петербург</div>
import json
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
def gen_headers():
    headers = Headers(browser='chrome',
                      os='win')
    return headers.generate()

response = requests.get('https://spb.hh.ru/search/vacancy?area=1&area=2&ored_clusters=true&order_by=publication_time&search_field=name&search_field=company_name&search_field=description&text=python&enable_snippets=false&salary=130000&only_with_salary=true',
                        headers=gen_headers())

main_html = response.text

main_soup = BeautifulSoup(main_html, 'lxml')

article_list_tag = main_soup.find('main', class_='vacancy-serp-content')

article_tags = article_list_tag.find_all('div', class_='serp-item serp-item_link')
print(len(article_tags))

vacancies = []

for item in article_tags:
    h2_tag = item.find('h3', class_='bloko-header-section-3')
    a_tag = h2_tag.find('a', class_='bloko-link')
    title = h2_tag.text.strip()
    link = a_tag['href']
    salary_fork = item.find('span', class_="bloko-header-section-2")
    name_company = item.find('div', class_='bloko-v-spacing-container bloko-v-spacing-container_base-2')
    city = item.find_all('div', class_='bloko-text')[1].text.strip()

    response = requests.get(link,
                            headers=gen_headers())

    article_html = response.text
    article_soup = BeautifulSoup(article_html, "lxml")
    full_article_tag = article_soup.find('div', class_="g-user-content")
    description = full_article_tag.text

    if "Django" in description or "Flask" in description:
        vacancies.append({
            'title': title,
            'link': link,
            'salary_fork': salary_fork.text.strip() if salary_fork else "",
            'name_company': name_company.text.strip() if name_company else "",
            'city': city.strip() if city else ""
        })


with open('vacancies.json', 'w', encoding='utf-8') as f:
    json.dump(vacancies, f, ensure_ascii=False, indent=4)


