import os
import json
import csv
import logging
from collections import Counter
from bs4 import BeautifulSoup
import requests

# Настройка логирования
logging.basicConfig(
    filename='scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class LamodaScraper:
    def __init__(self):
        self.list_categories = {
            "man_shoes": ["https://www.lamoda.ru/c/17/shoes-men/?sitelink=topmenuM&l=4", "Man"],
            "man_clothes": ["https://www.lamoda.ru/c/477/clothes-muzhskaya-odezhda/?sitelink=topmenuM&l=3", "Man"],
            "women_shoes": ["https://www.lamoda.ru/c/15/shoes-women/?sitelink=topmenuW&l=4", "Woman"],
            "women_clothes": ["https://www.lamoda.ru/c/355/clothes-zhenskaya-odezhda/?sitelink=topmenuW&l=3", "Woman"]
        }

        self.base_url = self.list_categories["man_shoes"][0]
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        }
        self.categories_constants = {
        "Блузы и рубашки": ["Блузы", "Рубашки", "Боди"],
        "Брюки": [
            "Брюки", "Бриджи и капри", "Горнолыжные брюки", "Джоггеры", "Карго",
            "Классические брюки", "Кожаные брюки", "Кюлоты", "Леггинсы",
            "Повседневные брюки", "Спортивные брюки", "Тайтсы","Зауженные брюки",
            "Утепленные брюки"
        ],
        "Верхняя одежда": [
            "Анораки", "Бомберы", "Горнолыжные куртки", "Демисезонные куртки",
            "Джинсовые куртки", "Жилеты", "Кожаные куртки", "Легкие куртки и ветровки",
            "Пальто", "Парки", "Плащи и тренчи", "Пончо и кейпы", "Пуховики и зимние куртки",
            "Утепленные костюмы и комбинезоны", "Шубы и дубленки","Зимние куртки"
        ],
        "Джемперы, свитеры, кардиганы": [
            "Водолазки", "Джемперы и пуловеры", "Жилеты", "Кардиганы", "Свитеры"
        ],
        "Джинсы": [
            "Джеггинсы", "Прямые джинсы", "Узкие джинсы", "Широкие и расклешенные джинсы"
        ],
        "Домашняя одежда": [
            "Брюки и шорты", "Джемперы и кардиганы", "Комбинезоны", "Комплекты",
            "Маски для сна", "Ночные сорочки", "Пижамы", "Платья", "Рубашки",
            "Толстовки и свитшоты", "Топы и майки", "Футболки и лонгсливы", "Халаты"
        ],
        "Комбинезоны": [
            "Джинсовые комбинезоны", "Кигуруми", "Комбинезоны с брюками",
            "Комбинезоны с шортами", "Спортивные комбинезоны"
        ],
        "Купальники и пляжная одежда": [
            "Лифы", "Парео", "Плавки", "Пляжные платья и туники",
            "Раздельные купальники", "Слитные купальники и монокини"
        ],
        "Нижнее белье": [
            "Аксессуары", "Боди", "Бюстгальтеры", "Комбинации", "Комплекты",
            "Корректирующее белье", "Корсеты", "Пояса для чулок", "Термобелье",
            "Трусы", "Эротическое белье"
        ],
        "Носки, чулки, колготки": [
            "Гольфы и гетры", "Колготки", "Короткие носки", "Носки",
            "Подследники", "Чулки"
        ],
        "Пиджаки и костюмы": [
            "Жакеты", "Жилеты", "Кимоно", "Костюмы с брюками",
            "Костюмы с шортами", "Костюмы с юбкой", "Пиджаки"
        ],
        "Платья и сарафаны": [
            "Вечерние платья", "Джинсовые платья", "Кожаные платья",
            "Платья с запахом", "Платья со спущенными плечами", "Повседневные платья",
            "Сарафаны", "Свадебные платья"
        ],
        "Топы и майки": [
            "Вязаные топы", "Корсеты", "Майки", "Спортивные майки",
            "Спортивные топы", "Топы в бельевом стиле", "Топы на бретелях",
            "Топы с баской", "Топы свободного кроя", "Топы со спущенными плечами"
        ],
        "Футболки и поло": [
            "Комплекты", "Лонгсливы", "Поло", "Спортивные футболки и лонгсливы", "Футболки","Туники"
        ],
        "Худи и свитшоты": [
            "Олимпийки", "Свитшоты", "Толстовки", "Флиски", "Худи"
        ],
        "Шорты": [
            "Бермуды", "Велосипедки", "Джинсовые шорты", "Карго",
            "Повседневные шорты", "Спортивные шорты"
        ],
        "Юбки": [
            "Джинсовые юбки", "Кожаные юбки", "Плиссированные юбки",
            "Прямые юбки", "Узкие юбки"
        ],
        "Прочее": ["Уход за одеждой","Шнурки","Уход за обувью"],
        "Балетки": [
            "Балетки с квадратным носом", "Балетки с круглым носом", "Балетки с острым носом"
        ],
        "Ботильоны": [
            "Ботильоны с квадратным носом", "Ботильоны с круглым носом",
            "Ботильоны с острым носом", "Ботильоны с открытым носом",
            "Высокие ботильоны", "Низкие ботильоны"
        ],
        "Ботинки": [
            "Высокие ботинки", "Мартинсы и др.", "Низкие ботинки",
            "Оксфорды и дерби", "Тимберленды и др.", "Трекинговые ботинки", "Челси",
            "Казаки","Дезерты"
        ],
        "Вечерняя обувь": [
            "Свадебные туфли", "Туфли с застежкой на лодыжке",
            "Туфли с открытой пяткой", "Туфли с открытой стопой", "Туфли с открытым носом"
        ],
        "Домашняя обувь": ["Сланцы"],
        "Кроссовки и кеды": [
            "Кеды", "Высокие кеды", "Низкие кеды",
            "Кроссовки", "Высокие кроссовки", "Низкие кроссовки", "Бутсы"
        ],
        "Мокасины и топсайдеры": ["Мокасины","Топсайдеры"],
        "Обувь с увеличенной полнотой": ["Обувь с увеличенной полнотой"],
        "Резиновая обувь": ["Галоши", "Джиббитсы","Акваобувь"],
        "Сабо и мюли": ["Сабо и мюли","Сабо", "Мюли"],
        "Сандалии": ["Эспадрильи","Сланцы"],
        "Сапоги": [
            "Ботфорты", "Валенки", "Дутики", "Полусапоги", "Сапоги",
            "Угги и унты"
        ],
        "Слипоны": ["Высокие слипоны", "Низкие слипоны"],
        "Туфли": [
            "Закрытые туфли", "Лодочки", "Лоферы", "Туфли Мэри Джейн",
            "Босоножки","Монки","Оксфорды","Дерби"
        ]
    }

    def get_category_for_subcategory(self, subcategory):
        """
        Функция для поиска категории по подкатегории.
        Возвращает категорию (ключ) из словаря, если подкатегория найдена.
        """
        for category, subcategories in self.categories_constants.items():
            if subcategory in subcategories:
                return category
        return "Не указано"  # Если подкатегория не найдена, возвращаем "Не указано"

    def fetch_page(self, custom_url=None, page_number=0):
        # Определяем URL: либо custom_url, либо формируем стандартный
        if page_number == 0:
            url = custom_url or f"{self.base_url}"
        else:
            url = custom_url or f"{self.base_url}?page={page_number}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            #logging.info(f"Успешный запрос к URL: {url}")
            return response.text
        except requests.RequestException as e:
            logging.error(f"Ошибка при запросе к URL {url}: {e}")
            return None


    def get_full_width_elements(self, url):
        html = self.fetch_page(url)
        if html:
            try:
                soup = BeautifulSoup(html, 'html.parser')
                category_elements = soup.find_all('div', class_='x-tree-view-catalog-navigation__category')

                categories_info = []
                for element in category_elements:
                    if element.get('class') == ['x-tree-view-catalog-navigation__category']:
                        link = element.find('a', class_='x-link')
                        count = element.find('span', class_='x-tree-view-catalog-navigation__found')

                        if link and count:
                            category_name = link.text.strip()
                            category_url = link['href']
                            item_count = count.text.strip()
                            categories_info.append({
                                'category_name': category_name,
                                'category_url': category_url,
                                'item_count': item_count
                            })

                logging.info(f"Найдено {len(categories_info)} элементов на странице {url}")
                return categories_info
            except Exception as e:
                logging.error(f"Ошибка при обработке HTML для URL {url}: {e}")
                return []
        else:
            logging.warning(f"HTML-код для URL {url} пуст")
            return []

    def parse_count_pages(self):
        extracted_text = self.fetch_page()
        if extracted_text:
            try:
                start_index = extracted_text.find('"pages":')
                if start_index != -1:
                    text_after_pages = extracted_text[start_index + len('"pages":'):]
                    pages_id = text_after_pages.split(',')[0].strip()
                    logging.info(f"Обнаружено страниц: {pages_id}")
                    return int(pages_id)
            except Exception as e:
                logging.error(f"Ошибка при парсинге количества страниц: {e}")
        return 0

    def get_all_atrib_from_page(self, url):
        # Получаем HTML страницы
        html = self.fetch_page(url)

        # Парсим HTML с помощью BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Находим все теги img с классом 'x-premium-product-gallery__image'
        gallery_images = soup.find_all('img', class_='x-premium-product-gallery__image')

        image_urls = []

        # Извлекаем значения 'src' и добавляем префикс https:
        for img in gallery_images:
            src = img.get('src')
            if src:
                # Добавляем к ссылке https если её нет
                full_url = f"https:{src}"
                image_urls.append(full_url)

        # Находим блок с описанием категорий
        categories_value = {}
        category_elements = soup.find_all('div', class_='x-breadcrumbs__slide')

        element = category_elements[len(category_elements) - 1]
        link = element.find('a')
        if link:
            category_name = link.get_text(strip=True)
            category_url = link.get('href')
            categories_value[category_name] = category_url

        # Находим блок с описанием атрибутов
        attributes_section = soup.find('div', class_='x-premium-product-page__description')

        attributes = {}

        if attributes_section:
            # Находим все элементы, содержащие атрибуты продукта
            attribute_items = attributes_section.find_all('p', class_='x-premium-product-description-attribute')

            # Проходимся по каждому элементу и извлекаем название и значение
            for item in attribute_items:
                name = item.find('span', class_='x-premium-product-description-attribute__name').text.strip()
                value = item.find('span', class_='x-premium-product-description-attribute__value').text.strip()
                attributes[name] = value
        other_atr_dict = self.extract_payload(soup)

        price = 'Цена не найдена'
        price_keys = ['onsite', 'original']

        for key in price_keys:
            price = other_atr_dict.get('product', {}).get('prices', {}).get(key, {}).get('price')
            if price:  # Если цена найдена, выходим из цикла
                break

        brand = other_atr_dict.get('product', {}).get('brand', {}).get('title', 'Бренд не найден')
        # Возвращаем изображения, атрибуты и категории
        return {
            "image_urls": image_urls,
            "attributes": attributes,
            "categories": categories_value,
            "price": price,
            "brand": brand
        }

    def extract_payload(self, soup):
        """
        Извлекает второй объект 'payload' из блока var __NUXT__ в HTML и преобразует его в словарь.

        :param html: HTML-код страницы
        :return: Словарь с данными из второго объекта payload
        """
        # Парсим HTML с помощью BeautifulSoup
        #soup = BeautifulSoup(html, 'html.parser')

        # Находим тег <script>, содержащий "var __NUXT__"
        script_tag = soup.find('script', string=lambda text: text and 'var __NUXT__' in text)
        if not script_tag:
            print("Не удалось найти блок var __NUXT__.")
            return None

        # Извлекаем содержимое скрипта
        script_content = script_tag.string

        # Находим первое вхождение 'payload' и его индекс
        first_payload_index = script_content.find('payload')
        if first_payload_index == -1:
            print("Не удалось найти первое вхождение payload.")
            return None

        # Ищем второе вхождение 'payload'
        second_payload_index = script_content.find('payload', first_payload_index + 1)
        if second_payload_index == -1:
            print("Не удалось найти второе вхождение payload.")
            return None

        # Ищем строку 'settings', чтобы обрезать данные до неё
        settings_index = script_content.find('settings', second_payload_index)
        if settings_index == -1:
            print("Не удалось найти строку 'settings'.")
            return None

        # Обрезаем строку между вторым 'payload' и 'settings'
        payload_str = script_content[second_payload_index + len('payload') + 1:settings_index].strip()

        # Преобразуем строку в валидный JSON-формат
        payload_str = payload_str[:-1]

        # Преобразуем в словарь
        try:
            payload_dict = json.loads(payload_str)
            #print("JSON успешно преобразован в словарь:", payload_dict)
            return payload_dict
        except json.JSONDecodeError as e:
            print(f"Ошибка при преобразовании JSON: {e}")
            return None

    def get_href_list(self, page=1, href_list=None):
        href_list = href_list or []
        html = self.fetch_page(None, page)
        if html:
            try:
                soup = BeautifulSoup(html, 'html.parser')
                grid_catalog = soup.find('div', class_='grid__catalog')
                if grid_catalog:
                    product_cards = grid_catalog.find_all('div', class_='x-product-card__card')
                    for product_card in product_cards:
                        product_link = product_card.find('a', class_='x-product-card__link')
                        if product_link:
                            href_list.append("https://www.lamoda.ru/" + product_link.get('href', ''))

                    logging.info(f"Добавлено {len(product_cards)} ссылок с страницы {page}")
            except Exception as e:
                logging.error(f"Ошибка при парсинге ссылок на странице {page}: {e}")
        else:
            logging.warning(f"HTML-код для страницы {page} пуст")
        return href_list

    def find_duplicates(self, all_links):
        duplicates = [link for link, count in Counter(all_links).items() if count > 1]
        logging.info(f"Найдено {len(duplicates)} дубликатов ссылок")
        return duplicates

    def remove_duplicates(self, all_links):
        unique_links = list(set(all_links))
        logging.info(f"Удалено дубликатов, осталось уникальных ссылок: {len(unique_links)}")
        return unique_links

    def download_image(self, url, save_dir, image_name):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                image_path = os.path.join(save_dir, image_name)
                with open(image_path, 'wb') as img_file:
                    img_file.write(response.content)
                logging.info(f"Картинка успешно загружена: {image_path}")
                return image_path
            else:
                logging.warning(f"Ошибка при скачивании изображения {url}: статус {response.status_code}")
        except Exception as e:
            logging.error(f"Не удалось скачать изображение {url}: {e}")
        return None

    def update_links_file_json(self, filename, parsed_links):
        current_links = {}
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                current_links = json.load(file)

        current_urls = {entry['url'] for entry in current_links.get("links", [])}
        new_links = [link for link in parsed_links if link not in current_urls]

        for link in new_links:
            current_links.setdefault("links", []).append({"url": link, "processed": False})

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(current_links, file, ensure_ascii=False, indent=4)

        logging.info(f"Добавлено {len(new_links)} новых ссылок в {filename}")
        return new_links

    def create_and_append_csv_json(self, json_file, output_csv, main_category, grpc_client=None):
        """
        Добавляет ссылки из JSON в существующий и новый CSV-файлы с категориями, тегами, эмбеддингом и источником.
        Обрабатывает только ссылки со статусом "processed: False". После обработки меняет статус на "processed: True".
        """

        # Создаём имя нового CSV-файла с припиской '_temp'
        temp_output_csv = os.path.splitext(output_csv)[0] + '_temp.csv'

        # Поля CSV-файла
        fieldnames = ['Source', 'Source_csv', 'Image_url', 'main_photo', 'Id', 'Gender', 'Category',
                      'Subcategory', 'Embedding', 'Price', 'Brand', 'Tags']
        print(main_category)
        # Определяем директорию для изображений
        if main_category[1] == "Man":
            images_dir = os.path.join("Photos", "Man", os.path.splitext(output_csv)[0])
        elif main_category[1] == "Woman":
            images_dir = os.path.join("Photos", "Woman", os.path.splitext(output_csv)[0])
        else:
            images_dir = os.path.splitext(output_csv)[0]  # Для других категорий

        # Создание директории для изображений, если ещё не существует
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)

        # Загрузка ссылок из JSON
        links_data = {}
        if os.path.exists(json_file):
            with open(json_file, 'r', encoding='utf-8') as file:
                links_data = json.load(file)

        # Выбираем только ссылки с "processed: False"
        unprocessed_links = [entry for entry in links_data.get("links", []) if not entry["processed"]]

        # Открываем исходный и новый CSV файлы
        with open(output_csv, 'a', newline='', encoding='utf-8') as old_csvfile, \
                open(temp_output_csv, 'w', newline='', encoding='utf-8') as new_csvfile:

            # Создаем писателей для обоих файлов
            old_writer = csv.DictWriter(old_csvfile, fieldnames=fieldnames)
            new_writer = csv.DictWriter(new_csvfile, fieldnames=fieldnames)



            if old_csvfile.tell() == 0:  # tell возвращает 0, если файл пуст
                old_writer.writeheader()
            new_writer.writeheader()  # Записываем заголовок в новый файл

            # Проходимся по каждой новой ссылке
            for link_entry in unprocessed_links:
                url = link_entry["url"].strip()

                try:
                    # Получаем атрибуты и изображения для текущей ссылки
                    result = self.get_all_atrib_from_page(url)
                except Exception as e:
                    logging.error(f"Ошибка при обработке URL {url}: {e}")
                    continue

                # Берём список URL картинок
                image_urls = result.get('image_urls', [])
                attributes = result.get('attributes', {})
                categories = result.get('categories', {})
                subcategory = list(categories.keys())[0] if categories else 'Не указано'
                price = result['price']
                brand = result['brand']

                # Записываем данные для каждой картинки
                for index, image_url in enumerate(image_urls):
                    # Загружаем изображение в директорию
                    image_name = image_url.split('/')[-1]
                    image_path = os.path.join(images_dir, image_name)
                    try:
                        if not os.path.exists(image_path):
                            self.download_image(image_url, images_dir, image_name)
                    except Exception as e:
                        logging.error(f"Ошибка при скачивании картинки {image_url}: {e}")
                        continue


                    # Получаем эмбеддинг через gRPC
                    try:
                        with open(image_path, "rb") as image_file:
                            image_data = image_file.read()
                            embedding_norm = grpc_client.get_embedding(image_name=image_path, image_data=image_data)
                    except Exception as e:
                        logging.error(f"Ошибка при получении эмбеддинга через gRPC для {image_name}: {e}")
                        embedding_norm = "Ошибка"
                        continue

                    #embedding_norm = "Ошибка"

                    # Определяем, является ли фото главным
                    main_photo = index == 0  # Первое фото True, остальные False

                    # Составляем строку данных
                    row_data = {
                        'Source': 'Lamoda',
                        'Source_csv': output_csv,
                        'Image_url': image_url,
                        'main_photo': main_photo,
                        'Id': image_url.split('/')[6].split('_')[0],
                        'Gender': main_category[1],
                        'Category': self.get_category_for_subcategory(subcategory),
                        'Subcategory': subcategory,
                        'Embedding': embedding_norm,
                        'Price': price,
                        'Brand': brand,
                        'Tags': json.dumps(attributes, ensure_ascii=False)  # Конвертируем атрибуты в JSON
                    }

                    # Записываем строку в оба CSV файла
                    old_writer.writerow(row_data)
                    new_writer.writerow(row_data)

                # Обновляем статус ссылки на "processed: True"
                link_entry["processed"] = True

        # Сохраняем обновлённый JSON с обновлёнными статусами
        with open(json_file, 'w', encoding='utf-8') as file:
            json.dump(links_data, file, ensure_ascii=False, indent=4)
        logging.info(f"Данные добавлены в '{output_csv}' и '{temp_output_csv}'")
        print(f"Данные добавлены в '{output_csv}' и '{temp_output_csv}'")



if __name__ == "__main__":
    scraper = LamodaScraper()
    #html = (scraper.fetch_page("https://www.lamoda.ru/c/477/clothes-muzhskaya-odezhda/?sitelink=topmenuM&l=3"))
    #count_and_extract_text_by_class(html, "x-footer-seo-menu-tab-links__item")

    main_category = scraper.list_categories["man_clothes"]
    category = scraper.get_full_width_elements(main_category[0])
    print(category)
    scraper.base_url = "https://www.lamoda.ru" + category[0]["category_url"]
    href = []
    for i in range(1, 4):
        href = scraper.get_href_list(i, href)
        print(href)
        scraper.remove_duplicates(href)
    scraper.update_links_file_json("1234.json", href)
    scraper.create_and_append_csv_json("123.json", "123.csv", main_category)


"""
    for main_category in scraper.list_categories:

        info = scraper.get_full_width_elements(scraper.list_categories[main_category][0])
        for subcategory in info:
            print(subcategory['category_name'])
            scraper.base_url = 'https://www.lamoda.ru' + subcategory['category_url']
            print(scraper.parse_count_pages())
"""