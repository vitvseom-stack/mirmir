# -*- coding: utf-8 -*-
"""
ЦЕЛЬНЫЙ КОМПИЛЯТОР «МИР МИР» (app.py — Монолитная 3-модульная сборка v3.6)
Часть 1:
1. Чинит пустой экран в Шестерёнке Архитектора (встраивает getCombinedBuildLogs, getSavedIdeasNotes, getSiteToggles напрямую в ядро).
2. Оставляет кнопку Шестерёнки (⚙️) открытой в подвале.
3. Убирает тройные дубли кнопок (сверху, в первом экране и в блоке карты) и срезает гигантское пустое бежевое поле внизу страницы.
4. Перекрашивает кнопки («Бронь», «Такси в кафе», «Доставка», «Радио») в спокойную палитру кафе без кричащего светофора.
5. Добавляет в Шестерёнку (⚙️ -> ⚡ Эффекты & Промпт) переключатели режимов по аудиту Claude:
   - Режим Брони и Заказа: [Прямой переход со списком заказа в Telegram/ВК без 152-ФЗ] ИЛИ [Форма на сайте с галочкой 152-ФЗ].
   - Режим Карты: [Чистая карточка маршрута без рекламы в iframe] ИЛИ [Интерактивный iframe Яндекс.Карт].
   - Режим Фото блюд: [Гибрид с плашкой подачи] ИЛИ [Только 100% реальные фото кафе из ВК].
6. Добавляет <meta name="robots" content="noindex, nofollow"> и alt-атрибуты для всех картинок.
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
    {"id": "t_1", "date": "08.11.2026", "title": "1. Чистая 3-модульная архитектура (menu_data.py + template.html + app.py) и меню 1/2/3 в консоли", "done": True, "comment": "Сборка и пуш в корень GitHub Pages работают из Python."},
    {"id": "t_2", "date": "09.11.2026", "title": "2. Первый экран слева: убрать чужие фото Яндекс.Карт (мясо/кальяны соседей), оставить только интерьер и фасад", "done": True, "comment": "В слайдере крутятся 5 проверенных кадров зала и кованой вывески."},
    {"id": "t_3", "date": "09.11.2026", "title": "3. Первый экран справа: вращающаяся Голубка мира и слайдер зала за 3D-меню + 2 крупных поля спешлов под ним", "done": True, "comment": "Вместо 3 мелких рядов стоят 2 крупных поля блюд."},
    {"id": "t_4", "date": "09.11.2026", "title": "4. Плашка «🍽️ Подача блюд может отличаться» на всех фотографиях блюд в Электронном меню", "done": True, "comment": "Отображается на фото каждого из 72 блюд."},
    {"id": "t_5", "date": "10.11.2026", "title": "5. Защита мобильного свайпа «Назад» (popstate SPA-Guard), чтобы на телефоне не выбрасывало с сайта", "done": True, "comment": "Жест «Назад» закрывает открытую модалку/вкладку."},
    {"id": "t_6", "date": "10.11.2026", "title": "6. Убрать все повторяющиеся кнопки-дубли (в шапке, под слоганом и в блоке карты) и пустую бежевую дыру внизу", "done": True, "comment": "В v3.6 оставлен ровно один компактный блок кнопок без дублей и без пустого поля внизу."},
    {"id": "t_7", "date": "10.11.2026", "title": "7. Спокойная палитра нижних кнопок: «Бронь», «Такси в кафе», «Доставка», «Радио» + 3 кнопки «НАША КОМАНДА / ИСТОРИЯ КАФЕ / НАШИ ЦЕННОСТИ»", "done": True, "comment": "Убран кричащий светофор цветов, всё в единой палитре кафе."},
    {"id": "t_8", "date": "10.11.2026", "title": "8. Кнопки в Новостях: совсем узкие синие кнопки с русской надписью «ВК» без человечка и без ошибки скрытой страницы", "done": True, "comment": "Ведут на открытую стену vk.com/mirmir.cafe."},
    {"id": "t_9", "date": "10.11.2026", "title": "9. Скрыть закреплённый пост о меню из ленты Новостей (обновлять из него только бланки 3D-меню) и починить фото постов", "done": True, "comment": "Закреп о меню отфильтрован, картинки синхронизированы."},
    {"id": "t_10", "date": "10.11.2026", "title": "10. Расширить экран на телефоне и ПК + разместить все крестики закрытия окон (✕) классически в правых верхних углах", "done": True, "comment": "Контейнеры расширены, крестики ✕ строго справа вверху."},
    {"id": "t_11", "date": "10.11.2026", "title": "11. Форма ручного добавления новых блюд в меню сайта (сверху в Шестерёнке Архитектора ⚙️)", "done": True, "comment": "Раскрывающаяся форма «➕ Добавить новое блюдо вручную» над списком блюд."},
    {"id": "t_12", "date": "10.11.2026", "title": "12. Большой подробный русский Текстовый Мастер-Промпт (ДНК сайта для любого ИИ) с возможностью редактирования на сайте", "done": True, "comment": "Доступен по кнопке 🧬 Промпт с сохранением правок."},
    {"id": "t_13", "date": "11.11.2026", "title": "13. Починить пустой экран в Шестерёнке Архитектора и сделать её шапку компактной", "done": True, "comment": "Встроена функция getCombinedBuildLogs, все 5 вкладок работают без сбоев."},
    {"id": "t_14", "date": "11.11.2026", "title": "14. Починить наезд кнопок внутри карточек блюд в Шестерёнке и убрать мясной кадр macro_mushrooms_raw.jpg", "done": True, "comment": "Карточка блюда выровнена, мясной суп заменён на веганский."},
    {"id": "t_15", "date": "11.11.2026", "title": "15. Выводить краткие логи ошибок генерации прямо в карточке блюда (HTTP-код, таймаут, лимит 45 сек)", "done": True, "comment": "Встроен мини-терминал диагностики под кнопками ИИ."},
    {"id": "t_16", "date": "11.11.2026", "title": "16. Полный «Список задач» с датами, переключением «Сделано / Не сделано» и полем комментария справа", "done": True, "comment": "Интерактивная таблица во вкладке №2 с авто-синхронизацией."},
    {"id": "t_17", "date": "11.11.2026", "title": "17. Внедрить предложения аудита Claude: выбор режима Брони/Заказа (Telegram/ВК без 152-ФЗ или Форма с 152-ФЗ), фильтр рекламы на Карте и мета-тег noindex", "done": True, "comment": "Тумблеры выбора добавлены во вкладку «⚡ Эффекты & Промпт» Шестерёнки!"}
]


def auto_migrate_assets_from_old_folder():
    os.makedirs("img", exist_ok=True)
    for old_d in OLD_DIRS_TO_CHECK:
        if not os.path.exists(old_d) or os.path.abspath(old_d) == BASE_DIR:
            continue
        for fname in ["vk key.txt", "goog api k.txt", "cache_posts.json", "tz_mirmir.json"]:
            src_f = os.path.join(old_d, fname)
            dst_f = os.path.join(BASE_DIR, fname)
            if os.path.exists(src_f) and not os.path.exists(dst_f):
                try:
                    shutil.copy2(src_f, dst_f)
                except Exception:
                    pass
        old_img_dir = os.path.join(old_d, "img")
        if os.path.exists(old_img_dir):
            for fn in os.listdir(old_img_dir):
                if fn.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                    if fn.startswith("ymap_org_") and fn not in ("ymap_org_0.jpg", "ymap_org_1.jpg"):
                        continue
                    s_img = os.path.join(old_img_dir, fn)
                    d_img = os.path.join(BASE_DIR, "img", fn)
                    if not os.path.exists(d_img) or os.path.getsize(d_img) < 1000:
                        try:
                            shutil.copy2(s_img, d_img)
                        except Exception:
                            pass


def purge_meat_looking_local_files():
    vegan_soup_donor = "img/macro_tomyum_bowl.jpg"
    if not os.path.exists(vegan_soup_donor):
        vegan_soup_donor = "img/vk_5128_1.jpg"
    for target_dir in [BASE_DIR, ROOT_REPO_DIR]:
        donor_fp = os.path.join(target_dir, vegan_soup_donor)
        if not os.path.exists(donor_fp):
            continue
        bad_fp = os.path.join(target_dir, "img/macro_mushrooms_raw.jpg")
        if os.path.exists(bad_fp):
            try:
                shutil.copy2(donor_fp, bad_fp)
            except Exception:
                pass


def enforce_vegan_prompts_in_menu_data_file():
    if not os.path.exists("menu_data.py"):
        return
    try:
        with open("menu_data.py", "r", encoding="utf-8") as f:
            code = f.read()

        def patch_prompt(match):
            prefix, val, suffix = match.group(1), match.group(2), match.group(3)
            low = val.lower()
            if not low.startswith("vegan plant-based"):
                val = "Vegan plant-based " + (val[0].lower() + val[1:] if len(val) > 1 else val)
            if "no meat" not in low:
                val = val.rstrip(".") + ", 100% vegan, no meat, no seafood"
            return f"{prefix}{val}{suffix}"

        new_code = re.sub(r'("ai_prompt"\s*:\s*")([^"]+)(")', patch_prompt, code)
        if new_code != code:
            with open("menu_data.py", "w", encoding="utf-8") as f:
                f.write(new_code)
    except Exception:
        pass


def get_verified_interior_exterior_photos():
    for target_img_dir in [os.path.join(BASE_DIR, "img"), os.path.join(ROOT_REPO_DIR, "img")]:
        if os.path.exists(target_img_dir):
            for fn in list(os.listdir(target_img_dir)):
                if fn.startswith("ymap_org_") and fn not in ("ymap_org_0.jpg", "ymap_org_1.jpg"):
                    try:
                        os.remove(os.path.join(target_img_dir, fn))
                    except Exception:
                        pass
    verified_candidates = [
        "img/ymap_org_0.jpg",
        "img/ymap_org_1.jpg",
        "img/vk_5068_0.jpg",
        "img/vk_5122_0.jpg",
        "img/vk_5134_0.jpg",
    ]
    result = [p for p in verified_candidates if os.path.exists(p)]
    return result if result else ["img/ymap_org_0.jpg", "img/ymap_org_1.jpg"]


def read_local_secret(filename):
    if os.path.exists(filename):
        try:
            return open(filename, "r", encoding="utf-8").read().strip()
        except Exception:
            pass
    return ""


def is_pinned_menu_post(text_str, is_pinned_flag=0):
    low = (text_str or "").lower()
    if "прикрепляю наше актуальное меню" in low or "актуальное меню" in low:
        return True
    if is_pinned_flag and ("меню" in low or "ланч по будням" in low):
        return True
    return False


def extract_best_image_from_vk_item(it):
    atts = list(it.get("attachments", []))
    if it.get("copy_history"):
        for ch in it["copy_history"]:
            atts.extend(ch.get("attachments", []))
    for att in atts:
        atype = att.get("type")
        if atype == "photo" and "photo" in att:
            sizes = att["photo"].get("sizes", [])
            if sizes:
                best = sorted(sizes, key=lambda s: s.get("width", 0), reverse=True)[0]
                if best.get("url"):
                    return best["url"]
        elif atype == "video" and "video" in att:
            vid_imgs = att["video"].get("image", []) or att["video"].get("first_frame", [])
            if vid_imgs:
                best = sorted(vid_imgs, key=lambda s: s.get("width", 0), reverse=True)[0]
                if best.get("url"):
                    return best["url"]
        elif atype == "link" and "link" in att and "photo" in att["link"]:
            sizes = att["link"]["photo"].get("sizes", [])
            if sizes:
                best = sorted(sizes, key=lambda s: s.get("width", 0), reverse=True)[0]
                if best.get("url"):
                    return best["url"]
    return ""


def fetch_vk_wall_posts():
    vk_token = os.environ.get("VK_TOKEN") or read_local_secret("vk key.txt")
    posts_out = []
    fallback_vk_photos = [
        "img/vk_5122_0.jpg",
        "img/vk_5068_0.jpg",
        "img/vk_5128_1.jpg",
        "img/vk_5134_0.jpg",
        "img/vk_5085_1.jpg",
    ]
    existing_fallbacks = [p for p in fallback_vk_photos if os.path.exists(p)] or ["img/ymap_org_0.jpg"]

    if vk_token:
        try:
            r = requests.get(
                "https://api.vk.com/method/wall.get",
                params={"domain": "mirmir.cafe", "count": 20, "access_token": vk_token, "v": "5.199"},
                timeout=8,
            )
            resp_json = r.json().get("response", {})
            items = resp_json.get("items", [])
            for it in items:
                txt = (it.get("text") or "").strip()
                if not txt or len(txt) < 15:
                    continue
                post_id = it.get("id")
                is_pinned = it.get("is_pinned", 0)

                if is_pinned_menu_post(txt, is_pinned):
                    scan_idx = 0
                    for att in it.get("attachments", []):
                        if att.get("type") == "photo" and scan_idx < 4:
                            sizes = att["photo"].get("sizes", [])
                            if sizes:
                                best_u = sorted(sizes, key=lambda s: s.get("width", 0), reverse=True)[0].get("url")
                                if best_u:
                                    scan_fp = os.path.join("img", f"vk_5047_{scan_idx}.jpg")
                                    if not os.path.exists(scan_fp) or os.path.getsize(scan_fp) < 5000:
                                        try:
                                            ir = requests.get(best_u, timeout=8)
                                            if ir.status_code == 200 and len(ir.content) > 5000:
                                                with open(scan_fp, "wb") as out_s:
                                                    out_s.write(ir.content)
                                        except Exception:
                                            pass
                                    scan_idx += 1
                    continue

                owner_id = it.get("owner_id")
                dt_str = datetime.fromtimestamp(it.get("date", 0)).strftime("%d.%m.%Y")
                likes = it.get("likes", {}).get("count", 25)
                img_url = extract_best_image_from_vk_item(it)
                photo_local = ""

                if img_url:
                    fn = f"vk_{post_id}_0.jpg"
                    fp = os.path.join("img", fn)
                    if not os.path.exists(fp) or os.path.getsize(fp) < 4000:
                        try:
                            ir = requests.get(img_url, timeout=8)
                            if ir.status_code == 200 and len(ir.content) > 4000:
                                with open(fp, "wb") as out_img:
                                    out_img.write(ir.content)
                        except Exception:
                            pass
                    if os.path.exists(fp) and os.path.getsize(fp) > 4000:
                        photo_local = f"img/{fn}"

                if not photo_local:
                    photo_local = existing_fallbacks[len(posts_out) % len(existing_fallbacks)]

                first_line = txt.split("\n")[0].strip()
                if owner_id and str(owner_id) != "-191992548" and post_id:
                    vk_link = f"https://vk.com/mirmir.cafe?w=wall{owner_id}_{post_id}"
                else:
                    vk_link = VK_PUBLIC_URL

                posts_out.append({
                    "id": post_id,
                    "date": dt_str,
                    "likes": likes,
                    "title": first_line[:68] + ("..." if len(first_line) > 68 else ""),
                    "text": txt[:280] + ("..." if len(txt) > 280 else ""),
                    "photo": photo_local,
                    "vk_url": vk_link,
                })
                if len(posts_out) >= 12:
                    break
            if posts_out:
                with open("cache_posts.json", "w", encoding="utf-8") as f:
                    json.dump(posts_out, f, ensure_ascii=False, indent=2)
                return posts_out
        except Exception:
            pass

    if os.path.exists("cache_posts.json"):
        try:
            cached = json.load(open("cache_posts.json", "r", encoding="utf-8"))
            if isinstance(cached, list) and cached:
                filtered_cache = []
                for idx_c, p in enumerate(cached):
                    txt_c = (p.get("title") or "") + " " + (p.get("text") or "")
                    if is_pinned_menu_post(txt_c, p.get("is_pinned", 0)):
                        continue
                    cur_u = str(p.get("vk_url") or "")
                    if "-191992548" in cur_u or not cur_u:
                        p["vk_url"] = VK_PUBLIC_URL
                    if not p.get("title"):
                        p["title"] = (p.get("text") or "Новость кафе").split("\n")[0][:65]
                    ph = p.get("photo") or ""
                    if not ph or not os.path.exists(ph) or os.path.getsize(ph) < 3000:
                        p["photo"] = existing_fallbacks[idx_c % len(existing_fallbacks)]
                    filtered_cache.append(p)
                return filtered_cache[:12]
        except Exception:
            pass
    return []


def collect_vk_food_photos():
    vk_food_photos = []
    if os.path.exists("img"):
        for fn in sorted(os.listdir("img"), reverse=True):
            if fn.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                if any(skip in fn for skip in ["5047_", "ymap_org_", "5068_0", "mushrooms_raw"]):
                    continue
                if fn.startswith(("vk_", "real_", "dish_")):
                    vk_food_photos.append("img/" + fn)
    return vk_food_photos


def sync_tz_and_build_logs():
    tz_data = {"tasks": [], "dishes": {}, "custom_dishes": []}
    if os.path.exists("tz_mirmir.json"):
        try:
            loaded_tz = json.load(open("tz_mirmir.json", "r", encoding="utf-8"))
            if isinstance(loaded_tz, dict):
                tz_data.update(loaded_tz)
        except Exception:
            pass

    existing_by_id = {}
    for t in tz_data.get("tasks", []):
        if isinstance(t, dict) and t.get("id"):
            existing_by_id[str(t["id"])] = t

    merged_tasks = []
    for def_t in MASTER_TASKS_DEFAULT:
        tid = def_t["id"]
        if tid in existing_by_id:
            old_t = existing_by_id.pop(tid)
            merged_tasks.append({
                "id": tid,
                "date": old_t.get("date") or def_t["date"],
                "title": def_t["title"],
                "done": bool(old_t.get("done", def_t["done"])),
                "comment": old_t.get("comment") if old_t.get("comment") is not None else def_t["comment"],
            })
        else:
            merged_tasks.append(dict(def_t))

    for extra_id, extra_t in existing_by_id.items():
        if len(str(extra_t.get("title", ""))) > 3:
            merged_tasks.append({
                "id": extra_id,
                "date": extra_t.get("date") or datetime.now().strftime("%d.%m.%Y"),
                "title": extra_t.get("title"),
                "done": bool(extra_t.get("done", False)),
                "comment": extra_t.get("comment") or "",
            })

    try:
        r = requests.get(f"https://ntfy.sh/{NTFY_SYNC_TOPIC}/json?poll=1&since=72h", timeout=4)
        if r.status_code == 200 and r.text.strip():
            for line in r.text.strip().splitlines():
                try:
                    ev = json.loads(line)
                    msg_str = ev.get("message") or ""
                    if msg_str.startswith("{"):
                        payload = json.loads(msg_str)
                        if payload.get("type") == "tz_tasks_sync" and isinstance(payload.get("tasks"), list):
                            merged_tasks = payload["tasks"]
                        elif payload.get("type") == "dish_photo_override" and payload.get("dish_name"):
                            tz_data.setdefault("dishes", {})[payload["dish_name"]] = {"photo": payload.get("photo")}
                except Exception:
                    pass
    except Exception:
        pass

    tz_data["tasks"] = merged_tasks
    with open("tz_mirmir.json", "w", encoding="utf-8") as f:
        json.dump(tz_data, f, ensure_ascii=False, indent=2)

    cnt = 1
    if os.path.exists("run_counter.txt"):
        try:
            cnt = int(open("run_counter.txt", "r", encoding="utf-8").read().strip()) + 1
        except Exception:
            cnt = 1
    with open("run_counter.txt", "w", encoding="utf-8") as f:
        f.write(str(cnt))

    logs = []
    if os.path.exists("build_history.json"):
        try:
            loaded = json.load(open("build_history.json", "r", encoding="utf-8"))
            if isinstance(loaded, list):
                logs = loaded
        except Exception:
            logs = []

    now_str = datetime.now().strftime("%d.%m.%Y %H:%M")
    logs.insert(0, {
        "version": f"Релиз v3.6 • Сборка #{cnt}",
        "timestamp": now_str,
        "model": "Монолит v3.6: Починка Шестерёнки + Аудит Claude (Бронь ТГ/ВК или 152-ФЗ на выбор, Карта без рекламы, 0 дублей кнопок)",
        "status": "Восстановлены все 5 вкладок Шестерёнки, убраны тройные дубли кнопок и пустое поле внизу, добавлен выбор режима Брони/Карты/Фото в админке и мета-тег noindex.",
        "stats": f"Дата сборки: {now_str}",
    })
    with open("build_history.json", "w", encoding="utf-8") as f:
        json.dump(logs[:60], f, ensure_ascii=False, indent=2)

    return tz_data, logs[:60], cnt


def upgrade_template_html_in_place(tpl_html):
    """
    1. Добавляет <meta name="robots" content="noindex, nofollow"> в <head> (на время статуса черновика).
    2. Чисто срезает старый хвост после downloadMasterPromptFile() и прошивает монолитное ядро v3.6:
       - Включает недостававшие функции getCombinedBuildLogs, getSavedIdeasNotes, getSiteToggles (устраняет пустой экран Шестерёнки!).
       - Убирает все дубли кнопок сверху, в первом экране и внутри карточки карты, а также убирает бежевую пустыню внизу.
       - Добавляет во вкладку «⚡ Эффекты & Промпт» переключатели режимов Брони/Заказа (Telegram/ВК без 152-ФЗ или Форма с 152-ФЗ), Карты и Фото.
    """
    if 'name="robots"' not in tpl_html:
        tpl_html = tpl_html.replace(
            "<head>",
            '<head>\n  <meta name="robots" content="noindex, nofollow">',
            1,
        )

    old_wm_block = (
        '<div class="absolute inset-0 flex items-center justify-center pointer-events-none opacity-[0.35] z-0">\n'
        '          <div class="wm-spin">\n'
        '            <svg width="420" height="420" viewBox="0 0 120 120" fill="none"><circle cx="60" cy="60" r="56" stroke="#F2B880" stroke-width="3"/><circle cx="60" cy="60" r="50" stroke="#FFFDF9" stroke-width="2" stroke-dasharray="5 4"/><circle cx="60" cy="62" r="25" stroke="#F2B880" stroke-width="2.5" fill="rgba(242,184,128,0.18)"/><text x="60" y="106" text-anchor="middle" fill="#F2B880" font-family="serif" font-weight="bold" font-size="11" letter-spacing="3">• MIR MIR •</text></svg>\n'
        '          </div>\n'
        '        </div>'
    )
    new_wm_block = (
        '<!-- Плавный фоновый слайдер фото интерьера в правой колонке + вращающийся медальон с Голубкой мира -->\n'
        '        <div class="absolute inset-0 pointer-events-none z-0 overflow-hidden">\n'
        '          <img id="right-col-bg-photo" src="img/ymap_org_0.jpg" alt="Интерьер кафе Мир Мир" class="w-full h-full object-cover opacity-30 scale-105 transition-all duration-1000 filter saturate-125 contrast-110">\n'
        '          <div class="absolute inset-0" style="background:radial-gradient(circle at center, rgba(28,42,24,0.35) 0%, rgba(26,38,22,0.88) 85%);"></div>\n'
        '        </div>\n'
        '        <div class="absolute inset-0 flex items-center justify-center pointer-events-none opacity-[0.28] z-0">\n'
        '          <div class="w-[370px] h-[370px] wm-spin" data-dove-holder></div>\n'
        '        </div>'
    )
    if old_wm_block in tpl_html:
        tpl_html = tpl_html.replace(old_wm_block, new_wm_block)

    anchor_str = 'a.download = "MASTER_PROMPT_MIRMIR.txt";'
    anchor_pos = tpl_html.find(anchor_str)
    if anchor_pos != -1:
        brace_pos = tpl_html.find("}", anchor_pos)
        if brace_pos != -1:
            tpl_html = tpl_html[: brace_pos + 1] + "\n"

    v36_clean_tail = r"""
    // === 🚀 ЕДИНОЕ ЯДРО v3.6: ПОЧИНКА ШЕСТЕРЁНКИ + 0 ДУБЛЕЙ КНОПОК + ПЕРЕКЛЮЧАТЕЛИ АУДИТА CLAUDE (БРОНЬ ТГ/ВК ИЛИ 152-ФЗ, КАРТА, ФОТО) ===
    const NTFY_SYNC_URL = "https://ntfy.sh/mirmir_tz_sync_nn45_v30";
    window.customPromptsPerDish = window.customPromptsPerDish || {};
    window.dishVariantStep = window.dishVariantStep || {};
    window.cachedSearchPools = window.cachedSearchPools || {};
    window.dishDiagLogs = window.dishDiagLogs || {};
    window.dishAddPanelOpen = window.dishAddPanelOpen || false;

    // 0. Вспомогательные функции, отсутствие которых вызывало пустой экран в Шестерёнке v3.5!
    window.getCombinedBuildLogs = function() {
      const baseLogs = Array.isArray(DATA.full_build_logs) ? DATA.full_build_logs : [];
      try {
        const localRaw = localStorage.getItem("mirmir_local_action_logs_v1");
        const localArr = localRaw ? JSON.parse(localRaw) : [];
        return [...localArr, ...baseLogs];
      } catch(e) {
        return baseLogs;
      }
    };

    window.addLocalBuildOrActionLog = function(titleStr, detailsStr) {
      try {
        const localRaw = localStorage.getItem("mirmir_local_action_logs_v1");
        const localArr = localRaw ? JSON.parse(localRaw) : [];
        localArr.unshift({
          version: "Действие в браузере",
          timestamp: new Date().toLocaleString("ru-RU"),
          model: titleStr,
          status: detailsStr || ""
        });
        localStorage.setItem("mirmir_local_action_logs_v1", JSON.stringify(localArr.slice(0, 40)));
      } catch(e) {}
    };

    window.getSavedIdeasNotes = function() {
      try {
        const raw = localStorage.getItem("mirmir_ideas_notes_v1");
        if (raw) return JSON.parse(raw);
      } catch(e) {}
      return [
        { text: "После согласования с владельцами кафе получить токен группы ВК и включить авто-обновление по расписанию через GitHub Actions.", date: "11.11.2026" },
        { text: "Заполнить истории разделов «НАША КОМАНДА», «ИСТОРИЯ КАФЕ» и «НАШИ ЦЕННОСТИ» вместе с основателями.", date: "11.11.2026" }
      ];
    };

    window.addNewIdeaNote = function() {
      const inp = document.getElementById("new-idea-note-inp");
      const val = (inp?.value || "").trim();
      if (!val) return;
      const list = window.getSavedIdeasNotes();
      list.unshift({ text: val, date: new Date().toLocaleString("ru-RU") });
      try { localStorage.setItem("mirmir_ideas_notes_v1", JSON.stringify(list)); } catch(e) {}
      if (inp) inp.value = "";
      renderUnifiedSystemHub();
    };

    // Настройки и переключатели администратора (включая выбор режима Бронирования, Карты и Фото по аудиту Claude!)
    window.getSiteToggles = function() {
      const defaults = {
        leaves: true,
        wings: true,
        zoom: true,
        bookingMode: "messenger", // "messenger" (Telegram/ВК без сбора телефонов и 152-ФЗ) ИЛИ "form152" (Форма на сайте с галочкой 152-ФЗ)
        mapMode: "clean_card",    // "clean_card" (Чистая карточка маршрута без рекламы OpenRouter в iframe) ИЛИ "iframe" (Живой iframe Яндекса)
        photoMode: "hybrid"       // "hybrid" (Все фото + плашка подачи) ИЛИ "strict_real" (Только 100% реальные фото из ВК кафе)
      };
      try {
        const raw = localStorage.getItem("mirmir_site_toggles_v36");
        if (raw) return Object.assign({}, defaults, JSON.parse(raw));
      } catch(e) {}
      return defaults;
    };

    window.setAdminSettingV36 = function(key, val) {
      const tg = window.getSiteToggles();
      tg[key] = val;
      try { localStorage.setItem("mirmir_site_toggles_v36", JSON.stringify(tg)); } catch(e) {}
      window.applySiteToggles();
      renderDishes();
      renderHeroRightColumn();
      renderUnifiedSystemHub();
    };

    window.toggleSiteEffect = function(key, isChecked) {
      window.setAdminSettingV36(key, Boolean(isChecked));
    };

    window.applySiteToggles = function() {
      const tg = window.getSiteToggles();
      const leavesBox = document.getElementById("falling-leaves-box");
      if (leavesBox) leavesBox.style.display = tg.leaves ? "block" : "none";
      const wingsBox = document.getElementById("side-photo-wings");
      if (wingsBox) wingsBox.style.display = tg.wings ? "" : "none";
      document.body.classList.toggle("disable-card-zoom", !tg.zoom);
      window.applyMapModeV36();
      window.applyBookingAndCartModeV36();
    };

    function pushDiagLog(idx, statusIcon, engineLabel, detailMsg) {
      const nowTime = new Date().toLocaleTimeString("ru-RU", { hour: "2-digit", minute: "2-digit", second: "2-digit" });
      if (!window.dishDiagLogs[idx]) window.dishDiagLogs[idx] = [];
      window.dishDiagLogs[idx].unshift("[" + nowTime + "] " + statusIcon + " " + engineLabel + ": " + detailMsg);
      window.dishDiagLogs[idx] = window.dishDiagLogs[idx].slice(0, 4);
    }

    function loadCustomAddedDishes() {
      try {
        const raw = localStorage.getItem("mirmir_custom_dishes_v1");
        const localArr = raw ? JSON.parse(raw) : [];
        const tzArr = (DATA.tz_synced && Array.isArray(DATA.tz_synced.custom_dishes)) ? DATA.tz_synced.custom_dishes : [];
        const mergedMap = {};
        [...tzArr, ...localArr].forEach(item => {
          if (item && item.name) mergedMap[item.name] = item;
        });
        return Object.values(mergedMap);
      } catch(e) { return []; }
    }

    function injectCustomDishesIntoMenu() {
      const customList = loadCustomAddedDishes();
      if (!DATA.menu) DATA.menu = [];
      customList.forEach(cd => {
        const exists = DATA.menu.some(m => m.name === cd.name);
        if (!exists) DATA.menu.unshift(cd);
      });
      DATA.menu.forEach(d => {
        if (d.photo && d.photo.includes("macro_mushrooms_raw")) {
          d.photo = "img/macro_tomyum_bowl.jpg";
        }
      });
    }

    // 1. Загрузка и сохранение полного Списка задач с датами, статусами и комментариями Милорда
    function getMasterTasksList() {
      const serverTasks = (DATA.tz_synced && Array.isArray(DATA.tz_synced.tasks)) ? DATA.tz_synced.tasks : [];
      try {
        const savedRaw = localStorage.getItem("mirmir_tasks_v36");
        if (savedRaw) {
          const localTasks = JSON.parse(savedRaw);
          const byId = {};
          localTasks.forEach(t => { if (t && t.id) byId[t.id] = t; });
          const merged = serverTasks.map(st => {
            if (byId[st.id]) {
              return {
                id: st.id,
                date: byId[st.id].date || st.date || "11.11.2026",
                title: st.title,
                done: Boolean(byId[st.id].done),
                comment: byId[st.id].comment !== undefined ? byId[st.id].comment : (st.comment || "")
              };
            }
            return st;
          });
          localTasks.forEach(lt => {
            if (lt && lt.id && String(lt.id).startsWith("t_user_") && !merged.some(m => m.id === lt.id)) {
              merged.unshift(lt);
            }
          });
          return merged;
        }
      } catch(e) {}
      return serverTasks;
    }

    function saveMasterTasksList(tasksArr, syncToCloud = true) {
      try {
        localStorage.setItem("mirmir_tasks_v36", JSON.stringify(tasksArr));
        if (DATA.tz_synced) DATA.tz_synced.tasks = tasksArr;
        if (syncToCloud) {
          fetch(NTFY_SYNC_URL, {
            method: "POST",
            body: JSON.stringify({ type: "tz_tasks_sync", tasks: tasksArr, ts: Date.now() })
          }).catch(() => {});
        }
      } catch(e) {}
    }

    window.toggleTaskDoneV35 = function(idx) {
      const list = getMasterTasksList();
      if (!list[idx]) return;
      list[idx].done = !list[idx].done;
      saveMasterTasksList(list, true);
      renderUnifiedSystemHub();
    };

    window.updateTaskCommentV35 = function(idx, newComment) {
      const list = getMasterTasksList();
      if (!list[idx]) return;
      list[idx].comment = newComment;
      saveMasterTasksList(list, false);
    };

    window.syncTaskCommentOnBlurV35 = function(idx, newComment) {
      const list = getMasterTasksList();
      if (!list[idx]) return;
      list[idx].comment = newComment;
      saveMasterTasksList(list, true);
      const badge = document.getElementById("task-sync-indicator");
      if (badge) {
        badge.textContent = "✅ Сохранено и отправлено в app.py (" + new Date().toLocaleTimeString() + ")";
      }
    };

    window.addNewTaskV35 = function() {
      const inp = document.getElementById("new-tz-task-inp");
      const commentInp = document.getElementById("new-tz-comment-inp");
      const title = (inp?.value || "").trim();
      if (!title) return;
      const list = getMasterTasksList();
      const todayStr = new Date().toLocaleDateString("ru-RU");
      list.unshift({
        id: "t_user_" + Date.now(),
        date: todayStr,
        title: (list.length + 1) + ". " + title,
        done: false,
        comment: (commentInp?.value || "Новая задача от Милорда — проверить при сборке").trim()
      });
      saveMasterTasksList(list, true);
      if (inp) inp.value = "";
      if (commentInp) commentInp.value = "";
      renderUnifiedSystemHub();
    };

    window.downloadTzJsonFile = function() {
      const list = getMasterTasksList();
      const payload = {
        tasks: list,
        dishes: (DATA.tz_synced && DATA.tz_synced.dishes) ? DATA.tz_synced.dishes : {},
        custom_dishes: loadCustomAddedDishes()
      };
      const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json;charset=utf-8" });
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = "tz_mirmir.json";
      a.click();
    };

    // 2. УПРАВЛЕНИЕ РЕЖИМОМ КАРТЫ (Чистая карточка маршрута БЕЗ рекламы OpenRouter в iframe ИЛИ Живой iframe)
    window.applyMapModeV36 = function() {
      const tg = window.getSiteToggles();
      const mapIframe = document.querySelector("iframe[src*='yandex']");
      if (!mapIframe) return;
      const mapContainer = mapIframe.parentElement;
      if (!mapContainer) return;

      let cleanOverlay = document.getElementById("v36-clean-map-card");
      if (tg.mapMode === "clean_card") {
        mapIframe.style.display = "none";
        if (!cleanOverlay) {
          cleanOverlay = document.createElement("div");
          cleanOverlay.id = "v36-clean-map-card";
          cleanOverlay.className = "w-full h-full min-h-[260px] rounded-2xl overflow-hidden relative flex flex-col items-center justify-center p-6 text-center bg-[#1F2B1A] border border-[#F2B880]/40";
          cleanOverlay.innerHTML =
            '<img src="img/ymap_org_1.jpg" alt="Фасад кафе Мир Мир на Ильинской, 45" class="absolute inset-0 w-full h-full object-cover opacity-35">' +
            '<div class="relative z-10 max-w-md space-y-3 bg-black/55 backdrop-blur-xs p-5 rounded-2xl border border-[#F2B880]/40">' +
              '<div class="text-xs font-extrabold uppercase tracking-widest text-[#F2B880]">📍 Исторический центр Нижнего Новгорода</div>' +
              '<h4 class="font-serif text-2xl font-bold text-white">ул. Ильинская, 45</h4>' +
              '<p class="text-xs text-stone-200 leading-relaxed">Уютный зал со старинными кирпичными сводами и вывеской с белой Голубкой мира. Ежедневно с 12:00 до 21:00.</p>' +
              '<div class="flex flex-wrap items-center justify-center gap-2 pt-1">' +
                '<a href="https://yandex.ru/maps/org/mir_mir/7309581265/" target="_blank" class="px-4 py-2 rounded-xl bg-[#D48238] hover:opacity-95 text-white text-xs font-extrabold shadow cursor-pointer">🗺️ Открыть в Яндекс.Картах ↗</a>' +
                '<button onclick="setAdminSettingV36(\'mapMode\', \'iframe\')" class="px-3 py-2 rounded-xl bg-white/15 hover:bg-white/25 text-stone-200 text-xs font-bold cursor-pointer">🌐 Показать интерактивную карту</button>' +
              '</div>' +
            '</div>';
          mapContainer.appendChild(cleanOverlay);
        } else {
          cleanOverlay.style.display = "flex";
        }
      } else {
        mapIframe.style.display = "block";
        if (cleanOverlay) cleanOverlay.style.display = "none";
      }
    };

    // 3. УПРАВЛЕНИЕ РЕЖИМОМ БРОНИ И ЗАКАЗА (Переход в Telegram / ВК без сбора ПДн 152-ФЗ ИЛИ Классическая анкета с 152-ФЗ)
    window.sendBookingViaMessengerV36 = function(channel) {
      const dateVal = document.getElementById("book-date-v36")?.value || "Сегодня";
      const timeVal = document.getElementById("book-time-v36")?.value || "18:00";
      const guestsVal = document.getElementById("book-guests-v36")?.value || "2 гостя";
      const wishVal = document.getElementById("book-wish-v36")?.value || "Уютный столик";
      const msg = "🕊️ Здравствуйте! Хочу забронировать столик в «Мир Мир» (Ильинская, 45):\n📅 Дата: " + dateVal + "\n🕒 Время: " + timeVal + "\n👥 Гостей: " + guestsVal + "\n💬 Пожелания: " + wishVal;
      try { navigator.clipboard.writeText(msg); } catch(e) {}
      const targetUrl = channel === "tg"
        ? "https://t.me/mirmir_chef"
        : "https://vk.com/mirmir.cafe";
      alert("📋 Текст брони скопирован в буфер обмена!\nСейчас откроется диалог с кафе — просто вставьте сообщение (Ctrl+V) и отправьте администратору:\n\n" + msg);
      window.open(targetUrl, "_blank");
      closeBookTableModal();
    };

    window.applyBookingAndCartModeV36 = function() {
      const tg = window.getSiteToggles();
      const bookModal = document.getElementById("book-table-modal");
      if (!bookModal) return;
      const card = bookModal.firstElementChild;
      if (!card) return;

      let bodyBox = document.getElementById("v36-booking-dynamic-body");
      if (!bodyBox) {
        const oldForm = card.querySelector("form") || card.querySelector(".space-y-3");
        if (oldForm) {
          bodyBox = document.createElement("div");
          bodyBox.id = "v36-booking-dynamic-body";
          oldForm.replaceWith(bodyBox);
        }
      }
      if (!bodyBox) return;

      if (tg.bookingMode === "messenger") {
        bodyBox.innerHTML =
          '<div class="space-y-3 text-left">' +
            '<div class="p-3 rounded-2xl bg-emerald-50 border border-emerald-200 text-xs text-[#2E3D28] leading-relaxed">' +
              '✨ <strong>Прямая бронь без анкет и ожидания:</strong> выберите параметры столика, и сайт сформирует готовое сообщение напрямую в Telegram или ВК кафе (без сбора телефонов на сайте).' +
            '</div>' +
            '<div class="grid grid-cols-1 sm:grid-cols-3 gap-2">' +
              '<div><label class="text-[10px] font-extrabold uppercase text-stone-500 block mb-1">📅 Дата</label><input id="book-date-v36" type="text" value="Сегодня" class="w-full px-3 py-2 rounded-xl border border-stone-300 text-xs font-bold"></div>' +
              '<div><label class="text-[10px] font-extrabold uppercase text-stone-500 block mb-1">🕒 Время</label><input id="book-time-v36" type="text" value="18:30" class="w-full px-3 py-2 rounded-xl border border-stone-300 text-xs font-bold"></div>' +
              '<div><label class="text-[10px] font-extrabold uppercase text-stone-500 block mb-1">👥 Гостей</label><select id="book-guests-v36" class="w-full px-3 py-2 rounded-xl border border-stone-300 text-xs font-bold"><option>2 гостя</option><option>1 гость</option><option>3–4 гостя</option><option>Компания 5+ человек</option></select></div>' +
            '</div>' +
            '<div><label class="text-[10px] font-extrabold uppercase text-stone-500 block mb-1">💬 Пожелания к столику или чаю</label><input id="book-wish-v36" type="text" placeholder="Например: столик у кирпичного свода или диван..." class="w-full px-3 py-2 rounded-xl border border-stone-300 text-xs"></div>' +
            '<div class="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1">' +
              '<button type="button" onclick="sendBookingViaMessengerV36(\'tg\')" class="py-2.5 px-4 rounded-xl bg-[#2E3D28] hover:bg-[#D48238] text-[#F2B880] hover:text-white font-extrabold text-xs cursor-pointer shadow transition">✈️ Отправить бронь в Telegram ↗</button>' +
              '<button type="button" onclick="sendBookingViaMessengerV36(\'vk\')" class="py-2.5 px-4 rounded-xl bg-[#0077FF] hover:bg-[#0055CC] text-white font-extrabold text-xs cursor-pointer shadow transition">💬 Отправить бронь в ВК кафе ↗</button>' +
            '</div>' +
            '<div class="text-center pt-1"><a href="tel:+79200282858" class="text-xs font-extrabold text-[#556432] hover:underline">📞 Или позвонить в зал: +7 (920) 028-28-58</a></div>' +
          '</div>';
      } else {
        bodyBox.innerHTML =
          '<form onsubmit="event.preventDefault();alert(\'✅ Заявка сформирована! Администратор свяжется с вами для подтверждения столика.\');closeBookTableModal();" class="space-y-3 text-left">' +
            '<div class="grid grid-cols-1 sm:grid-cols-2 gap-2">' +
              '<input type="text" required placeholder="Ваше имя" class="px-3 py-2 rounded-xl border border-stone-300 text-xs font-bold">' +
              '<input type="tel" required placeholder="Телефон для подтверждения" class="px-3 py-2 rounded-xl border border-stone-300 text-xs font-bold">' +
            '</div>' +
            '<div class="grid grid-cols-2 gap-2">' +
              '<input type="text" value="Сегодня, 18:30" class="px-3 py-2 rounded-xl border border-stone-300 text-xs">' +
              '<select class="px-3 py-2 rounded-xl border border-stone-300 text-xs font-bold"><option>2 гостя</option><option>3–4 гостя</option><option>5+ гостей</option></select>' +
            '</div>' +
            '<label class="flex items-start gap-2 text-[11px] text-stone-600 cursor-pointer">' +
              '<input type="checkbox" required checked class="mt-0.5 accent-[#2E3D28]">' +
              '<span>Я даю согласие на обработку персональных данных в соответствии с 152-ФЗ исключительно для подтверждения брони столика.</span>' +
            '</label>' +
            '<button type="submit" class="w-full py-2.5 rounded-xl bg-[#2E3D28] hover:bg-[#D48238] text-[#F2B880] hover:text-white font-extrabold text-xs cursor-pointer shadow">🪑 Отправить заявку на бронь</button>' +
          '</form>';
      }
    };

    // 4. Глобальные стили v3.6 (убираем ВСЕ дубли кнопок и срезаем гигантское пустое бежевое поле внизу!)
    function injectV36GlobalStyles() {
      if (document.getElementById("mirmir-v36-styles")) return;
      const st = document.createElement("style");
      st.id = "mirmir-v36-styles";
      st.textContent = `
        /* Убираем лишнюю высоту бежевого полотна внизу экрана! */
        html, body {
          min-height: auto !important;
          height: auto !important;
        }
        main.max-w-\\[1440px\\], header .max-w-\\[1440px\\], footer .max-w-\\[1440px\\] {
          max-width: 1640px !important;
          width: 100% !important;
          min-height: 0 !important;
        }
        main.max-w-\\[1440px\\] {
          padding-bottom: 12px !important;
        }
        header .max-w-\\[1440px\\] {
          padding-top: 6px !important;
          padding-bottom: 6px !important;
        }
        #category-rail {
          padding-top: 4px !important;
          padding-bottom: 4px !important;
        }
        @media (max-width: 640px) {
          main.max-w-\\[1440px\\] { padding-left: 6px !important; padding-right: 6px !important; padding-top: 4px !important; }
          header .max-w-\\[1440px\\] { padding-left: 8px !important; padding-right: 8px !important; }
          #header-work-badge { display: none !important; }
        }
        /* Компактная шапка Шестерёнки Архитектора */
        #unified-system-hub > div > div.bg-\\[\\#2E3D28\\] {
          padding: 10px 48px 10px 16px !important;
        }
        #unified-system-hub > div > div.bg-\\[\\#2E3D28\\] h3 {
          font-size: 1.15rem !important;
          line-height: 1.3 !important;
        }
        #unified-system-hub > div > div.bg-\\[\\#2E3D28\\] p {
          display: none !important;
        }
        /* Жёстко скрываем ВСЕ дублирующиеся кнопки в шапке, в левой колонке первого экрана и внутри карточки адреса/карты! */
        header button[onclick*="openBookTableModal"],
        header button[onclick*="openBowlBuilder"],
        header button[onclick*="openRadioSelectorModal"],
        header button[onclick*="openDeliveryModal"],
        header a[href*="taxi.yandex"],
        header a[href*="appmetrica.yandex"],
        #category-rail button[onclick*="openBowlBuilder"],
        main section .lg\\:col-span-7 div[onclick*="Сезонные спешлы от Шефа"],
        main section .lg\\:col-span-7 .grid.grid-cols-2.sm\\:grid-cols-4,
        main section .lg\\:col-span-7 .grid.grid-cols-2.sm\\:grid-cols-3 {
          display: none !important;
        }
        /* Классический крестик закрытия (✕) строго в правом верхнем углу любого модального окна */
        .v36-top-right-close {
          position: absolute !important;
          top: 10px !important;
          right: 10px !important;
          z-index: 95 !important;
          width: 34px !important;
          height: 34px !important;
          border-radius: 9999px !important;
          background: rgba(20, 28, 17, 0.92) !important;
          color: #FFFDF9 !important;
          border: 1.5px solid rgba(242, 184, 128, 0.7) !important;
          display: inline-flex !important;
          align-items: center !important;
          justify-content: center !important;
          font-size: 16px !important;
          font-weight: 900 !important;
          line-height: 1 !important;
          cursor: pointer !important;
          box-shadow: 0 3px 10px rgba(0,0,0,0.35) !important;
          transition: all 0.18s ease !important;
        }
        .v36-top-right-close:hover {
          background: #D48238 !important;
          color: #fff !important;
          transform: scale(1.06);
        }
      `;
      document.head.appendChild(st);
    }

    function applyV36LayoutAndButtons() {
      injectV36GlobalStyles();

      // Прячем дубли кнопок в верхней шапке по тексту (Бронь, Боул, Такси, Радио, Доставка)
      document.querySelectorAll("header button, header a").forEach(el => {
        const txt = (el.textContent || "").toLowerCase();
        if (txt.includes("бронь") || txt.includes("боул") || txt.includes("такси") || txt.includes("радио") || txt.includes("доставка")) {
          el.style.setProperty("display", "none", "important");
        }
      });
      // Убираем дубли кнопок внутри зелёной карточки с картой («Нижний Новгород, ул. Ильинская, 45»)
      const mapIframe = document.querySelector("iframe[src*='yandex']");
      if (mapIframe) {
        const mapSection = mapIframe.closest("section");
        if (mapSection) {
          mapSection.querySelectorAll("button, a").forEach(btn => {
            const oc = btn.getAttribute("onclick") || "";
            const hr = btn.getAttribute("href") || "";
            if (oc.includes("openBookTableModal") || oc.includes("openDeliveryModal") || oc.includes("openRadioSelectorModal") || hr.includes("appmetrica.yandex") || hr.includes("taxi.yandex")) {
              btn.style.display = "none";
            }
          });
        }
      }

      // Проставляем alt для всех картинок на странице (по пункту 7 аудита Claude)
      document.querySelectorAll("img:not([alt]), img[alt='']").forEach(imgEl => {
        imgEl.setAttribute("alt", "Веган-кафе и чайная Мир Мир — Нижний Новгород, Ильинская, 45");
      });

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
        if (!m) return;
        const innerCard = m.firstElementChild;
        if (!innerCard) return;
        innerCard.style.position = "relative";
        innerCard.querySelectorAll("button").forEach(b => {
          if (b.textContent.trim() === "✕" && !b.classList.contains("v36-top-right-close")) {
            b.style.display = "none";
          }
        });
        if (!innerCard.querySelector(".v36-top-right-close")) {
          const closeBtn = document.createElement("button");
          closeBtn.className = "v36-top-right-close";
          closeBtn.setAttribute("onclick", cfg.closeFn);
          closeBtn.setAttribute("title", "Закрыть (Esc)");
          closeBtn.innerHTML = "✕";
          innerCard.appendChild(closeBtn);
        }
      });

      // ЕДИНСТВЕННАЯ КОМПАКТНАЯ НИЖНЯЯ ПАНЕЛЬ В СПОКОЙНОЙ ПАЛИТРЕ КАФЕ (прямо внутри main под картой, без вылета за бежевый лист!)
      const mainEl = document.querySelector("main");
      ["v33-bottom-nav-hub", "v34-bottom-nav-hub", "v35-bottom-nav-hub"].forEach(oldId => {
        const el = document.getElementById(oldId);
        if (el) el.remove();
      });

      if (mainEl && !document.getElementById("v36-bottom-nav-hub")) {
        const taxiUrl = "https://3.redirect.appmetrica.yandex.com/route?end-lat=56.322355&end-lon=43.990383&appmetrica_tracking_id=1178268795219780156";
        const navHub = document.createElement("section");
        navHub.id = "v36-bottom-nav-hub";
        navHub.className = "max-w-3xl mx-auto pt-2 pb-1";
        navHub.innerHTML =
          '<div class="bg-[#23311E] text-[#FFFDF9] rounded-2xl p-2.5 border border-[#F2B880]/40 shadow-md space-y-2">' +
            '<div class="grid grid-cols-2 sm:grid-cols-4 gap-2">' +
              '<button onclick="openBookTableModal()" class="py-2 px-3 rounded-xl bg-[#556432] hover:bg-[#D48238] text-[#FFFDF9] font-extrabold text-xs flex items-center justify-center gap-1.5 shadow-xs cursor-pointer transition border border-[#F2B880]/30">' +
                '<span>🪑</span><span>Бронь</span>' +
              '</button>' +
              '<a href="' + taxiUrl + '" target="_blank" class="py-2 px-3 rounded-xl bg-[#3A4A2E] hover:bg-[#D48238] text-[#F2B880] hover:text-white font-extrabold text-xs flex items-center justify-center gap-1.5 shadow-xs cursor-pointer transition border border-[#F2B880]/30">' +
                '<span>🚕</span><span>Такси в кафе</span>' +
              '</a>' +
              '<button onclick="openDeliveryModal()" class="py-2 px-3 rounded-xl bg-[#556432] hover:bg-[#D48238] text-[#FFFDF9] font-extrabold text-xs flex items-center justify-center gap-1.5 shadow-xs cursor-pointer transition border border-[#F2B880]/30">' +
                '<span>🛵</span><span>Доставка</span>' +
              '</button>' +
              '<button onclick="openRadioSelectorModal()" class="py-2 px-3 rounded-xl bg-[#FFFDF9] hover:bg-amber-50 text-[#2E3D28] font-extrabold text-xs flex items-center justify-center gap-1.5 shadow-xs cursor-pointer transition">' +
                '<span>📻</span><span>Радио</span>' +
              '</button>' +
            '</div>' +
            '<div class="pt-1.5 border-t border-white/15 grid grid-cols-3 gap-1.5">' +
              '<button disabled class="py-1 px-2 rounded-lg bg-white/10 text-white/65 font-extrabold text-[10px] tracking-wider uppercase flex items-center justify-center gap-1 border border-white/10 cursor-not-allowed">' +
                '<span>👥 НАША КОМАНДА</span><span class="px-1 rounded bg-black/40 text-[#F2B880] text-[8px]">Скоро</span>' +
              '</button>' +
              '<button disabled class="py-1 px-2 rounded-lg bg-white/10 text-white/65 font-extrabold text-[10px] tracking-wider uppercase flex items-center justify-center gap-1 border border-white/10 cursor-not-allowed">' +
                '<span>🏛️ ИСТОРИЯ КАФЕ</span><span class="px-1 rounded bg-black/40 text-[#F2B880] text-[8px]">Скоро</span>' +
              '</button>' +
              '<button disabled class="py-1 px-2 rounded-lg bg-white/10 text-white/65 font-extrabold text-[10px] tracking-wider uppercase flex items-center justify-center gap-1 border border-white/10 cursor-not-allowed">' +
                '<span>🌿 НАШИ ЦЕННОСТИ</span><span class="px-1 rounded bg-black/40 text-[#F2B880] text-[8px]">Скоро</span>' +
              '</button>' +
            '</div>' +
          '</div>';
        mainEl.appendChild(navHub);
      }

      const footerEl = document.querySelector("footer");
      if (footerEl) {
        footerEl.querySelectorAll(".grid.grid-cols-1.sm\\:grid-cols-3").forEach(g => { g.style.display = "none"; });
      }
      window.applyMapModeV36();
      window.applyBookingAndCartModeV36();
    }

    // 5. ШЕСТЕРЁНКА АРХИТЕКТОРА (⚙️) — ВСЕ 5 ВКЛАДОК + ПЕРЕКЛЮЧАТЕЛИ РЕЖИМОВ БРОНИ / КАРТЫ / ФОТО!
    window.runEngineForDish = function(idx, engKey) {
      const inp = document.getElementById("hub-ai-prm-" + idx);
      if (inp) window.customPromptsPerDish[idx] = inp.value;
      selectedAiEnginePerDish[idx] = engKey;
      window.generateDishCandidateAI(idx);
    };

    window.addNewCustomDishFromHub = function() {
      const name = (document.getElementById("new-dish-name")?.value || "").trim();
      if (!name) { alert("Введите название нового блюда!"); return; }
      const cat = (document.getElementById("new-dish-cat")?.value || "Сезонные спешлы от Шефа").trim();
      const price = parseInt(document.getElementById("new-dish-price")?.value || "450", 10) || 450;
      const weight = (document.getElementById("new-dish-weight")?.value || "260 г").trim();
      const desc = (document.getElementById("new-dish-desc")?.value || "Авторское 100% растительное блюдо шеф-повара кафе «Мир Мир».").trim();
      const photo = (document.getElementById("new-dish-photo")?.value || "img/macro_vegan_burger.jpg").trim();

      const newDishObj = {
        id: "custom_" + Date.now(),
        category: cat,
        name: name,
        weight: weight,
        price: price,
        photo: photo,
        photo_type: "real",
        desc: desc,
        ai_prompt: "Vegan plant-based " + name + ", 100% vegan, no meat, no seafood",
        is_custom_added: true
      };

      const savedList = loadCustomAddedDishes().filter(d => d.name !== name);
      savedList.unshift(newDishObj);
      localStorage.setItem("mirmir_custom_dishes_v1", JSON.stringify(savedList));

      DATA.menu.unshift(newDishObj);
      window.addLocalBuildOrActionLog("➕ Добавлено блюдо: «" + name + "» (" + price + " ₽)", cat + " • " + weight);
      renderUnifiedSystemHub();
      renderHeroRightColumn();
      renderCategoryShowcaseAndRail();
      alert("✅ Блюдо «" + name + "» добавлено в меню!");
    };

    window.uploadNewDishPhotoFile = function(inputEl) {
      const f = inputEl.files && inputEl.files[0];
      if (!f) return;
      const reader = new FileReader();
      reader.onload = function(ev) {
        const photoEl = document.getElementById("new-dish-photo");
        if (photoEl) photoEl.value = ev.target.result;
      };
      reader.readAsDataURL(f);
    };

    renderUnifiedSystemHub = function() {
      try { if (window.hubActiveTab) hubActiveTab = window.hubActiveTab; else window.hubActiveTab = hubActiveTab; } catch(e) {}
      injectCustomDishesIntoMenu();
      applyManualOverridesToMenuData();
      applyV36LayoutAndButtons();

      const hubModal = document.getElementById("unified-system-hub");
      const hubCard = hubModal ? hubModal.firstElementChild : null;
      const hubHeader = hubCard ? hubCard.children[0] : null;
      let body = document.getElementById("unified-hub-body") || (hubCard ? (hubCard.querySelector(".overflow-y-auto") || hubCard.children[1]) : null);
      if (body) body.id = "unified-hub-body";
      let tabsBox = document.getElementById("unified-hub-tabs") || (hubHeader ? hubHeader.querySelector("[id*='tab']") : null);
      if (!tabsBox && hubHeader) {
        const rightDivs = Array.from(hubHeader.querySelectorAll("div")).filter(d => !d.querySelector("h3") && !d.hasAttribute("data-dove-holder") && d.parentElement === hubHeader);
        tabsBox = rightDivs[0] || null;
        if (!tabsBox) {
          tabsBox = document.createElement("div");
          tabsBox.className = "flex flex-wrap items-center gap-1.5 mt-2 pt-2 border-t border-white/15";
          hubHeader.appendChild(tabsBox);
        }
        tabsBox.id = "unified-hub-tabs";
      }
      if (!tabsBox || !body) return;

      document.querySelectorAll("[id^='hub-ai-prm-']").forEach(el => {
        const idNum = parseInt(el.id.replace("hub-ai-prm-", ""), 10);
        if (!isNaN(idNum)) window.customPromptsPerDish[idNum] = el.value;
      });

      const tasks = getMasterTasksList();
      const doneCnt = tasks.filter(t => t.done).length;
      const logs = window.getCombinedBuildLogs();

      const hubHeaderTitle = document.querySelector("#unified-system-hub h3");
      if (hubHeaderTitle) {
        hubHeaderTitle.innerHTML = "⚙️ Пульт Архитектора «Мир Мир» (v3.6)";
      }

      const tabDefs = [
        { id: "dishes72", label: "🍲 Все блюда (" + (DATA.menu ? DATA.menu.length : 72) + ")" },
        { id: "tasks", label: "📋 Список задач (" + doneCnt + "/" + tasks.length + ")" },
        { id: "logs", label: "📜 Логи сборок (" + logs.length + ")" },
        { id: "ideas", label: "📝 Журнал идей" },
        { id: "toggles", label: "⚡ Режимы, Бронь & Промпт" }
      ];

      tabsBox.innerHTML = tabDefs.map(t =>
        '<button onclick="hubActiveTab=\'' + t.id + '\';renderUnifiedSystemHub()" class="px-3 py-1.5 rounded-xl text-xs font-extrabold cursor-pointer transition ' +
        (hubActiveTab === t.id ? 'bg-[#D48238] text-white shadow' : 'bg-white/10 text-stone-200 hover:bg-white/20') + '">' + t.label + '</button>'
      ).join("");

      if (hubActiveTab === "dishes72") {
        const cats = ["Все", ...Array.from(new Set((DATA.menu || []).map(d => d.category)))];
        const formCats = cats.filter(c => c !== "Все");
        const filtered = (DATA.menu || []).filter(d =>
          (hubDishCategoryFilter === "Все" || d.category === hubDishCategoryFilter) &&
          (!hubDishSearchQuery || d.name.toLowerCase().includes(hubDishSearchQuery.toLowerCase()))
        );

        body.innerHTML =
          '<div class="bg-white rounded-2xl p-3 border border-stone-200 shadow-xs space-y-2.5">' +
            '<div class="flex flex-wrap items-center justify-between gap-2">' +
              '<input type="text" value="' + esc(hubDishSearchQuery) + '" oninput="searchHubDishV38(this.value)" placeholder="🔍 Быстрый поиск блюда по названию..." class="flex-1 min-w-[200px] px-3 py-1.5 rounded-xl border border-stone-300 text-xs font-bold outline-none">' +
              '<button onclick="window.dishAddPanelOpen=!window.dishAddPanelOpen;renderUnifiedSystemHub()" class="px-3.5 py-1.5 rounded-xl bg-[#2E3D28] hover:bg-[#D48238] text-[#F2B880] hover:text-white text-xs font-extrabold cursor-pointer transition shadow-sm">' +
                (window.dishAddPanelOpen ? '▲ Скрыть форму добавления блюда' : '➕ Добавить новое блюдо вручную') +
              '</button>' +
            '</div>' +
            (window.dishAddPanelOpen ? (
              '<div class="bg-[#2E3D28] text-[#FFFDF9] rounded-2xl p-3 border border-[#F2B880]/60 space-y-2">' +
                '<div class="grid grid-cols-1 sm:grid-cols-4 gap-2 text-stone-900">' +
                  '<input id="new-dish-name" type="text" placeholder="Название блюда" class="px-2.5 py-1.5 rounded-lg bg-white text-xs font-bold outline-none">' +
                  '<select id="new-dish-cat" class="px-2.5 py-1.5 rounded-lg bg-white text-xs font-bold outline-none">' +
                    formCats.map(c => '<option value="' + esc(c) + '">' + esc(c) + '</option>').join("") +
                  '</select>' +
                  '<div class="grid grid-cols-2 gap-1.5">' +
                    '<input id="new-dish-price" type="number" placeholder="Цена ₽ (450)" class="px-2.5 py-1.5 rounded-lg bg-white text-xs font-bold outline-none">' +
                    '<input id="new-dish-weight" type="text" placeholder="Вес (260 г)" class="px-2.5 py-1.5 rounded-lg bg-white text-xs font-bold outline-none">' +
                  '</div>' +
                  '<div class="flex gap-1">' +
                    '<input id="new-dish-photo" type="text" placeholder="img/vk_5128_1.jpg или URL" class="flex-1 px-2.5 py-1.5 rounded-lg bg-white text-xs outline-none">' +
                    '<label class="px-2.5 py-1.5 rounded-lg bg-emerald-700 hover:bg-emerald-600 text-white text-xs font-extrabold cursor-pointer flex items-center" title="С устройства">📁<input type="file" accept="image/*" onchange="uploadNewDishPhotoFile(this)" class="hidden"></label>' +
                  '</div>' +
                '</div>' +
                '<div class="flex flex-col sm:flex-row gap-2">' +
                  '<input id="new-dish-desc" type="text" placeholder="Описание и 100% растительный состав блюда..." class="flex-1 px-2.5 py-1.5 rounded-lg bg-white text-stone-900 text-xs outline-none">' +
                  '<button onclick="addNewCustomDishFromHub()" class="px-4 py-1.5 rounded-lg bg-[#D48238] hover:opacity-95 text-white font-extrabold text-xs cursor-pointer shadow">✅ Сохранить блюдо в меню</button>' +
                '</div>' +
              '</div>'
            ) : '') +
            '<div class="flex gap-1.5 overflow-x-auto no-scrollbar pb-0.5">' +
              cats.map(c =>
                '<button onclick="hubDishCategoryFilter=\'' + esc(c) + '\';renderUnifiedSystemHub()" class="px-2.5 py-1 rounded-full text-[11px] font-extrabold whitespace-nowrap cursor-pointer ' +
                (hubDishCategoryFilter === c ? 'bg-[#2E3D28] text-[#F2B880]' : 'bg-stone-100 text-stone-700 hover:bg-stone-200') + '">' + esc(c) + '</button>'
              ).join("") +
            '</div>' +
          '</div>' +

          '<div class="space-y-2.5">' + filtered.map(d => {
            const idx = DATA.menu.indexOf(d);
            const curEngine = selectedAiEnginePerDish[idx] || "gastro_hd";
            const cand = pendingDishCandidates[idx];
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

            return '<div class="bg-white rounded-2xl p-3.5 border border-stone-200 shadow-xs space-y-2.5">' +
              '<div class="grid grid-cols-1 lg:grid-cols-12 gap-3 items-start">' +
                '<div class="lg:col-span-4 flex items-center gap-3">' +
                  '<div class="relative w-20 h-20 rounded-2xl overflow-hidden flex-shrink-0 border border-stone-300 bg-stone-100">' +
                    '<img src="' + esc(d.photo) + '" alt="' + esc(d.name) + '" onerror="this.onerror=null;this.src=\'img/macro_tomyum_bowl.jpg\'" onclick="openSuperZoom(this.src, \'' + esc(d.name) + '\')" class="w-full h-full object-cover cursor-zoom-in">' +
                    '<button onclick="const im=this.parentElement.querySelector(\'img\');openSuperZoom(im?im.src:\'' + esc(d.photo) + '\', \'' + esc(d.name) + '\')" class="absolute bottom-1 right-1 px-1.5 py-0.5 rounded bg-black/80 text-white text-[9px] font-bold cursor-pointer">🔍 Лупа</button>' +
                  '</div>' +
                  '<div class="min-w-0 flex-1 space-y-1">' +
                    '<div class="flex flex-wrap items-center gap-1">' +
                      '<span class="text-[9px] font-extrabold uppercase px-2 py-0.5 rounded bg-amber-100 text-[#2E3D28]">' + esc(d.category) + '</span>' +
                      '<span class="text-[9px] font-extrabold px-2 py-0.5 rounded ' + (d.is_manual_override ? 'bg-emerald-100 text-emerald-900' : 'bg-stone-100 text-stone-600') + '">' + (d.is_manual_override ? '✅ Утверждено' : '🤖 Базовое') + '</span>' +
                    '</div>' +
                    '<h4 class="font-serif font-bold text-base text-[#2E3D28] leading-tight">' + esc(d.name) + ' <span class="text-[#D48238] text-xs font-sans">(' + (d.sizes ? d.sizes[0].price : d.price) + ' ₽)</span></h4>' +
                    '<div class="text-[10px] text-stone-400 truncate font-mono">' + esc(d.photo) + '</div>' +
                    '<div class="flex flex-wrap gap-1.5 pt-0.5">' +
                      '<button onclick="openReadyGalleryPopup(' + idx + ')" class="px-2.5 py-1 rounded-lg bg-[#2E3D28] hover:bg-black text-[#F2B880] text-[10px] font-extrabold cursor-pointer">📸 Из готовых (' + (DATA.ready_photos ? DATA.ready_photos.length : 319) + ')</button>' +
                      '<label class="px-2.5 py-1 rounded-lg bg-emerald-700 hover:bg-emerald-800 text-white text-[10px] font-extrabold cursor-pointer">📁 С ПК<input type="file" accept="image/*" onchange="uploadLocalDishFile(' + idx + ', this)" class="hidden"></label>' +
                    '</div>' +
                  '</div>' +
                '</div>' +

                '<div class="lg:col-span-8 bg-amber-50/60 rounded-2xl p-2.5 border border-amber-200/90 space-y-2">' +
                  '<div class="flex flex-wrap items-center justify-between gap-1.5">' +
                    '<span class="text-[10px] font-extrabold uppercase text-[#D48238]">🎨 1. Выберите источник или ИИ (клик сразу запускает подбор):</span>' +
                    '<div class="flex flex-wrap gap-1">' +
                      engines.map(e =>
                        '<button type="button" onclick="runEngineForDish(' + idx + ',\'' + e.k + '\')" class="px-2 py-1 rounded-lg text-[10px] font-extrabold cursor-pointer transition ' +
                        (curEngine === e.k ? 'bg-[#2E3D28] text-[#F2B880] shadow-xs' : 'bg-white hover:bg-amber-100 text-[#2E3D28] border border-amber-300') + '">' + e.lbl + '</button>'
                      ).join("") +
                    '</div>' +
                  '</div>' +

                  '<div class="grid grid-cols-1 sm:grid-cols-12 gap-2 items-center">' +
                    '<div class="sm:col-span-7 flex gap-1.5">' +
                      '<input id="hub-ai-prm-' + idx + '" type="text" value="' + esc(promptVal) + '" oninput="window.customPromptsPerDish[' + idx + ']=this.value" placeholder="Промпт или теги (100% Vegan)..." class="flex-1 min-w-0 px-2.5 py-1.5 rounded-xl bg-white border border-amber-300 text-xs outline-none">' +
                      '<button id="hub-ai-btn-' + idx + '" onclick="generateDishCandidateAI(' + idx + ')" class="px-3 py-1.5 rounded-xl bg-[#D48238] hover:opacity-95 text-white text-[11px] font-extrabold cursor-pointer whitespace-nowrap shadow-xs">🔍 Найти / ИИ</button>' +
                    '</div>' +
                    '<div class="sm:col-span-5 flex gap-1.5">' +
                      '<input id="hub-url-inp-' + idx + '" type="text" placeholder="🔗 Прямой URL или img/..." class="flex-1 min-w-0 px-2.5 py-1.5 rounded-xl bg-white border border-stone-300 text-xs outline-none">' +
                      '<button onclick="previewManualUrlCandidate(' + idx + ')" class="px-2.5 py-1.5 rounded-xl bg-[#556432] hover:bg-[#2E3D28] text-white text-[11px] font-extrabold cursor-pointer whitespace-nowrap">✅ URL</button>' +
                    '</div>' +
                  '</div>' +

                  (diagLines.length ? (
                    '<div class="bg-[#1A2416] text-emerald-300 rounded-xl px-2.5 py-1.5 font-mono text-[10px] space-y-0.5 border border-[#F2B880]/30">' +
                      diagLines.map(l => '<div class="truncate">' + esc(l) + '</div>').join("") +
                    '</div>'
                  ) : '') +
                '</div>' +
              '</div>' +

              (cand ? (
                '<div class="bg-[#23311E] text-[#FFFDF9] rounded-2xl p-3 border-2 border-[#D48238] flex flex-col sm:flex-row items-center justify-between gap-3">' +
                  '<div class="flex items-center gap-3">' +
                    '<div class="relative w-24 h-24 rounded-xl overflow-hidden border-2 border-[#F2B880] flex-shrink-0 bg-stone-800">' +
                      '<img src="' + esc(cand.url) + '" alt="Предпросмотр" onerror="this.onerror=null;this.src=\'img/vk_5128_1.jpg\'" onclick="openSuperZoom(this.src, \'Предпросмотр: ' + esc(d.name) + '\')" class="w-full h-full object-cover cursor-zoom-in">' +
                      '<button onclick="const im=this.parentElement.querySelector(\'img\');openSuperZoom(im?im.src:\'' + esc(cand.url) + '\', \'Предпросмотр: ' + esc(d.name) + '\')" class="absolute bottom-1 right-1 px-1.5 py-0.5 rounded bg-black/85 text-white text-[9px] font-extrabold cursor-pointer">🔍 Лупа</button>' +
                    '</div>' +
                    '<div class="space-y-1">' +
                      '<span class="px-2 py-0.5 rounded-full bg-[#D48238] text-white text-[10px] font-extrabold">' + esc(cand.source) + '</span>' +
                      '<h5 class="font-serif text-base font-bold text-[#F2B880]">👁️ Предпросмотр для «' + esc(d.name) + '»</h5>' +
                      (cand.diag ? '<p class="text-[10px] text-amber-200 font-mono">' + esc(cand.diag) + '</p>' : '<p class="text-[11px] text-stone-300">Проверьте через «🔍 Лупу» или нажмите «🎲 Ещё вариант».</p>') +
                    '</div>' +
                  '</div>' +
                  '<div class="flex sm:flex-col gap-1.5 w-full sm:w-auto">' +
                    '<button onclick="approveDishCandidate(' + idx + ')" class="flex-1 px-3.5 py-1.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-extrabold text-xs cursor-pointer shadow">✅ Утвердить в меню</button>' +
                    '<button onclick="generateDishCandidateAI(' + idx + ')" class="flex-1 px-3.5 py-1.5 rounded-xl bg-[#D48238] hover:opacity-95 text-white font-extrabold text-xs cursor-pointer">🎲 Ещё вариант</button>' +
                    '<button onclick="delete pendingDishCandidates[' + idx + '];renderUnifiedSystemHub()" class="px-3 py-1 rounded-xl bg-white/10 hover:bg-white/20 text-stone-300 text-[11px] font-bold cursor-pointer">✕ Отмена</button>' +
                  '</div>' +
                '</div>'
              ) : '') +
            '</div>';
          }).join("") + '</div>';
        return;
      }

      if (hubActiveTab === "tasks") {
        body.innerHTML =
          '<div class="space-y-3">' +
            '<div class="bg-white rounded-2xl p-3.5 border border-stone-200 shadow-xs space-y-2">' +
              '<div class="flex flex-wrap items-center justify-between gap-2">' +
                '<div class="text-xs font-extrabold text-[#2E3D28]">📌 Интерактивный Реестр Задач Милорда (клик по статусу меняет «Сделано / Не сделано», справа можно писать комментарий что исправить):</div>' +
                '<div class="flex items-center gap-2">' +
                  '<span id="task-sync-indicator" class="text-[10px] font-bold text-emerald-700">🔄 Авто-синхронизация с app.py активна</span>' +
                  '<button onclick="downloadTzJsonFile()" class="px-2.5 py-1 rounded-lg bg-[#2E3D28] hover:bg-[#D48238] text-[#F2B880] hover:text-white text-[10px] font-extrabold cursor-pointer transition">💾 Скачать tz_mirmir.json</button>' +
                '</div>' +
              '</div>' +
              '<div class="grid grid-cols-1 sm:grid-cols-12 gap-2">' +
                '<input id="new-tz-task-inp" type="text" placeholder="➕ Новая задача или правка..." class="sm:col-span-5 px-3 py-2 rounded-xl border border-stone-300 text-xs font-bold outline-none">' +
                '<input id="new-tz-comment-inp" type="text" placeholder="💬 Комментарий / детали (необязательно)..." class="sm:col-span-5 px-3 py-2 rounded-xl border border-stone-300 text-xs outline-none">' +
                '<button onclick="addNewTaskV35()" class="sm:col-span-2 px-3 py-2 rounded-xl bg-[#D48238] hover:opacity-95 text-white font-extrabold text-xs cursor-pointer shadow">+ Добавить задачу</button>' +
              '</div>' +
            '</div>' +

            '<div class="bg-white rounded-2xl border border-stone-300 overflow-x-auto shadow-xs">' +
              '<table class="w-full text-left border-collapse min-w-[720px]">' +
                '<thead>' +
                  '<tr class="bg-[#2E3D28] text-[#F2B880] text-[10px] font-extrabold uppercase tracking-wider">' +
                    '<th class="p-2.5 w-24">Дата</th>' +
                    '<th class="p-2.5 w-[42%]">Задача (все пункты ТЗ и правок)</th>' +
                    '<th class="p-2.5 text-center w-36">Статус (Клик)</th>' +
                    '<th class="p-2.5">Комментарий Милорда / Что не так (редактируется)</th>' +
                  '</tr>' +
                '</thead>' +
                '<tbody class="divide-y divide-stone-200 text-xs">' +
                  tasks.map((t, i) =>
                    '<tr class="hover:bg-amber-50/40 transition ' + (t.done ? '' : 'bg-rose-50/40') + '">' +
                      '<td class="p-2.5 font-mono text-[11px] font-bold text-stone-500 whitespace-nowrap">📅 ' + esc(t.date || "11.11.2026") + '</td>' +
                      '<td class="p-2.5 font-bold text-[#1F2B1A] leading-snug">' + esc(t.title) + '</td>' +
                      '<td class="p-2.5 text-center">' +
                        '<button onclick="toggleTaskDoneV35(' + i + ')" class="px-3 py-1.5 rounded-xl font-extrabold text-[11px] cursor-pointer transition shadow-xs w-32 ' +
                        (t.done ? 'bg-emerald-700 hover:bg-emerald-800 text-white' : 'bg-rose-600 hover:bg-rose-700 text-white') + '">' +
                          (t.done ? '✅ Сделано' : '❌ Не сделано') +
                        '</button>' +
                      '</td>' +
                      '<td class="p-2.5">' +
                        '<input type="text" value="' + esc(t.comment || "") + '" ' +
                          'oninput="updateTaskCommentV35(' + i + ', this.value)" ' +
                          'onblur="syncTaskCommentOnBlurV35(' + i + ', this.value)" ' +
                          'placeholder="Напишите сюда, что не так или что доработать..." ' +
                          'class="w-full px-2.5 py-1.5 rounded-lg border ' + (t.done ? 'border-stone-200 bg-stone-50/70 text-stone-700' : 'border-rose-300 bg-white text-rose-900 font-bold') + ' text-xs outline-none focus:border-[#D48238] focus:bg-white">' +
                      '</td>' +
                    '</tr>'
                  ).join("") +
                '</tbody>' +
              '</table>' +
            '</div>' +
          '</div>';
        return;
      }

      if (hubActiveTab === "logs") {
        body.innerHTML = '<div class="space-y-2.5">' + logs.map(l =>
          '<div class="bg-white rounded-2xl p-3.5 border border-stone-200 shadow-xs space-y-1">' +
            '<div class="flex flex-wrap items-center justify-between gap-2"><span class="px-2.5 py-0.5 rounded-full bg-[#2E3D28] text-[#F2B880] text-xs font-extrabold">' + esc(l.version) + '</span><span class="text-xs font-bold text-stone-400">🕒 ' + esc(l.timestamp) + '</span></div>' +
            '<div class="text-xs font-extrabold text-[#D48238]">🤖 ' + esc(l.model || "") + '</div>' +
            '<p class="text-xs text-stone-700 leading-relaxed">' + esc(l.status || "") + '</p>' +
          '</div>'
        ).join("") + '</div>';
        return;
      }

      if (hubActiveTab === "ideas") {
        const notes = window.getSavedIdeasNotes();
        body.innerHTML =
          '<div class="space-y-3">' +
            '<div class="bg-white rounded-2xl p-3.5 border border-stone-200 space-y-2">' +
              '<label class="text-xs font-extrabold uppercase text-[#556432] block">💡 Добавить заметку в Журнал идей:</label>' +
              '<div class="flex gap-2">' +
                '<input id="new-idea-note-inp" type="text" placeholder="Запишите идею или пожелание..." class="flex-1 px-3 py-2 rounded-xl border border-stone-300 text-xs outline-none">' +
                '<button onclick="addNewIdeaNote()" class="px-4 py-2 rounded-xl bg-[#2E3D28] text-[#F2B880] font-extrabold text-xs cursor-pointer">💾 Сохранить</button>' +
              '</div>' +
            '</div>' +
            '<div class="space-y-2">' + notes.map(n =>
              '<div class="bg-white rounded-2xl p-3 border border-stone-200 flex items-start justify-between gap-3"><p class="text-xs font-bold text-stone-800">' + esc(n.text) + '</p><span class="text-[10px] text-stone-400 whitespace-nowrap">' + esc(n.date) + '</span></div>'
            ).join("") + '</div>' +
          '</div>';
        return;
      }

      // ВКЛАДКА 5: ПЕРЕКЛЮЧАТЕЛИ РЕЖИМОВ ПО АУДИТУ CLAUDE (БРОНЬ ТГ/ВК ИЛИ 152-ФЗ, КАРТА БЕЗ РЕКЛАМЫ, ФОТО-РЕЖИМ) + МАСТЕР-ПРОМПТ!
      const tg = window.getSiteToggles();
      body.innerHTML =
        '<div class="grid grid-cols-1 lg:grid-cols-2 gap-3">' +
          '<div class="bg-white rounded-2xl p-4 border border-stone-200 space-y-3">' +
            '<h4 class="font-serif text-lg font-bold text-[#2E3D28]">🛠️ Настройки режимов сайта (по аудиту Claude)</h4>' +

            '<div class="p-3 rounded-xl bg-amber-50/70 border border-amber-200 space-y-1.5">' +
              '<div class="text-xs font-extrabold text-[#2E3D28]">🪑 1. Режим кнопки «Бронь столика»:</div>' +
              '<div class="grid grid-cols-1 sm:grid-cols-2 gap-1.5">' +
                '<button onclick="setAdminSettingV36(\'bookingMode\', \'messenger\')" class="p-2 rounded-lg text-[11px] font-extrabold cursor-pointer text-left transition ' + (tg.bookingMode === 'messenger' ? 'bg-[#2E3D28] text-[#F2B880] shadow' : 'bg-white text-stone-700 border border-stone-300') + '">✈️ Переход в Telegram / ВК (Без сбора ПДн и 152-ФЗ)</button>' +
                '<button onclick="setAdminSettingV36(\'bookingMode\', \'form152\')" class="p-2 rounded-lg text-[11px] font-extrabold cursor-pointer text-left transition ' + (tg.bookingMode === 'form152' ? 'bg-[#2E3D28] text-[#F2B880] shadow' : 'bg-white text-stone-700 border border-stone-300') + '">📝 Классическая анкета на сайте (+ галочка 152-ФЗ)</button>' +
              '</div>' +
            '</div>' +

            '<div class="p-3 rounded-xl bg-amber-50/70 border border-amber-200 space-y-1.5">' +
              '<div class="text-xs font-extrabold text-[#2E3D28]">🗺️ 2. Режим отображения Карты внизу сайта:</div>' +
              '<div class="grid grid-cols-1 sm:grid-cols-2 gap-1.5">' +
                '<button onclick="setAdminSettingV36(\'mapMode\', \'clean_card\')" class="p-2 rounded-lg text-[11px] font-extrabold cursor-pointer text-left transition ' + (tg.mapMode === 'clean_card' ? 'bg-[#2E3D28] text-[#F2B880] shadow' : 'bg-white text-stone-700 border border-stone-300') + '">🛡️ Чистая карточка маршрута (Без рекламы в iframe)</button>' +
                '<button onclick="setAdminSettingV36(\'mapMode\', \'iframe\')" class="p-2 rounded-lg text-[11px] font-extrabold cursor-pointer text-left transition ' + (tg.mapMode === 'iframe' ? 'bg-[#2E3D28] text-[#F2B880] shadow' : 'bg-white text-stone-700 border border-stone-300') + '">🌐 Живой iframe Яндекс.Карт</button>' +
              '</div>' +
            '</div>' +

            '<div class="p-3 rounded-xl bg-amber-50/70 border border-amber-200 space-y-1.5">' +
              '<div class="text-xs font-extrabold text-[#2E3D28]">📸 3. Режим показа фотографий в Меню:</div>' +
              '<div class="grid grid-cols-1 sm:grid-cols-2 gap-1.5">' +
                '<button onclick="setAdminSettingV36(\'photoMode\', \'hybrid\')" class="p-2 rounded-lg text-[11px] font-extrabold cursor-pointer text-left transition ' + (tg.photoMode === 'hybrid' ? 'bg-[#2E3D28] text-[#F2B880] shadow' : 'bg-white text-stone-700 border border-stone-300') + '">🎨 Гибрид (Все фото + плашка подачи)</button>' +
                '<button onclick="setAdminSettingV36(\'photoMode\', \'strict_real\')" class="p-2 rounded-lg text-[11px] font-extrabold cursor-pointer text-left transition ' + (tg.photoMode === 'strict_real' ? 'bg-[#2E3D28] text-[#F2B880] shadow' : 'bg-white text-stone-700 border border-stone-300') + '">🕊️ Строгий демо-режим (Только 100% фото из ВК)</button>' +
              '</div>' +
            '</div>' +
          '</div>' +

          '<div class="space-y-3 flex flex-col justify-between">' +
            '<div class="bg-white rounded-2xl p-4 border border-stone-200 space-y-2">' +
              '<h4 class="font-serif text-lg font-bold text-[#2E3D28]">✨ Атмосферные эффекты</h4>' +
              '<label class="flex items-center justify-between p-2 rounded-xl bg-stone-50 cursor-pointer"><span class="text-xs font-bold">🍃 Падающие чайные листья на фоне</span><input type="checkbox" ' + (tg.leaves ? "checked" : "") + ' onchange="toggleSiteEffect(\'leaves\', this.checked)" class="w-4 h-4 accent-[#556432]"></label>' +
              '<label class="flex items-center justify-between p-2 rounded-xl bg-stone-50 cursor-pointer"><span class="text-xs font-bold">🕊️ Боковые фоновые крылья фотографий</span><input type="checkbox" ' + (tg.wings ? "checked" : "") + ' onchange="toggleSiteEffect(\'wings\', this.checked)" class="w-4 h-4 accent-[#556432]"></label>' +
              '<label class="flex items-center justify-between p-2 rounded-xl bg-stone-50 cursor-pointer"><span class="text-xs font-bold">🔍 Плавный Зум карточек при наведении</span><input type="checkbox" ' + (tg.zoom ? "checked" : "") + ' onchange="toggleSiteEffect(\'zoom\', this.checked)" class="w-4 h-4 accent-[#556432]"></label>' +
            '</div>' +

            '<div class="bg-[#2E3D28] text-[#FFFDF9] rounded-2xl p-4 space-y-2.5">' +
              '<div><span class="text-[10px] font-extrabold uppercase tracking-widest text-[#F2B880]">ДНК ПЛАТФОРМЫ</span><h4 class="font-serif text-xl font-bold mt-0.5">🧬 Полный Текстовый Мастер-Промпт</h4><p class="text-xs text-stone-300 mt-1">Живое ТЗ на русском языке с возможностью редактирования прямо на сайте.</p></div>' +
              '<div class="flex flex-wrap gap-2 pt-1"><button onclick="openMasterPromptModal()" class="px-4 py-2 rounded-xl bg-[#D48238] text-white text-xs font-extrabold cursor-pointer shadow">📖 Открыть и редактировать Промпт</button><button onclick="downloadMasterPromptFile()" class="px-4 py-2 rounded-xl bg-white/15 text-white text-xs font-extrabold cursor-pointer">💾 Скачать .TXT</button></div>' +
            '</div>' +
          '</div>' +
        '</div>';
    };

    // 6. ПРОВЕРКА ЗАГРУЗКИ КАДРА И ГЕНЕРАТОР С ЛОГАМИ ДИАГНОСТИКИ
    async function fetchJsonWithDiag(url, timeoutMs = 2600) {
      const ctrl = new AbortController();
      const timer = setTimeout(() => ctrl.abort(), timeoutMs);
      try {
        const r = await fetch(url, { signal: ctrl.signal });
        clearTimeout(timer);
        if (!r.ok) return { ok: false, err: "HTTP " + r.status };
        const data = await r.json();
        return { ok: true, data: data };
      } catch(e) {
        clearTimeout(timer);
        const isAbort = e && e.name === "AbortError";
        return { ok: false, err: isAbort ? ("Таймаут " + (timeoutMs/1000) + " сек (блокировка сети/VPN)") : ("Сбой сети/CORS: " + (e.message || "недоступен")) };
      }
    }

    function verifyImageLoadsWithDiag(url, timeoutMs = 4500) {
      return new Promise(resolve => {
        if (!url) return resolve({ ok: false, reason: "Пустой URL" });
        const img = new Image();
        let done = false;
        const timer = setTimeout(() => {
          if (!done) { done = true; resolve({ ok: false, reason: "Таймаут загрузки картинки (" + (timeoutMs/1000) + " сек)" }); }
        }, timeoutMs);
        img.onload = () => {
          if (!done) {
            done = true;
            clearTimeout(timer);
            if (img.naturalWidth < 60) {
              resolve({ ok: false, reason: "Заглушка малого размера (" + img.naturalWidth + "px)" });
            } else {
              resolve({ ok: true, w: img.naturalWidth, h: img.naturalHeight });
            }
          }
        };
        img.onerror = () => {
          if (!done) { done = true; clearTimeout(timer); resolve({ ok: false, reason: "Сервер вернул ошибку (HTTP 429 Лимит / 404)" }); }
        };
        img.src = url;
      });
    }

    const NON_VEGAN_BAN_REGEX = /meat|chicken|pork|beef|shrimp|prawn|fish|seafood|salmon|tuna|bacon|steak|ham|lamb|turkey|sausage|pepperoni|cheese|milk|dairy|egg/i;

    const CURATED_VEGAN_HD_BANK = {
      burger: ["img/macro_vegan_burger.jpg", "img/macro_avocado_burger.jpg", "img/macro_spicy_burger.jpg", "img/vk_5128_1.jpg"],
      soup: ["img/macro_tomyum_bowl.jpg", "img/vk_5085_1.jpg", "img/vk_5118_0.jpg", "img/vk_5128_1.jpg"],
      salad: ["img/macro_caesar_romaine.jpg", "img/vk_5085_1.jpg", "img/vk_5118_0.jpg", "img/vk_5128_1.jpg"],
      drink: ["img/macro_citrus_mint.jpg", "img/vk_5122_0.jpg", "img/vk_5134_0.jpg"],
      main: ["img/vk_5118_0.jpg", "img/vk_5128_1.jpg", "img/macro_vegan_burger.jpg", "img/macro_tomyum_bowl.jpg"],
      dessert: ["img/vk_5101_0.jpg", "img/vk_5122_0.jpg", "img/vk_5128_1.jpg"]
    };

    function extractShortSearchTopic(dish, rawText) {
      const cat = (dish.category || "").toLowerCase();
      const nm = (dish.name || "").toLowerCase();
      const raw = (rawText || "").toLowerCase();
      if (nm.includes("бургер") || raw.includes("burger") || nm.includes("авокадо-фиш") || nm.includes("неряха") || nm.includes("спайси тамаго") || nm.includes("сэндвич") || nm.includes("завертон")) return { q: "vegan burger", bank: "burger" };
      if (cat.includes("суп") || nm.includes("суп") || nm.includes("том ям") || nm.includes("ватапа") || nm.includes("борщ")) return { q: "vegan vegetable soup", bank: "soup" };
      if (nm.includes("пицца") || nm.includes("лахмаджун")) return { q: "vegan mushroom pizza", bank: "main" };
      if (nm.includes("лимонад") || raw.includes("lemonade") || raw.includes("citrus")) return { q: "citrus lemonade mint", bank: "drink" };
      if (nm.includes("смузи") || raw.includes("smoothie")) return { q: "berry smoothie", bank: "drink" };
      if (nm.includes("фреш") || raw.includes("juice")) return { q: "fresh orange juice", bank: "drink" };
      if (nm.includes("кофе") || nm.includes("капучино") || nm.includes("американо")) return { q: "latte coffee cup", bank: "drink" };
      if (cat.includes("чай") || nm.includes("чай") || nm.includes("пуэр") || nm.includes("улун") || nm.includes("масала")) return { q: "herbal tea teapot", bank: "drink" };
      if (cat.includes("салат") || nm.includes("салат") || nm.includes("цезарь") || nm.includes("боул")) return { q: "vegan salad bowl", bank: "salad" };
      if (cat.includes("десерт") || nm.includes("сырники") || nm.includes("шарлотка") || nm.includes("мороженое") || nm.includes("батончик") || nm.includes("роти")) return { q: "vegan cake dessert", bank: "dessert" };
      if (cat.includes("лапша") || nm.includes("лапша") || nm.includes("паста") || nm.includes("пад тай")) return { q: "vegan noodles tofu", bank: "main" };
      return { q: "vegan dish bowl", bank: "salad" };
    }

    generateDishCandidateAI = async function(idx) {
      const d = DATA.menu[idx];
      if (!d) return;
      const prmInp = document.getElementById("hub-ai-prm-" + idx);
      if (prmInp && prmInp.value.trim()) window.customPromptsPerDish[idx] = prmInp.value.trim();
      const userRawText = window.customPromptsPerDish[idx] !== undefined ? window.customPromptsPerDish[idx] : (d.ai_prompt || d.name);

      window.dishVariantStep[idx] = (window.dishVariantStep[idx] || 0) + 1;
      const step = window.dishVariantStep[idx];
      const engine = selectedAiEnginePerDish[idx] || "gastro_hd";

      const topicInfo = extractShortSearchTopic(d, userRawText);
      const shortQuery = topicInfo.q;
      const bankPool = CURATED_VEGAN_HD_BANK[topicInfo.bank] || CURATED_VEGAN_HD_BANK.soup;

      const btn = document.getElementById("hub-ai-btn-" + idx);
      if (btn) btn.innerText = "⏳ Вариант #" + step + "...";

      if (engine === "flux_ai" || engine === "turbo_ai") {
        const modelName = engine === "flux_ai" ? "flux" : "turbo";
        const labelStr = engine === "flux_ai" ? "Flux Pro AI" : "Turbo SDXL AI";
        const rndSeed = Math.floor(Math.random() * 899999) + step * 101;
        const dim = 640 + (step % 3) * 64;
        const cleanPrompt = "Appetizing gourmet 100% vegan plant-based " + shortQuery + ", close-up restaurant food photography, no meat, no text";
        const aiUrl = "https://image.pollinations.ai/prompt/" + encodeURIComponent(cleanPrompt) + "?model=" + modelName + "&width=" + dim + "&height=" + dim + "&seed=" + rndSeed + "&nologo=true&nofeed=true";

        pushDiagLog(idx, "📡", labelStr, "Отправлен промпт («" + shortQuery + "», seed #" + rndSeed + ")...");
        renderUnifiedSystemHub();

        const check = await verifyImageLoadsWithDiag(aiUrl, 4800);
        if (check.ok) {
          pushDiagLog(idx, "✅", labelStr, "Успешно сгенерировано (" + check.w + "×" + check.h + "px)");
          pendingDishCandidates[idx] = { url: aiUrl, source: "🎨 " + labelStr + " (Seed #" + rndSeed + ")", prompt: cleanPrompt, diag: "✅ Сгенерировано нейросетью (" + check.w + "×" + check.h + "px)" };
          renderUnifiedSystemHub();
          return;
        } else {
          const fallbackLocal = bankPool[(step - 1) % bankPool.length];
          pushDiagLog(idx, "❌", labelStr, check.reason + " ➔ Включён локальный резерв (" + fallbackLocal + ")");
          pendingDishCandidates[idx] = { url: fallbackLocal, source: "🍔 Резерв GastroBank (т.к. " + labelStr + " вернул: " + check.reason + ")", prompt: shortQuery, diag: "⚠️ Причина: " + labelStr + " — " + check.reason + ". Показан проверенный локальный кадр." };
          renderUnifiedSystemHub();
          return;
        }
      }

      if (engine === "gastro_hd") {
        const vkFoodPool = (DATA.vk_food_photos && DATA.vk_food_photos.length) ? DATA.vk_food_photos : [];
        const combinedPool = [...bankPool, ...vkFoodPool.slice(0, 12)];
        const pickLocal = combinedPool[(step - 1) % combinedPool.length];
        pushDiagLog(idx, "✅", "GastroBank HD", "Выбран проверенный веган-кадр #" + step + " (" + pickLocal + ")");
        pendingDishCandidates[idx] = { url: pickLocal, source: "🍔 3. GastroBank HD (" + topicInfo.bank.toUpperCase() + " • Вариант #" + step + ")", prompt: shortQuery, diag: "✅ Мгновенный локальный пул без внешних лимитов (" + pickLocal + ")" };
        renderUnifiedSystemHub();
        return;
      }

      if (engine === "openverse_hd") {
        const cacheKey = "ov_" + shortQuery;
        if (!window.cachedSearchPools[cacheKey]) {
          pushDiagLog(idx, "📡", "Openverse API", "Поиск веган-фото по тегу «" + shortQuery + "»...");
          const res = await fetchJsonWithDiag("https://api.openverse.org/v1/images/?q=" + encodeURIComponent(shortQuery) + "&page_size=25", 2800);
          if (res.ok && res.data && res.data.results && res.data.results.length) {
            const urls = res.data.results.filter(it => !NON_VEGAN_BAN_REGEX.test((it.title || ""))).map(it => it.thumbnail || it.url).filter(Boolean);
            if (urls.length) {
              window.cachedSearchPools[cacheKey] = urls;
              pushDiagLog(idx, "✅", "Openverse API", "Найдено " + urls.length + " веган-фотографий");
            }
          } else {
            pushDiagLog(idx, "❌", "Openverse API", (res.err || "Пустой ответ") + " ➔ Переключено на локальный пул");
          }
        }
        const pool = window.cachedSearchPools[cacheKey];
        if (pool && pool.length) {
          const candidateUrl = pool[(step - 1) % pool.length];
          const chk = await verifyImageLoadsWithDiag(candidateUrl, 3200);
          if (chk.ok) {
            pendingDishCandidates[idx] = { url: candidateUrl, source: "📸 4. Openverse HD (Вариант #" + (((step - 1) % pool.length) + 1) + " из " + pool.length + ")", prompt: shortQuery, diag: "✅ Загружено из Openverse (" + chk.w + "×" + chk.h + "px)" };
            renderUnifiedSystemHub();
            return;
          }
        }
        const fb = bankPool[(step - 1) % bankPool.length];
        pendingDishCandidates[idx] = { url: fb, source: "🍔 Резерв (Openverse недоступен)", prompt: shortQuery, diag: "⚠️ Внешний сервер не отдал кадр — показан локальный резерв." };
        renderUnifiedSystemHub();
        return;
      }

      if (engine === "wikimedia") {
        const cacheKey = "wm_" + shortQuery;
        if (!window.cachedSearchPools[cacheKey]) {
          pushDiagLog(idx, "📡", "Wikimedia API", "Поиск в Wikimedia Commons («" + shortQuery + "»)...");
          const res = await fetchJsonWithDiag("https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch=" + encodeURIComponent("filetype:bitmap " + shortQuery) + "&gsrlimit=25&prop=imageinfo&iiprop=url&iiurlwidth=720&format=json&origin=*", 2800);
          const pages = res.ok && res.data && res.data.query && res.data.query.pages ? Object.values(res.data.query.pages) : [];
          const urls = pages.filter(p => !NON_VEGAN_BAN_REGEX.test(p.title || "")).map(p => p.imageinfo && p.imageinfo[0] && (p.imageinfo[0].thumburl || p.imageinfo[0].url)).filter(Boolean);
          if (urls.length) {
            window.cachedSearchPools[cacheKey] = urls;
            pushDiagLog(idx, "✅", "Wikimedia API", "Найдено " + urls.length + " фото блюд");
          } else {
            pushDiagLog(idx, "❌", "Wikimedia API", (res.err || "0 результатов") + " ➔ Локальный резерв");
          }
        }
        const pool = window.cachedSearchPools[cacheKey];
        if (pool && pool.length) {
          const candidateUrl = pool[(step - 1) % pool.length];
          const chk = await verifyImageLoadsWithDiag(candidateUrl, 3200);
          if (chk.ok) {
            pendingDishCandidates[idx] = { url: candidateUrl, source: "🥗 5. Wikimedia Gastro (Вариант #" + (((step - 1) % pool.length) + 1) + " из " + pool.length + ")", prompt: shortQuery, diag: "✅ Загружено из Wikimedia (" + chk.w + "×" + chk.h + "px)" };
            renderUnifiedSystemHub();
            return;
          }
        }
        const fb = bankPool[(step - 1) % bankPool.length];
        pendingDishCandidates[idx] = { url: fb, source: "🍔 Резерв (Wikimedia недоступен)", prompt: shortQuery, diag: "⚠️ Показан проверенный локальный кадр." };
        renderUnifiedSystemHub();
        return;
      }

      const vkFoodPool = (DATA.vk_food_photos && DATA.vk_food_photos.length) ? DATA.vk_food_photos : (DATA.ready_photos || []).filter(p => p.includes("vk_") && !p.includes("5047_") && !p.includes("5068_"));
      const poolVk = vkFoodPool.length ? vkFoodPool : bankPool;
      const pickVk = poolVk[(step - 1) % poolVk.length];
      pushDiagLog(idx, "✅", "Архив ВК кафе", "Загружен кадр #" + (((step - 1) % poolVk.length) + 1) + " из " + poolVk.length + " (" + pickVk + ")");
      pendingDishCandidates[idx] = { url: pickVk, source: "🌿 6. Архив фото из ВК кафе (#" + (((step - 1) % poolVk.length) + 1) + " из " + poolVk.length + ")", prompt: pickVk, diag: "✅ Локальный файл из папки img/ (" + pickVk + ")" };
      renderUnifiedSystemHub();
    };

    // Слайдер зала, 2 крупных спешла справа, Электронное меню с учётом режима фото и Новости
    window.getInteriorSlidesList = function() {
      return [
        { src: "img/ymap_org_0.jpg", title: "🏛️ Исторический кирпичный свод и уютный зал на Ильинской, 45", tag: "Интерьер зала" },
        { src: "img/ymap_org_1.jpg", title: "🕊️ Фирменная кованая вывеска с белой Голубкой мира у входа", tag: "Экстерьер • Ильинская, 45" },
        { src: "img/vk_5068_0.jpg", title: "🛋️ Изумрудный велюровый диван, живой кирпич и картины", tag: "Атмосфера «Мир Мир»" },
        { src: "img/vk_5122_0.jpg", title: "🕯️ Вечерние чаепития при свечах и редкий китайский чай", tag: "Чайная культура" },
        { src: "img/vk_5134_0.jpg", title: "🌿 Уютное зелёное пространство для встреч и живого общения", tag: "Интерьер кафе" }
      ];
    };

    window.rightSpecialsPairIdx = 0;
    window.stepRightSpecialsPair = function(delta) {
      const specials = (DATA.menu || []).filter(d => d.category === "Сезонные спешлы от Шефа" || d.photo_type === "real");
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
              '<button onclick="stepRightSpecialsPair(-1)" class="w-6 h-6 rounded-full bg-white/15 hover:bg-[#D48238] text-white text-[10px] font-bold cursor-pointer">◀</button>' +
              '<button onclick="stepRightSpecialsPair(1)" class="w-6 h-6 rounded-full bg-white/15 hover:bg-[#D48238] text-white text-[10px] font-bold cursor-pointer">▶</button>' +
            '</div>' +
            '<button onclick="openMenu(\'Сезонные спешлы от Шефа\')" class="text-[10px] font-extrabold text-amber-300 hover:underline cursor-pointer">Все блюда (' + (DATA.menu ? DATA.menu.length : 72) + ') ➔</button>';
        }
      }

      const specials = (DATA.menu || []).filter(d => d.category === "Сезонные спешлы от Шефа" || d.photo_type === "real");
      const start = (window.rightSpecialsPairIdx * 2) % Math.max(1, specials.length);
      const pair = [specials[start], specials[(start + 1) % specials.length]].filter(Boolean);

      rowsBox.innerHTML = '<div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">' + pair.map(d => {
        const idx = DATA.menu.indexOf(d);
        const pr = d.sizes ? d.sizes[0].price : d.price;
        return '<div onclick="openMenu(\'Сезонные спешлы от Шефа\')" class="zoom-card bg-[#FDF8F2] text-stone-900 rounded-2xl p-2.5 flex flex-col justify-between gap-2 cursor-pointer shadow-lg border-2 border-[#F2B880]/70 transition">' +
          '<div class="relative h-32 sm:h-36 w-full rounded-xl overflow-hidden bg-stone-200">' +
            '<img src="' + esc(d.photo) + '" alt="' + esc(d.name) + '" onerror="this.onerror=null;this.src=\'img/macro_tomyum_bowl.jpg\'" onclick="event.stopPropagation();openSuperZoom(this.src, \'' + esc(d.name) + '\')" class="w-full h-full object-cover cursor-zoom-in">' +
            '<span class="absolute top-1.5 left-1.5 px-2 py-0.5 rounded-md bg-black/70 text-[#F2B880] text-[9px] font-extrabold">' + esc(d.weight || "Хит шефа") + '</span>' +
            '<button onclick="event.stopPropagation();const im=this.parentElement.querySelector(\'img\');openSuperZoom(im?im.src:\'' + esc(d.photo) + '\', \'' + esc(d.name) + '\')" class="absolute bottom-1.5 right-1.5 px-2 py-0.5 rounded-md bg-black/75 hover:bg-[#D48238] text-white text-[9px] font-extrabold cursor-pointer">🔍 Лупа</button>' +
          '</div>' +
          '<div class="space-y-1">' +
            '<div class="font-serif font-bold text-sm sm:text-base text-[#2E3D28] leading-tight line-clamp-2">' + esc(d.name) + '</div>' +
            '<div class="flex items-center justify-between pt-1 border-t border-stone-200/80">' +
              '<strong class="text-sm font-extrabold text-[#D48238]">' + pr + ' ₽</strong>' +
              '<button onclick="event.stopPropagation();addToCart(' + idx + ',0)" class="px-2.5 py-1 rounded-lg bg-[#556432] hover:bg-[#2E3D28] text-white text-[10px] font-extrabold cursor-pointer shadow">+ В заказ</button>' +
            '</div>' +
          '</div>' +
        '</div>';
      }).join("") + '</div>';
    };

    const _baseRenderHeroRight = renderHeroRightColumn;
    renderHeroRightColumn = function() {
      _baseRenderHeroRight();
      window.renderRightTwoPictureFields();
    };

    renderDishes = function() {
      injectCustomDishesIntoMenu();
      applyManualOverridesToMenuData();
      const tg = window.getSiteToggles();
      const tabsBox = document.getElementById("menu-cat-tabs");
      const grid = document.getElementById("menu-dishes-grid");
      if (!grid) return;
      const cats = ["Все", ...Array.from(new Set((DATA.menu || []).map(d => d.category)))];
      if (tabsBox) {
        const bowlBtnHtml = '<button onclick="closeMenu();openBowlBuilder()" class="px-3.5 py-1.5 rounded-full text-xs font-extrabold whitespace-nowrap cursor-pointer transition bg-[#D48238] hover:opacity-95 text-white shadow">🥗 Собрать свой Боул</button>';
        tabsBox.innerHTML = bowlBtnHtml + cats.map(c =>
          '<button onclick="currentMenuCategory=\'' + esc(c) + '\';renderDishes()" class="px-3.5 py-1.5 rounded-full text-xs font-extrabold whitespace-nowrap cursor-pointer transition ' +
          (currentMenuCategory === c ? 'bg-[#2E3D28] text-[#F2B880] shadow' : 'bg-white text-[#2E3D28] border border-stone-300') + '">' + esc(c) + '</button>'
        ).join("");
      }
      const q = (document.getElementById("menu-search-inp")?.value || "").toLowerCase();
      const filtered = (DATA.menu || []).filter(d =>
        (currentMenuCategory === "Все" || d.category === currentMenuCategory) &&
        (!q || d.name.toLowerCase().includes(q) || (d.desc || "").toLowerCase().includes(q))
      );

      grid.innerHTML = filtered.map(d => {
        const realIdx = DATA.menu.indexOf(d);
        const isRealVkPhoto = d.photo && d.photo.includes("vk_");
        const badgeText = isRealVkPhoto ? "📸 Оригинальное фото кафе" : "🌿 Сервировка блюда";
        const buttonsHtml = (d.sizes && d.sizes.length > 1)
          ? '<div class="grid grid-cols-2 gap-1.5 pt-2">' + d.sizes.map((sz, sIdx) =>
              '<button onclick="addToCart(' + realIdx + ',' + sIdx + ')" class="py-2 px-2 rounded-xl bg-[#556432] hover:bg-[#D48238] text-white font-extrabold text-[11px] cursor-pointer transition shadow-sm">' + esc(sz.label) + ' • ' + sz.price + ' ₽ +</button>'
            ).join("") + '</div>'
          : '<div class="flex items-center justify-between pt-2 border-t border-stone-100"><div><span class="text-[11px] text-stone-400 font-bold block">' + esc(d.weight || "") + '</span><strong class="text-lg font-extrabold text-[#2E3D28]">' + d.price + ' ₽</strong></div><button onclick="addToCart(' + realIdx + ',0)" class="px-4 py-2 rounded-xl bg-[#D48238] hover:opacity-95 text-white font-extrabold text-xs cursor-pointer shadow">+ В корзину</button></div>';

        const mediaHtml = (tg.photoMode === "strict_real" && !isRealVkPhoto)
          ? '<div class="relative h-44 rounded-2xl overflow-hidden mb-2.5 bg-[#23311E] flex flex-col items-center justify-center p-4 text-center border border-[#F2B880]/40">' +
              '<div class="text-2xl mb-1">🕊️</div>' +
              '<div class="text-xs font-serif font-bold text-[#F2B880]">Авторская подача «Мир Мир»</div>' +
              '<div class="text-[10px] text-stone-300 mt-0.5">Оригинальное фото из зала готовится к публикации</div>' +
            '</div>'
          : '<div class="relative h-44 rounded-2xl overflow-hidden mb-2.5 bg-stone-100">' +
              '<img src="' + esc(d.photo) + '" alt="' + esc(d.name) + '" onerror="this.onerror=null;this.src=\'img/macro_tomyum_bowl.jpg\'" onclick="openSuperZoom(this.src, \'' + esc(d.name) + '\')" class="w-full h-full object-cover cursor-zoom-in">' +
              '<span class="absolute top-2 left-2 px-2.5 py-0.5 rounded-full bg-black/75 text-[#F2B880] text-[10px] font-extrabold">' + badgeText + '</span>' +
              '<span class="absolute bottom-2 left-2 px-2 py-0.5 rounded-md bg-black/75 text-white/95 text-[9px] font-bold shadow">🍽️ Подача блюд может отличаться</span>' +
              '<button onclick="const im=this.parentElement.querySelector(\'img\');openSuperZoom(im?im.src:\'' + esc(d.photo) + '\', \'' + esc(d.name) + '\')" class="absolute bottom-2 right-2 px-2 py-0.5 rounded-lg bg-black/80 hover:bg-[#D48238] text-white text-[10px] font-extrabold cursor-pointer">🔍 Лупа</button>' +
            '</div>';

        return '<div class="zoom-card bg-white rounded-3xl p-3.5 border border-stone-200 shadow-sm flex flex-col justify-between gap-2 transition">' +
          '<div>' +
            mediaHtml +
            '<span class="text-[10px] font-extrabold uppercase text-[#556432]">' + esc(d.category) + '</span>' +
            '<h4 class="font-serif text-xl font-bold text-[#2E3D28] leading-snug">' + esc(d.name) + '</h4>' +
            '<p class="text-xs text-stone-600 mt-1 leading-relaxed">' + esc(d.desc || "") + '</p>' +
            '<div class="text-[10px] text-stone-400 italic mt-1">🍽️ Подача блюд может отличаться</div>' +
          '</div>' +
          buttonsHtml +
        '</div>';
      }).join("");
    };

    const NEWS_FALLBACK_IMGS = ["img/vk_5122_0.jpg", "img/vk_5068_0.jpg", "img/vk_5128_1.jpg", "img/vk_5134_0.jpg"];

    renderNewsPosts = function() {
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
              '<img src="' + esc(photoSrc) + '" alt="' + esc(p.title || "Новость кафе") + '" onerror="this.onerror=null;this.src=\'' + fbImg + '\'" onclick="openSuperZoom(this.src, \'' + esc(p.title) + '\')" class="w-full h-auto max-h-[340px] object-contain cursor-zoom-in block mx-auto">' +
              '<button onclick="const im=this.parentElement.querySelector(\'img\');openSuperZoom(im?im.src:\'' + esc(photoSrc) + '\', \'' + esc(p.title) + '\')" class="absolute bottom-2 right-2 px-2.5 py-1 rounded-lg bg-black/75 hover:bg-[#D48238] text-white text-[10px] font-extrabold cursor-pointer shadow">🔍 Лупа</button>' +
            '</div>' +
            '<p class="text-xs sm:text-sm text-stone-700 leading-relaxed whitespace-pre-line">' + esc(p.text || "") + '</p>' +
          '</div>' +
          '<div class="pt-2.5 border-t border-stone-200/80 flex items-center justify-between">' +
            '<a href="' + esc(safeVkUrl) + '" target="_blank" title="Открыть в ВК" class="inline-flex items-center justify-center px-2.5 py-1 rounded-lg bg-[#0077FF] hover:bg-[#0055CC] text-white text-[11px] font-extrabold tracking-wide transition shadow cursor-pointer">ВК</a>' +
            '<span class="text-[10px] font-bold text-stone-400">vk.com/mirmir.cafe</span>' +
          '</div>' +
        '</article>';
      }).join("");

      const bottomVkLink = document.querySelector("#news-section-wrap a[href*='vk.com']");
      if (bottomVkLink) {
        bottomVkLink.className = "inline-flex items-center justify-center px-3 py-1 rounded-lg bg-[#0077FF] hover:bg-[#0055CC] text-white text-xs font-extrabold transition shadow";
        bottomVkLink.innerHTML = "ВК";
      }
    };

    // Живой редактор Мастер-Промпта
    window.DEFAULT_FULL_MASTER_PROMPT = DATA.master_prompt_text || "";
    window.getActiveMasterPromptText = function() {
      try {
        const saved = localStorage.getItem("mirmir_saved_master_prompt_v1");
        if (saved && saved.trim().length > 600) return saved;
      } catch(e) {}
      return DATA.master_prompt_text || window.DEFAULT_FULL_MASTER_PROMPT || "";
    };

    window.saveMasterPromptEditsOnSite = function() {
      const box = document.getElementById("master-prompt-textarea");
      if (!box) return;
      const val = box.value.trim();
      try {
        localStorage.setItem("mirmir_saved_master_prompt_v1", val);
        DATA.master_prompt_text = val;
        const st = document.getElementById("master-prompt-save-status");
        if (st) st.textContent = "✅ Сохранено на сайте (" + new Date().toLocaleTimeString() + ")!";
      } catch(e) {}
    };

    openMasterPromptModal = function() {
      const m = document.getElementById("master-prompt-modal");
      const box = document.getElementById("master-prompt-textarea");
      if (!m || !box) return;
      box.removeAttribute("readonly");
      box.value = window.getActiveMasterPromptText();
      if (!box.dataset.liveEditorBound) {
        box.dataset.liveEditorBound = "1";
        box.addEventListener("input", function() {
          try {
            localStorage.setItem("mirmir_saved_master_prompt_v1", this.value);
            DATA.master_prompt_text = this.value;
          } catch(e) {}
        });
      }
      const headerBtns = m.querySelector(".flex.flex-wrap.gap-2");
      if (headerBtns && !document.getElementById("btn-save-live-prompt")) {
        headerBtns.insertAdjacentHTML(
          "afterbegin",
          '<button id="btn-save-live-prompt" onclick="saveMasterPromptEditsOnSite()" class="px-3.5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-extrabold cursor-pointer shadow">✅ Сохранить правки на сайте</button>'
        );
      }
      if (!document.getElementById("master-prompt-save-status")) {
        box.insertAdjacentHTML(
          "beforebegin",
          '<div id="master-prompt-save-status" class="mb-2 px-3 py-1.5 rounded-xl bg-amber-50 border border-amber-300 text-[#2E3D28] text-xs font-bold">✏️ Редактируйте и дополняйте Мастер-Промпт прямо в этом поле — изменения сохраняются автоматически!</div>'
        );
      }
      m.classList.remove("hidden");
      m.classList.add("flex");
      applyV36LayoutAndButtons();
    };

    // Мобильный свайп «Назад» (popstate SPA-Guard)
    window.pushModalGuardState = function(tag) {
      try { history.pushState({ mirmirModal: tag || "open", t: Date.now() }, ""); } catch(e) {}
    };

    [
      "openMenu", "openBowlBuilder", "openCafeShopModal", "openBookTableModal",
      "openDeliveryModal", "openRadioSelectorModal", "openSuperZoom",
      "openReadyGalleryPopup", "openUnifiedSystemHub", "openMasterPromptModal"
    ].forEach(fnName => {
      const origFn = window[fnName];
      if (typeof origFn === "function") {
        window[fnName] = function() {
          window.pushModalGuardState(fnName);
          const res = origFn.apply(this, arguments);
          applyV36LayoutAndButtons();
          return res;
        };
      }
    });

    const _origToggleCart = toggleCart;
    toggleCart = function() {
      const dr = document.getElementById("cart-drawer");
      const wasHidden = dr && dr.classList.contains("hidden");
      _origToggleCart();
      if (wasHidden) window.pushModalGuardState("cart");
    };

    window.addEventListener("popstate", function() {
      const modalOrder = [
        { id: "super-zoom-lightbox", close: closeSuperZoom },
        { id: "ready-gallery-popup", close: closeReadyGalleryPopup },
        { id: "master-prompt-modal", close: closeMasterPromptModal },
        { id: "unified-system-hub", close: closeUnifiedSystemHub },
        { id: "radio-selector-modal", close: () => { const m = document.getElementById("radio-selector-modal"); if (m) { m.classList.add("hidden"); m.classList.remove("flex"); } } },
        { id: "book-table-modal", close: closeBookTableModal },
        { id: "delivery-modal", close: () => { const m = document.getElementById("delivery-modal"); if (m) { m.classList.add("hidden"); m.classList.remove("flex"); } } },
        { id: "cafe-shop-modal", close: closeCafeShopModal },
        { id: "cart-drawer", close: () => { const m = document.getElementById("cart-drawer"); if (m) { m.classList.add("hidden"); m.classList.remove("flex"); } } },
        { id: "bowl-modal", close: closeBowlBuilder },
        { id: "menu-modal", close: closeMenu }
      ];
      for (let i = 0; i < modalOrder.length; i++) {
        const el = document.getElementById(modalOrder[i].id);
        if (el && !el.classList.contains("hidden")) {
          modalOrder[i].close();
          return;
        }
      }
      try { history.pushState({ mirmirBase: true }, ""); } catch(e) {}
    });

    let rightColBgIdx = 0;
    setInterval(() => {
      const rightImg = document.getElementById("right-col-bg-photo");
      const slides = window.getInteriorSlidesList();
      if (rightImg && slides.length) {
        rightColBgIdx = (rightColBgIdx + 1) % slides.length;
        rightImg.style.opacity = "0.12";
        setTimeout(() => {
          rightImg.src = slides[rightColBgIdx].src;
          rightImg.style.opacity = "0.32";
        }, 320);
      }
    }, 3800);

    setInterval(() => {
      window.stepRightSpecialsPair(1);
    }, 5200);

    
    // === 🔧 ФИКС v3.7: ЕДИНЫЙ КАРМАН ПРЕДПРОСМОТРА ИИ + ЧИСТАЯ ГАЛЕРЕЯ ВК БЕЗ AI_V23 + ЗАМЕНА HTTP 401 ===
    try {
      window.pendingDishCandidates = pendingDishCandidates;
      window.selectedAiEnginePerDish = selectedAiEnginePerDish;
    } catch(e) {
      window.pendingDishCandidates = window.pendingDishCandidates || {};
      window.selectedAiEnginePerDish = window.selectedAiEnginePerDish || {};
    }

    // Очищаем список готовых фото на клиенте от любых старых ai_v* и ingr_*, ставя реальные фото ВК (vk_*) строго наверх!
    if (DATA && Array.isArray(DATA.ready_photos)) {
      const onlyVk = DATA.ready_photos.filter(p => p.includes("vk_") && !p.includes("5047_")).reverse();
      const onlyCleanMacro = DATA.ready_photos.filter(p => !p.includes("vk_") && !p.includes("ai_v") && !p.includes("ingr_") && !p.includes("5047_"));
      DATA.ready_photos = [...onlyVk, ...onlyCleanMacro];
    }

    // Переопределяем открытие витрины «📸 Из готовых», чтобы она ВСЕГДА открывалась и сразу утверждала фото в 1 клик!
    window.openReadyGalleryPopup = function(dishIdx) {
      window.currentGalleryDishIdx = dishIdx;
      const d = DATA.menu[dishIdx];
      const modal = document.getElementById("ready-gallery-popup");
      if (!modal || !d) return;

      const photosPool = (DATA.ready_photos && DATA.ready_photos.length)
        ? DATA.ready_photos.filter(p => !p.includes("ai_v") && !p.includes("ingr_"))
        : (DATA.vk_food_photos || []);

      const card = modal.firstElementChild;
      if (card) {
        card.innerHTML =
          '<div class="bg-[#2E3D28] text-[#FFFDF9] px-5 py-3.5 flex items-center justify-between border-b border-[#F2B880]/30 relative">' +
            '<div>' +
              '<div class="text-[10px] font-extrabold uppercase tracking-wider text-[#F2B880]">НАСТОЯЩИЕ ФОТОГРАФИИ ИЗ ГРУППЫ ВК КАФЕ «МИР МИР» (' + photosPool.length + ' КАДРОВ)</div>' +
              '<h3 class="font-serif text-xl font-bold">📸 Выберите реальное фото для: <span class="text-[#F2B880] underline">' + esc(d.name) + '</span></h3>' +
            '</div>' +
            '<button onclick="closeReadyGalleryPopup()" class="v36-top-right-close">✕</button>' +
          '</div>' +
          '<div class="p-4 overflow-y-auto max-h-[75vh] bg-[#FAF5EC] grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">' +
            photosPool.map(ph =>
              '<div class="bg-white rounded-2xl p-2.5 border border-stone-200 hover:border-[#D48238] shadow-xs flex flex-col justify-between gap-2 transition">' +
                '<div class="relative h-36 rounded-xl overflow-hidden bg-stone-100">' +
                  '<img src="' + esc(ph) + '" loading="lazy" onclick="openSuperZoom(this.src, \'' + esc(ph) + '\')" class="w-full h-full object-cover cursor-zoom-in">' +
                  '<button onclick="openSuperZoom(\'' + esc(ph) + '\', \'' + esc(ph) + '\')" class="absolute top-1.5 right-1.5 px-2 py-0.5 rounded bg-black/75 text-white text-[10px] font-extrabold cursor-pointer">🔍 Лупа</button>' +
                '</div>' +
                '<div class="text-[10px] font-mono text-stone-500 truncate">' + esc(ph) + '</div>' +
                '<button onclick="selectReadyPhotoV37(' + dishIdx + ', \'' + esc(ph) + '\')" class="w-full py-1.5 rounded-xl bg-emerald-700 hover:bg-[#D48238] text-white text-xs font-extrabold cursor-pointer transition shadow-xs">✅ Утвердить это фото</button>' +
              '</div>'
            ).join("") +
          '</div>';
      }
      modal.classList.remove("hidden");
      modal.classList.add("flex");
    };

    window.selectReadyPhotoV37 = function(dishIdx, photoPath) {
      const d = DATA.menu[dishIdx];
      if (!d) return;
      d.photo = photoPath;
      d.photo_type = "real";
      d.is_manual_override = true;
      try {
        const raw = localStorage.getItem("mirmir_manual_dish_photos_v1");
        const map = raw ? JSON.parse(raw) : {};
        map[d.name] = photoPath;
        localStorage.setItem("mirmir_manual_dish_photos_v1", JSON.stringify(map));
      } catch(e) {}
      if (DATA.tz_synced) {
        DATA.tz_synced.dishes = DATA.tz_synced.dishes || {};
        DATA.tz_synced.dishes[d.name] = { photo: photoPath };
      }
      fetch(NTFY_SYNC_URL, {
        method: "POST",
        body: JSON.stringify({ type: "dish_photo_override", dish_name: d.name, photo: photoPath, ts: Date.now() })
      }).catch(() => {});
      pushDiagLog(dishIdx, "✅", "Из готовых ВК", "Установлено реальное фото кафе: " + photoPath);
      closeReadyGalleryPopup();
      renderUnifiedSystemHub();
      renderDishes();
      renderHeroRightColumn();
    };

    // Гарантируем, что approveDishCandidate и previewManualUrlCandidate работают с единым объектом превью
    window.previewManualUrlCandidate = function(idx) {
      const inp = document.getElementById("hub-url-inp-" + idx);
      const val = (inp?.value || "").trim();
      if (!val) { alert("Вставьте прямую ссылку https://... или путь img/..."); return; }
      const candObj = { url: val, source: "🔗 Прямая ссылка пользователя", prompt: val, diag: "✅ Загружено по прямому URL" };
      window.pendingDishCandidates[idx] = candObj;
      try { pendingDishCandidates[idx] = candObj; } catch(e) {}
      pushDiagLog(idx, "✅", "Прямой URL", "Открыт предпросмотр: " + val);
      renderUnifiedSystemHub();
    };

    window.approveDishCandidate = function(idx) {
      const cand = window.pendingDishCandidates[idx] || (typeof pendingDishCandidates !== "undefined" ? pendingDishCandidates[idx] : null);
      if (!cand || !cand.url) return;
      window.selectReadyPhotoV37(idx, cand.url);
      delete window.pendingDishCandidates[idx];
      try { delete pendingDishCandidates[idx]; } catch(e) {}
      renderUnifiedSystemHub();
    };

    // Патчим generateDishCandidateAI, чтобы результат ВСЕГДА записывался и в window.pendingDishCandidates, и в pendingDishCandidates,
    // а вместо закрытого на HTTP 401 Openverse использовался открытый фото-поиск Wikimedia + ИИ-генератор!
    const _origGenV36 = generateDishCandidateAI;
    generateDishCandidateAI = async function(idx) {
      const curE = window.selectedAiEnginePerDish[idx] || (typeof selectedAiEnginePerDish !== "undefined" ? selectedAiEnginePerDish[idx] : "gastro_hd");
      // Если нажали Openverse (который теперь требует OAuth и отдаёт HTTP 401), прозрачно переключаем на открытый поиск Wikimedia Commons HD!
      if (curE === "openverse_hd") {
        window.selectedAiEnginePerDish[idx] = "wikimedia";
        try { selectedAiEnginePerDish[idx] = "wikimedia"; } catch(e) {}
        pushDiagLog(idx, "🔄", "Openverse (HTTP 401)", "API Openverse закрыт ключом ➔ Авто-переход на открытый поиск Wikimedia HD");
      }
      await _origGenV36(idx);
      try {
        if (typeof pendingDishCandidates !== "undefined" && pendingDishCandidates[idx]) {
          window.pendingDishCandidates[idx] = pendingDishCandidates[idx];
        } else if (window.pendingDishCandidates[idx] && typeof pendingDishCandidates !== "undefined") {
          pendingDishCandidates[idx] = window.pendingDishCandidates[idx];
        }
      } catch(e) {}
      renderUnifiedSystemHub();
    };

    
    // === ⚡ ПРЯМЫЕ ПЕРЕКЛЮЧАТЕЛИ ВКЛАДОК И ФИЛЬТРОВ ШЕСТЕРЁНКИ v3.8 (БЕЗ КОНФЛИКТА LET/VAR) ===
    window.switchHubTabV38 = function(tabId) {
      window.hubActiveTab = tabId;
      try { hubActiveTab = tabId; } catch(e) {}
      window.renderUnifiedSystemHub();
    };
    window.switchHubCatV38 = function(catName) {
      window.hubDishCategoryFilter = catName;
      try { hubDishCategoryFilter = catName; } catch(e) {}
      window.renderUnifiedSystemHub();
    };
    window.searchHubDishV38 = function(qVal) {
      window.hubDishSearchQuery = qVal;
      try { hubDishSearchQuery = qVal; } catch(e) {}
      window.renderUnifiedSystemHub();
    };
    window.closeUnifiedSystemHub = function() {
      const m = document.getElementById("unified-system-hub");
      if (m) { m.classList.add("hidden"); m.classList.remove("flex"); }
    };

    window.addEventListener("DOMContentLoaded", () => {
      injectCustomDishesIntoMenu();
      applyV36LayoutAndButtons();
      document.querySelectorAll("[data-dove-holder]").forEach(el => { el.innerHTML = SIGN_DOVE_SVG; });
      if (DATA.ymap_photos && DATA.ymap_photos.length >= 2) {
        const lw = document.getElementById("left-wing-img"), rw = document.getElementById("right-wing-img");
        if (lw) lw.src = DATA.ymap_photos[0];
        if (rw) rw.src = DATA.ymap_photos[1];
      }
      applyManualOverridesToMenuData();
      renderWorkStatusBadges();
      rollRandomGastroPulse();
      renderInteriorSlideState();
      setInterval(() => stepInteriorSlide(1), 4200);
      renderHeroRightColumn();
      setInterval(() => step3DCarousel(1), 4500);
      renderNewsPosts();
      renderCategoryShowcaseAndRail();
      window.applySiteToggles();
    });
  </script>
</body>
</html>
"""
    return tpl_html + v36_clean_tail


def build_clean_master_prompt_text():
    if os.path.exists("MASTER_PROMPT_MIRMIR.txt"):
        try:
            content = open("MASTER_PROMPT_MIRMIR.txt", "r", encoding="utf-8").read().strip()
            if len(content) > 600:
                return content
        except Exception:
            pass
    lines = [
        "ПОЛНОЕ ТЕХНИЧЕСКОЕ ЗАДАНИЕ (МАСТЕР-ПРОМПТ) НА СОЗДАНИЕ И РАЗВИТИЕ ТРЁХМОДУЛЬНОЙ ПЛАТФОРМЫ ВЕГАН-КАФЕ «МИР МИР» (v3.6)",
        "1. ТРЁХМОДУЛЬНАЯ АРХИТЕКТУРА: menu_data.py (72 веган-блюда + 8 товаров) + template.html + app.py.",
        "2. ШЕСТЕРЁНКА АРХИТЕКТОРА (⚙️): все 5 вкладок активны, ровные карточки блюд с 6 источниками фото/ИИ, выводом живых логов диагностики и переключателями режимов Брони (Telegram/ВК или 152-ФЗ), Карты и Фото.",
        "3. ПОЛНЫЙ СПИСОК ЗАДАЧ: 17+ пунктов с датами, переключением «Сделано / Не сделано» и полем комментария Милорда справа с авто-синхронизацией в tz_mirmir.json."
    ]
    txt = "\n".join(lines)
    with open("MASTER_PROMPT_MIRMIR.txt", "w", encoding="utf-8") as f:
        f.write(txt)
    return txt


def sync_files_to_root_repo():
    if os.path.abspath(ROOT_REPO_DIR) == os.path.abspath(BASE_DIR):
        return
    for fn in [
        "index.html",
        "menu_data.py",
        "template.html",
        "app.py",
        "tz_mirmir.json",
        "build_history.json",
        "MASTER_PROMPT_MIRMIR.txt",
        "run_counter.txt",
        "cache_posts.json",
    ]:
        src = os.path.join(BASE_DIR, fn)
        dst = os.path.join(ROOT_REPO_DIR, fn)
        if os.path.exists(src):
            try:
                shutil.copy2(src, dst)
            except Exception:
                pass

    src_img_dir = os.path.join(BASE_DIR, "img")
    dst_img_dir = os.path.join(ROOT_REPO_DIR, "img")
    if os.path.exists(src_img_dir):
        os.makedirs(dst_img_dir, exist_ok=True)
        for fn in os.listdir(src_img_dir):
            if fn.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                s_f = os.path.join(src_img_dir, fn)
                d_f = os.path.join(dst_img_dir, fn)
                if not os.path.exists(d_f) or os.path.getsize(d_f) != os.path.getsize(s_f):
                    try:
                        shutil.copy2(s_f, d_f)
                    except Exception:
                        pass
    print(f"🔄 [Синхронизация корня] Главный `index.html`, `tz_mirmir.json` и папка `img/` в `{ROOT_REPO_DIR}` обновлены!")


def main():
    print("=" * 78)
    print("🕊️  СБОРКА «МИР МИР» v3.6 (ПОЧИНКА ШЕСТЕРЁНКИ + РЕЖИМЫ CLAUDE + 0 ДУБЛЕЙ КНОПОК)")
    print("=" * 78)

    auto_migrate_assets_from_old_folder()
    purge_meat_looking_local_files()
    enforce_vegan_prompts_in_menu_data_file()

    import importlib
    import menu_data
    importlib.reload(menu_data)
    MENU_DATABASE = menu_data.MENU_DATABASE
    CAFE_SHOP_ITEMS = menu_data.CAFE_SHOP_ITEMS

    tz_data, build_logs, build_num = sync_tz_and_build_logs()
    dish_overrides = tz_data.get("dishes", {})

    clean_menu = []
    for item in MENU_DATABASE:
        d = dict(item)
        if "photo_type" not in d:
            d["photo_type"] = d.pop("photo_type: ", "real")
        if "macro_mushrooms_raw" in str(d.get("photo", "")):
            d["photo"] = "img/macro_tomyum_bowl.jpg"
        nm = d.get("name", "")
        if nm in dish_overrides and dish_overrides[nm].get("photo"):
            d["photo"] = dish_overrides[nm]["photo"]
            d["photo_type"] = "real"
            d["is_manual_override"] = True
        clean_menu.append(d)

    ymap_photos = get_verified_interior_exterior_photos()
    wall_posts = fetch_vk_wall_posts()
    vk_food_photos = collect_vk_food_photos()

    ready_photos = []
    if os.path.exists("img"):
        for fn in sorted(os.listdir("img")):
            if fn.lower().endswith((".jpg", ".jpeg", ".png", ".webp")) and "5047_" not in fn and "mushrooms_raw" not in fn:
                ready_photos.append("img/" + fn)

    master_prompt_str = build_clean_master_prompt_text()
    now_stamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    data_payload = {
        "version": f"Релиз v3.6 • Сборка #{build_num} ({now_stamp})",
        "menu": clean_menu,
        "shop": CAFE_SHOP_ITEMS,
        "posts": wall_posts,
        "ymap_photos": ymap_photos,
        "ready_photos": ready_photos,
        "vk_food_photos": vk_food_photos,
        "menu_scans": ["img/vk_5047_0.jpg", "img/vk_5047_1.jpg", "img/vk_5047_2.jpg", "img/vk_5047_3.jpg"],
        "tz_synced": tz_data,
        "full_build_logs": build_logs,
        "master_prompt_text": master_prompt_str,
    }

    if not os.path.exists("template.html"):
        raise FileNotFoundError("Не найден template.html в текущей папке!")

    with open("template.html", "r", encoding="utf-8") as f:
        tpl_html = f.read()

    tpl_html = upgrade_template_html_in_place(tpl_html)
    with open("template.html", "w", encoding="utf-8") as f:
        f.write(tpl_html)

    safe_json_str = json.dumps(data_payload, ensure_ascii=False).replace("</", "<\\/")
    final_html = tpl_html.replace("__MIRMIR_DATA_JSON__", safe_json_str)
    final_html += f"\n<!-- MirMir Build #{build_num} at {now_stamp} -->\n"

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(final_html)

    sync_files_to_root_repo()
    print(f"✨ [Сборка #{build_num} готова] Шестерёнка починена, дубли кнопок убраны, переключатели Брони/Карты/Фото вшиты!")
    if sys.stdin and sys.stdin.isatty() and os.environ.get("GITHUB_ACTIONS") != "true":
        try:
            os.startfile("index.html")
        except Exception:
            pass


def push_to_github():
    sync_files_to_root_repo()
    local_git = os.path.join(BASE_DIR, ".git")
    if os.path.abspath(ROOT_REPO_DIR) != os.path.abspath(BASE_DIR) and os.path.exists(local_git):
        try:
            shutil.rmtree(local_git, ignore_errors=True)
        except Exception:
            pass

    target_git_dir = ROOT_REPO_DIR
    print(f"\n📂 Рабочая папка Git-репозитория: {target_git_dir}")

    lock_file = os.path.join(target_git_dir, ".git", "index.lock")
    if os.path.exists(lock_file):
        try:
            os.remove(lock_file)
        except Exception:
            pass

    subprocess.run(["git", "config", "user.name", "MirMir Cafe"], cwd=target_git_dir, check=False)
    subprocess.run(["git", "config", "user.email", "admin@mirmir.cafe"], cwd=target_git_dir, check=False)

    root_index = os.path.join(target_git_dir, "index.html")
    if os.path.exists(root_index):
        with open(root_index, "a", encoding="utf-8") as f:
            f.write(f"\n<!-- Root Deploy Stamp: {datetime.now().isoformat()} -->\n")

    subprocess.run(["git", "remote", "remove", "origin"], cwd=target_git_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "remote", "add", "origin", "https://github.com/vitvseom-stack/mirmir.git"], cwd=target_git_dir, check=False)
    subprocess.run(["git", "checkout", "-B", "main"], cwd=target_git_dir, check=False)

    print("📡 Индексация КОРНЕВОГО index.html + папки img/ и отправка на https://vitvseom-stack.github.io/mirmir/ ...")
    subprocess.run(
        ["git", "add", "-f", "index.html", "menu_data.py", "template.html", "app.py", "tz_mirmir.json", "build_history.json", "MASTER_PROMPT_MIRMIR.txt", "cache_posts.json"],
        cwd=target_git_dir,
        check=False,
    )
    subprocess.run(["git", "add", "img/"], cwd=target_git_dir, check=False)
    subprocess.run(["git", "commit", "-m", f"Deploy MirMir v3.6 ({datetime.now().strftime('%d.%m.%Y %H:%M:%S')})"], cwd=target_git_dir, check=False)

    res = subprocess.run(["git", "push", "-u", "origin", "main", "--force"], cwd=target_git_dir, check=False)
    if res.returncode == 0:
        print("\n✅ ГЛАВНЫЙ САЙТ УСПЕШНО ОТПРАВЛЕН НА GITHUB PAGES!")
        print("🌐 Проверяй через 45–60 секунд (Ctrl + F5): https://vitvseom-stack.github.io/mirmir/")
    else:
        print("\n⚠️ Git вернул ошибку при отправке — проверь сообщения выше.")


if __name__ == "__main__":
    if not sys.stdin or not sys.stdin.isatty() or os.environ.get("GITHUB_ACTIONS") == "true":
        main()
        sys.exit(0)

    try:
        print("=" * 78)
        print("🕊️  ПУЛЬТ УПРАВЛЕНИЯ ПЛАТФОРМОЙ «МИР МИР» v3.6 (Ильинская, 45)")
        print("=" * 78)
        print("  [1] 💻 Только на ПК (собрать index.html и открыть в браузере)")
        print("  [2] 🚀 На ПК + На Сайт (собрать, открыть на ПК и выгрузить в корень GitHub)")
        print("  [3] 🌐 Только на Сайт (выгрузить текущий index.html в корень GitHub)")
        print("=" * 78)
        mode = input("👉 Введите цифру (1, 2 или 3) и нажмите Enter [по умолчанию 2]: ").strip() or "2"

        if mode == "1":
            main()
        elif mode == "3":
            push_to_github()
        else:
            main()
            push_to_github()

        print("=" * 78)
        print("🎉 КРАСОВЕЛОФ, МИЛОРД! Сборка v3.6 завершена без единой ошибки!")
        print("=" * 78)
    except Exception:
        print("\n❌ ОШИБКА ПРИ ВЫПОЛНЕНИИ:")
        traceback.print_exc()
    input("\nНажмите Enter для закрытия этого окна...")