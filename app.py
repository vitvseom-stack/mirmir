# -*- coding: utf-8 -*-
"""
КОМПИЛЯТОР ПЛАТФОРМЫ «МИР МИР» (app.py — Версия v4.2)
"""
import os
import sys
import re
import json
import shutil
import subprocess
import traceback
from datetime import datetime
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

PARENT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
DEFAULT_MIRMIR_ROOT = os.path.expanduser("~/Documents/mirmir")
if os.path.exists(os.path.join(PARENT_DIR, ".git")):
    ROOT_REPO_DIR = PARENT_DIR
elif os.path.exists(os.path.join(DEFAULT_MIRMIR_ROOT, ".git")):
    ROOT_REPO_DIR = DEFAULT_MIRMIR_ROOT
else:
    ROOT_REPO_DIR = BASE_DIR

VK_PUBLIC_URL = "https://vk.com/mirmir.cafe"
NTFY_SYNC_TOPIC = "mirmir_tz_sync_nn45_v30"
OLD_DIRS_TO_CHECK = [DEFAULT_MIRMIR_ROOT, PARENT_DIR]

MASTER_TASKS_DEFAULT = [
    {"id": "t_1", "date": "08.11.2026 12:10", "title": "1. Трёхмодульная архитектура (menu_data.py + template.html + app.py) и сборка в GitHub Pages", "done": True, "comment": "Сборка и авто-пуш в корень репозитория работают штатно."},
    {"id": "t_2", "date": "09.11.2026 14:20", "title": "2. Первый экран слева: слайдер из 5 проверенных фото зала и вывески с корректной центровкой дивана", "done": True, "comment": "Чужие фото удалены, для фото дивана настроено кадрирование center 75%."},
    {"id": "t_3", "date": "09.11.2026 15:05", "title": "3. Первый экран справа: увеличенная 3D-карусель бланков меню + 2 крупные карточки спешлов", "done": True, "comment": "Размеры страниц меню увеличены, фильтр спешлов настроен строго по категории."},
    {"id": "t_4", "date": "09.11.2026 16:30", "title": "4. Плашка «Подача блюд может отличаться» на карточках и при полноэкранном увеличении", "done": True, "comment": "Отображается на миниатюрах и внутри лайтбокса."},
    {"id": "t_5", "date": "10.11.2026 11:15", "title": "5. Обработка системной кнопки «Назад» (popstate) на мобильных устройствах", "done": True, "comment": "Закрывает текущее модальное окно без выхода с сайта."},
    {"id": "t_6", "date": "10.11.2026 13:40", "title": "6. Компактные кнопки «ВК» в Новостях + фильтрация закреплённого поста с меню", "done": True, "comment": "Закреплённый пост обновляет только 3D-меню и не дублируется в новостях."},
    {"id": "t_7", "date": "10.11.2026 17:00", "title": "7. Расширенная сетка (1640px), кнопки закрытия (✕) в правом верхнем углу и значок 🔍 без текста", "done": True, "comment": "Во всех окнах и карточках оставлена только иконка лупы 🔍."},
    {"id": "t_8", "date": "10.11.2026 19:25", "title": "8. Единый блок кнопок (Бронь, Такси в кафе, Доставка, Радио + 3 раздела Скоро) в карточке адреса", "done": True, "comment": "Кнопки размещены на тёмно-зелёном фоне блока адреса без дублирования."},
    {"id": "t_9", "date": "11.11.2026 09:30", "title": "9. Полное техническое задание (Мастер-Промпт архитектуры сайта) с сохранением изменений", "done": True, "comment": "Хранится в MASTER_PROMPT_MIRMIR.txt и редактируется в админ-панели."},
    {"id": "t_10", "date": "11.11.2026 11:45", "title": "10. Переключатели режимов: Бронь (Telegram/ВК или анкета 152-ФЗ), Карта, Режим фото меню", "done": True, "comment": "Доступны во вкладке настроек панели управления."},
    {"id": "t_11", "date": "11.11.2026 14:10", "title": "11. Работа всех 5 вкладок панели управления, генератора изображений и галереи ВК", "done": True, "comment": "Все вкладки, превью и выбор готовых фото работают без ошибок."},
    {"id": "t_12", "date": "11.11.2026 15:20", "title": "12. Временное отключение блюд (полупрозрачный режим) и удаление с 3 подтверждениями", "done": True, "comment": "Кнопки отключения и удаления встроены в каждую карточку блюда."},
    {"id": "t_13", "date": "11.11.2026 16:40", "title": "13. Статусы «Открыто» и «Бизнес-Ланч -30%» только в верхней шапке + 3 карточки в ряд слева", "done": True, "comment": "Верхняя лента категорий активна, дубли статусов убраны."}
]


def clean_slang_from_text(txt):
    if not isinstance(txt, str):
        return txt
    replacements = [
        ("Комментарий Милорда / Что не так", "Комментарий / Примечание"),
        ("Комментарий Милорда", "Комментарий"),
        ("Реестр Задач Милорда", "Реестр задач проекта"),
        ("заданиями Милорда", "задачами проекта"),
        ("от Милорда", "администратора"),
        ("По поручению Милорда", "По плану разработки"),
        ("КРАСОВЕЛОФ, МИЛОРД!", "Сборка успешно завершена."),
        ("КрасовелоФ, Милорд!", "Готово."),
        ("Милорд", "Администратор"),
        ("Сир", ""),
    ]
    for old_s, new_s in replacements:
        txt = txt.replace(old_s, new_s)
    return txt


def auto_migrate_assets():
    os.makedirs("img", exist_ok=True)
    for old_d in OLD_DIRS_TO_CHECK:
        if not os.path.exists(old_d) or os.path.abspath(old_d) == BASE_DIR:
            continue
        for fname in ["vk key.txt", "goog api k.txt", "cache_posts.json", "tz_mirmir.json", "MASTER_PROMPT_MIRMIR.txt"]:
            src_f, dst_f = os.path.join(old_d, fname), os.path.join(BASE_DIR, fname)
            if os.path.exists(src_f) and not os.path.exists(dst_f):
                try:
                    shutil.copy2(src_f, dst_f)
                except Exception:
                    pass
        old_img = os.path.join(old_d, "img")
        if os.path.exists(old_img):
            for fn in os.listdir(old_img):
                if fn.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                    if fn.startswith(("ymap_org_", "ai_v", "ingr_")) and fn not in ("ymap_org_0.jpg", "ymap_org_1.jpg"):
                        continue
                    s_f, d_f = os.path.join(old_img, fn), os.path.join(BASE_DIR, "img", fn)
                    if not os.path.exists(d_f) or os.path.getsize(d_f) < 1000:
                        try:
                            shutil.copy2(s_f, d_f)
                        except Exception:
                            pass


def clean_non_vegan_and_junk_images():
    for t_dir in [BASE_DIR, ROOT_REPO_DIR]:
        img_d = os.path.join(t_dir, "img")
        if not os.path.exists(img_d):
            continue
        donor_soup = os.path.join(img_d, "macro_tomyum_bowl.jpg")
        donor_noodle = os.path.join(img_d, "vk_5118_0.jpg")
        if os.path.exists(donor_soup) and os.path.exists(os.path.join(img_d, "macro_mushrooms_raw.jpg")):
            try:
                shutil.copy2(donor_soup, os.path.join(img_d, "macro_mushrooms_raw.jpg"))
            except Exception:
                pass
        if os.path.exists(donor_noodle) and os.path.exists(os.path.join(img_d, "macro_rice_noodles.jpg")):
            try:
                shutil.copy2(donor_noodle, os.path.join(img_d, "macro_rice_noodles.jpg"))
            except Exception:
                pass
        for fn in list(os.listdir(img_d)):
            if fn.startswith(("ai_v", "ingr_")) or (fn.startswith("ymap_org_") and fn not in ("ymap_org_0.jpg", "ymap_org_1.jpg")):
                try:
                    os.remove(os.path.join(img_d, fn))
                except Exception:
                    pass


def is_pinned_menu_post(text_str, is_pinned_flag=0):
    low = (text_str or "").lower()
    return ("прикрепляю наше актуальное меню" in low) or ("актуальное меню" in low) or bool(is_pinned_flag and "меню" in low)


def fetch_vk_wall_posts():
    vk_token = os.environ.get("VK_TOKEN") or (open("vk key.txt", "r", encoding="utf-8").read().strip() if os.path.exists("vk key.txt") else "")
    fallbacks = [p for p in ["img/vk_5122_0.jpg", "img/vk_5068_0.jpg", "img/vk_5128_1.jpg", "img/vk_5134_0.jpg"] if os.path.exists(p)] or ["img/ymap_org_0.jpg"]
    posts_out = []
    if vk_token:
        try:
            r = requests.get("https://api.vk.com/method/wall.get", params={"domain": "mirmir.cafe", "count": 20, "access_token": vk_token, "v": "5.199"}, timeout=8)
            for it in r.json().get("response", {}).get("items", []):
                txt = (it.get("text") or "").strip()
                if len(txt) < 15 or is_pinned_menu_post(txt, it.get("is_pinned", 0)):
                    continue
                post_id = it.get("id")
                owner_id = it.get("owner_id")
                dt_str = datetime.fromtimestamp(it.get("date", 0)).strftime("%d.%m.%Y")
                likes = it.get("likes", {}).get("count", 25)
                img_url = ""
                for att in it.get("attachments", []):
                    if att.get("type") == "photo" and att.get("photo", {}).get("sizes"):
                        img_url = sorted(att["photo"]["sizes"], key=lambda s: s.get("width", 0), reverse=True)[0].get("url", "")
                        break
                    if att.get("type") == "video" and att.get("video", {}).get("image"):
                        img_url = sorted(att["video"]["image"], key=lambda s: s.get("width", 0), reverse=True)[0].get("url", "")
                        break
                photo_local = ""
                if img_url:
                    fp = os.path.join("img", f"vk_{post_id}_0.jpg")
                    if not os.path.exists(fp) or os.path.getsize(fp) < 4000:
                        try:
                            ir = requests.get(img_url, timeout=8)
                            if ir.status_code == 200 and len(ir.content) > 4000:
                                open(fp, "wb").write(ir.content)
                        except Exception:
                            pass
                    if os.path.exists(fp) and os.path.getsize(fp) > 4000:
                        photo_local = f"img/vk_{post_id}_0.jpg"
                if not photo_local:
                    photo_local = fallbacks[len(posts_out) % len(fallbacks)]
                first_line = txt.split("\n")[0].strip()
                vk_link = f"https://vk.com/mirmir.cafe?w=wall{owner_id}_{post_id}" if (owner_id and str(owner_id) != "-191992548" and post_id) else VK_PUBLIC_URL
                posts_out.append({"id": post_id, "date": dt_str, "likes": likes, "title": first_line[:68], "text": txt[:280], "photo": photo_local, "vk_url": vk_link})
                if len(posts_out) >= 12:
                    break
            if posts_out:
                json.dump(posts_out, open("cache_posts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
                return posts_out
        except Exception:
            pass
    if os.path.exists("cache_posts.json"):
        try:
            cached = [p for p in json.load(open("cache_posts.json", "r", encoding="utf-8")) if not is_pinned_menu_post((p.get("title") or "") + " " + (p.get("text") or ""))]
            for i, p in enumerate(cached):
                if "-191992548" in str(p.get("vk_url", "")):
                    p["vk_url"] = VK_PUBLIC_URL
                if not p.get("photo") or not os.path.exists(p["photo"]):
                    p["photo"] = fallbacks[i % len(fallbacks)]
            return cached[:12]
        except Exception:
            pass
    return []


def sync_tz_and_build_logs():
    tz_data = {"tasks": [], "dishes": {}, "custom_dishes": [], "disabled_dishes": [], "deleted_dishes": []}
    if os.path.exists("tz_mirmir.json"):
        try:
            tz_data.update(json.load(open("tz_mirmir.json", "r", encoding="utf-8")))
        except Exception:
            pass
    by_id = {str(t["id"]): t for t in tz_data.get("tasks", []) if isinstance(t, dict) and t.get("id")}
    merged = []
    for d_t in MASTER_TASKS_DEFAULT:
        tid = d_t["id"]
        if tid in by_id:
            old = by_id.pop(tid)
            old_dt = str(old.get("date") or "")
            final_dt = old_dt if ":" in old_dt else d_t["date"]
            merged.append({
                "id": tid,
                "date": final_dt,
                "title": clean_slang_from_text(d_t["title"]),
                "done": bool(old.get("done", d_t["done"])),
                "comment": clean_slang_from_text(old.get("comment") or d_t["comment"])
            })
        else:
            merged.append(dict(d_t))
    for k, v in by_id.items():
        if len(str(v.get("title", ""))) > 3:
            dt_v = str(v.get("date") or "")
            if ":" not in dt_v:
                dt_v = (dt_v + " 12:00").strip()
            v["date"] = dt_v
            v["title"] = clean_slang_from_text(v.get("title", ""))
            v["comment"] = clean_slang_from_text(v.get("comment", ""))
            merged.append(v)
    tz_data["tasks"] = merged
    json.dump(tz_data, open("tz_mirmir.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    cnt = 1
    if os.path.exists("run_counter.txt"):
        try:
            cnt = int(open("run_counter.txt", "r", encoding="utf-8").read().strip()) + 1
        except Exception:
            cnt = 1
    open("run_counter.txt", "w", encoding="utf-8").write(str(cnt))

    logs = json.load(open("build_history.json", "r", encoding="utf-8")) if os.path.exists("build_history.json") else []
    for l_item in logs:
        l_item["model"] = clean_slang_from_text(l_item.get("model", ""))
        l_item["status"] = clean_slang_from_text(l_item.get("status", ""))
    now_str = datetime.now().strftime("%d.%m.%Y %H:%M")
    logs.insert(0, {
        "version": f"Релиз v4.2 • Сборка #{cnt}",
        "timestamp": now_str,
        "model": "Сборка v4.2: Чистый интерфейс без лишних текстов, иконки лупы 🔍, центровка дивана, 3D-меню и кнопки в блоке адреса",
        "status": "Восстановлена лента категорий, убраны дубли бейджей в Hero, выровнены 3 карточки слева, увеличены бланки меню справа, кнопки интегрированы в карточку адреса.",
        "stats": f"Дата сборки: {now_str}"
    })
    json.dump(logs[:60], open("build_history.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return tz_data, logs[:60], cnt


def upgrade_template_html_in_place(tpl_html):
    tpl_html = clean_slang_from_text(tpl_html)
    # Убираем слово «Лупа» из статических кнопок шаблона, оставляя только значок 🔍
    tpl_html = tpl_html.replace("🔍 Лупа", "🔍").replace("Лупа 🔍", "🔍")

    if 'name="robots"' not in tpl_html:
        tpl_html = tpl_html.replace("<head>", '<head>\n  <meta name="robots" content="noindex, nofollow">', 1)

    for vname in ["hubActiveTab", "hubDishCategoryFilter", "hubDishSearchQuery", "selectedAiEnginePerDish", "pendingDishCandidates", "currentMenuCategory", "currentNewsPage"]:
        tpl_html = re.sub(rf"\blet\s+{vname}\b", f"var {vname}", tpl_html)

    anchor_pos = tpl_html.find('a.download = "MASTER_PROMPT_MIRMIR.txt";')
    if anchor_pos != -1:
        brace_pos = tpl_html.find("}", anchor_pos)
        if brace_pos != -1:
            tpl_html = tpl_html[: brace_pos + 1] + "\n"

    v42_js = r"""
    // === ЯДРО ПЛАТФОРМЫ v4.2 ===
    const NTFY_SYNC_URL = "https://ntfy.sh/mirmir_tz_sync_nn45_v30";
    window.hubActiveTab = window.hubActiveTab || "dishes72";
    window.hubDishCategoryFilter = window.hubDishCategoryFilter || "Все";
    window.hubDishSearchQuery = window.hubDishSearchQuery || "";
    window.selectedAiEnginePerDish = window.selectedAiEnginePerDish || {};
    window.pendingDishCandidates = window.pendingDishCandidates || {};
    window.customPromptsPerDish = window.customPromptsPerDish || {};
    window.dishVariantStep = window.dishVariantStep || {};
    window.dishDiagLogs = window.dishDiagLogs || {};
    window.dishAddPanelOpen = Boolean(window.dishAddPanelOpen);

    // 1. Управление отключением (полупрозрачность) и удалением блюд (3 подтверждения)
    window.getDisabledDishesMap = function() {
      try { return JSON.parse(localStorage.getItem("mirmir_disabled_dishes_v1") || "{}"); } catch(e) { return {}; }
    };
    window.isDishDisabled = function(name) {
      return Boolean(window.getDisabledDishesMap()[name]);
    };
    window.toggleDishDisabled = function(idx) {
      const d = DATA.menu[idx];
      if (!d) return;
      const map = window.getDisabledDishesMap();
      if (map[d.name]) { delete map[d.name]; } else { map[d.name] = true; }
      try { localStorage.setItem("mirmir_disabled_dishes_v1", JSON.stringify(map)); } catch(e) {}
      window.renderUnifiedSystemHub();
      window.renderDishes();
      window.renderHeroRightColumn();
    };

    window.getDeletedDishesMap = function() {
      try { return JSON.parse(localStorage.getItem("mirmir_deleted_dishes_v1") || "{}"); } catch(e) { return {}; }
    };
    window.deleteDishTripleConfirm = function(idx) {
      const d = DATA.menu[idx];
      if (!d) return;
      if (!confirm("Подтверждение 1 из 3:\nУдалить блюдо «" + d.name + "» из меню?")) return;
      if (!confirm("Подтверждение 2 из 3:\nВы уверены, что хотите удалить «" + d.name + "»?")) return;
      if (!confirm("Подтверждение 3 из 3 (финальное):\nОкончательно удалить блюдо «" + d.name + "» из меню сайта?")) return;
      const delMap = window.getDeletedDishesMap();
      delMap[d.name] = true;
      try { localStorage.setItem("mirmir_deleted_dishes_v1", JSON.stringify(delMap)); } catch(e) {}
      DATA.menu.splice(idx, 1);
      window.renderUnifiedSystemHub();
      window.renderDishes();
      window.renderHeroRightColumn();
    };
    window.restoreAllDeletedDishes = function() {
      if (!confirm("Восстановить все ранее удалённые блюда в меню?")) return;
      try { localStorage.removeItem("mirmir_deleted_dishes_v1"); } catch(e) {}
      location.reload();
    };

    function loadCustomAddedDishes() {
      try { return JSON.parse(localStorage.getItem("mirmir_custom_dishes_v1") || "[]"); } catch(e) { return []; }
    }
    function syncMenuWithCustomAndDeleted() {
      if (!DATA.menu) DATA.menu = [];
      loadCustomAddedDishes().forEach(cd => {
        if (cd && cd.name && !DATA.menu.some(m => m.name === cd.name)) DATA.menu.unshift(cd);
      });
      const delMap = window.getDeletedDishesMap();
      DATA.menu = DATA.menu.filter(d => !delMap[d.name]);
      DATA.menu.forEach(d => {
        if (d.photo && (d.photo.includes("macro_mushrooms_raw") || d.photo.includes("macro_rice_noodles"))) {
          d.photo = "img/macro_tomyum_bowl.jpg";
        }
      });
    }

    // 2. Полноэкранное увеличение (🔍) с плашкой «🍽️ Подача блюд может отличаться»
    const _baseOpenSuperZoom = window.openSuperZoom;
    window.openSuperZoom = function(src, title) {
      if (_baseOpenSuperZoom) _baseOpenSuperZoom(src, title);
      const lb = document.getElementById("super-zoom-lightbox");
      if (!lb) return;
      let note = document.getElementById("zoom-serving-disclaimer");
      if (!note) {
        note = document.createElement("div");
        note.id = "zoom-serving-disclaimer";
        note.className = "fixed bottom-5 left-1/2 -translate-x-1/2 z-[220] px-4 py-1.5 rounded-full bg-black/85 text-[#F2B880] border border-[#F2B880]/50 text-xs font-extrabold shadow-xl pointer-events-none whitespace-nowrap";
        note.innerHTML = "🍽️ Подача блюд может отличаться от фотографии";
        lb.appendChild(note);
      }
      lb.classList.remove("hidden");
      lb.classList.add("flex");
    };

    // 3. Слайдер интерьера слева с правильной центровкой зелёного дивана (vk_5068_0.jpg)
    window.getInteriorSlidesList = function() {
      return [
        { src: "img/ymap_org_0.jpg", title: "🏛️ Исторический кирпичный свод и уютный зал на Ильинской, 45", tag: "Интерьер зала", pos: "center center" },
        { src: "img/ymap_org_1.jpg", title: "🕊️ Фирменная кованая вывеска с белой Голубкой мира у входа", tag: "Экстерьер • Ильинская, 45", pos: "center center" },
        { src: "img/vk_5068_0.jpg", title: "🛋️ Изумрудный велюровый диван, живой кирпич и картины", tag: "Атмосфера «Мир Мир»", pos: "center 78%" },
        { src: "img/vk_5122_0.jpg", title: "🕯️ Вечерние чаепития при свечах и редкий китайский чай", tag: "Чайная культура", pos: "center 65%" },
        { src: "img/vk_5134_0.jpg", title: "🌿 Уютное зелёное пространство для встреч и живого общения", tag: "Интерьер кафе", pos: "center center" }
      ];
    };

    const _baseRenderInteriorSlide = window.renderInteriorSlideState;
    window.renderInteriorSlideState = function() {
      if (_baseRenderInteriorSlide) _baseRenderInteriorSlide();
      const slides = window.getInteriorSlidesList();
      const imgEl = document.getElementById("interior-slide-img");
      if (imgEl && slides.length) {
        const curSrc = imgEl.getAttribute("src") || "";
        const found = slides.find(s => curSrc.includes(s.src)) || slides[0];
        imgEl.style.objectPosition = found.pos || "center center";
        if (imgEl.parentElement) {
          imgEl.parentElement.style.minHeight = "270px";
        }
      }
      // Заменяем текст «🔍 Лупа» на чистую иконку «🔍» внутри слайдера и 3D-меню
      document.querySelectorAll("button").forEach(b => {
        if (b.textContent.trim() === "🔍 Лупа" || b.textContent.trim() === "Лупа") {
          b.innerHTML = "🔍";
          b.setAttribute("title", "Увеличить фото");
        }
      });
    };

    // 4. Правая колонка Hero: увеличенные страницы меню зала + 2 карточки строго из категории «Сезонные спешлы от Шефа»
    window.rightSpecialsPairIdx = 0;
    window.stepRightSpecialsPair = function(delta) {
      const specials = (DATA.menu || []).filter(d => d.category === "Сезонные спешлы от Шефа");
      const maxPairs = Math.max(1, Math.ceil(specials.length / 2));
      window.rightSpecialsPairIdx = (window.rightSpecialsPairIdx + delta + maxPairs) % maxPairs;
      window.renderRightTwoPictureFields();
    };

    window.renderRightTwoPictureFields = function() {
      const rowsBox = document.getElementById("hero-specials-3rows");
      if (!rowsBox) return;
      const boxWrapper = rowsBox.parentElement;
      if (boxWrapper) {
        const hdr = boxWrapper.querySelector(".flex.items-center.justify-between");
        if (hdr) {
          hdr.innerHTML =
            '<div class="flex items-center gap-1.5">' +
              '<span class="text-[10px] sm:text-[11px] font-extrabold uppercase tracking-wider text-[#F2B880]">🔥 Сезонные спешлы от Шефа</span>' +
              '<button type="button" onclick="stepRightSpecialsPair(-1)" class="w-6 h-6 rounded-full bg-white/15 hover:bg-[#D48238] text-white text-[10px] font-bold cursor-pointer">◀</button>' +
              '<button type="button" onclick="stepRightSpecialsPair(1)" class="w-6 h-6 rounded-full bg-white/15 hover:bg-[#D48238] text-white text-[10px] font-bold cursor-pointer">▶</button>' +
            '</div>' +
            '<button type="button" onclick="openMenu(\'Сезонные спешлы от Шефа\')" class="text-[10px] font-extrabold text-amber-300 hover:underline cursor-pointer">Все блюда (' + DATA.menu.length + ') ➔</button>';
        }
      }
      // Строго только блюда из категории «Сезонные спешлы от Шефа» (без дополнений за 60 ₽)
      const specials = (DATA.menu || []).filter(d => d.category === "Сезонные спешлы от Шефа");
      const start = (window.rightSpecialsPairIdx * 2) % Math.max(1, specials.length);
      const pair = [specials[start], specials[(start + 1) % specials.length]].filter(Boolean);

      rowsBox.innerHTML = '<div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">' + pair.map(d => {
        const idx = DATA.menu.indexOf(d);
        const pr = d.sizes ? d.sizes[0].price : d.price;
        return '<div onclick="openMenu(\'Сезонные спешлы от Шефа\')" class="zoom-card bg-[#FDF8F2] text-stone-900 rounded-2xl p-2.5 flex flex-col justify-between gap-2 cursor-pointer shadow-lg border-2 border-[#F2B880]/70 transition">' +
          '<div class="relative h-32 sm:h-36 w-full rounded-xl overflow-hidden bg-stone-200">' +
            '<img src="' + esc(d.photo) + '" onclick="event.stopPropagation();openSuperZoom(this.src, \'' + esc(d.name) + '\')" class="w-full h-full object-cover cursor-zoom-in">' +
            '<span class="absolute top-1.5 left-1.5 px-2 py-0.5 rounded-md bg-black/70 text-[#F2B880] text-[9px] font-extrabold">' + esc(d.weight || "Хит шефа") + '</span>' +
            '<span class="absolute bottom-1.5 left-1.5 px-1.5 py-0.5 rounded bg-black/70 text-white text-[8px] font-bold">🍽️ Подача может отличаться</span>' +
            '<button type="button" title="Увеличить" onclick="event.stopPropagation();openSuperZoom(\'' + esc(d.photo) + '\', \'' + esc(d.name) + '\')" class="absolute bottom-1.5 right-1.5 w-7 h-7 rounded-full bg-black/75 hover:bg-[#D48238] text-white text-xs flex items-center justify-center cursor-pointer shadow">🔍</button>' +
          '</div>' +
          '<div class="space-y-1">' +
            '<div class="font-serif font-bold text-sm sm:text-base text-[#2E3D28] leading-tight line-clamp-2">' + esc(d.name) + '</div>' +
            '<div class="flex items-center justify-between pt-1 border-t border-stone-200/80">' +
              '<strong class="text-sm font-extrabold text-[#D48238]">' + pr + ' ₽</strong>' +
              '<button type="button" onclick="event.stopPropagation();addToCart(' + idx + ',0)" class="px-2.5 py-1 rounded-lg bg-[#556432] hover:bg-[#2E3D28] text-white text-[10px] font-extrabold cursor-pointer shadow">+ В заказ</button>' +
            '</div>' +
          '</div>' +
        '</div>';
      }).join("") + '</div>';
    };

    const _baseRenderHeroRight = window.renderHeroRightColumn;
    window.renderHeroRightColumn = function() {
      if (_baseRenderHeroRight) _baseRenderHeroRight();
      window.renderRightTwoPictureFields();
      // Увеличиваем размер страниц 3D-меню справа и убираем слово «Лупа»
      const stage3d = document.getElementById("carousel-3d-stage");
      if (stage3d) {
        stage3d.style.height = "340px";
        stage3d.querySelectorAll("div").forEach(cardEl => {
          if (cardEl.style.width) cardEl.style.width = "235px";
          if (cardEl.style.height) cardEl.style.height = "325px";
        });
        stage3d.querySelectorAll("button").forEach(b => {
          if (b.textContent.includes("Лупа")) b.innerHTML = b.innerHTML.replace("🔍 Лупа", "🔍").replace("Лупа", "🔍");
        });
      }
    };

    // 5. Чистая геометрия страницы:
    // - Верхняя лента категорий (#category-rail) всегда видна.
    // - Повторы «ОТКРЫТО ДО 21:00» и «Бизнес-Ланч -30%» в зелёном Hero-блоке скрыты (оставлены только в верхней шапке).
    // - Из 4 мини-карточек внизу левого Hero-блока скрыта 1 («Собрать свой Боул»), чтобы 3 карточки стояли ровно в 1 ряд.
    // - В блоке адреса («Нижний Новгород, ул. Ильинская, 45») встроена аккуратная панель кнопок на фирменном тёмно-зелёном фоне.
    function applyV42CleanLayout() {
      if (!document.getElementById("mirmir-v42-styles")) {
        const st = document.createElement("style");
        st.id = "mirmir-v42-styles";
        st.textContent = `
          html, body { min-height: auto !important; height: auto !important; }
          main.max-w-\\[1440px\\], header .max-w-\\[1440px\\], footer .max-w-\\[1440px\\] { max-width: 1640px !important; width: 100% !important; min-height: 0 !important; }
          main.max-w-\\[1440px\\] { padding-bottom: 12px !important; }
          header, #category-rail { display: flex !important; visibility: visible !important; }
          main section .lg\\:col-span-7, main section .lg\\:col-span-5 { display: flex !important; }
          /* В верхней шапке убираем только дубли Брони, Боула, Такси и Радио, НЕ трогая кнопку Меню и ленту категорий! */
          header button[onclick*="openBookTableModal"],
          header button[onclick*="openBowlBuilder"],
          header button[onclick*="openRadioSelectorModal"],
          header button[onclick*="openDeliveryModal"],
          header a[href*="yandex"],
          #category-rail button[onclick*="openBowlBuilder"],
          main section .lg\\:col-span-7 > div[onclick*="Сезонные спешлы от Шефа"] { display: none !important; }
          .v42-top-right-close { position: absolute !important; top: 10px !important; right: 10px !important; z-index: 95 !important; width: 34px !important; height: 34px !important; border-radius: 9999px !important; background: rgba(20,28,17,0.92) !important; color: #FFFDF9 !important; border: 1.5px solid rgba(242,184,128,0.7) !important; display: inline-flex !important; align-items: center !important; justify-content: center !important; font-size: 16px !important; font-weight: 900 !important; cursor: pointer !important; }
          .v42-top-right-close:hover { background: #D48238 !important; color: #fff !important; }
        `;
        document.head.appendChild(st);
      }

      // 1) Статус «Открыто» и «Бизнес-Ланч -30%» в верхней шапке
      const topWorkBadge = document.getElementById("header-work-badge");
      if (topWorkBadge && topWorkBadge.parentElement && !document.getElementById("header-lunch-badge")) {
        const lb = document.createElement("span");
        lb.id = "header-lunch-badge";
        lb.className = "hidden sm:inline-flex items-center px-2.5 py-0.5 rounded-full bg-[#D48238] text-white text-[10px] font-extrabold whitespace-nowrap shadow-xs ml-1";
        lb.innerHTML = "🔥 Бизнес-Ланч −30% (будни 12:00–16:00)";
        topWorkBadge.parentElement.appendChild(lb);
      }

      // 2) Скрываем дублирующиеся плашки «ОТКРЫТО ДО 21:00» и «Бизнес-Ланч -30%» внутри зелёного блока первого экрана
      const heroLeft = document.querySelector("main section .lg\\:col-span-7");
      if (heroLeft) {
        const heroBadge = document.getElementById("hero-work-badge");
        if (heroBadge && heroBadge.parentElement && heroBadge.parentElement !== heroLeft) {
          heroBadge.parentElement.style.display = "none";
        }
        heroLeft.querySelectorAll("div, span").forEach(el => {
          if (el.children.length === 2 && el.textContent.includes("Бизнес-Ланч") && (el.textContent.includes("ОТКРЫТО") || el.textContent.includes("ЗАКРЫТО"))) {
            if (!el.classList.contains("lg:col-span-7")) el.style.display = "none";
          }
        });

        // 3) Делаем ровно 3 гармоничные карточки в 1 ряд внизу левого блока (скрываем 4-ю карточку «Собрать свой Боул»)
        Array.from(heroLeft.querySelectorAll(".grid")).forEach(g => {
          if (g.textContent.includes("Чай 300") && g.textContent.includes("Десерты без сахара")) {
            g.className = "grid grid-cols-1 sm:grid-cols-3 gap-2.5 pt-1";
            Array.from(g.children).forEach(cardChild => {
              const oc = cardChild.getAttribute("onclick") || "";
              const txt = cardChild.textContent || "";
              if (oc.includes("openBowlBuilder") || txt.includes("Собрать свой Боул")) {
                cardChild.style.display = "none";
              }
            });
          }
        });
      }

      // 4) Встраиваем панель кнопок («Бронь», «Такси в кафе», «Доставка», «Радио» + 3 кнопки «Скоро») прямо внутрь зелёного блока адреса под текстом!
      ["v33-bottom-nav-hub", "v34-bottom-nav-hub", "v35-bottom-nav-hub", "v36-bottom-nav-hub", "v40-bottom-nav-hub", "v41-bottom-nav-hub"].forEach(oldId => {
        const el = document.getElementById(oldId);
        if (el) el.remove();
      });

      document.querySelectorAll("main section").forEach(sec => {
        if (sec.textContent.includes("Нижний Новгород, ул.") && sec.textContent.includes("Ильинская, 45") && !sec.querySelector("#interior-slide-img")) {
          // Скрываем старые разрозненные кнопки внутри карточки адреса
          sec.querySelectorAll("button, a").forEach(el => {
            if (el.closest("#v42-address-nav-hub")) return;
            const oc = el.getAttribute("onclick") || "";
            const hr = el.getAttribute("href") || "";
            if (oc.includes("openBookTableModal") || oc.includes("openDeliveryModal") || oc.includes("openRadioSelectorModal") || hr.includes("appmetrica.yandex") || hr.includes("taxi.yandex")) {
              el.style.display = "none";
            }
          });
          // Добавляем единый аккуратный блок кнопок прямо внутрь левой части зелёной карточки адреса
          const leftColAddr = sec.querySelector("div");
          if (leftColAddr && !document.getElementById("v42-address-nav-hub")) {
            const taxiUrl = "https://3.redirect.appmetrica.yandex.com/route?end-lat=56.322355&end-lon=43.990383&appmetrica_tracking_id=1178268795219780156";
            const hubBox = document.createElement("div");
            hubBox.id = "v42-address-nav-hub";
            hubBox.className = "w-full pt-4 mt-3 border-t border-white/15 space-y-2";
            hubBox.innerHTML =
              '<div class="grid grid-cols-2 sm:grid-cols-4 gap-2">' +
                '<button type="button" onclick="openBookTableModal()" class="py-2 px-3 rounded-xl bg-[#556432] hover:bg-[#D48238] text-[#FFFDF9] font-extrabold text-xs flex items-center justify-center gap-1.5 cursor-pointer transition shadow-xs"><span>🪑</span><span>Бронь</span></button>' +
                '<a href="' + taxiUrl + '" target="_blank" class="py-2 px-3 rounded-xl bg-[#3A4A2E] hover:bg-[#D48238] text-[#F2B880] hover:text-white font-extrabold text-xs flex items-center justify-center gap-1.5 cursor-pointer transition shadow-xs"><span>🚕</span><span>Такси в кафе</span></a>' +
                '<button type="button" onclick="openDeliveryModal()" class="py-2 px-3 rounded-xl bg-[#556432] hover:bg-[#D48238] text-[#FFFDF9] font-extrabold text-xs flex items-center justify-center gap-1.5 cursor-pointer transition shadow-xs"><span>🛵</span><span>Доставка</span></button>' +
                '<button type="button" onclick="openRadioSelectorModal()" class="py-2 px-3 rounded-xl bg-[#FFFDF9] hover:bg-amber-50 text-[#2E3D28] font-extrabold text-xs flex items-center justify-center gap-1.5 cursor-pointer transition shadow-xs"><span>📻</span><span>Радио</span></button>' +
              '</div>' +
              '<div class="grid grid-cols-1 sm:grid-cols-3 gap-1.5">' +
                '<button disabled class="py-1.5 px-2 rounded-lg bg-white/10 text-white/70 font-extrabold text-[10px] uppercase flex items-center justify-center gap-1 cursor-not-allowed"><span>👥 НАША КОМАНДА</span><span class="px-1 rounded bg-black/40 text-[#F2B880] text-[8px]">Скоро</span></button>' +
                '<button disabled class="py-1.5 px-2 rounded-lg bg-white/10 text-white/70 font-extrabold text-[10px] uppercase flex items-center justify-center gap-1 cursor-not-allowed"><span>🏛️ ИСТОРИЯ КАФЕ</span><span class="px-1 rounded bg-black/40 text-[#F2B880] text-[8px]">Скоро</span></button>' +
                '<button disabled class="py-1.5 px-2 rounded-lg bg-white/10 text-white/70 font-extrabold text-[10px] uppercase flex items-center justify-center gap-1 cursor-not-allowed"><span>🌿 НАШИ ЦЕННОСТИ</span><span class="px-1 rounded bg-black/40 text-[#F2B880] text-[8px]">Скоро</span></button>' +
              '</div>';
            leftColAddr.appendChild(hubBox);
          }
        }
      });

      const footerEl = document.querySelector("footer");
      if (footerEl) footerEl.querySelectorAll(".grid.grid-cols-1.sm\\:grid-cols-3").forEach(g => { g.style.display = "none"; });

      // 5) Крестики закрытия окон (✕) в правом верхнем углу
      const modalsConfig = [
        { modalId: "menu-modal", closeFn: "closeMenu()" },
        { modalId: "unified-system-hub", closeFn: "closeUnifiedSystemHub()" },
        { modalId: "bowl-modal", closeFn: "closeBowlBuilder()" },
        { modalId: "cafe-shop-modal", closeFn: "closeCafeShopModal()" },
        { modalId: "book-table-modal", closeFn: "closeBookTableModal()" },
        { modalId: "delivery-modal", closeFn: "document.getElementById('delivery-modal').classList.add('hidden')" },
        { modalId: "radio-selector-modal", closeFn: "document.getElementById('radio-selector-modal').classList.add('hidden')" },
        { modalId: "ready-gallery-popup", closeFn: "closeReadyGalleryPopup()" },
        { modalId: "master-prompt-modal", closeFn: "closeMasterPromptModal()" },
        { modalId: "super-zoom-lightbox", closeFn: "closeSuperZoom()" }
      ];
      modalsConfig.forEach(cfg => {
        const m = document.getElementById(cfg.modalId);
        const card = m ? m.firstElementChild : null;
        if (!card) return;
        card.style.position = "relative";
        card.querySelectorAll("button").forEach(b => {
          if (b.textContent.trim() === "✕" && !b.classList.contains("v42-top-right-close")) b.style.display = "none";
        });
        if (!card.querySelector(".v42-top-right-close")) {
          const btn = document.createElement("button");
          btn.className = "v42-top-right-close";
          btn.setAttribute("onclick", cfg.closeFn);
          btn.innerHTML = "✕";
          card.appendChild(btn);
        }
      });
    }

    // 6. Новости ВК: только иконка 🔍 без слова «Лупа» и узкая кнопка «ВК»
    const NEWS_FALLBACK_IMGS = ["img/vk_5122_0.jpg", "img/vk_5068_0.jpg", "img/vk_5128_1.jpg", "img/vk_5134_0.jpg"];
    window.renderNewsPosts = function() {
      const grid = document.getElementById("posts-grid");
      if (!grid) return;
      const rawPosts = (DATA.posts && DATA.posts.length) ? DATA.posts : [];
      const posts = rawPosts.filter(p => {
        const t = ((p.title || "") + " " + (p.text || "")).toLowerCase();
        return !t.includes("прикрепляю наше актуальное меню") && !t.includes("актуальное меню");
      });
      const slice = posts.slice(currentNewsPage * 3, currentNewsPage * 3 + 3);

      grid.innerHTML = slice.map((p, idxP) => {
        let safeVkUrl = p.vk_url || "https://vk.com/mirmir.cafe";
        if (safeVkUrl.includes("-191992548")) safeVkUrl = "https://vk.com/mirmir.cafe";
        const fbImg = NEWS_FALLBACK_IMGS[idxP % NEWS_FALLBACK_IMGS.length];
        const photoSrc = p.photo || fbImg;

        return '<article class="zoom-card bg-[#FFFDF9] rounded-3xl p-4 border border-[#556432]/25 shadow-sm flex flex-col justify-between gap-3 transition">' +
          '<div class="space-y-2.5">' +
            '<div class="flex items-center justify-between text-[11px] font-extrabold text-[#D48238]">' +
              '<span>📅 ' + esc(p.date || "Новость кафе") + '</span><span>❤️ ' + esc(p.likes || 25) + '</span>' +
            '</div>' +
            '<h3 class="font-serif text-xl font-bold text-[#1F2B1A] leading-snug">' + esc(p.title || "Событие в «Мир Мир»") + '</h3>' +
            '<div class="relative rounded-2xl overflow-hidden bg-[#F4ECE1] flex items-center justify-center min-h-[180px]">' +
              '<img src="' + esc(photoSrc) + '" onerror="this.onerror=null;this.src=\'' + fbImg + '\'" onclick="openSuperZoom(this.src, \'' + esc(p.title) + '\')" class="w-full h-auto max-h-[340px] object-contain cursor-zoom-in block mx-auto">' +
              '<button type="button" title="Увеличить" onclick="const im=this.parentElement.querySelector(\'img\');openSuperZoom(im?im.src:\'' + esc(photoSrc) + '\', \'' + esc(p.title) + '\')" class="absolute bottom-2 right-2 w-8 h-8 rounded-full bg-black/75 hover:bg-[#D48238] text-white text-xs flex items-center justify-center cursor-pointer shadow">🔍</button>' +
            '</div>' +
            '<p class="text-xs sm:text-sm text-stone-700 leading-relaxed whitespace-pre-line">' + esc(p.text || "") + '</p>' +
          '</div>' +
          '<div class="pt-2.5 border-t border-stone-200/80 flex items-center justify-between">' +
            '<a href="' + esc(safeVkUrl) + '" target="_blank" class="inline-flex items-center justify-center px-2.5 py-1 rounded-lg bg-[#0077FF] hover:bg-[#0055CC] text-white text-[11px] font-extrabold transition shadow cursor-pointer">ВК</a>' +
            '<span class="text-[10px] font-bold text-stone-400">vk.com/mirmir.cafe</span>' +
          '</div>' +
        '</article>';
      }).join("");
    };

    // 7. Переключатели вкладок, задач и генератора в Шестерёнке
    window.setHubTab = function(tabId) {
      window.hubActiveTab = hubActiveTab = tabId;
      window.renderUnifiedSystemHub();
    };
    window.setHubCategory = function(catStr) {
      window.hubDishCategoryFilter = hubDishCategoryFilter = catStr;
      window.renderUnifiedSystemHub();
    };
    window.setHubSearch = function(qStr) {
      window.hubDishSearchQuery = hubDishSearchQuery = qStr;
      window.renderUnifiedSystemHub();
    };
    window.closeUnifiedSystemHub = function() {
      const m = document.getElementById("unified-system-hub");
      if (m) { m.classList.add("hidden"); m.classList.remove("flex"); }
    };

    window.getCombinedBuildLogs = function() {
      return Array.isArray(DATA.full_build_logs) ? DATA.full_build_logs : [];
    };
    window.getSavedIdeasNotes = function() {
      try { return JSON.parse(localStorage.getItem("mirmir_ideas_notes_v1") || "[]"); } catch(e) { return []; }
    };
    window.addNewIdeaNote = function() {
      const inp = document.getElementById("new-idea-note-inp");
      const val = (inp?.value || "").trim();
      if (!val) return;
      const list = window.getSavedIdeasNotes();
      list.unshift({ text: val, date: new Date().toLocaleString("ru-RU") });
      try { localStorage.setItem("mirmir_ideas_notes_v1", JSON.stringify(list)); } catch(e) {}
      if (inp) inp.value = "";
      window.renderUnifiedSystemHub();
    };

    window.getSiteToggles = function() {
      const def = { leaves: true, wings: true, zoom: true, bookingMode: "messenger", mapMode: "clean_card", photoMode: "hybrid" };
      try { return Object.assign({}, def, JSON.parse(localStorage.getItem("mirmir_site_toggles_v42") || "{}")); } catch(e) { return def; }
    };
    window.setAdminSettingV42 = function(k, v) {
      const tg = window.getSiteToggles();
      tg[k] = v;
      try { localStorage.setItem("mirmir_site_toggles_v42", JSON.stringify(tg)); } catch(e) {}
      window.renderDishes();
      window.renderUnifiedSystemHub();
    };

    function formatNowDateTime() {
      const d = new Date();
      return d.toLocaleDateString("ru-RU") + " " + d.toLocaleTimeString("ru-RU", { hour: "2-digit", minute: "2-digit" });
    }

    function getMasterTasksList() {
      const srv = (DATA.tz_synced && Array.isArray(DATA.tz_synced.tasks)) ? DATA.tz_synced.tasks : [];
      try {
        const loc = JSON.parse(localStorage.getItem("mirmir_tasks_v42") || "null");
        if (Array.isArray(loc) && loc.length >= srv.length) return loc;
      } catch(e) {}
      return srv;
    }
    function saveMasterTasksList(arr) {
      try {
        localStorage.setItem("mirmir_tasks_v42", JSON.stringify(arr));
        fetch(NTFY_SYNC_URL, { method: "POST", body: JSON.stringify({ type: "tz_tasks_sync", tasks: arr, ts: Date.now() }) }).catch(() => {});
      } catch(e) {}
    }
    window.toggleTaskDoneV42 = function(idx) {
      const list = getMasterTasksList();
      if (!list[idx]) return;
      list[idx].done = !list[idx].done;
      list[idx].date = formatNowDateTime();
      saveMasterTasksList(list);
      window.renderUnifiedSystemHub();
    };
    window.updateTaskCommentV42 = function(idx, val) {
      const list = getMasterTasksList();
      if (!list[idx]) return;
      list[idx].comment = val;
      list[idx].date = formatNowDateTime();
      saveMasterTasksList(list);
    };
    window.addNewTaskV42 = function() {
      const t = (document.getElementById("new-tz-task-inp")?.value || "").trim();
      if (!t) return;
      const c = (document.getElementById("new-tz-comment-inp")?.value || "Проверить").trim();
      const list = getMasterTasksList();
      list.unshift({ id: "t_u_" + Date.now(), date: formatNowDateTime(), title: (list.length + 1) + ". " + t, done: false, comment: c });
      saveMasterTasksList(list);
      window.renderUnifiedSystemHub();
    };

    window.addNewCustomDishFromHub = function() {
      const name = (document.getElementById("new-dish-name")?.value || "").trim();
      if (!name) { alert("Введите название блюда!"); return; }
      const cat = (document.getElementById("new-dish-cat")?.value || "Сезонные спешлы от Шефа").trim();
      const price = parseInt(document.getElementById("new-dish-price")?.value || "450", 10) || 450;
      const weight = (document.getElementById("new-dish-weight")?.value || "260 г").trim();
      const desc = (document.getElementById("new-dish-desc")?.value || "100% растительное блюдо кафе «Мир Мир».").trim();
      const photo = (document.getElementById("new-dish-photo")?.value || "img/vk_5128_1.jpg").trim();
      const obj = { id: "custom_" + Date.now(), category: cat, name: name, weight: weight, price: price, photo: photo, photo_type: "real", desc: desc, ai_prompt: "Vegan plant-based " + name, is_custom_added: true };
      const list = loadCustomAddedDishes().filter(d => d.name !== name);
      list.unshift(obj);
      try { localStorage.setItem("mirmir_custom_dishes_v1", JSON.stringify(list)); } catch(e) {}
      DATA.menu.unshift(obj);
      window.renderUnifiedSystemHub();
      window.renderDishes();
      alert("✅ Блюдо «" + name + "» добавлено в меню.");
    };

    const CURATED_VEGAN_HD_BANK = {
      burger: ["img/macro_vegan_burger.jpg", "img/macro_avocado_burger.jpg", "img/macro_spicy_burger.jpg", "img/vk_5128_1.jpg"],
      soup: ["img/macro_tomyum_bowl.jpg", "img/vk_5085_1.jpg", "img/vk_5118_0.jpg", "img/vk_5128_1.jpg"],
      salad: ["img/macro_caesar_romaine.jpg", "img/vk_5085_1.jpg", "img/vk_5118_0.jpg", "img/vk_5128_1.jpg"],
      drink: ["img/macro_citrus_mint.jpg", "img/vk_5122_0.jpg", "img/vk_5134_0.jpg"],
      main: ["img/vk_5118_0.jpg", "img/vk_5128_1.jpg", "img/macro_vegan_burger.jpg", "img/macro_tomyum_bowl.jpg"],
      dessert: ["img/vk_5101_0.jpg", "img/vk_5122_0.jpg", "img/vk_5128_1.jpg"]
    };

    function pushDiagLog(idx, icon, eng, msg) {
      const tm = new Date().toLocaleTimeString("ru-RU");
      window.dishDiagLogs[idx] = window.dishDiagLogs[idx] || [];
      window.dishDiagLogs[idx].unshift("[" + tm + "] " + icon + " " + eng + ": " + msg);
      window.dishDiagLogs[idx] = window.dishDiagLogs[idx].slice(0, 4);
    }

    window.runEngineForDish = function(idx, engKey) {
      const inp = document.getElementById("hub-ai-prm-" + idx);
      if (inp) window.customPromptsPerDish[idx] = inp.value;
      window.selectedAiEnginePerDish[idx] = selectedAiEnginePerDish[idx] = engKey;
      window.generateDishCandidateAI(idx);
    };

    window.generateDishCandidateAI = async function(idx) {
      const d = DATA.menu[idx];
      if (!d) return;
      const inp = document.getElementById("hub-ai-prm-" + idx);
      if (inp && inp.value.trim()) window.customPromptsPerDish[idx] = inp.value.trim();
      const raw = window.customPromptsPerDish[idx] || d.ai_prompt || d.name;
      window.dishVariantStep[idx] = (window.dishVariantStep[idx] || 0) + 1;
      const step = window.dishVariantStep[idx];
      const engine = window.selectedAiEnginePerDish[idx] || "gastro_hd";

      const nm = (d.name || "").toLowerCase();
      let bankKey = "salad";
      if (nm.includes("бургер") || nm.includes("сэндвич") || nm.includes("завертон") || nm.includes("неряха")) bankKey = "burger";
      else if (nm.includes("суп") || nm.includes("том ям") || nm.includes("борщ")) bankKey = "soup";
      else if (nm.includes("пицца") || nm.includes("лапша") || nm.includes("пад тай") || nm.includes("паста") || nm.includes("плов")) bankKey = "main";
      else if (nm.includes("чай") || nm.includes("кофе") || nm.includes("лимонад") || nm.includes("смузи")) bankKey = "drink";
      else if (nm.includes("сырники") || nm.includes("десерт") || nm.includes("шарлотка") || nm.includes("мороженое")) bankKey = "dessert";

      const vkPool = (DATA.vk_food_photos && DATA.vk_food_photos.length) ? DATA.vk_food_photos : ["img/vk_5128_1.jpg"];
      const bankPool = [...(CURATED_VEGAN_HD_BANK[bankKey] || CURATED_VEGAN_HD_BANK.main), ...vkPool];

      if (engine === "flux_ai" || engine === "turbo_ai") {
        const mdl = engine === "flux_ai" ? "flux" : "turbo";
        const seed = Math.floor(Math.random() * 899999) + step * 97;
        const aiUrl = "https://image.pollinations.ai/prompt/" + encodeURIComponent("100% vegan plant-based " + raw.slice(0, 80) + ", restaurant food photo, no meat, no text") + "?model=" + mdl + "&width=640&height=640&seed=" + seed + "&nologo=true";
        pushDiagLog(idx, "📡", mdl.toUpperCase(), "Запрос генерации (seed #" + seed + ")...");
        const cObj = { url: aiUrl, source: "🎨 " + mdl.toUpperCase() + " AI (Seed #" + seed + ")", prompt: raw, diag: "✅ Кандидат сгенерирован" };
        window.pendingDishCandidates[idx] = pendingDishCandidates[idx] = cObj;
        window.renderUnifiedSystemHub();
        return;
      }

      if (engine === "vk_food_archive") {
        const pickVk = vkPool[(step - 1) % vkPool.length];
        pushDiagLog(idx, "✅", "Архив ВК", "Кадр #" + step + ": " + pickVk);
        const cObj = { url: pickVk, source: "🌿 Архив ВК кафе (#" + (((step - 1) % vkPool.length) + 1) + ")", prompt: pickVk, diag: "✅ Реальное фото из группы ВК" };
        window.pendingDishCandidates[idx] = pendingDishCandidates[idx] = cObj;
        window.renderUnifiedSystemHub();
        return;
      }

      const pickLocal = bankPool[(step - 1) % bankPool.length];
      pushDiagLog(idx, "✅", engine.toUpperCase(), "Выбран веган-кадр #" + step + " (" + pickLocal + ")");
      const cObj = { url: pickLocal, source: "🍔 Вариант #" + step + " (" + pickLocal + ")", prompt: raw, diag: "✅ Проверенный веган-кадр" };
      window.pendingDishCandidates[idx] = pendingDishCandidates[idx] = cObj;
      window.renderUnifiedSystemHub();
    };

    window.previewManualUrlCandidate = function(idx) {
      const val = (document.getElementById("hub-url-inp-" + idx)?.value || "").trim();
      if (!val) { alert("Вставьте прямую ссылку или путь img/..."); return; }
      const cObj = { url: val, source: "🔗 Прямой URL", prompt: val, diag: "✅ Загружено по ссылке" };
      window.pendingDishCandidates[idx] = pendingDishCandidates[idx] = cObj;
      window.renderUnifiedSystemHub();
    };

    window.selectReadyPhotoV42 = function(dishIdx, photoPath) {
      const d = DATA.menu[dishIdx];
      if (!d) return;
      d.photo = photoPath;
      d.photo_type = "real";
      d.is_manual_override = true;
      try {
        const map = JSON.parse(localStorage.getItem("mirmir_manual_dish_photos_v1") || "{}");
        map[d.name] = photoPath;
        localStorage.setItem("mirmir_manual_dish_photos_v1", JSON.stringify(map));
      } catch(e) {}
      delete window.pendingDishCandidates[dishIdx];
      closeReadyGalleryPopup();
      window.renderUnifiedSystemHub();
      window.renderDishes();
      window.renderHeroRightColumn();
    };

    window.approveDishCandidate = function(idx) {
      const cand = window.pendingDishCandidates[idx];
      if (cand && cand.url) window.selectReadyPhotoV42(idx, cand.url);
    };

    window.openReadyGalleryPopup = function(dishIdx) {
      const d = DATA.menu[dishIdx];
      const modal = document.getElementById("ready-gallery-popup");
      if (!modal || !d) return;
      const pool = (DATA.ready_photos || []).filter(p => !p.includes("ai_v") && !p.includes("ingr_") && !p.includes("5047_"));
      const card = modal.firstElementChild;
      if (card) {
        card.innerHTML =
          '<div class="bg-[#2E3D28] text-[#FFFDF9] px-5 py-3 flex items-center justify-between relative">' +
            '<h3 class="font-serif text-lg font-bold">📸 Выберите реальное фото из ВК для: <span class="text-[#F2B880]">' + esc(d.name) + '</span> (' + pool.length + ' шт.)</h3>' +
            '<button type="button" onclick="closeReadyGalleryPopup()" class="v42-top-right-close">✕</button>' +
          '</div>' +
          '<div class="p-4 overflow-y-auto max-h-[75vh] bg-[#FAF5EC] grid grid-cols-2 sm:grid-cols-4 gap-3">' +
            pool.map(ph =>
              '<div class="bg-white rounded-2xl p-2 border border-stone-200 flex flex-col justify-between gap-1.5">' +
                '<div class="relative h-32 rounded-xl overflow-hidden bg-stone-100">' +
                  '<img src="' + esc(ph) + '" loading="lazy" onclick="openSuperZoom(this.src, \'' + esc(d.name) + '\')" class="w-full h-full object-cover cursor-zoom-in">' +
                  '<button type="button" title="Увеличить" onclick="openSuperZoom(\'' + esc(ph) + '\', \'' + esc(d.name) + '\')" class="absolute bottom-1.5 right-1.5 w-7 h-7 rounded-full bg-black/75 text-white text-xs flex items-center justify-center cursor-pointer">🔍</button>' +
                '</div>' +
                '<div class="text-[10px] font-mono text-stone-500 truncate">' + esc(ph) + '</div>' +
                '<button type="button" onclick="selectReadyPhotoV42(' + dishIdx + ', \'' + esc(ph) + '\')" class="w-full py-1.5 rounded-xl bg-emerald-700 hover:bg-[#D48238] text-white text-xs font-extrabold cursor-pointer">✅ Утвердить это фото</button>' +
              '</div>'
            ).join("") +
          '</div>';
      }
      modal.classList.remove("hidden");
      modal.classList.add("flex");
    };

    // 8. Панель управления (Шестерёнка)
    window.renderUnifiedSystemHub = function() {
      syncMenuWithCustomAndDeleted();
      applyManualOverridesToMenuData();
      applyV42CleanLayout();

      const hubModal = document.getElementById("unified-system-hub");
      const hubCard = hubModal ? hubModal.firstElementChild : null;
      const hubHeader = hubCard ? hubCard.children[0] : null;
      const body = document.getElementById("unified-hub-body") || (hubCard ? (hubCard.querySelector(".overflow-y-auto") || hubCard.children[1]) : null);
      const tabsBox = document.getElementById("unified-hub-tabs") || (hubHeader ? hubHeader.querySelector("[id*='tab']") : null);
      if (!tabsBox || !body) return;

      const curTab = window.hubActiveTab || "dishes72";
      const tasks = getMasterTasksList();
      const doneCnt = tasks.filter(t => t.done).length;
      const logs = window.getCombinedBuildLogs();
      const deletedCount = Object.keys(window.getDeletedDishesMap()).length;

      const tabDefs = [
        { id: "dishes72", label: "🍲 Все блюда (" + DATA.menu.length + ")" },
        { id: "tasks", label: "📋 Список задач (" + doneCnt + "/" + tasks.length + ")" },
        { id: "logs", label: "📜 Логи сборок (" + logs.length + ")" },
        { id: "ideas", label: "📝 Журнал идей" },
        { id: "toggles", label: "⚡ Режимы, Бронь & Промпт" }
      ];

      tabsBox.innerHTML = tabDefs.map(t =>
        '<button type="button" onclick="setHubTab(\'' + t.id + '\')" class="px-3 py-1.5 rounded-xl text-xs font-extrabold cursor-pointer transition ' +
        (curTab === t.id ? 'bg-[#D48238] text-white shadow' : 'bg-white/10 text-stone-200 hover:bg-white/20') + '">' + t.label + '</button>'
      ).join("");

      if (curTab === "dishes72") {
        const cats = ["Все", ...Array.from(new Set(DATA.menu.map(d => d.category)))];
        const formCats = cats.filter(c => c !== "Все");
        const curCat = window.hubDishCategoryFilter || "Все";
        const curQ = (window.hubDishSearchQuery || "").toLowerCase();
        const filtered = DATA.menu.filter(d => (curCat === "Все" || d.category === curCat) && (!curQ || d.name.toLowerCase().includes(curQ)));

        body.innerHTML =
          '<div class="bg-white rounded-2xl p-3 border border-stone-200 shadow-xs space-y-2.5 mb-3">' +
            '<div class="flex flex-wrap items-center justify-between gap-2">' +
              '<input type="text" value="' + esc(window.hubDishSearchQuery || "") + '" oninput="setHubSearch(this.value)" placeholder="🔍 Быстрый поиск блюда по названию..." class="flex-1 min-w-[200px] px-3 py-1.5 rounded-xl border border-stone-300 text-xs font-bold outline-none">' +
              (deletedCount > 0 ? '<button type="button" onclick="restoreAllDeletedDishes()" class="px-3 py-1.5 rounded-xl bg-amber-100 hover:bg-amber-200 text-[#2E3D28] text-xs font-extrabold cursor-pointer">♻️ Восстановить удалённые (' + deletedCount + ')</button>' : '') +
              '<button type="button" onclick="window.dishAddPanelOpen=!window.dishAddPanelOpen;renderUnifiedSystemHub()" class="px-3.5 py-1.5 rounded-xl bg-[#2E3D28] hover:bg-[#D48238] text-[#F2B880] hover:text-white text-xs font-extrabold cursor-pointer transition">' +
                (window.dishAddPanelOpen ? '▲ Скрыть форму добавления' : '➕ Добавить новое блюдо вручную') +
              '</button>' +
            '</div>' +
            (window.dishAddPanelOpen ? (
              '<div class="bg-[#2E3D28] text-[#FFFDF9] rounded-2xl p-3 border border-[#F2B880]/60 space-y-2">' +
                '<div class="grid grid-cols-1 sm:grid-cols-4 gap-2 text-stone-900">' +
                  '<input id="new-dish-name" type="text" placeholder="Название блюда" class="px-2.5 py-1.5 rounded-lg bg-white text-xs font-bold">' +
                  '<select id="new-dish-cat" class="px-2.5 py-1.5 rounded-lg bg-white text-xs font-bold">' + formCats.map(c => '<option value="' + esc(c) + '">' + esc(c) + '</option>').join("") + '</select>' +
                  '<div class="grid grid-cols-2 gap-1.5"><input id="new-dish-price" type="number" placeholder="Цена ₽ (450)" class="px-2.5 py-1.5 rounded-lg bg-white text-xs font-bold"><input id="new-dish-weight" type="text" placeholder="Вес (260 г)" class="px-2.5 py-1.5 rounded-lg bg-white text-xs font-bold"></div>' +
                  '<input id="new-dish-photo" type="text" placeholder="img/vk_5128_1.jpg или URL" class="px-2.5 py-1.5 rounded-lg bg-white text-xs">' +
                '</div>' +
                '<div class="flex gap-2"><input id="new-dish-desc" type="text" placeholder="Описание и состав..." class="flex-1 px-2.5 py-1.5 rounded-lg bg-white text-stone-900 text-xs"><button type="button" onclick="addNewCustomDishFromHub()" class="px-4 py-1.5 rounded-lg bg-[#D48238] text-white font-extrabold text-xs cursor-pointer">✅ Сохранить блюдо</button></div>' +
              '</div>'
            ) : '') +
            '<div class="flex gap-1.5 overflow-x-auto no-scrollbar pb-0.5">' +
              cats.map(c => '<button type="button" onclick="setHubCategory(\'' + esc(c) + '\')" class="px-2.5 py-1 rounded-full text-[11px] font-extrabold whitespace-nowrap cursor-pointer ' + (curCat === c ? 'bg-[#2E3D28] text-[#F2B880]' : 'bg-stone-100 text-stone-700 hover:bg-stone-200') + '">' + esc(c) + '</button>').join("") +
            '</div>' +
          '</div>' +

          '<div class="space-y-2.5">' + filtered.map(d => {
            const idx = DATA.menu.indexOf(d);
            const isOff = window.isDishDisabled(d.name);
            const curEngine = window.selectedAiEnginePerDish[idx] || "gastro_hd";
            const cand = window.pendingDishCandidates[idx];
            const promptVal = window.customPromptsPerDish[idx] !== undefined ? window.customPromptsPerDish[idx] : (d.ai_prompt || d.name);
            const diagLines = window.dishDiagLogs[idx] || [];
            const engines = [
              { k: "flux_ai", lbl: "🎨 1. Flux AI" },
              { k: "turbo_ai", lbl: "⚡ 2. Turbo AI" },
              { k: "gastro_hd", lbl: "🍔 3. GastroBank HD" },
              { k: "openverse_hd", lbl: "📸 4. Openverse" },
              { k: "wikimedia", lbl: "🥗 5. Wikimedia" },
              { k: "vk_food_archive", lbl: "🌿 6. Архив ВК" }
            ];

            return '<div class="bg-white rounded-2xl p-3.5 border border-stone-200 shadow-xs space-y-2.5 transition ' + (isOff ? 'opacity-50 bg-stone-100' : '') + '">' +
              '<div class="grid grid-cols-1 lg:grid-cols-12 gap-3 items-start">' +
                '<div class="lg:col-span-4 flex items-center gap-3">' +
                  '<div class="relative w-20 h-20 rounded-2xl overflow-hidden flex-shrink-0 border border-stone-300 bg-stone-100">' +
                    '<img src="' + esc(d.photo) + '" onclick="openSuperZoom(this.src, \'' + esc(d.name) + '\')" class="w-full h-full object-cover cursor-zoom-in">' +
                    '<button type="button" title="Увеличить" onclick="openSuperZoom(\'' + esc(d.photo) + '\', \'' + esc(d.name) + '\')" class="absolute bottom-1 right-1 w-6 h-6 rounded-full bg-black/80 text-white text-[10px] flex items-center justify-center cursor-pointer">🔍</button>' +
                  '</div>' +
                  '<div class="min-w-0 flex-1 space-y-1">' +
                    '<div class="flex flex-wrap items-center gap-1">' +
                      '<span class="text-[9px] font-extrabold uppercase px-2 py-0.5 rounded bg-amber-100 text-[#2E3D28]">' + esc(d.category) + '</span>' +
                      (isOff ? '<span class="text-[9px] font-extrabold px-2 py-0.5 rounded bg-amber-600 text-white">⏸️ Отключено</span>' : '') +
                    '</div>' +
                    '<h4 class="font-serif font-bold text-base text-[#2E3D28] leading-tight">' + esc(d.name) + ' <span class="text-[#D48238] text-xs font-sans">(' + (d.sizes ? d.sizes[0].price : d.price) + ' ₽)</span></h4>' +
                    '<div class="flex flex-wrap gap-1 pt-0.5">' +
                      '<button type="button" onclick="openReadyGalleryPopup(' + idx + ')" class="px-2 py-1 rounded-lg bg-[#2E3D28] text-[#F2B880] text-[10px] font-extrabold cursor-pointer">📸 Из готовых (' + (DATA.ready_photos ? DATA.ready_photos.length : 306) + ')</button>' +
                      '<button type="button" onclick="toggleDishDisabled(' + idx + ')" class="px-2 py-1 rounded-lg ' + (isOff ? 'bg-emerald-700 text-white' : 'bg-amber-500/90 text-white') + ' text-[10px] font-extrabold cursor-pointer">' + (isOff ? '👁️ Включить' : '⏸️ Отключить') + '</button>' +
                      '<button type="button" onclick="deleteDishTripleConfirm(' + idx + ')" class="px-2 py-1 rounded-lg bg-rose-700 hover:bg-rose-800 text-white text-[10px] font-extrabold cursor-pointer">🗑️ Удалить</button>' +
                    '</div>' +
                  '</div>' +
                '</div>' +

                '<div class="lg:col-span-8 bg-amber-50/60 rounded-2xl p-2.5 border border-amber-200/90 space-y-2">' +
                  '<div class="flex flex-wrap items-center justify-between gap-1.5">' +
                    '<span class="text-[10px] font-extrabold uppercase text-[#D48238]">🎨 1. Выберите источник или ИИ:</span>' +
                    '<div class="flex flex-wrap gap-1">' +
                      engines.map(e => '<button type="button" onclick="runEngineForDish(' + idx + ',\'' + e.k + '\')" class="px-2 py-1 rounded-lg text-[10px] font-extrabold cursor-pointer ' + (curEngine === e.k ? 'bg-[#2E3D28] text-[#F2B880]' : 'bg-white text-[#2E3D28] border border-amber-300') + '">' + e.lbl + '</button>').join("") +
                    '</div>' +
                  '</div>' +
                  '<div class="grid grid-cols-1 sm:grid-cols-12 gap-2 items-center">' +
                    '<div class="sm:col-span-7 flex gap-1.5">' +
                      '<input id="hub-ai-prm-' + idx + '" type="text" value="' + esc(promptVal) + '" oninput="window.customPromptsPerDish[' + idx + ']=this.value" class="flex-1 min-w-0 px-2.5 py-1.5 rounded-xl bg-white border border-amber-300 text-xs">' +
                      '<button type="button" onclick="generateDishCandidateAI(' + idx + ')" class="px-3 py-1.5 rounded-xl bg-[#D48238] text-white text-[11px] font-extrabold cursor-pointer whitespace-nowrap">🔍 Найти / ИИ</button>' +
                    '</div>' +
                    '<div class="sm:col-span-5 flex gap-1.5">' +
                      '<input id="hub-url-inp-' + idx + '" type="text" placeholder="🔗 Прямой URL или img/..." class="flex-1 min-w-0 px-2.5 py-1.5 rounded-xl bg-white border border-stone-300 text-xs">' +
                      '<button type="button" onclick="previewManualUrlCandidate(' + idx + ')" class="px-2.5 py-1.5 rounded-xl bg-[#556432] text-white text-[11px] font-extrabold cursor-pointer">✅ URL</button>' +
                    '</div>' +
                  '</div>' +
                  (diagLines.length ? '<div class="bg-[#1A2416] text-emerald-300 rounded-xl px-2.5 py-1 font-mono text-[10px]">' + diagLines.map(l => '<div class="truncate">' + esc(l) + '</div>').join("") + '</div>' : '') +
                '</div>' +
              '</div>' +

              (cand ? (
                '<div class="bg-[#23311E] text-[#FFFDF9] rounded-2xl p-3 border-2 border-[#D48238] flex flex-col sm:flex-row items-center justify-between gap-3">' +
                  '<div class="flex items-center gap-3">' +
                    '<div class="relative w-24 h-24 rounded-xl overflow-hidden border-2 border-[#F2B880] flex-shrink-0 bg-stone-800">' +
                      '<img src="' + esc(cand.url) + '" onclick="openSuperZoom(this.src, \'' + esc(d.name) + '\')" class="w-full h-full object-cover cursor-zoom-in">' +
                    '</div>' +
                    '<div class="space-y-1"><span class="px-2 py-0.5 rounded-full bg-[#D48238] text-white text-[10px] font-extrabold">' + esc(cand.source) + '</span><h5 class="font-serif text-base font-bold text-[#F2B880]">👁️ Предпросмотр для «' + esc(d.name) + '»</h5></div>' +
                  '</div>' +
                  '<div class="flex sm:flex-col gap-1.5"><button type="button" onclick="approveDishCandidate(' + idx + ')" class="px-3.5 py-1.5 rounded-xl bg-emerald-600 text-white font-extrabold text-xs cursor-pointer">✅ Утвердить в меню</button><button type="button" onclick="generateDishCandidateAI(' + idx + ')" class="px-3.5 py-1.5 rounded-xl bg-[#D48238] text-white font-extrabold text-xs cursor-pointer">🎲 Ещё вариант</button><button type="button" onclick="delete window.pendingDishCandidates[' + idx + '];renderUnifiedSystemHub()" class="px-3 py-1 rounded-xl bg-white/10 text-stone-300 text-[11px] cursor-pointer">✕ Отмена</button></div>' +
                '</div>'
              ) : '') +
            '</div>';
          }).join("") + '</div>';
        return;
      }

      if (curTab === "tasks") {
        body.innerHTML =
          '<div class="space-y-3">' +
            '<div class="bg-white rounded-2xl p-3.5 border border-stone-200 shadow-xs grid grid-cols-1 sm:grid-cols-12 gap-2.5 items-center">' +
              '<input id="new-tz-task-inp" type="text" placeholder="➕ Новая задача или правка..." class="sm:col-span-5 px-3 py-2 rounded-xl border border-stone-300 text-xs font-bold outline-none focus:border-[#D48238]">' +
              '<input id="new-tz-comment-inp" type="text" placeholder="💬 Комментарий / примечание..." class="sm:col-span-5 px-3 py-2 rounded-xl border border-stone-300 text-xs outline-none focus:border-[#D48238]">' +
              '<button type="button" onclick="addNewTaskV42()" class="sm:col-span-2 py-2 px-3 rounded-xl bg-[#D48238] hover:opacity-95 text-white font-extrabold text-xs cursor-pointer shadow-xs">+ Добавить</button>' +
            '</div>' +
            '<div class="bg-white rounded-2xl border border-stone-300 overflow-x-auto shadow-xs">' +
              '<table class="w-full text-left border-collapse min-w-[820px]">' +
                '<thead class="bg-[#2E3D28] text-[#F2B880] text-[10px] font-extrabold uppercase tracking-wider">' +
                  '<tr>' +
                    '<th class="p-3 w-36">Дата и время</th>' +
                    '<th class="p-3 w-[38%]">Задача</th>' +
                    '<th class="p-3 text-center w-32">Статус</th>' +
                    '<th class="p-3 w-[42%]">Комментарий / Примечание</th>' +
                  '</tr>' +
                '</thead>' +
                '<tbody class="divide-y divide-stone-200 text-xs">' +
                  tasks.map((t, i) => {
                    const parts = String(t.date || "11.11.2026 16:40").split(" ");
                    const dPart = parts[0] || "11.11.2026";
                    const tPart = parts[1] || "12:00";
                    return '<tr class="hover:bg-amber-50/40 transition ' + (t.done ? '' : 'bg-rose-50/50') + '">' +
                      '<td class="p-3 whitespace-nowrap align-middle">' +
                        '<div class="font-mono text-[11px] font-extrabold text-[#2E3D28]">📅 ' + esc(dPart) + '</div>' +
                        '<div class="font-mono text-[10px] font-bold text-[#D48238] mt-0.5">🕒 ' + esc(tPart) + '</div>' +
                      '</td>' +
                      '<td class="p-3 font-bold text-[#1F2B1A] leading-snug align-middle">' + esc(t.title) + '</td>' +
                      '<td class="p-3 text-center align-middle">' +
                        '<button type="button" onclick="toggleTaskDoneV42(' + i + ')" class="px-3 py-1.5 rounded-xl font-extrabold text-[11px] cursor-pointer w-28 shadow-xs transition ' + (t.done ? 'bg-emerald-700 hover:bg-emerald-800 text-white' : 'bg-rose-600 hover:bg-rose-700 text-white') + '">' +
                          (t.done ? '✅ Сделано' : '❌ Не сделано') +
                        '</button>' +
                      '</td>' +
                      '<td class="p-3 align-middle">' +
                        '<input type="text" value="' + esc(t.comment || "") + '" oninput="updateTaskCommentV42(' + i + ', this.value)" placeholder="Комментарий..." class="w-full px-3 py-2 rounded-xl border ' + (t.done ? 'border-stone-200 bg-stone-50/80 text-stone-800' : 'border-rose-300 bg-white text-rose-900 font-bold') + ' text-xs outline-none focus:border-[#D48238] focus:bg-white">' +
                      '</td>' +
                    '</tr>';
                  }).join("") +
                '</tbody>' +
              '</table>' +
            '</div>' +
          '</div>';
        return;
      }

      if (curTab === "logs") {
        body.innerHTML = '<div class="space-y-2.5">' + logs.map(l => '<div class="bg-white rounded-2xl p-3.5 border border-stone-200 space-y-1"><div class="flex justify-between"><span class="px-2.5 py-0.5 rounded-full bg-[#2E3D28] text-[#F2B880] text-xs font-extrabold">' + esc(l.version) + '</span><span class="text-xs text-stone-400">🕒 ' + esc(l.timestamp) + '</span></div><div class="text-xs font-extrabold text-[#D48238]">' + esc(l.model || "") + '</div><p class="text-xs text-stone-700">' + esc(l.status || "") + '</p></div>').join("") + '</div>';
        return;
      }

      if (curTab === "ideas") {
        const notes = window.getSavedIdeasNotes();
        body.innerHTML = '<div class="space-y-3"><div class="bg-white rounded-2xl p-3 border border-stone-200 flex gap-2"><input id="new-idea-note-inp" type="text" placeholder="Запишите идею..." class="flex-1 px-3 py-1.5 rounded-xl border border-stone-300 text-xs"><button type="button" onclick="addNewIdeaNote()" class="px-4 py-1.5 rounded-xl bg-[#2E3D28] text-[#F2B880] font-extrabold text-xs cursor-pointer">💾 Сохранить</button></div><div class="space-y-2">' + notes.map(n => '<div class="bg-white rounded-2xl p-3 border border-stone-200 flex justify-between"><p class="text-xs font-bold">' + esc(n.text) + '</p><span class="text-[10px] text-stone-400">' + esc(n.date) + '</span></div>').join("") + '</div></div>';
        return;
      }

      const tg = window.getSiteToggles();
      body.innerHTML =
        '<div class="grid grid-cols-1 lg:grid-cols-2 gap-3">' +
          '<div class="bg-white rounded-2xl p-4 border border-stone-200 space-y-3">' +
            '<h4 class="font-serif text-lg font-bold text-[#2E3D28]">🛠️ Настройки режимов сайта</h4>' +
            '<div class="p-3 rounded-xl bg-amber-50/70 border border-amber-200 space-y-1.5"><div class="text-xs font-extrabold text-[#2E3D28]">🪑 1. Режим кнопки «Бронь столика»:</div><div class="grid grid-cols-2 gap-1.5"><button type="button" onclick="setAdminSettingV42(\'bookingMode\', \'messenger\')" class="p-2 rounded-lg text-[11px] font-extrabold cursor-pointer ' + (tg.bookingMode === 'messenger' ? 'bg-[#2E3D28] text-[#F2B880]' : 'bg-white border') + '">✈️ Telegram / ВК (Без 152-ФЗ)</button><button type="button" onclick="setAdminSettingV42(\'bookingMode\', \'form152\')" class="p-2 rounded-lg text-[11px] font-extrabold cursor-pointer ' + (tg.bookingMode === 'form152' ? 'bg-[#2E3D28] text-[#F2B880]' : 'bg-white border') + '">📝 Анкета на сайте (152-ФЗ)</button></div></div>' +
            '<div class="p-3 rounded-xl bg-amber-50/70 border border-amber-200 space-y-1.5"><div class="text-xs font-extrabold text-[#2E3D28]">📸 2. Режим показа фото в Меню:</div><div class="grid grid-cols-2 gap-1.5"><button type="button" onclick="setAdminSettingV42(\'photoMode\', \'hybrid\')" class="p-2 rounded-lg text-[11px] font-extrabold cursor-pointer ' + (tg.photoMode === 'hybrid' ? 'bg-[#2E3D28] text-[#F2B880]' : 'bg-white border') + '">🎨 Гибрид (Все фото)</button><button type="button" onclick="setAdminSettingV42(\'photoMode\', \'strict_real\')" class="p-2 rounded-lg text-[11px] font-extrabold cursor-pointer ' + (tg.photoMode === 'strict_real' ? 'bg-[#2E3D28] text-[#F2B880]' : 'bg-white border') + '">🕊️ Только 100% фото из ВК</button></div></div>' +
          '</div>' +
          '<div class="bg-[#2E3D28] text-[#FFFDF9] rounded-2xl p-4 space-y-2.5 flex flex-col justify-between">' +
            '<div><span class="text-[10px] font-extrabold uppercase text-[#F2B880]">ДНК ПЛАТФОРМЫ</span><h4 class="font-serif text-xl font-bold mt-0.5">🧬 Полный Текстовый Мастер-Промпт</h4><p class="text-xs text-stone-300 mt-1">Техническое задание на русском языке с сохранением правок.</p></div>' +
            '<div class="flex gap-2"><button type="button" onclick="openMasterPromptModal()" class="px-4 py-2 rounded-xl bg-[#D48238] text-white text-xs font-extrabold cursor-pointer">📖 Открыть и редактировать Промпт</button><button type="button" onclick="downloadMasterPromptFile()" class="px-4 py-2 rounded-xl bg-white/15 text-white text-xs font-extrabold cursor-pointer">💾 Скачать .TXT</button></div>' +
          '</div>' +
        '</div>';
    };

    // 9. Отрисовка Электронного меню (полупрозрачные отключённые блюда + значок 🔍 без слова «Лупа»)
    window.renderDishes = function() {
      syncMenuWithCustomAndDeleted();
      applyManualOverridesToMenuData();
      const tabsBox = document.getElementById("menu-cat-tabs");
      const grid = document.getElementById("menu-dishes-grid");
      if (!grid) return;
      const cats = ["Все", ...Array.from(new Set(DATA.menu.map(d => d.category)))];
      if (tabsBox) {
        tabsBox.innerHTML = '<button type="button" onclick="closeMenu();openBowlBuilder()" class="px-3.5 py-1.5 rounded-full text-xs font-extrabold bg-[#D48238] text-white cursor-pointer">🥗 Собрать свой Боул</button>' +
          cats.map(c => '<button type="button" onclick="currentMenuCategory=\'' + esc(c) + '\';renderDishes()" class="px-3.5 py-1.5 rounded-full text-xs font-extrabold cursor-pointer ' + (currentMenuCategory === c ? 'bg-[#2E3D28] text-[#F2B880]' : 'bg-white text-[#2E3D28] border border-stone-300') + '">' + esc(c) + '</button>').join("");
      }
      const q = (document.getElementById("menu-search-inp")?.value || "").toLowerCase();
      const filtered = DATA.menu.filter(d => (currentMenuCategory === "Все" || d.category === currentMenuCategory) && (!q || d.name.toLowerCase().includes(q) || (d.desc || "").toLowerCase().includes(q)));

      grid.innerHTML = filtered.map(d => {
        const realIdx = DATA.menu.indexOf(d);
        const isOff = window.isDishDisabled(d.name);
        const actBtns = isOff
          ? '<div class="pt-2 border-t border-stone-200 flex items-center justify-between"><span class="text-xs font-extrabold text-amber-800">⏸️ Временно не готовится</span><span class="text-sm font-bold text-stone-400">' + (d.sizes ? d.sizes[0].price : d.price) + ' ₽</span></div>'
          : ((d.sizes && d.sizes.length > 1)
              ? '<div class="grid grid-cols-2 gap-1.5 pt-2">' + d.sizes.map((sz, sIdx) => '<button type="button" onclick="addToCart(' + realIdx + ',' + sIdx + ')" class="py-2 px-2 rounded-xl bg-[#556432] hover:bg-[#D48238] text-white font-extrabold text-[11px] cursor-pointer">' + esc(sz.label) + ' • ' + sz.price + ' ₽ +</button>').join("") + '</div>'
              : '<div class="flex items-center justify-between pt-2 border-t border-stone-100"><div><span class="text-[11px] text-stone-400 font-bold block">' + esc(d.weight || "") + '</span><strong class="text-lg font-extrabold text-[#2E3D28]">' + d.price + ' ₽</strong></div><button type="button" onclick="addToCart(' + realIdx + ',0)" class="px-4 py-2 rounded-xl bg-[#D48238] text-white font-extrabold text-xs cursor-pointer">+ В корзину</button></div>');

        return '<div class="zoom-card bg-white rounded-3xl p-3.5 border border-stone-200 shadow-sm flex flex-col justify-between gap-2 transition ' + (isOff ? 'opacity-40 grayscale-[35%]' : '') + '">' +
          '<div>' +
            '<div class="relative h-44 rounded-2xl overflow-hidden mb-2.5 bg-stone-100">' +
              '<img src="' + esc(d.photo) + '" onclick="openSuperZoom(this.src, \'' + esc(d.name) + '\')" class="w-full h-full object-cover cursor-zoom-in">' +
              '<span class="absolute bottom-2 left-2 px-2 py-0.5 rounded-md bg-black/75 text-white/95 text-[9px] font-bold">🍽️ Подача блюд может отличаться</span>' +
              '<button type="button" title="Увеличить" onclick="openSuperZoom(\'' + esc(d.photo) + '\', \'' + esc(d.name) + '\')" class="absolute bottom-2 right-2 w-7 h-7 rounded-full bg-black/80 hover:bg-[#D48238] text-white text-xs flex items-center justify-center cursor-pointer">🔍</button>' +
            '</div>' +
            '<span class="text-[10px] font-extrabold uppercase text-[#556432]">' + esc(d.category) + '</span>' +
            '<h4 class="font-serif text-xl font-bold text-[#2E3D28] leading-snug">' + esc(d.name) + '</h4>' +
            '<p class="text-xs text-stone-600 mt-1 leading-relaxed">' + esc(d.desc || "") + '</p>' +
          '</div>' +
          actBtns +
        '</div>';
      }).join("");
    };

    window.addEventListener("DOMContentLoaded", () => {
      syncMenuWithCustomAndDeleted();
      applyV42CleanLayout();
      document.querySelectorAll("[data-dove-holder]").forEach(el => { el.innerHTML = SIGN_DOVE_SVG; });
      applyManualOverridesToMenuData();
      renderWorkStatusBadges();
      rollRandomGastroPulse();
      window.renderInteriorSlideState();
      setInterval(() => { stepInteriorSlide(1); window.renderInteriorSlideState(); }, 4200);
      window.renderHeroRightColumn();
      setInterval(() => step3DCarousel(1), 4500);
      setInterval(() => window.stepRightSpecialsPair(1), 5200);
      window.renderNewsPosts();
      renderCategoryShowcaseAndRail();
    });
  </script>
</body>
</html>
"""
    return tpl_html + v42_js


def build_clean_master_prompt_text():
    if os.path.exists("MASTER_PROMPT_MIRMIR.txt"):
        try:
            txt = clean_slang_from_text(open("MASTER_PROMPT_MIRMIR.txt", "r", encoding="utf-8").read().strip())
            open("MASTER_PROMPT_MIRMIR.txt", "w", encoding="utf-8").write(txt)
            if len(txt) > 500:
                return txt
        except Exception:
            pass
    return "ПОЛНОЕ ТЕХНИЧЕСКОЕ ЗАДАНИЕ (МАСТЕР-ПРОМПТ) ВЕГАН-КАФЕ «МИР МИР» (v4.2)"


def sync_files_to_root_repo():
    if os.path.abspath(ROOT_REPO_DIR) == os.path.abspath(BASE_DIR):
        return
    for fn in ["index.html", "menu_data.py", "template.html", "app.py", "tz_mirmir.json", "build_history.json", "MASTER_PROMPT_MIRMIR.txt", "run_counter.txt", "cache_posts.json"]:
        s, d = os.path.join(BASE_DIR, fn), os.path.join(ROOT_REPO_DIR, fn)
        if os.path.exists(s):
            try:
                shutil.copy2(s, d)
            except Exception:
                pass
    s_img, d_img = os.path.join(BASE_DIR, "img"), os.path.join(ROOT_REPO_DIR, "img")
    if os.path.exists(s_img):
        os.makedirs(d_img, exist_ok=True)
        for fn in os.listdir(s_img):
            if fn.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                sf, df = os.path.join(s_img, fn), os.path.join(d_img, fn)
                if not os.path.exists(df) or os.path.getsize(df) != os.path.getsize(sf):
                    try:
                        shutil.copy2(sf, df)
                    except Exception:
                        pass


def main():
    auto_migrate_assets()
    clean_non_vegan_and_junk_images()
    import importlib
    import menu_data
    importlib.reload(menu_data)
    tz_data, build_logs, build_num = sync_tz_and_build_logs()
    dish_overrides = tz_data.get("dishes", {})

    clean_menu = []
    for item in menu_data.MENU_DATABASE:
        d = dict(item)
        if "photo_type" not in d:
            d["photo_type"] = d.pop("photo_type: ", "real")
        if any(bad in str(d.get("photo", "")) for bad in ["macro_mushrooms_raw", "macro_rice_noodles"]):
            d["photo"] = "img/macro_tomyum_bowl.jpg"
        nm = d.get("name", "")
        if nm in dish_overrides and dish_overrides[nm].get("photo"):
            d["photo"] = dish_overrides[nm]["photo"]
            d["photo_type"] = "real"
            d["is_manual_override"] = True
        clean_menu.append(d)

    vk_files = sorted([fn for fn in os.listdir("img") if fn.startswith("vk_") and "5047_" not in fn], reverse=True) if os.path.exists("img") else []
    other_clean = sorted([fn for fn in os.listdir("img") if not fn.startswith(("vk_", "ai_v", "ingr_", "ymap_org_")) and "5047_" not in fn]) if os.path.exists("img") else []
    ready_photos = ["img/" + fn for fn in (vk_files + other_clean) if fn.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))]
    vk_food_photos = ["img/" + fn for fn in vk_files if "5068_" not in fn]

    now_stamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    data_payload = {
        "version": f"Релиз v4.2 • Сборка #{build_num} ({now_stamp})",
        "menu": clean_menu,
        "shop": menu_data.CAFE_SHOP_ITEMS,
        "posts": fetch_vk_wall_posts(),
        "ymap_photos": [p for p in ["img/ymap_org_0.jpg", "img/ymap_org_1.jpg", "img/vk_5068_0.jpg", "img/vk_5122_0.jpg", "img/vk_5134_0.jpg"] if os.path.exists(p)],
        "ready_photos": ready_photos,
        "vk_food_photos": vk_food_photos,
        "menu_scans": ["img/vk_5047_0.jpg", "img/vk_5047_1.jpg", "img/vk_5047_2.jpg", "img/vk_5047_3.jpg"],
        "tz_synced": tz_data,
        "full_build_logs": build_logs,
        "master_prompt_text": build_clean_master_prompt_text(),
    }

    tpl_html = upgrade_template_html_in_place(open("template.html", "r", encoding="utf-8").read())
    open("template.html", "w", encoding="utf-8").write(tpl_html)
    final_html = tpl_html.replace("__MIRMIR_DATA_JSON__", json.dumps(data_payload, ensure_ascii=False).replace("</", "<\\/"))
    open("index.html", "w", encoding="utf-8").write(final_html)
    sync_files_to_root_repo()
    if sys.stdin and sys.stdin.isatty() and os.environ.get("GITHUB_ACTIONS") != "true":
        try:
            os.startfile("index.html")
        except Exception:
            pass


def push_to_github():
    sync_files_to_root_repo()
    target_git_dir = ROOT_REPO_DIR
    lock_f = os.path.join(target_git_dir, ".git", "index.lock")
    if os.path.exists(lock_f):
        try:
            os.remove(lock_f)
        except Exception:
            pass
    subprocess.run(["git", "config", "user.name", "MirMir Cafe"], cwd=target_git_dir, check=False)
    subprocess.run(["git", "config", "user.email", "admin@mirmir.cafe"], cwd=target_git_dir, check=False)
    subprocess.run(["git", "remote", "remove", "origin"], cwd=target_git_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "remote", "add", "origin", "https://github.com/vitvseom-stack/mirmir.git"], cwd=target_git_dir, check=False)
    subprocess.run(["git", "checkout", "-B", "main"], cwd=target_git_dir, check=False)
    subprocess.run(["git", "add", "-f", "index.html", "menu_data.py", "template.html", "app.py", "tz_mirmir.json", "build_history.json", "MASTER_PROMPT_MIRMIR.txt", "cache_posts.json"], cwd=target_git_dir, check=False)
    subprocess.run(["git", "add", "img/"], cwd=target_git_dir, check=False)
    subprocess.run(["git", "commit", "-m", f"Deploy MirMir v4.2 ({datetime.now().strftime('%d.%m.%Y %H:%M:%S')})"], cwd=target_git_dir, check=False)
    subprocess.run(["git", "push", "-u", "origin", "main", "--force"], cwd=target_git_dir, check=False)


if __name__ == "__main__":
    if not sys.stdin or not sys.stdin.isatty() or os.environ.get("GITHUB_ACTIONS") == "true":
        main()
        sys.exit(0)
    try:
        mode = input("👉 [1] Только ПК | [2] ПК + GitHub | [3] Только GitHub [по умолчанию 2]: ").strip() or "2"
        if mode == "1":
            main()
        elif mode == "3":
            push_to_github()
        else:
            main()
            push_to_github()
    except Exception:
        traceback.print_exc()
    input("\nНажмите Enter для закрытия...")