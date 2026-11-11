# -*- coding: utf-8 -*-
"""
МОНОЛИТНЫЙ КОМПИЛЯТОР «МИР МИР» (app.py — Версия v4.0)
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
    {"id": "t_1", "date": "08.11.2026", "title": "1. Чистая 3-модульная архитектура (menu_data.py + template.html + app.py) и меню 1/2/3", "done": True, "comment": "Сборка и авто-пуш в корень GitHub Pages активны."},
    {"id": "t_2", "date": "09.11.2026", "title": "2. Первый экран слева: только проверенные фото интерьера и кованой вывески", "done": True, "comment": "Чужие фото с Яндекс.Карт удалены."},
    {"id": "t_3", "date": "09.11.2026", "title": "3. Первый экран справа: вращающаяся Голубка за 3D-меню + 2 крупных спешла под ним", "done": True, "comment": "Работает в 2 колонки."},
    {"id": "t_4", "date": "09.11.2026", "title": "4. Плашка «🍽️ Подача блюд может отличаться» на миниатюрах И при увеличении Лупой", "done": True, "comment": "В v4.0 добавлена также внутрь полноэкранной Лупы."},
    {"id": "t_5", "date": "10.11.2026", "title": "5. Защита мобильного свайпа «Назад» (popstate SPA-Guard) на смартфонах", "done": True, "comment": "Закрывает текущее окно без вылета с сайта."},
    {"id": "t_6", "date": "10.11.2026", "title": "6. Узкие синие кнопки «ВК» в Новостях + фильтр закреплённого поста о меню", "done": True, "comment": "Закреп обновляет только 3D-меню и скрыт из новостей."},
    {"id": "t_7", "date": "10.11.2026", "title": "7. Широкий экран (1640px) + классические крестики (✕) строго в правом верхнем углу", "done": True, "comment": "Активно для всех модальных окон."},
    {"id": "t_8", "date": "10.11.2026", "title": "8. Спокойная палитра нижних кнопок (Бронь, Такси в кафе, Доставка, Радио + 3 кнопки Скоро)", "done": True, "comment": "Без дублей и без пустого поля внизу."},
    {"id": "t_9", "date": "11.11.2026", "title": "9. Полный русский Текстовый Мастер-Промпт (ДНК сайта) с сохранением правок", "done": True, "comment": "Хранится в MASTER_PROMPT_MIRMIR.txt."},
    {"id": "t_10", "date": "11.11.2026", "title": "10. Переключатели по аудиту Claude: Бронь (ТГ/ВК без 152-ФЗ или анкета), Карта без рекламы, Фото-режим", "done": True, "comment": "Находятся во вкладке №5 Шестерёнки."},
    {"id": "t_11", "date": "11.11.2026", "title": "11. Починить переключение всех вкладок и кнопок генерации/галереи в Шестерёнке (v4.0)", "done": True, "comment": "Устранён конфликт областей видимости let/window."},
    {"id": "t_12", "date": "11.11.2026", "title": "12. Отключение блюд (полупрозрачный вид в меню с кнопкой включения) и удаление с 3 подтверждениями", "done": True, "comment": "Кнопки «👁️ Отключить/Включить» и «🗑️ Удалить (3 подтв.)» в каждой карточке."},
    {"id": "t_13", "date": "11.11.2026", "title": "13. Плашки «Открыто» и «Бизнес-Ланч -30%» оставить только в самом верху без повторений в Hero", "done": True, "comment": "Дубли в зелёном блоке убраны, плашки стоят только в верхней шапке."}
]


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
            merged.append({"id": tid, "date": old.get("date") or d_t["date"], "title": d_t["title"], "done": bool(old.get("done", d_t["done"])), "comment": old.get("comment") or d_t["comment"]})
        else:
            merged.append(dict(d_t))
    for k, v in by_id.items():
        if len(str(v.get("title", ""))) > 3:
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
        "version": f"Релиз v4.0 • Сборка #{cnt}",
        "timestamp": now_str,
        "model": "Монолит v4.0: Рабочие вкладки + Отключение (прозрачность) и Удаление блюд (3 подтв.) + Лупа с подачей + Верхние бейджи",
        "status": "Все кнопки пульта работают напрямую, добавлено отключение и удаление блюд, плашка подачи в Лупе и перенос Бизнес-ланча в верхнюю шапку.",
        "stats": f"Дата сборки: {now_str}"
    })
    json.dump(logs[:60], open("build_history.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return tz_data, logs[:60], cnt


def upgrade_template_html_in_place(tpl_html):
    if 'name="robots"' not in tpl_html:
        tpl_html = tpl_html.replace("<head>", '<head>\n  <meta name="robots" content="noindex, nofollow">', 1)

    # Убираем ключевое слово let у глобальных переменных шаблона, чтобы они жили напрямую в window и кнопки не блокировались!
    for vname in ["hubActiveTab", "hubDishCategoryFilter", "hubDishSearchQuery", "selectedAiEnginePerDish", "pendingDishCandidates", "currentMenuCategory", "currentNewsPage"]:
        tpl_html = re.sub(rf"\blet\s+{vname}\b", f"var {vname}", tpl_html)

    anchor_pos = tpl_html.find('a.download = "MASTER_PROMPT_MIRMIR.txt";')
    if anchor_pos != -1:
        brace_pos = tpl_html.find("}", anchor_pos)
        if brace_pos != -1:
            tpl_html = tpl_html[: brace_pos + 1] + "\n"

    v40_js = r"""
    // === 🚀 ЯДРО v4.0: РАБОЧИЕ КНОПКИ + ОТКЛЮЧЕНИЕ (ПРОЗРАЧНОСТЬ) + УДАЛЕНИЕ (3 ПОДТВ.) + ЛУПА С ПОДАЧЕЙ + БЕЙДЖИ ТОЛЬКО ВВЕРХУ ===
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

    // 1. Хранилища отключённых (полупрозрачных) и удалённых блюд
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
      if (!confirm("⚠️ ПОДТВЕРЖДЕНИЕ 1 из 3:\nВы действительно хотите удалить блюдо «" + d.name + "» из меню?")) return;
      if (!confirm("⚠️ ПОДТВЕРЖДЕНИЕ 2 из 3:\nТочно удаляем «" + d.name + "»? Оно исчезнет из витрины сайта.")) return;
      if (!confirm("🚨 ПОДТВЕРЖДЕНИЕ 3 из 3 (ФИНАЛЬНОЕ):\nОкончательно удалить блюдо «" + d.name + "» из меню?")) return;
      const delMap = window.getDeletedDishesMap();
      delMap[d.name] = true;
      try { localStorage.setItem("mirmir_deleted_dishes_v1", JSON.stringify(delMap)); } catch(e) {}
      DATA.menu.splice(idx, 1);
      window.renderUnifiedSystemHub();
      window.renderDishes();
      window.renderHeroRightColumn();
      alert("🗑️ Блюдо «" + d.name + "» удалено из меню.");
    };
    window.restoreAllDeletedDishes = function() {
      if (!confirm("Восстановить все ранее удалённые блюда обратно в меню?")) return;
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

    // 2. Полноэкранная Лупа с обязательным предупреждением «🍽️ Подача блюд может отличаться»
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

    // 3. Верхняя шапка: оставляем «Открыто» и «Бизнес-Ланч -30%» ТОЛЬКО наверху, убирая их повтор в зелёном Hero-блоке!
    function enforceTopHeaderBadgesOnly() {
      const topBadge = document.getElementById("header-work-badge");
      if (topBadge && topBadge.parentElement && !document.getElementById("header-lunch-badge")) {
        const lb = document.createElement("span");
        lb.id = "header-lunch-badge";
        lb.className = "px-2.5 py-0.5 rounded-full bg-[#D48238] text-white text-[10px] font-extrabold whitespace-nowrap shadow-xs";
        lb.innerHTML = "🔥 Бизнес-Ланч −30% (будни 12:00–16:00)";
        topBadge.parentElement.appendChild(lb);
      }
      // Скрываем дублирующуюся строку «ОТКРЫТО ДО 21:00 / Бизнес-Ланч -30%» внутри зелёного Hero-блока
      const heroLeft = document.querySelector("main section .lg\\:col-span-7");
      if (heroLeft) {
        heroLeft.querySelectorAll("span, div").forEach(el => {
          const txt = (el.textContent || "").trim();
          if ((txt.includes("ОТКРЫТО ДО 21:00") || txt.includes("ЗАКРЫТО ДО 12:00")) && el.parentElement && el.parentElement.textContent.includes("Бизнес-Ланч")) {
            el.parentElement.style.display = "none";
          }
        });
      }
    }

    // 4. Стили и удаление дублей кнопок
    function applyV40StylesAndLayout() {
      if (!document.getElementById("mirmir-v40-styles")) {
        const st = document.createElement("style");
        st.id = "mirmir-v40-styles";
        st.textContent = `
          html, body { min-height: auto !important; height: auto !important; }
          main.max-w-\\[1440px\\], header .max-w-\\[1440px\\], footer .max-w-\\[1440px\\] { max-width: 1640px !important; width: 100% !important; min-height: 0 !important; }
          main.max-w-\\[1440px\\] { padding-bottom: 12px !important; }
          header .max-w-\\[1440px\\] { padding-top: 6px !important; padding-bottom: 6px !important; }
          header button[onclick*="openBookTableModal"], header button[onclick*="openBowlBuilder"], header button[onclick*="openRadioSelectorModal"], header button[onclick*="openDeliveryModal"], header a[href*="yandex"],
          #category-rail button[onclick*="openBowlBuilder"],
          main section .lg\\:col-span-7 div[onclick*="Сезонные спешлы от Шефа"],
          main section .lg\\:col-span-7 .grid.grid-cols-2 { display: none !important; }
          .v40-top-right-close { position: absolute !important; top: 10px !important; right: 10px !important; z-index: 95 !important; width: 34px !important; height: 34px !important; border-radius: 9999px !important; background: rgba(20,28,17,0.92) !important; color: #FFFDF9 !important; border: 1.5px solid rgba(242,184,128,0.7) !important; display: inline-flex !important; align-items: center !important; justify-content: center !important; font-size: 16px !important; font-weight: 900 !important; cursor: pointer !important; }
          .v40-top-right-close:hover { background: #D48238 !important; color: #fff !important; }
        `;
        document.head.appendChild(st);
      }
      enforceTopHeaderBadgesOnly();

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
          if (b.textContent.trim() === "✕" && !b.classList.contains("v40-top-right-close")) b.style.display = "none";
        });
        if (!card.querySelector(".v40-top-right-close")) {
          const btn = document.createElement("button");
          btn.className = "v40-top-right-close";
          btn.setAttribute("onclick", cfg.closeFn);
          btn.innerHTML = "✕";
          card.appendChild(btn);
        }
      });

      const mainEl = document.querySelector("main");
      if (mainEl && !document.getElementById("v40-bottom-nav-hub")) {
        const taxiUrl = "https://3.redirect.appmetrica.yandex.com/route?end-lat=56.322355&end-lon=43.990383&appmetrica_tracking_id=1178268795219780156";
        const navHub = document.createElement("section");
        navHub.id = "v40-bottom-nav-hub";
        navHub.className = "max-w-3xl mx-auto pt-2 pb-1";
        navHub.innerHTML =
          '<div class="bg-[#23311E] text-[#FFFDF9] rounded-2xl p-2.5 border border-[#F2B880]/40 shadow-md space-y-2">' +
            '<div class="grid grid-cols-2 sm:grid-cols-4 gap-2">' +
              '<button onclick="openBookTableModal()" class="py-2 px-3 rounded-xl bg-[#556432] hover:bg-[#D48238] text-[#FFFDF9] font-extrabold text-xs flex items-center justify-center gap-1.5 cursor-pointer transition"><span>🪑</span><span>Бронь</span></button>' +
              '<a href="' + taxiUrl + '" target="_blank" class="py-2 px-3 rounded-xl bg-[#3A4A2E] hover:bg-[#D48238] text-[#F2B880] hover:text-white font-extrabold text-xs flex items-center justify-center gap-1.5 cursor-pointer transition"><span>🚕</span><span>Такси в кафе</span></a>' +
              '<button onclick="openDeliveryModal()" class="py-2 px-3 rounded-xl bg-[#556432] hover:bg-[#D48238] text-[#FFFDF9] font-extrabold text-xs flex items-center justify-center gap-1.5 cursor-pointer transition"><span>🛵</span><span>Доставка</span></button>' +
              '<button onclick="openRadioSelectorModal()" class="py-2 px-3 rounded-xl bg-[#FFFDF9] hover:bg-amber-50 text-[#2E3D28] font-extrabold text-xs flex items-center justify-center gap-1.5 cursor-pointer transition"><span>📻</span><span>Радио</span></button>' +
            '</div>' +
            '<div class="pt-1.5 border-t border-white/15 grid grid-cols-3 gap-1.5">' +
              '<button disabled class="py-1 px-2 rounded-lg bg-white/10 text-white/65 font-extrabold text-[10px] uppercase flex items-center justify-center gap-1 cursor-not-allowed"><span>👥 НАША КОМАНДА</span><span class="px-1 rounded bg-black/40 text-[#F2B880] text-[8px]">Скоро</span></button>' +
              '<button disabled class="py-1 px-2 rounded-lg bg-white/10 text-white/65 font-extrabold text-[10px] uppercase flex items-center justify-center gap-1 cursor-not-allowed"><span>🏛️ ИСТОРИЯ КАФЕ</span><span class="px-1 rounded bg-black/40 text-[#F2B880] text-[8px]">Скоро</span></button>' +
              '<button disabled class="py-1 px-2 rounded-lg bg-white/10 text-white/65 font-extrabold text-[10px] uppercase flex items-center justify-center gap-1 cursor-not-allowed"><span>🌿 НАШИ ЦЕННОСТИ</span><span class="px-1 rounded bg-black/40 text-[#F2B880] text-[8px]">Скоро</span></button>' +
            '</div>' +
          '</div>';
        mainEl.appendChild(navHub);
      }
      const footerEl = document.querySelector("footer");
      if (footerEl) footerEl.querySelectorAll(".grid.grid-cols-1.sm\\:grid-cols-3").forEach(g => { g.style.display = "none"; });
    }

    // 5. Прямые глобальные переключатели вкладок, задач, настроек и генератора в Шестерёнке
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
      try { return Object.assign({}, def, JSON.parse(localStorage.getItem("mirmir_site_toggles_v40") || "{}")); } catch(e) { return def; }
    };
    window.setAdminSettingV40 = function(k, v) {
      const tg = window.getSiteToggles();
      tg[k] = v;
      try { localStorage.setItem("mirmir_site_toggles_v40", JSON.stringify(tg)); } catch(e) {}
      window.renderDishes();
      window.renderUnifiedSystemHub();
    };

    function getMasterTasksList() {
      const srv = (DATA.tz_synced && Array.isArray(DATA.tz_synced.tasks)) ? DATA.tz_synced.tasks : [];
      try {
        const loc = JSON.parse(localStorage.getItem("mirmir_tasks_v40") || "null");
        if (Array.isArray(loc) && loc.length >= srv.length) return loc;
      } catch(e) {}
      return srv;
    }
    function saveMasterTasksList(arr) {
      try {
        localStorage.setItem("mirmir_tasks_v40", JSON.stringify(arr));
        fetch(NTFY_SYNC_URL, { method: "POST", body: JSON.stringify({ type: "tz_tasks_sync", tasks: arr, ts: Date.now() }) }).catch(() => {});
      } catch(e) {}
    }
    window.toggleTaskDoneV40 = function(idx) {
      const list = getMasterTasksList();
      if (!list[idx]) return;
      list[idx].done = !list[idx].done;
      saveMasterTasksList(list);
      window.renderUnifiedSystemHub();
    };
    window.updateTaskCommentV40 = function(idx, val) {
      const list = getMasterTasksList();
      if (!list[idx]) return;
      list[idx].comment = val;
      saveMasterTasksList(list);
    };
    window.addNewTaskV40 = function() {
      const t = (document.getElementById("new-tz-task-inp")?.value || "").trim();
      if (!t) return;
      const c = (document.getElementById("new-tz-comment-inp")?.value || "Проверить").trim();
      const list = getMasterTasksList();
      list.unshift({ id: "t_u_" + Date.now(), date: new Date().toLocaleDateString("ru-RU"), title: t, done: false, comment: c });
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
      alert("✅ Блюдо «" + name + "» добавлено в меню!");
    };

    // 6. Генератор фото и галерея «Из готовых»
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
      const cObj = { url: pickLocal, source: "🍔 Вариант #" + step + " (" + pickLocal + ")", prompt: raw, diag: "✅ Проверенный веган-кадр без лимитов" };
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

    window.selectReadyPhotoV40 = function(dishIdx, photoPath) {
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
      if (cand && cand.url) window.selectReadyPhotoV40(idx, cand.url);
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
            '<button onclick="closeReadyGalleryPopup()" class="v40-top-right-close">✕</button>' +
          '</div>' +
          '<div class="p-4 overflow-y-auto max-h-[75vh] bg-[#FAF5EC] grid grid-cols-2 sm:grid-cols-4 gap-3">' +
            pool.map(ph =>
              '<div class="bg-white rounded-2xl p-2 border border-stone-200 flex flex-col justify-between gap-1.5">' +
                '<div class="relative h-32 rounded-xl overflow-hidden bg-stone-100">' +
                  '<img src="' + esc(ph) + '" loading="lazy" onclick="openSuperZoom(this.src, \'' + esc(d.name) + '\')" class="w-full h-full object-cover cursor-zoom-in">' +
                '</div>' +
                '<div class="text-[10px] font-mono text-stone-500 truncate">' + esc(ph) + '</div>' +
                '<button onclick="selectReadyPhotoV40(' + dishIdx + ', \'' + esc(ph) + '\')" class="w-full py-1.5 rounded-xl bg-emerald-700 hover:bg-[#D48238] text-white text-xs font-extrabold cursor-pointer">✅ Утвердить это фото</button>' +
              '</div>'
            ).join("") +
          '</div>';
      }
      modal.classList.remove("hidden");
      modal.classList.add("flex");
    };

    // 7. Рендер Шестерёнки Архитектора (все 5 вкладок + Отключение/Включение + Удаление с 3 подтверждениями)
    window.renderUnifiedSystemHub = function() {
      syncMenuWithCustomAndDeleted();
      applyManualOverridesToMenuData();
      applyV40StylesAndLayout();

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
                    '<button type="button" onclick="openSuperZoom(\'' + esc(d.photo) + '\', \'' + esc(d.name) + '\')" class="absolute bottom-1 right-1 px-1.5 py-0.5 rounded bg-black/80 text-white text-[9px] font-bold cursor-pointer">🔍 Лупа</button>' +
                  '</div>' +
                  '<div class="min-w-0 flex-1 space-y-1">' +
                    '<div class="flex flex-wrap items-center gap-1">' +
                      '<span class="text-[9px] font-extrabold uppercase px-2 py-0.5 rounded bg-amber-100 text-[#2E3D28]">' + esc(d.category) + '</span>' +
                      (isOff ? '<span class="text-[9px] font-extrabold px-2 py-0.5 rounded bg-amber-600 text-white">⏸️ Отключено (прозрачное)</span>' : '') +
                    '</div>' +
                    '<h4 class="font-serif font-bold text-base text-[#2E3D28] leading-tight">' + esc(d.name) + ' <span class="text-[#D48238] text-xs font-sans">(' + (d.sizes ? d.sizes[0].price : d.price) + ' ₽)</span></h4>' +
                    '<div class="flex flex-wrap gap-1 pt-0.5">' +
                      '<button type="button" onclick="openReadyGalleryPopup(' + idx + ')" class="px-2 py-1 rounded-lg bg-[#2E3D28] text-[#F2B880] text-[10px] font-extrabold cursor-pointer">📸 Из готовых (' + (DATA.ready_photos ? DATA.ready_photos.length : 306) + ')</button>' +
                      '<button type="button" onclick="toggleDishDisabled(' + idx + ')" class="px-2 py-1 rounded-lg ' + (isOff ? 'bg-emerald-700 text-white' : 'bg-amber-500/90 text-white') + ' text-[10px] font-extrabold cursor-pointer">' + (isOff ? '👁️ Включить' : '⏸️ Отключить') + '</button>' +
                      '<button type="button" onclick="deleteDishTripleConfirm(' + idx + ')" class="px-2 py-1 rounded-lg bg-rose-700 hover:bg-rose-800 text-white text-[10px] font-extrabold cursor-pointer" title="Удалить с 3 подтверждениями">🗑️ Удалить</button>' +
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
            '<div class="bg-white rounded-2xl p-3 border border-stone-200 grid grid-cols-1 sm:grid-cols-12 gap-2">' +
              '<input id="new-tz-task-inp" type="text" placeholder="➕ Новая задача..." class="sm:col-span-5 px-3 py-1.5 rounded-xl border border-stone-300 text-xs font-bold">' +
              '<input id="new-tz-comment-inp" type="text" placeholder="💬 Комментарий..." class="sm:col-span-5 px-3 py-1.5 rounded-xl border border-stone-300 text-xs">' +
              '<button type="button" onclick="addNewTaskV40()" class="sm:col-span-2 px-3 py-1.5 rounded-xl bg-[#D48238] text-white font-extrabold text-xs cursor-pointer">+ Добавить</button>' +
            '</div>' +
            '<div class="bg-white rounded-2xl border border-stone-300 overflow-x-auto">' +
              '<table class="w-full text-left border-collapse min-w-[700px]"><thead class="bg-[#2E3D28] text-[#F2B880] text-[10px] font-extrabold uppercase"><tr><th class="p-2.5 w-24">Дата</th><th class="p-2.5">Задача</th><th class="p-2.5 text-center w-36">Статус</th><th class="p-2.5">Комментарий / Что не так</th></tr></thead><tbody class="divide-y divide-stone-200 text-xs">' +
                tasks.map((t, i) => '<tr class="' + (t.done ? '' : 'bg-rose-50/40') + '"><td class="p-2.5 font-mono text-[11px] text-stone-500">📅 ' + esc(t.date || "11.11.2026") + '</td><td class="p-2.5 font-bold text-[#1F2B1A]">' + esc(t.title) + '</td><td class="p-2.5 text-center"><button type="button" onclick="toggleTaskDoneV40(' + i + ')" class="px-3 py-1.5 rounded-xl font-extrabold text-[11px] cursor-pointer w-32 ' + (t.done ? 'bg-emerald-700 text-white' : 'bg-rose-600 text-white') + '">' + (t.done ? '✅ Сделано' : '❌ Не сделано') + '</button></td><td class="p-2.5"><input type="text" value="' + esc(t.comment || "") + '" oninput="updateTaskCommentV40(' + i + ', this.value)" class="w-full px-2.5 py-1.5 rounded-lg border border-stone-200 text-xs"></td></tr>').join("") +
              '</tbody></table>' +
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
            '<h4 class="font-serif text-lg font-bold text-[#2E3D28]">🛠️ Настройки режимов сайта (Аудит Claude)</h4>' +
            '<div class="p-3 rounded-xl bg-amber-50/70 border border-amber-200 space-y-1.5"><div class="text-xs font-extrabold text-[#2E3D28]">🪑 1. Режим кнопки «Бронь столика»:</div><div class="grid grid-cols-2 gap-1.5"><button type="button" onclick="setAdminSettingV40(\'bookingMode\', \'messenger\')" class="p-2 rounded-lg text-[11px] font-extrabold cursor-pointer ' + (tg.bookingMode === 'messenger' ? 'bg-[#2E3D28] text-[#F2B880]' : 'bg-white border') + '">✈️ Telegram / ВК (Без 152-ФЗ)</button><button type="button" onclick="setAdminSettingV40(\'bookingMode\', \'form152\')" class="p-2 rounded-lg text-[11px] font-extrabold cursor-pointer ' + (tg.bookingMode === 'form152' ? 'bg-[#2E3D28] text-[#F2B880]' : 'bg-white border') + '">📝 Анкета на сайте (152-ФЗ)</button></div></div>' +
            '<div class="p-3 rounded-xl bg-amber-50/70 border border-amber-200 space-y-1.5"><div class="text-xs font-extrabold text-[#2E3D28]">📸 2. Режим показа фото в Меню:</div><div class="grid grid-cols-2 gap-1.5"><button type="button" onclick="setAdminSettingV40(\'photoMode\', \'hybrid\')" class="p-2 rounded-lg text-[11px] font-extrabold cursor-pointer ' + (tg.photoMode === 'hybrid' ? 'bg-[#2E3D28] text-[#F2B880]' : 'bg-white border') + '">🎨 Гибрид (Все фото)</button><button type="button" onclick="setAdminSettingV40(\'photoMode\', \'strict_real\')" class="p-2 rounded-lg text-[11px] font-extrabold cursor-pointer ' + (tg.photoMode === 'strict_real' ? 'bg-[#2E3D28] text-[#F2B880]' : 'bg-white border') + '">🕊️ Только 100% фото из ВК</button></div></div>' +
          '</div>' +
          '<div class="bg-[#2E3D28] text-[#FFFDF9] rounded-2xl p-4 space-y-2.5 flex flex-col justify-between">' +
            '<div><span class="text-[10px] font-extrabold uppercase text-[#F2B880]">ДНК ПЛАТФОРМЫ</span><h4 class="font-serif text-xl font-bold mt-0.5">🧬 Полный Текстовый Мастер-Промпт</h4><p class="text-xs text-stone-300 mt-1">Живое ТЗ на русском языке с сохранением правок.</p></div>' +
            '<div class="flex gap-2"><button type="button" onclick="openMasterPromptModal()" class="px-4 py-2 rounded-xl bg-[#D48238] text-white text-xs font-extrabold cursor-pointer">📖 Открыть и редактировать Промпт</button><button type="button" onclick="downloadMasterPromptFile()" class="px-4 py-2 rounded-xl bg-white/15 text-white text-xs font-extrabold cursor-pointer">💾 Скачать .TXT</button></div>' +
          '</div>' +
        '</div>';
    };

    // 8. Отрисовка Электронного меню с поддержкой полупрозрачных (отключённых) блюд и плашки подачи
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
              '<button type="button" onclick="openSuperZoom(\'' + esc(d.photo) + '\', \'' + esc(d.name) + '\')" class="absolute bottom-2 right-2 px-2 py-0.5 rounded-lg bg-black/80 text-white text-[10px] font-extrabold cursor-pointer">🔍 Лупа</button>' +
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
      applyV40StylesAndLayout();
      document.querySelectorAll("[data-dove-holder]").forEach(el => { el.innerHTML = SIGN_DOVE_SVG; });
      applyManualOverridesToMenuData();
      renderWorkStatusBadges();
      enforceTopHeaderBadgesOnly();
      rollRandomGastroPulse();
      renderInteriorSlideState();
      renderHeroRightColumn();
      renderNewsPosts();
      renderCategoryShowcaseAndRail();
    });
  </script>
</body>
</html>
"""
    return tpl_html + v40_js


def build_clean_master_prompt_text():
    if os.path.exists("MASTER_PROMPT_MIRMIR.txt"):
        try:
            txt = open("MASTER_PROMPT_MIRMIR.txt", "r", encoding="utf-8").read().strip()
            if len(txt) > 500:
                return txt
        except Exception:
            pass
    return "ПОЛНЫЙ МАСТЕР-ПРОМПТ ВЕГАН-КАФЕ «МИР МИР» (v4.0)"


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
        "version": f"Релиз v4.0 • Сборка #{build_num} ({now_stamp})",
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
    subprocess.run(["git", "commit", "-m", f"Deploy MirMir v4.0 ({datetime.now().strftime('%d.%m.%Y %H:%M:%S')})"], cwd=target_git_dir, check=False)
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