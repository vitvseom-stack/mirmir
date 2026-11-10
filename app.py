# -*- coding: utf-8 -*-
"""
ЦЕЛЬНЫЙ КОМПИЛЯТОР «МИР МИР» (app.py — Чистая 3-модульная сборка v2.7)
1. Автоматически синхронизирует собранный index.html из подпапки `new` в КОРЕНЬ репозитория `Documents/mirmir/`,
   чтобы главная витрина https://vitvseom-stack.github.io/mirmir/ обновлялась со 100% гарантией!
2. Удаляет чужие фото с Яндекс.Карт (мясо/кальяны) и в `new/img/`, и в корневом `img/`.
3. Слева под слоганом крутит только проверенные фото ИНТЕРЬЕРА и ЭКСТЕРЬЕРА кафе.
4. Справа под 3D-меню выводит 2 КРУПНЫХ ПОЛЯ ДЛЯ КАРТИНОК блюд + Голубку мира на фоне.
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

# Определяем корневую папку главного репозитория (если мы внутри mirmir/new)
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
YANDEX_ORG_ID = "7309581265"

OLD_DIRS_TO_CHECK = [
    DEFAULT_MIRMIR_ROOT,
    PARENT_DIR,
]


def auto_migrate_assets_from_old_folder():
    """Переносит папку img/, ключи и кэши из старой папки mirmir в новую."""
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


def get_verified_interior_exterior_photos():
    """Удаляет чужие фото ymap_org_2..99 и возвращает проверенные кадры ИНТЕРЬЕРА и ЭКСТЕРЬЕРА «Мир Мир»."""
    for target_img_dir in [os.path.join(BASE_DIR, "img"), os.path.join(ROOT_REPO_DIR, "img")]:
        if os.path.exists(target_img_dir):
            for fn in list(os.listdir(target_img_dir)):
                if fn.startswith("ymap_org_") and fn not in ("ymap_org_0.jpg", "ymap_org_1.jpg"):
                    try:
                        os.remove(os.path.join(target_img_dir, fn))
                    except Exception:
                        pass

    verified_candidates = [
        "img/ymap_org_0.jpg",  # Кирпичный свод и зал на Ильинской, 45
        "img/ymap_org_1.jpg",  # Уличная кованая вывеска с белой Голубкой мира (Экстерьер)
        "img/vk_5068_0.jpg",   # Изумрудный велюровый диван, кирпич и картины (Интерьер)
        "img/vk_5122_0.jpg",   # Вечерние чаепития при свечах (Атмосфера зала)
        "img/vk_5134_0.jpg",   # Уютный зал и живые растения (Интерьер)
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


def fetch_vk_wall_posts():
    """Синхронизирует посты со стены ВК или отдаёт проверенный локальный кэш."""
    vk_token = os.environ.get("VK_TOKEN") or read_local_secret("vk key.txt")
    posts_out = []
    if vk_token:
        try:
            r = requests.get(
                "https://api.vk.com/method/wall.get",
                params={"owner_id": VK_OWNER_ID, "count": 15, "access_token": vk_token, "v": "5.199"},
                timeout=8,
            )
            items = r.json().get("response", {}).get("items", [])
            for it in items:
                txt = (it.get("text") or "").strip()
                if not txt or len(txt) < 15:
                    continue
                post_id = it.get("id")
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
                posts_out.append({
                    "id": post_id,
                    "date": dt_str,
                    "likes": likes,
                    "title": first_line[:68] + ("..." if len(first_line) > 68 else ""),
                    "text": txt[:280] + ("..." if len(txt) > 280 else ""),
                    "photo": photo_local,
                    "vk_url": f"https://vk.com/wall{VK_OWNER_ID}_{post_id}",
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
                for p in cached:
                    pid = p.get("id", "")
                    if not p.get("vk_url"):
                        p["vk_url"] = f"https://vk.com/wall{VK_OWNER_ID}_{pid}" if pid else "https://vk.com/mirmir.cafe"
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
        "version": f"Релиз v2.7 • Сборка #{cnt}",
        "timestamp": now_str,
        "model": "Прямая синхронизация корня GitHub Pages + 2 крупных поля блюд",
        "status": "Корневой index.html синхронизирован с подпапкой new. Убраны чужие фото Яндекс.Карт, слева — интерьер/экстерьер, справа — 2 крупных поля спешлов.",
        "stats": f"Дата сборки: {now_str}",
    })
    with open("build_history.json", "w", encoding="utf-8") as f:
        json.dump(logs[:60], f, ensure_ascii=False, indent=2)

    return tz_data, logs[:60], cnt


def upgrade_template_html_in_place(tpl_html):
    """Модернизирует template.html (Голубка справа + 5 чистых слайдов зала слева + 2 крупных поля блюд справа)."""
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

    tpl_html = re.sub(
        r"// === 🚀 АПГРЕЙД v2\.[567]:[\s\S]*?(?=window\.addEventListener\(\"DOMContentLoaded\")",
        "",
        tpl_html,
    )

    v27_override_js = """
    // === 🚀 АПГРЕЙД v2.7: СЛЕВА ТОЛЬКО ИНТЕРЬЕР/ЭКСТЕРЬЕР + СПРАВА ПОД МЕНЮ 2 КРУПНЫХ ПОЛЯ ДЛЯ КАРТИНОК БЛЮД ===
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

    const _origRenderHeroRight = window.renderHeroRightColumn;
    window.renderHeroRightColumn = function() {
      if (_origRenderHeroRight) _origRenderHeroRight();
      window.renderRightTwoPictureFields();
    };

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
    """

    tpl_html = tpl_html.replace(
        'window.addEventListener("DOMContentLoaded"',
        v27_override_js + '\n    window.addEventListener("DOMContentLoaded"',
    )
    return tpl_html


def build_clean_master_prompt_text():
    lines = [
        "ПОЛНОЕ ТЕКСТОВОЕ ТЕХНИЧЕСКОЕ ЗАДАНИЕ (МАСТЕР-ПРОМПТ) НА РАЗРАБОТКУ ТРЁХМОДУЛЬНОЙ ПЛАТФОРМЫ ВЕГАН-КАФЕ «МИР МИР»",
        "",
        "1. ЧИСТАЯ ТРЁХМОДУЛЬНАЯ АРХИТЕКТУРА: menu_data.py (72 блюда + 8 товаров магазина) + template.html + app.py.",
        "2. ПЕРВЫЙ ЭКРАН: слева под слоганом слайдер строго верифицированных фотографий ИНТЕРЬЕРА и ЭКСТЕРЬЕРА кафе; справа 3D-карусель 4 страниц меню зала на фоне вращающейся Голубки мира, а прямо под ней — 2 крупных поля для картинок сезонных блюд от Шефа.",
        "3. ШЕСТЕРЁНКА АРХИТЕКТОРА (⚙️): 5 вкладок, включая студию всех 72 блюд с 6 независимыми фото-движками без лимитов, полноэкранной Лупой z-200 и кнопкой «✅ Утвердить в меню».",
    ]
    txt = "\n".join(lines)
    with open("MASTER_PROMPT_MIRMIR.txt", "w", encoding="utf-8") as f:
        f.write(txt)
    return txt


def sync_files_to_root_repo():
    """Копирует свежесобранный index.html и модули из подпапки `new` в корень `Documents/mirmir/`."""
    if os.path.abspath(ROOT_REPO_DIR) == os.path.abspath(BASE_DIR):
        return
    files_to_mirror = [
        "index.html",
        "menu_data.py",
        "template.html",
        "app.py",
        "tz_mirmir.json",
        "build_history.json",
        "MASTER_PROMPT_MIRMIR.txt",
        "run_counter.txt",
    ]
    for fn in files_to_mirror:
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
    print("🕊️  СБОРКА «МИР МИР» v2.7 (СИНХРОНИЗАЦИЯ КОРНЯ + 2 КРУПНЫХ ПОЛЯ БЛЮД СПРАВА)")
    print("=" * 78)

    auto_migrate_assets_from_old_folder()
    from menu_data import MENU_DATABASE, CAFE_SHOP_ITEMS

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
        "version": f"Релиз v2.7 • Сборка #{build_num} ({now_stamp})",
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

    # Сразу копируем готовый index.html в корневую папку C:\Users\vitvs\Documents\mirmir\
    sync_files_to_root_repo()

    print(f"✨ [Сборка #{build_num} готова] Чистых фото зала/фасада: {len(ymap_photos)}, Справа под меню: 2 крупных фото-поля!")
    try:
        os.startfile("index.html")
    except Exception:
        pass


def push_to_github():
    """Удаляет ложную полупустую папку new/.git и пушит напрямую из КОРНЕВОГО репозитория Documents/mirmir!"""
    sync_files_to_root_repo()

    # Если мы в подпапке mirmir/new, а в родительской папке mirmir есть настоящий .git — убираем мешающий new/.git
    local_git = os.path.join(BASE_DIR, ".git")
    if os.path.abspath(ROOT_REPO_DIR) != os.path.abspath(BASE_DIR) and os.path.exists(local_git):
        try:
            shutil.rmtree(local_git, ignore_errors=True)
            print("🧹 Убрана пустая вложенная папка `new/.git` (используем главный корневой репозиторий).")
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

    print("📡 Индексация КОРНЕВОГО index.html и принудительная отправка на https://vitvseom-stack.github.io/mirmir/ ...")
    subprocess.run(
        ["git", "add", "-f", "index.html", "menu_data.py", "template.html", "app.py", "tz_mirmir.json", "build_history.json", "MASTER_PROMPT_MIRMIR.txt"],
        cwd=target_git_dir,
        check=False,
    )
    subprocess.run(["git", "commit", "-m", f"Root Deploy MirMir v2.7 ({datetime.now().strftime('%d.%m.%Y %H:%M:%S')})"], cwd=target_git_dir, check=False)

    res = subprocess.run(["git", "push", "-u", "origin", "main", "--force"], cwd=target_git_dir, check=False)
    if res.returncode == 0:
        print("\n✅ ГЛАВНЫЙ КОРНЕВОЙ INDEX.HTML УСПЕШНО ОТПРАВЛЕН НА GITHUB PAGES!")
        print("🌐 Через 40–60 секунд открой https://vitvseom-stack.github.io/mirmir/ и нажми Ctrl + F5!")
    else:
        print("\n⚠️ Git вернул ошибку при отправке — проверь сообщения в консоли выше.")


if __name__ == "__main__":
    try:
        print("=" * 78)
        print("🕊️  ПУЛЬТ УПРАВЛЕНИЯ ПЛАТФОРМОЙ «МИР МИР» (Ильинская, 45)")
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
        print("🎉 КРАСОВЕЛОФ, МИЛОРД! Все операции выполнены чисто!")
        print("=" * 78)
    except Exception:
        print("\n❌ ОШИБКА ПРИ ВЫПОЛНЕНИИ:")
        traceback.print_exc()
    input("\nНажмите Enter для закрытия этого окна...")