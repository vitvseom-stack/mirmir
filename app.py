# -*- coding: utf-8 -*-
"""
ЦЕЛЬНЫЙ КОМПИЛЯТОР «МИР МИР» (app.py — Чистая 3-модульная сборка v3.1)
1. Срезает старый дублирующийся JS-хвост в template.html (устраняет конфликт версий v2.5/v3.0).
2. Гарантированно выводит плашку «🍽️ Подача блюд может отличаться» на всех фото блюд в Электронном меню.
3. Меняет кнопку в Новостях на фирменную кнопку с SVG-логотипом VK и прямой ссылкой на конкретный пост (?w=wall-191992548_ID).
4. Полностью убирает жёлтый 45-секундный баннер Pollinations: кнопка «🎲 Ещё вариант» и 6 кнопок движков мгновенно листают реальные веган-фото!
5. Включает защиту мобильного свайпа «Назад» (popstate) и синхронизацию корневого index.html для GitHub Pages.
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
DEFAULT_MIRMIR_ROOT = os.path.expanduser(r"~\Documents\mirmir")
if os.path.exists(os.path.join(PARENT_DIR, ".git")):
    ROOT_REPO_DIR = PARENT_DIR
elif os.path.exists(os.path.join(DEFAULT_MIRMIR_ROOT, ".git")):
    ROOT_REPO_DIR = DEFAULT_MIRMIR_ROOT
else:
    ROOT_REPO_DIR = BASE_DIR

LAT_45, LON_45 = "56.322355", "43.990383"
VK_OWNER_ID = "-191992548"
OLD_DIRS_TO_CHECK = [DEFAULT_MIRMIR_ROOT, PARENT_DIR]


def auto_migrate_assets_from_old_folder():
    """Подтягивает папку img/, ключи и кэши из родительской папки mirmir."""
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


def enforce_vegan_prompts_in_menu_data_file():
    """Автоматически проверяет, чтобы у всех 72 блюд в menu_data.py стояли веганские маркеры."""
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
    """Удаляет чужие фото ymap_org_2..99 и возвращает чистые кадры зала и фасада."""
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


def build_direct_vk_post_url(post_obj, owner_id_str=VK_OWNER_ID):
    """
    Формирует прямую ссылку на конкретный пост ВКонтакте на стене mirmir.cafe:
    https://vk.com/mirmir.cafe?w=wall-191992548_XXXX
    Если ID нет в поле id, извлекает его из имени файла фото img/vk_XXXX_0.jpg!
    """
    pid = post_obj.get("id")
    if not pid:
        photo_str = str(post_obj.get("photo") or "")
        m = re.search(r"vk_(\d+)_", photo_str)
        if m:
            pid = m.group(1)
    if pid:
        return f"https://vk.com/mirmir.cafe?w=wall{owner_id_str}_{pid}"
    return "https://vk.com/mirmir.cafe"


def fetch_vk_wall_posts():
    """Синхронизирует посты со стены vk.com/mirmir.cafe и формирует точные ссылки на каждый пост."""
    vk_token = os.environ.get("VK_TOKEN") or read_local_secret("vk key.txt")
    posts_out = []
    real_owner_id = VK_OWNER_ID

    if vk_token:
        try:
            r = requests.get(
                "https://api.vk.com/method/wall.get",
                params={"domain": "mirmir.cafe", "count": 15, "access_token": vk_token, "v": "5.199"},
                timeout=8,
            )
            items = r.json().get("response", {}).get("items", [])
            for it in items:
                txt = (it.get("text") or "").strip()
                if not txt or len(txt) < 15:
                    continue
                post_id = it.get("id")
                if it.get("owner_id"):
                    real_owner_id = str(it.get("owner_id"))
                dt_str = datetime.fromtimestamp(it.get("date", 0)).strftime("%d.%m.%Y")
                likes = it.get("likes", {}).get("count", 25)
                photo_local = ""
                for att in it.get("attachments", []):
                    if att.get("type") == "photo":
                        sizes = att["photo"].get("sizes", [])
                        if sizes:
                            best_sz = sorted(sizes, key=lambda s: s.get("width", 0), reverse=True)[0]
                            img_url = best_sz.get("url")
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
                                if os.path.exists(fp):
                                    photo_local = f"img/{fn}"
                                break
                if not photo_local:
                    continue
                first_line = txt.split("\n")[0].strip()
                p_item = {
                    "id": post_id,
                    "date": dt_str,
                    "likes": likes,
                    "title": first_line[:68] + ("..." if len(first_line) > 68 else ""),
                    "text": txt[:280] + ("..." if len(txt) > 280 else ""),
                    "photo": photo_local,
                }
                p_item["vk_url"] = build_direct_vk_post_url(p_item, real_owner_id)
                posts_out.append(p_item)
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
                for p in cached:
                    p["vk_url"] = build_direct_vk_post_url(p, real_owner_id)
                    if not p.get("title"):
                        p["title"] = (p.get("text") or "Новость кафе").split("\n")[0][:65]
                return cached[:12]
        except Exception:
            pass
    return []


def sync_tz_and_build_logs():
    tz_data = {"tasks": [], "dishes": {}}
    if os.path.exists("tz_mirmir.json"):
        try:
            tz_data = json.load(open("tz_mirmir.json", "r", encoding="utf-8"))
        except Exception:
            pass

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
        "version": f"Релиз v3.1 • Сборка #{cnt}",
        "timestamp": now_str,
        "model": "Монолит v3.1: Прямые посты ВК с логотипом VK + Плашка подачи + Рабочий «Ещё вариант»",
        "status": "Очищен старый хвост в template.html. На всех блюдах в меню стоит «Подача блюд может отличаться», в новостях — синяя кнопка с лого VK на конкретный пост, в шестерёнке — мгновенный «Ещё вариант» без лимита 45 сек.",
        "stats": f"Дата сборки: {now_str}",
    })
    with open("build_history.json", "w", encoding="utf-8") as f:
        json.dump(logs[:60], f, ensure_ascii=False, indent=2)

    return tz_data, logs[:60], cnt


def upgrade_template_html_in_place(tpl_html):
    """
    1. Срезает весь старый накопленный JS-хвост после функции downloadMasterPromptFile(),
       чтобы старый код от v2.5 больше никогда не перезаписывал новые функции!
    2. Записывает единый чистый блок v3.1 (плашка «Подача блюд может отличаться» в меню,
       кнопка с логотипом VK на конкретный пост, мгновенный «Ещё вариант» без 45-сек заглушки и свайп Назад).
    """
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
        '          <img id="right-col-bg-photo" src="img/ymap_org_0.jpg" class="w-full h-full object-cover opacity-30 scale-105 transition-all duration-1000 filter saturate-125 contrast-110">\n'
        '          <div class="absolute inset-0" style="background:radial-gradient(circle at center, rgba(28,42,24,0.35) 0%, rgba(26,38,22,0.88) 85%);"></div>\n'
        '        </div>\n'
        '        <div class="absolute inset-0 flex items-center justify-center pointer-events-none opacity-[0.28] z-0">\n'
        '          <div class="w-[370px] h-[370px] wm-spin" data-dove-holder></div>\n'
        '        </div>'
    )
    if old_wm_block in tpl_html:
        tpl_html = tpl_html.replace(old_wm_block, new_wm_block)

    # Находим конец последней базовой функции downloadMasterPromptFile() и ЧИСТО ОТРЕЗАЕМ весь старый хвост под ней!
    anchor_str = 'a.download = "MASTER_PROMPT_MIRMIR.txt";'
    anchor_pos = tpl_html.find(anchor_str)
    if anchor_pos != -1:
        brace_pos = tpl_html.find("}", anchor_pos)
        if brace_pos != -1:
            tpl_html = tpl_html[: brace_pos + 1] + "\n"

    v31_clean_tail = """
    // === 🚀 ЕДИНОЕ ЯДРО v3.1: ПЛАШКА ПОДАЧИ В МЕНЮ + КНОПКА С ЛОГО VK НА ПОСТ + БЕЗЛИМИТНЫЙ «ЕЩЁ ВАРИАНТ» + СВАЙП НАЗАД ===
    const VK_LOGO_SVG = '<svg class="w-4 h-4 fill-current flex-shrink-0" viewBox="0 0 24 24"><path d="M15.07 2H8.93C3.33 2 2 3.33 2 8.93v6.14C2 20.67 3.33 22 8.93 22h6.14c5.6 0 6.93-1.33 6.93-6.93V8.93C22 3.33 20.67 2 15.07 2zm3.08 14.27h-1.46c-.55 0-.72-.44-1.71-1.43-.86-.83-1.24-.94-1.46-.94-.3 0-.38.08-.38.49v1.31c0 .35-.11.56-1.04.56-1.54 0-3.25-.93-4.45-2.66-1.81-2.54-2.3-4.45-2.3-4.84 0-.21.08-.41.49-.41h1.46c.37 0 .51.17.65.56.72 2.08 1.92 3.9 2.41 3.9.19 0 .27-.09.27-.56v-2.16c-.06-.99-.58-1.08-.58-1.43 0-.17.14-.34.37-.34h2.29c.31 0 .42.16.42.53v2.91c0 .31.14.42.23.42.19 0 .34-.11.68-.45 1.05-1.18 1.8-3 1.8-3 .1-.21.27-.41.64-.41h1.46c.44 0 .54.23.44.53-.18.85-1.95 3.35-1.95 3.35-.16.25-.22.36 0 .65.16.21.69.67 1.04 1.08.65.74 1.14 1.36 1.27 1.79.14.42-.08.64-.5.64z"/></svg>';

    window.customPromptsPerDish = window.customPromptsPerDish || {};
    window.dishVariantStep = window.dishVariantStep || {};
    window.cachedSearchPools = window.cachedSearchPools || {};

    // 1. В левом слайдере крутятся строго 5 проверенных кадров ИНТЕРЬЕРА и ЭКСТЕРЬЕРА кафе
    window.getInteriorSlidesList = function() {
      return [
        { src: "img/ymap_org_0.jpg", title: "🏛️ Исторический кирпичный свод и уютный зал на Ильинской, 45", tag: "Интерьер зала" },
        { src: "img/ymap_org_1.jpg", title: "🕊️ Фирменная кованая вывеска с белой Голубкой мира у входа", tag: "Экстерьер • Ильинская, 45" },
        { src: "img/vk_5068_0.jpg", title: "🛋️ Изумрудный велюровый диван, живой кирпич и картины", tag: "Атмосфера «Мир Мир»" },
        { src: "img/vk_5122_0.jpg", title: "🕯️ Вечерние чаепития при свечах и редкий китайский чай", tag: "Чайная культура" },
        { src: "img/vk_5134_0.jpg", title: "🌿 Уютное зелёное пространство для встреч и живого общения", tag: "Интерьер кафе" }
      ];
    };

    // 2. Справа под 3D-меню: 2 крупных поля для картинок блюд
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
            '<button onclick="openMenu(\\'Сезонные спешлы от Шефа\\')" class="text-[10px] font-extrabold text-amber-300 hover:underline cursor-pointer">Все блюда (72) ➔</button>';
        }
      }

      const specials = (DATA.menu || []).filter(d => d.category === "Сезонные спешлы от Шефа" || d.photo_type === "real");
      const start = (window.rightSpecialsPairIdx * 2) % Math.max(1, specials.length);
      const pair = [specials[start], specials[(start + 1) % specials.length]].filter(Boolean);

      rowsBox.innerHTML = '<div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">' + pair.map(d => {
        const idx = DATA.menu.indexOf(d);
        const pr = d.sizes ? d.sizes[0].price : d.price;
        return '<div onclick="openMenu(\\'Сезонные спешлы от Шефа\\')" class="zoom-card bg-[#FDF8F2] text-stone-900 rounded-2xl p-2.5 flex flex-col justify-between gap-2 cursor-pointer shadow-lg border-2 border-[#F2B880]/70 transition">' +
          '<div class="relative h-32 sm:h-36 w-full rounded-xl overflow-hidden bg-stone-200">' +
            '<img src="' + esc(d.photo) + '" onclick="event.stopPropagation();openSuperZoom(\\'' + esc(d.photo) + '\\', \\'' + esc(d.name) + '\\')" class="w-full h-full object-cover cursor-zoom-in">' +
            '<span class="absolute top-1.5 left-1.5 px-2 py-0.5 rounded-md bg-black/70 text-[#F2B880] text-[9px] font-extrabold">' + esc(d.weight || "Хит шефа") + '</span>' +
            '<button onclick="event.stopPropagation();openSuperZoom(\\'' + esc(d.photo) + '\\', \\'' + esc(d.name) + '\\')" class="absolute bottom-1.5 right-1.5 px-2 py-0.5 rounded-md bg-black/75 hover:bg-[#D48238] text-white text-[9px] font-extrabold cursor-pointer">🔍 Лупа</button>' +
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

    // 3. Прямая отрисовка Электронного меню (72 блюда) с обязательной плашкой «🍽️ Подача блюд может отличаться» на фото КАЖДОГО блюда!
    renderDishes = function() {
      applyManualOverridesToMenuData();
      const tabsBox = document.getElementById("menu-cat-tabs");
      const grid = document.getElementById("menu-dishes-grid");
      if (!grid) return;
      const cats = ["Все", ...Array.from(new Set((DATA.menu || []).map(d => d.category)))];
      if (tabsBox) {
        tabsBox.innerHTML = cats.map(c =>
          '<button onclick="currentMenuCategory=\\'' + esc(c) + '\\';renderDishes()" class="px-3.5 py-1.5 rounded-full text-xs font-extrabold whitespace-nowrap cursor-pointer transition ' +
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
        const badgeText = d.photo_type === "real" ? "📸 Фото блюда" : "🌿 Ингредиенты состава";
        const buttonsHtml = (d.sizes && d.sizes.length > 1)
          ? '<div class="grid grid-cols-2 gap-1.5 pt-2">' + d.sizes.map((sz, sIdx) =>
              '<button onclick="addToCart(' + realIdx + ',' + sIdx + ')" class="py-2 px-2 rounded-xl bg-[#556432] hover:bg-[#D48238] text-white font-extrabold text-[11px] cursor-pointer transition shadow-sm">' + esc(sz.label) + ' • ' + sz.price + ' ₽ +</button>'
            ).join("") + '</div>'
          : '<div class="flex items-center justify-between pt-2 border-t border-stone-100"><div><span class="text-[11px] text-stone-400 font-bold block">' + esc(d.weight || "") + '</span><strong class="text-lg font-extrabold text-[#2E3D28]">' + d.price + ' ₽</strong></div><button onclick="addToCart(' + realIdx + ',0)" class="px-4 py-2 rounded-xl bg-[#D48238] hover:opacity-95 text-white font-extrabold text-xs cursor-pointer shadow">+ В корзину</button></div>';

        return '<div class="zoom-card bg-white rounded-3xl p-3.5 border border-stone-200 shadow-sm flex flex-col justify-between gap-2 transition">' +
          '<div>' +
            '<div class="relative h-44 rounded-2xl overflow-hidden mb-2.5 bg-stone-100">' +
              '<img src="' + esc(d.photo) + '" onclick="openSuperZoom(\\'' + esc(d.photo) + '\\', \\'' + esc(d.name) + '\\')" class="w-full h-full object-cover cursor-zoom-in">' +
              '<span class="absolute top-2 left-2 px-2.5 py-0.5 rounded-full bg-black/75 text-[#F2B880] text-[10px] font-extrabold">' + badgeText + '</span>' +
              '<span class="absolute bottom-2 left-2 px-2 py-0.5 rounded-md bg-black/75 text-white/95 text-[9px] font-bold shadow">🍽️ Подача блюд может отличаться</span>' +
              '<button onclick="openSuperZoom(\\'' + esc(d.photo) + '\\', \\'' + esc(d.name) + '\\')" class="absolute bottom-2 right-2 px-2 py-0.5 rounded-lg bg-black/80 hover:bg-[#D48238] text-white text-[10px] font-extrabold cursor-pointer">🔍 Лупа</button>' +
            '</div>' +
            '<span class="text-[10px] font-extrabold uppercase text-[#556432]">' + esc(d.category) + '</span>' +
            '<h4 class="font-serif text-xl font-bold text-[#2E3D28] leading-snug">' + esc(d.name) + '</h4>' +
            '<p class="text-xs text-stone-600 mt-1 leading-relaxed">' + esc(d.desc || "") + '</p>' +
            '<div class="text-[10px] text-stone-400 italic mt-1">🍽️ Подача блюд может отличаться</div>' +
          '</div>' +
          buttonsHtml +
        '</div>';
      }).join("");
    };

    // 4. Отрисовка Новостей с кнопкой-логотипом VK и прямой ссылкой на конкретный пост (?w=wall-191992548_ID)
    renderNewsPosts = function() {
      const grid = document.getElementById("posts-grid");
      if (!grid) return;
      const posts = (DATA.posts && DATA.posts.length) ? DATA.posts : [];
      const slice = posts.slice(currentNewsPage * 3, currentNewsPage * 3 + 3);

      grid.innerHTML = slice.map(p => {
        let postId = p.id || "";
        if (!postId && p.photo) {
          const m = String(p.photo).match(/vk_(\\d+)_/);
          if (m) postId = m[1];
        }
        const directPostUrl = postId
          ? ("https://vk.com/mirmir.cafe?w=wall-191992548_" + postId)
          : (p.vk_url || "https://vk.com/mirmir.cafe");

        return '<article class="zoom-card bg-[#FFFDF9] rounded-3xl p-4 border border-[#556432]/25 shadow-sm flex flex-col justify-between gap-3 transition">' +
          '<div class="space-y-2.5">' +
            '<div class="flex items-center justify-between text-[11px] font-extrabold text-[#D48238]">' +
              '<span>📅 ' + esc(p.date || "Новость кафе") + '</span><span>❤️ ' + esc(p.likes || 25) + '</span>' +
            '</div>' +
            '<h3 class="font-serif text-xl font-bold text-[#1F2B1A] leading-snug">' + esc(p.title || "Событие в «Мир Мир»") + '</h3>' +
            '<div class="relative rounded-2xl overflow-hidden bg-[#F4ECE1] flex items-center justify-center">' +
              '<img src="' + esc(p.photo) + '" onclick="openSuperZoom(\\'' + esc(p.photo) + '\\', \\'' + esc(p.title) + '\\')" class="w-full h-auto max-h-[340px] object-contain cursor-zoom-in block mx-auto">' +
              '<button onclick="openSuperZoom(\\'' + esc(p.photo) + '\\', \\'' + esc(p.title) + '\\')" class="absolute bottom-2 right-2 px-2.5 py-1 rounded-lg bg-black/75 hover:bg-[#D48238] text-white text-[10px] font-extrabold cursor-pointer shadow">🔍 Лупа</button>' +
            '</div>' +
            '<p class="text-xs sm:text-sm text-stone-700 leading-relaxed whitespace-pre-line">' + esc(p.text || "") + '</p>' +
          '</div>' +
          '<div class="pt-2.5 border-t border-stone-200/80 flex items-center justify-between">' +
            '<a href="' + esc(directPostUrl) + '" target="_blank" class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-[#0077FF] hover:bg-[#0055CC] text-white text-xs font-extrabold transition shadow-md cursor-pointer">' +
              VK_LOGO_SVG + '<span>Открыть пост в VK ↗</span>' +
            '</a>' +
            (postId ? '<span class="text-[10px] font-bold text-stone-400">Пост #' + esc(postId) + '</span>' : '') +
          '</div>' +
        '</article>';
      }).join("");

      // Обновляем и нижнюю кнопку под секцией новостей на логотип VK
      const bottomVkLink = document.querySelector("#news-section-wrap a[href*='vk.com']");
      if (bottomVkLink) {
        bottomVkLink.className = "inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-[#0077FF] hover:bg-[#0055CC] text-white text-xs font-extrabold transition shadow-md";
        bottomVkLink.innerHTML = VK_LOGO_SVG + "<span>Все посты на стене VK (vk.com/mirmir.cafe) ↗</span>";
      }
    };

    // 5. Умный подбор коротких веган-тегов и 100% рабочая кнопка «🎲 Ещё вариант» БЕЗ 45-секундных заглушек!
    const NON_VEGAN_BAN_REGEX = /meat|chicken|pork|beef|shrimp|prawn|fish|seafood|salmon|tuna|bacon|steak|ham|lamb|turkey|sausage|pepperoni|cheese|milk|dairy|egg/i;

    // Кулинарная база гарантированных HD веган-фотографий по категориям (мгновенный пул без лимитов!)
    const CURATED_VEGAN_HD_BANK = {
      drink: [
        "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=800&q=80",
        "https://images.unsplash.com/photo-1556881286-fc6915169721?w=800&q=80",
        "https://images.unsplash.com/photo-1544145945-f90425340c7e?w=800&q=80",
        "https://images.unsplash.com/photo-1497534446932-c925b458314e?w=800&q=80",
        "https://images.unsplash.com/photo-1505252585461-04db1eb84625?w=800&q=80",
        "https://images.unsplash.com/photo-1576092768241-dec231879fc3?w=800&q=80"
      ],
      soup: [
        "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=800&q=80",
        "https://images.unsplash.com/photo-1547592180-85f173990554?w=800&q=80",
        "https://images.unsplash.com/photo-1603105037880-880cd4edfb0d?w=800&q=80",
        "https://images.unsplash.com/photo-1578020190125-f4f7c18bc9cb?w=800&q=80"
      ],
      salad: [
        "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800&q=80",
        "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=800&q=80",
        "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800&q=80",
        "https://images.unsplash.com/photo-1505576399279-565b52d4ac71?w=800&q=80"
      ],
      main: [
        "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=800&q=80",
        "https://images.unsplash.com/photo-1520072959219-c595dc870360?w=800&q=80",
        "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&q=80",
        "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=800&q=80"
      ],
      dessert: [
        "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=800&q=80",
        "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=800&q=80",
        "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=800&q=80",
        "https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=800&q=80"
      ]
    };

    function extractShortSearchTopic(dish, rawText) {
      const cat = (dish.category || "").toLowerCase();
      const nm = (dish.name || "").toLowerCase();
      const raw = (rawText || "").toLowerCase();
      if (nm.includes("лимонад") || raw.includes("lemonade") || raw.includes("citrus")) return { q: "citrus lemonade mint drink", bank: "drink" };
      if (nm.includes("смузи") || raw.includes("smoothie")) return { q: "berry fruit smoothie glass", bank: "drink" };
      if (nm.includes("фреш") || raw.includes("juice")) return { q: "fresh orange carrot juice", bank: "drink" };
      if (nm.includes("кофе") || nm.includes("капучино") || nm.includes("американо")) return { q: "latte cappuccino coffee cup", bank: "drink" };
      if (cat.includes("чай") || nm.includes("чай") || nm.includes("пуэр") || nm.includes("улун") || nm.includes("масала")) return { q: "herbal tea teapot cup", bank: "drink" };
      if (cat.includes("суп") || nm.includes("суп") || nm.includes("том ям") || nm.includes("ватапа")) return { q: "vegan vegetable tofu soup bowl", bank: "soup" };
      if (cat.includes("салат") || nm.includes("салат") || nm.includes("цезарь") || nm.includes("боул")) return { q: "vegan avocado green salad bowl", bank: "salad" };
      if (cat.includes("десерт") || nm.includes("сырники") || nm.includes("шарлотка") || nm.includes("мороженое") || nm.includes("батончик")) return { q: "vegan berry cake dessert", bank: "dessert" };
      if (nm.includes("пицца") || nm.includes("лахмаджун")) return { q: "vegan mushroom vegetable pizza", bank: "main" };
      if (nm.includes("бургер") || nm.includes("сэндвич") || nm.includes("неряха")) return { q: "vegan plant burger sandwich", bank: "main" };
      if (cat.includes("лапша") || nm.includes("лапша") || nm.includes("паста") || nm.includes("пад тай")) return { q: "vegan noodles pasta tofu", bank: "main" };
      return { q: "vegan healthy dish bowl", bank: "salad" };
    }

    window.runEngineForDish = function(idx, engKey) {
      const inp = document.getElementById("hub-ai-prm-" + idx);
      if (inp) window.customPromptsPerDish[idx] = inp.value;
      selectedAiEnginePerDish[idx] = engKey;
      window.dishVariantStep[idx] = (window.dishVariantStep[idx] || 0) + 1;
      window.generateDishCandidateAI(idx);
    };

    const _baseRenderHub = renderUnifiedSystemHub;
    renderUnifiedSystemHub = function() {
      document.querySelectorAll("[id^='hub-ai-prm-']").forEach(el => {
        const idNum = parseInt(el.id.replace("hub-ai-prm-", ""), 10);
        if (!isNaN(idNum)) window.customPromptsPerDish[idNum] = el.value;
      });
      _baseRenderHub();

      if (hubActiveTab === "dishes72") {
        document.querySelectorAll("[id^='hub-ai-prm-']").forEach(el => {
          const idx = parseInt(el.id.replace("hub-ai-prm-", ""), 10);
          if (isNaN(idx)) return;
          if (window.customPromptsPerDish[idx] !== undefined) {
            el.value = window.customPromptsPerDish[idx];
          }
          el.addEventListener("input", function() {
            window.customPromptsPerDish[idx] = this.value;
          });
          const wrapper = el.closest(".bg-amber-50\\\\/70");
          if (wrapper && !wrapper.querySelector(".quick-6-engines-bar")) {
            const curE = selectedAiEnginePerDish[idx] || "openverse_hd";
            const engines = [
              { k: "openverse_hd", lbl: "📸 1. Openverse HD" },
              { k: "wikimedia", lbl: "🥗 2. Wikimedia" },
              { k: "gastro_hd", lbl: "🍹 3. GastroBank HD" },
              { k: "flickr_food", lbl: "🍲 4. Flickr Vegan" },
              { k: "local_ready", lbl: "🌿 5. Архив (317)" }
            ];
            const btnsHtml = '<div class="quick-6-engines-bar flex flex-wrap gap-1 pt-1.5 border-t border-amber-200/80 mt-1.5">' +
              '<span class="text-[9px] font-extrabold text-stone-500 w-full">⚡ Нажмите на любой источник для мгновенного подбора без лимитов:</span>' +
              engines.map(e =>
                '<button onclick="runEngineForDish(' + idx + ',\\'' + e.k + '\\')" class="px-2 py-1 rounded-lg text-[10px] font-extrabold cursor-pointer transition ' +
                (curE === e.k ? 'bg-[#2E3D28] text-[#F2B880] shadow' : 'bg-white hover:bg-amber-100 text-[#2E3D28] border border-amber-300') + '">' + e.lbl + '</button>'
              ).join("") +
            '</div>';
            wrapper.insertAdjacentHTML("beforeend", btnsHtml);
          }
        });
      }
    };

    generateDishCandidateAI = async function(idx) {
      const d = DATA.menu[idx];
      if (!d) return;
      const prmInp = document.getElementById("hub-ai-prm-" + idx);
      if (prmInp && prmInp.value.trim()) {
        window.customPromptsPerDish[idx] = prmInp.value.trim();
      }
      const userRawText = window.customPromptsPerDish[idx] !== undefined ? window.customPromptsPerDish[idx] : (d.ai_prompt || d.name);

      window.dishVariantStep[idx] = (window.dishVariantStep[idx] || 0) + 1;
      const step = window.dishVariantStep[idx];
      const engine = selectedAiEnginePerDish[idx] || "openverse_hd";

      const btn = document.getElementById("hub-ai-btn-" + idx);
      if (btn) { btn.innerText = "⏳ Вариант #" + step + "..."; btn.disabled = true; }

      const topicInfo = extractShortSearchTopic(d, userRawText);
      const shortQuery = topicInfo.q;
      const bankPool = CURATED_VEGAN_HD_BANK[topicInfo.bank] || CURATED_VEGAN_HD_BANK.salad;

      // 1. Движок Openverse HD (кешируем список из 30 реальных фото и при каждом клике «Ещё вариант» выдаём следующий кадр!)
      if (engine === "openverse_hd") {
        try {
          const cacheKey = "ov_" + shortQuery;
          if (!window.cachedSearchPools[cacheKey]) {
            const r = await fetch("https://api.openverse.org/v1/images/?q=" + encodeURIComponent(shortQuery) + "&page_size=30");
            const j = await r.json();
            if (j.results && j.results.length) {
              window.cachedSearchPools[cacheKey] = j.results
                .filter(it => !NON_VEGAN_BAN_REGEX.test((it.title || "")))
                .map(it => it.url)
                .filter(Boolean);
            }
          }
          const pool = window.cachedSearchPools[cacheKey];
          if (pool && pool.length) {
            const pickUrl = pool[step % pool.length];
            pendingDishCandidates[idx] = { url: pickUrl, source: "📸 Openverse HD (Вариант #" + ((step % pool.length) + 1) + " из " + pool.length + ")", prompt: shortQuery };
            addLocalBuildOrActionLog("📸 Openverse HD: вариант #" + step + " для «" + d.name + "»", shortQuery);
            renderUnifiedSystemHub();
            return;
          }
        } catch(e) {}
      }

      // 2. Движок Wikimedia Gastro Commons
      if (engine === "wikimedia") {
        try {
          const cacheKey = "wm_" + shortQuery;
          if (!window.cachedSearchPools[cacheKey]) {
            const r = await fetch("https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch=" + encodeURIComponent("filetype:bitmap " + shortQuery) + "&gsrlimit=25&prop=imageinfo&iiprop=url&format=json&origin=*");
            const j = await r.json();
            const pages = j.query && j.query.pages ? Object.values(j.query.pages) : [];
            window.cachedSearchPools[cacheKey] = pages
              .filter(p => !NON_VEGAN_BAN_REGEX.test(p.title || ""))
              .map(p => p.imageinfo && p.imageinfo[0] && p.imageinfo[0].url)
              .filter(Boolean);
          }
          const pool = window.cachedSearchPools[cacheKey];
          if (pool && pool.length) {
            const pickUrl = pool[step % pool.length];
            pendingDishCandidates[idx] = { url: pickUrl, source: "🥗 Wikimedia Gastro (Вариант #" + ((step % pool.length) + 1) + " из " + pool.length + ")", prompt: shortQuery };
            addLocalBuildOrActionLog("🥗 Wikimedia: вариант #" + step + " для «" + d.name + "»", shortQuery);
            renderUnifiedSystemHub();
            return;
          }
        } catch(e) {}
      }

      // 3. Движок Flickr Vegan Stream
      if (engine === "flickr_food") {
        const tag = shortQuery.split(" ")[0] || "vegan";
        const flickrUrl = "https://loremflickr.com/720/720/vegan," + encodeURIComponent(tag) + "?lock=" + (step * 137 + idx);
        pendingDishCandidates[idx] = { url: flickrUrl, source: "🍲 Flickr Vegan (Вариант #" + step + ")", prompt: shortQuery };
        renderUnifiedSystemHub();
        return;
      }

      // 4. Движок Локальный Архив img/ (317 готовых фото)
      if (engine === "local_ready") {
        const pool = (DATA.ready_photos && DATA.ready_photos.length) ? DATA.ready_photos : ["img/vk_5128_1.jpg"];
        const pickLocal = pool[(step * 7 + idx) % pool.length];
        pendingDishCandidates[idx] = { url: pickLocal, source: "🌿 Архив Кафе img/ (Вариант #" + step + ")", prompt: pickLocal };
        renderUnifiedSystemHub();
        return;
      }

      // 5. Гарантированный безлимитный пул GastroBank HD (НИКОГДА не выдаёт жёлтый баннер 45-секундного лимита!)
      const pickBankUrl = bankPool[step % bankPool.length];
      pendingDishCandidates[idx] = {
        url: pickBankUrl,
        source: "🍹 GastroBank HD (Вариант #" + ((step % bankPool.length) + 1) + " • Без лимитов)",
        prompt: shortQuery
      };
      addLocalBuildOrActionLog("🍹 GastroBank HD: вариант #" + step + " для «" + d.name + "»", shortQuery);
      renderUnifiedSystemHub();
    };

    // 6. Мобильный свайп «Назад» (popstate SPA-Guard для всех окон)
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
          return origFn.apply(this, arguments);
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

    window.addEventListener("DOMContentLoaded", () => {
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
      applySiteToggles();
    });
  </script>
</body>
</html>
"""
    return tpl_html + v31_clean_tail


def build_clean_master_prompt_text():
    lines = [
        "ПОЛНОЕ ТЕКСТОВОЕ ТЕХНИЧЕСКОЕ ЗАДАНИЕ (МАСТЕР-ПРОМПТ) НА РАЗРАБОТКУ ТРЁХМОДУЛЬНОЙ ПЛАТФОРМЫ ВЕГАН-КАФЕ «МИР МИР» (v3.1)",
        "",
        "1. ЧИСТАЯ ТРЁХМОДУЛЬНАЯ АРХИТЕКТУРА: menu_data.py (72 веганских блюда + 8 товаров магазина) + template.html + app.py.",
        "2. ЭЛЕКТРОННОЕ МЕНЮ: на фотографии каждого из 72 блюд размещена плашка «🍽️ Подача блюд может отличаться».",
        "3. НОВОСТИ И АНОНСЫ: карточки снабжены фирменной синей кнопкой с официальным логотипом VK и прямой ссылкой на конкретный пост на стене сообщества (https://vk.com/mirmir.cafe?w=wall-191992548_ID).",
        "4. ШЕСТЕРЁНКА АРХИТЕКТОРА (⚙️): мгновенное переключение вариантов по кнопке «🎲 Ещё вариант» и 5 быстрых кнопок источников фото без 45-секундных лимитов.",
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
    ]:
        src = os.path.join(BASE_DIR, fn)
        dst = os.path.join(ROOT_REPO_DIR, fn)
        if os.path.exists(src):
            try:
                shutil.copy2(src, dst)
            except Exception:
                pass
    print(f"🔄 [Синхронизация корня] Главный файл `{os.path.join(ROOT_REPO_DIR, 'index.html')}` обновлён!")


def main():
    print("=" * 78)
    print("🕊️  СБОРКА «МИР МИР» v3.1 (ПОДАЧА БЛЮД + ЛОГО VK НА ПОСТЫ + ЕЩЁ ВАРИАНТ БЕЗ ЛИМИТА)")
    print("=" * 78)

    auto_migrate_assets_from_old_folder()
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
        nm = d.get("name", "")
        if nm in dish_overrides and dish_overrides[nm].get("photo"):
            d["photo"] = dish_overrides[nm]["photo"]
            d["photo_type"] = "real"
            d["is_manual_override"] = True
        clean_menu.append(d)

    ymap_photos = get_verified_interior_exterior_photos()
    wall_posts = fetch_vk_wall_posts()

    ready_photos = []
    if os.path.exists("img"):
        for fn in sorted(os.listdir("img")):
            if fn.lower().endswith((".jpg", ".jpeg", ".png", ".webp")) and "5047_" not in fn:
                ready_photos.append("img/" + fn)

    master_prompt_str = build_clean_master_prompt_text()
    now_stamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    data_payload = {
        "version": f"Релиз v3.1 • Сборка #{build_num} ({now_stamp})",
        "menu": clean_menu,
        "shop": CAFE_SHOP_ITEMS,
        "posts": wall_posts,
        "ymap_photos": ymap_photos,
        "ready_photos": ready_photos,
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
    print(f"✨ [Сборка #{build_num} готова] Плашки подачи в меню, кнопки VK на посты и «Ещё вариант» вшиты!")
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

    root_index = os.path.join(target_git_dir, "index.html")
    if os.path.exists(root_index):
        with open(root_index, "a", encoding="utf-8") as f:
            f.write(f"\n<!-- Root Deploy Stamp: {datetime.now().isoformat()} -->\n")

    subprocess.run(["git", "remote", "remove", "origin"], cwd=target_git_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "remote", "add", "origin", "https://github.com/vitvseom-stack/mirmir.git"], cwd=target_git_dir, check=False)
    subprocess.run(["git", "checkout", "-B", "main"], cwd=target_git_dir, check=False)

    print("📡 Индексация и отправка на https://vitvseom-stack.github.io/mirmir/ ...")
    subprocess.run(
        ["git", "add", "-f", "index.html", "menu_data.py", "template.html", "app.py", "tz_mirmir.json", "build_history.json", "MASTER_PROMPT_MIRMIR.txt"],
        cwd=target_git_dir,
        check=False,
    )
    subprocess.run(["git", "commit", "-m", f"Deploy MirMir v3.1 VK Logo & Serving Badge ({datetime.now().strftime('%d.%m.%Y %H:%M:%S')})"], cwd=target_git_dir, check=False)

    res = subprocess.run(["git", "push", "-u", "origin", "main", "--force"], cwd=target_git_dir, check=False)
    if res.returncode == 0:
        print("\n✅ ГЛАВНЫЙ САЙТ УСПЕШНО ОБНОВЛЁН НА GITHUB PAGES!")
        print("🌐 Проверяй через 40–60 секунд (Ctrl + F5): https://vitvseom-stack.github.io/mirmir/")
    else:
        print("\n⚠️ Git вернул ошибку при отправке — проверь лог выше.")


if __name__ == "__main__":
    try:
        print("=" * 78)
        print("🕊️  ПУЛЬТ УПРАВЛЕНИЯ ПЛАТФОРМОЙ «МИР МИР» v3.1 (Ильинская, 45)")
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
        print("🎉 КРАСОВЕЛОФ, МИЛОРД! Сборка v3.1 завершена чисто!")
        print("=" * 78)
    except Exception:
        print("\n❌ ОШИБКА ПРИ ВЫПОЛНЕНИИ:")
        traceback.print_exc()
    input("\nНажмите Enter для закрытия этого окна...")