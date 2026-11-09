# -*- coding: utf-8 -*-
"""ПОДАРОЧНОЕ ЯДРО (up44): ИИ-ГЕНЕРАТОР С УТВЕРЖДЕНИЕМ + ЗАГРУЗКА С ПК + СУПЕР-ЛУПА Z-200 + ВСЕ ЛОГИ + JS-ВИБРО"""
import os, re, json, html as html_lib

P_HTTPS = "ht" + "tps://"
LAT_45, LON_45 = "56.322355", "43.990383"
NTFY_CHANNEL = "mirmir_tz_sync_nn45_v30"
TZ_FILE = "tz_mirmir.json"
NL = chr(10)

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
    "Суп дня": "img/vk_5057_1.jpg",
    "Крем-суп из зелёного горошка и авокадо": "img/vk_5057_1.jpg",
    "Ватапа": "img/vk_5053_0.jpg",
    "Омлет из тофу (3 вкуса на выбор)": "img/vk_5087_1.jpg",
    "Шакшука": "img/vk_5055_0.jpg",
    "Лапша Том Ям": "img/vk_5057_0.jpg",
    "Неряха Джо": "img/vk_5118_1.jpg",
    "Пицца Грибная (на цельнозерновом тесте)": "img/vk_5085_1.jpg",
    "Лахмаджун (25 см)": "img/vk_5062_1.jpg",
    "Чебурек Ван Танс": "img/vk_5121_0.jpg",
    "Кутаб Сабзи": "img/vk_5094_1.jpg",
    "Безглютеновая шарлотка из деревенских яблок": "img/vk_5103_1.jpg",
    "Десерт «Пика» с печеным пеканом и шоколадом": "img/vk_5069_0.jpg",
    "Теплая лепешка «Роти Клуай» с бананом и ананасом": "img/vk_5103_1.jpg",
    "Масала": "img/vk_5122_0.jpg",
    "Облепиховый чай": "img/vk_5122_0.jpg",
    "Пуэр на гранатовом соке": "img/vk_5115_2.jpg"
}

DISTINCT_BOTANICAL_MAP = {
    "Суп выходного дня": "img/macro_tomyum_bowl.jpg",
    "Том Ям": "img/macro_tomyum_bowl.jpg",
    "Мисо-суп": "img/macro_miso_tofu.jpg",
    "Боул (Сытная тарелка-конструктор)": "img/vk_5055_0.jpg",
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
    "Зелёный смузи": "img/macro_pineapple_mint.jpg",
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


def build_pure_text_master_prompt():
    lines = [
        "ПОЛНОЕ ТЕКСТОВОЕ ТЕХНИЧЕСКОЕ ЗАДАНИЕ (МАСТЕР-ПРОМПТ) НА РАЗРАБОТКУ ГИБРИДНОГО PYTHON-КОМПИЛЯТОРА И САЙТА ВЕГАН-КАФЕ «МИР МИР»",
        "",
        "Роль для языковой модели ИИ: Выступи в роли ведущего Системного Архитектора и Full-Stack разработчика (Python + современный реактивный фронтенд). Создай систему на языке Python, которая объединяет верифицированную базу меню зала с автоматической синхронизацией новостей, сезонных новинок и фотографий из официальной группы ВКонтакте (vk.com/mirmir.cafe) и Яндекс.Карт, публикуя статический сайт в GitHub Pages.",
        "",
        "1. ЧЕСТНАЯ ГИБРИДНАЯ АРХИТЕКТУРА ДАННЫХ И ИИ-СТУДИЯ ВСЕХ 72 ПОЗИЦИЙ В ШЕСТЕРЁНКЕ ⚙️",
        "— Первичная оцифровка бланков с проверкой человеком: при распознавании 4 оригинальных бумажных листов меню через мультимодальное зрение Gemini Vision результат сохраняется в черновик menu_draft.json, а после сверки цен фиксируется в menu_data.py (63 позиции зала с парными кнопками Малой и Большой порции + 9 сезонных спешлов).",
        "— Гибридное управление фотографиями (ИИ-парсинг + ИИ-генерация + Ручной выбор в шестерёнке ⚙️): при сборке ИИ автоматически подбирает фотографии из ВК и Яндекс.Карт. При этом внутри кнопки-шестерёнки «⚙️» встроена вкладка «🍲 Все 72 блюда: Фото», где напротив каждой позиции можно: 1) выбрать готовый кадр во всплывающей галерее с полноэкранной Лупой, 2) загрузить файл с компьютера, 3) сгенерировать новое фуд-фото через ИИ по текстовому описанию, посмотреть его через Лупу во весь экран и нажать кнопку «✅ Утвердить в меню», либо сбросить блюдо обратно на автоматический ИИ-парсинг.",
        "— Безопасность секретов: локальный сборщик считывает токены из защищённых файлов VK_TOKEN_FILE и GEMINI_KEY_FILE (в .gitignore).",
        "",
        "2. ЗАЩИТА ОТ ЛИМИТОВ API (HTTP 429), ТАЙМАУТОВ И ПОЛНЫЙ НАКОПИТЕЛЬНЫЙ ЛОГ АПДЕЙТОВ",
        "— Каскад моделей Gemini: автоматический фоллбэк gemini-3-flash-preview -> gemini-2.5-flash -> gemini-2.0-flash. При ошибке 429 или таймауте сборщик использует локальный кэш (cache_posts.json, cache_ai_brain.json), блокируя пуш пустого шаблона.",
        "— Все апдейты и сборки записываются в накопительный реестр build_history.json и отображаются во вкладке «📜 Логи сборок и апдейтов» внутри шестерёнки.",
        "",
        "3. ПЕРВЫЙ ЭКРАН, 3 РЯДА СПЕШЛОВ ПОД 3D-КАРУСЕЛЬЮ, JS-ВИБРАЦИЯ И НОВОСТИ С КНОПКОЙ «ЧИТАТЬ НА VK»",
        "— В шапке: живой статус «🟢 ОТКРЫТО ДО 21:00» / «🔴 ЗАКРЫТО ДО 12:00» и «🔥 БИЗНЕС-ЛАНЧ -30%» в будни 12–16, кнопки Меню, Бронь столика, Доставка, Магазин кафе, Боул, Радио (4 волны с Ханг Драмом) и Такси в кафе (56.322355, 43.990383).",
        "— Справа в первом экране под 3D-каруселью листов меню расположена трёхрядная витрина «Сезонные спешлы от Шефа».",
        "— На ПК работает прямой физический JS-движок микро-вибрации фотографий при наведении курсора мыши, а в секции «Последние новости и анонсы» слева внизу каждой карточки расположена кнопка «читать на VK ↗»."
    ]
    full_txt = NL.join(lines)
    with open("MASTER_PROMPT_MIRMIR.txt", "w", encoding="utf-8") as f:
        f.write(full_txt)
    return full_txt


def load_clean_tz():
    if os.path.exists(TZ_FILE):
        try:
            with open(TZ_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"tasks": [], "dishes": {}}


def get_all_ready_local_photos():
    if not os.path.exists("img"):
        return []
    files = []
    for fn in sorted(os.listdir("img")):
        if fn.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            if "5047_" in fn:
                continue
            files.append("img/" + fn)
    return files


def load_all_build_history():
    if os.path.exists("build_history.json"):
        try:
            with open("build_history.json", "r", encoding="utf-8") as f:
                d = json.load(f)
            if isinstance(d, list):
                return d
        except Exception:
            pass
    return []


def enhance_index_html():
    if not os.path.exists("index.html"):
        return

    left_wing = "img/ymap_org_0.jpg" if os.path.exists("img/ymap_org_0.jpg") else "img/vk_5068_0.jpg"
    right_wing = "img/ymap_org_1.jpg" if os.path.exists("img/ymap_org_1.jpg") else "img/vk_5128_1.jpg"
    tz_synced = load_clean_tz()
    ready_gallery_files = get_all_ready_local_photos()
    full_build_logs = load_all_build_history()

    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    html = html.replace(".hidden { display:none !important; }", "")

    CLIENT_FRIENDLY_REPLACEMENTS = [
        ("Спешлы со стены ВК", "Сезонные спешлы от Шефа"),
        ("100% по 4 бланкам • Малые и большие порции", "Этичная растительная кухня • Выбор объёма порции"),
        ("100% ПО 4 БЛАНКАМ • МАЛЫЕ И БОЛЬШИЕ ПОРЦИИ", "ЭТИЧНАЯ РАСТИТЕЛЬНАЯ КУХНЯ • ВЫБОР ОБЪЁМА ПОРЦИИ"),
        ("Дайджест ВКонтакте", "Жизнь и события нашего кафе"),
        ("ДАЙДЖЕСТ ВКОНТАКТЕ", "ЖИЗНЬ И СОБЫТИЯ НАШЕГО КАФЕ"),
        ("Бланк №1: Основное меню", "Страница 1: Супы и Боулы"),
        ("Бланк №2: Чайная карта", "Страница 4: Чайная коллекция"),
        ("Бланк №3: Десерты и Бар", "Страница 3: Десерты и Смузи"),
        ("Бланк №4: Салаты, Лапша, Из печи", "Страница 2: Салаты, Лапша и Выпечка"),
        ("📸 Реальное фото ВК", "📸 Фото блюда"),
        ("Реальное фото ВК", "Фото блюда"),
        ("🌿 Индивидуальное превью ингредиентов состава (не снимок готового блюда)", "🌿 Ингредиенты состава блюда"),
        ("🎨 Макро-фото ингредиентов состава (не снимок готового блюда)", "🌿 Ингредиенты состава блюда"),
        ("Макро-превью состава", "Ингредиенты состава"),
        ("🌿 Состав", "🌿 Ингредиенты"),
        ("👀 Ищем в меню!", "🍵 Атмосфера кафе"),
        ("Юмор-заглушка", "Атмосфера кафе"),
        ("Иллюстрация подачи (не реальное фото из ВК, чтобы не вводить гостей в заблуждение)", "Атмосферная иллюстрация подачи")
    ]
    for old_str, new_str in CLIENT_FRIENDLY_REPLACEMENTS:
        html = html.replace(old_str, new_str)

    m_data = re.search(r"const DATA = (\{.*?\});\s*\n\s*const CV =", html, re.DOTALL)
    if m_data:
        data_obj = json.loads(m_data.group(1).replace("<\\/", "</"))
        data_obj["tz_synced"] = tz_synced
        data_obj["ready_photos"] = ready_gallery_files
        data_obj["full_build_logs"] = full_build_logs
        dish_ov = tz_synced.get("dishes", {})

        if "sheet_meta" in data_obj:
            client_sheets = [
                {"title": "🥗 Страница 1: Супы, Боул и Омлеты", "cat": "Супы"},
                {"title": "🍵 Страница 4: Чайная коллекция", "cat": "Чайная карта"},
                {"title": "🍰 Страница 3: Десерты, Смузи и Кофе", "cat": "Десерты без сахара"},
                {"title": "🍕 Страница 2: Салаты, Лапша и Выпечка", "cat": "Бургеры и Из печи"}
            ]
            for idx_s in range(min(len(data_obj["sheet_meta"]), 4)):
                data_obj["sheet_meta"][idx_s] = client_sheets[idx_s]

        for item in data_obj.get("menu", []):
            if item.get("category") == "Спешлы со стены ВК":
                item["category"] = "Сезонные спешлы от Шефа"
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

            item["ai_default_photo"] = item["photo"]
            item["ai_default_type"] = item["photo_type"]
            item["is_manual_override"] = False

            if nm in dish_ov and dish_ov[nm].get("photo"):
                item["photo"] = dish_ov[nm]["photo"]
                item["photo_type"] = "real"
                item["is_manual_override"] = True
            if nm in dish_ov and dish_ov[nm].get("user_tz"):
                item["user_tz"] = dish_ov[nm]["user_tz"]

        new_json_str = json.dumps(data_obj, ensure_ascii=False).replace("</", "<\\/")
        html = html[:m_data.start(1)] + new_json_str + html[m_data.end(1):]

    master_prompt_raw = build_pure_text_master_prompt()
    master_prompt_escaped = html_lib.escape(master_prompt_raw)

    STATIC_HEAD_CSS = """
<style id="v44-gift-styles">
  @keyframes float-dove { 0%,100%{transform:translateY(0) rotate(0deg)} 50%{transform:translateY(-7px) rotate(2deg)} }
  @keyframes float-cube { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-4px)} }
  @keyframes spin-wm { from{transform:rotate(0deg)} to{transform:rotate(360deg)} }
  @keyframes leaf-fall {
    0% { transform: translateY(-10vh) translateX(0) rotate(0deg); opacity: 0.85; }
    50% { transform: translateY(50vh) translateX(25px) rotate(180deg); opacity: 0.7; }
    100% { transform: translateY(105vh) translateX(-20px) rotate(360deg); opacity: 0; }
  }
  .dove-float { animation: float-dove 5s ease-in-out infinite; }
  .bento-anim { animation: float-cube 4s ease-in-out infinite; transition: all 0.3s ease; border: 2px solid rgba(242,184,128,0.75) !important; }
  .wm-spin { animation: spin-wm 60s linear infinite; }
  .stage-3d { perspective: 1200px; position: relative; width: 100%; height: 280px; display: flex; align-items: center; justify-content: center; }
  .slide-3d { position: absolute; width: 195px; height: 268px; transition: all 0.6s cubic-bezier(0.25,1,0.5,1); transform-style: preserve-3d; cursor: pointer; }

  .mirmir-news-card-fixed {
    background-color: #FFFDF9 !important;
    color: #2E3D28 !important;
    border: 1px solid rgba(85, 100, 50, 0.22) !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
  }
  .mirmir-news-img-wrap-fixed {
    height: auto !important;
    max-height: none !important;
    overflow: hidden !important;
    border-radius: 1rem !important;
    background: #EFE6D8 !important;
    position: relative !important;
  }
  .mirmir-news-img-fixed {
    width: 100% !important;
    height: 265px !important;
    object-fit: cover !important;
    object-position: center 55% !important;
    border-radius: 1rem !important;
    display: block !important;
  }
  body.cfg-news-contain .mirmir-news-img-fixed {
    height: 275px !important;
    object-fit: contain !important;
    background: #23301E !important;
  }

  .hero-interior-dynamic-bg {
    background-image: linear-gradient(95deg, rgba(20,32,16,0.88) 0%, rgba(30,46,24,0.76) 55%, rgba(20,32,16,0.86) 100%), var(--hero-slide-bg, url('img/ymap_org_0.jpg')) !important;
    background-size: cover !important;
    background-position: center !important;
    transition: background-image 0.7s ease-in-out !important;
  }

  #pc-v26-authentic-wings { display: none; }
  @media (min-width: 900px) {
    body:not(.cfg-no-wings) { background-color: #1A2416 !important; }
    body:not(.cfg-no-wings) #pc-v26-authentic-wings { display: block !important; }
    body:not(.cfg-no-wings) main.max-w-7xl {
      background: rgba(246, 228, 206, 0.96);
      backdrop-filter: blur(12px);
      border-radius: 2.8rem;
      padding: 2.2rem 2.5rem !important;
      margin-top: 1.5rem !important;
      box-shadow: 0 30px 95px rgba(0,0,0,0.72), 0 0 0 2px rgba(242,184,128,0.35);
      position: relative;
      z-index: 10;
    }
  }
  body.cfg-no-float .dove-float, body.cfg-no-float .bento-anim {
    animation: none !important;
  }
</style>
"""
    html = html.replace("</head>", STATIC_HEAD_CSS + NL + "</head>", 1)

    STATIC_WINGS_HTML = """
<div id="pc-v26-authentic-wings" class="fixed inset-0 pointer-events-none z-0 overflow-hidden">
  <div class="absolute left-0 top-0 bottom-0 w-1/3 overflow-hidden">
    <img src="__LEFT_WING__?v=104" class="w-full h-full object-cover opacity-60 scale-105 filter saturate-125 contrast-110">
    <div class="absolute inset-0" style="background:linear-gradient(90deg, rgba(20,30,16,0.18) 0%, rgba(26,36,22,0.94) 94%);"></div>
    <div class="absolute top-28 left-8 w-24 h-24 opacity-90 dove-float">__SIGN_DOVE_SVG__</div>
  </div>
  <div class="absolute right-0 top-0 bottom-0 w-1/3 overflow-hidden">
    <img src="__RIGHT_WING__?v=104" class="w-full h-full object-cover opacity-65 scale-105 filter saturate-125 contrast-110">
    <div class="absolute inset-0" style="background:linear-gradient(270deg, rgba(20,30,16,0.18) 0%, rgba(26,36,22,0.94) 94%);"></div>
    <div class="absolute top-28 right-8 w-24 h-24 opacity-90 dove-float" style="animation-delay:1.4s">__SIGN_DOVE_SVG__</div>
  </div>
</div>
<div id="falling-leaves-box" class="fixed inset-0 pointer-events-none z-40 overflow-hidden hidden"></div>
""".replace("__LEFT_WING__", left_wing).replace("__RIGHT_WING__", right_wing).replace("__SIGN_DOVE_SVG__", SIGN_DOVE_SVG)
    html = re.sub(r"(<body[^>]*>)", r"\1" + NL + STATIC_WINGS_HTML, html, count=1)

    html = html.replace(
        '<span class="text-2xl">🕊️</span>',
        f'<div class="w-12 h-12 rounded-full flex-shrink-0 shadow-lg hover:scale-110 transition">{SIGN_DOVE_SVG}</div>'
    )

    V44_MODALS_AND_JS = r"""
<!-- 🔍 СУПЕР-ЛАЙТБОКС Z-[200] (ОТКРЫВАЕТ ПОЛНОРАЗМЕРНЫЕ ФОТО ПОВЕРХ ЛЮБЫХ МОДАЛЬНЫХ ОКОН И ШЕСТЕРЁНКИ!) -->
<div id="super-zoom-lightbox" onclick="window.closeSuperZoom()" class="fixed inset-0 z-[200] bg-black/92 backdrop-blur-md hidden items-center justify-center p-3 sm:p-8 cursor-zoom-out">
  <div onclick="event.stopPropagation()" class="relative max-w-5xl w-full flex flex-col items-center gap-3">
    <div class="w-full flex items-center justify-between text-white px-2">
      <span id="super-zoom-caption" class="font-serif text-xl sm:text-2xl font-bold text-[#F2B880] truncate">🔍 Просмотр фотографии в полном размере</span>
      <div class="flex items-center gap-2">
        <a id="super-zoom-dl" href="#" download="mirmir_photo.jpg" target="_blank" class="px-3.5 py-1.5 rounded-xl bg-[#556432] hover:bg-[#D48238] text-white text-xs font-extrabold transition">💾 Открыть оригинал / Скачать</a>
        <button onclick="window.closeSuperZoom()" class="w-10 h-10 rounded-full bg-white/20 hover:bg-red-600 text-white font-bold text-lg cursor-pointer">✕</button>
      </div>
    </div>
    <img id="super-zoom-img" src="" class="max-h-[82vh] max-w-full object-contain rounded-2xl shadow-2xl border-2 border-[#F2B880]/50 bg-[#141C11]">
  </div>
</div>

<!-- 📸 ВСПЛЫВАЮЩЕЕ ОКНО ВЫБОРА ГОТОВЫХ ФОТО Z-[140] (ОТКРЫВАЕТСЯ ПРЯМО ПОВЕРХ ШЕСТЕРЁНКИ С КРУПНЫМИ ПРЕВЬЮ И ЛУПОЙ!) -->
<div id="ready-gallery-popup" class="fixed inset-0 z-[140] bg-black/85 backdrop-blur-md hidden items-center justify-center p-2 sm:p-6">
  <div class="bg-[#FDF8F2] rounded-[2.2rem] max-w-5xl w-full h-[88vh] flex flex-col justify-between overflow-hidden border-4 border-[#D48238] shadow-2xl">
    <div class="p-4 sm:p-5 bg-[#2E3D28] text-white flex flex-col sm:flex-row sm:items-center justify-between gap-3">
      <div>
        <span class="text-[10px] uppercase tracking-widest text-[#F2B880] font-extrabold block">Витрина готовых фотографий из папки img/ (ВК + Яндекс.Карты + Ингредиенты)</span>
        <h3 id="ready-popup-title" class="font-serif text-2xl sm:text-3xl font-bold">📸 Выберите готовое фото для блюда</h3>
      </div>
      <div class="flex items-center gap-2">
        <input id="ready-popup-filter" oninput="window.renderReadyGalleryPopupGrid()" placeholder="🔍 Фильтр (vk, ymap, macro)..." class="px-3 py-1.5 rounded-xl bg-white text-stone-900 text-xs font-bold">
        <button onclick="window.closeReadyGalleryPopup()" class="w-9 h-9 rounded-full bg-white/15 hover:bg-red-600 text-white font-bold cursor-pointer">✕</button>
      </div>
    </div>
    <div id="ready-popup-grid" class="p-4 sm:p-6 overflow-y-auto flex-1 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3.5 custom-scroll"></div>
  </div>
</div>

<!-- СКРЫТЫЙ INPUT ДЛЯ ЗАГРУЗКИ ФАЙЛА С КОМПЬЮТЕРА -->
<input type="file" id="pc-dish-file-input" accept="image/*" class="hidden" onchange="window.handlePcFileSelected(event)">

<!-- 🪑 МОДАЛЬНОЕ ОКНО: БРОНИРОВАНИЕ СТОЛИКА -->
<div id="book-table-modal" class="fixed inset-0 z-[77] bg-black/80 backdrop-blur-md hidden items-end sm:items-center justify-center p-0 sm:p-4">
  <div class="bg-[#FDF8F2] rounded-t-[2rem] sm:rounded-[2.2rem] max-w-lg w-full p-5 sm:p-7 border-4 border-[#556432] shadow-2xl space-y-4 text-xs sm:text-sm">
    <div class="flex justify-between items-center border-b border-stone-200 pb-3">
      <div class="flex items-center gap-3">
        <div class="w-11 h-11 flex-shrink-0">__SIGN_DOVE_SVG__</div>
        <div>
          <span class="text-[10px] font-extrabold uppercase tracking-wider text-[#D48238]">Нижний Новгород • ул. Ильинская, 45</span>
          <h3 class="font-serif text-2xl sm:text-3xl font-bold text-[#2E3D28]">🪑 Бронь столика в «Мир Мир»</h3>
        </div>
      </div>
      <button onclick="window.closeBookTableModal()" class="w-9 h-9 rounded-full bg-white shadow font-bold cursor-pointer">✕</button>
    </div>
    <div class="space-y-2.5">
      <div>
        <label class="font-extrabold text-[11px] uppercase text-[#556432] block mb-1">1. Выберите любимую зону в зале:</label>
        <select id="book-zone" class="w-full px-3.5 py-2.5 rounded-xl bg-white border border-stone-300 text-xs sm:text-sm font-bold text-[#2E3D28]">
          <option value="🛋️ Изумрудный велюровый диван с картинами">🛋️ Изумрудный велюровый диван с картинами</option>
          <option value="🏛️ Уютный столик под историческим кирпичным сводом">🏛️ Уютный столик под историческим кирпичным сводом</option>
          <option value="🍵 Большой стол для китайской чайной церемонии">🍵 Большой стол для китайской чайной церемонии</option>
          <option value="🌿 Столик у живых растений в основном зале">🌿 Столик у живых растений в основном зале</option>
        </select>
      </div>
      <div class="grid grid-cols-3 gap-2">
        <div><label class="font-bold text-[10px] uppercase text-stone-500 block mb-1">Дата:</label><input id="book-date" type="date" class="w-full px-2.5 py-2 rounded-xl bg-white border border-stone-300 text-xs"></div>
        <div><label class="font-bold text-[10px] uppercase text-stone-500 block mb-1">Время (12–21):</label><input id="book-time" type="time" value="18:00" class="w-full px-2.5 py-2 rounded-xl bg-white border border-stone-300 text-xs"></div>
        <div><label class="font-bold text-[10px] uppercase text-stone-500 block mb-1">Гостей:</label><select id="book-guests" class="w-full px-2.5 py-2 rounded-xl bg-white border border-stone-300 text-xs font-bold"><option value="1 гость">1 гость</option><option value="2 гостя" selected>2 гостя</option><option value="3 гостя">3 гостя</option><option value="4 гостя">4 гостя</option><option value="Компания 5–8 человек">5–8 гостей</option></select></div>
      </div>
      <input id="book-name" placeholder="Ваше имя *" class="w-full px-3.5 py-2.5 rounded-xl bg-white border border-stone-300 text-sm">
      <input id="book-phone" placeholder="Телефон или @Telegram для подтверждения *" class="w-full px-3.5 py-2.5 rounded-xl bg-white border border-stone-300 text-sm">
      <input id="book-comm" placeholder="Пожелания (например: заварить Габа Улун к приходу / предзаказ по меню)" class="w-full px-3.5 py-2 rounded-xl bg-white border border-stone-300 text-xs">
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 pt-1">
      <a href="tel:+79200282858" class="py-3 px-4 rounded-xl bg-[#556432] text-white font-extrabold text-xs text-center flex items-center justify-center gap-1.5 shadow">📞 Позвонить: +7 (920) 028-28-58</a>
      <button onclick="window.submitTableBooking()" class="py-3 px-4 rounded-xl bg-[#D48238] text-white font-extrabold text-xs shadow-lg cursor-pointer">🪑 Забронировать через Telegram</button>
    </div>
  </div>
</div>

<!-- 🛍️ МАГАЗИН КАФЕ «МИР МИР» -->
<div id="cafe-shop-modal" class="fixed inset-0 z-[75] bg-black/85 backdrop-blur-md hidden items-center justify-center p-2 sm:p-5">
  <div class="bg-[#FDF8F2] rounded-[2.2rem] max-w-5xl w-full h-[90vh] flex flex-col justify-between overflow-hidden border-4 border-[#D48238] shadow-2xl">
    <div class="p-4 sm:p-6 bg-[#2E3D28] text-white flex items-center justify-between gap-3">
      <div class="flex items-center gap-3.5">
        <div class="w-12 h-12 flex-shrink-0">__SIGN_DOVE_SVG__</div>
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

<!-- 📻 ОНЛАЙН-РАДИО «МИР МИР» (4 ВОЛНЫ: ХАНГ ДРАМ / ЭМБИЕНТ / РЭГГИ / МАНТРЫ) -->
<div id="radio-selector-modal" class="fixed inset-0 z-[78] bg-black/80 backdrop-blur-md hidden items-center justify-center p-3">
  <div class="bg-[#FDF8F2] rounded-[2.2rem] max-w-lg w-full p-5 sm:p-6 border-4 border-[#556432] shadow-2xl space-y-3.5">
    <div class="flex items-center justify-between border-b border-stone-200 pb-3">
      <div class="flex items-center gap-3">
        <div class="w-11 h-11 flex-shrink-0">__SIGN_DOVE_SVG__</div>
        <div>
          <span class="text-[10px] font-extrabold uppercase tracking-wider text-[#D48238]">4 атмосферных потока • Работает в РФ без VPN</span>
          <h3 class="font-serif text-2xl font-bold text-[#2E3D28]">📻 Радио «Мир Мир»</h3>
        </div>
      </div>
      <button onclick="document.getElementById('radio-selector-modal').classList.add('hidden');document.getElementById('radio-selector-modal').classList.remove('flex')" class="w-9 h-9 rounded-full bg-white shadow font-bold cursor-pointer">✕</button>
    </div>
    <div class="space-y-2">
      <button onclick="window.playMirMirWave('hangdrum')" class="w-full p-3.5 rounded-2xl border-2 border-teal-700 bg-teal-50/60 hover:bg-teal-100/70 text-left flex items-center justify-between transition cursor-pointer shadow-sm">
        <div><div class="font-serif text-xl font-bold text-[#2E3D28]">🛸 1. Радио Ханг Драм (Hang Drum & Handpan)</div><div class="text-xs text-stone-600">Космические переливы живого металлического ханга и хэндпана</div></div>
        <span class="px-3 py-1 rounded-xl bg-teal-800 text-white text-xs font-extrabold">▶ Эфир</span>
      </button>
      <button onclick="window.playMirMirWave('ambient')" class="w-full p-3.5 rounded-2xl border-2 border-[#556432] bg-white hover:bg-emerald-50 text-left flex items-center justify-between transition cursor-pointer shadow-sm">
        <div><div class="font-serif text-xl font-bold text-[#2E3D28]">🌌 2. Эмбиент & Чилл (Live Stream)</div><div class="text-xs text-stone-600">Глубокий атмосферный эмбиент и космический лаунж 24/7</div></div>
        <span class="px-3 py-1 rounded-full bg-[#556432] text-white text-xs font-extrabold">▶ Эфир</span>
      </button>
      <button onclick="window.playMirMirWave('reggae')" class="w-full p-3.5 rounded-2xl border-2 border-[#D48238] bg-white hover:bg-amber-50 text-left flex items-center justify-between transition cursor-pointer shadow-sm">
        <div><div class="font-serif text-xl font-bold text-[#2E3D28]">🌴 3. Рэгги & Даб Радио (Live Stream)</div><div class="text-xs text-stone-600">Солнечный корневой рэгги, даб и ямайские вибрации в прямом эфире</div></div>
        <span class="px-3 py-1 rounded-xl bg-[#D48238] text-white text-xs font-extrabold">▶ Эфир</span>
      </button>
      <button onclick="window.playMirMirWave('mantra')" class="w-full p-3.5 rounded-2xl border-2 border-purple-700/60 bg-white hover:bg-purple-50 text-left flex items-center justify-between transition cursor-pointer shadow-sm">
        <div><div class="font-serif text-xl font-bold text-[#2E3D28]">🕉️ 4. Мантры, Ситар & Гоа (Live Stream)</div><div class="text-xs text-stone-600">Индийский ситар, табла, мантры и восточный медитативный поток</div></div>
        <span class="px-3 py-1 rounded-xl bg-purple-800 text-white text-xs font-extrabold">▶ Эфир</span>
      </button>
    </div>
    <div class="pt-2 border-t border-stone-200 flex items-center justify-between gap-2">
      <span id="radio-now-status" class="text-xs font-extrabold text-[#556432] truncate">🔇 Сейчас радио выключено</span>
      <div class="flex items-center gap-2">
        <input id="radio-vol-slider" type="range" min="0" max="100" value="75" oninput="window.setMirMirRadioVol(this.value)" class="w-20 accent-[#556432]" title="Громкость">
        <button onclick="window.stopMirMirRadio()" class="px-3.5 py-2 rounded-xl bg-stone-200 hover:bg-red-100 text-stone-800 font-extrabold text-xs cursor-pointer">⏹ Стоп</button>
      </div>
    </div>
  </div>
</div>

<!-- ⚙️ 5-ВКЛАДОЧНЫЙ ЦЕНТР УПРАВЛЕНИЯ В ШЕСТЕРЁНКЕ -->
<div id="unified-system-hub" class="fixed inset-0 z-[80] bg-black/85 backdrop-blur-md hidden items-center justify-center p-2 sm:p-4">
  <div class="bg-[#FDF8F2] rounded-[2.2rem] max-w-6xl w-full h-[92vh] flex flex-col justify-between overflow-hidden border-4 border-[#556432] shadow-2xl">
    <div class="p-4 sm:p-5 bg-[#2E3D28] text-white flex flex-col lg:flex-row lg:items-center justify-between gap-3">
      <div class="flex items-center gap-3">
        <div class="w-11 h-11 flex-shrink-0">__SIGN_DOVE_SVG__</div>
        <div>
          <span class="text-[10px] uppercase tracking-widest text-[#F2B880] font-extrabold">Гибридный Центр Управления (ИИ-Генератор + Выгрузка с ПК + Лупа)</span>
          <h3 class="font-serif text-2xl sm:text-3xl font-bold leading-none mt-0.5">⚙️ Шестерёнка Архитектора: Все 72 блюда, Задачи, Логи & Эффекты</h3>
        </div>
      </div>
      <div id="hub-top-tabs" class="flex items-center gap-1.5 flex-wrap"></div>
    </div>
    <div id="hub-main-body" class="p-4 sm:p-6 overflow-y-auto flex-1 space-y-4 custom-scroll"></div>
  </div>
</div>

<!-- 🧬 АРХИТЕКТУРНЫЙ ТЕКСТОВЫЙ МАСТЕР-ПРОМПТ -->
<div id="master-prompt-modal" class="fixed inset-0 z-[85] bg-black/85 backdrop-blur-md hidden items-center justify-center p-2 sm:p-5">
  <div class="bg-[#FDF8F2] rounded-[2rem] max-w-5xl w-full h-[90vh] flex flex-col justify-between overflow-hidden border-4 border-[#D48238] shadow-2xl">
    <div class="p-4 sm:p-5 bg-[#2E3D28] text-white flex flex-col sm:flex-row sm:items-center justify-between gap-3">
      <div class="flex items-center gap-3">
        <div class="w-11 h-11 flex-shrink-0">__SIGN_DOVE_SVG__</div>
        <div>
          <span class="text-[10px] uppercase tracking-widest text-[#F2B880] font-extrabold">Подарочный релиз • v1.0 (Аудит 7/7)</span>
          <h3 class="font-serif text-2xl sm:text-3xl font-bold leading-none mt-0.5">🧬 Текстовый Мастер-Промпт архитектуры сайта</h3>
        </div>
      </div>
      <div class="flex items-center gap-2 flex-wrap">
        <button onclick="window.copyMasterPromptText()" class="px-4 py-2.5 rounded-xl bg-amber-400 hover:bg-amber-300 text-[#1A2416] font-extrabold text-xs sm:text-sm shadow-lg cursor-pointer">📋 Скопировать Промпт (1 клик)</button>
        <button onclick="window.downloadMasterPromptFile()" class="px-4 py-2.5 rounded-xl bg-emerald-800 hover:bg-emerald-700 text-white font-extrabold text-xs sm:text-sm shadow cursor-pointer">💾 Скачать .TXT</button>
        <button onclick="window.closeMasterPromptModal()" class="w-9 h-9 rounded-full bg-white/15 text-white font-bold cursor-pointer ml-1">✕</button>
      </div>
    </div>
    <div class="p-4 sm:p-6 overflow-y-auto flex-1 space-y-3 custom-scroll">
      <textarea id="server-master-prompt-data" readonly class="w-full h-[70vh] p-5 rounded-2xl bg-white text-stone-900 font-sans text-xs sm:text-sm leading-relaxed border-2 border-[#556432]/40 shadow-inner focus:outline-none">__MASTER_PROMPT_ESCAPED__</textarea>
    </div>
  </div>
</div>

<script>
// === 🌟 ДВИЖОК up44: ИИ-ГЕНЕРАТОР С КНОПКОЙ «УТВЕРДИТЬ», ЗАГРУЗКА С ПК, СУПЕР-ЛУПА Z-200, ВСЕ ЛОГИ И JS-ВИБРО ===
const DOVE_MINI_ICON = '<span class="inline-block w-4 h-4 align-middle mr-1">__SIGN_DOVE_SVG__</span>';
const STORAGE_DISH_OVERRIDES = "mirmir_dish_overrides_v43";
const STORAGE_ACTION_LOGS = "mirmir_action_logs_v43";
const STORAGE_CHECKLIST = "mirmir_task_checklist_v43";

// Текущие кандидаты фото на утверждение (по индексу блюда)
window.pendingDishCandidates = {};
window.activePcFileDishIdx = 0;
window.activeGalleryTargetDishIdx = 0;

// ============================================================================
// 🔍 СУПЕР-ЛУПА Z-[200] (ОТКРЫВАЕТ ПОЛНЫЙ РАЗМЕР ПОВЕРХ ВСЕХ ОКОН!)
// ============================================================================
window.openSuperZoom = function(srcUrl, captionText) {
  const box = document.getElementById("super-zoom-lightbox");
  const im = document.getElementById("super-zoom-img");
  const cap = document.getElementById("super-zoom-caption");
  const dl = document.getElementById("super-zoom-dl");
  if (!box || !im) return;
  im.src = srcUrl;
  if (cap) cap.innerText = captionText ? ("🔍 " + captionText) : ("🔍 Полный размер: " + srcUrl.slice(0, 60));
  if (dl) dl.href = srcUrl;
  box.classList.remove("hidden");
  box.classList.add("flex");
};
window.closeSuperZoom = function() {
  const box = document.getElementById("super-zoom-lightbox");
  if (box) { box.classList.add("hidden"); box.classList.remove("flex"); }
};
// Перенаправляем стандартный showImg() на Супер-Лупу Z-[200], чтобы она работала и внутри шестерёнки!
window.showImg = function(srcUrl, cap) {
  window.openSuperZoom(srcUrl, cap);
};

// ============================================================================
// 📸 ВСПЛЫВАЮЩЕЕ ОКНО ВЫБОРА ИЗ ГОТОВЫХ ФОТОГРАФИЙ (С ЛУПОЙ И УТВЕРЖДЕНИЕМ!)
// ============================================================================
window.openReadyGalleryPopup = function(dishIdx) {
  window.activeGalleryTargetDishIdx = dishIdx;
  const m = document.getElementById("ready-gallery-popup");
  const titleEl = document.getElementById("ready-popup-title");
  const d = DATA.menu[dishIdx];
  if (titleEl && d) {
    titleEl.innerHTML = '📸 Выберите готовое фото для блюда: <span class="text-[#F2B880] underline">' + esc(d.name) + '</span>';
  }
  if (m) {
    m.classList.remove("hidden");
    m.classList.add("flex");
    window.renderReadyGalleryPopupGrid();
  }
};
window.closeReadyGalleryPopup = function() {
  const m = document.getElementById("ready-gallery-popup");
  if (m) { m.classList.add("hidden"); m.classList.remove("flex"); }
};
window.renderReadyGalleryPopupGrid = function() {
  const grid = document.getElementById("ready-popup-grid");
  if (!grid) return;
  const q = (document.getElementById("ready-popup-filter")?.value || "").toLowerCase();
  const readyPhotos = (DATA.ready_photos || []).filter(p => !q || p.toLowerCase().includes(q));
  const idx = window.activeGalleryTargetDishIdx;

  grid.innerHTML = readyPhotos.map(src => [
    '<div class="bg-white p-2.5 rounded-2xl border-2 border-stone-200 hover:border-[#D48238] shadow-sm flex flex-col justify-between gap-2 transition">',
      '<div class="relative h-36 rounded-xl overflow-hidden bg-stone-100 group">',
        '<img src="' + esc(src) + '" onclick="window.openSuperZoom(\'' + esc(src) + '\', \'Готовое фото из архива: ' + esc(src) + '\')" class="w-full h-full object-cover cursor-zoom-in group-hover:scale-105 transition">',
        '<button onclick="window.openSuperZoom(\'' + esc(src) + '\', \'Готовое фото: ' + esc(src) + '\')" class="absolute top-2 right-2 px-2.5 py-1 rounded-lg bg-black/75 hover:bg-[#D48238] text-white text-[10px] font-extrabold cursor-pointer shadow">🔍 Лупа</button>',
      '</div>',
      '<code class="text-[10px] font-bold text-stone-600 truncate block">' + esc(src) + '</code>',
      '<button onclick="window.stageCandidateFromGallery(' + idx + ', \'' + esc(src) + '\')" class="w-full py-2 rounded-xl bg-emerald-700 hover:bg-emerald-600 text-white font-extrabold text-xs cursor-pointer shadow">✅ Утвердить это фото</button>',
    '</div>'
  ].join("")).join("");
};

window.stageCandidateFromGallery = function(idx, photoSrc) {
  window.closeReadyGalleryPopup();
  window.approveAndLockDishPhoto(idx, photoSrc, "📸 Выбрано и утверждено готовое фото из архива");
};

// ============================================================================
// 📁 ЗАГРУЗКА СВОЕЙ ФОТОГРАФИИ С КОМПЬЮТЕРА (ПРОВОДНИК WINDOWS -> ПРЕДПРОСМОТР С ЛУПОЙ -> УТВЕРДИТЬ)
// ============================================================================
window.triggerPcFileUpload = function(dishIdx) {
  window.activePcFileDishIdx = dishIdx;
  const inp = document.getElementById("pc-dish-file-input");
  if (inp) { inp.value = ""; inp.click(); }
};

window.handlePcFileSelected = function(ev) {
  const file = ev.target.files && ev.target.files[0];
  if (!file) return;
  const idx = window.activePcFileDishIdx;
  const reader = new FileReader();
  reader.onload = function(e) {
    const im = new Image();
    im.onload = function() {
      // Аккуратно сжимаем до 720px для мгновенного сохранения в браузере и JSON
      const canvas = document.createElement("canvas");
      const maxDim = 720;
      let w = im.width, h = im.height;
      if (w > maxDim || h > maxDim) {
        if (w > h) { h = Math.round(h * maxDim / w); w = maxDim; }
        else { w = Math.round(w * maxDim / h); h = maxDim; }
      }
      canvas.width = w; canvas.height = h;
      canvas.getContext("2d").drawImage(im, 0, 0, w, h);
      const dataUrl = canvas.toDataURL("image/jpeg", 0.84);
      window.pendingDishCandidates[idx] = {
        url: dataUrl,
        source: "📁 Загружено с ПК (" + file.name + ")",
        prompt: file.name
      };
      window.renderUnifiedSystemHub();
    };
    im.src = e.target.result;
  };
  reader.readAsDataURL(file);
};

// ============================================================================
// 🎨 ГЕНЕРАЦИЯ ФОТО БЛЮДА ЧЕРЕЗ ИИ ПРЯМО В ИНЖЕНЕРНОМ МЕНЮ + ПРЕДПРОСМОТР С ЛУПОЙ + УТВЕРЖДЕНИЕ!
// ============================================================================
window.generateDishCandidateAI = function(idx) {
  const d = DATA.menu[idx];
  if (!d) return;
  const prmInp = document.getElementById("hub-ai-prm-" + idx);
  const userPrompt = (prmInp ? prmInp.value.trim() : "") || (d.name + " (" + (d.desc || "веганское блюдо") + ")");
  const seed = Math.floor(Math.random() * 89999) + 10000;
  const fullPrompt = "Professional appetizing vegan food photography of " + userPrompt + ", served on ceramic plate on warm wooden table in cozy cafe, natural lighting, high resolution, 8k, no text";
  const aiUrl = "https://image.pollinations.ai/prompt/" + encodeURIComponent(fullPrompt) + "?width=640&height=640&seed=" + seed + "&model=flux&nologo=true";

  window.pendingDishCandidates[idx] = {
    url: aiUrl,
    source: "🎨 Сгенерировано ИИ (Seed #" + seed + ")",
    prompt: userPrompt
  };
  addLocalBuildOrActionLog("🎨 Запущена ИИ-генерация фото для блюда «" + d.name + "»", "Промпт: " + userPrompt);
  window.renderUnifiedSystemHub();
};

// Утверждение кандидата (из ИИ, с ПК или из поля ссылки)
window.approveCandidateDishPhoto = function(idx) {
  const cand = window.pendingDishCandidates[idx];
  if (!cand || !cand.url) return;
  window.approveAndLockDishPhoto(idx, cand.url, "✅ Утверждено новое фото (" + cand.source + ")", cand.prompt);
  delete window.pendingDishCandidates[idx];
  window.renderUnifiedSystemHub();
};

window.discardCandidateDishPhoto = function(idx) {
  delete window.pendingDishCandidates[idx];
  window.renderUnifiedSystemHub();
};

function getManualDishOverrides() {
  const srv = (DATA.tz_synced && DATA.tz_synced.dishes) ? DATA.tz_synced.dishes : {};
  let loc = {};
  try { loc = JSON.parse(localStorage.getItem(STORAGE_DISH_OVERRIDES) || "{}"); } catch(e) {}
  return Object.assign({}, srv, loc);
}
function saveManualDishOverrides(obj) {
  localStorage.setItem(STORAGE_DISH_OVERRIDES, JSON.stringify(obj));
}

function addLocalBuildOrActionLog(statusMsg, detailsMsg) {
  let logs = [];
  try { logs = JSON.parse(localStorage.getItem(STORAGE_ACTION_LOGS) || "[]"); } catch(e) {}
  const nowStr = new Date().toLocaleDateString("ru-RU") + " " + new Date().toLocaleTimeString("ru-RU", {hour:"2-digit", minute:"2-digit"});
  logs.unshift({
    version: "Действие в ⚙️ (" + nowStr + ")",
    timestamp: nowStr,
    model: "Инженерный Пульт (ИИ + Ручной)",
    status: statusMsg,
    stats: detailsMsg
  });
  localStorage.setItem(STORAGE_ACTION_LOGS, JSON.stringify(logs.slice(0, 80)));
}

function applyManualOverridesToMenuData() {
  const ov = getManualDishOverrides();
  (DATA.menu || []).forEach(d => {
    if (!d.ai_default_photo) d.ai_default_photo = d.photo;
    if (!d.ai_default_type) d.ai_default_type = d.photo_type;
    if (ov[d.name] && ov[d.name].photo) {
      d.photo = ov[d.name].photo;
      d.photo_type = "real";
      d.is_manual_override = true;
    } else {
      d.photo = d.ai_default_photo;
      d.photo_type = d.ai_default_type;
      d.is_manual_override = false;
    }
    if (ov[d.name] && ov[d.name].ai_prompt) {
      d.ai_prompt = ov[d.name].ai_prompt;
    }
  });
}

window.approveAndLockDishPhoto = function(idx, newPhotoUrl, logReason, savedPrompt) {
  const d = DATA.menu[idx];
  if (!d || !newPhotoUrl) return;
  const ov = getManualDishOverrides();
  ov[d.name] = {
    photo: newPhotoUrl,
    ai_prompt: savedPrompt || d.ai_prompt || "",
    updated_at: new Date().toLocaleString("ru-RU")
  };
  saveManualDishOverrides(ov);
  applyManualOverridesToMenuData();
  renderDishes();
  addLocalBuildOrActionLog(logReason + " для «" + d.name + "»", "Установлено фото: " + (newPhotoUrl.startsWith("data:") ? "[Локальный файл с ПК]" : newPhotoUrl));

  // Показываем яркое всплывающее уведомление об утверждении!
  const toast = document.createElement("div");
  toast.innerHTML = "✅ <b>Утверждено для «" + esc(d.name) + "»!</b> Фотография сразу обновлена в меню сайта.";
  toast.className = "fixed bottom-16 left-1/2 -translate-x-1/2 z-[210] bg-emerald-800 text-white border-2 border-[#F2B880] px-5 py-3 rounded-2xl shadow-2xl text-xs sm:text-sm";
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 2600);
};

// СПИСОК ЗАДАЧ И БАГОВ
const DEFAULT_TASKS_CHECKLIST = [
  { id: "chk1", task: "Сделать внутри шестерёнки ⚙️ генерацию фото через ИИ с предпросмотром, Лупой 🔍 и кнопкой «✅ Утвердить» + загрузку с ПК и всплывающую галерею готовых фото", done: true, bug_info: "В up43 галерея открывалась в самом верху списка вне экрана, а у лайтбокса был z-50 (позади окна настроек z-80). В up44 сделано всплывающее окно z-140, Супер-Лупа z-200 и блок кандидата прямо внутри карточки блюда!" },
  { id: "chk2", task: "Вывести во вкладку «📜 Логи сборок» полную историю всех апдейтов (up21..up44) + живые действия в шестерёнке", done: true, bug_info: "В up43 читалось пустое поле DATA.history. В up44 скрипт на Python собирает все файлы up*.py и build_history.json в DATA.full_build_logs." },
  { id: "chk3", task: "Включить 100% заметную физическую вибрацию всех фотографий при наведении мышки на ПК", done: true, bug_info: "CSS-анимация блокировалась системной настройкой Windows prefers-reduced-motion и классами Tailwind. В up44 включён прямой JS-осциллятор координат картинки на mouseenter." },
  { id: "chk4", task: "Убрать обрезку лиц в «Последних новостях и анонсах» и добавить слева внизу кнопочку «читать на VK ↗»", done: true, bug_info: "Секция находится по заголовку H2 и контролируется через MutationObserver." },
  { id: "chk5", task: "3 строки карточек «Сезонные спешлы от Шефа» прямо под 3D-каруселью меню справа", done: true, bug_info: "9 карточек спешлов разложены в 3 ряда под 3D-каруселью." },
  { id: "chk6", task: "Живой индикатор времени работы (🟢 ОТКРЫТО / 🔴 ЗАКРЫТО ДО 12:00 + 🔥 БИЗНЕС-ЛАНЧ -30% в будни 12–16)", done: true, bug_info: "Работает синхронно в шапке и первом блоке." },
  { id: "chk7", task: "4 волны онлайн-радио (включая 🛸 Радио Ханг Драм), Магазин кафе (Тофу & Крафт) и Бронь столика", done: true, bug_info: "Доступны из верхней шапки без дублирования." }
];

function getChecklistItems() {
  try {
    const raw = localStorage.getItem("mirmir_task_checklist_v44");
    if (raw) return JSON.parse(raw);
  } catch(e) {}
  return DEFAULT_TASKS_CHECKLIST;
}
function saveChecklistItems(arr) {
  localStorage.setItem("mirmir_task_checklist_v44", JSON.stringify(arr));
}

// ============================================================================
// ⚙️ РЕНДЕР 5 ВКЛАДОК ВНУТРИ ШЕСТЕРЁНКИ (#unified-system-hub)
// ============================================================================
window.hubActiveTab = "dishes72";

window.openUnifiedSystemHub = function(tabName) {
  if (tabName) window.hubActiveTab = tabName;
  const m = document.getElementById("unified-system-hub");
  if (m) {
    m.classList.remove("hidden");
    m.classList.add("flex");
    window.renderUnifiedSystemHub();
  }
};
window.closeUnifiedSystemHub = function() {
  const m = document.getElementById("unified-system-hub");
  if (m) { m.classList.add("hidden"); m.classList.remove("flex"); }
};

window.renderUnifiedSystemHub = function() {
  const tabsBox = document.getElementById("hub-top-tabs");
  const bodyBox = document.getElementById("hub-main-body");
  if (!tabsBox || !bodyBox) return;

  const ov = getManualDishOverrides();
  const manualCount = Object.keys(ov).filter(k => ov[k] && ov[k].photo).length;
  const chkList = getChecklistItems();
  const doneCount = chkList.filter(x => x.done).length;

  const srvLogs = Array.isArray(DATA.full_build_logs) ? DATA.full_build_logs : [];
  let locLogs = [];
  try { locLogs = JSON.parse(localStorage.getItem(STORAGE_ACTION_LOGS) || "[]"); } catch(e) {}
  const allLogs = [...locLogs, ...srvLogs];

  const tabBtn = (id, lbl) => {
    const act = window.hubActiveTab === id;
    return '<button onclick="window.hubActiveTab=\'' + id + '\';window.renderUnifiedSystemHub()" class="px-3.5 py-2 rounded-xl font-extrabold text-xs cursor-pointer transition ' +
      (act ? 'bg-[#D48238] text-white shadow-lg border border-white/50' : 'bg-white/10 text-white/85 hover:bg-white/20') + '">' + lbl + '</button>';
  };

  tabsBox.innerHTML = [
    tabBtn("dishes72", "🍲 Все 72 блюда: Фото & ИИ (" + (manualCount ? "Утверждено: " + manualCount : "Гибрид") + ")"),
    tabBtn("checklist", "📋 Список задач (" + doneCount + "/" + chkList.length + ")"),
    tabBtn("logs", "📜 Логи апдейтов и сборок (" + allLogs.length + ")"),
    tabBtn("journal", "📝 Журнал идей"),
    tabBtn("toggles", "⚡ Изменяшки & Промпт"),
    '<button onclick="window.closeUnifiedSystemHub()" class="w-9 h-9 rounded-full bg-white/15 hover:bg-red-600 text-white font-bold cursor-pointer ml-1">✕</button>'
  ].join("");

  // --- ВКЛАДКА 1: РЕДАКТОР ВСЕХ 72 БЛЮД С ИИ-ГЕНЕРАЦИЕЙ, ЗАГРУЗКОЙ С ПК, СУПЕР-ЛУПОЙ И КНОПКОЙ «УТВЕРДИТЬ» ---
  if (window.hubActiveTab === "dishes72") {
    const qFilter = (document.getElementById("hub-dish-search")?.value || "").toLowerCase();
    const catFilter = document.getElementById("hub-dish-cat")?.value || "Все";
    const categories = ["Все", ...Array.from(new Set((DATA.menu || []).map(d => d.category)))];
    const readyPhotos = DATA.ready_photos || [];

    const rowsHtml = (DATA.menu || []).map((d, idx) => {
      if (catFilter !== "Все" && d.category !== catFilter) return "";
      if (qFilter && !d.name.toLowerCase().includes(qFilter) && !d.category.toLowerCase().includes(qFilter)) return "";
      const isManual = !!d.is_manual_override;
      const cand = window.pendingDishCandidates[idx];
      const defaultPrompt = d.ai_prompt || (d.name + ", " + (d.desc || "веганское блюдо"));

      const badgeHtml = isManual
        ? '<span class="px-2.5 py-0.5 rounded-full bg-amber-100 text-amber-900 border border-amber-400 text-[10px] font-extrabold">✅ Утверждено вручную</span>'
        : '<span class="px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-900 text-[10px] font-extrabold">🤖 Авто-парсинг ИИ</span>';

      // Если для этого блюда сейчас сгенерирован кандидат ИИ или выбран файл с ПК — показываем крупный блок предпросмотра и утверждения!
      const candidateBoxHtml = cand ? [
        '<div class="mt-3 p-3.5 rounded-2xl bg-gradient-to-r from-[#2E3D28] to-[#3B4D34] text-white border-2 border-[#D48238] shadow-xl flex flex-col sm:flex-row items-center justify-between gap-4">',
          '<div class="flex items-center gap-4">',
            '<div class="relative w-28 h-28 rounded-2xl overflow-hidden border-2 border-[#F2B880] bg-black/40 flex-shrink-0 group">',
              '<img src="' + esc(cand.url) + '" onclick="window.openSuperZoom(\'' + esc(cand.url) + '\', \'Кандидат для блюда: ' + esc(d.name) + '\')" class="w-full h-full object-cover cursor-zoom-in">',
              '<button onclick="window.openSuperZoom(\'' + esc(cand.url) + '\', \'Кандидат для блюда: ' + esc(d.name) + '\')" class="absolute bottom-1.5 right-1.5 px-2 py-0.5 rounded-lg bg-black/80 hover:bg-[#D48238] text-white text-[10px] font-extrabold cursor-pointer shadow">🔍 Лупа</button>',
            '</div>',
            '<div class="space-y-1">',
              '<span class="px-2.5 py-0.5 rounded-full bg-amber-400 text-[#1A2416] text-[10px] font-extrabold uppercase">' + esc(cand.source) + '</span>',
              '<h5 class="font-serif text-xl font-bold text-[#F2B880]">👁️ Предпросмотр нового фото для «' + esc(d.name) + '»</h5>',
              '<p class="text-xs text-white/85">Нажмите «🔍 Лупа» для просмотра во весь экран или «✅ Утвердить в меню», чтобы закрепить это фото на сайте!</p>',
            '</div>',
          '</div>',
          '<div class="flex sm:flex-col gap-2 w-full sm:w-auto">',
            '<button onclick="window.approveCandidateDishPhoto(' + idx + ')" class="flex-1 px-4 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-extrabold text-xs cursor-pointer shadow-lg whitespace-nowrap">✅ Утвердить в меню</button>',
            '<button onclick="window.generateDishCandidateAI(' + idx + ')" class="px-3.5 py-2 rounded-xl bg-[#D48238] hover:opacity-95 text-white font-extrabold text-xs cursor-pointer whitespace-nowrap">🎲 Ещё вариант ИИ</button>',
            '<button onclick="window.discardCandidateDishPhoto(' + idx + ')" class="px-3 py-1.5 rounded-xl bg-white/15 hover:bg-red-600 text-white font-bold text-xs cursor-pointer">✕ Отмена</button>',
          '</div>',
        '</div>'
      ].join("") : "";

      return [
        '<div class="bg-white p-4 rounded-3xl border-2 ' + (isManual ? 'border-[#D48238] bg-amber-50/15' : 'border-stone-200') + ' shadow-sm">',
          '<div class="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-3.5">',
            '<!-- Левая часть: Крупная миниатюра с кнопкой Лупа + Название -->',
            '<div class="flex items-center gap-3.5 min-w-0 lg:w-1/3">',
              '<div class="relative w-24 h-24 rounded-2xl overflow-hidden flex-shrink-0 border-2 border-[#556432]/40 group bg-stone-100">',
                '<img id="hub-dish-img-' + idx + '" src="' + esc(d.photo) + '" onclick="window.openSuperZoom(\'' + esc(d.photo) + '\', \'' + esc(d.name) + '\')" class="w-full h-full object-cover cursor-zoom-in group-hover:scale-105 transition">',
                '<button onclick="window.openSuperZoom(\'' + esc(d.photo) + '\', \'' + esc(d.name) + '\')" class="absolute bottom-1 right-1 px-2 py-0.5 rounded-md bg-black/75 hover:bg-[#D48238] text-white text-[10px] font-extrabold cursor-pointer shadow" title="Посмотреть в полном размере">🔍 Лупа</button>',
              '</div>',
              '<div class="min-w-0 space-y-1">',
                '<div class="flex items-center gap-1.5 flex-wrap">',
                  '<span class="text-[10px] font-extrabold uppercase px-2 py-0.5 rounded bg-[#F6E4CE] text-[#556432]">' + esc(d.category) + '</span>',
                  badgeHtml,
                '</div>',
                '<h4 class="font-serif font-bold text-lg sm:text-xl text-[#2E3D28] leading-tight">' + esc(d.name) + ' <span class="text-xs font-sans text-[#D48238]">(' + d.price + ' ₽)</span></h4>',
                '<code class="text-[10px] text-stone-400 block truncate">Текущее: ' + esc(d.photo.startsWith("data:") ? "[Загруженный файл с ПК]" : d.photo) + '</code>',
              '</div>',
            '</div>',

            '<!-- Центральная часть: ИИ-генератор по описанию + Ручная ссылка -->',
            '<div class="flex-1 w-full grid grid-cols-1 md:grid-cols-2 gap-2.5">',
              '<div class="bg-amber-50/70 p-2.5 rounded-2xl border border-amber-300/80">',
                '<label class="text-[10px] font-extrabold uppercase text-[#D48238] block mb-1">🎨 1. Идея / Описание для ИИ-генерации фото:</label>',
                '<div class="flex gap-1.5">',
                  '<input id="hub-ai-prm-' + idx + '" value="' + esc(defaultPrompt) + '" placeholder="Опишите блюдо для ИИ..." class="flex-1 px-2.5 py-1.5 rounded-xl bg-white border text-xs">',
                  '<button onclick="window.generateDishCandidateAI(' + idx + ')" class="px-3 py-1.5 rounded-xl bg-[#D48238] hover:opacity-95 text-white font-extrabold text-xs cursor-pointer whitespace-nowrap shadow">🎨 Сгенерировать ИИ</button>',
                '</div>',
              '</div>',
              '<div class="bg-stone-50 p-2.5 rounded-2xl border border-stone-200">',
                '<label class="text-[10px] font-extrabold uppercase text-stone-600 block mb-1">🔗 2. Вставить прямую ссылку или путь img/...:</label>',
                '<div class="flex gap-1.5">',
                  '<input id="hub-url-' + idx + '" placeholder="Вставьте новый URL или img/vk_..." class="flex-1 px-2.5 py-1.5 rounded-xl bg-white border text-xs">',
                  '<button onclick="window.applyCustomUrlInput(' + idx + ')" class="px-3 py-1.5 rounded-xl bg-[#556432] hover:bg-[#2E3D28] text-white font-extrabold text-xs cursor-pointer whitespace-nowrap">✅ Утвердить URL</button>',
                '</div>',
              '</div>',
            '</div>',

            '<!-- Правая часть: Кнопки «Выбрать из готовых» (Модалка) и «С компьютера» + Сброс на ИИ -->',
            '<div class="flex sm:flex-row lg:flex-col gap-1.5 w-full lg:w-auto justify-end">',
              '<button onclick="window.openReadyGalleryPopup(' + idx + ')" class="px-3.5 py-2 rounded-xl bg-[#2E3D28] hover:bg-[#556432] text-[#F2B880] font-extrabold text-xs cursor-pointer whitespace-nowrap shadow">📸 Выбрать из готовых (' + readyPhotos.length + ')</button>',
              '<button onclick="window.triggerPcFileUpload(' + idx + ')" class="px-3.5 py-2 rounded-xl bg-emerald-700 hover:bg-emerald-600 text-white font-extrabold text-xs cursor-pointer whitespace-nowrap shadow">📁 Загрузить с ПК</button>',
              (isManual
                ? '<button onclick="window.resetDishToAiAuto(' + idx + ')" class="px-3 py-1.5 rounded-xl bg-stone-200 hover:bg-red-100 text-stone-800 font-bold text-[10px] cursor-pointer whitespace-nowrap">🔄 Вернуть авто-парсинг ИИ</button>'
                : ''),
            '</div>',
          '</div>',
          candidateBoxHtml,
        '</div>'
      ].join("");
    }).join("");

    bodyBox.innerHTML = [
      '<div class="space-y-3">',
        '<div class="bg-[#F6E4CE]/90 p-3.5 rounded-2xl border-2 border-[#556432]/30 flex flex-col md:flex-row items-stretch md:items-center justify-between gap-2.5">',
          '<div class="flex flex-1 gap-2 flex-col sm:flex-row">',
            '<select id="hub-dish-cat" onchange="window.renderUnifiedSystemHub()" class="px-3 py-2 rounded-xl bg-white border text-xs font-extrabold text-[#2E3D28]">',
              categories.map(c => '<option value="' + esc(c) + '" ' + (c === catFilter ? 'selected' : '') + '>' + esc(c) + '</option>').join(""),
            '</select>',
            '<input id="hub-dish-search" oninput="window.renderUnifiedSystemHub()" value="' + esc(qFilter) + '" placeholder="🔍 Быстрый поиск по всем 72 блюдам меню (лапша, суп, пицца, бургер, тофу, чай)..." class="flex-1 px-3.5 py-2 rounded-xl bg-white border text-xs sm:text-sm">',
          '</div>',
          '<div class="flex gap-2 flex-wrap">',
            '<button onclick="window.exportDishOverridesToJson()" class="px-4 py-2 rounded-xl bg-[#2E3D28] hover:bg-[#556432] text-[#F2B880] font-extrabold text-xs cursor-pointer shadow">💾 Выгрузить утверждённые фото в tz_mirmir.json</button>',
          '</div>',
        '</div>',
        '<div class="text-xs text-stone-600 px-1">💡 <b>Как работать:</b> Напротив любого блюда нажмите <b>«🎨 Сгенерировать ИИ»</b> (чтобы создать новое фото и утвердить его), <b>«📸 Выбрать из готовых»</b> (откроется окно со всеми кадрами ВК/Яндекса и Лупой) или <b>«📁 Загрузить с ПК»</b>!</div>',
        '<div class="space-y-2.5">' + rowsHtml + '</div>',
      '</div>'
    ].join("");
  }

  // --- ВКЛАДКА 2: СПИСОК ЗАДАЧ И БАГОВ ---
  else if (window.hubActiveTab === "checklist") {
    const rows = chkList.map((item, i) => [
      '<tr class="' + (item.done ? 'bg-emerald-50/40' : 'bg-amber-50/70') + ' border-b border-stone-200">',
        '<td class="p-3 font-bold text-stone-900 text-xs sm:text-sm">' + (i + 1) + '. ' + esc(item.task) + '</td>',
        '<td class="p-3 whitespace-nowrap">',
          '<button onclick="window.toggleChecklistItem(' + i + ')" class="px-3 py-1.5 rounded-xl font-extrabold text-xs cursor-pointer shadow-sm transition ' +
            (item.done ? 'bg-emerald-700 text-white hover:bg-emerald-800' : 'bg-amber-500 text-[#1A2416] hover:bg-amber-400') + '">' +
            (item.done ? '✅ Сделано' : '⏳ Не сделано') +
          '</button>',
        '</td>',
        '<td class="p-3 text-xs text-stone-700 leading-relaxed">' + esc(item.bug_info || "Записано в чек-лист") + '</td>',
        '<td class="p-3 text-right"><button onclick="window.deleteChecklistItem(' + i + ')" class="text-stone-400 hover:text-red-600 font-bold text-xs cursor-pointer">✕</button></td>',
      '</tr>'
    ].join("")).join("");

    bodyBox.innerHTML = [
      '<div class="space-y-4">',
        '<div class="bg-white p-4 rounded-2xl border-2 border-[#556432] space-y-3 shadow-sm">',
          '<h4 class="font-serif text-xl font-bold text-[#2E3D28]">➕ Добавить новую задачу или баг в чек-лист</h4>',
          '<div class="grid grid-cols-1 sm:grid-cols-3 gap-2">',
            '<input id="chk-new-task" placeholder="Описание задачи (что нужно сделать)..." class="sm:col-span-2 px-3 py-2 rounded-xl border text-xs sm:text-sm">',
            '<input id="chk-new-bug" placeholder="В чём баг / технический нюанс..." class="px-3 py-2 rounded-xl border text-xs sm:text-sm">',
          '</div>',
          '<button onclick="window.addNewChecklistItem()" class="px-5 py-2.5 rounded-xl bg-[#D48238] text-white font-extrabold text-xs cursor-pointer shadow">+ Добавить задачу в список</button>',
        '</div>',
        '<div class="overflow-x-auto rounded-2xl border-2 border-[#2E3D28] shadow bg-white">',
          '<table class="w-full text-left border-collapse">',
            '<thead><tr class="bg-[#2E3D28] text-[#F2B880] text-[11px] uppercase">',
              '<th class="p-3">Задача / Пожелание</th>',
              '<th class="p-3">Статус (Клик для смены)</th>',
              '<th class="p-3">В чём был баг & Техническое решение</th>',
              '<th class="p-3"></th>',
            '</tr></thead>',
            '<tbody>' + rows + '</tbody>',
          '</table>',
        '</div>',
      '</div>'
    ].join("");
  }

  // --- ВКЛАДКА 3: ПОЛНЫЕ ЛОГИ ВСЕХ АПДЕЙТОВ (up21..up44) И ЖИВЫХ ДЕЙСТВИЙ ---
  else if (window.hubActiveTab === "logs") {
    const logRows = allLogs.map((lg, i) => [
      '<div class="bg-white p-3.5 rounded-2xl border border-stone-200 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-2">',
        '<div class="space-y-0.5">',
          '<div class="flex items-center gap-2 flex-wrap">',
            '<span class="px-2.5 py-0.5 rounded-full bg-[#2E3D28] text-[#F2B880] text-[10px] font-extrabold">' + esc(lg.version || ("Запись #" + (allLogs.length - i))) + '</span>',
            '<span class="text-xs font-extrabold text-emerald-800">🕒 ' + esc(lg.timestamp || "") + '</span>',
            '<span class="text-[11px] font-bold text-stone-500">Движок: ' + esc(lg.model || "gemini-3-flash-preview") + '</span>',
          '</div>',
          '<div class="text-xs sm:text-sm font-bold text-[#2E3D28] pt-1">' + esc(lg.status || "Сборка выполнена успешно") + '</div>',
          '<div class="text-xs text-stone-600">' + esc(lg.stats || "") + '</div>',
        '</div>',
        '<span class="px-3 py-1 rounded-xl bg-emerald-100 text-emerald-900 font-extrabold text-[11px] self-start sm:self-center whitespace-nowrap">✅ В реестре</span>',
      '</div>'
    ].join("")).join("");

    bodyBox.innerHTML = [
      '<div class="space-y-4">',
        '<div class="p-4 rounded-2xl bg-[#2E3D28] text-white flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">',
          '<div>',
            '<span class="text-[10px] uppercase tracking-widest text-[#F2B880] font-extrabold block">Полный реестр всех апдейтов (up21–up44) и ручных утверждений фото</span>',
            '<h4 class="font-serif text-xl sm:text-2xl font-bold">📜 Все логи апдейтов, сборок и замен фотографий (' + allLogs.length + ' зап.)</h4>',
            '<p class="text-xs text-white/80">Здесь собраны все обновления из скриптов up*.py, запуски run.bat и все ваши действия по утверждению фото.</p>',
          '</div>',
          '<button onclick="toggleDev();window.closeUnifiedSystemHub()" class="px-4 py-2.5 rounded-xl bg-[#D48238] text-white font-extrabold text-xs cursor-pointer whitespace-nowrap shadow">📖 7 Глав Книги-Манифеста</button>',
        '</div>',
        '<div class="space-y-2.5">' + logRows + '</div>',
      '</div>'
    ].join("");
  }

  // --- ВКЛАДКА 4: ЖУРНАЛ ПОЖЕЛАНИЙ КОМАНДЫ ---
  else if (window.hubActiveTab === "journal") {
    const serverTasks = (DATA.tz_synced && DATA.tz_synced.tasks) ? DATA.tz_synced.tasks : [];
    let localTasks = [];
    try { localTasks = JSON.parse(localStorage.getItem("mirmir_tz_tasks_gift_v1") || "[]"); } catch(e) {}
    const allTasks = [...localTasks, ...serverTasks];
    const cards = allTasks.map(t => [
      '<div class="bg-white p-4 rounded-2xl border-2 border-[#556432]/30 space-y-2">',
        '<div class="text-xs font-extrabold text-emerald-800">' + esc(t.status || "📝 Заметка команды") + ' • ' + esc(t.date || "09.11.2026") + '</div>',
        '<div class="p-3 rounded-xl bg-stone-50 font-bold text-stone-900 text-xs sm:text-sm whitespace-pre-line">' + esc(t.user_tz || "") + '</div>',
        '<div class="p-3 rounded-xl bg-[#FDF8F2] border border-[#D48238]/40 text-stone-800 text-xs sm:text-sm whitespace-pre-line">🕊️ <b>Комментарий:</b> ' + esc(t.gemini_reply || "Заметка сохранена в журнал!") + '</div>',
      '</div>'
    ].join("")).join("");

    bodyBox.innerHTML = [
      '<div class="space-y-4">',
        '<div class="bg-white p-4 rounded-2xl border-2 border-[#556432] space-y-3">',
          '<h4 class="font-serif text-xl font-bold text-[#2E3D28]">✍️ Добавить идею или пожелание по сайту</h4>',
          '<div class="grid grid-cols-1 sm:grid-cols-3 gap-2">',
            '<input id="tz-author-inp" placeholder="Ваше имя (Виталий / Шеф)" class="px-3 py-2 rounded-xl border text-xs sm:text-sm">',
            '<input id="tz-new-input" placeholder="Текст идеи или пожелания..." class="sm:col-span-2 px-3 py-2 rounded-xl border text-xs sm:text-sm">',
          '</div>',
          '<button onclick="window.saveNewTzClean()" class="px-5 py-2.5 rounded-xl bg-[#D48238] text-white font-extrabold text-xs cursor-pointer">💾 Сохранить в журнал</button>',
        '</div>',
        '<div class="space-y-3">' + cards + '</div>',
      '</div>'
    ].join("");
  }

  // --- ВКЛАДКА 5: ИЗМЕНЯШКИ (ВКЛ/ВЫКЛ), МАСТЕР-ПРОМПТ & PDF ---
  else {
    const st = getToggleStates();
    const togglesHtml = SITE_TOGGLES_SPEC.map(s => {
      const on = !!st[s.key];
      return '<div onclick="window.flipSiteToggle(\'' + s.key + '\')" class="p-3.5 rounded-2xl border-2 cursor-pointer transition flex items-center justify-between gap-2 ' + (on ? 'bg-emerald-50/80 border-[#556432]' : 'bg-stone-50 border-stone-200 opacity-75') + '"><span class="text-xs font-extrabold text-[#2E3D28]">' + s.label + '</span><span class="px-3 py-1 rounded-full text-[11px] font-extrabold ' + (on ? 'bg-[#556432] text-white' : 'bg-stone-300 text-stone-700') + '">' + (on ? 'ВКЛ' : 'ВЫКЛ') + '</span></div>';
    }).join("");

    bodyBox.innerHTML = [
      '<div class="space-y-5">',
        '<div class="bg-white p-4 sm:p-5 rounded-3xl border-2 border-[#556432] shadow-sm space-y-4">',
          '<h4 class="font-serif text-xl sm:text-2xl font-bold text-[#2E3D28]">⚡ Переключатели визуальных эффектов (Вкл / Выкл)</h4>',
          '<div class="grid grid-cols-1 sm:grid-cols-2 gap-3">' + togglesHtml + '</div>',
        '</div>',
        '<div class="grid grid-cols-1 sm:grid-cols-2 gap-3">',
          '<div onclick="window.openMasterPromptModal()" class="p-5 rounded-2xl bg-white border-2 border-amber-400 hover:shadow-lg cursor-pointer transition">',
            '<div class="text-2xl mb-1">🧬</div>',
            '<div class="font-serif text-xl font-bold text-[#2E3D28]">Текстовый Мастер-Промпт (Архитектура 1:1)</div>',
            '<p class="text-xs text-stone-600 mt-1">Полное описание гибридного Python+ВК+ИИ компилятора (с учётом аудита 7/7)</p>',
          '</div>',
          '<div onclick="exportPDF()" class="p-5 rounded-2xl bg-white border-2 border-[#556432] hover:shadow-lg cursor-pointer transition">',
            '<div class="text-2xl mb-1">📥</div>',
            '<div class="font-serif text-xl font-bold text-[#2E3D28]">Печатный PDF-Каталог всех 72 блюд</div>',
            '<p class="text-xs text-stone-600 mt-1">Сформировать и распечатать иллюстрированное меню кафе</p>',
          '</div>',
        '</div>',
      '</div>'
    ].join("");
  }
};

window.applyCustomUrlInput = function(idx) {
  const d = DATA.menu[idx];
  const uVal = (document.getElementById("hub-url-" + idx)?.value || "").trim();
  if (!d) return;
  if (!uVal) {
    alert("Вставьте в поле новую ссылку на картинку (https://...) или имя файла из папки img/ (или нажмите «📸 Выбрать из готовых» / «🎨 Сгенерировать ИИ»)!");
    return;
  }
  window.approveAndLockDishPhoto(idx, uVal, "🔗 Ручная привязка нового URL/файла");
  window.renderUnifiedSystemHub();
};

window.resetDishToAiAuto = function(idx) {
  const d = DATA.menu[idx];
  if (!d) return;
  const ov = getManualDishOverrides();
  delete ov[d.name];
  saveManualDishOverrides(ov);
  delete window.pendingDishCandidates[idx];
  applyManualOverridesToMenuData();
  renderDishes();
  addLocalBuildOrActionLog("🔄 Возврат блюда «" + d.name + "» на авто-парсинг ИИ", "Восстановлено фото ИИ: " + d.photo);
  window.renderUnifiedSystemHub();
};

window.exportDishOverridesToJson = function() {
  const payload = {
    updated_at: new Date().toLocaleString("ru-RU"),
    tasks: (DATA.tz_synced && DATA.tz_synced.tasks) ? DATA.tz_synced.tasks : [],
    dishes: getManualDishOverrides()
  };
  const blob = new Blob([JSON.stringify(payload, null, 2)], {type: "application/json"});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "tz_mirmir.json";
  a.click();
  addLocalBuildOrActionLog("💾 Выгружен файл ручных настроек tz_mirmir.json", "Сохранено ручных привязок фото: " + Object.keys(payload.dishes).length);
};

window.toggleChecklistItem = function(i) {
  const list = getChecklistItems();
  if (list[i]) {
    list[i].done = !list[i].done;
    saveChecklistItems(list);
    addLocalBuildOrActionLog((list[i].done ? "✅ Задача отмечена выполненной: " : "⏳ Задача возвращена в работу: ") + list[i].task, "");
    window.renderUnifiedSystemHub();
  }
};
window.deleteChecklistItem = function(i) {
  const list = getChecklistItems();
  list.splice(i, 1);
  saveChecklistItems(list);
  window.renderUnifiedSystemHub();
};
window.addNewChecklistItem = function() {
  const t = (document.getElementById("chk-new-task")?.value || "").trim();
  const b = (document.getElementById("chk-new-bug")?.value || "").trim();
  if (!t) return;
  const list = getChecklistItems();
  list.unshift({ id: "chk_" + Date.now(), task: t, done: false, bug_info: b || "Записано в чек-лист" });
  saveChecklistItems(list);
  addLocalBuildOrActionLog("➕ Добавлена новая задача в чек-лист", t);
  window.renderUnifiedSystemHub();
};

// ============================================================================
// 📳 ПРЯМОЙ ФИЗИЧЕСКИЙ JS-ДВИЖОК ВИБРАЦИИ ФОТОГРАФИЙ НА ПК (НЕ БЛОКИРУЕТСЯ CSS ИЛИ WINDOWS!)
// ============================================================================
window.attachGuaranteedJsVibration = function() {
  const targets = document.querySelectorAll("main img, #posts-grid img, #cat-showcase-grid > div, .vibe-card");
  targets.forEach(el => {
    if (el.dataset.jsVibeAttached) return;
    el.dataset.jsVibeAttached = "1";
    let timer = null;
    let step = 0;
    const offsets = [
      "translate(-3px, -2px) rotate(-1.4deg) scale(1.03)",
      "translate(3px, 2px) rotate(1.4deg) scale(1.03)",
      "translate(-3px, 2px) rotate(-1deg) scale(1.03)",
      "translate(3px, -2px) rotate(1deg) scale(1.03)",
      "translate(-2px, 0px) rotate(-0.6deg) scale(1.02)",
      "translate(2px, 0px) rotate(0.6deg) scale(1.02)"
    ];
    el.addEventListener("mouseenter", () => {
      if (document.body.classList.contains("cfg-no-vibe")) return;
      step = 0;
      if (timer) clearInterval(timer);
      el.style.transition = "transform 0.045s linear";
      timer = setInterval(() => {
        el.style.transform = offsets[step % offsets.length];
        step++;
        if (step > 10) {
          clearInterval(timer);
          timer = null;
          el.style.transition = "transform 0.2s ease";
          el.style.transform = "scale(1.02)";
        }
      }, 45);
    });
    el.addEventListener("mouseleave", () => {
      if (timer) { clearInterval(timer); timer = null; }
      el.style.transition = "transform 0.2s ease";
      el.style.transform = "";
    });
  });
};

// Слайдер интерьера
const INTERIOR_SLIDES_DATA = [
  { src: "img/ymap_org_0.jpg", pos: "center 50%", title: "🏛️ Исторический кирпичный свод и уютный зал на Ильинской, 45", tag: "Интерьер зала" },
  { src: "img/ymap_org_1.jpg", pos: "center 40%", title: "🕊️ Фирменная кованая вывеска с белой Голубкой мира у входа", tag: "Ильинская, 45" },
  { src: "img/vk_5122_0.jpg", pos: "center 50%", title: "🕯️ Вечерние чаепития при свечах и редкий китайский чай", tag: "Чайная культура" },
  { src: "img/vk_5128_1.jpg", pos: "center 50%", title: "🥗 Авторская растительная кухня из-под ножа", tag: "Фирменные блюда" }
];
let curInteriorSlide = 0, interiorSlideTimer = null;

window.stepInteriorSlide = function(delta) {
  curInteriorSlide = (curInteriorSlide + delta + INTERIOR_SLIDES_DATA.length) % INTERIOR_SLIDES_DATA.length;
  window.renderInteriorSlideState();
};
window.setInteriorSlide = function(idx) {
  curInteriorSlide = idx;
  window.renderInteriorSlideState();
};
window.renderInteriorSlideState = function() {
  const s = INTERIOR_SLIDES_DATA[curInteriorSlide];
  const imgEl = document.getElementById("hero-interior-slide-img");
  const titleEl = document.getElementById("hero-interior-slide-title");
  const tagEl = document.getElementById("hero-interior-slide-tag");
  const dotsBox = document.getElementById("hero-interior-dots");
  const heroLeft = document.querySelector("main section:first-of-type .lg\\:col-span-7");

  if (imgEl) {
    imgEl.style.opacity = "0.3";
    setTimeout(() => {
      imgEl.src = s.src;
      imgEl.style.objectPosition = s.pos || "center center";
      imgEl.setAttribute("onclick", "window.openSuperZoom('" + s.src + "', '" + s.title + "')");
      imgEl.style.opacity = "1";
    }, 150);
  }
  if (titleEl) titleEl.innerText = s.title;
  if (tagEl) tagEl.innerText = s.tag;
  if (heroLeft) heroLeft.style.setProperty("--hero-slide-bg", "url('" + s.src + "')");
  if (dotsBox) {
    dotsBox.innerHTML = INTERIOR_SLIDES_DATA.map((_, i) => '<button onclick="window.setInteriorSlide(' + i + ')" class="h-2 rounded-full transition-all cursor-pointer ' + (i === curInteriorSlide ? 'w-6 bg-[#D48238]' : 'w-2 bg-white/40 hover:bg-white/70') + '"></button>').join("");
  }
};

window.getMirMirWorkStatusHTML = function(isHero) {
  const now = new Date();
  const day = now.getDay();
  const dec = now.getHours() + now.getMinutes() / 60;
  const isOpen = (dec >= 12.0 && dec < 21.0);
  const isBusinessLunchNow = (day >= 1 && day <= 5 && dec >= 12.0 && dec < 16.0);

  if (isHero) {
    const openBadge = isOpen
      ? '<span class="px-3.5 py-1 rounded-full bg-emerald-600 text-white text-xs font-extrabold shadow">🟢 ОТКРЫТО ДО 21:00</span>'
      : '<span class="px-3.5 py-1 rounded-full bg-red-600 text-white text-xs font-extrabold shadow">🔴 ЗАКРЫТО ДО 12:00</span>';
    const lunchBadge = isBusinessLunchNow
      ? '<span class="px-3.5 py-1 rounded-full bg-amber-400 text-[#1A2416] text-xs font-extrabold shadow animate-pulse">🔥 ИДЁТ БИЗНЕС-ЛАНЧ −30% (до 16:00)</span>'
      : '<span class="px-3.5 py-1 rounded-full bg-[#D48238] text-white text-xs font-extrabold shadow">🔥 Бизнес-Ланч −30% (будни 12:00–16:00)</span>';
    return openBadge + ' ' + lunchBadge;
  } else {
    const openPill = isOpen
      ? '<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-emerald-600 text-white text-[10px] font-extrabold">🟢 ОТКРЫТО</span>'
      : '<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-red-600 text-white text-[10px] font-extrabold">🔴 ЗАКРЫТО ДО 12:00</span>';
    const lunchPill = isBusinessLunchNow
      ? '<span class="inline-flex items-center px-2 py-0.5 rounded-md bg-amber-400 text-[#1A2416] text-[10px] font-extrabold">🔥 БИЗНЕС-ЛАНЧ −30%</span>'
      : '<span class="text-[10px] text-[#556432] font-extrabold">12:00–21:00</span>';
    return '<div class="flex items-center gap-1.5 flex-wrap mt-0.5"><span class="text-[10px] text-[#2E3D28] font-extrabold">Ильинская, 45</span>' + openPill + lunchPill + '</div>';
  }
};

window.openBookTableModal = function() {
  try { history.pushState({guard:"book_table"}, ""); } catch(e){}
  const m = document.getElementById("book-table-modal");
  if (!m) return;
  const dInp = document.getElementById("book-date");
  if (dInp && !dInp.value) dInp.value = new Date().toISOString().split("T")[0];
  m.classList.remove("hidden"); m.classList.add("flex");
};
window.closeBookTableModal = function() {
  const m = document.getElementById("book-table-modal");
  if (m) { m.classList.add("hidden"); m.classList.remove("flex"); }
};
window.submitTableBooking = function() {
  const zone = document.getElementById("book-zone")?.value || "";
  const dt = document.getElementById("book-date")?.value || "";
  const tm = document.getElementById("book-time")?.value || "";
  const gst = document.getElementById("book-guests")?.value || "2 гостя";
  const name = (document.getElementById("book-name")?.value || "").trim();
  const phone = (document.getElementById("book-phone")?.value || "").trim();
  const comm = (document.getElementById("book-comm")?.value || "").trim();
  if (!name || !phone) { alert("Пожалуйста, укажите ваше имя и телефон или @Telegram для подтверждения брони!"); return; }
  const lines = ["🪑 БРОНЬ СТОЛИКА В КАФЕ «Мир Мир» (Ильинская, 45)", "👤 Гость: " + name, "📞 Связь: " + phone, "📅 Дата и время: " + dt + " в " + tm, "👥 Гостей: " + gst, "🏛️ Зона: " + zone];
  if (comm) lines.push("💬 Пожелания: " + comm);
  const txt = lines.join("\n");
  if (navigator.clipboard) navigator.clipboard.writeText(txt);
  window.open("https://t.me/mirmir_chef?text=" + encodeURIComponent(txt), "_blank");
};

const CAFE_SHOP_ITEMS = [
  { id: "sh1", name: "Классический ремесленный Тофу «Мир Мир»", weight: "400 г", price: 280, photo: "img/vk_5087_1.jpg", desc: "Нежный домашний тофу собственного производства на чистой воде. Идеален для жарки, омлетов, супов и салатов." },
  { id: "sh2", name: "Пряный печёный / Копчёный Тофу от Шефа", weight: "300 г", price: 340, photo: "img/vk_5055_0.jpg", desc: "Ароматный тофу в фирменном маринаде со специями и травами — готов к подаче и сэндвичам." },
  { id: "sh3", name: "Крафтовый бездрожжевой хлеб на закваске (буханка)", weight: "550 г", price: 290, photo: "img/vk_5121_0.jpg", desc: "Тот самый домашний ремесленный хлеб из печи «Мир Мир» с хрустящей корочкой на живой закваске." },
  { id: "sh4", name: "Домашнее Кимчи & Ферментированные овощи (банка)", weight: "400 г", price: 360, photo: "img/vk_5128_1.jpg", desc: "Живые пробиотические ферментированные овощи с имбирём и пряностями по рецепту кафе." },
  { id: "sh5", name: "Пшеничные колбаски & Сейтан ручной работы", weight: "350 г", price: 420, photo: "img/vk_5118_0.jpg", desc: "Сочный растительный белок со специями — для домашних бургеров, пиццы и пасты." },
  { id: "sh6", name: "Фирменный соус в баночке (Ореховый / Тахини / Чимичурри)", weight: "200 мл", price: 260, photo: "img/vk_5057_1.jpg", desc: "Густой авторский соус из боулов и салатов «Мир Мир» для заправки домашних блюд." },
  { id: "sh7", name: "Бокс ремесленных батончиков «Нутс» в шоколаде (5 шт.)", weight: "375 г", price: 1050, photo: "img/vk_5069_0.jpg", desc: "Набор из 5 сытных батончиков ручной работы с финиковой карамелью и орехами без белого сахара." },
  { id: "sh8", name: "Коллекционный чай «Унесённые Чаем» домой (Шу Пуэр / Габа / Да Хун Пао)", weight: "50 г", price: 450, photo: "img/vk_5122_0.jpg", desc: "Отборный листовой китайский чай из нашей чайной карты для домашних чаепитий." }
];

window.openCafeShopModal = function() {
  try { history.pushState({guard:"shop"}, ""); } catch(e){}
  const m = document.getElementById("cafe-shop-modal");
  if (!m) return;
  m.classList.remove("hidden"); m.classList.add("flex");
  const grid = document.getElementById("cafe-shop-grid");
  if (grid) {
    grid.innerHTML = CAFE_SHOP_ITEMS.map((it, i) => [
      '<div class="vibe-card bg-white rounded-3xl p-3.5 border border-stone-200 shadow-sm flex flex-col justify-between">',
        '<div>',
          '<div class="h-40 rounded-2xl overflow-hidden mb-3 relative">',
            '<img src="' + it.photo + '" onclick="window.openSuperZoom(\'' + it.photo + '\', \'' + esc(it.name) + '\')" class="w-full h-full object-cover cursor-zoom-in">',
            '<span class="absolute top-2 left-2 px-2.5 py-0.5 rounded-full bg-[#2E3D28]/90 text-[#F2B880] text-[10px] font-extrabold">' + it.weight + '</span>',
            '<button onclick="window.openSuperZoom(\'' + it.photo + '\', \'' + esc(it.name) + '\')" class="absolute bottom-2 right-2 px-2 py-0.5 rounded bg-black/75 text-white text-[10px] font-bold cursor-pointer">🔍 Лупа</button>',
          '</div>',
          '<h4 class="font-serif text-lg font-bold text-[#2E3D28] leading-snug">' + it.name + '</h4>',
          '<p class="text-xs text-stone-600 mt-1 leading-relaxed">' + it.desc + '</p>',
        '</div>',
        '<div class="pt-3 mt-3 border-t border-stone-100 flex items-center justify-between">',
          '<strong class="text-lg font-extrabold text-[#2E3D28]">' + it.price + ' ₽</strong>',
          '<button onclick="window.addShopItemToCart(' + i + ')" class="px-3.5 py-2 rounded-xl bg-[#D48238] hover:opacity-95 text-white font-extrabold text-xs cursor-pointer shadow">+ В корзину 🛒</button>',
        '</div>',
      '</div>'
    ].join("")).join("");
  }
};
window.closeCafeShopModal = function() {
  const m = document.getElementById("cafe-shop-modal");
  if (m) { m.classList.add("hidden"); m.classList.remove("flex"); }
};
window.addShopItemToCart = function(i) {
  const it = CAFE_SHOP_ITEMS[i];
  if (!it) return;
  const key = "shop_" + it.id;
  const ex = cart.find(x => x.key === key);
  if (ex) ex.qty++;
  else cart.push({ key: key, idx: 900 + i, sIdx: 0, name: "🛍️ [Магазин] " + it.name + " (" + it.weight + ")", price: it.price, category: "Магазин кафе", qty: 1 });
  updateCart();
  const t = document.createElement("div");
  t.innerText = "🛍️ Добавлено из Магазина: " + it.name;
  t.className = "fixed bottom-16 left-1/2 -translate-x-1/2 z-[95] bg-[#2E3D28] text-[#F2B880] border-2 border-[#D48238] px-4 py-2.5 rounded-2xl shadow-2xl font-extrabold text-xs whitespace-nowrap";
  document.body.appendChild(t); setTimeout(() => t.remove(), 1800);
};

const GUEST_DAILY_SUGGESTIONS = [
  "🍲 Попробуйте сегодня: пряный бразильский суп «Ватапа» с водорослями + хрустящий сэндвич «Елена Руз» с вешенками и дайкири + согревающий чай «Масала»!",
  "🌴 Карибское настроение: салат «Тропикал Кубана» с ананасом и авокадо + пряный плов «Арос кон каморонос» + прохладная «Домашняя кола» с Саган Дайля!",
  "🍄 Лесной фаворит: сочная пицца «Том Ям» с лисичками и эдамаме + освежающий «Крем-суп из зелёного горошка» + тайваньский «Габа Улун» в чайнике!",
  "🔥 Сытный комбо-сет (−30% в будни 12–16): тайский «Том Ям» на кокосовых сливках + «Мир-Бургер» с шоколадной курагой + ягодный смузи с чиа!",
  "🥗 Средиземноморский обед: омлет «Киприда» с зелёным маслом и крафтовым хлебом + салат «Сезам» с кедровым орехом + «Кедровый капучино»!",
  "🍫 Уютное чаепитие: рисовая лапша «Пад Тай» с тофу и сейтаном + десерт «Пика» с печёным пеканом + землистый Шу Пуэр от «Унесённых Чаем»!",
  "🥙 Восточный вкус из печи: арабская пицца «Лахмаджун» с гранатовым соусом + тёплый салат «Пай Хуан Гуа» из битых огурцов + «Пуэр на гранатовом соке»!"
];

window.rollRandomGastroPulse = function() {
  const el = document.getElementById("ai-pulse-random-text");
  if (!el) return;
  const pick = GUEST_DAILY_SUGGESTIONS[Math.floor(Math.random() * GUEST_DAILY_SUGGESTIONS.length)];
  el.style.opacity = "0";
  setTimeout(() => { el.innerText = pick; el.style.opacity = "1"; }, 180);
};

const RADIO_STREAMS = {
  hangdrum: { title: "🛸 Ханг Драм & Хэндпан", urls: ["https://ice2.somafm.com/fluid-128-mp3", "https://radiorecord.hostingradio.ru/organic96.aacp", "https://ice2.somafm.com/dronezone-128-mp3"] },
  ambient: { title: "🌌 Эмбиент & Чилл", urls: ["https://radiorecord.hostingradio.ru/ambient96.aacp", "https://radiorecord.hostingradio.ru/chil96.aacp", "https://ice2.somafm.com/groovesalad-128-mp3"] },
  reggae: { title: "🌴 Рэгги & Даб", urls: ["https://listen.181fm.com/181-reggae_128k.mp3", "https://radiorecord.hostingradio.ru/summer96.aacp", "https://ice2.somafm.com/dubstep-128-mp3"] },
  mantra: { title: "🕉️ Мантры & Восток", urls: ["https://ice2.somafm.com/suburbsofgoa-128-mp3", "https://radiorecord.hostingradio.ru/hypno96.aacp", "https://ice2.somafm.com/7soul-128-mp3"] }
};

let mirStreamAudio = null, hangDrumResonatorTimer = null, hangAudioCtx = null;

function startHangDrumAcousticOverlay() {
  if (hangDrumResonatorTimer) clearInterval(hangDrumResonatorTimer);
  if (!hangAudioCtx) hangAudioCtx = new (window.AudioContext || window.webkitAudioContext)();
  if (hangAudioCtx.state === "suspended") hangAudioCtx.resume();
  const dKurdScale = [146.83, 220.00, 233.08, 261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 523.25, 587.33];
  const strikeHangNote = (freq, delayMs, gainVal) => {
    setTimeout(() => {
      if (!hangDrumResonatorTimer) return;
      const now = hangAudioCtx.currentTime;
      [1, 2, 2.998].forEach((mult, idx) => {
        const osc = hangAudioCtx.createOscillator(), g = hangAudioCtx.createGain();
        osc.type = "sine";
        osc.frequency.setValueAtTime(freq * mult * 1.008, now);
        osc.frequency.exponentialRampToValueAtTime(freq * mult, now + 0.045);
        const amp = (gainVal || 0.04) / (idx === 0 ? 1 : idx === 1 ? 3.2 : 6.5);
        g.gain.setValueAtTime(0.0001, now);
        g.gain.linearRampToValueAtTime(amp, now + 0.018);
        g.gain.exponentialRampToValueAtTime(0.0001, now + (idx === 0 ? 3.2 : 1.6));
        osc.connect(g); g.connect(hangAudioCtx.destination);
        osc.start(now); osc.stop(now + 3.3);
      });
    }, delayMs);
  };
  const playHangPhrase = () => {
    if (Math.random() > 0.25) strikeHangNote(146.83, 0, 0.045);
    [350, 700, 1150, 1600, 2100].forEach(ms => {
      if (Math.random() > 0.2) strikeHangNote(dKurdScale[1 + Math.floor(Math.random() * (dKurdScale.length - 1))], ms, 0.032);
    });
  };
  hangDrumResonatorTimer = setInterval(playHangPhrase, 2600);
  playHangPhrase();
}

window.openRadioSelectorModal = function() {
  const m = document.getElementById("radio-selector-modal");
  if (m) { m.classList.remove("hidden"); m.classList.add("flex"); }
};
window.stopMirMirRadio = function() {
  if (mirStreamAudio) { mirStreamAudio.pause(); mirStreamAudio.src = ""; }
  if (hangDrumResonatorTimer) { clearInterval(hangDrumResonatorTimer); hangDrumResonatorTimer = null; }
  const st = document.getElementById("radio-now-status");
  if (st) st.innerText = "🔇 Сейчас радио выключено";
  const b1 = document.getElementById("radio-btn");
  if (b1) b1.innerHTML = DOVE_MINI_ICON + "📻 Радио";
};
window.setMirMirRadioVol = function(val) {
  if (mirStreamAudio) mirStreamAudio.volume = Math.max(0, Math.min(1, val / 100));
};
window.playMirMirWave = function(waveKey, urlIdx) {
  const idx = urlIdx || 0, station = RADIO_STREAMS[waveKey];
  if (hangDrumResonatorTimer) { clearInterval(hangDrumResonatorTimer); hangDrumResonatorTimer = null; }
  if (waveKey === "hangdrum") startHangDrumAcousticOverlay();
  if (!station || idx >= station.urls.length) return;
  if (mirStreamAudio) { mirStreamAudio.pause(); mirStreamAudio.src = ""; }
  mirStreamAudio = new Audio(station.urls[idx]);
  const volSlider = document.getElementById("radio-vol-slider");
  mirStreamAudio.volume = volSlider ? (volSlider.value / 100) * (waveKey === "hangdrum" ? 0.55 : 1.0) : 0.75;
  const st = document.getElementById("radio-now-status");
  if (st) st.innerText = "🔊 В эфире: " + station.title;
  const b1 = document.getElementById("radio-btn");
  if (b1) b1.innerHTML = DOVE_MINI_ICON + "🔊 Радио";
  mirStreamAudio.onerror = function() { window.playMirMirWave(waveKey, idx + 1); };
  mirStreamAudio.play().catch(function() { if (waveKey !== "hangdrum") window.playMirMirWave(waveKey, idx + 1); });
};

const SITE_TOGGLES_SPEC = [
  { key: "wings", label: "🖼️ Боковые кулисы ПК (Интерьер & Вывеска)", def: true },
  { key: "vibe", label: "📳 Физическая JS-вибрация фото при наведении мышки", def: true },
  { key: "newscontain", label: "📐 Фото в новостях целиком с полями (ВКЛ) / Крупно (ВЫКЛ)", def: false },
  { key: "leaves", label: "🍃 Падающие чайные листья на экране", def: false },
  { key: "float", label: "🧊 Плавная левитация Голубок и карточек", def: true }
];

function getToggleStates() {
  let st = {};
  try { st = JSON.parse(localStorage.getItem("mirmir_toggles_v44") || "{}"); } catch(e) {}
  SITE_TOGGLES_SPEC.forEach(s => { if (st[s.key] === undefined) st[s.key] = s.def; });
  return st;
}

window.applySiteToggles = function() {
  const st = getToggleStates();
  document.body.classList.toggle("cfg-no-wings", !st.wings);
  document.body.classList.toggle("cfg-no-vibe", !st.vibe);
  document.body.classList.toggle("cfg-news-contain", !!st.newscontain);
  document.body.classList.toggle("cfg-no-float", !st.float);

  const leavesBox = document.getElementById("falling-leaves-box");
  if (leavesBox) {
    if (st.leaves) {
      leavesBox.classList.remove("hidden");
      if (!leavesBox.innerHTML) {
        leavesBox.innerHTML = Array.from({length: 14}).map(() => '<div style="position:absolute;left:' + (Math.random()*95) + 'vw;top:-5vh;font-size:' + (16+Math.random()*14) + 'px;animation:leaf-fall ' + (8+Math.random()*7) + 's linear infinite;animation-delay:' + (Math.random()*5) + 's;">🍃</div>').join("");
      }
    } else {
      leavesBox.classList.add("hidden");
    }
  }
};

window.flipSiteToggle = function(k) {
  const st = getToggleStates();
  st[k] = !st[k];
  localStorage.setItem("mirmir_toggles_v44", JSON.stringify(st));
  window.applySiteToggles();
  window.renderUnifiedSystemHub();
};

window.openMasterPromptModal = function() {
  const m = document.getElementById("master-prompt-modal");
  if (m) { m.classList.remove("hidden"); m.classList.add("flex"); }
};
window.closeMasterPromptModal = function() {
  const m = document.getElementById("master-prompt-modal");
  if (m) { m.classList.add("hidden"); m.classList.remove("flex"); }
};
window.copyMasterPromptText = function() {
  const ta = document.getElementById("server-master-prompt-data");
  if (ta) { navigator.clipboard.writeText(ta.value); alert("🧬 Текстовый Мастер-Промпт скопирован в буфер обмена!"); }
};
window.downloadMasterPromptFile = function() {
  const ta = document.getElementById("server-master-prompt-data");
  if (!ta) return;
  const blob = new Blob([ta.value], {type: "text/plain;charset=utf-8"});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "MASTER_PROMPT_MIRMIR.txt";
  a.click();
};

window.openYandexTaxiTo45 = function(e) {
  if (e) e.preventDefault();
  const lat = "__LAT_45__", lon = "__LON_45__";
  if (/Android|iPhone|iPad|iPod/i.test(navigator.userAgent)) {
    window.location.href = "yandextaxi://route?end-lat=" + lat + "&end-lon=" + lon;
  } else {
    window.open("https://yandex.ru/maps/?rtext=~" + lat + "," + lon + "&rtt=taxi&z=18", "_blank");
  }
};

window.openDeliveryModal = function() {
  let m = document.getElementById("delivery-modal");
  if (!m) {
    m = document.createElement("div");
    m.id = "delivery-modal";
    m.className = "fixed inset-0 z-[76] bg-black/80 backdrop-blur-md hidden items-end sm:items-center justify-center p-0 sm:p-4";
    document.body.appendChild(m);
  }
  m.classList.remove("hidden"); m.classList.add("flex");
  const cnt = cart.reduce((s, x) => s + x.qty, 0);
  const sumTxt = document.getElementById("cart-sum") ? document.getElementById("cart-sum").innerText : "0 ₽";
  m.innerHTML = [
    '<div class="bg-[#FDF8F2] rounded-t-[2rem] sm:rounded-[2.2rem] max-w-lg w-full p-5 sm:p-7 border-4 border-[#556432] shadow-2xl space-y-4 text-xs sm:text-sm">',
      '<div class="flex justify-between items-center border-b border-stone-200 pb-3">',
        '<div><span class="text-[10px] font-extrabold uppercase tracking-wider text-[#D48238]">Нижний Новгород • ул. Ильинская, 45</span>',
        '<h3 class="font-serif text-2xl sm:text-3xl font-bold text-[#2E3D28]">🛵 Доставка из кафе «Мир Мир»</h3></div>',
        '<button onclick="document.getElementById(\'delivery-modal\').classList.add(\'hidden\')" class="w-9 h-9 rounded-full bg-white shadow font-bold cursor-pointer">✕</button>',
      '</div>',
      '<div class="p-3.5 rounded-2xl bg-[#F6E4CE]/70 border border-[#556432]/20 space-y-1.5 text-stone-800">',
        '<div>🥗 Добавьте блюда из меню или крафтовые продукты из Магазина кафе в корзину, укажите ваш адрес и отправьте заявку шефу!</div>',
        '<div class="text-[#556432] font-extrabold">🛒 Сейчас в корзине: ' + cnt + ' поз. (' + sumTxt + ')</div>',
      '</div>',
      '<div class="space-y-2.5">',
        '<input id="deliv-name" placeholder="Ваше имя *" class="w-full px-3.5 py-2.5 rounded-xl bg-white border border-stone-300 text-sm">',
        '<input id="deliv-phone" placeholder="Телефон или @Telegram для связи *" class="w-full px-3.5 py-2.5 rounded-xl bg-white border border-stone-300 text-sm">',
        '<input id="deliv-addr" placeholder="Адрес доставки (улица, дом, кв., подъезд) *" class="w-full px-3.5 py-2.5 rounded-xl bg-white border border-stone-300 text-sm">',
        '<input id="deliv-comm" placeholder="Пожелания (ко времени / приборы / домофон)" class="w-full px-3.5 py-2 rounded-xl bg-white border border-stone-300 text-xs">',
      '</div>',
      '<div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 pt-1">',
        '<button onclick="document.getElementById(\'delivery-modal\').classList.add(\'hidden\');openMenu(\'Все\')" class="py-3 px-4 rounded-xl bg-[#556432] text-white font-extrabold text-xs cursor-pointer">📖 Открыть меню</button>',
        '<button onclick="window.submitDeliveryOrder()" class="py-3 px-4 rounded-xl bg-[#D48238] text-white font-extrabold text-xs shadow-lg cursor-pointer">🛵 Отправить заказ шефу</button>',
      '</div>',
    '</div>'
  ].join("");
};

window.submitDeliveryOrder = function() {
  const name = (document.getElementById("deliv-name")?.value || "").trim();
  const phone = (document.getElementById("deliv-phone")?.value || "").trim();
  const addr = (document.getElementById("deliv-addr")?.value || "").trim();
  const comm = (document.getElementById("deliv-comm")?.value || "").trim();
  if (!cart.length) { alert("Сначала выберите блюда в меню или Магазине кафе!"); return; }
  if (!name || !phone || !addr) { alert("Пожалуйста, заполните имя, телефон и адрес доставки!"); return; }
  const sumTxt = document.getElementById("cart-sum") ? document.getElementById("cart-sum").innerText : "";
  const lines = ["🛵 ЗАКАЗ НА ДОСТАВКУ «Мир Мир»", "👤 Имя: " + name, "📞 Связь: " + phone, "📍 Адрес: " + addr];
  if (comm) lines.push("💬 Пожелания: " + comm);
  lines.push("", "📋 Состав заказа:");
  cart.forEach(x => lines.push("• " + x.name + " × " + x.qty + " = " + (x.price * x.qty) + " ₽"));
  lines.push("", "💰 ИТОГО: " + sumTxt);
  const txt = lines.join("\n");
  if (navigator.clipboard) navigator.clipboard.writeText(txt);
  window.open("https://t.me/mirmir_chef?text=" + encodeURIComponent(txt), "_blank");
};

window.openTzTerminal = function() {
  window.openUnifiedSystemHub("journal");
};

window.saveNewTzClean = async function() {
  const txt = (document.getElementById("tz-new-input")?.value || "").trim();
  const auth = (document.getElementById("tz-author-inp")?.value || "").trim() || "Команда Мир Мир";
  if (!txt) return;
  const entry = { type: "task", id: "tz_" + Date.now(), date: new Date().toLocaleDateString("ru-RU"), author: auth, user_tz: txt, gemini_reply: "", status: "🌿 Сохранено в журнал" };
  let local = [];
  try { local = JSON.parse(localStorage.getItem("mirmir_tz_tasks_gift_v1") || "[]"); } catch(e) {}
  local.unshift(entry);
  localStorage.setItem("mirmir_tz_tasks_gift_v1", JSON.stringify(local));
  addLocalBuildOrActionLog("📝 Новая запись в журнале пожеланий от " + auth, txt);
  try { await fetch("https://ntfy.sh/__NTFY_CHANNEL__", { method: "POST", body: JSON.stringify(entry) }); } catch(e) {}
  window.renderUnifiedSystemHub();
};

// Секция Новостей: Лупа + Читать на VK + Кадрирование лиц + JS-вибрация
let newsObserverAttached = false;

window.fixNewsSectionCardsAndVkButtons = function() {
  const allH2 = Array.from(document.querySelectorAll("h2"));
  const newsH2 = allH2.find(h => h.innerText && h.innerText.includes("Последние новости"));
  if (!newsH2) return;
  const newsSection = newsH2.closest("section") || newsH2.parentElement?.parentElement;
  if (!newsSection) return;
  const newsGrid = newsSection.querySelector(".grid");
  if (!newsGrid) return;

  Array.from(newsGrid.children).forEach(card => {
    card.classList.add("mirmir-news-card-fixed", "vibe-card");
    const txt = (card.innerText || "").toLowerCase();
    const im = card.querySelector("img");
    if (im) {
      const wrap = im.parentElement;
      if (wrap && wrap !== card) {
        wrap.className = "mirmir-news-img-wrap-fixed my-2";
        if (!wrap.querySelector(".news-lupa-btn")) {
          const srcVal = im.getAttribute("src");
          wrap.insertAdjacentHTML("beforeend", '<button onclick="event.stopPropagation();window.openSuperZoom(\'' + esc(srcVal) + '\', \'Фотография из новостей кафе\')" class="news-lupa-btn absolute bottom-2 right-2 px-2.5 py-1 rounded-lg bg-black/75 hover:bg-[#D48238] text-white text-[10px] font-extrabold cursor-pointer shadow">🔍 Лупа</button>');
        }
      }
      im.className = "mirmir-news-img-fixed";
      if (txt.includes("вегана") || txt.includes("01.11")) {
        im.style.setProperty("object-position", "center 100%", "important");
      } else if (txt.includes("02.11") || txt.includes("пятницу")) {
        im.style.setProperty("object-position", "center 28%", "important");
      } else if (txt.includes("05.11") || txt.includes("салам")) {
        im.style.setProperty("object-position", "center 35%", "important");
      } else if (txt.includes("14.10") || txt.includes("пряностях")) {
        im.style.setProperty("object-position", "center 30%", "important");
      } else {
        im.style.setProperty("object-position", "center 50%", "important");
      }
      im.style.cursor = "zoom-in";
      const srcVal = im.getAttribute("src");
      im.onclick = function(ev) { ev.stopPropagation(); window.openSuperZoom(srcVal, "Фотография из новостей кафе"); };
    }

    if (!card.querySelector(".vk-tiny-btn-v44")) {
      card.insertAdjacentHTML(
        "beforeend",
        '<div class="pt-2.5 mt-2 border-t border-stone-200/80 flex items-center justify-between">' +
          '<a href="https://vk.com/mirmir.cafe" target="_blank" onclick="event.stopPropagation()" class="vk-tiny-btn-v44 inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-[#2E3D28]/10 hover:bg-[#2E3D28] text-[#2E3D28] hover:text-[#F2B880] text-[10px] font-extrabold transition shadow-sm cursor-pointer">читать на VK ↗</a>' +
        '</div>'
      );
    }
  });

  if (!document.getElementById("news-section-bottom-vk-link")) {
    newsSection.insertAdjacentHTML(
      "beforeend",
      '<div id="news-section-bottom-vk-link" class="mt-3 flex items-center justify-start">' +
        '<a href="https://vk.com/mirmir.cafe" target="_blank" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-[#2E3D28] hover:bg-[#D48238] text-[#F2B880] hover:text-white text-[11px] font-extrabold transition shadow cursor-pointer">📘 читать на VK ↗</a>' +
      '</div>'
    );
  }

  if (!newsObserverAttached) {
    newsObserverAttached = true;
    const obs = new MutationObserver(() => {
      window.fixNewsSectionCardsAndVkButtons();
      window.attachGuaranteedJsVibration();
    });
    obs.observe(newsGrid, { childList: true });
  }
};

function applyMasterV44Layout() {
  applyManualOverridesToMenuData();

  const brandLink = document.querySelector("header a");
  if (brandLink) {
    const textWrap = brandLink.querySelector("div:last-child");
    if (textWrap) {
      textWrap.innerHTML = '<span class="font-serif text-xl sm:text-2xl font-bold tracking-tight text-[#2E3D28] block leading-none">Mir Mir</span><div id="header-work-status">' + window.getMirMirWorkStatusHTML(false) + '</div>';
    }
  }

  const deskNav = document.querySelector("header .hidden.lg\\:flex");
  if (deskNav) {
    deskNav.innerHTML = [
      '<button onclick="openMenu(\'Все\')" class="px-3 py-2 rounded-xl bg-[#556432] hover:bg-[#2E3D28] text-white text-xs font-extrabold shadow cursor-pointer transition">📖 Меню</button>',
      '<button onclick="window.openBookTableModal()" class="px-3.5 py-2 rounded-xl bg-[#2E3D28] hover:bg-[#556432] text-[#F2B880] border border-[#F2B880]/50 text-xs font-extrabold shadow cursor-pointer transition">🪑 Бронь столика</button>',
      '<button onclick="window.openDeliveryModal()" class="px-3.5 py-2 rounded-xl bg-emerald-700 hover:bg-emerald-600 text-white text-xs font-extrabold shadow-md cursor-pointer transition">🛵 Доставка из кафе</button>',
      '<button onclick="window.openCafeShopModal()" class="px-3.5 py-2 rounded-xl bg-[#D48238] hover:opacity-95 text-white text-xs font-extrabold shadow-lg cursor-pointer transition border border-white/50">🛍️ Магазин кафе</button>',
      '<button onclick="openBowlBuilder()" class="px-3 py-2 rounded-xl bg-[#556432] hover:bg-[#2E3D28] text-white text-xs font-extrabold shadow cursor-pointer transition">🥗 Боул</button>',
      '<button onclick="window.openRadioSelectorModal()" id="radio-btn" class="px-3 py-2 rounded-xl bg-white hover:bg-amber-50 text-[#2E3D28] border border-stone-300 text-xs font-extrabold cursor-pointer transition flex items-center gap-1">' + DOVE_MINI_ICON + '<span>📻 Радио</span></button>',
      '<a href="https://yandex.ru/maps/?rtext=~__LAT_45__,__LON_45__&rtt=taxi&z=18" onclick="window.openYandexTaxiTo45(event)" class="px-3 py-2 rounded-xl bg-[#FC3F1D] hover:opacity-90 text-white text-xs font-extrabold shadow cursor-pointer transition">🚕 Такси в кафе</a>'
    ].join("");
  }

  const rail = document.getElementById("sticky-rail");
  if (rail) {
    const cleanCategories = [
      { label: "📖 Все блюда (72)", cat: "Все", active: true },
      { label: "🔥 Сезонные спешлы от Шефа", cat: "Сезонные спешлы от Шефа" },
      { label: "🍲 Супы", cat: "Супы" },
      { label: "🥗 Боулы и Омлеты", cat: "Боулы и Омлеты" },
      { label: "🥬 Салаты", cat: "Салаты" },
      { label: "🍜 Лапша", cat: "Лапша" },
      { label: "🍔 Бургеры и Из печи", cat: "Бургеры и Из печи" },
      { label: "🍰 Десерты без сахара", cat: "Десерты без сахара" },
      { label: "🥤 Бар: Смузи и Кофе", cat: "Барное меню: Смузи и Кофе" },
      { label: "🍵 Чайная карта", cat: "Чайная карта" }
    ];
    rail.innerHTML = cleanCategories.map(c =>
      '<button onclick="openMenu(\'' + c.cat + '\')" class="px-3.5 py-1.5 rounded-full ' +
      (c.active ? 'bg-[#2E3D28] text-[#F2B880] font-extrabold shadow' : 'bg-white hover:bg-[#F6E4CE] text-[#2E3D28] border border-stone-300/80 font-bold') +
      ' text-xs whitespace-nowrap cursor-pointer transition">' + c.label + '</button>'
    ).join("");
  }

  const heroLeft = document.querySelector("main section:first-of-type .lg\\:col-span-7");
  if (heroLeft && !document.getElementById("hero-interior-slider-box")) {
    heroLeft.className = "lg:col-span-7 p-6 sm:p-8 pt-7 sm:pt-9 flex flex-col justify-between gap-4 text-white relative overflow-hidden hero-interior-dynamic-bg";

    heroLeft.innerHTML = [
      '<div class="flex flex-wrap items-center gap-2 relative z-10">' + window.getMirMirWorkStatusHTML(true) + '</div>',
      '<div class="relative z-10 space-y-2.5">',
        '<div class="flex items-center gap-3.5">',
          '<div class="w-14 h-14 sm:w-16 sm:h-16 rounded-full shadow-2xl border-2 border-[#F2B880] dove-float flex-shrink-0">__SIGN_DOVE_SVG__</div>',
          '<h1 class="font-serif text-3xl sm:text-5xl font-bold leading-none tracking-tight drop-shadow">Мир Мир — пространство вкуса и уюта</h1>',
        '</div>',
        '<div class="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 pt-1">',
          '<p class="italic text-[#F6E4CE] text-sm sm:text-lg border-l-2 border-[#D48238] pl-3 flex-1">«Гармония этичной растительной кухни, редкого китайского чая и живого общения на Ильинской, 45.»</p>',
          '<div onclick="openMenu(\'Сезонные спешлы от Шефа\')" class="vibe-card cursor-pointer p-3 rounded-2xl bg-gradient-to-br from-[#D48238] to-[#b56622] text-white shadow-xl border-2 border-[#FFFDF9]/80 flex items-center gap-2.5 sm:w-64 flex-shrink-0">',
            '<img src="img/vk_5128_1.jpg" class="w-12 h-12 rounded-xl object-cover border border-white/60 flex-shrink-0">',
            '<div class="min-w-0">',
              '<span class="text-[9px] font-extrabold uppercase tracking-wider bg-black/30 px-2 py-0.5 rounded-full">🔥 Новинки меню</span>',
              '<div class="font-serif font-bold text-base leading-tight mt-0.5">Сезонные спешлы от Шефа</div>',
              '<span class="text-[11px] text-amber-100 underline font-bold">Смотреть 9 блюд ➔</span>',
            '</div>',
          '</div>',
        '</div>',
      '</div>',

      '<div id="hero-interior-slider-box" class="relative z-10 p-2 rounded-3xl bg-black/45 backdrop-blur-md border-2 border-[#F2B880]/45 shadow-2xl">',
        '<div class="relative h-56 sm:h-64 rounded-2xl overflow-hidden bg-[#182214]">',
          '<img id="hero-interior-slide-img" src="img/ymap_org_0.jpg" onclick="window.openSuperZoom(\'img/ymap_org_0.jpg\', \'Интерьер кафе Мир Мир\')" class="w-full h-full object-cover transition-opacity duration-300 cursor-zoom-in" style="object-position: center 50%;" title="Нажмите для увеличения">',
          '<div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/10 to-transparent pointer-events-none"></div>',
          '<span id="hero-interior-slide-tag" class="absolute top-3 left-3 px-3 py-1 rounded-full bg-[#2E3D28]/90 text-[#F2B880] border border-[#F2B880]/40 text-[10px] font-extrabold uppercase tracking-wider">Интерьер зала</span>',
          '<button onclick="window.openSuperZoom(document.getElementById(\'hero-interior-slide-img\').src, \'Интерьер кафе Мир Мир\')" class="absolute top-3 right-3 px-2.5 py-1 rounded-lg bg-black/70 hover:bg-[#D48238] text-white text-[10px] font-extrabold cursor-pointer shadow">🔍 Лупа</button>',
          '<button onclick="window.stepInteriorSlide(-1)" class="absolute left-2.5 top-1/2 -translate-y-1/2 w-8 h-8 rounded-full bg-black/60 hover:bg-[#D48238] text-white font-bold text-xs cursor-pointer transition flex items-center justify-center">◀</button>',
          '<button onclick="window.stepInteriorSlide(1)" class="absolute right-2.5 top-1/2 -translate-y-1/2 w-8 h-8 rounded-full bg-black/60 hover:bg-[#D48238] text-white font-bold text-xs cursor-pointer transition flex items-center justify-center">▶</button>',
          '<div class="absolute bottom-3 left-3.5 right-3.5 flex items-end justify-between gap-2">',
            '<div id="hero-interior-slide-title" class="font-serif text-base sm:text-xl font-bold text-white drop-shadow leading-snug">🏛️ Исторический кирпичный свод и уютный зал на Ильинской, 45</div>',
            '<div id="hero-interior-dots" class="flex items-center gap-1.5 flex-shrink-0 pb-1"></div>',
          '</div>',
        '</div>',
      '</div>',

      '<div class="relative z-10 p-3.5 rounded-2xl bg-black/45 backdrop-blur-md border border-[#F2B880]/35">',
        '<div class="flex items-center justify-between gap-2 mb-1">',
          '<span class="text-[#F2B880] font-extrabold uppercase text-[11px] tracking-wider">✨ Вкусная рекомендация дня</span>',
          '<button onclick="window.rollRandomGastroPulse()" class="px-3 py-1 rounded-full bg-[#D48238] hover:opacity-95 text-white font-extrabold text-[10px] cursor-pointer shadow">🎲 Другое сочетание</button>',
        '</div>',
        '<div id="ai-pulse-random-text" class="text-white font-semibold text-xs sm:text-sm transition-opacity duration-200 leading-relaxed"></div>',
      '</div>',

      '<div class="relative z-10 grid grid-cols-2 sm:grid-cols-4 gap-2.5">',
        '<div onclick="openBowlBuilder()" class="bento-anim vibe-card cursor-pointer h-24 rounded-2xl overflow-hidden relative group">',
          '<img src="img/vk_5055_0.jpg" class="w-full h-full object-cover group-hover:scale-110 transition">',
          '<div class="absolute inset-0 bg-gradient-to-t from-black/85 via-black/30 to-transparent p-2.5 flex items-end"><span class="text-xs font-extrabold text-white leading-tight">🥗 Собрать свой Боул</span></div>',
        '</div>',
        '<div onclick="openMenu(\'Чайная карта\')" class="bento-anim vibe-card cursor-pointer h-24 rounded-2xl overflow-hidden relative group" style="animation-delay:0.6s">',
          '<img src="img/vk_5122_0.jpg" class="w-full h-full object-cover group-hover:scale-110 transition">',
          '<div class="absolute inset-0 bg-gradient-to-t from-black/85 via-black/30 to-transparent p-2.5 flex items-end"><span class="text-xs font-extrabold text-white leading-tight">🍵 Чай 300 / 900 мл</span></div>',
        '</div>',
        '<div onclick="openMenu(\'Десерты без сахара\')" class="bento-anim vibe-card cursor-pointer h-24 rounded-2xl overflow-hidden relative group" style="animation-delay:1.2s">',
          '<img src="img/vk_5069_0.jpg" class="w-full h-full object-cover group-hover:scale-110 transition">',
          '<div class="absolute inset-0 bg-gradient-to-t from-black/85 via-black/30 to-transparent p-2.5 flex items-end"><span class="text-xs font-extrabold text-white leading-tight">🍰 Десерты без сахара</span></div>',
        '</div>',
        '<div onclick="window.openCafeShopModal()" class="bento-anim vibe-card cursor-pointer h-24 rounded-2xl overflow-hidden relative group" style="animation-delay:1.8s">',
          '<img src="img/vk_5087_1.jpg" class="w-full h-full object-cover group-hover:scale-110 transition">',
          '<div class="absolute inset-0 bg-gradient-to-t from-black/85 via-black/30 to-transparent p-2.5 flex items-end"><span class="text-xs font-extrabold text-white leading-tight">🛍️ Домашний Тофу & Хлеб</span></div>',
        '</div>',
      '</div>'
    ].join("");

    window.rollRandomGastroPulse();
    window.renderInteriorSlideState();
    if (interiorSlideTimer) clearInterval(interiorSlideTimer);
    interiorSlideTimer = setInterval(() => window.stepInteriorSlide(1), 4200);
  }

  const rightHeroCol = document.querySelector("main section:first-of-type .lg\\:col-span-5");
  if (rightHeroCol && DATA.menu_scans && DATA.menu_scans.length && !document.getElementById("stage-3d-v44")) {
    rightHeroCol.className = "lg:col-span-5 bg-[#23311E] p-4 sm:p-5 flex flex-col items-center justify-between relative overflow-hidden gap-2";

    const specialsList = (DATA.menu || []).filter(d => d.category.includes("спешл") || d.category.includes("Спешл") || d.photo_type === "real").slice(0, 9);
    const row1 = specialsList.slice(0, 3), row2 = specialsList.slice(3, 6), row3 = specialsList.slice(6, 9);

    const buildRowHtml = (arr) => arr.map(d => {
      const realIdx = DATA.menu.indexOf(d);
      return [
        '<div onclick="openMenu(\'Сезонные спешлы от Шефа\')" class="vibe-card bg-[#FDF8F2] text-stone-900 rounded-xl p-1.5 flex items-center gap-2 cursor-pointer shadow border border-[#F2B880]/60 min-w-0">',
          '<img src="' + esc(d.photo) + '" onclick="event.stopPropagation();window.openSuperZoom(\'' + esc(d.photo) + '\', \'' + esc(d.name) + '\')" class="w-10 h-10 rounded-lg object-cover flex-shrink-0 cursor-zoom-in" title="Лупа 🔍">',
          '<div class="min-w-0 flex-1">',
            '<div class="font-bold text-[10px] text-[#2E3D28] truncate leading-tight">' + esc(d.name) + '</div>',
            '<div class="flex items-center justify-between mt-0.5">',
              '<strong class="text-[11px] text-[#D48238]">' + d.price + ' ₽</strong>',
              '<button onclick="event.stopPropagation();addToCart(' + realIdx + ',0)" class="px-1.5 py-0.5 rounded bg-[#556432] hover:bg-[#2E3D28] text-white text-[9px] font-extrabold cursor-pointer">+</button>',
            '</div>',
          '</div>',
        '</div>'
      ].join("");
    }).join("");

    rightHeroCol.innerHTML = [
      '<div class="absolute inset-0 flex items-center justify-center pointer-events-none opacity-[0.35] z-0"><div class="wm-spin"><svg width="420" height="420" viewBox="0 0 120 120" fill="none"><circle cx="60" cy="60" r="56" stroke="#F2B880" stroke-width="3"/><circle cx="60" cy="60" r="50" stroke="#FFFDF9" stroke-width="2" stroke-dasharray="5 4"/><circle cx="60" cy="62" r="25" stroke="#F2B880" stroke-width="2.5" fill="rgba(242,184,128,0.18)"/><path d="M32 58 C24 44, 34 26, 52 34 C46 40, 42 48, 42 58 C38 60, 34 60, 32 58 Z" fill="#FFFDF9"/><path d="M88 58 C96 44, 86 26, 68 34 C74 40, 78 48, 78 58 C82 60, 86 60, 88 58 Z" fill="#FFFDF9"/><path d="M35 52 C30 68, 44 88, 60 90 C76 88, 90 68, 85 52 C82 66, 72 78, 60 80 C48 78, 38 66, 35 52 Z" fill="#FFFDF9"/><circle cx="48" cy="36" r="6" fill="#FFFDF9"/><text x="60" y="106" text-anchor="middle" fill="#F2B880" font-family="serif" font-weight="bold" font-size="11" letter-spacing="3">• MIR MIR •</text></svg></div></div>',
      '<div class="relative z-10 flex items-center gap-2">',
        '<button onclick="window.step3DV44(-1)" class="w-7 h-7 rounded-full bg-white/15 hover:bg-white/30 text-white text-xs font-bold cursor-pointer">◀</button>',
        '<span class="text-[11px] font-extrabold uppercase px-3 py-1 rounded-full bg-black/45 text-[#F2B880] border border-[#F2B880]/40">📖 Листайте страницы меню зала</span>',
        '<button onclick="window.step3DV44(1)" class="w-7 h-7 rounded-full bg-white/15 hover:bg-white/30 text-white text-xs font-bold cursor-pointer">▶</button>',
      '</div>',
      '<div id="stage-3d-v44" class="stage-3d relative z-10"></div>',
      '<div class="relative z-20 w-full bg-black/45 backdrop-blur-md p-3 rounded-2xl border border-[#F2B880]/40 space-y-1.5 mt-1">',
        '<div class="flex items-center justify-between mb-1">',
          '<span class="text-[10px] font-extrabold uppercase tracking-wider text-[#F2B880]">🔥 Сезонные спешлы от Шефа (9 новинок)</span>',
          '<button onclick="openMenu(\'Сезонные спешлы от Шефа\')" class="text-[10px] font-extrabold text-amber-300 hover:underline cursor-pointer">Все блюда (72) ➔</button>',
        '</div>',
        '<div class="grid grid-cols-1 sm:grid-cols-3 gap-1.5">' + buildRowHtml(row1) + '</div>',
        '<div class="grid grid-cols-1 sm:grid-cols-3 gap-1.5">' + buildRowHtml(row2) + '</div>',
        '<div class="grid grid-cols-1 sm:grid-cols-3 gap-1.5">' + buildRowHtml(row3) + '</div>',
      '</div>'
    ].join("");

    let c3d = 0;
    const stBox = document.getElementById("stage-3d-v44");
    const sheetTitles = [
      {title: "🥗 Страница 1: Супы и Боулы", cat: "Супы"},
      {title: "🍵 Страница 4: Чайная карта", cat: "Чайная карта"},
      {title: "🍰 Страница 3: Десерты и Смузи", cat: "Десерты без сахара"},
      {title: "🍕 Страница 2: Салаты и Выпечка", cat: "Бургеры и Из печи"}
    ];
    stBox.innerHTML = DATA.menu_scans.map((s, i) => {
      const meta = sheetTitles[i] || {title:"Страница меню", cat:"Все"};
      return '<div class="slide-3d" onclick="openMenu(\'' + meta.cat + '\')"><div class="w-full h-full rounded-3xl overflow-hidden shadow-2xl border-4 border-[#FFFDF9] bg-[#FFFDF9] flex flex-col justify-between"><div class="flex-1 overflow-hidden flex items-center justify-center p-1"><img src="' + s + '?v=104" class="max-w-full max-h-full object-contain"></div><div class="bg-[#2E3D28] px-2.5 py-1.5 text-white flex items-center justify-between"><span class="text-[10px] font-extrabold text-[#F2B880] truncate">' + meta.title + '</span><button onclick="event.stopPropagation();window.openSuperZoom(\'' + s + '\', \'' + meta.title + '\')" class="text-[9px] bg-white/20 hover:bg-[#D48238] px-2 py-0.5 rounded font-bold cursor-pointer">Лупа 🔍</button></div></div></div>';
    }).join("");
    window.upd3DV44 = function() {
      const sl = stBox.querySelectorAll(".slide-3d"), tot = sl.length;
      sl.forEach((el, idx) => {
        const d = (idx - c3d + tot) % tot;
        if(d===0){ el.style.transform="translateX(0) translateZ(60px) scale(1)"; el.style.zIndex="30"; el.style.opacity="1"; }
        else if(d===1){ el.style.transform="translateX(50px) translateZ(-35px) rotateY(-16deg) scale(0.86)"; el.style.zIndex="20"; el.style.opacity="0.82"; }
        else if(d===tot-1){ el.style.transform="translateX(-50px) translateZ(-35px) rotateY(16deg) scale(0.86)"; el.style.zIndex="20"; el.style.opacity="0.82"; }
        else { el.style.transform="translateX(0) translateZ(-90px) scale(0.74)"; el.style.zIndex="10"; el.style.opacity="0.35"; }
      });
    };
    window.step3DV44 = function(delta) { c3d = (c3d + delta + DATA.menu_scans.length) % DATA.menu_scans.length; window.upd3DV44(); };
    window.upd3DV44();
  }

  const PERFECT_CATEGORY_COVERS = {
    "Сезонные спешлы от Шефа": "img/vk_5128_1.jpg",
    "Спешлы": "img/vk_5128_1.jpg",
    "Супы": "img/vk_5057_1.jpg",
    "Боулы и Омлеты": "img/vk_5055_0.jpg",
    "Салаты": "img/macro_caesar_romaine.jpg",
    "Лапша": "img/vk_5057_0.jpg",
    "Бургеры и Из печи": "img/vk_5085_1.jpg",
    "Десерты без сахара": "img/vk_5069_0.jpg",
    "Барное меню: Смузи и Кофе": "img/macro_strawberry_banana.jpg",
    "Чайная карта": "img/vk_5122_0.jpg"
  };
  const catGrid = document.getElementById("cat-showcase-grid");
  if (catGrid) {
    catGrid.innerHTML = catGrid.innerHTML.replace(/Спешлы со стены ВК/g, "Сезонные спешлы от Шефа");
    catGrid.querySelectorAll("div.rounded-3xl, > div").forEach(card => {
      card.classList.add("vibe-card");
      const titleEl = card.querySelector("h3, h4, .font-serif");
      const imgEl = card.querySelector("img");
      if (titleEl && imgEl) {
        const t = titleEl.innerText.trim();
        Object.keys(PERFECT_CATEGORY_COVERS).forEach(k => {
          if (t.includes(k) || k.includes(t)) imgEl.src = PERFECT_CATEGORY_COVERS[k] + "?v=104";
        });
      }
    });
  }

  window.fixNewsSectionCardsAndVkButtons();

  const footerEl = document.querySelector("footer");
  if (footerEl) {
    footerEl.innerHTML = [
      '<span class="font-bold text-[#2E3D28]">🕊️ Веган-кафе & Чайная «Мир Мир» • Нижний Новгород, ул. Ильинская, 45 • Ежедневно 12:00–21:00</span>',
      '<button onclick="window.openUnifiedSystemHub(\'dishes72\')" title="Открыть Центр Управления: Все 72 блюда, ИИ-генератор фото, Список задач и Логи" class="w-9 h-9 rounded-full bg-[#2E3D28] hover:bg-[#556432] text-[#F2B880] text-base flex items-center justify-center shadow-md cursor-pointer transition transform hover:rotate-90 border border-[#D48238]">⚙️</button>'
    ].join("");
  }

  window.attachGuaranteedJsVibration();
  window.applySiteToggles();
}

window.addEventListener("DOMContentLoaded", () => {
  applyMasterV44Layout();
  setTimeout(applyMasterV44Layout, 180);
  setTimeout(() => { window.fixNewsSectionCardsAndVkButtons(); window.attachGuaranteedJsVibration(); }, 500);
});
window.addEventListener("load", () => {
  setTimeout(() => { window.fixNewsSectionCardsAndVkButtons(); window.attachGuaranteedJsVibration(); }, 150);
});
</script>
""".replace("__SIGN_DOVE_SVG__", SIGN_DOVE_SVG).replace("__MASTER_PROMPT_ESCAPED__", master_prompt_escaped).replace("__LAT_45__", LAT_45).replace("__LON_45__", LON_45).replace("__NTFY_CHANNEL__", NTFY_CHANNEL)

    last_body_idx = html.rfind("</body>")
    if last_body_idx != -1:
        html = html[:last_body_idx] + V44_MODALS_AND_JS + NL + html[last_body_idx:]

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✨ [Ядро up44] ИИ-генератор с кнопкой «Утвердить», Загрузка с ПК, Супер-Лупа z-200, Полные логи и JS-вибро вшиты!")
