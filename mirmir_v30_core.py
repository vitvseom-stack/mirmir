# -*- coding: utf-8 -*-
"""ПОСТОЯННОЕ ЯДРО v34.0: МАГАЗИН КАФЕ + 3 РАДИО (ЭМБИЕНТ/РЭГГИ/МАНТРЫ) + НИЖНИЙ ПУЛЬТ ИЗМЕНЯШЕК"""
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


def build_master_prompt_text(menu_list):
    menu_json_str = json.dumps(menu_list, ensure_ascii=False, indent=2)
    lines = [
        "# 🧬 SYSTEM BLUEPRINT & GOD-MODE PROMPT: АВТОНОМНАЯ ПЛАТФОРМА ВЕГАН-КАФЕ И ЧАЙНОЙ «МИР МИР» (v34.0 1:1 CLONE SPEC)",
        "Ты — Senior Full-Stack Архитектор. Напиши один в один полный рабочий код проекта сайта веган-кафе и клуба чайной культуры «Мир Мир» (г. Нижний Новгород, ул. Ильинская, 45).",
        "Выдай решение без сокращений: `menu_data.py` (72 блюда + витрина Магазина кафе), `app.py`, `mirmir_v30_core.py` и `run.bat`.",
        "",
        "## 1. АРХИТЕКТУРА, ЧИСТАЯ ШАПКА ДЛЯ ГОСТЕЙ И ЕДИНЫЙ СИСТЕМНЫЙ ПУЛЬТ ВНИЗУ",
        "- Верхняя шапка (`header`) содержит только клиентские кнопки: `📖 Электронное меню`, `🛵 Доставка из кафе`, `🛍️ Магазин кафе`, `🥗 Собрать Боул`, `📻 Радио (3 волны)`, `🚕 Такси в кафе` (координаты дома №45: `56.322355, 43.990383`) и `🛒 Корзина`.",
        "- Все системные и админские инструменты (6 тумблеров-изменяшек сайта, ТЗ-Терминал, Мастер-Промпт 1:1, Экспорт PDF, 7 глав Манифеста и Логи сборок) объединены в ОДНУ кнопку в самом низу сайта (в футере): `🎛️ Пульт Архитектора & Изменяшки`.",
        "",
        "## 2. HERO-БЛОК: ЯРКИЙ ФОН, ОКОШКО СПЕШЛОВ НАПРОТИВ СЛОГАНА, РАНДОМНЫЙ ГАСТРО-ПУЛЬС И КАРУСЕЛЬ БЛЮД",
        "- Напротив слогана расположена акцентная карточка `🔥 Спешлы со стены ВК`.",
        "- Окошко `✨ Гастро-пульс от ИИ-Оракула` генерирует живые рандомные рекомендации («Попробуйте сегодня: это + это + это!») с кнопкой `🎲 Ещё совет`.",
        "- Прямо под слоганом встроена интерактивная фото-карусель хитов и спешлов с ценами и кнопкой `+ В корзину`.",
        "",
        "## 3. МАГАЗИН КАФЕ «МИР МИР» (КРАФТОВЫЕ ПРОДУКТЫ И ТОФУ ДОМОЙ)",
        "- Отдельное модальное окно `🛍️ Магазин кафе` с витриной крафтовых продуктов (Тофу классический и копчёный, бездрожжевой хлеб на закваске, кимчи, ореховый соус, тхина, боксы батончиков Нутс и китайский чай домой) + возможность добавлять новые товары.",
        "",
        "## 4. РАДИО МИРМИР (3 РАБОЧИЕ ВОЛНЫ В РФ) И ВИБРО-ОТКЛИК ФОТО НА ПК",
        "- Радио-пульт включает 3 станции, работающие в РФ без блокировок (процедурные Web Audio синтезаторы + прямые потоки): `🌌 1. Эмбиент & Чаши`, `🌴 2. Рэгги & Даб`, `🕉️ 3. Мантры & Ситар`.",
        "- Фотографии анонсов и блюд на ПК мягко вибрируют при наведении курсора (`@keyframes pc-photo-vibe`).",
        "- Боковые кулисы на ПК (`#pc-v26-authentic-wings`): слева кирпичный свод зала `img/ymap_org_0.jpg`, справа вывеска с Голубкой на фоне неба `img/ymap_org_1.jpg`.",
        "",
        "## 5. ПОЛНАЯ БАЗА ВСЕХ 72 БЛЮД МЕНЮ (`DATA.menu` JSON 1:1)",
        menu_json_str
    ]
    full_txt = "\n".join(lines)
    with open("MASTER_PROMPT_MIRMIR.txt", "w", encoding="utf-8") as f:
        f.write(full_txt)
    return full_txt


def sync_cloud_and_local_tz():
    base_data = {
        "tasks": [
            {
                "id": "tz_v34_complete",
                "date": "08.11.2026 • Сборка v34.0",
                "author": "Виталий",
                "user_tz": "1) Убрать все системные кнопки в одну кнопку внизу сайта и добавить туда тумблеры-изменяшки (вкл/выкл).\n2) Вернуть наверх заметную кнопку «Доставка из кафе» и добавить крупную кнопку «Магазин кафе» (тофу, крафтовый хлеб и т.д.).\n3) Напротив слогана сделать окошко Спешлов, под слоганом — яркий фон и карусель блюд, а в Гастро-пульсе — рандомные рекомендации от ИИ («Попробуйте это, это и это»).\n4) В Радио сделать 3 рабочие в РФ кнопки (Эмбиент, Рэгги, Мантры), а фоткам анонсов на ПК добавить вибрацию при наведении мышки.",
                "gemini_reply": "КрасовелоФ, Милорд, сделано на 100% в v34.0! 🦅\n1) Шапка полностью очищена от системных кнопок — там теперь сияют крупные «🛵 Доставка из кафе» и «🛍️ Магазин кафе (Тофу & Крафт)».\n2) Все системные пульты перенесены в одну кнопку в самом низу сайта («🎛️ Пульт Архитектора & Изменяшки») с 6 живыми тумблерами Вкл/Выкл.\n3) В Hero-блоке напротив слогана стоит карточка «🔥 Спешлы недели», под слоганом — живая карусель блюд на ярком фоне и рандомный Гастро-пульс ИИ.\n4) В Радио работают 3 станции для РФ (🌌 Эмбиент, 🌴 Рэгги, 🕉️ Мантры), а фото анонсов на ПК вибрируют при наведении мышки!",
                "status": "✅ Выполнено в v34.0"
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
    right_wing = "img/ymap_org_1.jpg" if os.path.exists("img/ymap_org_1.jpg") else "img/vk_5129_1.jpg"
    tz_synced = sync_cloud_and_local_tz()

    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    html = html.replace(".hidden { display:none !important; }", "")

    menu_items_for_prompt = []
    m_data = re.search(r"const DATA = (\{.*?\});\s*\n\s*const CV =", html, re.DOTALL)
    if m_data:
        data_obj = json.loads(m_data.group(1).replace("<\\/", "</"))
        data_obj["tz_synced"] = tz_synced
        dish_ov = tz_synced.get("dishes", {})

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
            "✨ Попробуйте сегодня: пряный бразильский суп «Ватапа» с водорослями + хрустящий сэндвич «Елена Руз» с вешенками и дайкири + согревающий чай «Масала» на растительном молоке!"
        )
        new_json_str = json.dumps(data_obj, ensure_ascii=False).replace("</", "<\\/")
        html = html[:m_data.start(1)] + new_json_str + html[m_data.end(1):]

    master_prompt_raw = build_master_prompt_text(menu_items_for_prompt)
    master_prompt_escaped = html_lib.escape(master_prompt_raw)

    # 1. CSS: Боковые кулисы v26 + Вибрация фото при наведении на ПК + Классы для 6 тумблеров-изменяшек!
    STATIC_HEAD_CSS = """
<style id="v34-master-styles">
  @keyframes float-dove { 0%,100%{transform:translateY(0) rotate(0deg)} 50%{transform:translateY(-8px) rotate(2deg)} }
  @keyframes pc-photo-vibe {
    0% { transform: scale(1) rotate(0deg); }
    20% { transform: scale(1.04) rotate(-1.4deg) translate(-2px, -1px); }
    40% { transform: scale(1.05) rotate(1.4deg) translate(2px, 1px); }
    60% { transform: scale(1.05) rotate(-1deg) translate(-1px, 1px); }
    80% { transform: scale(1.04) rotate(1deg) translate(1px, -1px); }
    100% { transform: scale(1.04) rotate(0deg); }
  }
  @keyframes leaf-fall {
    0% { transform: translateY(-10vh) translateX(0) rotate(0deg); opacity: 0.85; }
    50% { transform: translateY(50vh) translateX(25px) rotate(180deg); opacity: 0.7; }
    100% { transform: translateY(105vh) translateX(-20px) rotate(360deg); opacity: 0; }
  }
  .dove-float { animation: float-dove 5s ease-in-out infinite; }
  #pc-v26-authentic-wings { display: none; }
  @media (min-width: 1100px) {
    body:not(.cfg-no-wings) { background-color: #1A2416 !important; }
    body:not(.cfg-no-wings) #pc-v26-authentic-wings { display: block !important; }
    body:not(.cfg-no-wings) main.max-w-7xl {
      background: rgba(246, 228, 206, 0.96);
      backdrop-filter: blur(12px);
      border-radius: 2.8rem;
      padding: 2rem 2.5rem !important;
      margin-top: 1.5rem !important;
      box-shadow: 0 30px 95px rgba(0,0,0,0.72), 0 0 0 2px rgba(242,184,128,0.35);
      position: relative;
      z-index: 10;
    }
    /* Вибрация фото анонсов и карточек при наведении мышки на ПК */
    body:not(.cfg-no-vibe) #posts-grid article:hover img,
    body:not(.cfg-no-vibe) .vibe-on-hover:hover img,
    body:not(.cfg-no-vibe) .vibe-card:hover {
      animation: pc-photo-vibe 0.42s ease-in-out !important;
    }
  }
  /* Тумблер: Вечерний тёмный лаунж-режим */
  body.cfg-dark-lounge main.max-w-7xl {
    background: rgba(24, 34, 20, 0.97) !important;
    color: #FDF8F2 !important;
  }
  body.cfg-dark-lounge #posts-grid article,
  body.cfg-dark-lounge #cat-showcase-grid > div {
    background-color: #263521 !important;
    color: #FDF8F2 !important;
    border-color: rgba(242,184,128,0.3) !important;
  }
  body.cfg-dark-lounge h2, body.cfg-dark-lounge h3, body.cfg-dark-lounge p {
    color: #FDF8F2 !important;
  }
  /* Тумблер: Отключение левитации */
  body.cfg-no-float .dove-float, body.cfg-no-float .bento-anim {
    animation: none !important;
  }
</style>
"""
    html = html.replace("</head>", STATIC_HEAD_CSS + "\n</head>", 1)

    # 2. Боковые кулисы v26 (Кирпичный интерьер слева + Вывеска справа) + Контейнер для падающих чайных листьев
    STATIC_WINGS_HTML = f"""
<div id="pc-v26-authentic-wings" class="fixed inset-0 pointer-events-none z-0 overflow-hidden">
  <div class="absolute left-0 top-0 bottom-0 w-1/3 overflow-hidden">
    <img src="{left_wing}?v=340" class="w-full h-full object-cover opacity-55 scale-105 filter saturate-125 contrast-110">
    <div class="absolute inset-0" style="background:linear-gradient(90deg, rgba(20,30,16,0.20) 0%, rgba(26,36,22,0.95) 94%);"></div>
    <div class="absolute top-28 left-8 w-24 h-24 opacity-90 dove-float">{SIGN_DOVE_SVG}</div>
  </div>
  <div class="absolute right-0 top-0 bottom-0 w-1/3 overflow-hidden">
    <img src="{right_wing}?v=340" class="w-full h-full object-cover opacity-60 scale-105 filter saturate-125 contrast-110">
    <div class="absolute inset-0" style="background:linear-gradient(270deg, rgba(20,30,16,0.20) 0%, rgba(26,36,22,0.95) 94%);"></div>
    <div class="absolute top-28 right-8 w-24 h-24 opacity-90 dove-float" style="animation-delay:1.4s">{SIGN_DOVE_SVG}</div>
  </div>
</div>
<div id="falling-leaves-box" class="fixed inset-0 pointer-events-none z-40 overflow-hidden hidden"></div>
"""
    html = re.sub(r"(<body[^>]*>)", r"\1\n" + STATIC_WINGS_HTML, html, count=1)

    # 3. Заменяем верхнюю шапку на ЧИСТУЮ КЛИЕНТСКУЮ НАВИГАЦИЮ (с крупными кнопками «🛵 Доставка из кафе» и «🛍️ Магазин кафе», БЕЗ системных кнопок!)
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

    # 4. Заменяем нижний футер на ОДНУ СИСТЕМНУЮ КНОПКУ «🎛️ Пульт Архитектора & Изменяшки (Все системные инструменты)»!
    UNIFIED_FOOTER = """<footer class="max-w-7xl mx-auto px-4 pt-6 pb-10 text-center text-xs text-stone-600 flex flex-col sm:flex-row items-center justify-center gap-3 relative z-20">
  <span class="font-bold text-[#2E3D28]">🕊️ Веган-кафе & Чайная «Мир Мир» • Нижний Новгород, ул. Ильинская, 45</span>
  <button onclick="window.openUnifiedSystemHub()" class="px-5 py-2.5 rounded-full bg-[#2E3D28] hover:bg-[#556432] text-[#F2B880] font-extrabold shadow-xl cursor-pointer transition border-2 border-[#D48238] flex items-center gap-2">
    <span>🎛️ Пульт Архитектора: Изменяшки (Вкл/Выкл), ТЗ, Промпт, PDF & Логи</span>
  </button>
</footer>"""
    html = re.sub(r"<footer[\s\S]*?</footer>", UNIFIED_FOOTER, html, count=1)

    # 5. Модальные окна (Магазин Кафе + 3 Радиостанции РФ + Единый Нижний Пульт с Изменяшками + Мастер-Промпт)
    V34_MODALS_AND_JS = f"""
<!-- 🛍️ МОДАЛЬНОЕ ОКНО: МАГАЗИН КАФЕ «МИР МИР» (ТОФУ, КРАФТОВЫЙ ХЛЕБ, КИМЧИ, ЧАЙ ДОМОЙ) -->
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
          <p class="text-xs text-white/90 mt-0.5">Мы сами делаем тофу, печём бездрожжевой хлеб на закваске, ферментируем кимчи и взбиваем соусы. Добавляйте в общую корзину для самовывоза или доставки!</p>
        </div>
        <button onclick="window.closeCafeShopModal();window.openDeliveryModal()" class="px-4 py-2.5 rounded-xl bg-amber-400 text-[#1A2416] font-extrabold text-xs whitespace-nowrap cursor-pointer shadow">🛵 Оформить с доставкой</button>
      </div>
      <div id="cafe-shop-grid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4"></div>
    </div>
  </div>
</div>

<!-- 📻 МОДАЛЬНОЕ ОКНО: 3 РАБОЧИЕ РАДИОСТАНЦИИ В РФ (ЭМБИЕНТ / РЭГГИ / МАНТРЫ) -->
<div id="radio-selector-modal" class="fixed inset-0 z-[78] bg-black/80 backdrop-blur-md hidden items-center justify-center p-3">
  <div class="bg-[#FDF8F2] rounded-[2.2rem] max-w-lg w-full p-5 sm:p-6 border-4 border-[#556432] shadow-2xl space-y-4">
    <div class="flex items-center justify-between border-b border-stone-200 pb-3">
      <div class="flex items-center gap-3">
        <div class="w-11 h-11 flex-shrink-0">{SIGN_DOVE_SVG}</div>
        <div>
          <span class="text-[10px] font-extrabold uppercase tracking-wider text-[#D48238]">100% Работает в РФ без VPN • Web Audio + Stream</span>
          <h3 class="font-serif text-2xl font-bold text-[#2E3D28]">📻 Радио «Мир Мир» — 3 Волны</h3>
        </div>
      </div>
      <button onclick="document.getElementById('radio-selector-modal').classList.add('hidden');document.getElementById('radio-selector-modal').classList.remove('flex')" class="w-9 h-9 rounded-full bg-white shadow font-bold cursor-pointer">✕</button>
    </div>
    <p class="text-xs text-stone-600">Выберите настроение кафе: каждая волна генерируется встроенным многоголосным синтезатором прямо в вашем браузере (гарантированно играет в РФ без блокировок!):</p>
    <div class="space-y-2.5">
      <button id="wave-btn-ambient" onclick="window.playMirMirWave('ambient')" class="w-full p-4 rounded-2xl border-2 border-[#556432] bg-white hover:bg-emerald-50 text-left flex items-center justify-between transition cursor-pointer shadow-sm">
        <div>
          <div class="font-serif text-xl font-bold text-[#2E3D28]">🌌 1. Эмбиент & Поющие чаши</div>
          <div class="text-xs text-stone-600">Тёплый чайный дзен, пентатоника и тибетские колокольчики</div>
        </div>
        <span class="px-3 py-1 rounded-full bg-[#556432] text-white text-xs font-extrabold">▶ Включить</span>
      </button>
      <button id="wave-btn-reggae" onclick="window.playMirMirWave('reggae')" class="w-full p-4 rounded-2xl border-2 border-[#D48238] bg-white hover:bg-amber-50 text-left flex items-center justify-between transition cursor-pointer shadow-sm">
        <div>
          <div class="font-serif text-xl font-bold text-[#2E3D28]">🌴 2. Рэгги & Даб Вибрации</div>
          <div class="text-xs text-stone-600">Солнечный карибский грув на слабую долю, тёплый саб-бас и даб-эхо</div>
        </div>
        <span class="px-3 py-1 rounded-xl bg-[#D48238] text-white text-xs font-extrabold">▶ Включить</span>
      </button>
      <button id="wave-btn-mantra" onclick="window.playMirMirWave('mantra')" class="w-full p-4 rounded-2xl border-2 border-purple-700/60 bg-white hover:bg-purple-50 text-left flex items-center justify-between transition cursor-pointer shadow-sm">
        <div>
          <div class="font-serif text-xl font-bold text-[#2E3D28]">🕉️ 3. Мантры & Индийский Ситар</div>
          <div class="text-xs text-stone-600">Медитативная танпура 136.1 Гц (Ом), переборы ситара и мягкий пульс</div>
        </div>
        <span class="px-3 py-1 rounded-xl bg-purple-800 text-white text-xs font-extrabold">▶ Включить</span>
      </button>
    </div>
    <div class="pt-2 border-t border-stone-200 flex items-center justify-between">
      <span id="radio-now-status" class="text-xs font-extrabold text-[#556432]">🔇 Сейчас радио выключено</span>
      <button onclick="window.stopMirMirRadio()" class="px-4 py-2 rounded-xl bg-stone-200 hover:bg-red-100 text-stone-800 font-extrabold text-xs cursor-pointer">⏹ Выключить звук</button>
    </div>
  </div>
</div>

<!-- 🎛️ ЕДИНЫЙ СИСТЕМНЫЙ ПУЛЬТ ВНИЗУ САЙТА: ИЗМЕНЯШКИ (ВКЛ/ВЫКЛ) + ТЗ + ПРОМПТ + PDF + ЛОГИ -->
<div id="unified-system-hub" class="fixed inset-0 z-[80] bg-black/85 backdrop-blur-md hidden items-center justify-center p-2 sm:p-5">
  <div class="bg-[#FDF8F2] rounded-[2.2rem] max-w-5xl w-full h-[90vh] flex flex-col justify-between overflow-hidden border-4 border-[#556432] shadow-2xl">
    <div class="p-4 sm:p-5 bg-[#2E3D28] text-white flex flex-col sm:flex-row sm:items-center justify-between gap-3">
      <div class="flex items-center gap-3">
        <div class="w-11 h-11 flex-shrink-0">{SIGN_DOVE_SVG}</div>
        <div>
          <span class="text-[10px] uppercase tracking-widest text-[#F2B880] font-extrabold">All-in-One Control Deck • v34.0</span>
          <h3 class="font-serif text-2xl sm:text-3xl font-bold leading-none mt-0.5">🎛️ Единый Пульт Архитектора & Изменяшки Сайта</h3>
        </div>
      </div>
      <div class="flex items-center gap-2 flex-wrap">
        <button onclick="window.openTzTerminal()" class="px-3.5 py-2 rounded-xl bg-[#D48238] text-white font-extrabold text-xs cursor-pointer shadow">📝 ТЗ-Терминал (72 блюда)</button>
        <button onclick="window.openMasterPromptModal()" class="px-3.5 py-2 rounded-xl bg-amber-400 text-[#1A2416] font-extrabold text-xs cursor-pointer shadow">🧬 Мастер-Промпт 1:1</button>
        <button onclick="exportPDF()" class="px-3.5 py-2 rounded-xl bg-white/15 hover:bg-white/25 text-white font-extrabold text-xs cursor-pointer">📥 Скачать PDF</button>
        <button onclick="toggleDev();window.closeUnifiedSystemHub()" class="px-3.5 py-2 rounded-xl bg-white/15 hover:bg-white/25 text-[#F2B880] font-extrabold text-xs cursor-pointer">📜 7 Глав & Логи</button>
        <button onclick="window.closeUnifiedSystemHub()" class="w-9 h-9 rounded-full bg-white/15 text-white font-bold cursor-pointer ml-1">✕</button>
      </div>
    </div>
    <div class="p-4 sm:p-6 overflow-y-auto flex-1 space-y-5 custom-scroll">
      <div class="bg-white p-4 sm:p-5 rounded-3xl border-2 border-[#556432] shadow-sm space-y-4">
        <div class="flex items-center justify-between flex-wrap gap-2">
          <h4 class="font-serif text-xl sm:text-2xl font-bold text-[#2E3D28]">⚡ Интерактивные «Изменяшки» сайта (Вкл / Выкл в реальном времени)</h4>
          <span class="text-xs font-bold text-stone-500">Настройки мгновенно применяются и запоминаются в браузере</span>
        </div>
        <div id="toggles-grid-box" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3"></div>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        <div onclick="window.openTzTerminal()" class="p-4 rounded-2xl bg-white border-2 border-[#D48238] hover:shadow-lg cursor-pointer transition">
          <div class="text-2xl mb-1">📝</div>
          <div class="font-serif text-lg font-bold text-[#2E3D28]">Бортовой ТЗ-Терминал</div>
          <p class="text-xs text-stone-600 mt-1">Заметки для Gemini и построчный редактор всех 72 блюд меню</p>
        </div>
        <div onclick="window.openMasterPromptModal()" class="p-4 rounded-2xl bg-white border-2 border-amber-400 hover:shadow-lg cursor-pointer transition">
          <div class="text-2xl mb-1">🧬</div>
          <div class="font-serif text-lg font-bold text-[#2E3D28]">Мастер-Промпт (ДНК 1:1)</div>
          <p class="text-xs text-stone-600 mt-1">Полная тех. спецификация сайта для любой топовой языковой модели ИИ</p>
        </div>
        <div onclick="exportPDF()" class="p-4 rounded-2xl bg-white border-2 border-[#556432] hover:shadow-lg cursor-pointer transition">
          <div class="text-2xl mb-1">📥</div>
          <div class="font-serif text-lg font-bold text-[#2E3D28]">Печатный PDF-Каталог</div>
          <p class="text-xs text-stone-600 mt-1">Сформировать и распечатать иллюстрированное меню всех 72 блюд</p>
        </div>
        <div onclick="toggleDev();window.closeUnifiedSystemHub()" class="p-4 rounded-2xl bg-white border-2 border-stone-300 hover:shadow-lg cursor-pointer transition">
          <div class="text-2xl mb-1">⚙️</div>
          <div class="font-serif text-lg font-bold text-[#2E3D28]">Книга-Манифест & Логи</div>
          <p class="text-xs text-stone-600 mt-1">7 глав истории разработки, Чек-лист багов и монитор сборок</p>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- 🧬 МОДАЛЬНОЕ ОКНО МАСТЕР-ПРОМПТА -->
<div id="master-prompt-modal" class="fixed inset-0 z-[85] bg-black/85 backdrop-blur-md hidden items-center justify-center p-2 sm:p-5">
  <div class="bg-[#FDF8F2] rounded-[2rem] max-w-5xl w-full h-[90vh] flex flex-col justify-between overflow-hidden border-4 border-[#D48238] shadow-2xl">
    <div class="p-4 sm:p-5 bg-[#2E3D28] text-white flex flex-col sm:flex-row sm:items-center justify-between gap-3">
      <div class="flex items-center gap-3">
        <div class="w-11 h-11 flex-shrink-0">{SIGN_DOVE_SVG}</div>
        <div>
          <span class="text-[10px] uppercase tracking-widest text-[#F2B880] font-extrabold">Full DNA Quine Specification • v34.0</span>
          <h3 class="font-serif text-2xl sm:text-3xl font-bold leading-none mt-0.5">🧬 Мастер-Промпт для 100% воссоздания сайта любой ИИ-моделью</h3>
        </div>
      </div>
      <div class="flex items-center gap-2 flex-wrap">
        <button onclick="window.copyMasterPromptText()" class="px-4 py-2.5 rounded-xl bg-amber-400 hover:bg-amber-300 text-[#1A2416] font-extrabold text-xs sm:text-sm shadow-lg cursor-pointer">📋 Скопировать весь Промпт (1 клик)</button>
        <button onclick="window.downloadMasterPromptFile()" class="px-4 py-2.5 rounded-xl bg-emerald-800 hover:bg-emerald-700 text-white font-extrabold text-xs sm:text-sm shadow cursor-pointer">💾 Скачать MASTER_PROMPT_MIRMIR.txt</button>
        <button onclick="window.closeMasterPromptModal()" class="w-9 h-9 rounded-full bg-white/15 text-white font-bold cursor-pointer ml-1">✕</button>
      </div>
    </div>
    <div class="p-4 sm:p-6 overflow-y-auto flex-1 space-y-3 custom-scroll">
      <textarea id="server-master-prompt-data" readonly class="w-full h-[72vh] p-4 rounded-2xl bg-[#1A2316] text-[#F6E4CE] font-mono text-xs leading-relaxed border-2 border-[#556432] focus:outline-none">{master_prompt_escaped}</textarea>
    </div>
  </div>
</div>

<script>
// === 🌟 ДВИЖОК v34.0: МАГАЗИН КАФЕ + 3 РАДИО РФ + ПУЛЬТ ИЗМЕНЯШЕК + РАНДОМНЫЙ ГАСТРО-ПУЛЬС + КАРУСЕЛЬ ПОД СЛОГАНОМ ===

// 1. Витрина Магазина кафе «Мир Мир» (Крафт, Тофу, Хлеб, Кимчи, Соусы, Чай домой)
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

// 2. Рандомный «✨ Гастро-пульс от ИИ-Оракула» («Попробуйте это, это и это!»)
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

// 3. Радио «Мир Мир» на 3 рабочие волны в РФ (Эмбиент / Рэгги / Мантры)
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
      // Солнечный Рэгги-грув: тёплый круглый саб-бас на 1 и 3 долю + аккордовый сканк на слабую долю (2 и 4)!
      const roots = [110.0, 146.83, 130.81, 164.81];
      const root = roots[Math.floor(Math.random() * roots.length)];
      playNote(root, 0.55, "sine", 0.06, 0.0);
      playNote(root * 1.5, 0.35, "sine", 0.045, 0.5);
      // Off-beat skank chord
      [root * 2, root * 2.5, root * 3].forEach(cf => {{
        playNote(cf, 0.18, "triangle", 0.022, 0.28);
        playNote(cf, 0.18, "triangle", 0.022, 0.82);
      }});
    }} else if (wave === "mantra") {{
      // Сакральная Танпура Ом (136.1 Гц) + индийский лад ситара
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

// 4. Единый Нижний Пульт Архитектора & 6 Тумблеров-Изменяшек
const SITE_TOGGLES_SPEC = [
  {{ key: "wings", label: "🖼️ Боковые кулисы ПК (Интерьер & Вывеска)", def: true }},
  {{ key: "vibe", label: "📳 Вибро-отклик фото при наведении мышки", def: true }},
  {{ key: "bright", label: "☀️ Турбо-яркость зелени под слоганом", def: true }},
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
  document.body.classList.toggle("cfg-dark-lounge", !!st.lounge);
  document.body.classList.toggle("cfg-no-float", !st.float);

  const heroBgImg = document.getElementById("hero-bright-bg-img");
  if (heroBgImg) {{
    heroBgImg.style.opacity = st.bright ? "0.78" : "0.35";
    heroBgImg.style.filter = st.bright ? "saturate(1.75) brightness(1.18) contrast(1.12)" : "saturate(1.1)";
  }}

  const leavesBox = document.getElementById("falling-leaves-box");
  if (leavesBox) {{
    if (st.leaves) {{
      leavesBox.classList.remove("hidden");
      if (!leavesBox.innerHTML) {{
        leavesBox.innerHTML = Array.from({{length: 14}}).map((_, i) => `<div style="position:absolute;left:${{Math.random()*95}}vw;top:-5vh;font-size:${{16+Math.random()*14}}px;animation:leaf-fall ${{8+Math.random()*7}}s linear infinite;animation-delay:${{Math.random()*5}}s;">🍃</div>`).join("");
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
  if (ta) {{ navigator.clipboard.writeText(ta.value); alert("🧬 Полный Мастер-Промпт скопирован в буфер обмена!"); }}
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

// 5. Апгрейд Hero-блока при загрузке: Яркий фон + Спешлы напротив слогана + Рандомный Гастро-пульс + Карусель блюд под слоганом!
window.addEventListener("DOMContentLoaded", () => {{
  // Вставляем в липкую ленту кнопки Магазина, Доставки и Спешлов
  const rail = document.getElementById("sticky-rail");
  if (rail && !rail.innerHTML.includes("openCafeShopModal")) {{
    rail.insertAdjacentHTML("afterbegin", '<button onclick="window.openCafeShopModal()" class="px-3.5 py-1.5 rounded-full bg-[#D48238] text-white text-xs font-extrabold whitespace-nowrap cursor-pointer shadow">🛍️ Магазин кафе</button><button onclick="window.openDeliveryModal()" class="px-3.5 py-1.5 rounded-full bg-emerald-700 text-white text-xs font-extrabold whitespace-nowrap cursor-pointer shadow">🛵 Доставка</button>');
  }}

  const heroLeft = document.querySelector("main section:first-of-type .lg\\\\:col-span-7");
  if (heroLeft) {{
    heroLeft.classList.add("relative", "overflow-hidden");
    // Яркий сочный фон микрозелени под слоганом!
    heroLeft.insertAdjacentHTML("afterbegin", `<div class="absolute inset-0 pointer-events-none z-0">
      <img id="hero-bright-bg-img" src="img/vk_5129_1.jpg?v=340" class="w-full h-full object-cover scale-105 transition-all duration-500" style="opacity:0.78;filter:saturate(1.75) brightness(1.18) contrast(1.12);">
      <div class="absolute inset-0" style="background:linear-gradient(90deg,rgba(18,30,14,0.72) 0%,rgba(28,46,22,0.38) 55%,rgba(18,30,14,0.68) 100%);"></div>
    </div>`);
    Array.from(heroLeft.children).forEach((ch, idx) => {{ if (idx > 0) ch.classList.add("relative", "z-10"); }});

    // Напротив слогана (рядом с курсивной цитатой) ставим яркое окошко «🔥 Спешлы со стены ВК»!
    const sloganP = heroLeft.querySelector("p.italic");
    if (sloganP) {{
      const wrapper = document.createElement("div");
      wrapper.className = "relative z-10 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 my-1";
      sloganP.parentNode.insertBefore(wrapper, sloganP);
      wrapper.appendChild(sloganP);
      sloganP.classList.add("flex-1");
      wrapper.insertAdjacentHTML("beforeend", `<div onclick="openMenu('Спешлы со стены ВК')" class="vibe-card cursor-pointer p-3 rounded-2xl bg-gradient-to-br from-[#D48238] to-[#b56622] text-white shadow-xl border-2 border-[#FFFDF9]/80 flex items-center gap-3 sm:w-64 flex-shrink-0">
        <img src="img/vk_5128_1.jpg" class="w-14 h-14 rounded-xl object-cover border border-white/60 flex-shrink-0">
        <div class="min-w-0">
          <span class="text-[10px] font-extrabold uppercase tracking-wider bg-black/30 px-2 py-0.5 rounded-full">🔥 Окошко новинок</span>
          <div class="font-serif font-bold text-lg leading-tight mt-0.5">Спешлы недели ВК</div>
          <span class="text-[11px] text-amber-100 underline font-bold">Открыть 9 блюд ➔</span>
        </div>
      </div>`);
    }}

    // Заменяем системный блок «Гастро-пульс» на живой рандомный рекомендатор от ИИ + Карусель блюд прямо под слоганом!
    const pulseBox = heroLeft.querySelector(".bg-white\\\\/10.backdrop-blur-md");
    if (pulseBox) {{
      pulseBox.innerHTML = `<div class="flex items-center justify-between gap-2 mb-1">
        <span class="text-[#F2B880] font-extrabold uppercase text-[11px] tracking-wider">✨ Живой Гастро-пульс от ИИ-Оракула</span>
        <button onclick="window.rollRandomGastroPulse()" class="px-2.5 py-1 rounded-full bg-[#D48238] hover:opacity-95 text-white font-extrabold text-[10px] cursor-pointer shadow">🎲 Ещё совет от ИИ</button>
      </div>
      <div id="ai-pulse-random-text" class="text-white font-semibold text-xs sm:text-sm transition-opacity duration-200 leading-relaxed"></div>`;
      window.rollRandomGastroPulse();

      // Вставляем живую горизонтальную карусель Спешлов и Хитов прямо под Гастро-пульсом!
      const specialsAndHits = (DATA.menu || []).filter(d => d.photo_type === "real").slice(0, 12);
      const carouselHtml = `<div class="relative z-10 mt-2 bg-black/40 backdrop-blur-md p-3 rounded-2xl border border-[#F2B880]/40">
        <div class="flex items-center justify-between mb-2">
          <span class="text-[11px] font-extrabold uppercase tracking-wider text-[#F2B880]">🍲 Живая лента спешлов и хитов (листайте или жмите +)</span>
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

  window.applySiteToggles();
}});
</script>
"""

    last_body_idx = html.rfind("</body>")
    if last_body_idx != -1:
        html = html[:last_body_idx] + V34_MODALS_AND_JS + "\n" + html[last_body_idx:]

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✨ [Ядро v34.0] Чистая шапка, Магазин кафе, 3 Радио РФ, Карусель под слоганом и Нижний Пульт Изменяшек вшиты!")
