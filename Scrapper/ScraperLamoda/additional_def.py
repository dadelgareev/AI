import json

from bs4 import BeautifulSoup

from scraper import LamodaScraper

categories_constants = {
        "Блузы и рубашки": [
            "Блузы", "Рубашки","Рубашки с длинным рукавом",
            "Джинсовые рубашки","Рубашки с коротким рукавом",
            "Рубашки и сорочки","Джинсовые","Блузы и рубашки","Блузы с коротким рукавом",
            "Блузы с длинным рукавом","Блузы с рюшами и воланами","Кружевные блузы","Блузы без рукавов",
            "Блузы с бантом","Блузы с открытыми плечами","Рубашки и топы"
        ],
        "Брюки": [
            "Брюки", "Бриджи и капри", "Горнолыжные брюки", "Джоггеры", "Карго",
            "Классические брюки", "Кожаные брюки", "Кюлоты", "Леггинсы",
            "Повседневные брюки", "Спортивные брюки", "Тайтсы","Зауженные брюки",
            "Утепленные брюки","Брюки и шорты","Прямые брюки","Леггинсы и тайтсы",
            "Прямые","Бордшорты"
        ],
        "Верхняя одежда": [
            "Анораки", "Бомберы", "Горнолыжные куртки", "Демисезонные куртки",
            "Джинсовые куртки", "Кожаные куртки", "Легкие куртки и ветровки",
            "Пальто", "Парки", "Плащи и тренчи", "Пончо и кейпы", "Пуховики и зимние куртки",
            "Утепленные костюмы и комбинезоны", "Шубы и дубленки","Зимние куртки",
            "Верхняя одежда","Пуховики","Куртки","Плащи","Толстовки и куртки","Куртки меховые",
            "Одежда","Шубы","Демисезонные пальто","Двубортные пальто","Классические",
            "Ветровки и куртки","Плащи и тренчкоты","Тренчи","Спортивные","Дубленки",
            "Широкие и расклешенные","Ветровки","Зимние пальто","Летние пальто",
            "Пальто меховые","Накидки и пончо"
        ],
        "Джемперы, свитеры, кардиганы": [
            "Водолазки", "Джемперы и пуловеры", "Жилеты", "Кардиганы", "Свитеры","Джемперы","Джемперы и кардиганы",
            "Джемперы, свитеры и кардиганы","Джемперы","Утепленные жилеты","Меховые жилеты",
            "Удлиненные жилеты","Утепленные","Кожаные жилеты","Джинсовые жилеты","Пончо, жилеты и накидки","Накидки"
        ],
        "Джинсы": [
            "Джеггинсы", "Прямые джинсы", "Узкие джинсы", "Широкие и расклешенные джинсы",
            "Зауженные джинсы","Зауженные джинсы","Джинсы","Зауженные","Классические",
            "Широкие джинсы","Расклешенные джинсы","Джинсы-бойфренды","Джинсы-мом"
        ],
        "Домашняя одежда": [
            "Комбинезоны", "Комплекты",
            "Маски для сна", "Ночные сорочки", "Пижамы",
            "Халаты","Хлопковые халаты","Махровые халаты","Домашняя одежда",
            "Бархатные халаты","Атласные и кружевные халаты","Пижамы с брюками",
            "Пижамы с шортами","Трикотажные халаты","Флисовые халаты"

        ],
        "Комбинезоны": [
            "Джинсовые комбинезоны", "Кигуруми", "Комбинезоны с брюками",
            "Комбинезоны с шортами", "Спортивные комбинезоны","Вечерние комбинезоны", "Комбинезоны джинсовые",
            "Брюки и комбинезоны"
        ],
        "Купальники и пляжная одежда": [
            "Лифы", "Парео", "Плавки", "Пляжные платья и туники",
            "Раздельные купальники", "Слитные купальники и монокини","Плавки и шорты для плавания",
            "Шорты для плавания","Слитные купальники","Купальники и пляжная одежда","Купальники-халтер",
            "Плавки с завышенной талией","Купальники и парео","Спортивные купальники","Купальники-бралетт",
            "Плавки-бразилиана","Плавки на завязках","Монокини","Купальники-бандо","Купальники",
            "Пляжная одежда"
        ],
        "Нижнее белье": [
            "Аксессуары", "Бюстгальтеры", "Комбинации", "Комплекты",
            "Корректирующее белье", "Корсеты", "Пояса для чулок", "Термобелье",
            "Трусы", "Эротическое белье","Брифы","Трусы-шорты","Боксеры","Бралетт",
            "Нижнее белье","Стринги","Верх","Низ","Бесшовные","Бесшовные трусы",
            "Трусы-бразилиана","Слипы","Корректирующее","Комплекты трусов",
            "Эротическое","Балконет","Лифы-бралетт","С треугольными чашечками","Слитные","Бандо",
            "Лифы-бандо", "Лифы-халтер","Бандажи"
        ],
        "Носки, чулки, колготки": [
            "Гольфы и гетры", "Колготки", "Короткие носки", "Носки",
            "Подследники", "Чулки","Кальсоны","Носки и гетры","Носки и колготки",
            "Гетры"
        ],
        "Пиджаки и костюмы": [
            "Жакеты", "Кимоно", "Костюмы с брюками",
            "Костюмы с шортами", "Костюмы с юбкой", "Пиджаки",
            "Костюмы","Классические костюмы","Спортивные костюмы","Пиджаки и костюмы","Жакеты и пиджаки",
            "Костюмы и комбинезоны","Костюмы и жакеты"

        ],
        "Платья и сарафаны": [
            "Вечерние платья", "Джинсовые платья", "Кожаные платья",
            "Платья с запахом", "Платья со спущенными плечами", "Повседневные платья",
            "Сарафаны", "Свадебные платья","Платья","Платья-рубашки","Трикотажные платья",
            "Платья-комбинации","Платья-футляр","Платья-пиджаки","Платья-футболки",
            "Платья-майки","Платья и сарафаны","Платья и туники","Кружевные платья"
        ],
        "Топы и майки": [
            "Вязаные топы", "Корсеты", "Майки", "Спортивные майки",
            "Спортивные топы", "Топы в бельевом стиле", "Топы на бретелях",
            "Топы с баской", "Топы свободного кроя", "Топы со спущенными плечами","Топы",
            "Топы и майки","Боди с коротким рукавом","Боди","Боди c длинным рукавом",
            "Кроп-топы","Спортивные топы и майки","Майки и топы"
        ],
        "Футболки и поло": [
            "Комплекты", "Лонгсливы", "Поло", "Спортивные футболки и лонгсливы", "Футболки","Туники","Футболки и майки",
            "Поло с коротким рукавом","Футболки и поло","Футболки с коротким рукавом","Футболки и лонгсливы",
            "Спортивные футболки","Спортивные лонгсливы","Рашгарды"
        ],
        "Худи и свитшоты": [
            "Олимпийки", "Свитшоты", "Толстовки", "Флиски", "Худи","Толстовки и свитшоты","Поло с длинным рукавом",
            "Худи и свитшоты","Олимпийки и толстовки","Платья-толстовки","Пуловеры"
        ],
        "Шорты": [
            "Бермуды", "Велосипедки", "Джинсовые шорты", "Карго",
            "Повседневные шорты", "Спортивные шорты","Шорты","Шортики",
            "Кожаные шорты"
        ],
        "Юбки": [
            "Джинсовые юбки", "Кожаные юбки", "Плиссированные юбки",
            "Прямые юбки", "Узкие юбки","Юбки","Юбки-трапеции и широкие",
            "Юбки-шорты","Юбки и парео"
        ],
        "Прочее": ["Уход за одеждой","Шнурки","Уход за обувью","Экипировка","Спортивный инвентарь"],
        "Балетки": [
            "Балетки с квадратным носом", "Балетки с круглым носом", "Балетки с острым носом"
        ],
        "Ботильоны": [
            "Ботильоны с квадратным носом", "Ботильоны с круглым носом",
            "Ботильоны с острым носом", "Ботильоны с открытым носом",
            "Высокие ботильоны", "Низкие ботильоны","Ботильоны"
        ],
        "Ботинки": [
            "Высокие ботинки", "Мартинсы и др.", "Низкие ботинки",
            "Оксфорды и дерби", "Тимберленды и др.", "Трекинговые ботинки", "Челси",
            "Казаки","Дезерты","Ботинки","Обувь"
        ],
        "Вечерняя обувь": [
            "Свадебные туфли", "Туфли с застежкой на лодыжке",
            "Туфли с открытой пяткой", "Туфли с открытой стопой", "Туфли с открытым носом",
            "Вечерняя обувь"
        ],
        "Домашняя обувь": ["Сланцы","Домашняя обувь"],
        "Кроссовки и кеды": [
            "Кеды", "Высокие кеды", "Низкие кеды",
            "Кроссовки", "Высокие кроссовки", "Низкие кроссовки", "Бутсы"
        ],
        "Мокасины и топсайдеры": ["Мокасины","Топсайдеры","Мокасины и топсайдеры"],
        "Обувь с увеличенной полнотой": ["Обувь с увеличенной полнотой"],
        "Резиновая обувь": ["Галоши", "Джиббитсы","Акваобувь","Резиновая обувь","Кроксы и др."],
        "Сабо и мюли": ["Сабо и мюли","Сабо", "Мюли"],
        "Сандалии": [
            "Эспадрильи","Сланцы","Повседневные сандалии","Спортивные сандалии",
            "Сандалии","Сандалии на завязках"
        ],
        "Сапоги": [
            "Ботфорты", "Валенки", "Дутики", "Полусапоги", "Сапоги",
            "Угги и унты","Сапоги-чулки","Сапоги-трубы"
        ],
        "Слипоны": ["Высокие слипоны", "Низкие слипоны","Слипоны"],
        "Туфли": [
            "Закрытые туфли", "Лодочки", "Лоферы", "Туфли Мэри Джейн",
            "Босоножки","Монки","Оксфорды","Дерби","Туфли","Туфли с открытыми боками"
        ]
    }


def count_and_extract_text_by_class(html, target_class):
    # Парсим HTML с помощью BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Находим все элементы с указанным классом
    elements_with_class = soup.find_all(class_=target_class)

    # Подсчитываем количество элементов
    count = len(elements_with_class)

    # Извлекаем текстовое содержимое элементов
    texts = [element.get_text(strip=True) for element in elements_with_class]

    # Вывод результата
    print(f"Количество элементов с классом '{target_class}': {count}")
    print("Тексты этих элементов:")
    for text in texts:
        print(f"- {text}")

    return count, texts


def get_category_for_subcategory(subcategory):
    """
    Функция для поиска категории по подкатегории.
    Возвращает категорию (ключ) из словаря, если подкатегория найдена.
    """
    for category, subcategories in categories_constants.items():
        if subcategory in subcategories:
            return category
    return "Не указано"  # Если подкатегория не найдена, возвращаем "Не указано"


def save_dict_to_json(data_dict, file_name):
    """
    Преобразует словарь в JSON и сохраняет его в файл.

    Args:
        data_dict (dict): Словарь для сохранения.
        file_name (str): Имя файла, в который будет сохранен JSON.

    Returns:
        str: Сообщение о результате сохранения.
    """
    try:
        with open(file_name, 'w', encoding='utf-8') as json_file:
            json.dump(data_dict, json_file, indent=4, ensure_ascii=False)
        return f"JSON-файл успешно сохранен как '{file_name}'."
    except Exception as e:
        return f"Ошибка при сохранении JSON-файла: {e}"

# Пример использования функции
subcategory = "Блузы"  # пример подкатегории
category = get_category_for_subcategory(subcategory)
print(category)
save_dict_to_json(categories_constants,"constant.json")
scraper = LamodaScraper()
print(scraper.fetch_page("https://www.lamoda.ru/p/mp002xw173k4/clothes-ostin-zhaket/"))
