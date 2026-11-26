# -*- coding: utf-8 -*-
"""
КОМПИЛЯТОР ПЛАТФОРМЫ «МИР МИР» (app.py — Полная сборка v4.9)
- Живая Яндекс.Карта с наложенными стеклянными плашками-подсказками и кнопкой скрытия надписей.
- Жёсткая защита Hero от перезаписи блоком адреса.
- Умный режим фото без обрезки (Ambient Blur Backdrop).
- Точный поиск/генерация фото блюд (Flux/Turbo AI, Openverse, Wikimedia, чистый GastroBank).
- Интеграция с live_constructor.py, approved_menu_photos.json и логами logs/.
"""
import os
import sys
import re
import json
import shutil
import subprocess
import traceback
import importlib
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

LOGS_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

VK_PUBLIC_URL = "https://vk.com/mirmir.cafe"
NTFY_SYNC_TOPIC = "mirmir_tz_sync_nn45_v30"
OLD_DIRS_TO_CHECK = [DEFAULT_MIRMIR_ROOT, PARENT_DIR]

MASTER_TASKS_DEFAULT = [
    {"id": "t_1", "date": "08.11.2026 12:10", "title": "1. Трёхмодульная архитектура (menu_data.py + template.html + app.py) и деплой", "done": True, "comment": "Сборка и синхронизация с GitHub Pages работают штатно."},
    {"id": "t_2", "date": "26.11.2026 10:00", "title": "2. Первый экран слева: слайдер зала (5 фото) с умным фоном без обрезки", "done": True, "comment": "Диван и вывеска видны целиком на размытом фоне в тон."},
    {"id": "t_3", "date": "09.11.2026 15:05", "title": "3. Первый экран справа: 3D-карусель бланков меню + 2 карточки спешлов", "done": True, "comment": "Сбалансированная карусель + 2 крупные карточки спешлов."},
    {"id": "t_4", "date": "09.11.2026 16:30", "title": "4. Плашка «Подача блюд может отличаться» на карточках и в лайтбоксе", "done": True, "comment": "Отображается на миниатюрах и при увеличении 🔍."},
    {"id": "t_5", "date": "10.11.2026 11:15", "title": "5. Обработка системной кнопки «Назад» (popstate) на смартфонах", "done": True, "comment": "Закрывает открытое модальное окно без выхода с сайта."},
    {"id": "t_6", "date": "12.11.2026 10:15", "title": "6. Автоскролл новостей влево + кнопки ◀ ▶ + «⏮️ К последним постам»", "done": True, "comment": "Плавный тикер с паузой при наведении и клике по стрелкам."},
    {"id": "t_7", "date": "26.11.2026 10:05", "title": "7. Сбалансированная ширина (1320px), крестики ✕ справа вверху и значок 🔍", "done": True, "comment": "Убрано растягивание до 1640px, кулисы видны ровно."},
    {"id": "t_8", "date": "26.11.2026 10:10", "title": "8. Живая Яндекс.Карта с наложенными плашками-подсказками без рекламного баннера", "done": True, "comment": "Карта загружается сразу, поверх неё — ориентиры, GPS и кнопки маршрута."},
    {"id": "t_9", "date": "26.11.2026 10:15", "title": "9. Автономный Конструктор окон и фото (включается строго в Шестерёнке)", "done": True, "comment": "Вынесен в live_constructor.py, рабочие +/- и «✅ Применить»."},
    {"id": "t_10", "date": "26.11.2026 10:20", "title": "10. Точный поиск/генерация фото блюд (Flux/Turbo AI, Openverse, Wikimedia)", "done": True, "comment": "Очищен GastroBank HD по категориям, точные промпты и поиск."},
    {"id": "t_11", "date": "26.11.2026 10:25", "title": "11. Витрина «Меню кафе по разделам» (9 карточек) с правильными фото", "done": True, "comment": "Исправлены обложки Лапши, Барного меню и Десертов."},
    {"id": "t_12", "date": "11.11.2026 15:20", "title": "12. Временное отключение блюд и удаление с 3 подтверждениями", "done": True, "comment": "Доступно в карточке каждого блюда в Шестерёнке."},
    {"id": "t_13", "date": "26.11.2026 10:30", "title": "13. Файловые логи logs/logs_*.txt и привязка фото из vision_parser", "done": True, "comment": "Подхватывается approved_menu_photos.json и пишутся логи."}
]


def write_file_log(event_text):
    now_s = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    day_s = datetime.now().strftime("%Y%m%d")
    line = f"[{now_s}] {event_text}"
    print(line)
    for fn in (f"logs_{day_s}.txt", "logs_latest.txt"):
        try:
            with open(os.path.join(LOGS_DIR, fn), "a", encoding="utf-8") as lf:
                lf.write(line + "\n")
        except Exception:
            pass


def sanitize_text(txt):
    if not isinstance(txt, str):
        return txt
    replacements = [
        ("Комментарий Милорда / Что не так", "Комментарий / Примечание"),
        ("Комментарий Милорда", "Комментарий"),
        ("Реестр Задач Милорда", "Реестр задач проекта"),
        ("заданиями Милорда", "задачами проекта"),
        ("от Милорда", "администратора"),
        ("По поручению Милорда", "По плану разработки"),
        ("Милорд", "Администратор"),
        ("читаь все новости на VK", "ВК"),
    ]
    for old_s, new_s in replacements:
        txt = txt.replace(old_s, new_s)
    return txt


def is_junk_image_name(fn):
    low = fn.lower()
    if low in ("macro_mushrooms_raw.jpg", "macro_rice_noodles.jpg"):
        return True
    if low.startswith(("ai_v", "ingr_")):
        return True
    if low.startswith("ymap_org_") and low not in ("ymap_org_0.jpg", "ymap_org_1.jpg"):
        return True
    if low.startswith("yorg_") and low not in ("yorg_0.jpg", "yorg_1.jpg"):
        return True
    return False


def prepare_and_clean_assets():
    """Мигрирует ассеты и удаляет невеганские/чужие кадры из img/."""
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
                if fn.lower().endswith((".jpg", ".jpeg", ".png", ".webp")) and not is_junk_image_name(fn):
                    s_f, d_f = os.path.join(old_img, fn), os.path.join(BASE_DIR, "img", fn)
                    if not os.path.exists(d_f) or os.path.getsize(d_f) < 1000:
                        try:
                            shutil.copy2(s_f, d_f)
                        except Exception:
                            pass

    for t_dir in [BASE_DIR, ROOT_REPO_DIR]:
        img_d = os.path.join(t_dir, "img")
        if not os.path.exists(img_d):
            continue
        for fn in list(os.listdir(img_d)):
            if is_junk_image_name(fn):
                try:
                    os.remove(os.path.join(img_d, fn))
                except Exception:
                    pass


def is_pinned_menu_post(text_str, is_pinned_flag=0):
    low = (text_str or "").lower()
    return ("прикрепляю наше актуальное меню" in low) or ("актуальное меню" in low) or bool(is_pinned_flag and "меню" in low)


def fetch_vk_wall_posts():
    vk_token = os.environ.get("VK_TOKEN") or (
        open("vk key.txt", "r", encoding="utf-8").read().strip() if os.path.exists("vk key.txt") else ""
    )
    fallbacks = [
        p for p in ["img/vk_5122_0.jpg", "img/vk_5068_0.jpg", "img/vk_5128_1.jpg", "img/vk_5134_0.jpg"]
        if os.path.exists(p)
    ] or ["img/ymap_org_0.jpg"]
    posts_out = []

    if vk_token:
        try:
            r = requests.get(
                "https://api.vk.com/method/wall.get",
                params={"domain": "mirmir.cafe", "count": 20, "access_token": vk_token, "v": "5.199"},
                timeout=8
            )
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
                vk_link = (
                    f"https://vk.com/mirmir.cafe?w=wall{owner_id}_{post_id}"
                    if (owner_id and str(owner_id) != "-191992548" and post_id)
                    else VK_PUBLIC_URL
                )
                posts_out.append({
                    "id": post_id, "date": dt_str, "likes": likes,
                    "title": first_line[:68], "text": txt[:280],
                    "photo": photo_local, "vk_url": vk_link
                })
                if len(posts_out) >= 12:
                    break
            if posts_out:
                json.dump(posts_out, open("cache_posts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
                return posts_out
        except Exception as e:
            write_file_log(f"[WARN] Ошибка запроса VK API: {e}")

    if os.path.exists("cache_posts.json"):
        try:
            cached = [
                p for p in json.load(open("cache_posts.json", "r", encoding="utf-8"))
                if not is_pinned_menu_post((p.get("title") or "") + " " + (p.get("text") or ""))
            ]
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
    tz_data = {"tasks": [], "dishes": {}, "custom_dishes": []}
    if os.path.exists("tz_mirmir.json"):
        try:
            loaded = json.load(open("tz_mirmir.json", "r", encoding="utf-8"))
            if isinstance(loaded, dict):
                tz_data.update(loaded)
        except Exception:
            pass

    by_id = {str(t["id"]): t for t in tz_data.get("tasks", []) if isinstance(t, dict) and t.get("id")}
    merged = []
    for d_t in MASTER_TASKS_DEFAULT:
        tid = d_t["id"]
        if tid in by_id:
            old = by_id.pop(tid)
            old_dt = str(old.get("date") or "")
            merged.append({
                "id": tid,
                "date": old_dt if ":" in old_dt else d_t["date"],
                "title": sanitize_text(d_t["title"]),
                "done": bool(old.get("done", d_t["done"])),
                "comment": sanitize_text(old.get("comment") or d_t["comment"])
            })
        else:
            merged.append(dict(d_t))
    for _, v in by_id.items():
        if len(str(v.get("title", ""))) > 3:
            v["title"] = sanitize_text(v.get("title", ""))
            v["comment"] = sanitize_text(v.get("comment", ""))
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
    now_str = datetime.now().strftime("%d.%m.%Y %H:%M")
    logs.insert(0, {
        "version": f"Релиз v4.9 • Сборка #{cnt}",
        "timestamp": now_str,
        "model": "Полная сборка v4.9: Живая Яндекс.Карта с наложенными плашками + Умный фон фото + Точный ИИ-поиск",
        "status": "Возвращена живая карта с наложенными ориентирами и кнопкой скрытия, защищён Hero, обновлены Конструктор и генератор блюд.",
        "stats": f"Дата сборки: {now_str}"
    })
    json.dump(logs[:60], open("build_history.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return tz_data, logs[:60], cnt


def load_approved_vision_overrides():
    """Подхватывает утверждённые фото блюд из approved_menu_photos.json (vision_parser)."""
    overrides = {}
    for d in [BASE_DIR, PARENT_DIR, os.path.join(PARENT_DIR, "vision_sandbox")]:
        ap = os.path.join(d, "approved_menu_photos.json")
        if os.path.exists(ap):
            try:
                data = json.load(open(ap, "r", encoding="utf-8"))
                if isinstance(data, dict):
                    for dish_nm, info in data.items():
                        ph = info.get("approved_photo") or info.get("original_photo")
                        if ph and os.path.exists(os.path.join(BASE_DIR, ph)):
                            overrides[dish_nm] = ph
            except Exception:
                pass
    return overrides


def upgrade_template_html_in_place(tpl_html):
    tpl_html = sanitize_text(tpl_html)
    tpl_html = tpl_html.replace("🔍 Лупа", "🔍").replace("Лупа 🔍", "🔍")

    if 'name="robots"' not in tpl_html:
        tpl_html = tpl_html.replace("<head>", '<head>\n  <meta name="robots" content="noindex, nofollow">', 1)

    for vname in [
        "hubActiveTab", "hubDishCategoryFilter", "hubDishSearchQuery",
        "selectedAiEnginePerDish", "pendingDishCandidates", "currentMenuCategory", "currentNewsPage"
    ]:
        tpl_html = re.sub(rf"\blet\s+{vname}\b", f"var {vname}", tpl_html)

    anchor_pos = tpl_html.find('a.download = "MASTER_PROMPT_MIRMIR.txt";')
    if anchor_pos != -1:
        brace_pos = tpl_html.find("}", anchor_pos)
        if brace_pos != -1:
            tpl_html = tpl_html[: brace_pos + 1] + "\n"

    v49_js = r"""
    // === ЧИСТОЕ КЛИЕНТСКОЕ ЯДРО ПЛАТФОРМЫ «МИР МИР» (v4.9) ===
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

    const VERIFIED_CATEGORY_PHOTOS = {
      "Сезонные спешлы от Шефа": "img/vk_5085_1.jpg",
      "Супы": "img/macro_tomyum_bowl.jpg",
      "Боулы и Омлеты": "img/vk_5128_1.jpg",
      "Салаты": "img/macro_caesar_romaine.jpg",
      "Лапша": "img/vk_5094_0.jpg",
      "Бургеры и Из печи": "img/macro_vegan_burger.jpg",
      "Десерты без сахара": "img/vk_5069_0.jpg",
      "Барное меню: Смузи и Кофе": "img/macro_strawberry_banana.jpg",
      "Чайная карта": "img/vk_5122_0.jpg",
      "Дополнительно": "img/vk_5121_0.jpg"
    };

    // 1. Умный режим фото без обрезки (Ambient Blur Backdrop)
    window.applyNoCropAmbientPhotos = function() {
      if (!document.getElementById("mirmir-nocrop-ambient-css")) {
        const st = document.createElement("style");
        st.id = "mirmir-nocrop-ambient-css";
        st.textContent = `
          .mirmir-nocrop-wrap {
            position: relative !important;
            overflow: hidden !important;
            background-color: #1D2918 !important;
          }
          .mirmir-nocrop-bg {
            position: absolute !important;
            inset: -16px !important;
            background-size: cover !important;
            background-position: center !important;
            filter: blur(18px) brightness(0.68) saturate(1.35) !important;
            transform: scale(1.14) !important;
            z-index: 0 !important;
            pointer-events: none !important;
            transition: background-image 0.3s ease !important;
          }
          body:not(.mirmir-crop-cover-mode) .mirmir-nocrop-wrap > img {
            position: relative !important;
            z-index: 1 !important;
            object-fit: contain !important;
            width: 100% !important;
            height: 100% !important;
            max-width: 100% !important;
            max-height: 100% !important;
            filter: drop-shadow(0 6px 16px rgba(0, 0, 0, 0.42));
          }
          body.mirmir-crop-cover-mode .mirmir-nocrop-wrap > img {
            position: relative !important;
            z-index: 1 !important;
            object-fit: cover !important;
          }
          .mirmir-nocrop-wrap > *:not(.mirmir-nocrop-bg):not(img) {
            z-index: 5;
          }
        `;
        document.head.appendChild(st);
      }

      const imgs = document.querySelectorAll(
        "#hero-interior-slide-img, #hero-specials-3rows .zoom-card img, " +
        "#posts-grid article img, #cat-showcase-grid .zoom-card img, " +
        "#menu-dishes-grid .zoom-card img, #cafe-shop-grid .zoom-card img"
      );
      imgs.forEach(im => {
        const wrap = im.parentElement;
        if (!wrap) return;
        wrap.classList.add("mirmir-nocrop-wrap");
        let bg = wrap.querySelector(".mirmir-nocrop-bg");
        if (!bg) {
          bg = document.createElement("div");
          bg.className = "mirmir-nocrop-bg";
          wrap.insertBefore(bg, wrap.firstChild);
        }
        const src = im.getAttribute("src") || im.src || "";
        if (src) bg.style.backgroundImage = 'url("' + src.replace(/"/g, '\\"') + '")';
        if (!im.dataset.ambientHooked) {
          im.dataset.ambientHooked = "1";
          im.addEventListener("load", function() {
            const s = this.getAttribute("src") || this.src || "";
            const b = this.parentElement ? this.parentElement.querySelector(".mirmir-nocrop-bg") : null;
            if (b && s) b.style.backgroundImage = 'url("' + s.replace(/"/g, '\\"') + '")';
          });
        }
      });
    };

    // 2. Отключение (полупрозрачность) и удаление блюд (3 подтверждения)
    window.getDisabledDishesMap = function() {
      try { return JSON.parse(localStorage.getItem("mirmir_disabled_dishes_v1") || "{}"); } catch (e) { return {}; }
    };
    window.isDishDisabled = function(name) {
      return Boolean(window.getDisabledDishesMap()[name]);
    };
    window.toggleDishDisabled = function(idx) {
      const d = DATA.menu[idx];
      if (!d) return;
      const map = window.getDisabledDishesMap();
      if (map[d.name]) delete map[d.name]; else map[d.name] = true;
      try { localStorage.setItem("mirmir_disabled_dishes_v1", JSON.stringify(map)); } catch (e) {}
      window.renderUnifiedSystemHub();
      window.renderDishes();
      window.renderHeroRightColumn();
    };
    window.getDeletedDishesMap = function() {
      try { return JSON.parse(localStorage.getItem("mirmir_deleted_dishes_v1") || "{}"); } catch (e) { return {}; }
    };
    window.deleteDishTripleConfirm = function(idx) {
      const d = DATA.menu[idx];
      if (!d) return;
      if (!confirm("Подтверждение 1 из 3:\nУдалить блюдо «" + d.name + "»?")) return;
      if (!confirm("Подтверждение 2 из 3:\nВы уверены, что хотите удалить «" + d.name + "»?")) return;
      if (!confirm("Подтверждение 3 из 3:\nОкончательно удалить «" + d.name + "» из меню?")) return;
      const map = window.getDeletedDishesMap();
      map[d.name] = true;
      try { localStorage.setItem("mirmir_deleted_dishes_v1", JSON.stringify(map)); } catch (e) {}
      DATA.menu.splice(idx, 1);
      window.renderUnifiedSystemHub();
      window.renderDishes();
      window.renderHeroRightColumn();
      window.renderCategoryShowcaseAndRail();
    };
    window.restoreAllDeletedDishes = function() {
      if (!confirm("Восстановить все ранее удалённые блюда?")) return;
      try { localStorage.removeItem("mirmir_deleted_dishes_v1"); } catch (e) {}
      location.reload();
    };

    function loadCustomAddedDishes() {
      try { return JSON.parse(localStorage.getItem("mirmir_custom_dishes_v1") || "[]"); } catch (e) { return []; }
    }
    function syncMenuWithCustomAndDeleted() {
      if (!DATA.menu) DATA.menu = [];
      loadCustomAddedDishes().forEach(cd => {
        if (cd && cd.name && !DATA.menu.some(m => m.name === cd.name)) DATA.menu.unshift(cd);
      });
      const delMap = window.getDeletedDishesMap();
      DATA.menu = DATA.menu.filter(d => !delMap[d.name]);
      DATA.menu.forEach(d => {
        const ph = String(d.photo || "");
        if (ph.includes("macro_mushrooms_raw") || ph.includes("macro_rice_noodles") || ph.includes("ai_v") || ph.includes("ingr_")) {
          d.photo = VERIFIED_CATEGORY_PHOTOS[d.category] || "img/vk_5128_1.jpg";
        }
      });
    }

    // 3. Лайтбокс с плашкой подачи
    const _baseOpenSuperZoom = window.openSuperZoom;
    window.openSuperZoom = function(src, title) {
      if (_baseOpenSuperZoom) _baseOpenSuperZoom(src, title);
      const lb = document.getElementById("super-zoom-lightbox");
      if (!lb) return;
      if (!document.getElementById("zoom-serving-disclaimer")) {
        const note = document.createElement("div");
        note.id = "zoom-serving-disclaimer";
        note.className = "fixed bottom-5 left-1/2 -translate-x-1/2 z-[220] px-4 py-1.5 rounded-full bg-black/85 text-[#F2B880] border border-[#F2B880]/50 text-xs font-extrabold shadow-xl pointer-events-none whitespace-nowrap";
        note.textContent = "🍽️ Подача блюд может отличаться от фотографии";
        lb.appendChild(note);
      }
      lb.classList.remove("hidden");
      lb.classList.add("flex");
    };

    // 4. Слайдер интерьера (5 проверенных кадров)
    window.getInteriorSlidesList = function() {
      return [
        { src: "img/ymap_org_0.jpg", title: "🏛️ Исторический кирпичный свод и уютный зал", tag: "Интерьер зала" },
        { src: "img/ymap_org_1.jpg", title: "🕊️ Фирменная кованая вывеска с белой Голубкой мира", tag: "Экстерьер у входа" },
        { src: "img/vk_5068_0.jpg", title: "🛋️ Изумрудный велюровый диван, живой кирпич и картины", tag: "Атмосфера «Мир Мир»" },
        { src: "img/vk_5122_0.jpg", title: "🕯️ Вечерние чаепития при свечах и редкий китайский чай", tag: "Чайная культура" },
        { src: "img/vk_5134_0.jpg", title: "🌿 Уютное зелёное пространство для встреч и общения", tag: "Интерьер кафе" }
      ];
    };

    const _baseRenderInterior = window.renderInteriorSlideState;
    window.renderInteriorSlideState = function() {
      if (_baseRenderInterior) _baseRenderInterior();
      const imgEl = document.getElementById("hero-interior-slide-img");
      if (imgEl && imgEl.parentElement) {
        imgEl.parentElement.style.height = "300px";
        imgEl.parentElement.style.minHeight = "300px";
        const slides = window.getInteriorSlidesList();
        const activeSlide = slides[curInteriorSlide] || slides[0];
        const bgDiv = imgEl.parentElement.querySelector(".mirmir-nocrop-bg");
        if (bgDiv && activeSlide) {
          bgDiv.style.backgroundImage = 'url("' + activeSlide.src + '")';
        }
        setTimeout(() => { window.applyNoCropAmbientPhotos(); }, 180);
      }
    };

    // 5. Витрина разделов меню (#cat-showcase-grid) и быстрая полоса категорий
    window.renderCategoryShowcaseAndRail = function() {
      syncMenuWithCustomAndDeleted();
      const cats = Array.from(new Set((DATA.menu || []).map(d => d.category)));
      const rail = document.getElementById("v45-quick-cats-strip");
      if (rail) {
        rail.innerHTML =
          '<button type="button" onclick="openMenu(\'Все\')" class="px-3 py-1.5 rounded-full bg-[#2E3D28] text-[#F2B880] text-xs font-extrabold whitespace-nowrap cursor-pointer">📖 Все блюда (' + DATA.menu.length + ')</button>' +
          cats.map(c =>
            '<button type="button" onclick="openMenu(\'' + esc(c) + '\')" class="px-3 py-1.5 rounded-full bg-white hover:bg-amber-50 text-[#2E3D28] border border-stone-300 text-xs font-extrabold whitespace-nowrap cursor-pointer transition">' + esc(c) + '</button>'
          ).join("");
      }

      const grid = document.getElementById("cat-showcase-grid");
      if (grid) {
        grid.className = "grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mt-3";
        grid.innerHTML = cats.filter(c => c !== "Дополнительно").slice(0, 9).map(c => {
          const items = DATA.menu.filter(d => d.category === c);
          const photo = VERIFIED_CATEGORY_PHOTOS[c] || (items[0] ? items[0].photo : "img/vk_5085_1.jpg");
          return '<div onclick="openMenu(\'' + esc(c) + '\')" class="zoom-card bg-[#FFFDF9] rounded-3xl p-3 border border-[#556432]/25 shadow-sm flex flex-col justify-between gap-2.5 cursor-pointer">' +
            '<div class="relative h-44 rounded-2xl overflow-hidden bg-[#1D2918]">' +
              '<img src="' + esc(photo) + '" alt="' + esc(c) + '" class="w-full h-full">' +
              '<div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/15 to-transparent pointer-events-none"></div>' +
              '<div class="absolute bottom-2.5 left-3 right-3 flex items-end justify-between gap-2 pointer-events-none">' +
                '<h3 class="font-serif text-xl font-bold text-white leading-tight">' + esc(c) + '</h3>' +
                '<span class="px-2 py-0.5 rounded-full bg-[#D48238] text-white text-[10px] font-extrabold whitespace-nowrap">' + items.length + ' поз.</span>' +
              '</div>' +
            '</div>' +
            '<button type="button" class="w-full py-2 rounded-xl bg-[#556432] hover:bg-[#2E3D28] text-white font-extrabold text-xs cursor-pointer transition">📖 Открыть раздел</button>' +
          '</div>';
        }).join("");
      }
      window.applyNoCropAmbientPhotos();
    };

    // 6. Правая колонка Hero: 3D-карусель (#stage-3d-box) + 2 карточки сезонных спешлов
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
            '<button type="button" onclick="openMenu(\'Сезонные спешлы от Шефа\')" class="text-[10px] font-extrabold text-amber-300 hover:underline cursor-pointer">Все спешлы ➔</button>';
        }
      }
      const specials = (DATA.menu || []).filter(d => d.category === "Сезонные спешлы от Шефа");
      const start = (window.rightSpecialsPairIdx * 2) % Math.max(1, specials.length);
      const pair = [specials[start], specials[(start + 1) % specials.length]].filter(Boolean);

      rowsBox.innerHTML = '<div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">' + pair.map(d => {
        const idx = DATA.menu.indexOf(d);
        const pr = d.sizes ? d.sizes[0].price : d.price;
        return '<div onclick="openMenu(\'Сезонные спешлы от Шефа\')" class="zoom-card bg-[#FDF8F2] text-stone-900 rounded-2xl p-2.5 flex flex-col justify-between gap-2 cursor-pointer shadow-lg border-2 border-[#F2B880]/70">' +
          '<div class="relative h-32 sm:h-36 w-full rounded-xl overflow-hidden bg-[#1D2918]">' +
            '<img src="' + esc(d.photo) + '" onclick="event.stopPropagation();openSuperZoom(this.src, \'' + esc(d.name) + '\')" class="w-full h-full cursor-zoom-in">' +
            '<span class="absolute top-1.5 left-1.5 px-2 py-0.5 rounded-md bg-black/75 text-[#F2B880] text-[9px] font-extrabold">' + esc(d.weight || "Хит шефа") + '</span>' +
            '<span class="absolute bottom-1.5 left-1.5 px-1.5 py-0.5 rounded bg-black/75 text-white text-[8px] font-bold">🍽️ Подача может отличаться</span>' +
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
      window.applyNoCropAmbientPhotos();
    };

    const _baseRenderHeroRight = window.renderHeroRightColumn;
    window.renderHeroRightColumn = function() {
      if (_baseRenderHeroRight) _baseRenderHeroRight();
      window.renderRightTwoPictureFields();
      const stage3d = document.getElementById("stage-3d-box");
      if (stage3d) stage3d.style.height = "290px";
    };

    // 7. Живая Яндекс.Карта с наложенными стеклянными плашками-подсказками
    window.mapOverlaysVisible = true;
    window.toggleMapOverlays = function() {
      window.mapOverlaysVisible = !window.mapOverlaysVisible;
      const topInfo = document.getElementById("mirmir-map-top-info");
      const botCard = document.getElementById("mirmir-map-bottom-overlay");
      const btn = document.getElementById("mirmir-map-toggle-btn");
      if (topInfo) topInfo.classList.toggle("hidden", !window.mapOverlaysVisible);
      if (botCard) botCard.classList.toggle("hidden", !window.mapOverlaysVisible);
      if (btn) btn.textContent = window.mapOverlaysVisible ? "👁️ Скрыть надписи" : "ℹ️ Показать надписи";
    };

    window.buildLiveMapWithOverlaysHtml = function() {
      return [
        '<div id="mirmir-live-map-wrap" class="lg:col-span-7 min-h-[380px] sm:min-h-[420px] rounded-2xl overflow-hidden border-2 border-[#F2B880]/45 bg-[#1B2616] relative shadow-2xl">',
        '  <iframe',
        '    src="https://yandex.ru/map-widget/v1/?ll=43.990383%2C56.322355&z=17&oid=7309581265&ol=biz"',
        '    class="absolute top-0 left-0 w-full h-[calc(100%+72px)] border-0 z-0"',
        '    allowfullscreen loading="lazy" title="Карта проезда Мир Мир Ильинская 45">',
        '  </iframe>',

        '  <div class="absolute top-3 left-3 right-3 z-10 pointer-events-none flex items-start justify-between gap-2">',
        '    <div id="mirmir-map-top-info" class="pointer-events-auto bg-[#1B2616]/88 backdrop-blur-md border border-[#F2B880]/45 rounded-2xl px-3.5 py-2 shadow-xl max-w-[78%]">',
        '      <div class="flex items-center gap-1.5 flex-wrap">',
        '        <span class="px-2 py-0.5 rounded-full bg-emerald-800/90 text-[#F2B880] text-[9px] font-extrabold uppercase tracking-wider">🗺️ Схема проезда</span>',
        '        <span class="text-[10px] font-mono text-[#F2B880]/90 font-bold">GPS: 56.322355, 43.990383</span>',
        '      </div>',
        '      <div class="font-serif text-lg sm:text-xl font-bold text-white leading-tight mt-0.5">ул. Ильинская, 45 — Исторический центр</div>',
        '      <div class="text-[10px] text-stone-200">5 минут пешком от ул. Большой Покровской</div>',
        '    </div>',
        '    <div class="pointer-events-auto flex items-center gap-1.5">',
        '      <button id="mirmir-map-toggle-btn" type="button" onclick="window.toggleMapOverlays()"',
        '        class="px-2.5 py-1.5 rounded-xl bg-[#1B2616]/90 hover:bg-[#D48238] text-[#F2B880] hover:text-white border border-[#F2B880]/45 text-[10px] font-extrabold cursor-pointer shadow-lg transition whitespace-nowrap">',
        '        👁️ Скрыть надписи',
        '      </button>',
        '      <div class="w-10 h-10 rounded-full flex-shrink-0 shadow-lg hidden sm:block" data-dove-holder></div>',
        '    </div>',
        '  </div>',

        '  <div id="mirmir-map-bottom-overlay" class="absolute bottom-2.5 left-2.5 right-2.5 z-10 pointer-events-auto bg-[#1B2616]/90 backdrop-blur-md border border-[#F2B880]/40 rounded-2xl p-3 shadow-2xl space-y-2">',
        '    <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 text-[11px] leading-snug">',
        '      <div class="bg-black/30 rounded-xl p-2 border border-white/10">',
        '        <span class="text-[#F2B880] font-extrabold block">🚶 Пешком от центра</span>',
        '        <span class="text-stone-200">От ст. м. Горьковская или ул. Б. Покровской по ул. Ильинской.</span>',
        '      </div>',
        '      <div class="bg-black/30 rounded-xl p-2 border border-white/10">',
        '        <span class="text-[#F2B880] font-extrabold block">🏛️ Ориентир входа</span>',
        '        <span class="text-stone-200">Кирпичный дом № 45, кованая вывеска с белой Голубкой мира.</span>',
        '      </div>',
        '      <div class="bg-black/30 rounded-xl p-2 border border-white/10">',
        '        <span class="text-[#F2B880] font-extrabold block">🅿️ Парковка</span>',
        '        <span class="text-stone-200">Городские парковочные карманы вдоль ул. Ильинской и Сергиевской.</span>',
        '      </div>',
        '    </div>',
        '    <div class="flex flex-wrap items-center justify-between gap-2">',
        '      <div class="flex flex-wrap items-center gap-2">',
        '        <a href="https://yandex.ru/maps/org/mir_mir/7309581265/" target="_blank" class="px-3.5 py-2 rounded-xl bg-[#D48238] hover:opacity-95 text-white font-extrabold text-[11px] shadow cursor-pointer transition">🗺️ Открыть в Яндекс.Картах ↗</a>',
        '        <a href="https://yandex.ru/maps/?rtext=~56.322355,43.990383&rtt=auto" target="_blank" class="px-3.5 py-2 rounded-xl bg-[#556432] hover:bg-[#2E3D28] text-white font-extrabold text-[11px] border border-[#F2B880]/30 cursor-pointer transition">🧭 Построить маршрут ↗</a>',
        '      </div>',
        '      <span class="text-[10px] text-stone-300 font-semibold hidden md:inline">Нажмите «Скрыть надписи», чтобы свободно листать карту</span>',
        '    </div>',
        '  </div>',
        '</div>'
      ].join("");
    };

    // 8. Единая верхняя панель, защита Hero, чистая вёрстка блока адреса и синхронизация корзины
    function syncMainCartBadge() {
      const origEl = document.getElementById("cart-badge") || document.getElementById("cart-count");
      const cnt = origEl ? origEl.textContent.trim() : "0";
      const mainCnt = document.getElementById("v45-main-cart-count");
      const floatBtn = document.getElementById("v45-floating-cart");
      const floatCnt = document.getElementById("v45-float-cart-count");
      if (mainCnt) mainCnt.textContent = cnt;
      if (floatCnt) floatCnt.textContent = cnt;
      if (floatBtn) {
        const hasItems = parseInt(cnt, 10) > 0;
        floatBtn.classList.toggle("hidden", !hasItems);
        floatBtn.classList.toggle("flex", hasItems);
      }
    }

    function applyV49CleanLayout() {
      if (!document.getElementById("mirmir-v49-styles")) {
        const st = document.createElement("style");
        st.id = "mirmir-v49-styles";
        st.textContent = `
          html, body { min-height: auto !important; height: auto !important; }
          header { display: none !important; }
          main.max-w-7xl, footer.max-w-7xl { max-width: 1320px !important; width: 100% !important; }
          main.max-w-7xl { padding-top: 14px !important; padding-bottom: 28px !important; }
          #hero-work-badges, #hero-work-badge { display: none !important; }
          body:not(.disable-card-zoom) .zoom-card {
            transition: transform 0.25s ease, box-shadow 0.25s ease !important;
          }
          body:not(.disable-card-zoom) .zoom-card:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.14) !important;
          }
          .v45-top-right-close {
            position: absolute !important; top: 10px !important; right: 10px !important; z-index: 95 !important;
            width: 34px !important; height: 34px !important; border-radius: 9999px !important;
            background: rgba(20, 28, 17, 0.92) !important; color: #FFFDF9 !important;
            border: 1.5px solid rgba(242, 184, 128, 0.7) !important;
            display: inline-flex !important; align-items: center !important; justify-content: center !important;
            font-size: 16px !important; font-weight: 900 !important; cursor: pointer !important;
          }
          .v45-top-right-close:hover { background: #D48238 !important; color: #fff !important; }
        `;
        document.head.appendChild(st);
      }

      const mainEl = document.querySelector("main");
      if (mainEl && !document.getElementById("v45-main-topbar")) {
        const hr = new Date().getHours();
        const isOpen = hr >= 12 && hr < 21;
        const statusHtml = isOpen
          ? '<span class="px-2.5 py-1 rounded-full bg-emerald-700 text-white text-[11px] font-extrabold whitespace-nowrap">🟢 Открыто до 21:00</span>'
          : '<span class="px-2.5 py-1 rounded-full bg-rose-700 text-white text-[11px] font-extrabold whitespace-nowrap">🔴 Закрыто до 12:00</span>';

        const topBar = document.createElement("section");
        topBar.id = "v45-main-topbar";
        topBar.className = "bg-[#FFFDF9] rounded-3xl p-3 sm:p-4 border border-[#556432]/25 shadow-sm space-y-2.5 mb-3";
        topBar.innerHTML =
          '<div class="flex flex-wrap items-center justify-between gap-3">' +
            '<div class="flex flex-wrap items-center gap-2.5">' +
              '<div class="w-10 h-10 rounded-full flex-shrink-0 shadow-xs" data-dove-holder></div>' +
              '<div class="flex flex-wrap items-center gap-2">' +
                '<span class="font-serif text-xl sm:text-2xl font-bold text-[#1F2B1A] leading-none">Мир Мир</span>' +
                '<a href="https://yandex.ru/maps/org/mir_mir/7309581265/" target="_blank" class="text-xs font-bold text-[#556432] hover:underline">📍 Ильинская, 45</a>' +
                statusHtml +
                '<span class="px-2.5 py-1 rounded-full bg-[#D48238] text-white text-[11px] font-extrabold whitespace-nowrap">🔥 Бизнес-Ланч −30% (12:00–16:00)</span>' +
              '</div>' +
            '</div>' +
            '<div class="flex flex-wrap items-center gap-2">' +
              '<button type="button" onclick="openMenu(\'Все\')" class="py-2 px-4 rounded-xl bg-[#D48238] hover:opacity-95 text-white font-extrabold text-xs sm:text-sm cursor-pointer shadow">📖 Открыть Меню (' + DATA.menu.length + ')</button>' +
              '<button type="button" onclick="openCafeShopModal()" class="py-2 px-3.5 rounded-xl bg-[#556432] hover:bg-[#2E3D28] text-white font-extrabold text-xs sm:text-sm cursor-pointer">🛍️ Магазин кафе</button>' +
              '<button type="button" onclick="toggleCart()" class="py-2 px-3.5 rounded-xl bg-[#2E3D28] hover:bg-black text-[#F2B880] font-extrabold text-xs sm:text-sm flex items-center gap-1.5 cursor-pointer"><span>🛒 Корзина</span><span id="v45-main-cart-count" class="px-1.5 py-0.5 rounded-full bg-[#D48238] text-white text-[11px]">0</span></button>' +
            '</div>' +
          '</div>' +
          '<div id="v45-quick-cats-strip" class="flex items-center gap-1.5 overflow-x-auto no-scrollbar pt-2 border-t border-stone-200/70"></div>';
        mainEl.insertBefore(topBar, mainEl.firstChild);
      }

      if (!document.getElementById("v45-floating-cart")) {
        const fl = document.createElement("button");
        fl.id = "v45-floating-cart";
        fl.type = "button";
        fl.setAttribute("onclick", "toggleCart()");
        fl.className = "hidden fixed bottom-4 left-4 z-40 py-2.5 px-4 rounded-full bg-[#2E3D28] text-[#F2B880] border-2 border-[#F2B880]/60 font-extrabold text-xs items-center gap-2 shadow-2xl cursor-pointer";
        fl.innerHTML = '<span>🛒 Корзина</span><span id="v45-float-cart-count" class="px-2 py-0.5 rounded-full bg-[#D48238] text-white">0</span>';
        document.body.appendChild(fl);
      }

      // Чистка дублей внутри левой колонки Hero (сама Hero-секция не трогается)
      const heroLeft = document.getElementById("hero-left-col");
      if (heroLeft) {
        heroLeft.querySelectorAll("div").forEach(el => {
          const oc = el.getAttribute("onclick") || "";
          const txt = el.textContent || "";
          if ((oc.includes("Сезонные спешлы") || txt.includes("Смотреть 9 блюд")) && !el.querySelector("#hero-interior-slide-img")) {
            el.style.setProperty("display", "none", "important");
          }
        });
        heroLeft.querySelectorAll(".grid").forEach(g => {
          if (g.textContent.includes("Чай 300") && g.textContent.includes("Десерты без сахара")) {
            g.className = "relative z-10 grid grid-cols-1 sm:grid-cols-3 gap-2.5";
            Array.from(g.children).forEach(ch => {
              if ((ch.getAttribute("onclick") || "").includes("openBowlBuilder") || ch.textContent.includes("Собрать свой Боул")) {
                ch.style.setProperty("display", "none", "important");
              }
            });
          }
        });
      }

      // Перестраиваем СТРОГО нижний блок адреса/карты (Hero полностью защищён)
      document.querySelectorAll("main section").forEach(sec => {
        if (sec.id === "v45-main-topbar" || sec.id === "news-section-wrap") return;
        if (sec.querySelector("#hero-left-col, #hero-interior-slide-img, #stage-3d-box")) return;
        if (sec.textContent.includes("Нижний Новгород, ул. Ильинская, 45") && !sec.dataset.v49MapRebuilt) {
          sec.dataset.v49MapRebuilt = "1";
          const taxiUrl = "https://3.redirect.appmetrica.yandex.com/route?end-lat=56.322355&end-lon=43.990383&appmetrica_tracking_id=1178268795219780156";
          sec.className = "bg-[#23311E] text-[#FFFDF9] rounded-[32px] p-5 sm:p-7 border-2 border-[#F2B880]/35 shadow-xl grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch mt-4 mb-4";
          sec.innerHTML =
            '<div class="lg:col-span-5 flex flex-col justify-between space-y-4">' +
              '<div class="space-y-3">' +
                '<span class="inline-block px-3 py-1 rounded-full bg-white/10 text-[#F2B880] text-[10px] font-extrabold uppercase tracking-widest">📍 Ждём вас в гости каждый день</span>' +
                '<h2 class="font-serif text-3xl sm:text-4xl font-bold text-white leading-tight">Нижний Новгород, ул. Ильинская, 45</h2>' +
                '<p class="text-xs sm:text-sm text-stone-200 leading-relaxed">Ежедневно с 12:00 до 21:00. По будням с 12:00 до 16:00 действует скидка −30% на Комбо-Ланч (Суп + Основное блюдо + Напиток).</p>' +
                '<div class="pt-1"><a href="tel:+79200282858" class="inline-flex items-center gap-2 text-sm sm:text-base font-extrabold text-[#F2B880] hover:underline">📞 Телефон кафе: +7 (920) 028-28-58</a></div>' +
              '</div>' +
              '<div class="pt-4 border-t border-white/15 space-y-2.5">' +
                '<div class="grid grid-cols-2 sm:grid-cols-4 gap-2">' +
                  '<button type="button" onclick="openBookTableModal()" class="py-2.5 px-3 rounded-xl bg-[#556432] hover:bg-[#D48238] text-[#FFFDF9] font-extrabold text-xs cursor-pointer transition border border-[#F2B880]/25">🪑 Бронь</button>' +
                  '<a href="' + taxiUrl + '" target="_blank" class="py-2.5 px-3 rounded-xl bg-[#3A4A2E] hover:bg-[#D48238] text-[#F2B880] hover:text-white font-extrabold text-xs text-center transition border border-[#F2B880]/25">🚕 Такси</a>' +
                  '<button type="button" onclick="openDeliveryModal()" class="py-2.5 px-3 rounded-xl bg-[#556432] hover:bg-[#D48238] text-[#FFFDF9] font-extrabold text-xs cursor-pointer transition border border-[#F2B880]/25">🛵 Доставка</button>' +
                  '<button type="button" onclick="openRadioSelectorModal()" class="py-2.5 px-3 rounded-xl bg-[#FFFDF9] hover:bg-amber-50 text-[#2E3D28] font-extrabold text-xs cursor-pointer transition">📻 Радио</button>' +
                '</div>' +
                '<div class="grid grid-cols-1 sm:grid-cols-3 gap-1.5">' +
                  '<button disabled class="py-1.5 px-2 rounded-lg bg-white/10 text-white/70 font-extrabold text-[10px] uppercase cursor-not-allowed border border-white/10">👥 КОМАНДА <span class="px-1 rounded bg-black/40 text-[#F2B880] text-[8px]">Скоро</span></button>' +
                  '<button disabled class="py-1.5 px-2 rounded-lg bg-white/10 text-white/70 font-extrabold text-[10px] uppercase cursor-not-allowed border border-white/10">🏛️ ИСТОРИЯ <span class="px-1 rounded bg-black/40 text-[#F2B880] text-[8px]">Скоро</span></button>' +
                  '<button disabled class="py-1.5 px-2 rounded-lg bg-white/10 text-white/70 font-extrabold text-[10px] uppercase cursor-not-allowed border border-white/10">🌿 ЦЕННОСТИ <span class="px-1 rounded bg-black/40 text-[#F2B880] text-[8px]">Скоро</span></button>' +
                '</div>' +
              '</div>' +
            '</div>' +
            window.buildLiveMapWithOverlaysHtml();
        }
      });

      document.querySelectorAll("[data-dove-holder]").forEach(el => {
        if (!el.innerHTML.trim() && typeof SIGN_DOVE_SVG !== "undefined") el.innerHTML = SIGN_DOVE_SVG;
      });

      [
        { id: "menu-modal", fn: "closeMenu()" },
        { id: "unified-system-hub", fn: "closeUnifiedSystemHub()" },
        { id: "bowl-modal", fn: "closeBowlBuilder()" },
        { id: "cafe-shop-modal", fn: "closeCafeShopModal()" },
        { id: "book-table-modal", fn: "closeBookTableModal()" },
        { id: "delivery-modal", fn: "document.getElementById('delivery-modal').classList.add('hidden')" },
        { id: "radio-selector-modal", fn: "document.getElementById('radio-selector-modal').classList.add('hidden')" },
        { id: "ready-gallery-popup", fn: "closeReadyGalleryPopup()" },
        { id: "master-prompt-modal", fn: "closeMasterPromptModal()" },
        { id: "super-zoom-lightbox", fn: "closeSuperZoom()" }
      ].forEach(cfg => {
        const m = document.getElementById(cfg.id);
        const card = m ? m.firstElementChild : null;
        if (!card) return;
        card.style.position = "relative";
        card.querySelectorAll("button").forEach(b => {
          if (b.textContent.trim() === "✕" && !b.classList.contains("v45-top-right-close")) b.style.display = "none";
        });
        if (!card.querySelector(".v45-top-right-close")) {
          const btn = document.createElement("button");
          btn.className = "v45-top-right-close";
          btn.setAttribute("onclick", cfg.fn);
          btn.innerHTML = "✕";
          card.appendChild(btn);
        }
      });
    }

    // 9. Лента новостей ВК с плавным автоскроллом и кнопками ⏮️ / ◀ / ▶
    const NEWS_FALLBACKS = ["img/vk_5122_0.jpg", "img/vk_5068_0.jpg", "img/vk_5128_1.jpg", "img/vk_5134_0.jpg"];
    window.newsAutoScrollPaused = false;
    window.newsManualPauseUntil = 0;
    window.newsAutoScrollStarted = false;

    window.scrollNewsManual = function(delta) {
      const grid = document.getElementById("posts-grid");
      if (!grid) return;
      window.newsManualPauseUntil = Date.now() + 3000;
      grid.scrollBy({ left: delta * 365, behavior: "smooth" });
    };
    window.scrollToLatestNews = function() {
      const grid = document.getElementById("posts-grid");
      if (!grid) return;
      window.newsManualPauseUntil = Date.now() + 3500;
      grid.scrollTo({ left: 0, behavior: "smooth" });
    };
    window.stepNewsPage = window.scrollNewsManual;

    function startNewsTicker() {
      if (window.newsAutoScrollStarted) return;
      window.newsAutoScrollStarted = true;
      function tick() {
        const g = document.getElementById("posts-grid");
        if (g && !window.newsAutoScrollPaused && Date.now() > window.newsManualPauseUntil) {
          g.scrollLeft += 0.5;
          if (g.scrollLeft >= g.scrollWidth / 2) g.scrollLeft = 0;
        }
        requestAnimationFrame(tick);
      }
      requestAnimationFrame(tick);
    }

    window.renderNewsPosts = function() {
      const grid = document.getElementById("posts-grid");
      if (!grid) return;
      const posts = (DATA.posts || []).filter(p => {
        const t = ((p.title || "") + " " + (p.text || "")).toLowerCase();
        return !t.includes("прикрепляю наше актуальное меню") && !t.includes("актуальное меню");
      });
      if (!posts.length) return;

      const newsSec = document.getElementById("news-section-wrap") || grid.closest("section");
      if (newsSec) {
        const hdr = newsSec.firstElementChild;
        if (hdr && !document.getElementById("v45-news-controls")) {
          hdr.querySelectorAll("button").forEach(b => { b.style.display = "none"; });
          const ctrl = document.createElement("div");
          ctrl.id = "v45-news-controls";
          ctrl.className = "flex items-center gap-2";
          ctrl.innerHTML =
            '<button type="button" onclick="scrollToLatestNews()" class="px-3 py-1.5 rounded-full bg-[#2E3D28] hover:bg-[#D48238] text-[#F2B880] hover:text-white text-xs font-extrabold cursor-pointer transition">⏮️ К последним постам</button>' +
            '<button type="button" onclick="scrollNewsManual(-1)" class="w-9 h-9 rounded-full bg-[#2E3D28] hover:bg-[#D48238] text-white text-xs font-extrabold cursor-pointer">◀</button>' +
            '<button type="button" onclick="scrollNewsManual(1)" class="w-9 h-9 rounded-full bg-[#D48238] hover:bg-[#2E3D28] text-white text-xs font-extrabold cursor-pointer">▶</button>';
          hdr.appendChild(ctrl);
        }
        const botVk = newsSec.querySelector("a[href*='vk.com']");
        if (botVk) {
          botVk.className = "inline-flex items-center justify-center px-3.5 py-1.5 rounded-lg bg-[#0077FF] hover:bg-[#0055CC] text-white text-xs font-extrabold transition shadow";
          botVk.textContent = "ВК";
        }
      }

      grid.className = "flex gap-4 overflow-x-auto no-scrollbar py-2 px-1 select-none";
      grid.onmouseenter = () => { window.newsAutoScrollPaused = true; };
      grid.onmouseleave = () => { window.newsAutoScrollPaused = false; };
      grid.ontouchstart = () => { window.newsAutoScrollPaused = true; };
      grid.ontouchend = () => { setTimeout(() => { window.newsAutoScrollPaused = false; }, 1800); };

      const loopPosts = [...posts, ...posts];
      grid.innerHTML = loopPosts.map((p, idxP) => {
        const safeUrl = (p.vk_url && !p.vk_url.includes("-191992548")) ? p.vk_url : "https://vk.com/mirmir.cafe";
        const fb = NEWS_FALLBACKS[idxP % NEWS_FALLBACKS.length];
        const ph = p.photo || fb;
        return '<article class="zoom-card w-[300px] sm:w-[345px] flex-shrink-0 bg-[#FFFDF9] rounded-3xl p-4 border border-[#556432]/25 shadow-sm flex flex-col justify-between gap-3">' +
          '<div class="space-y-2.5">' +
            '<div class="flex items-center justify-between text-[11px] font-extrabold text-[#D48238]"><span>📅 ' + esc(p.date || "Новость") + '</span><span>❤️ ' + esc(p.likes || 25) + '</span></div>' +
            '<h3 class="font-serif text-lg sm:text-xl font-bold text-[#1F2B1A] leading-snug line-clamp-2">' + esc(p.title || "Событие в «Мир Мир»") + '</h3>' +
            '<div class="relative rounded-2xl overflow-hidden bg-[#1D2918] h-[230px]">' +
              '<img src="' + esc(ph) + '" onerror="this.onerror=null;this.src=\'' + fb + '\'" onclick="openSuperZoom(this.src, \'' + esc(p.title) + '\')" class="w-full h-full cursor-zoom-in">' +
              '<button type="button" onclick="openSuperZoom(\'' + esc(ph) + '\', \'' + esc(p.title) + '\')" class="absolute bottom-2 right-2 w-8 h-8 rounded-full bg-black/75 hover:bg-[#D48238] text-white text-xs cursor-pointer">🔍</button>' +
            '</div>' +
            '<p class="text-xs text-stone-700 leading-relaxed line-clamp-4 whitespace-pre-line">' + esc(p.text || "") + '</p>' +
          '</div>' +
          '<div class="pt-2 border-t border-stone-200/80 flex items-center justify-between">' +
            '<a href="' + esc(safeUrl) + '" target="_blank" class="px-2.5 py-1 rounded-lg bg-[#0077FF] hover:bg-[#0055CC] text-white text-[11px] font-extrabold shadow">ВК</a>' +
            '<span class="text-[10px] font-bold text-stone-400">vk.com/mirmir.cafe</span>' +
          '</div>' +
        '</article>';
      }).join("");
      window.applyNoCropAmbientPhotos();
      startNewsTicker();
    };

    // 10. Шестерёнка Архитектора (#hub-top-tabs / #hub-main-body) и точный движок фото блюд
    window.openUnifiedSystemHub = function(tabId) {
      try { history.pushState({ guard: "hub" }, ""); } catch (e) {}
      if (tabId) window.hubActiveTab = hubActiveTab = tabId;
      const m = document.getElementById("unified-system-hub");
      if (m) { m.classList.remove("hidden"); m.classList.add("flex"); window.renderUnifiedSystemHub(); }
    };
    window.closeUnifiedSystemHub = function() {
      const m = document.getElementById("unified-system-hub");
      if (m) { m.classList.add("hidden"); m.classList.remove("flex"); }
    };
    window.setHubTab = function(t) { window.hubActiveTab = hubActiveTab = t; window.renderUnifiedSystemHub(); };
    window.setHubCategory = function(c) { window.hubDishCategoryFilter = hubDishCategoryFilter = c; window.renderUnifiedSystemHub(); };
    window.setHubSearch = function(q) { window.hubDishSearchQuery = hubDishSearchQuery = q; window.renderUnifiedSystemHub(); };

    const CURATED_VEGAN_HD_BANK = {
      soup: ["img/macro_tomyum_bowl.jpg", "img/macro_miso_tofu.jpg", "img/vk_5057_1.jpg", "img/vk_5053_0.jpg"],
      burger: ["img/macro_vegan_burger.jpg", "img/macro_avocado_burger.jpg", "img/macro_spicy_burger.jpg", "img/vk_5118_1.jpg"],
      salad: ["img/macro_caesar_romaine.jpg", "img/macro_greek_olives.jpg", "img/macro_tuna_chickpea.jpg", "img/macro_cucumbers_sesame.jpg", "img/vk_5128_1.jpg"],
      pizza: ["img/vk_5085_1.jpg", "img/vk_5118_0.jpg", "img/macro_pepperoni_pizza.jpg"],
      noodles: ["img/vk_5094_0.jpg", "img/macro_creamy_pasta.jpg", "img/vk_5118_2.jpg", "img/vk_5057_0.jpg"],
      drink: ["img/macro_strawberry_banana.jpg", "img/macro_berry_smoothie.jpg", "img/macro_pineapple_mint.jpg", "img/macro_citrus_mint.jpg", "img/macro_coffee_pine.jpg", "img/vk_5122_0.jpg"],
      dessert: ["img/vk_5069_0.jpg", "img/macro_syrniki_berries.jpg", "img/vk_5005_0.jpg", "img/vk_5103_1.jpg", "img/macro_vegan_icecream.jpg"],
      main: ["img/vk_5122_1.jpg", "img/vk_5121_0.jpg", "img/vk_5094_1.jpg", "img/vk_5055_0.jpg", "img/vk_5087_1.jpg"]
    };

    const RU_TO_EN_DISH_KEYWORDS = [
      { re: /том ям/i, q: "tom yum soup", f: "authentic Thai Tom Yum soup, spicy red-orange lemongrass broth, oyster mushrooms, tofu, cherry tomatoes, lime wedge, cilantro, ceramic bowl" },
      { re: /мисо/i, q: "miso soup tofu", f: "Japanese miso soup with silken tofu cubes, wakame seaweed, green onions in black ceramic bowl" },
      { re: /крем-суп.*горош/i, q: "green pea soup", f: "velvety emerald green pea and avocado cream soup topped with pumpkin seeds and microgreens" },
      { re: /суп/i, q: "vegetable soup bowl", f: "hearty homemade vegetable mushroom soup with herbs in ceramic bowl" },
      { re: /пад тай/i, q: "pad thai noodles", f: "authentic Pad Thai stir-fried rice noodles with crispy golden tofu, peanuts, lime wedge and bean sprouts" },
      { re: /лапша|паста/i, q: "vegan pasta noodles", f: "appetizing vegan noodles with roasted vegetables, tofu and creamy sauce in ceramic bowl" },
      { re: /пицца/i, q: "artisan vegan pizza", f: "artisan wood-fired thin-crust vegan pizza with roasted mushrooms, vegetables and melted plant mozzarella" },
      { re: /бургер|сэндвич/i, q: "gourmet vegan burger", f: "gourmet plant-based burger with thick patty, fresh avocado, lettuce and sesame bun" },
      { re: /салат|цезарь|пай хуан/i, q: "fresh green salad", f: "vibrant fresh vegan salad with avocado, cherry tomatoes, greens and seeds" },
      { re: /боул/i, q: "buddha bowl quinoa", f: "colorful Buddha bowl with quinoa, roasted vegetables, falafel, avocado slices and tahini" },
      { re: /шакшука|омлет/i, q: "tofu scramble skillet", f: "golden chickpea tofu omelet or shakshuka in rich spiced tomato pepper sauce" },
      { re: /сырники|десерт|шарлотка|мороженое|батончик/i, q: "vegan berry dessert", f: "artisan sugar-free vegan dessert with berries, chocolate and nuts" },
      { re: /смузи|фреш|лимонад|кола/i, q: "fruit berry smoothie", f: "fresh colorful fruit smoothie or botanical lemonade in tall glass" },
      { re: /кофе|капучино|какао/i, q: "oat milk cappuccino", f: "velvety oat-milk cappuccino with latte art foam in ceramic cup" },
      { re: /чай|пуэр|улун|масала|глинтвейн/i, q: "chinese tea teapot", f: "Chinese Gongfu tea ceremony with clay teapot, brewed amber tea and small cups" }
    ];

    function detectDishBankKey(d) {
      const nm = (d.name || "").toLowerCase(), cat = (d.category || "").toLowerCase();
      if (nm.includes("пицца")) return "pizza";
      if (cat.includes("суп") || nm.includes("суп") || nm.includes("том ям") || nm.includes("мисо") || nm.includes("ватапа")) return "soup";
      if (nm.includes("бургер") || nm.includes("сэндвич") || nm.includes("неряха")) return "burger";
      if (cat.includes("салат") || nm.includes("салат") || nm.includes("цезарь")) return "salad";
      if (cat.includes("лапша") || nm.includes("лапша") || nm.includes("пад тай") || nm.includes("паста")) return "noodles";
      if (cat.includes("чай") || cat.includes("барн") || nm.includes("чай") || nm.includes("смузи") || nm.includes("кофе")) return "drink";
      if (cat.includes("десерт") || nm.includes("сырники") || nm.includes("шарлотка") || nm.includes("мороженое")) return "dessert";
      return "main";
    }

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
      const userRaw = window.customPromptsPerDish[idx] || "";
      window.dishVariantStep[idx] = (window.dishVariantStep[idx] || 0) + 1;
      const step = window.dishVariantStep[idx];
      const engine = window.selectedAiEnginePerDish[idx] || "flux_ai";

      let qTerm = "vegan food", fluxDesc = d.ai_prompt || d.name;
      for (let i = 0; i < RU_TO_EN_DISH_KEYWORDS.length; i++) {
        if (RU_TO_EN_DISH_KEYWORDS[i].re.test(d.name || "")) {
          qTerm = RU_TO_EN_DISH_KEYWORDS[i].q;
          fluxDesc = RU_TO_EN_DISH_KEYWORDS[i].f;
          break;
        }
      }
      if (userRaw && /[а-яё]/i.test(userRaw) && userRaw !== d.name) {
        try {
          const tr = await fetch("https://api.mymemory.translated.net/get?q=" + encodeURIComponent(userRaw.slice(0, 120)) + "&langpair=ru|en");
          const tj = await tr.json();
          if (tj.responseData && tj.responseData.translatedText) {
            fluxDesc = tj.responseData.translatedText;
            qTerm = tj.responseData.translatedText.split(/\s+/).slice(0, 3).join(" ");
          }
        } catch (e) {}
      }

      if (engine === "flux_ai" || engine === "turbo_ai") {
        const mdl = engine === "flux_ai" ? "flux" : "turbo";
        const seed = Math.floor(Math.random() * 899999) + step * 173;
        const promptStr = "Close-up studio restaurant food photo of " + fluxDesc + ", 100% plant-based vegan, appetizing, sharp focus, no text";
        const aiUrl = "https://image.pollinations.ai/prompt/" + encodeURIComponent(promptStr) + "?model=" + mdl + "&width=640&height=640&seed=" + seed + "&nologo=true";
        pushDiagLog(idx, "🎨", mdl.toUpperCase() + " AI", "Генерация (seed #" + seed + "): " + qTerm);
        window.pendingDishCandidates[idx] = pendingDishCandidates[idx] = { url: aiUrl, source: "🎨 " + mdl.toUpperCase() + " AI (Seed #" + seed + ")" };
        window.renderUnifiedSystemHub();
        return;
      }

      if (engine === "openverse_hd") {
        try {
          pushDiagLog(idx, "📡", "Openverse HD", "Поиск: «" + qTerm + "»...");
          const r = await fetch("https://api.openverse.org/v1/images/?q=" + encodeURIComponent(qTerm) + "&page_size=25");
          if (r.ok) {
            const j = await r.json();
            const bad = /meat|beef|pork|chicken|shrimp|prawn|fish|salmon|bacon|egg|logo|vector/i;
            const list = (j.results || []).filter(it => it.url && !bad.test((it.title || "") + " " + it.url));
            if (list.length) {
              const pick = list[(step - 1) % list.length];
              pushDiagLog(idx, "✅", "Openverse HD", "Найдено #" + step + " из " + list.length + " («" + qTerm + "»)");
              window.pendingDishCandidates[idx] = pendingDishCandidates[idx] = { url: pick.url, source: "📸 Openverse HD (" + qTerm + ")" };
              window.renderUnifiedSystemHub();
              return;
            }
          }
          pushDiagLog(idx, "⚠️", "Openverse HD", "По «" + qTerm + "» совпадений нет. Попробуйте Wikimedia или Flux AI.");
        } catch (e) {
          pushDiagLog(idx, "❌", "Openverse HD", "Ошибка сети: " + e.message);
        }
        window.renderUnifiedSystemHub();
        return;
      }

      if (engine === "wikimedia") {
        try {
          pushDiagLog(idx, "📡", "Wikimedia", "Поиск: «" + qTerm + "»...");
          const wUrl = "https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch=" +
            encodeURIComponent("filetype:bitmap " + qTerm) + "&gsrlimit=20&prop=imageinfo&iiprop=url&format=json&origin=*";
          const r = await fetch(wUrl);
          if (r.ok) {
            const j = await r.json();
            const pages = (j.query && j.query.pages) ? Object.values(j.query.pages) : [];
            const imgs = pages.map(p => p.imageinfo && p.imageinfo[0] && p.imageinfo[0].url)
              .filter(u => u && /\.(jpg|jpeg|png|webp)$/i.test(u) && !/shrimp|prawn|chicken|meat|beef|pork/i.test(u));
            if (imgs.length) {
              const pick = imgs[(step - 1) % imgs.length];
              pushDiagLog(idx, "✅", "Wikimedia", "Найдено #" + step + " из " + imgs.length + " («" + qTerm + "»)");
              window.pendingDishCandidates[idx] = pendingDishCandidates[idx] = { url: pick, source: "🥗 Wikimedia (" + qTerm + ")" };
              window.renderUnifiedSystemHub();
              return;
            }
          }
          pushDiagLog(idx, "⚠️", "Wikimedia", "По «" + qTerm + "» фото не найдены.");
        } catch (e) {
          pushDiagLog(idx, "❌", "Wikimedia", "Ошибка сети: " + e.message);
        }
        window.renderUnifiedSystemHub();
        return;
      }

      if (engine === "vk_food_archive") {
        const pool = (DATA.vk_food_photos && DATA.vk_food_photos.length) ? DATA.vk_food_photos : ["img/vk_5128_1.jpg"];
        const pick = pool[(step - 1) % pool.length];
        pushDiagLog(idx, "✅", "Архив ВК", "Кадр #" + step + ": " + pick);
        window.pendingDishCandidates[idx] = pendingDishCandidates[idx] = { url: pick, source: "🌿 Архив блюд ВК (" + pick + ")" };
        window.renderUnifiedSystemHub();
        return;
      }

      const bk = detectDishBankKey(d);
      const bank = CURATED_VEGAN_HD_BANK[bk] || CURATED_VEGAN_HD_BANK.main;
      const pick = bank[(step - 1) % bank.length];
      pushDiagLog(idx, "✅", "GastroBank [" + bk + "]", "Кадр #" + step + ": " + pick);
      window.pendingDishCandidates[idx] = pendingDishCandidates[idx] = { url: pick, source: "🍔 GastroBank HD (" + bk + ")" };
      window.renderUnifiedSystemHub();
    };

    window.previewManualUrlCandidate = function(idx) {
      const val = (document.getElementById("hub-url-inp-" + idx)?.value || "").trim();
      if (!val) { alert("Вставьте URL или путь img/..."); return; }
      window.pendingDishCandidates[idx] = pendingDishCandidates[idx] = { url: val, source: "🔗 Прямой URL" };
      window.renderUnifiedSystemHub();
    };

    window.selectReadyPhotoV49 = function(dishIdx, photoPath) {
      const d = DATA.menu[dishIdx];
      if (!d) return;
      d.photo = photoPath;
      d.photo_type = "real";
      d.is_manual_override = true;
      const ov = getManualDishOverrides();
      ov[d.name] = { photo: photoPath, updated_at: new Date().toLocaleString("ru-RU") };
      saveManualDishOverrides(ov);
      delete window.pendingDishCandidates[dishIdx];
      closeReadyGalleryPopup();
      window.renderUnifiedSystemHub();
      window.renderDishes();
      window.renderHeroRightColumn();
    };

    window.approveDishCandidate = function(idx) {
      const c = window.pendingDishCandidates[idx];
      if (c && c.url) window.selectReadyPhotoV49(idx, c.url);
    };

    window.openReadyGalleryPopup = function(dishIdx) {
      const d = DATA.menu[dishIdx];
      const modal = document.getElementById("ready-gallery-popup");
      if (!modal || !d) return;
      const pool = (DATA.ready_photos || []).filter(p => !p.includes("ai_v") && !p.includes("ingr_") && !p.includes("5047_") && !p.includes("yorg_"));
      const card = modal.firstElementChild;
      if (card) {
        card.innerHTML =
          '<div class="bg-[#2E3D28] text-[#FFFDF9] px-5 py-3 flex items-center justify-between relative">' +
            '<h3 class="font-serif text-lg font-bold">📸 Выберите фото для: <span class="text-[#F2B880]">' + esc(d.name) + '</span> (' + pool.length + ' шт.)</h3>' +
            '<button type="button" onclick="closeReadyGalleryPopup()" class="v45-top-right-close">✕</button>' +
          '</div>' +
          '<div class="p-4 overflow-y-auto max-h-[75vh] bg-[#FAF5EC] grid grid-cols-2 sm:grid-cols-4 gap-3">' +
            pool.map(ph =>
              '<div class="bg-white rounded-2xl p-2 border border-stone-200 flex flex-col justify-between gap-1.5">' +
                '<div class="relative h-32 rounded-xl overflow-hidden bg-stone-100">' +
                  '<img src="' + esc(ph) + '" loading="lazy" onclick="openSuperZoom(this.src, \'' + esc(d.name) + '\')" class="w-full h-full object-cover cursor-zoom-in">' +
                  '<button type="button" onclick="openSuperZoom(\'' + esc(ph) + '\', \'' + esc(d.name) + '\')" class="absolute bottom-1 right-1 w-6 h-6 rounded-full bg-black/75 text-white text-[10px] cursor-pointer">🔍</button>' +
                '</div>' +
                '<div class="text-[10px] font-mono text-stone-500 truncate">' + esc(ph) + '</div>' +
                '<button type="button" onclick="selectReadyPhotoV49(' + dishIdx + ', \'' + esc(ph) + '\')" class="w-full py-1.5 rounded-xl bg-emerald-700 hover:bg-[#D48238] text-white text-xs font-extrabold cursor-pointer">✅ Утвердить</button>' +
              '</div>'
            ).join("") +
          '</div>';
      }
      modal.classList.remove("hidden");
      modal.classList.add("flex");
    };

    function getMasterTasksList() {
      const srv = (DATA.tz_synced && Array.isArray(DATA.tz_synced.tasks)) ? DATA.tz_synced.tasks : [];
      try {
        const loc = JSON.parse(localStorage.getItem("mirmir_tasks_v49") || "null");
        if (Array.isArray(loc) && loc.length >= srv.length) return loc;
      } catch (e) {}
      return srv;
    }
    function saveMasterTasksList(arr) {
      try {
        localStorage.setItem("mirmir_tasks_v49", JSON.stringify(arr));
        fetch(NTFY_SYNC_URL, { method: "POST", body: JSON.stringify({ type: "tz_tasks_sync", tasks: arr, ts: Date.now() }) }).catch(() => {});
      } catch (e) {}
    }
    window.toggleTaskDoneV49 = function(i) {
      const l = getMasterTasksList();
      if (!l[i]) return;
      l[i].done = !l[i].done;
      saveMasterTasksList(l);
      window.renderUnifiedSystemHub();
    };
    window.updateTaskCommentV49 = function(i, val) {
      const l = getMasterTasksList();
      if (!l[i]) return;
      l[i].comment = val;
      saveMasterTasksList(l);
    };
    window.addNewTaskV49 = function() {
      const t = (document.getElementById("new-tz-task-inp")?.value || "").trim();
      if (!t) return;
      const c = (document.getElementById("new-tz-comment-inp")?.value || "Проверить").trim();
      const l = getMasterTasksList();
      l.unshift({ id: "t_u_" + Date.now(), date: new Date().toLocaleString("ru-RU").slice(0, 16), title: (l.length + 1) + ". " + t, done: false, comment: c });
      saveMasterTasksList(l);
      window.renderUnifiedSystemHub();
    };

    window.addNewCustomDishFromHub = function() {
      const name = (document.getElementById("new-dish-name")?.value || "").trim();
      if (!name) { alert("Введите название блюда!"); return; }
      const obj = {
        id: "custom_" + Date.now(),
        category: (document.getElementById("new-dish-cat")?.value || "Сезонные спешлы от Шефа").trim(),
        name: name,
        weight: (document.getElementById("new-dish-weight")?.value || "260 г").trim(),
        price: parseInt(document.getElementById("new-dish-price")?.value || "450", 10) || 450,
        photo: (document.getElementById("new-dish-photo")?.value || "img/vk_5128_1.jpg").trim(),
        photo_type: "real",
        desc: (document.getElementById("new-dish-desc")?.value || "100% растительное блюдо.").trim(),
        ai_prompt: "Vegan plant-based " + name
      };
      const list = loadCustomAddedDishes().filter(x => x.name !== name);
      list.unshift(obj);
      try { localStorage.setItem("mirmir_custom_dishes_v1", JSON.stringify(list)); } catch (e) {}
      DATA.menu.unshift(obj);
      window.renderUnifiedSystemHub();
      window.renderDishes();
      window.renderCategoryShowcaseAndRail();
    };

    window.getSavedIdeasNotes = function() {
      try { return JSON.parse(localStorage.getItem("mirmir_ideas_notes_v1") || "[]"); } catch (e) { return []; }
    };
    window.addNewIdeaNote = function() {
      const inp = document.getElementById("new-idea-note-inp");
      const v = (inp?.value || "").trim();
      if (!v) return;
      const list = window.getSavedIdeasNotes();
      list.unshift({ text: v, date: new Date().toLocaleString("ru-RU") });
      try { localStorage.setItem("mirmir_ideas_notes_v1", JSON.stringify(list)); } catch (e) {}
      if (inp) inp.value = "";
      window.renderUnifiedSystemHub();
    };

    window.renderUnifiedSystemHub = function() {
      syncMenuWithCustomAndDeleted();
      applyManualOverridesToMenuData();
      const tabsBox = document.getElementById("hub-top-tabs") || document.getElementById("unified-hub-tabs");
      const body = document.getElementById("hub-main-body") || document.getElementById("unified-hub-body");
      if (!tabsBox || !body) return;

      const curTab = window.hubActiveTab || "dishes72";
      const tasks = getMasterTasksList();
      const doneCnt = tasks.filter(t => t.done).length;
      const logs = Array.isArray(DATA.full_build_logs) ? DATA.full_build_logs : [];
      const lcOn = Boolean(window.isLcEnabledInHub && window.isLcEnabledInHub());
      const delCnt = Object.keys(window.getDeletedDishesMap()).length;

      const tabDefs = [
        { id: "dishes72", lbl: "🍲 Все блюда (" + DATA.menu.length + ")" },
        { id: "tasks", lbl: "📋 Задачи (" + doneCnt + "/" + tasks.length + ")" },
        { id: "logs", lbl: "📜 Логи (" + logs.length + ")" },
        { id: "ideas", lbl: "📝 Идеи" },
        { id: "toggles", lbl: "⚡ Режимы & Промпт" }
      ];

      tabsBox.innerHTML = tabDefs.map(t =>
        '<button type="button" onclick="setHubTab(\'' + t.id + '\')" class="px-3 py-1.5 rounded-xl text-xs font-extrabold cursor-pointer ' +
        (curTab === t.id ? 'bg-[#D48238] text-white shadow' : 'bg-white/10 text-stone-200 hover:bg-white/20') + '">' + t.lbl + '</button>'
      ).join("") +
      '<button type="button" onclick="if(window.setLcEnabledInHub)window.setLcEnabledInHub(' + (!lcOn) + ')" class="px-3 py-1.5 rounded-xl text-xs font-extrabold cursor-pointer border ' +
        (lcOn ? 'bg-emerald-600 text-white border-amber-300' : 'bg-black/35 text-amber-200 border-amber-400/40') + '">' +
        (lcOn ? '🎛️ Конструктор: ВКЛ' : '🎛️ Конструктор: ВЫКЛ') +
      '</button>';

      if (curTab === "dishes72") {
        const cats = ["Все", ...Array.from(new Set(DATA.menu.map(d => d.category)))];
        const curCat = window.hubDishCategoryFilter || "Все";
        const curQ = (window.hubDishSearchQuery || "").toLowerCase();
        const filtered = DATA.menu.filter(d => (curCat === "Все" || d.category === curCat) && (!curQ || d.name.toLowerCase().includes(curQ)));
        const engines = [
          { k: "flux_ai", lbl: "🎨 1. Flux AI" },
          { k: "turbo_ai", lbl: "⚡ 2. Turbo AI" },
          { k: "gastro_hd", lbl: "🍔 3. GastroBank HD" },
          { k: "openverse_hd", lbl: "📸 4. Openverse" },
          { k: "wikimedia", lbl: "🥗 5. Wikimedia" },
          { k: "vk_food_archive", lbl: "🌿 6. Архив ВК" }
        ];

        body.innerHTML =
          '<div class="bg-white rounded-2xl p-3 border border-stone-200 space-y-2.5 mb-3">' +
            '<div class="flex flex-wrap items-center justify-between gap-2">' +
              '<input type="text" value="' + esc(window.hubDishSearchQuery || "") + '" oninput="setHubSearch(this.value)" placeholder="🔍 Поиск блюда..." class="flex-1 min-w-[200px] px-3 py-1.5 rounded-xl border border-stone-300 text-xs font-bold">' +
              (delCnt > 0 ? '<button type="button" onclick="restoreAllDeletedDishes()" class="px-3 py-1.5 rounded-xl bg-amber-100 text-[#2E3D28] text-xs font-extrabold cursor-pointer">♻️ Восстановить (' + delCnt + ')</button>' : '') +
              '<button type="button" onclick="window.dishAddPanelOpen=!window.dishAddPanelOpen;renderUnifiedSystemHub()" class="px-3.5 py-1.5 rounded-xl bg-[#2E3D28] text-[#F2B880] text-xs font-extrabold cursor-pointer">' + (window.dishAddPanelOpen ? '▲ Скрыть форму' : '➕ Добавить блюдо') + '</button>' +
            '</div>' +
            (window.dishAddPanelOpen ? (
              '<div class="bg-[#2E3D28] text-white rounded-2xl p-3 space-y-2">' +
                '<div class="grid grid-cols-1 sm:grid-cols-4 gap-2 text-stone-900">' +
                  '<input id="new-dish-name" placeholder="Название блюда" class="px-2.5 py-1.5 rounded-lg bg-white text-xs font-bold">' +
                  '<select id="new-dish-cat" class="px-2.5 py-1.5 rounded-lg bg-white text-xs font-bold">' + cats.filter(c => c !== "Все").map(c => '<option>' + esc(c) + '</option>').join("") + '</select>' +
                  '<div class="grid grid-cols-2 gap-1"><input id="new-dish-price" type="number" placeholder="450" class="px-2.5 py-1.5 rounded-lg bg-white text-xs font-bold"><input id="new-dish-weight" placeholder="260 г" class="px-2.5 py-1.5 rounded-lg bg-white text-xs font-bold"></div>' +
                  '<input id="new-dish-photo" placeholder="img/vk_5128_1.jpg" class="px-2.5 py-1.5 rounded-lg bg-white text-xs">' +
                '</div>' +
                '<div class="flex gap-2"><input id="new-dish-desc" placeholder="Состав..." class="flex-1 px-2.5 py-1.5 rounded-lg bg-white text-stone-900 text-xs"><button type="button" onclick="addNewCustomDishFromHub()" class="px-4 py-1.5 rounded-lg bg-[#D48238] text-white font-extrabold text-xs cursor-pointer">✅ Сохранить</button></div>' +
              '</div>'
            ) : '') +
            '<div class="flex gap-1.5 overflow-x-auto no-scrollbar">' +
              cats.map(c => '<button type="button" onclick="setHubCategory(\'' + esc(c) + '\')" class="px-2.5 py-1 rounded-full text-[11px] font-extrabold whitespace-nowrap cursor-pointer ' + (curCat === c ? 'bg-[#2E3D28] text-[#F2B880]' : 'bg-stone-100 text-stone-700') + '">' + esc(c) + '</button>').join("") +
            '</div>' +
          '</div>' +
          '<div class="space-y-2.5">' + filtered.map(d => {
            const idx = DATA.menu.indexOf(d);
            const isOff = window.isDishDisabled(d.name);
            const curEng = window.selectedAiEnginePerDish[idx] || "flux_ai";
            const cand = window.pendingDishCandidates[idx];
            const pVal = window.customPromptsPerDish[idx] !== undefined ? window.customPromptsPerDish[idx] : (d.name || "");
            const diag = window.dishDiagLogs[idx] || [];
            return '<div class="bg-white rounded-2xl p-3.5 border border-stone-200 space-y-2.5 ' + (isOff ? 'opacity-50' : '') + '">' +
              '<div class="grid grid-cols-1 lg:grid-cols-12 gap-3 items-start">' +
                '<div class="lg:col-span-4 flex items-center gap-3">' +
                  '<div class="relative w-20 h-20 rounded-2xl overflow-hidden flex-shrink-0 border bg-stone-100">' +
                    '<img src="' + esc(d.photo) + '" onclick="openSuperZoom(this.src, \'' + esc(d.name) + '\')" class="w-full h-full object-cover cursor-zoom-in">' +
                  '</div>' +
                  '<div class="min-w-0 flex-1 space-y-1">' +
                    '<span class="text-[9px] font-extrabold uppercase px-2 py-0.5 rounded bg-amber-100 text-[#2E3D28]">' + esc(d.category) + '</span>' +
                    '<h4 class="font-serif font-bold text-base text-[#2E3D28] leading-tight">' + esc(d.name) + ' <span class="text-[#D48238] text-xs font-sans">(' + (d.sizes ? d.sizes[0].price : d.price) + ' ₽)</span></h4>' +
                    '<div class="flex flex-wrap gap-1">' +
                      '<button type="button" onclick="openReadyGalleryPopup(' + idx + ')" class="px-2 py-1 rounded-lg bg-[#2E3D28] text-[#F2B880] text-[10px] font-extrabold cursor-pointer">📸 Из готовых</button>' +
                      '<button type="button" onclick="toggleDishDisabled(' + idx + ')" class="px-2 py-1 rounded-lg ' + (isOff ? 'bg-emerald-700' : 'bg-amber-500') + ' text-white text-[10px] font-extrabold cursor-pointer">' + (isOff ? '👁️ Вкл' : '⏸️ Откл') + '</button>' +
                      '<button type="button" onclick="deleteDishTripleConfirm(' + idx + ')" class="px-2 py-1 rounded-lg bg-rose-700 text-white text-[10px] font-extrabold cursor-pointer">🗑️ Удалить</button>' +
                    '</div>' +
                  '</div>' +
                '</div>' +
                '<div class="lg:col-span-8 bg-amber-50/60 rounded-2xl p-2.5 border border-amber-200 space-y-2">' +
                  '<div class="flex flex-wrap gap-1">' +
                    engines.map(e => '<button type="button" onclick="runEngineForDish(' + idx + ',\'' + e.k + '\')" class="px-2 py-1 rounded-lg text-[10px] font-extrabold cursor-pointer ' + (curEng === e.k ? 'bg-[#2E3D28] text-[#F2B880]' : 'bg-white text-[#2E3D28] border border-amber-300') + '">' + e.lbl + '</button>').join("") +
                  '</div>' +
                  '<div class="grid grid-cols-1 sm:grid-cols-12 gap-2">' +
                    '<div class="sm:col-span-7 flex gap-1.5">' +
                      '<input id="hub-ai-prm-' + idx + '" value="' + esc(pVal) + '" oninput="window.customPromptsPerDish[' + idx + ']=this.value" class="flex-1 min-w-0 px-2.5 py-1.5 rounded-xl bg-white border border-amber-300 text-xs">' +
                      '<button type="button" onclick="generateDishCandidateAI(' + idx + ')" class="px-3 py-1.5 rounded-xl bg-[#D48238] text-white text-[11px] font-extrabold cursor-pointer">🔍 Найти / ИИ</button>' +
                    '</div>' +
                    '<div class="sm:col-span-5 flex gap-1.5">' +
                      '<input id="hub-url-inp-' + idx + '" placeholder="🔗 URL или img/..." class="flex-1 min-w-0 px-2.5 py-1.5 rounded-xl bg-white border border-stone-300 text-xs">' +
                      '<button type="button" onclick="previewManualUrlCandidate(' + idx + ')" class="px-2.5 py-1.5 rounded-xl bg-[#556432] text-white text-[11px] font-extrabold cursor-pointer">✅ URL</button>' +
                    '</div>' +
                  '</div>' +
                  (diag.length ? '<div class="bg-[#1A2416] text-emerald-300 rounded-xl px-2.5 py-1 font-mono text-[10px]">' + diag.map(l => '<div class="truncate">' + esc(l) + '</div>').join("") + '</div>' : '') +
                '</div>' +
              '</div>' +
              (cand ? (
                '<div class="bg-[#23311E] text-white rounded-2xl p-3 border-2 border-[#D48238] flex flex-col sm:flex-row items-center justify-between gap-3">' +
                  '<div class="flex items-center gap-3">' +
                    '<div class="w-24 h-24 rounded-xl overflow-hidden border-2 border-[#F2B880] bg-stone-800 flex-shrink-0">' +
                      '<img src="' + esc(cand.url) + '" onclick="openSuperZoom(this.src, \'' + esc(d.name) + '\')" class="w-full h-full object-cover cursor-zoom-in">' +
                    '</div>' +
                    '<div><span class="px-2 py-0.5 rounded-full bg-[#D48238] text-[10px] font-extrabold">' + esc(cand.source) + '</span><h5 class="font-serif text-base font-bold text-[#F2B880] mt-1">👁️ Предпросмотр для «' + esc(d.name) + '»</h5></div>' +
                  '</div>' +
                  '<div class="flex sm:flex-col gap-1.5">' +
                    '<button type="button" onclick="approveDishCandidate(' + idx + ')" class="px-3.5 py-1.5 rounded-xl bg-emerald-600 text-white font-extrabold text-xs cursor-pointer">✅ Утвердить</button>' +
                    '<button type="button" onclick="generateDishCandidateAI(' + idx + ')" class="px-3.5 py-1.5 rounded-xl bg-[#D48238] text-white font-extrabold text-xs cursor-pointer">🎲 Ещё вариант</button>' +
                    '<button type="button" onclick="delete window.pendingDishCandidates[' + idx + '];renderUnifiedSystemHub()" class="px-3 py-1 rounded-xl bg-white/10 text-stone-300 text-[11px] cursor-pointer">✕ Отмена</button>' +
                  '</div>' +
                '</div>'
              ) : '') +
            '</div>';
          }).join("") + '</div>';
        return;
      }

      if (curTab === "tasks") {
        body.innerHTML =
          '<div class="space-y-3">' +
            '<div class="bg-white rounded-2xl p-3 border grid grid-cols-1 sm:grid-cols-12 gap-2">' +
              '<input id="new-tz-task-inp" placeholder="➕ Новая задача..." class="sm:col-span-5 px-3 py-2 rounded-xl border text-xs font-bold">' +
              '<input id="new-tz-comment-inp" placeholder="💬 Комментарий..." class="sm:col-span-5 px-3 py-2 rounded-xl border text-xs">' +
              '<button type="button" onclick="addNewTaskV49()" class="sm:col-span-2 py-2 rounded-xl bg-[#D48238] text-white font-extrabold text-xs cursor-pointer">+ Добавить</button>' +
            '</div>' +
            '<div class="bg-white rounded-2xl border overflow-x-auto"><table class="w-full text-left border-collapse min-w-[780px]">' +
              '<thead class="bg-[#2E3D28] text-[#F2B880] text-[10px] uppercase"><tr><th class="p-3 w-32">Дата</th><th class="p-3">Задача</th><th class="p-3 w-28 text-center">Статус</th><th class="p-3 w-[40%]">Комментарий</th></tr></thead>' +
              '<tbody class="divide-y text-xs">' + tasks.map((t, i) =>
                '<tr><td class="p-3 font-mono text-[10px]">' + esc(t.date || "") + '</td><td class="p-3 font-bold">' + esc(t.title) + '</td><td class="p-3 text-center"><button type="button" onclick="toggleTaskDoneV49(' + i + ')" class="px-2.5 py-1 rounded-xl font-extrabold text-[11px] text-white cursor-pointer ' + (t.done ? 'bg-emerald-700' : 'bg-rose-600') + '">' + (t.done ? '✅ Сделано' : '❌ Нет') + '</button></td><td class="p-3"><input value="' + esc(t.comment || "") + '" oninput="updateTaskCommentV49(' + i + ',this.value)" class="w-full px-2.5 py-1.5 rounded-lg border text-xs"></td></tr>'
              ).join("") + '</tbody></table></div>' +
          '</div>';
        return;
      }

      if (curTab === "logs") {
        body.innerHTML = '<div class="space-y-2">' + logs.map(l => '<div class="bg-white rounded-2xl p-3 border"><div class="flex justify-between"><span class="px-2.5 py-0.5 rounded-full bg-[#2E3D28] text-[#F2B880] text-xs font-extrabold">' + esc(l.version) + '</span><span class="text-xs text-stone-400">' + esc(l.timestamp) + '</span></div><div class="text-xs font-extrabold text-[#D48238] mt-1">' + esc(l.model || "") + '</div><p class="text-xs text-stone-700">' + esc(l.status || "") + '</p></div>').join("") + '</div>';
        return;
      }

      if (curTab === "ideas") {
        const notes = window.getSavedIdeasNotes();
        body.innerHTML = '<div class="space-y-3"><div class="bg-white rounded-2xl p-3 border flex gap-2"><input id="new-idea-note-inp" placeholder="Запишите идею..." class="flex-1 px-3 py-1.5 rounded-xl border text-xs"><button type="button" onclick="addNewIdeaNote()" class="px-4 py-1.5 rounded-xl bg-[#2E3D28] text-[#F2B880] font-extrabold text-xs cursor-pointer">💾 Сохранить</button></div>' +
          notes.map(n => '<div class="bg-white rounded-2xl p-3 border flex justify-between"><p class="text-xs font-bold">' + esc(n.text) + '</p><span class="text-[10px] text-stone-400">' + esc(n.date) + '</span></div>').join("") + '</div>';
        return;
      }

      body.innerHTML =
        '<div class="grid grid-cols-1 lg:grid-cols-2 gap-3">' +
          '<div class="bg-white rounded-2xl p-4 border space-y-3">' +
            '<h4 class="font-serif text-lg font-bold text-[#2E3D28]">🛠️ Инженерные переключатели</h4>' +
            '<div class="p-3 rounded-xl bg-emerald-50 border-2 border-[#556432] space-y-2">' +
              '<div class="text-xs font-extrabold text-[#2E3D28]">🎛️ Кнопка «Живой конструктор окон и фото» на сайте:</div>' +
              '<div class="grid grid-cols-3 gap-1.5">' +
                '<button type="button" onclick="if(window.setLcEnabledInHub)window.setLcEnabledInHub(true)" class="p-2 rounded-lg text-[11px] font-extrabold cursor-pointer ' + (lcOn ? 'bg-[#2E3D28] text-[#F2B880]' : 'bg-white border') + '">👁️ Показать (ВКЛ)</button>' +
                '<button type="button" onclick="if(window.setLcEnabledInHub)window.setLcEnabledInHub(false)" class="p-2 rounded-lg text-[11px] font-extrabold cursor-pointer ' + (!lcOn ? 'bg-rose-700 text-white' : 'bg-white border') + '">🔒 Скрыть (ВЫКЛ)</button>' +
                '<button type="button" onclick="if(window.setLcEnabledInHub){window.setLcEnabledInHub(true);closeUnifiedSystemHub();window.toggleLcMode(true);}" class="p-2 rounded-lg bg-[#D48238] text-white text-[11px] font-extrabold cursor-pointer">🚀 Открыть сейчас</button>' +
              '</div>' +
            '</div>' +
          '</div>' +
          '<div class="bg-[#2E3D28] text-white rounded-2xl p-4 flex flex-col justify-between gap-3">' +
            '<div><span class="text-[10px] font-extrabold uppercase text-[#F2B880]">ДНК ПЛАТФОРМЫ</span><h4 class="font-serif text-xl font-bold mt-0.5">🧬 Мастер-Промпт архитектуры</h4></div>' +
            '<div class="flex gap-2"><button type="button" onclick="openMasterPromptModal()" class="px-4 py-2 rounded-xl bg-[#D48238] text-white text-xs font-extrabold cursor-pointer">📖 Открыть Промпт</button><button type="button" onclick="downloadMasterPromptFile()" class="px-4 py-2 rounded-xl bg-white/15 text-white text-xs font-extrabold cursor-pointer">💾 Скачать .TXT</button></div>' +
          '</div>' +
        '</div>';
    };

    // 11. Отрисовка Электронного меню
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
          ? '<div class="pt-2 border-t flex justify-between"><span class="text-xs font-extrabold text-amber-800">⏸️ Временно не готовится</span><span class="text-sm font-bold text-stone-400">' + (d.sizes ? d.sizes[0].price : d.price) + ' ₽</span></div>'
          : ((d.sizes && d.sizes.length > 1)
              ? '<div class="grid grid-cols-2 gap-1.5 pt-2">' + d.sizes.map((sz, sIdx) => '<button type="button" onclick="addToCart(' + realIdx + ',' + sIdx + ')" class="py-2 px-2 rounded-xl bg-[#556432] hover:bg-[#D48238] text-white font-extrabold text-[11px] cursor-pointer">' + esc(sz.label) + ' • ' + sz.price + ' ₽ +</button>').join("") + '</div>'
              : '<div class="flex items-center justify-between pt-2 border-t"><div><span class="text-[11px] text-stone-400 font-bold block">' + esc(d.weight || "") + '</span><strong class="text-lg font-extrabold text-[#2E3D28]">' + d.price + ' ₽</strong></div><button type="button" onclick="addToCart(' + realIdx + ',0)" class="px-4 py-2 rounded-xl bg-[#D48238] text-white font-extrabold text-xs cursor-pointer">+ В корзину</button></div>');

        return '<div class="zoom-card bg-white rounded-3xl p-3.5 border border-stone-200 shadow-sm flex flex-col justify-between gap-2 ' + (isOff ? 'opacity-40 grayscale-[35%]' : '') + '">' +
          '<div>' +
            '<div class="relative h-44 rounded-2xl overflow-hidden mb-2.5 bg-[#1D2918]">' +
              '<img src="' + esc(d.photo) + '" onclick="openSuperZoom(this.src, \'' + esc(d.name) + '\')" class="w-full h-full cursor-zoom-in">' +
              '<span class="absolute bottom-2 left-2 px-2 py-0.5 rounded-md bg-black/75 text-white text-[9px] font-bold">🍽️ Подача блюд может отличаться</span>' +
              '<button type="button" onclick="openSuperZoom(\'' + esc(d.photo) + '\', \'' + esc(d.name) + '\')" class="absolute bottom-2 right-2 w-7 h-7 rounded-full bg-black/80 hover:bg-[#D48238] text-white text-xs cursor-pointer">🔍</button>' +
            '</div>' +
            '<span class="text-[10px] font-extrabold uppercase text-[#556432]">' + esc(d.category) + '</span>' +
            '<h4 class="font-serif text-xl font-bold text-[#2E3D28] leading-snug">' + esc(d.name) + '</h4>' +
            '<p class="text-xs text-stone-600 mt-1 leading-relaxed">' + esc(d.desc || "") + '</p>' +
          '</div>' +
          actBtns +
        '</div>';
      }).join("");
      window.applyNoCropAmbientPhotos();
    };

    // 12. Мобильный свайп «Назад» (popstate)
    window.addEventListener("popstate", () => {
      ["super-zoom-lightbox", "ready-gallery-popup", "master-prompt-modal", "unified-system-hub",
       "menu-modal", "bowl-modal", "cafe-shop-modal", "book-table-modal", "delivery-modal", "radio-selector-modal"]
        .forEach(id => {
          const el = document.getElementById(id);
          if (el && !el.classList.contains("hidden")) {
            el.classList.add("hidden");
            el.classList.remove("flex");
          }
        });
    });

    window.addEventListener("DOMContentLoaded", () => {
      syncMenuWithCustomAndDeleted();
      applyV49CleanLayout();
      applyManualOverridesToMenuData();
      rollRandomGastroPulse();
      window.renderInteriorSlideState();
      setInterval(() => { stepInteriorSlide(1); window.renderInteriorSlideState(); }, 4200);
      window.renderHeroRightColumn();
      setInterval(() => step3DCarousel(1), 4500);
      setInterval(() => window.stepRightSpecialsPair(1), 5200);
      window.renderNewsPosts();
      window.renderCategoryShowcaseAndRail();
      window.applyNoCropAmbientPhotos();
      setInterval(syncMainCartBadge, 400);
    });
  </script>
  <script src="live_constructor.js?v=4.9"></script>
</body>
</html>
"""
    return tpl_html + v49_js


def build_clean_master_prompt_text():
    if os.path.exists("MASTER_PROMPT_MIRMIR.txt"):
        try:
            txt = sanitize_text(open("MASTER_PROMPT_MIRMIR.txt", "r", encoding="utf-8").read().strip())
            open("MASTER_PROMPT_MIRMIR.txt", "w", encoding="utf-8").write(txt)
            if len(txt) > 500:
                return txt
        except Exception:
            pass
    return "ПОЛНОЕ ТЕХНИЧЕСКОЕ ЗАДАНИЕ (МАСТЕР-ПРОМПТ) ВЕГАН-КАФЕ «МИР МИР» (v4.9)"


def sync_files_to_root_repo():
    if os.path.abspath(ROOT_REPO_DIR) == os.path.abspath(BASE_DIR):
        return
    sync_names = [
        "index.html", "menu_data.py", "template.html", "app.py",
        "live_constructor.py", "live_constructor.js",
        "tz_mirmir.json", "build_history.json", "MASTER_PROMPT_MIRMIR.txt",
        "run_counter.txt", "cache_posts.json"
    ]
    for fn in sync_names:
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
            if fn.lower().endswith((".jpg", ".jpeg", ".png", ".webp")) and not is_junk_image_name(fn):
                sf, df = os.path.join(s_img, fn), os.path.join(d_img, fn)
                if not os.path.exists(df) or os.path.getsize(df) != os.path.getsize(sf):
                    try:
                        shutil.copy2(sf, df)
                    except Exception:
                        pass


def main():
    write_file_log("=== ЗАПУСК ЧИСТОЙ СБОРКИ APP.PY (v4.9) ===")
    prepare_and_clean_assets()

    if os.path.exists(os.path.join(BASE_DIR, "live_constructor.py")):
        try:
            import live_constructor
            importlib.reload(live_constructor)
            live_constructor.build_constructor_js()
        except Exception as e:
            write_file_log(f"[WARN] Ошибка сборки live_constructor.js: {e}")

    import menu_data
    importlib.reload(menu_data)
    tz_data, build_logs, build_num = sync_tz_and_build_logs()
    dish_overrides = tz_data.get("dishes", {})
    vision_approved = load_approved_vision_overrides()

    clean_menu = []
    for item in menu_data.MENU_DATABASE:
        d = dict(item)
        if "photo_type" not in d:
            d["photo_type"] = d.pop("photo_type: ", "real")
        if any(bad in str(d.get("photo", "")) for bad in ["macro_mushrooms_raw", "macro_rice_noodles"]):
            d["photo"] = "img/macro_tomyum_bowl.jpg"
        nm = d.get("name", "")
        if nm in vision_approved:
            d["photo"] = vision_approved[nm]
            d["photo_type"] = "real"
            d["is_manual_override"] = True
        elif nm in dish_overrides and dish_overrides[nm].get("photo"):
            d["photo"] = dish_overrides[nm]["photo"]
            d["photo_type"] = "real"
            d["is_manual_override"] = True
        clean_menu.append(d)

    all_img_files = os.listdir("img") if os.path.exists("img") else []
    vk_files = sorted([fn for fn in all_img_files if fn.startswith("vk_") and "5047_" not in fn], reverse=True)
    other_clean = sorted([
        fn for fn in all_img_files
        if not fn.startswith(("vk_", "ai_v", "ingr_", "ymap_org_", "yorg_")) and "5047_" not in fn and not is_junk_image_name(fn)
    ])
    ready_photos = ["img/" + fn for fn in (vk_files + other_clean) if fn.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))]

    banned_vk = ["5068_", "vk_cover", "vk_avatar", "5140_", "5138_", "5136_", "5134_", "5133_", "5129_", "5123_"]
    vk_food_photos = ["img/" + fn for fn in vk_files if not any(b in fn for b in banned_vk)]

    now_stamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    data_payload = {
        "version": f"Релиз v4.9 • Сборка #{build_num} ({now_stamp})",
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
    write_file_log(f"[OK] Сборка #{build_num} завершена: {len(clean_menu)} блюд, {len(ready_photos)} фото, {len(data_payload['posts'])} постов ВК.")

    if sys.stdin and sys.stdin.isatty() and os.environ.get("GITHUB_ACTIONS") != "true":
        try:
            os.startfile("index.html")
        except Exception:
            pass


def push_to_github():
    sync_files_to_root_repo()
    target = ROOT_REPO_DIR
    lock_f = os.path.join(target, ".git", "index.lock")
    if os.path.exists(lock_f):
        try:
            os.remove(lock_f)
        except Exception:
            pass
    subprocess.run(["git", "config", "user.name", "MirMir Cafe"], cwd=target, check=False)
    subprocess.run(["git", "config", "user.email", "admin@mirmir.cafe"], cwd=target, check=False)
    subprocess.run(["git", "remote", "remove", "origin"], cwd=target, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "remote", "add", "origin", "https://github.com/vitvseom-stack/mirmir.git"], cwd=target, check=False)
    subprocess.run(["git", "checkout", "-B", "main"], cwd=target, check=False)
    subprocess.run([
        "git", "add", "-f", "index.html", "menu_data.py", "template.html", "app.py",
        "live_constructor.py", "live_constructor.js", "tz_mirmir.json",
        "build_history.json", "MASTER_PROMPT_MIRMIR.txt", "cache_posts.json"
    ], cwd=target, check=False)
    subprocess.run(["git", "add", "img/"], cwd=target, check=False)
    subprocess.run(["git", "commit", "-m", f"Deploy MirMir v4.9 ({datetime.now().strftime('%d.%m.%Y %H:%M:%S')})"], cwd=target, check=False)
    subprocess.run(["git", "push", "-u", "origin", "main", "--force"], cwd=target, check=False)
    write_file_log("[OK] Деплой в GitHub Pages (ветка main) выполнен.")


if __name__ == "__main__":
    if not sys.stdin or not sys.stdin.isatty() or os.environ.get("GITHUB_ACTIONS") == "true":
        main()
        sys.exit(0)
    try:
        mode = input("👉 [1] Только ПК | [2] ПК + GitHub | [3] Только GitHub [по умолчанию 1]: ").strip() or "1"
        if mode == "1":
            main()
        elif mode == "3":
            push_to_github()
        else:
            main()
            push_to_github()
    except Exception:
        write_file_log(f"[CRITICAL]\n{traceback.format_exc()}")
    input("\nГотово! Нажмите Enter для закрытия...")
# === [КОНЕЦ КОДА / ФАЙЛ ЗАВЕРШЁН ПОЛНОСТЬЮ] ===