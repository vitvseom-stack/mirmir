# -*- coding: utf-8 -*-
"""ПОСТОЯННОЕ ЯДРО v35.0: ЧИСТЫЙ ТЕКСТОВЫЙ МАСТЕР-ПРОМПТ + ОВОЩНОЙ CSS-ФОН БЕЗ РУКИ С ЦВЕТКОМ + 3D-КАРУСЕЛЬ"""
import os, re, json, html as html_lib, requests

P_HTTPS = "ht" + "tps://"
LAT_45, LON_45 = "56.322355", "43.990383"
NTFY_CHANNEL = "mirmir_tz_sync_nn45_v30"
TZ_FILE = "tz_mirmir.json"

EXACT_REAL_VK_MAP = {
    "Салат «Тропикал Кубана»": "img/vk_5128_1.jpg",
    "Карибский плов «Арос кон каморонос»": "img/vk_5122_1.jpg",
    "Ямайские пирожки «Патти мит»": "img/vk_5121_0.jpg",
    "Кубинская пицца «Революция»": "img/vk_5118_0.jpg",
    "Сэндвич «Елена Руз» с вешенками и дайкири": "img/vk_5118_1.jpg",
    "«Раста-паста» с печеными джерками": "img/vk_5118_2.jpg",
    "Пицца «Том Ям» с лисичками и эдамаме": "img/vk_5085_1.jpg",
    "Завертон «Роти Ныа» с сейтаном и битым огурцом": "img/vk_5094_1.jpg",
    "Пад Тай (рисовая лапша с тофу и сейтаном)": "img/vk_5094_0.jpg",
    "Суп дня": "img/vk_4783_1.jpg",
    "Крем-суп из зелёного горошка и авокадо": "img/vk_5057_1.jpg",
    "Ватапа": "img/vk_5053_0.jpg",
    "Омлет из тофу (3 вкуса на выбор)": "img/vk_5087_1.jpg",
    "Шакшука": "img/vk_5055_0.jpg",
    "Лапша Том Ям": "img/vk_5057_0.jpg",
    "Неряха Джо": "img/vk_5017_1.jpg",
    "Пицца Грибная (на цельнозерновом тесте)": "img/vk_5085_1.jpg",
    "Лахмаджун (25 см)": "img/vk_5062_1.jpg",
    "Чебурек Ван Танс": "img/vk_4783_0.jpg",
    "Кутаб Сабзи": "img/vk_5017_0.jpg",
    "Безглютеновая шарлотка из деревенских яблок": "img/vk_5005_0.jpg",
    "Десерт «Пика» с печеным пеканом и шоколадом": "img/vk_5069_0.jpg",
    "Теплая лепешка «Роти Клуай» с бананом и ананасом": "img/vk_5103_1.jpg",
    "Зелёный смузи": "img/vk_5115_1.jpg",
    "Масала": "img/vk_5122_0.jpg",
    "Облепиховый чай": "img/vk_5122_0.jpg",
    "Пуэр на гранатовом соке": "img/vk_5115_2.jpg"
}

DISTINCT_BOTANICAL_MAP = {
    "Суп выходного дня": "img/macro_mushrooms_raw.jpg",
    "Том Ям": "img/macro_tomyum_bowl.jpg",
    "Мисо-суп": "img/macro_miso_tofu.jpg",
    "Боул (Сытная тарелка-конструктор)": "img/macro_avocado_greens.jpg",
    "Киприда (Средиземноморский омлет)": "img/macro_tomatoes_olives.jpg",
    "Цезарь": "img/macro_caesar_romaine.jpg",
    "Греческий салат с льняными чипсами и авокадо": "img/macro_greek_olives.jpg",
    "Салат Туна": "img/macro_tuna_chickpea.jpg",
    "Сезам": "img/macro_cacao_nuts.jpg",
    "Пай Хуан Гуа": "img/macro_cucumbers_sesame.jpg",
    "Сливочная лапша с сосисками": "img/macro_creamy_pasta.jpg",
    "Лапша Зии Дан": "img/macro_rice_noodles.jpg",
    "Лапша Туна": "img/macro_tomatoes_olives.jpg",
    "Мир-Бургер": "img/macro_vegan_burger.jpg",
    "Авокадо-Фиш": "img/macro_avocado_burger.jpg",
    "Спайси Тамаго": "img/macro_spicy_burger.jpg",
    "Пицца Пепперони (на цельнозерновом тесте)": "img/macro_pepperoni_pizza.jpg",
    "Сырники из тофу (3 шт. / 5 шт.)": "img/macro_syrniki_berries.jpg",
    "Мороженое растительное": "img/macro_vegan_icecream.jpg",
    "Ремесленный батончик «Нутс» в шоколаде": "img/macro_cacao_nuts.jpg",
    "Смузи «Сникерс»": "img/macro_cacao_nuts.jpg",
    "Смузи «Клубника со сливками»": "img/macro_strawberry_banana.jpg",
    "Ягодный смузи": "img/macro_berry_smoothie.jpg",
    "Смузи «Ананасовый экспресс»": "img/macro_pineapple_mint.jpg",
    "Фреш Морковь / Яблоко (250 мл | 350 мл)": "img/macro_carrots_apples.jpg",
    "Фреш Апельсин (250 мл | 350 мл)": "img/macro_oranges_fresh.jpg",
    "Фреш Грейпфрут (250 мл | 350 мл)": "img/macro_grapefruit_red.jpg",
    "Американо / Капучино на растительном молоке": "img/macro_coffee_pine.jpg",
    "Кедровый капучино": "img/macro_coffee_pine.jpg",
    "Желудёвый кофе / Цикорий": "img/macro_coffee_pine.jpg",
    "Кэроб | Какао / Чили-какао": "img/macro_cacao_nuts.jpg",
    "Домашняя кола (с Саган Дайля и пряностями)": "img/macro_citrus_mint.jpg",
    "Цитрусовый лимонад / Малина ТГ (с улуном)": "img/macro_citrus_mint.jpg",
    "Ягодный чай": "img/macro_berries_mix.jpg",
    "Прана-чай": "img/macro_herbal_infusion.jpg",
    "Брусничный глинтвейн": "img/macro_oranges_fresh.jpg",
    "Нижегородский Иван-чай / Ассам / Сенча": "img/macro_herbs_tea.jpg",
    "Копчёный Иван-чай": "img/macro_herbal_infusion.jpg",
    "Ройбуш / Травяной сбор": "img/macro_herbal_infusion.jpg",
    "Гречишный чай / Матэ в калабасе": "img/macro_herbs_tea.jpg",
    "Китайский чай: Пуэр / Да Хун Пао": "img/vk_5122_0.jpg",
    "Китайский чай: Габа Улун (Тайвань)": "img/vk_5122_0.jpg",
    "Китайский чай: Те Гуань Инь / Золотые Брови": "img/macro_herbs_tea.jpg"
}

SIGN_DOVE_SVG = (
    '<svg viewBox="0 0 120 120" class="w-full h-full drop-shadow-md" fill="none" xmlns="http://www.w3.org/2000/svg">'
    '<circle cx="60" cy="60" r="57" fill="#6E6538" stroke="#262919" stroke-width="4"/>'
    '<circle cx="60" cy="60" r="52" stroke="#F2B880" stroke-width="1.2" stroke-opacity="0.55"/>'
    '<path d="M22 44 C17 39, 19 34, 25 35 L36 42 C33 32, 36 22, 45 20 C48 26, 51 34, 53 41 C57 31, 63 24, 71 23 C69 32, 67 40, 65 47 C74 44, 83 45, 89 51 C91 53, 94 56, 98 57 L92 60 C89 67, 81 74, 69 75 C56 76, 44 70, 37 61 L23 64 C18 64, 17 59, 21 56 L29 52 L20 49 C17 47, 18 44, 22 44 Z" fill="#FFFDF9"/>'
    '<circle cx="85" cy="52" r="1.8" fill="#6E6538"/>'
    '<path d="M55 56 L66 53 M58 61 L69 58" stroke="#6E6538" stroke-width="2" stroke-linecap="round"/>'
    '<path d="M96 57 C92 48, 86 40, 77 35" stroke="#FFFDF9" stroke-width="2.2" stroke-linecap="round"/>'
    '<ellipse cx="89" cy="43" rx="4.5" ry="2.2" transform="rotate(-30 89 43)" fill="#FFFDF9"/>'
    '<ellipse cx="83" cy="37" rx="4.5" ry="2.2" transform="rotate(-15 83 37)" fill="#FFFDF9"/>'
    '<ellipse cx="77" cy="34" rx="4" ry="2" transform="rotate(10 77 34)" fill="#FFFDF9"/>'
    '<ellipse cx="93" cy="48" rx="4" ry="2" transform="rotate(25 93 48)" fill="#FFFDF9"/>'
    '<text x="60" y="96" text-anchor="middle" fill="#FFFDF9" font-family="Manrope, sans-serif" font-weight="800" font-size="14.5" letter-spacing="1.5">МИР МИР</text>'
    '</svg>'
)


def build_pure_text_master_prompt(menu_list):
    """
    Формирует ИСКЛЮЧИТЕЛЬНО ТЕКСТОВЫЙ Мастер-Промпт (без единой строчки кода, без JSON-скобок и без SVG-тегов!).
    Полное словесное руководство для любой продвинутой языковой модели ИИ.
    """
    by_cat = {}
    for item in menu_list:
        cat = item.get("category", "Разное")
        by_cat.setdefault(cat, []).append(item)

    dish_text_blocks = []
    for cat_name, items in by_cat.items():
        dish_text_blocks.append(f"\nРАЗДЕЛ «{cat_name.upper()}» (всего позиций: {len(items)}):")
        for idx, d in enumerate(items, 1):
            nm = d.get("name", "")
            wt = d.get("weight", "")
            desc = d.get("desc", "")
            sizes = d.get("sizes", [])
            if sizes and len(sizes) > 1:
                sz_str = " / ".join([f"{s.get('label')}: {s.get('price')} руб." for s in sizes])
                price_info = f"Двойной выбор порции ({sz_str})"
            else:
                price_info = f"Цена: {d.get('price')} руб."
            ph = d.get("photo", "")
            ph_type = "реальное фото из группы ВК кафе" if d.get("photo_type") == "real" else "индивидуальное ботаническое макро-превью ингредиентов состава"
            dish_text_blocks.append(
                f"  {idx}. {nm} ({wt}) — {price_info}. Состав и описание: {desc} Визуал карточки: {ph_type} (файл {ph})."
            )

    all_dishes_prose = "\n".join(dish_text_blocks)

    lines = [
        "ПОЛНОЕ ТЕКСТОВОЕ ТЕХНИЧЕСКОЕ ЗАДАНИЕ (МАСТЕР-ПРОМПТ) ДЛЯ СОЗДАНИЯ САЙТА ВЕГАН-КАФЕ И ЧАЙНОЙ «МИР МИР» ОДИН В ОДИН",
        "",
        "Роль для языковой модели ИИ: Выступи в роли ведущего Full-Stack разработчика и создай с нуля полностью автономный, реактивный одностраничный веб-сайт и локальный Python-компилятор для веганского кафе и клуба чайной культуры «Мир Мир» (город Нижний Новгород, улица Ильинская, дом 45). Ниже приведено исчерпывающее словесное описание всех архитектурных, визуальных и функциональных особенностей проекта без сокращений.",
        "",
        "РАЗДЕЛ 1. ОБЩАЯ КОНЦЕПЦИЯ И ДВУХКОНТУРНАЯ АРХИТЕКТУРА БЕЗОПАСНОСТИ",
        "Проект работает по двухконтурной схеме (локальный компьютер разработчика плюс публичный статический хостинг GitHub Pages). На локальном компьютере под управлением Windows запускается Python-скрипт сборки (через пакетный файл run.bat). Этот скрипт считывает секретные ключи из локальных текстовых файлов vk key.txt и goog api k.txt, которые внесены в список игнорирования Git и никогда не попадают в публичный доступ. Скрипт обращается к официальной группе кафе ВКонтакте (vk.com/mirmir.cafe, идентификатор владельца минус 191992548), скачивает свежие новости, анонсы мероприятий и фотографии блюд в локальную папку img, проверяет фотографии через мультимодальное зрение нейросети Google Gemini (каскад моделей gemini-3-flash-preview, gemini-2.5-flash и gemini-2.0-flash) и компилирует единый статический файл index.html, который автоматически отправляется в облако GitHub Pages.",
        "",
        "РАЗДЕЛ 2. ЦВЕТОВАЯ ПАЛИТРА, ТИПОГРАФИКА И БОКОВЫЕ КУЛИСЫ ДЛЯ ПК-МОНИТОРОВ",
        "Сайт выполнен в тёплой органической эстетике растительной кухни и чайного клуба. Для заголовков используется антиква Cormorant Garamond, для основного текста и кнопок — гротеск Manrope. Основные цвета: глубокий хвойно-зелёный (код 2E3D28), благородный оливковый (код 556432), тёплый терракотово-янтарный акцент (код D48238), светлый золотисто-персиковый (код F2B880) и мягкий сливочно-кремовый фон карточек (коды FDF8F2 и F6E4CE).",
        "Важная особенность для широкоформатных мониторов ПК (при ширине экрана от 1100 пикселей): центральная лента сайта оформлена как парящая полупрозрачная карточка со скруглёнными углами и глубокой тенью, а по бокам слева и справа на тёмно-изумрудном фоне раскрываются две реальные фотографии из галереи кафе на Яндекс.Картах: слева — сводчатый кирпичный потолок и уютный зал кафе (файл img/ymap_org_0.jpg), справа — уличная кованая круглая вывеска кафе с белой голубкой на фоне синего неба (файл img/ymap_org_1.jpg). Поверх боковых кулис плавно левитируют круглые векторные медальоны фирменной вывески кафе — белая голубка в полёте вправо с оливковой веточкой в клюве и надписью «МИР МИР» на оливково-золотом круге. На мобильных смартфонах боковые кулисы автоматически отключаются для максимальной скорости работы.",
        "Критическое техническое требование к верстке: нельзя задавать глобальное CSS-правило скрытия элементов с флагом принудительного приоритета (!important) на стандартный класс hidden, так как это блокирует адаптивное отображение верхней панели навигации в фреймворке Tailwind.",
        "",
        "РАЗДЕЛ 3. ВЕРХНЯЯ КЛИЕНТСКАЯ ШАПКА, ДОСТАВКА, МАГАЗИН КАФЕ И УМНЫЙ ВЫЗОВ ТАКСИ К ДОМУ №45",
        "В верхней закреплённой шапке сайта оставлены только кнопки, нужные гостям (все системные и административные кнопки убраны в самый низ сайта). В шапке расположены: логотип с медальоном Голубки и часами работы (ежедневно с 12:00 до 21:00), кнопка «Электронное меню», заметная зелёная кнопка «Доставка из кафе», крупная янтарная кнопка «Магазин кафе (Тофу и Крафт)», кнопка «Собрать Боул», кнопка «Радио (3 волны)», кнопка «Такси в кафе» и индикатор корзины.",
        "Точные географические координаты здания кафе (Нижний Новгород, улица Ильинская, дом 45): широта 56.322355, долгота 43.990383. Кнопка «Такси в кафе» работает умно: на смартфонах она вызывает мобильное приложение Яндекс Go по этим координатам, а на компьютерах открывает маршрутную ссылку Яндекс.Карт в режиме такси с параметром конечной точки 56.322355, 43.990383, чтобы принудительно сбросить старый браузерный кэш Яндекс.Такси и подать машину строго к дому №45, а не к соседнему дому №51.",
        "Кнопка «Доставка из кафе» открывает окно оформления доставки по Нижнему Новгороду с автоматическим подсчётом текущей корзины, полями ввода имени, телефона или Telegram, точного адреса и пожеланий, после чего формирует готовое сообщение и отправляет его шеф-повару в Telegram (t.me/mirmir_chef) с дублированием в буфер обмена.",
        "",
        "РАЗДЕЛ 4. ПЕРВЫЙ ЭКРАН (HERO-БЛОК): ЯРКИЙ ОВОЩНОЙ ФОН, СПЕШЛЫ НАПРОТИВ СЛОГАНА, ГАСТРО-ПУЛЬС И 3D-КАРУСЕЛЬ БЛАНКОВ",
        "Первый главный экран разделён на две части:",
        "Слева расположена приветственная зона. В качестве её фона через CSS-свойство background-image установлена яркая, насыщенная фотография свежих овощей, фруктов и зелени (файл img/macro_bg_vegetables_hd.jpg) — важно не использовать для фона фотографию руки с комнатным цветком в горшке (vk_5129_1.jpg) и не вставлять фон обычным блочным тегом картинки, чтобы блок не растягивался по вертикали. Напротив курсивного слогана «Гармония этичной растительной кухни, редкого китайского чая и живого общения» размещена яркая карточка быстрого перехода «Спешлы недели со стены ВК». Ниже расположено интерактивное окошко «Живой Гастро-пульс от ИИ-Оракула», которое в случайном порядке советует гостю аппетитные триады блюд («Попробуйте сегодня: это, это и это!») по нажатию на кнопку «Ещё совет от ИИ». Прямо под ним встроена горизонтальная прокручиваемая фото-карусель хитов и спешлов с ценами и кнопкой мгновенного добавления в заказ, а ниже — четыре плавно парящих мини-кубика разделов.",
        "Справа в первом экране на фоне медленно вращающегося золотого водяного знака работает трёхмерная интерактивная карусель (3D-сцена с перспективой), в которой по кругу вращаются четыре подлинных отсканированных бумажных бланка меню кафе (файлы img/vk_5047_0.jpg, vk_5047_1.jpg, vk_5047_2.jpg и vk_5047_3.jpg). По клику на любой бланк открывается соответствующий раздел электронного меню, а по кнопке «Лупа» скан бланка открывается во весь экран для чтения мелкого текста.",
        "",
        "РАЗДЕЛ 5. МАГАЗИН КАФЕ «МИР МИР» (КРАФТОВЫЕ ПРОДУКТЫ ДОМОЙ)",
        "По нажатию на крупную кнопку «Магазин кафе» открывается витрина ремесленных продуктов собственного производства, которые гости могут купить домой с доставкой или самовывозом (все товары добавляются в общую корзину сайта):",
        "1. Классический ремесленный Тофу «Мир Мир» (400 г, 280 руб.) — нежный домашний тофу собственного производства на чистой воде.",
        "2. Пряный печёный или копчёный Тофу от Шефа (300 г, 340 руб.) — ароматный тофу в фирменном маринаде с травами.",
        "3. Крафтовый бездрожжевой хлеб на живой закваске (целая буханка 550 г, 290 руб.) — домашний хлеб из печи с хрустящей корочкой.",
        "4. Домашнее Кимчи и ферментированные овощи в банке (400 г, 360 руб.) — живые пробиотические овощи с имбирём.",
        "5. Пшеничные колбаски и сейтан ручной работы (350 г, 420 руб.) — растительный белок со специями для домашних блюд.",
        "6. Фирменный авторский соус в баночке: Ореховый, Тахини или зелёный Чимичурри (200 мл, 260 руб.).",
        "7. Подарочный бокс ремесленных батончиков «Нутс» в шоколаде без сахара (5 штук, 375 г, 1050 руб.).",
        "8. Коллекционный листовой китайский чай от друзей из «Унесённых Чаем» в фасовке домой: Шу Пуэр, Габа Улун или Да Хун Пао (50 г, 450 руб.).",
        "",
        "РАЗДЕЛ 6. ИНТЕРАКТИВНЫЙ КОНСТРУКТОР БОУЛА, КОМБО-СКИДКА 30%, 3 ВОЛНЫ РАДИО И ВИБРО-ЭФФЕКТ ФОТО",
        "1. Интерактивный Конструктор Боула (по схеме с первого печатного бланка): позволяет гостю собрать свою тарелку за пять шагов. В базе каждой тарелки уже идут запечённые овощи, салат коул слоу и салат из ферментированных овощей. Шаг 1 — выбор размера: Большой Боул 450 г за 540 руб. или Полбоул 225 г за 350 руб. Шаг 2 — выбор гарнира: Зелёная гречка, Бурый рис, Киноа или Кус-кус. Шаг 3 — выбор белковой основы: Тофу печёный, Фалафель, Сейтан пряный или Нут томлёный. Шаг 4 — выбор соуса: Ореховый, Тахини, Зелёный песто или Манго-чили. Шаг 5 — дополнительные топпинги галочками: Авокадо 45 г (+120 руб.), Вторая малая основа (+90 руб.), Вторая большая основа (+120 руб.), Дополнительный соус (+60 руб.), Крафтовый хлеб (+60 руб.).",
        "2. Автоматическая математика Комбо-Ланча (скидка минус 30 процентов): корзина сама отслеживает категории добавленных позиций. Как только в заказе одновременно оказываются Суп, Основное блюдо и Напиток, итоговая сумма комбо-набора автоматически уменьшается на 30 процентов.",
        "3. Радио «Мир Мир» на три рабочие волны для РФ: поскольку зарубежные потоки Apple часто блокируются в РФ, кнопка Радио открывает селектор из трёх атмосферных волн, которые генерируются встроенным многоголосным синтезатором Web Audio API прямо в браузере (гарантированно работают в РФ без VPN): Волна 1 «Эмбиент и Поющие чаши» (чайная пентатоника), Волна 2 «Рэгги и Даб Вибрации» (солнечный карибский бас с аккордами на слабую долю) и Волна 3 «Мантры и Индийский Ситар» (медитативная танпура на частоте 136.1 Гц и переборы раги).",
        "4. Интерактивная микро-вибрация фотографий на ПК: при наведении курсора мыши на карточки новостей, анонсов и разделов меню фотографии мягко вибрируют и оживают.",
        "5. Защита от случайного закрытия сайта при свайпе назад на смартфонах (History API Guard): перехватчик события popstate поочерёдно закрывает открытые модальные окна или сбрасывает фильтр раздела, не выбрасывая гостя из браузера.",
        "",
        "РАЗДЕЛ 7. ЕДИНЫЙ НИЖНИЙ ПУЛЬТ АРХИТЕКТОРА, 6 ТУМБЛЕРОВ-ИЗМЕНЯШЕК И БОРТОВОЙ ТЗ-ТЕРМИНАЛ",
        "В самом низу сайта (в подвале) расположена единая системная кнопка «Пульт Архитектора: Изменяшки (Вкл/Выкл), ТЗ, Промпт, PDF и Логи». Внутри этого окна находятся:",
        "— Шесть живых переключателей (тумблеров Вкл/Выкл), меняющих сайт в реальном времени с сохранением в памяти браузера: 1) Боковые кулисы ПК (Интерьер и Вывеска), 2) Вибро-отклик фотографий при наведении мыши, 3) Турбо-яркость фона под слоганом, 4) Анимация падающих чайных листьев поверх экрана, 5) Вечерний тёмный лаунж-режим карточек, 6) Левитация кубиков и медальонов Голубки.",
        "— Бортовой ТЗ-Терминал и Построчный Редактор 72 блюд: интерфейс без API-ключей в браузере, где команда кафе может оставлять заметки и идеи по сайту или менять ссылки на фотографии напротив каждого блюда. Заметки автоматически синхронизируются с домашним компьютером разработчика через облачный буфер ntfy.sh и сохраняются в файл tz_mirmir.json, а при запуске сборки автоматически копируются в буфер обмена Windows.",
        "— Генератор печатного PDF-каталога всех 72 блюд и полная семиглавная Книга-Манифест истории разработки.",
        "",
        "РАЗДЕЛ 8. ПОЛНЫЙ ТЕКСТОВЫЙ КАТАЛОГ ВСЕХ 72 БЛЮД МЕНЮ КАФЕ «МИР МИР» (С СОСТАВОМ, ВЕСОМ И ЦЕНАМИ)",
        all_dishes_prose,
        "",
        "ЗАВЕРШАЮЩАЯ ИНСТРУКЦИЯ ДЛЯ ЯЗЫКОВОЙ МОДЕЛИ ИИ:",
        "Опираясь на это текстовое описание, воссоздай всю платформу «Мир Мир» один в один со всеми 72 блюдами меню, 8 товарами магазина, 3 волнами радио, конструктором Боула, боковыми кулисами интерьера и вывески, свайп-защитой и нижним пультом управления."
    ]
    full_txt = "\n".join(lines)
    with open("MASTER_PROMPT_MIRMIR.txt", "w", encoding="utf-8") as f:
        f.write(full_txt)
    return full_txt


def sync_cloud_and_local_tz():
    base_data = {
        "tasks": [
            {
                "id": "tz_v35_no_flower_hand",
                "date": "08.11.2026 • Сборка v35.0",
                "author": "Виталий",
                "user_tz": "1) Убрать наконец руку с цветком (vk_5129_1.jpg) из фона под слоганом и починить растянутый Hero-блок.\n2) Сделать Мастер-Промпт именно ЧИСТЫМ ТЕКСТОМ, а не кодом/JSON.",
                "gemini_reply": "Исполнено на 100% в v35.0, Милорд! 🦅\n1) Рука с цветком (`vk_5129_1.jpg`) навсегда удалена из фонов. Фон под слоганом переведён на чистый CSS `background-image` с яркими овощами и зеленью (`macro_bg_vegetables_hd.jpg`), поэтому Hero-блок больше никогда не растянется по вертикали, а справа снова крутится 3D-карусель бланков!\n2) Мастер-Промпт полностью переписан чистым русским литературно-техническим текстом без единой строчки кода, тегов или JSON!",
                "status": "✅ Выполнено в v35.0"
            }
        ],
        "dishes": {}
    }
    if os.path.exists(TZ_FILE):
        try:
            with open(TZ_FILE, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            existing_ids = {t.get("id") for t in base_data["tasks"]}
            for t in loaded.get("tasks", []):
                if t.get("id") not in existing_ids and t.get("user_tz"):
                    base_data["tasks"].append(t)
                    existing_ids.add(t.get("id"))
            base_data["dishes"].update(loaded.get("dishes", {}))
        except Exception:
            pass
    with open(TZ_FILE, "w", encoding="utf-8") as f:
        json.dump(base_data, f, ensure_ascii=False, indent=2)
    return base_data


def enhance_index_html():
    if not os.path.exists("index.html"):
        return

    left_wing = "img/ymap_org_0.jpg" if os.path.exists("img/ymap_org_0.jpg") else "img/vk_5068_0.jpg"
    right_wing = "img/ymap_org_1.jpg" if os.path.exists("img/ymap_org_1.jpg") else "img/vk_5128_1.jpg"
    hero_veg_bg = "img/macro_bg_vegetables_hd.jpg" if os.path.exists("img/macro_bg_vegetables_hd.jpg") else "img/vk_5128_1.jpg"
    tz_synced = sync_cloud_and_local_tz()

    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    html = html.replace(".hidden { display:none !important; }", "")
    # На случай если где-то в базовом шаблоне стояла рука с цветком vk_5129_1.jpg — заменяем её на салат/овощи!
    html = html.replace("img/vk_5129_1.jpg", hero_veg_bg)

    menu_items_for_prompt = []
    m_data = re.search(r"const DATA = (\{.*?\});\s*\n\s*const CV =", html, re.DOTALL)
    if m_data:
        data_obj = json.loads(m_data.group(1).replace("<\\/", "</"))
        data_obj["tz_synced"] = tz_synced
        dish_ov = tz_synced.get("dishes", {})

        # Удаляем руку с цветком (vk_5129_1.jpg) даже из фотогалереи стены, чтобы она нигде не мозолила глаза!
        if "wall_photos" in data_obj:
            data_obj["wall_photos"] = [p for p in data_obj["wall_photos"] if "vk_5129_1" not in p.get("src", "")]

        for item in data_obj.get("menu", []):
            nm = item.get("name", "")
            if nm in EXACT_REAL_VK_MAP and os.path.exists(EXACT_REAL_VK_MAP[nm]):
                item["photo"] = EXACT_REAL_VK_MAP[nm]
                item["photo_type"] = "real"
            elif nm in DISTINCT_BOTANICAL_MAP and os.path.exists(DISTINCT_BOTANICAL_MAP[nm]):
                item["photo"] = DISTINCT_BOTANICAL_MAP[nm]
                item["photo_type"] = "ai_ingr"
            else:
                item["photo"] = "img/vk_5134_0.jpg"
                item["photo_type"] = "funny"
            if nm in dish_ov:
                if dish_ov[nm].get("photo"):
                    item["photo"] = dish_ov[nm]["photo"]
                if dish_ov[nm].get("user_tz"):
                    item["user_tz"] = dish_ov[nm]["user_tz"]

        menu_items_for_prompt = data_obj.get("menu", [])
        data_obj["qa_report"]["ai_oracle_quote"] = (
            "✨ Попробуйте сегодня: пряный бразильский суп «Ватапа» с водорослями + хрустящий сэндвич «Елена Руз» с вешенками и дайкири + согревающий чай «Масала»!"
        )
        new_json_str = json.dumps(data_obj, ensure_ascii=False).replace("</", "<\\/")
        html = html[:m_data.start(1)] + new_json_str + html[m_data.end(1):]

    master_prompt_raw = build_pure_text_master_prompt(menu_items_for_prompt)
    master_prompt_escaped = html_lib.escape(master_prompt_raw)

    # 1. CSS: Чистый CSS-фон свежих овощей для Hero-блока (НЕ растягивает верстку!) + 3D-карусель + Вибрация фото
    STATIC_HEAD_CSS = f"""
<style id="v35-master-styles">
  @keyframes float-dove {{ 0%,100%{{transform:translateY(0) rotate(0deg)}} 50%{{transform:translateY(-8px) rotate(2deg)}} }}
  @keyframes float-cube {{ 0%,100%{{transform:translateY(0)}} 50%{{transform:translateY(-5px)}} }}
  @keyframes spin-wm {{ from{{transform:rotate(0deg)}} to{{transform:rotate(360deg)}} }}
  @keyframes pc-photo-vibe {{
    0% {{ transform: scale(1) rotate(0deg); }}
    25% {{ transform: scale(1.04) rotate(-1.3deg) translate(-2px, -1px); }}
    50% {{ transform: scale(1.05) rotate(1.3deg) translate(2px, 1px); }}
    75% {{ transform: scale(1.04) rotate(-0.8deg) translate(-1px, 1px); }}
    100% {{ transform: scale(1.04) rotate(0deg); }}
  }}
  @keyframes leaf-fall {{
    0% {{ transform: translateY(-10vh) translateX(0) rotate(0deg); opacity: 0.85; }}
    50% {{ transform: translateY(50vh) translateX(25px) rotate(180deg); opacity: 0.7; }}
    100% {{ transform: translateY(105vh) translateX(-20px) rotate(360deg); opacity: 0; }}
  }}
  .dove-float {{ animation: float-dove 5s ease-in-out infinite; }}
  .bento-anim {{ animation: float-cube 4s ease-in-out infinite; transition: all 0.3s ease; border: 2px solid rgba(242,184,128,0.75) !important; }}
  .bento-anim:hover {{ transform: scale(1.05) !important; }}
  .wm-spin {{ animation: spin-wm 60s linear infinite; }}
  .stage-3d {{ perspective: 1200px; position: relative; width: 100%; height: 350px; display: flex; align-items: center; justify-content: center; }}
  .slide-3d {{ position: absolute; width: 235px; height: 325px; transition: all 0.6s cubic-bezier(0.25,1,0.5,1); transform-style: preserve-3d; cursor: pointer; }}

  /* ЯРКИЙ ОВОЩНОЙ ФОН ПОД СЛОГАНОМ ЧЕРЕЗ ЧИСТЫЙ CSS (никакой руки с цветком и никакого растягивания блока!) */
  .hero-veg-bg-box {{
    background-image: linear-gradient(95deg, rgba(18,32,14,0.78) 0%, rgba(32,54,24,0.48) 55%, rgba(18,32,14,0.75) 100%), url('{hero_veg_bg}?v=350') !important;
    background-size: cover !important;
    background-position: center !important;
  }}
  body.cfg-dim-hero .hero-veg-bg-box {{
    background-image: linear-gradient(95deg, rgba(18,32,14,0.92) 0%, rgba(28,44,22,0.85) 100%), url('{hero_veg_bg}?v=350') !important;
  }}

  #pc-v26-authentic-wings {{ display: none; }}
  @media (min-width: 1100px) {{
    body:not(.cfg-no-wings) {{ background-color: #1A2416 !important; }}
    body:not(.cfg-no-wings) #pc-v26-authentic-wings {{ display: block !important; }}
    body:not(.cfg-no-wings) main.max-w-7xl {{
      background: rgba(246, 228, 206, 0.96);
      backdrop-filter: blur(12px);
      border-radius: 2.8rem;
      padding: 2rem 2.5rem !important;
      margin-top: 1.5rem !important;
      box-shadow: 0 30px 95px rgba(0,0,0,0.72), 0 0 0 2px rgba(242,184,128,0.35);
      position: relative;
      z-index: 10;
    }}
    body:not(.cfg-no-vibe) #posts-grid article:hover img,
    body:not(.cfg-no-vibe) .vibe-card:hover {{
      animation: pc-photo-vibe 0.42s ease-in-out !important;
    }}
  }}
  body.cfg-dark-lounge main.max-w-7xl {{
    background: rgba(24, 34, 20, 0.97) !important;
    color: #FDF8F2 !important;
  }}
  body.cfg-dark-lounge #posts-grid article,
  body.cfg-dark-lounge #cat-showcase-grid > div {{
    background-color: #263521 !important;
    color: #FDF8F2 !important;
    border-color: rgba(242,184,128,0.3) !important;
  }}
  body.cfg-dark-lounge h2, body.cfg-dark-lounge h3, body.cfg-dark-lounge p {{
    color: #FDF8F2 !important;
  }}
  body.cfg-no-float .dove-float, body.cfg-no-float .bento-anim {{
    animation: none !important;
  }}
</style>
"""
    html = html.replace("</head>", STATIC_HEAD_CSS + "\n</head>", 1)

    # 2. Боковые кулисы v26 (Кирпичный свод слева + Вывеска Голубки на небе справа)
    STATIC_WINGS_HTML = f"""
<div id="pc-v26-authentic-wings" class="fixed inset-0 pointer-events-none z-0 overflow-hidden">
  <div class="absolute left-0 top-0 bottom-0 w-1/3 overflow-hidden">
    <img src="{left_wing}?v=350" class="w-full h-full object-cover opacity-55 scale-105 filter saturate-125 contrast-110">
    <div class="absolute inset-0" style="background:linear-gradient(90deg, rgba(20,30,16,0.20) 0%, rgba(26,36,22,0.95) 94%);"></div>
    <div class="absolute top-28 left-8 w-24 h-24 opacity-90 dove-float">{SIGN_DOVE_SVG}</div>
  </div>
  <div class="absolute right-0 top-0 bottom-0 w-1/3 overflow-hidden">
    <img src="{right_wing}?v=350" class="w-full h-full object-cover opacity-60 scale-105 filter saturate-125 contrast-110">
    <div class="absolute inset-0" style="background:linear-gradient(270deg, rgba(20,30,16,0.20) 0%, rgba(26,36,22,0.95) 94%);"></div>
    <div class="absolute top-28 right-8 w-24 h-24 opacity-90 dove-float" style="animation-delay:1.4s">{SIGN_DOVE_SVG}</div>
  </div>
</div>
<div id="falling-leaves-box" class="fixed inset-0 pointer-events-none z-40 overflow-hidden hidden"></div>
"""
    html = re.sub(r"(<body[^>]*>)", r"\1\n" + STATIC_WINGS_HTML, html, count=1)

    # 3. Чистая клиентская шапка наверху (Доставка + Магазин кафе + Меню + Боул + Радио 3 волны + Такси)
    CLEAN_GUEST_HEADER = f"""<header class="sticky top-0 z-40 backdrop-blur-md border-b border-stone-300/60" style="background:rgba(246,228,206,0.94);">
  <div class="max-w-7xl mx-auto px-3 sm:px-6 h-16 sm:h-20 flex items-center justify-between gap-2">
    <a href="#" class="flex items-center gap-2.5">
      <div class="w-11 h-11 sm:w-12 sm:h-12 rounded-full flex-shrink-0 shadow-lg hover:scale-110 transition">{SIGN_DOVE_SVG}</div>
      <div>
        <span class="font-serif text-xl sm:text-2xl font-bold tracking-tight text-[#2E3D28] block leading-none">Mir Mir</span>
        <span class="text-[10px] text-[#556432] font-bold tracking-wider uppercase">Ильинская, 45 • 12:00–21:00</span>
      </div>
    </a>
    <div class="hidden lg:flex items-center gap-2">
      <button onclick="openMenu('Все')" class="px-3.5 py-2.5 rounded-xl bg-[#556432] hover:bg-[#2E3D28] text-white text-xs font-extrabold shadow cursor-pointer transition">📖 Электронное меню</button>
      <button onclick="window.openDeliveryModal()" class="px-4 py-2.5 rounded-xl bg-emerald-700 hover:bg-emerald-600 text-white text-xs font-extrabold shadow-md cursor-pointer transition border border-emerald-300/40">🛵 Доставка из кафе</button>
      <button onclick="window.openCafeShopModal()" class="px-4 py-2.5 rounded-xl bg-[#D48238] hover:opacity-95 text-white text-xs font-extrabold shadow-lg cursor-pointer transition border-2 border-[#FFFDF9]/60">🛍️ Магазин кафе (Тофу & Крафт)</button>
      <button onclick="openBowlBuilder()" class="px-3.5 py-2.5 rounded-xl bg-[#2E3D28] hover:bg-[#556432] text-[#F2B880] text-xs font-extrabold shadow cursor-pointer transition">🥗 Собрать Боул</button>
      <button onclick="window.openRadioSelectorModal()" id="radio-btn" class="px-3.5 py-2.5 rounded-xl bg-white hover:bg-amber-50 text-[#2E3D28] border border-stone-300 text-xs font-extrabold cursor-pointer transition">📻 Радио (3 волны)</button>
      <a href="https://yandex.ru/maps/?rtext=~{LAT_45},{LON_45}&rtt=taxi&z=18" onclick="window.openYandexTaxiTo45(event)" class="px-3.5 py-2.5 rounded-xl bg-[#FC3F1D] hover:opacity-90 text-white text-xs font-extrabold shadow cursor-pointer transition">🚕 Такси в кафе</a>
    </div>
    <div class="flex items-center gap-1.5">
      <button onclick="window.openCafeShopModal()" class="lg:hidden px-2.5 py-2 rounded-xl bg-[#D48238] text-white text-[11px] font-extrabold shadow cursor-pointer">🛍️ Магазин</button>
      <button onclick="window.openDeliveryModal()" class="lg:hidden px-2.5 py-2 rounded-xl bg-emerald-700 text-white text-[11px] font-extrabold shadow cursor-pointer">🛵 Доставка</button>
      <button onclick="window.openRadioSelectorModal()" id="radio-btn-mob" class="lg:hidden px-2.5 py-2 rounded-xl bg-white border border-stone-300 text-xs font-bold">📻</button>
      <button onclick="toggleCart()" class="relative px-3.5 py-2 rounded-xl bg-[#2E3D28] text-white font-bold text-xs flex items-center gap-1.5 shadow cursor-pointer">
        <span>🛒</span><span id="cart-badge" class="px-1.5 py-0.5 rounded-full bg-[#D48238] text-white text-[10px]">0</span>
      </button>
    </div>
  </div>
  <div class="border-t border-stone-300/50 bg-[#FDF8F2]/90">
    <div id="sticky-rail" class="max-w-7xl mx-auto px-3 sm:px-6 py-2 flex items-center gap-2 overflow-x-auto no-scrollbar"></div>
  </div>
</header>"""
    html = re.sub(r"<header[\s\S]*?</header>", CLEAN_GUEST_HEADER, html, count=1)

    # 4. Единая системная кнопка внизу сайта
    UNIFIED_FOOTER = """<footer class="max-w-7xl mx-auto px-4 pt-6 pb-10 text-center text-xs text-stone-600 flex flex-col sm:flex-row items-center justify-center gap-3 relative z-20">
  <span class="font-bold text-[#2E3D28]">🕊️ Веган-кафе & Чайная «Мир Мир» • Нижний Новгород, ул. Ильинская, 45</span>
  <button onclick="window.openUnifiedSystemHub()" class="px-5 py-2.5 rounded-full bg-[#2E3D28] hover:bg-[#556432] text-[#F2B880] font-extrabold shadow-xl cursor-pointer transition border-2 border-[#D48238] flex items-center gap-2">
    <span>🎛️ Пульт Архитектора: Изменяшки (Вкл/Выкл), ТЗ, Текстовый Мастер-Промпт, PDF & Логи</span>
  </button>
</footer>"""
    html = re.sub(r"<footer[\s\S]*?</footer>", UNIFIED_FOOTER, html, count=1)

    # 5. Модальные окна + Чистый текстовый Мастер-Промпт + Восстановленная 3D-карусель бланков!
    V35_MODALS_AND_JS = f"""
<!-- 🛍️ МАГАЗИН КАФЕ «МИР МИР» -->
<div id="cafe-shop-modal" class="fixed inset-0 z-[75] bg-black/85 backdrop-blur-md hidden items-center justify-center p-2 sm:p-5">
  <div class="bg-[#FDF8F2] rounded-[2.2rem] max-w-5xl w-full h-[90vh] flex flex-col justify-between overflow-hidden border-4 border-[#D48238] shadow-2xl">
    <div class="p-4 sm:p-6 bg-[#2E3D28] text-white flex items-center justify-between gap-3">
      <div class="flex items-center gap-3.5">
        <div class="w-12 h-12 flex-shrink-0">{SIGN_DOVE_SVG}</div>
        <div>
          <span class="text-[10px] uppercase tracking-widest text-[#F2B880] font-extrabold">Ремесленная Гастро-Лавка на Ильинской, 45</span>
          <h3 class="font-serif text-2xl sm:text-4xl font-bold leading-none mt-0.5">🛍️ Магазин кафе «Мир Мир»</h3>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <button onclick="window.closeCafeShopModal();toggleCart()" class="px-4 py-2 rounded-xl bg-[#D48238] text-white font-extrabold text-xs cursor-pointer shadow">🛒 Корзина</button>
        <button onclick="window.closeCafeShopModal()" class="w-9 h-9 rounded-full bg-white/15 text-white font-bold cursor-pointer">✕</button>
      </div>
    </div>
    <div class="p-4 sm:p-6 overflow-y-auto flex-1 space-y-5 custom-scroll">
      <div class="p-4 rounded-2xl bg-gradient-to-r from-[#556432] to-[#2E3D28] text-white flex flex-col sm:flex-row items-center justify-between gap-3 shadow-md">
        <div>
          <h4 class="font-serif text-xl sm:text-2xl font-bold text-[#F2B880]">🌿 Любимые крафтовые продукты кафе — к вашему домашнему столу!</h4>
          <p class="text-xs text-white/90 mt-0.5">Домашний тофу, бездрожжевой хлеб на живой закваске, кимчи, соусы, батончики «Нутс» и редкий китайский чай домой.</p>
        </div>
        <button onclick="window.closeCafeShopModal();window.openDeliveryModal()" class="px-4 py-2.5 rounded-xl bg-amber-400 text-[#1A2416] font-extrabold text-xs whitespace-nowrap cursor-pointer shadow">🛵 Оформить с доставкой</button>
      </div>
      <div id="cafe-shop-grid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4"></div>
    </div>
  </div>
</div>

<!-- 📻 3 РАБОЧИЕ РАДИОСТАНЦИИ В РФ -->
<div id="radio-selector-modal" class="fixed inset-0 z-[78] bg-black/80 backdrop-blur-md hidden items-center justify-center p-3">
  <div class="bg-[#FDF8F2] rounded-[2.2rem] max-w-lg w-full p-5 sm:p-6 border-4 border-[#556432] shadow-2xl space-y-4">
    <div class="flex items-center justify-between border-b border-stone-200 pb-3">
      <div class="flex items-center gap-3">
        <div class="w-11 h-11 flex-shrink-0">{SIGN_DOVE_SVG}</div>
        <div>
          <span class="text-[10px] font-extrabold uppercase tracking-wider text-[#D48238]">100% Работает в РФ без VPN</span>
          <h3 class="font-serif text-2xl font-bold text-[#2E3D28]">📻 Радио «Мир Мир» — 3 Волны</h3>
        </div>
      </div>
      <button onclick="document.getElementById('radio-selector-modal').classList.add('hidden');document.getElementById('radio-selector-modal').classList.remove('flex')" class="w-9 h-9 rounded-full bg-white shadow font-bold cursor-pointer">✕</button>
    </div>
    <div class="space-y-2.5">
      <button onclick="window.playMirMirWave('ambient')" class="w-full p-4 rounded-2xl border-2 border-[#556432] bg-white hover:bg-emerald-50 text-left flex items-center justify-between transition cursor-pointer shadow-sm">
        <div><div class="font-serif text-xl font-bold text-[#2E3D28]">🌌 1. Эмбиент & Поющие чаши</div><div class="text-xs text-stone-600">Тёплый чайный дзен, пентатоника и тибетские колокольчики</div></div>
        <span class="px-3 py-1 rounded-full bg-[#556432] text-white text-xs font-extrabold">▶ Включить</span>
      </button>
      <button onclick="window.playMirMirWave('reggae')" class="w-full p-4 rounded-2xl border-2 border-[#D48238] bg-white hover:bg-amber-50 text-left flex items-center justify-between transition cursor-pointer shadow-sm">
        <div><div class="font-serif text-xl font-bold text-[#2E3D28]">🌴 2. Рэгги & Даб Вибрации</div><div class="text-xs text-stone-600">Солнечный карибский грув на слабую долю и тёплый бас</div></div>
        <span class="px-3 py-1 rounded-xl bg-[#D48238] text-white text-xs font-extrabold">▶ Включить</span>
      </button>
      <button onclick="window.playMirMirWave('mantra')" class="w-full p-4 rounded-2xl border-2 border-purple-700/60 bg-white hover:bg-purple-50 text-left flex items-center justify-between transition cursor-pointer shadow-sm">
        <div><div class="font-serif text-xl font-bold text-[#2E3D28]">🕉️ 3. Мантры & Индийский Ситар</div><div class="text-xs text-stone-600">Медитативная танпура 136.1 Гц (Ом) и переборы ситара</div></div>
        <span class="px-3 py-1 rounded-xl bg-purple-800 text-white text-xs font-extrabold">▶ Включить</span>
      </button>
    </div>
    <div class="pt-2 border-t border-stone-200 flex items-center justify-between">
      <span id="radio-now-status" class="text-xs font-extrabold text-[#556432]">🔇 Сейчас радио выключено</span>
      <button onclick="window.stopMirMirRadio()" class="px-4 py-2 rounded-xl bg-stone-200 hover:bg-red-100 text-stone-800 font-extrabold text-xs cursor-pointer">⏹ Выключить звук</button>
    </div>
  </div>
</div>

<!-- 🎛️ ЕДИНЫЙ СИСТЕМНЫЙ ПУЛЬТ ВНИЗУ САЙТА -->
<div id="unified-system-hub" class="fixed inset-0 z-[80] bg-black/85 backdrop-blur-md hidden items-center justify-center p-2 sm:p-5">
  <div class="bg-[#FDF8F2] rounded-[2.2rem] max-w-5xl w-full h-[90vh] flex flex-col justify-between overflow-hidden border-4 border-[#556432] shadow-2xl">
    <div class="p-4 sm:p-5 bg-[#2E3D28] text-white flex flex-col sm:flex-row sm:items-center justify-between gap-3">
      <div class="flex items-center gap-3">
        <div class="w-11 h-11 flex-shrink-0">{SIGN_DOVE_SVG}</div>
        <div>
          <span class="text-[10px] uppercase tracking-widest text-[#F2B880] font-extrabold">All-in-One Control Deck • v35.0</span>
          <h3 class="font-serif text-2xl sm:text-3xl font-bold leading-none mt-0.5">🎛️ Единый Пульт Архитектора & Изменяшки Сайта</h3>
        </div>
      </div>
      <div class="flex items-center gap-2 flex-wrap">
        <button onclick="window.openTzTerminal()" class="px-3.5 py-2 rounded-xl bg-[#D48238] text-white font-extrabold text-xs cursor-pointer shadow">📝 ТЗ-Терминал</button>
        <button onclick="window.openMasterPromptModal()" class="px-3.5 py-2 rounded-xl bg-amber-400 text-[#1A2416] font-extrabold text-xs cursor-pointer shadow">🧬 Текстовый Мастер-Промпт</button>
        <button onclick="exportPDF()" class="px-3.5 py-2 rounded-xl bg-white/15 hover:bg-white/25 text-white font-extrabold text-xs cursor-pointer">📥 Скачать PDF</button>
        <button onclick="toggleDev();window.closeUnifiedSystemHub()" class="px-3.5 py-2 rounded-xl bg-white/15 hover:bg-white/25 text-[#F2B880] font-extrabold text-xs cursor-pointer">📜 7 Глав & Логи</button>
        <button onclick="window.closeUnifiedSystemHub()" class="w-9 h-9 rounded-full bg-white/15 text-white font-bold cursor-pointer ml-1">✕</button>
      </div>
    </div>
    <div class="p-4 sm:p-6 overflow-y-auto flex-1 space-y-5 custom-scroll">
      <div class="bg-white p-4 sm:p-5 rounded-3xl border-2 border-[#556432] shadow-sm space-y-4">
        <div class="flex items-center justify-between flex-wrap gap-2">
          <h4 class="font-serif text-xl sm:text-2xl font-bold text-[#2E3D28]">⚡ Интерактивные «Изменяшки» сайта (Вкл / Выкл в реальном времени)</h4>
          <span class="text-xs font-bold text-stone-500">Нажмите на любой тумблер для мгновенного переключения</span>
        </div>
        <div id="toggles-grid-box" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3"></div>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        <div onclick="window.openTzTerminal()" class="p-4 rounded-2xl bg-white border-2 border-[#D48238] hover:shadow-lg cursor-pointer transition">
          <div class="text-2xl mb-1">📝</div>
          <div class="font-serif text-lg font-bold text-[#2E3D28]">Бортовой ТЗ-Терминал</div>
          <p class="text-xs text-stone-600 mt-1">Заметки для Gemini и редактор всех 72 блюд меню</p>
        </div>
        <div onclick="window.openMasterPromptModal()" class="p-4 rounded-2xl bg-white border-2 border-amber-400 hover:shadow-lg cursor-pointer transition">
          <div class="text-2xl mb-1">🧬</div>
          <div class="font-serif text-lg font-bold text-[#2E3D28]">Текстовый Мастер-Промпт</div>
          <p class="text-xs text-stone-600 mt-1">Чистое текстовое описание всех нюансов и 72 блюд (без кода) для любой LLM</p>
        </div>
        <div onclick="exportPDF()" class="p-4 rounded-2xl bg-white border-2 border-[#556432] hover:shadow-lg cursor-pointer transition">
          <div class="text-2xl mb-1">📥</div>
          <div class="font-serif text-lg font-bold text-[#2E3D28]">Печатный PDF-Каталог</div>
          <p class="text-xs text-stone-600 mt-1">Сформировать и распечатать иллюстрированное меню всех 72 блюд</p>
        </div>
        <div onclick="toggleDev();window.closeUnifiedSystemHub()" class="p-4 rounded-2xl bg-white border-2 border-stone-300 hover:shadow-lg cursor-pointer transition">
          <div class="text-2xl mb-1">⚙️</div>
          <div class="font-serif text-lg font-bold text-[#2E3D28]">Книга-Манифест & Логи</div>
          <p class="text-xs text-stone-600 mt-1">7 глав истории разработки и монитор сборок</p>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- 🧬 ЧИСТЫЙ ТЕКСТОВЫЙ МАСТЕР-ПРОМПТ (БЕЗ КОДА И БЕЗ JSON!) -->
<div id="master-prompt-modal" class="fixed inset-0 z-[85] bg-black/85 backdrop-blur-md hidden items-center justify-center p-2 sm:p-5">
  <div class="bg-[#FDF8F2] rounded-[2rem] max-w-5xl w-full h-[90vh] flex flex-col justify-between overflow-hidden border-4 border-[#D48238] shadow-2xl">
    <div class="p-4 sm:p-5 bg-[#2E3D28] text-white flex flex-col sm:flex-row sm:items-center justify-between gap-3">
      <div class="flex items-center gap-3">
        <div class="w-11 h-11 flex-shrink-0">{SIGN_DOVE_SVG}</div>
        <div>
          <span class="text-[10px] uppercase tracking-widest text-[#F2B880] font-extrabold">Pure Natural Language Specification • v35.0</span>
          <h3 class="font-serif text-2xl sm:text-3xl font-bold leading-none mt-0.5">🧬 Полный Текстовый Мастер-Промпт (без кода) для любой ИИ-модели</h3>
        </div>
      </div>
      <div class="flex items-center gap-2 flex-wrap">
        <button onclick="window.copyMasterPromptText()" class="px-4 py-2.5 rounded-xl bg-amber-400 hover:bg-amber-300 text-[#1A2416] font-extrabold text-xs sm:text-sm shadow-lg cursor-pointer">📋 Скопировать весь Текст (1 клик)</button>
        <button onclick="window.downloadMasterPromptFile()" class="px-4 py-2.5 rounded-xl bg-emerald-800 hover:bg-emerald-700 text-white font-extrabold text-xs sm:text-sm shadow cursor-pointer">💾 Скачать MASTER_PROMPT_MIRMIR.txt</button>
        <button onclick="window.closeMasterPromptModal()" class="w-9 h-9 rounded-full bg-white/15 text-white font-bold cursor-pointer ml-1">✕</button>
      </div>
    </div>
    <div class="p-4 sm:p-6 overflow-y-auto flex-1 space-y-3 custom-scroll">
      <div class="p-3.5 rounded-2xl bg-amber-50 border border-[#D48238]/40 text-xs text-stone-800">
        💡 <b>100% Чистый Текст (без кода и JSON):</b> Здесь русским литературным и техническим языком описаны все особенности архитектуры, дизайна, кнопок, радиоволн, конструктора Боула, витрины Магазина и все 72 блюда меню. Скопируйте этот текст и отправьте любой языковой модели!
      </div>
      <textarea id="server-master-prompt-data" readonly class="w-full h-[66vh] p-5 rounded-2xl bg-white text-stone-900 font-sans text-xs sm:text-sm leading-relaxed border-2 border-[#556432]/40 shadow-inner focus:outline-none">{master_prompt_escaped}</textarea>
    </div>
  </div>
</div>

<script>
// === 🌟 ДВИЖОК v35.0: БЕЗ РУКИ С ЦВЕТКОМ + 3D-КАРУСЕЛЬ БЛАНКОВ + ТЕКСТОВЫЙ ПРОМПТ ===
const CAFE_SHOP_ITEMS = [
  {{ id: "sh1", name: "Классический ремесленный Тофу «Мир Мир»", weight: "400 г", price: 280, photo: "img/vk_5087_1.jpg", desc: "Нежный домашний тофу собственного производства на чистой воде. Идеален для жарки, омлетов, супов и салатов." }},
  {{ id: "sh2", name: "Пряный печёный / Копчёный Тофу от Шефа", weight: "300 г", price: 340, photo: "img/vk_5055_0.jpg", desc: "Ароматный тофу в фирменном маринаде со специями и травами — готов к подаче и сэндвичам." }},
  {{ id: "sh3", name: "Крафтовый бездрожжевой хлеб на закваске (буханка)", weight: "550 г", price: 290, photo: "img/vk_5121_0.jpg", desc: "Тот самый домашний ремесленный хлеб из печи «Мир Мир» с хрустящей корочкой на живой закваске." }},
  {{ id: "sh4", name: "Домашнее Кимчи & Ферментированные овощи (банка)", weight: "400 г", price: 360, photo: "img/vk_5128_1.jpg", desc: "Живые пробиотические ферментированные овощи с имбирём и пряностями по рецепту кафе." }},
  {{ id: "sh5", name: "Пшеничные колбаски & Сейтан ручной работы", weight: "350 г", price: 420, photo: "img/vk_5118_0.jpg", desc: "Сочный растительный белок со специями — для домашних бургеров, пиццы и пасты." }},
  {{ id: "sh6", name: "Фирменный соус в баночке (Ореховый / Тахини / Чимичурри)", weight: "200 мл", price: 260, photo: "img/vk_5057_1.jpg", desc: "Густой авторский соус из боулов и салатов «Мир Мир» для заправки домашних блюд." }},
  {{ id: "sh7", name: "Бокс ремесленных батончиков «Нутс» в шоколаде (5 шт.)", weight: "375 г", price: 1050, photo: "img/vk_5069_0.jpg", desc: "Набор из 5 сытных батончиков ручной работы с финиковой карамелью и орехами без белого сахара." }},
  {{ id: "sh8", name: "Коллекционный чай «Унесённые Чаем» домой (Шу Пуэр / Габа / Да Хун Пао)", weight: "50 г", price: 450, photo: "img/vk_5122_0.jpg", desc: "Отборный листовой китайский чай из нашей чайной карты для домашних чаепитий." }}
];

window.openCafeShopModal = function() {{
  try {{ history.pushState({{guard:"shop"}}, ""); }} catch(e){{}}
  const m = document.getElementById("cafe-shop-modal");
  if (!m) return;
  m.classList.remove("hidden"); m.classList.add("flex");
  const grid = document.getElementById("cafe-shop-grid");
  if (grid) {{
    grid.innerHTML = CAFE_SHOP_ITEMS.map((it, i) => `<div class="vibe-card bg-white rounded-3xl p-3.5 border border-stone-200 shadow-sm flex flex-col justify-between">
      <div>
        <div class="h-40 rounded-2xl overflow-hidden mb-3 relative">
          <img src="${{it.photo}}" class="w-full h-full object-cover">
          <span class="absolute top-2 left-2 px-2.5 py-0.5 rounded-full bg-[#2E3D28]/90 text-[#F2B880] text-[10px] font-extrabold">${{it.weight}}</span>
        </div>
        <h4 class="font-serif text-lg font-bold text-[#2E3D28] leading-snug">${{it.name}}</h4>
        <p class="text-xs text-stone-600 mt-1 leading-relaxed">${{it.desc}}</p>
      </div>
      <div class="pt-3 mt-3 border-t border-stone-100 flex items-center justify-between">
        <strong class="text-lg font-extrabold text-[#2E3D28]">${{it.price}} ₽</strong>
        <button onclick="window.addShopItemToCart(${{i}})" class="px-3.5 py-2 rounded-xl bg-[#D48238] hover:opacity-95 text-white font-extrabold text-xs cursor-pointer shadow">+ В корзину 🛒</button>
      </div>
    </div>`).join("");
  }}
}};

window.closeCafeShopModal = function() {{
  const m = document.getElementById("cafe-shop-modal");
  if (m) {{ m.classList.add("hidden"); m.classList.remove("flex"); }}
}};

window.addShopItemToCart = function(i) {{
  const it = CAFE_SHOP_ITEMS[i];
  if (!it) return;
  const key = "shop_" + it.id;
  const ex = cart.find(x => x.key === key);
  if (ex) ex.qty++;
  else cart.push({{ key: key, idx: 900 + i, sIdx: 0, name: "🛍️ [Магазин] " + it.name + " (" + it.weight + ")", price: it.price, category: "Магазин кафе", qty: 1 }});
  updateCart();
  const t = document.createElement("div");
  t.innerText = "🛍️ Добавлено из Магазина: " + it.name;
  t.className = "fixed bottom-16 left-1/2 -translate-x-1/2 z-[95] bg-[#2E3D28] text-[#F2B880] border-2 border-[#D48238] px-4 py-2.5 rounded-2xl shadow-2xl font-extrabold text-xs whitespace-nowrap";
  document.body.appendChild(t); setTimeout(() => t.remove(), 1800);
}};

const AI_RANDOM_SUGGESTIONS = [
  "✨ ИИ-Оракул рекомендует сегодня: Попробуйте пряный бразильский суп «Ватапа» с водорослями + хрустящий сэндвич «Елена Руз» с вешенками и дайкири + согревающий чай «Масала»!",
  "🌴 Карибский сет от ИИ: Попробуйте салат «Тропикал Кубана» с ананасом и авокадо + пряный плов «Арос кон каморонос» + прохладную «Домашнюю колу» с Саган Дайля!",
  "🍄 Лесной фаворит: Попробуйте сочную пиццу «Том Ям» с лисичками и эдамаме + освежающий «Крем-суп из зелёного горошка» + тайваньский «Габа Улун» в чайнике!",
  "🔥 Сытный веган-комбо (-30%): Попробуйте тайский «Том Ям» на кокосовых сливках + «Мир-Бургер» с шоколадной курагой + ягодный смузи с семенами чиа!",
  "🥗 Средиземноморский дзен: Попробуйте омлет «Киприда» с зелёным маслом и крафтовым хлебом + салат «Сезам» с кедровым орехом + «Кедровый капучино»!",
  "🍫 Безглютеновый релакс: Попробуйте рисовую лапшу «Пад Тай» с тофу и сейтаном + десерт «Пика» с печёным пеканом + землистый Шу Пуэр от «Унесённых Чаем»!",
  "🥙 Восточный вайб из печи: Попробуйте арабскую пиццу «Лахмаджун» с гранатовым соусом + тёплый салат «Пай Хуан Гуа» из битых огурцов + «Пуэр на гранатовом соке»!"
];

window.rollRandomGastroPulse = function() {{
  const el = document.getElementById("ai-pulse-random-text");
  if (!el) return;
  const pick = AI_RANDOM_SUGGESTIONS[Math.floor(Math.random() * AI_RANDOM_SUGGESTIONS.length)];
  el.style.opacity = "0";
  setTimeout(() => {{ el.innerText = pick; el.style.opacity = "1"; }}, 180);
}};

let mirAudioCtx = null, mirRadioTimer = null, currentWaveName = "";

window.openRadioSelectorModal = function() {{
  const m = document.getElementById("radio-selector-modal");
  if (m) {{ m.classList.remove("hidden"); m.classList.add("flex"); }}
}};

window.stopMirMirRadio = function() {{
  if (mirRadioTimer) {{ clearInterval(mirRadioTimer); mirRadioTimer = null; }}
  currentWaveName = "";
  const st = document.getElementById("radio-now-status");
  if (st) st.innerText = "🔇 Сейчас радио выключено";
  const b1 = document.getElementById("radio-btn");
  if (b1) b1.innerText = "📻 Радио (3 волны)";
}};

window.playMirMirWave = function(wave) {{
  if (mirRadioTimer) clearInterval(mirRadioTimer);
  if (!mirAudioCtx) mirAudioCtx = new (window.AudioContext || window.webkitAudioContext)();
  if (mirAudioCtx.state === "suspended") mirAudioCtx.resume();
  currentWaveName = wave;

  const names = {{ ambient: "🌌 Волна 1: Эмбиент & Чаши", reggae: "🌴 Волна 2: Рэгги & Даб", mantra: "🕉️ Волна 3: Мантры & Ситар" }};
  const st = document.getElementById("radio-now-status");
  if (st) st.innerText = "🔊 Играет: " + names[wave];
  const b1 = document.getElementById("radio-btn");
  if (b1) b1.innerText = "🔊 " + (wave === "ambient" ? "Эмбиент" : wave === "reggae" ? "Рэгги" : "Мантры");

  const playNote = (freq, dur, type, vol, delaySec) => {{
    setTimeout(() => {{
      if (!currentWaveName) return;
      const now = mirAudioCtx.currentTime;
      const osc = mirAudioCtx.createOscillator();
      const gain = mirAudioCtx.createGain();
      osc.type = type || "sine";
      osc.frequency.setValueAtTime(freq, now);
      gain.gain.setValueAtTime(0.0001, now);
      gain.gain.exponentialRampToValueAtTime(vol || 0.03, now + 0.08);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + dur);
      osc.connect(gain); gain.connect(mirAudioCtx.destination);
      osc.start(now); osc.stop(now + dur + 0.05);
    }}, (delaySec || 0) * 1000);
  }};

  const triggerCycle = () => {{
    if (wave === "ambient") {{
      const notes = [261.63, 293.66, 329.63, 392.00, 440.00, 523.25];
      const f = notes[Math.floor(Math.random() * notes.length)];
      playNote(f, 3.6, "sine", 0.03, 0);
      playNote(f * 1.5, 3.2, "triangle", 0.015, 0.4);
    }} else if (wave === "reggae") {{
      const roots = [110.0, 146.83, 130.81, 164.81];
      const root = roots[Math.floor(Math.random() * roots.length)];
      playNote(root, 0.55, "sine", 0.06, 0.0);
      playNote(root * 1.5, 0.35, "sine", 0.045, 0.5);
      [root * 2, root * 2.5, root * 3].forEach(cf => {{
        playNote(cf, 0.18, "triangle", 0.022, 0.28);
        playNote(cf, 0.18, "triangle", 0.022, 0.82);
      }});
    }} else if (wave === "mantra") {{
      playNote(136.1, 3.4, "sine", 0.035, 0);
      playNote(204.15, 3.0, "sine", 0.02, 0.2);
      const raga = [272.2, 306.2, 340.25, 408.3, 459.3, 544.4];
      const rf = raga[Math.floor(Math.random() * raga.length)];
      playNote(rf, 1.4, "triangle", 0.025, 0.6);
      playNote(rf * 1.125, 1.2, "sine", 0.02, 1.4);
    }}
  }};

  triggerCycle();
  mirRadioTimer = setInterval(triggerCycle, wave === "reggae" ? 1150 : 2800);
}};

const SITE_TOGGLES_SPEC = [
  {{ key: "wings", label: "🖼️ Боковые кулисы ПК (Интерьер & Вывеска)", def: true }},
  {{ key: "vibe", label: "📳 Вибро-отклик фото при наведении мышки", def: true }},
  {{ key: "bright", label: "☀️ Турбо-яркость овощного фона под слоганом", def: true }},
  {{ key: "leaves", label: "🍃 Падающие чайные листья на экране", def: false }},
  {{ key: "lounge", label: "🌙 Вечерний тёмный лаунж-режим карточек", def: false }},
  {{ key: "float", label: "🧊 3D-левитация кубиков и Голубок", def: true }}
];

function getToggleStates() {{
  let st = {{}};
  try {{ st = JSON.parse(localStorage.getItem("mirmir_toggles_v34") || "{{}}"); }} catch(e) {{}}
  SITE_TOGGLES_SPEC.forEach(s => {{ if (st[s.key] === undefined) st[s.key] = s.def; }});
  return st;
}}

window.applySiteToggles = function() {{
  const st = getToggleStates();
  document.body.classList.toggle("cfg-no-wings", !st.wings);
  document.body.classList.toggle("cfg-no-vibe", !st.vibe);
  document.body.classList.toggle("cfg-dim-hero", !st.bright);
  document.body.classList.toggle("cfg-dark-lounge", !!st.lounge);
  document.body.classList.toggle("cfg-no-float", !st.float);

  const leavesBox = document.getElementById("falling-leaves-box");
  if (leavesBox) {{
    if (st.leaves) {{
      leavesBox.classList.remove("hidden");
      if (!leavesBox.innerHTML) {{
        leavesBox.innerHTML = Array.from({{length: 14}}).map(() => `<div style="position:absolute;left:${{Math.random()*95}}vw;top:-5vh;font-size:${{16+Math.random()*14}}px;animation:leaf-fall ${{8+Math.random()*7}}s linear infinite;animation-delay:${{Math.random()*5}}s;">🍃</div>`).join("");
      }}
    }} else {{
      leavesBox.classList.add("hidden");
    }}
  }}
}};

window.flipSiteToggle = function(k) {{
  const st = getToggleStates();
  st[k] = !st[k];
  localStorage.setItem("mirmir_toggles_v34", JSON.stringify(st));
  window.applySiteToggles();
  window.renderSystemTogglesUI();
}};

window.renderSystemTogglesUI = function() {{
  const box = document.getElementById("toggles-grid-box");
  if (!box) return;
  const st = getToggleStates();
  box.innerHTML = SITE_TOGGLES_SPEC.map(s => {{
    const on = !!st[s.key];
    return `<div onclick="window.flipSiteToggle('${{s.key}}')" class="p-3.5 rounded-2xl border-2 cursor-pointer transition flex items-center justify-between gap-2 ${{on ? 'bg-emerald-50/80 border-[#556432]' : 'bg-stone-50 border-stone-200 opacity-75'}}">
      <span class="text-xs font-extrabold text-[#2E3D28]">${{s.label}}</span>
      <span class="px-3 py-1 rounded-full text-[11px] font-extrabold ${{on ? 'bg-[#556432] text-white' : 'bg-stone-300 text-stone-700'}}">${{on ? 'ВКЛ' : 'ВЫКЛ'}}</span>
    </div>`;
  }}).join("");
}};

window.openUnifiedSystemHub = function() {{
  const m = document.getElementById("unified-system-hub");
  if (m) {{ m.classList.remove("hidden"); m.classList.add("flex"); window.renderSystemTogglesUI(); }}
}};
window.closeUnifiedSystemHub = function() {{
  const m = document.getElementById("unified-system-hub");
  if (m) {{ m.classList.add("hidden"); m.classList.remove("flex"); }}
}};

window.openMasterPromptModal = function() {{
  const m = document.getElementById("master-prompt-modal");
  if (m) {{ m.classList.remove("hidden"); m.classList.add("flex"); }}
}};
window.closeMasterPromptModal = function() {{
  const m = document.getElementById("master-prompt-modal");
  if (m) {{ m.classList.add("hidden"); m.classList.remove("flex"); }}
}};
window.copyMasterPromptText = function() {{
  const ta = document.getElementById("server-master-prompt-data");
  if (ta) {{ navigator.clipboard.writeText(ta.value); alert("🧬 Полный текстовый Мастер-Промпт (без кода) скопирован в буфер обмена!"); }}
}};
window.downloadMasterPromptFile = function() {{
  const ta = document.getElementById("server-master-prompt-data");
  if (!ta) return;
  const blob = new Blob([ta.value], {{type: "text/plain;charset=utf-8"}});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "MASTER_PROMPT_MIRMIR.txt";
  a.click();
}};

window.openYandexTaxiTo45 = function(e) {{
  if (e) e.preventDefault();
  const lat = "{LAT_45}", lon = "{LON_45}";
  if (/Android|iPhone|iPad|iPod/i.test(navigator.userAgent)) {{
    window.location.href = "yandextaxi://route?end-lat=" + lat + "&end-lon=" + lon;
  }} else {{
    window.open("https://yandex.ru/maps/?rtext=~" + lat + "," + lon + "&rtt=taxi&z=18", "_blank");
  }}
}};

window.openDeliveryModal = function() {{
  let m = document.getElementById("delivery-modal");
  if (!m) {{
    m = document.createElement("div");
    m.id = "delivery-modal";
    m.className = "fixed inset-0 z-[76] bg-black/80 backdrop-blur-md hidden items-end sm:items-center justify-center p-0 sm:p-4";
    document.body.appendChild(m);
  }}
  m.classList.remove("hidden"); m.classList.add("flex");
  const cnt = cart.reduce((s, x) => s + x.qty, 0);
  const sumTxt = document.getElementById("cart-sum") ? document.getElementById("cart-sum").innerText : "0 ₽";
  m.innerHTML = `<div class="bg-[#FDF8F2] rounded-t-[2rem] sm:rounded-[2.2rem] max-w-lg w-full p-5 sm:p-7 border-4 border-[#556432] shadow-2xl space-y-4 text-xs sm:text-sm">
    <div class="flex justify-between items-center border-b border-stone-200 pb-3">
      <div><span class="text-[10px] font-extrabold uppercase tracking-wider text-[#D48238]">Нижний Новгород • ул. Ильинская, 45</span>
      <h3 class="font-serif text-2xl sm:text-3xl font-bold text-[#2E3D28]">🛵 Доставка из кафе «Мир Мир»</h3></div>
      <button onclick="document.getElementById('delivery-modal').classList.add('hidden')" class="w-9 h-9 rounded-full bg-white shadow font-bold cursor-pointer">✕</button>
    </div>
    <div class="p-3.5 rounded-2xl bg-[#F6E4CE]/70 border border-[#556432]/20 space-y-1.5 text-stone-800">
      <div>🥗 Добавьте блюда из меню или крафтовые продукты из Магазина кафе в корзину, укажите ваш адрес и отправьте заявку шефу!</div>
      <div class="text-[#556432] font-extrabold">🛒 Сейчас в корзине: ${{cnt}} поз. (${{sumTxt}})</div>
    </div>
    <div class="space-y-2.5">
      <input id="deliv-name" placeholder="Ваше имя *" class="w-full px-3.5 py-2.5 rounded-xl bg-white border border-stone-300 text-sm">
      <input id="deliv-phone" placeholder="Телефон или @Telegram для связи *" class="w-full px-3.5 py-2.5 rounded-xl bg-white border border-stone-300 text-sm">
      <input id="deliv-addr" placeholder="Адрес доставки (улица, дом, кв., подъезд) *" class="w-full px-3.5 py-2.5 rounded-xl bg-white border border-stone-300 text-sm">
      <input id="deliv-comm" placeholder="Пожелания (ко времени / приборы / домофон)" class="w-full px-3.5 py-2 rounded-xl bg-white border border-stone-300 text-xs">
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 pt-1">
      <button onclick="document.getElementById('delivery-modal').classList.add('hidden');openMenu('Все')" class="py-3 px-4 rounded-xl bg-[#556432] text-white font-extrabold text-xs cursor-pointer">📖 Открыть меню</button>
      <button onclick="window.submitDeliveryOrder()" class="py-3 px-4 rounded-xl bg-[#D48238] text-white font-extrabold text-xs shadow-lg cursor-pointer">🛵 Отправить заказ шефу</button>
    </div>
  </div>`;
}};

window.submitDeliveryOrder = function() {{
  const name = (document.getElementById("deliv-name")?.value || "").trim();
  const phone = (document.getElementById("deliv-phone")?.value || "").trim();
  const addr = (document.getElementById("deliv-addr")?.value || "").trim();
  const comm = (document.getElementById("deliv-comm")?.value || "").trim();
  if (!cart.length) {{ alert("Сначала выберите блюда в меню или Магазине кафе!"); return; }}
  if (!name || !phone || !addr) {{ alert("Пожалуйста, заполните имя, телефон и адрес доставки!"); return; }}
  const sumTxt = document.getElementById("cart-sum") ? document.getElementById("cart-sum").innerText : "";
  const lines = ["🛵 ЗАКАЗ НА ДОСТАВКУ «Мир Мир»", "👤 Имя: " + name, "📞 Связь: " + phone, "📍 Адрес: " + addr];
  if (comm) lines.push("💬 Пожелания: " + comm);
  lines.push("", "📋 Состав заказа:");
  cart.forEach(x => lines.push("• " + x.name + " × " + x.qty + " = " + (x.price * x.qty) + " ₽"));
  lines.push("", "💰 ИТОГО: " + sumTxt);
  const txt = lines.join("\\n");
  if (navigator.clipboard) navigator.clipboard.writeText(txt);
  window.open("https://t.me/mirmir_chef?text=" + encodeURIComponent(txt), "_blank");
}};

window.openTzTerminal = function() {{
  let m = document.getElementById("tz-terminal-modal");
  if (!m) {{
    m = document.createElement("div");
    m.id = "tz-terminal-modal";
    m.className = "fixed inset-0 z-[82] bg-black/85 backdrop-blur-md hidden items-center justify-center p-2 sm:p-5";
    document.body.appendChild(m);
  }}
  m.classList.remove("hidden"); m.classList.add("flex");
  window.renderTzTerminalClean();
}};
window.closeTzTerminal = function() {{
  const m = document.getElementById("tz-terminal-modal");
  if (m) {{ m.classList.add("hidden"); m.classList.remove("flex"); }}
}};

window.renderTzTerminalClean = function() {{
  const m = document.getElementById("tz-terminal-modal");
  if (!m) return;
  const serverTasks = (DATA.tz_synced && DATA.tz_synced.tasks) ? DATA.tz_synced.tasks : [];
  let localTasks = [];
  try {{ localTasks = JSON.parse(localStorage.getItem("mirmir_tz_tasks_v30") || "[]"); }} catch(e) {{}}
  const allTasks = [...localTasks, ...serverTasks];
  const cards = allTasks.map(t => `<div class="bg-white p-4 rounded-2xl border-2 border-[#556432]/30 space-y-2">
    <div class="text-xs font-extrabold text-emerald-800">${{esc(t.status || "📝 Заметка ТЗ")}} • ${{esc(t.date || "")}}</div>
    <div class="p-3 rounded-xl bg-stone-50 font-bold text-stone-900 text-xs sm:text-sm whitespace-pre-line">${{esc(t.user_tz || "")}}</div>
    <div class="p-3 rounded-xl bg-[#FDF8F2] border border-[#D48238]/40 text-stone-800 text-xs sm:text-sm whitespace-pre-line">🤖 <b>Ответ Gemini:</b> ${{esc(t.gemini_reply || "Сохранено! Запустите run.bat для синхронизации.")}}</div>
  </div>`).join("");

  m.innerHTML = `<div class="bg-[#FDF8F2] rounded-[2rem] max-w-5xl w-full h-[88vh] flex flex-col justify-between overflow-hidden border-4 border-[#556432] shadow-2xl">
    <div class="p-4 sm:p-5 bg-[#2E3D28] text-white flex items-center justify-between gap-3 flex-wrap">
      <h3 class="font-serif text-2xl sm:text-3xl font-bold">📝 Бортовой ТЗ-Терминал</h3>
      <button onclick="window.closeTzTerminal()" class="w-9 h-9 rounded-full bg-white/15 text-white font-bold cursor-pointer">✕</button>
    </div>
    <div class="p-4 sm:p-6 overflow-y-auto flex-1 space-y-4 custom-scroll">
      <div class="bg-white p-4 rounded-2xl border-2 border-[#556432] space-y-3">
        <h4 class="font-serif text-xl font-bold text-[#2E3D28]">✍️ Добавить новую заметку в ТЗ</h4>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-2">
          <input id="tz-author-inp" placeholder="Ваше имя (Виталий / Шеф)" class="px-3 py-2 rounded-xl border text-xs sm:text-sm">
          <input id="tz-new-input" placeholder="Текст задачи или идеи..." class="sm:col-span-2 px-3 py-2 rounded-xl border text-xs sm:text-sm">
        </div>
        <button onclick="window.saveNewTzClean()" class="px-5 py-2.5 rounded-xl bg-[#D48238] text-white font-extrabold text-xs cursor-pointer">💾 Сохранить заметку в ТЗ</button>
      </div>
      <div class="space-y-3">${{cards}}</div>
    </div>
  </div>`;
}};

window.saveNewTzClean = async function() {{
  const txt = (document.getElementById("tz-new-input")?.value || "").trim();
  const auth = (document.getElementById("tz-author-inp")?.value || "").trim() || "Виталий";
  if (!txt) return;
  const entry = {{ type: "task", id: "tz_" + Date.now(), date: new Date().toLocaleString("ru-RU"), author: auth, user_tz: txt, gemini_reply: "", status: "📡 Сохранено" }};
  let local = [];
  try {{ local = JSON.parse(localStorage.getItem("mirmir_tz_tasks_v30") || "[]"); }} catch(e) {{}}
  local.unshift(entry);
  localStorage.setItem("mirmir_tz_tasks_v30", JSON.stringify(local));
  try {{ await fetch("https://ntfy.sh/{NTFY_CHANNEL}", {{ method: "POST", body: JSON.stringify(entry) }}); }} catch(e) {{}}
  window.renderTzTerminalClean();
}};

// 5. Инициализация Hero-блока (Чистый CSS-фон без руки с цветком + 3D-карусель бланков справа + Карусель блюд!)
window.addEventListener("DOMContentLoaded", () => {{
  const rail = document.getElementById("sticky-rail");
  if (rail && !rail.innerHTML.includes("openCafeShopModal")) {{
    rail.insertAdjacentHTML("afterbegin", '<button onclick="window.openCafeShopModal()" class="px-3.5 py-1.5 rounded-full bg-[#D48238] text-white text-xs font-extrabold whitespace-nowrap cursor-pointer shadow">🛍️ Магазин кафе</button><button onclick="window.openDeliveryModal()" class="px-3.5 py-1.5 rounded-full bg-emerald-700 text-white text-xs font-extrabold whitespace-nowrap cursor-pointer shadow">🛵 Доставка</button>');
  }}

  const heroLeft = document.querySelector("main section:first-of-type .lg\\\\:col-span-7");
  if (heroLeft) {{
    // Вешаем чистый CSS-класс с овощным фоном (НЕ вставляем тег <img>, чтобы блок никогда не растягивался!)
    heroLeft.classList.add("hero-veg-bg-box");

    // Удаляем любые старые <img> фоны внутри heroLeft, если они там были (особенно руку с цветком!)
    Array.from(heroLeft.children).forEach(ch => {{
      if (ch.tagName === "DIV" && ch.classList.contains("pointer-events-none")) ch.remove();
    }});

    // Напротив слогана ставим карточку «🔥 Спешлы недели ВК»
    const sloganP = heroLeft.querySelector("p.italic");
    if (sloganP && !heroLeft.querySelector(".specials-opposite-card")) {{
      const wrapper = document.createElement("div");
      wrapper.className = "flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 my-1";
      sloganP.parentNode.insertBefore(wrapper, sloganP);
      wrapper.appendChild(sloganP);
      sloganP.classList.add("flex-1");
      wrapper.insertAdjacentHTML("beforeend", `<div onclick="openMenu('Спешлы со стены ВК')" class="specials-opposite-card vibe-card cursor-pointer p-3 rounded-2xl bg-gradient-to-br from-[#D48238] to-[#b56622] text-white shadow-xl border-2 border-[#FFFDF9]/80 flex items-center gap-3 sm:w-64 flex-shrink-0">
        <img src="img/vk_5128_1.jpg" class="w-14 h-14 rounded-xl object-cover border border-white/60 flex-shrink-0">
        <div class="min-w-0">
          <span class="text-[10px] font-extrabold uppercase tracking-wider bg-black/30 px-2 py-0.5 rounded-full">🔥 Новинки</span>
          <div class="font-serif font-bold text-lg leading-tight mt-0.5">Спешлы со стены ВК</div>
          <span class="text-[11px] text-amber-100 underline font-bold">Открыть 9 блюд ➔</span>
        </div>
      </div>`);
    }}

    // Настраиваем 4 левитирующих кубика (без руки с цветком!)
    const cubes = heroLeft.querySelectorAll(".grid > div");
    const cleanCubeImgs = ["img/vk_5115_1.jpg", "img/vk_5128_1.jpg", "img/vk_5122_0.jpg", "img/vk_5069_0.jpg"];
    cubes.forEach((cube, i) => {{
      cube.classList.add("bento-anim");
      cube.style.animationDelay = (i * 0.6) + "s";
      const im = cube.querySelector("img");
      if (im && cleanCubeImgs[i]) im.src = cleanCubeImgs[i];
    }});

    // Живой рандомный «✨ Гастро-пульс от ИИ-Оракула» + Карусель блюд прямо под слоганом!
    const pulseBox = heroLeft.querySelector(".bg-white\\\\/10.backdrop-blur-md");
    if (pulseBox) {{
      pulseBox.innerHTML = `<div class="flex items-center justify-between gap-2 mb-1">
        <span class="text-[#F2B880] font-extrabold uppercase text-[11px] tracking-wider">✨ Живой Гастро-пульс от ИИ-Оракула</span>
        <button onclick="window.rollRandomGastroPulse()" class="px-2.5 py-1 rounded-full bg-[#D48238] hover:opacity-95 text-white font-extrabold text-[10px] cursor-pointer shadow">🎲 Ещё совет от ИИ</button>
      </div>
      <div id="ai-pulse-random-text" class="text-white font-semibold text-xs sm:text-sm transition-opacity duration-200 leading-relaxed"></div>`;
      window.rollRandomGastroPulse();

      if (!document.getElementById("hero-dish-carousel")) {{
        const specialsAndHits = (DATA.menu || []).filter(d => d.photo_type === "real").slice(0, 12);
        const carouselHtml = `<div class="mt-2 bg-black/45 backdrop-blur-md p-3 rounded-2xl border border-[#F2B880]/40">
          <div class="flex items-center justify-between mb-2">
            <span class="text-[11px] font-extrabold uppercase tracking-wider text-[#F2B880]">🍲 Карусель спешлов и хитов кафе (листайте или жмите +)</span>
            <div class="flex gap-1.5">
              <button onclick="document.getElementById('hero-dish-carousel').scrollBy({{left:-240,behavior:'smooth'}})" class="w-6 h-6 rounded-full bg-white/20 text-white text-xs font-bold cursor-pointer">◀</button>
              <button onclick="document.getElementById('hero-dish-carousel').scrollBy({{left:240,behavior:'smooth'}})" class="w-6 h-6 rounded-full bg-white/20 text-white text-xs font-bold cursor-pointer">▶</button>
            </div>
          </div>
          <div id="hero-dish-carousel" class="flex gap-2.5 overflow-x-auto no-scrollbar pb-1">
            ${{specialsAndHits.map((d) => {{
              const realIdx = DATA.menu.indexOf(d);
              return `<div onclick="openMenu('${{esc(d.category)}}')" class="vibe-card flex-shrink-0 w-48 bg-[#FDF8F2] text-stone-900 rounded-xl p-2 flex items-center gap-2.5 cursor-pointer shadow border border-[#F2B880]/50">
                <img src="${{esc(d.photo)}}" class="w-12 h-12 rounded-lg object-cover flex-shrink-0">
                <div class="min-w-0 flex-1">
                  <div class="font-bold text-[11px] text-[#2E3D28] truncate">${{esc(d.name)}}</div>
                  <div class="flex items-center justify-between mt-1">
                    <strong class="text-xs text-[#D48238]">${{d.price}} ₽</strong>
                    <button onclick="event.stopPropagation();addToCart(${{realIdx}},0)" class="px-2 py-0.5 rounded bg-[#556432] text-white text-[10px] font-extrabold cursor-pointer">+ В заказ</button>
                  </div>
                </div>
              </div>`;
            }}).join("")}}
          </div>
        </div>`;
        pulseBox.insertAdjacentHTML("afterend", carouselHtml);
      }}
    }}
  }}

  // ВОЗВРАЩАЕМ 3D-КАРУСЕЛЬ 4 ОРИГИНАЛЬНЫХ БЛАНКОВ МЕНЮ СПРАВА В HERO-БЛОКЕ!
  const scansBox = document.getElementById("scans-top-box");
  if (scansBox && DATA.menu_scans && DATA.menu_scans.length) {{
    const parentCol = scansBox.parentElement;
    parentCol.classList.add("relative", "overflow-hidden");
    parentCol.innerHTML = `<div class="absolute inset-0 flex items-center justify-center pointer-events-none opacity-[0.42] z-0">
      <div class="wm-spin">
        <svg width="450" height="450" viewBox="0 0 120 120" fill="none"><circle cx="60" cy="60" r="56" stroke="#F2B880" stroke-width="3"/><circle cx="60" cy="60" r="50" stroke="#FFFDF9" stroke-width="2" stroke-dasharray="5 4"/><circle cx="60" cy="62" r="25" stroke="#F2B880" stroke-width="2.5" fill="rgba(242,184,128,0.18)"/><path d="M32 58 C24 44, 34 26, 52 34 C46 40, 42 48, 42 58 C38 60, 34 60, 32 58 Z" fill="#FFFDF9"/><path d="M88 58 C96 44, 86 26, 68 34 C74 40, 78 48, 78 58 C82 60, 86 60, 88 58 Z" fill="#FFFDF9"/><path d="M35 52 C30 68, 44 88, 60 90 C76 88, 90 68, 85 52 C82 66, 72 78, 60 80 C48 78, 38 66, 35 52 Z" fill="#FFFDF9"/><circle cx="48" cy="36" r="6" fill="#FFFDF9"/><text x="60" y="106" text-anchor="middle" fill="#F2B880" font-family="serif" font-weight="bold" font-size="11" letter-spacing="3">• MIR MIR •</text></svg>
      </div>
    </div>
    <span class="relative z-10 text-xs font-extrabold uppercase px-3.5 py-1 rounded-full bg-black/50 text-[#F2B880] border border-[#F2B880]/40 mb-2">🔄 3D-карусель оригинальных бланков</span>
    <div id="stage-3d-v35" class="stage-3d relative z-10"></div>
    <div class="relative z-20 flex items-center gap-3 mt-2">
      <button onclick="window.step3DV35(-1)" class="w-9 h-9 rounded-full bg-white/20 hover:bg-white/35 text-white font-bold cursor-pointer">◀</button>
      <button onclick="openMenu('Все')" class="px-4 py-2 rounded-full bg-[#D48238] text-white text-xs font-extrabold uppercase shadow-lg cursor-pointer">📖 Все блюда (${{DATA.menu.length}})</button>
      <button onclick="window.step3DV35(1)" class="w-9 h-9 rounded-full bg-white/20 hover:bg-white/35 text-white font-bold cursor-pointer">▶</button>
    </div>`;
    let c3d = 0;
    const stBox = document.getElementById("stage-3d-v35");
    stBox.innerHTML = DATA.menu_scans.map((s, i) => {{
      const meta = (DATA.sheet_meta && DATA.sheet_meta[i]) || {{title:"Бланк меню", cat:"Все"}};
      return `<div class="slide-3d" onclick="openMenu('${{meta.cat}}')"><div class="w-full h-full rounded-3xl overflow-hidden shadow-2xl border-4 border-[#FFFDF9] bg-[#FFFDF9] flex flex-col justify-between"><div class="flex-1 overflow-hidden flex items-center justify-center p-1.5"><img src="${{s}}?v=350" class="max-w-full max-h-full object-contain"></div><div class="bg-[#2E3D28] px-3 py-2 text-white flex items-center justify-between"><span class="text-[11px] font-extrabold text-[#F2B880] truncate">${{meta.title}}</span><button onclick="event.stopPropagation();showImg('${{s}}')" class="text-[10px] bg-white/20 px-2 py-0.5 rounded font-bold">Лупа 🔍</button></div></div></div>`;
    }}).join("");
    window.upd3DV35 = function() {{
      const sl = stBox.querySelectorAll(".slide-3d"), tot = sl.length;
      sl.forEach((el, idx) => {{
        const d = (idx - c3d + tot) % tot;
        if(d===0){{ el.style.transform="translateX(0) translateZ(65px) scale(1)"; el.style.zIndex="30"; el.style.opacity="1"; }}
        else if(d===1){{ el.style.transform="translateX(55px) translateZ(-35px) rotateY(-16deg) scale(0.88)"; el.style.zIndex="20"; el.style.opacity="0.82"; }}
        else if(d===tot-1){{ el.style.transform="translateX(-55px) translateZ(-35px) rotateY(16deg) scale(0.88)"; el.style.zIndex="20"; el.style.opacity="0.82"; }}
        else {{ el.style.transform="translateX(0) translateZ(-95px) scale(0.75)"; el.style.zIndex="10"; el.style.opacity="0.35"; }}
      }});
    }};
    window.step3DV35 = function(delta) {{ c3d = (c3d + delta + DATA.menu_scans.length) % DATA.menu_scans.length; window.upd3DV35(); }};
    window.upd3DV35();
    setInterval(() => window.step3DV35(1), 4000);
  }}

  window.applySiteToggles();
}});
</script>
"""

    last_body_idx = html.rfind("</body>")
    if last_body_idx != -1:
        html = html[:last_body_idx] + V35_MODALS_AND_JS + "\n" + html[last_body_idx:]

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✨ [Ядро v35.0] Рука с цветком удалена, Hero-блок и 3D-карусель выровнены, Мастер-Промпт переписан ЧИСТЫМ ТЕКСТОМ!")
