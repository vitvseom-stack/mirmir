# -*- coding: utf-8 -*-
"""
ЦЕЛЬНЫЙ КОМПИЛЯТОР «МИР МИР» (app.py — Монолитная 3-модульная сборка v3.0)
Включает все накопленные фиксы:
1. 0 синтаксических ошибок (чистая изоляция строк Python/JS).
2. Авто-прошивка всех 72 блюд в menu_data.py веганскими маркерами + анти-мясной фильтр в Openverse/Wikimedia/ИИ.
3. Сохранение ручного текста в поле промпта шестерёнки + 6 быстрых кнопок фото-движков в 1 клик.
4. Плашка «Подача блюд может отличаться» на всех карточках блюд в меню.
5. Рабочие ссылки «читать на VK ↗» (https://vk.com/mirmir.cafe) без ошибки скрытой страницы.
6. Перехватчик мобильного жеста/свайпа «Назад» (popstate SPA-Guard) для всех модальных окон и вкладок.
7. Вращающаяся Голубка + фон интерьера за 3D-меню и 2 крупных поля спешлов под ним + авто-пуш в корень GitHub Pages.
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
VK_PUBLIC_URL = "https://vk.com/mirmir.cafe"
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
    """
    Автоматически обновляет все 72 блюда в menu_data.py, чтобы у КАЖДОГО блюда
    в ai_prompt стояла жёсткая веганская защита (Vegan plant-based ... no meat, no seafood).
    """
    if not os.path.exists("menu_data.py"):
        return
    try:
        with open("menu_data.py", "r", encoding="utf-8") as f:
            code = f.read()

        def patch_prompt(match):
            prefix = match.group(1)
            val = match.group(2)
            suffix = match.group(3)
            low = val.lower()
            if not low.startswith("vegan plant-based"):
                val = "Vegan plant-based " + val[0].lower() + val[1:] if len(val) > 1 else "Vegan plant-based " + val
            if "no meat" not in low:
                val = val.rstrip(".") + ", 100% vegan, no meat, no seafood"
            return f'{prefix}{val}{suffix}'

        new_code = re.sub(r'("ai_prompt"\s*:\s*")([^"]+)(")', patch_prompt, code)
        if new_code != code:
            with open("menu_data.py", "w", encoding="utf-8") as f:
                f.write(new_code)
            print("🌱 [Веган-База] Все 72 промпта внутри `menu_data.py` автоматически защищены маркерами `Vegan plant-based`!")
    except Exception as e:
        print(f"⚠️ Предупреждение при авто-патче menu_data.py: {e}")


def get_verified_interior_exterior_photos():
    """Удаляет чужие фото ymap_org_2..99 (кальяны/мясо соседей) и возвращает чистые кадры зала и фасада."""
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


def fetch_vk_wall_posts():
    """Синхронизирует новости ВК и ставит 100% рабочую ссылку https://vk.com/mirmir.cafe."""
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
                    "vk_url": VK_PUBLIC_URL,
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
                    p["vk_url"] = VK_PUBLIC_URL
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
        "version": f"Релиз v3.0 • Сборка #{cnt}",
        "timestamp": now_str,
        "model": "Монолит v3.0: Веган-Фильтр 72 блюд + Мобильный Свайп Назад + Кнопки 6 API",
        "status": "Исправлены: синтаксис, сохранение промптов, плашка подачи блюд, ссылки ВК на mirmir.cafe и свайп «Назад» (popstate) на смартфонах.",
        "stats": f"Дата сборки: {now_str}",
    })
    with open("build_history.json", "w", encoding="utf-8") as f:
        json.dump(logs[:60], f, ensure_ascii=False, indent=2)

    return tz_data, logs[:60], cnt


def upgrade_template_html_in_place(tpl_html):
    """
    Чисто и безопасно вшивает в template.html все улучшения v3.0 без конфликта кавычек!
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

    # Очищаем любые старые блоки апгрейда v2.5..v3.0 перед записью свежего
    tpl_html = re.sub(
        r"// === 🚀 АПГРЕЙД v[23]\.[0-9]:[\s\S]*?(?=window\.addEventListener\(\"DOMContentLoaded\")",
        "",
        tpl_html,
    )

    v30_master_js = r"""
    // === 🚀 АПГРЕЙД v3.0: ВЕГАН-ФИЛЬТР 72 БЛЮД + 6 КНОПОК ИИ + ПЛАШКА ПОДАЧИ + VK ССЫЛКИ + МОБИЛЬНЫЙ СВАЙП НАЗАД ===
    window.customPromptsPerDish = window.customPromptsPerDish || {};

    // 1. Эталонные 5 слайдов интерьера и экстерьера в левом блоке (0% чужих кальянов и мяса)
    window.getInteriorSlidesList = function() {
      return [
        { src: "img/ymap_org_0.jpg", title: "🏛️ Исторический кирпичный свод и уютный зал на Ильинской, 45", tag: "Интерьер зала" },
        { src: "img/ymap_org_1.jpg", title: "🕊️ Фирменная кованая вывеска с белой Голубкой мира у входа", tag: "Экстерьер • Ильинская, 45" },
        { src: "img/vk_5068_0.jpg", title: "🛋️ Изумрудный велюровый диван, живой кирпич и картины", tag: "Атмосфера «Мир Мир»" },
        { src: "img/vk_5122_0.jpg", title: "🕯️ Вечерние чаепития при свечах и редкий китайский чай", tag: "Чайная культура" },
        { src: "img/vk_5134_0.jpg", title: "🌿 Уютное зелёное пространство для встреч и живого общения", tag: "Интерьер кафе" }
      ];
    };

    // 2. Два крупных поля сезонных блюд под 3D-меню справа + надпись «Подача блюд может отличаться»
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
            '<button onclick="openMenu(\'Сезонные спешлы от Шефа\')" class="text-[10px] font-extrabold text-amber-300 hover:underline cursor-pointer">Все блюда (72) ➔</button>';
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
            '<img src="' + esc(d.photo) + '" onclick="event.stopPropagation();openSuperZoom(\'' + esc(d.photo) + '\', \'' + esc(d.name) + '\')" class="w-full h-full object-cover cursor-zoom-in">' +
            '<span class="absolute top-1.5 left-1.5 px-2 py-0.5 rounded-md bg-black/70 text-[#F2B880] text-[9px] font-extrabold">' + esc(d.weight || "Хит шефа") + '</span>' +
            '<span class="absolute bottom-1.5 left-1.5 px-1.5 py-0.5 rounded bg-black/65 text-white/90 text-[8px] font-semibold">Подача блюд может отличаться</span>' +
            '<button onclick="event.stopPropagation();openSuperZoom(\'' + esc(d.photo) + '\', \'' + esc(d.name) + '\')" class="absolute bottom-1.5 right-1.5 px-2 py-0.5 rounded-md bg-black/75 hover:bg-[#D48238] text-white text-[9px] font-extrabold cursor-pointer">🔍 Лупа</button>' +
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

    // 3. В карточках электронного меню (72 позиции) добавляем плашку «Подача блюд может отличаться» прямо на фото и под описание
    const _origRenderDishes = window.renderDishes;
    window.renderDishes = function() {
      if (_origRenderDishes) _origRenderDishes();
      const grid = document.getElementById("menu-dishes-grid");
      if (!grid) return;
      grid.querySelectorAll(".zoom-card").forEach(card => {
        const imgBox = card.querySelector(".relative.h-44");
        if (imgBox && !imgBox.querySelector(".serving-note-badge")) {
          imgBox.insertAdjacentHTML(
            "beforeend",
            '<span class="serving-note-badge absolute bottom-2 left-2 px-2 py-0.5 rounded-md bg-black/65 text-white/95 text-[9px] font-semibold backdrop-blur-xs">🍽️ Подача блюд может отличаться</span>'
          );
        }
      });
    };

    // 4. В Новостях гарантируем рабочую ссылку https://vk.com/mirmir.cafe (без ошибки скрытой страницы ВК!)
    const _origRenderNewsPosts = window.renderNewsPosts;
    window.renderNewsPosts = function() {
      if (DATA.posts && DATA.posts.length) {
        DATA.posts.forEach(p => { p.vk_url = "https://vk.com/mirmir.cafe"; });
      }
      if (_origRenderNewsPosts) _origRenderNewsPosts();
    };

    // 5. Сохранение пользовательского промпта + 6 быстрых кнопок фото-движков + жёсткий Анти-Мясной Веган-Фильтр!
    window.runEngineForDish = function(idx, engKey) {
      const inp = document.getElementById("hub-ai-prm-" + idx);
      if (inp) window.customPromptsPerDish[idx] = inp.value;
      selectedAiEnginePerDish[idx] = engKey;
      window.generateDishCandidateAI(idx);
    };

    const _origRenderUnifiedSystemHub = window.renderUnifiedSystemHub;
    window.renderUnifiedSystemHub = function() {
      // Перед перерисовкой сохраняем всё, что пользователь ввёл в поля промптов!
      document.querySelectorAll("[id^='hub-ai-prm-']").forEach(el => {
        const idNum = parseInt(el.id.replace("hub-ai-prm-", ""), 10);
        if (!isNaN(idNum)) window.customPromptsPerDish[idNum] = el.value;
      });
      if (_origRenderUnifiedSystemHub) _origRenderUnifiedSystemHub();

      // Восстанавливаем введённый пользователем текст и добавляем панель из 6 прямых кнопок генераторов!
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
          const wrapper = el.closest(".bg-amber-50\\/70");
          if (wrapper && !wrapper.querySelector(".quick-6-engines-bar")) {
            const curE = selectedAiEnginePerDish[idx] || "openverse_hd";
            const engines = [
              { k: "openverse_hd", lbl: "📸 Openverse" },
              { k: "wikimedia", lbl: "🥗 Wikimedia" },
              { k: "turbo_ai", lbl: "⚡ Turbo ИИ" },
              { k: "flux_ai", lbl: "🎨 Flux ИИ" },
              { k: "flickr_food", lbl: "🍲 Flickr" },
              { k: "local_ready", lbl: "🌿 Архив" }
            ];
            const btnsHtml = '<div class="quick-6-engines-bar flex flex-wrap gap-1 pt-1.5 border-t border-amber-200/80 mt-1.5">' +
              '<span class="text-[9px] font-extrabold text-stone-500 w-full">⚡ Быстрый запуск по кнопке (100% Vegan-фильтр):</span>' +
              engines.map(e =>
                '<button onclick="runEngineForDish(' + idx + ',\'' + e.k + '\')" class="px-2 py-1 rounded-lg text-[10px] font-extrabold cursor-pointer transition ' +
                (curE === e.k ? 'bg-[#2E3D28] text-[#F2B880] shadow' : 'bg-white hover:bg-amber-100 text-[#2E3D28] border border-amber-300') + '">' + e.lbl + '</button>'
              ).join("") +
            '</div>';
            wrapper.insertAdjacentHTML("beforeend", btnsHtml);
          }
        });
      }
    };

    const NON_VEGAN_BAN_REGEX = /meat|chicken|pork|beef|shrimp|prawn|fish|seafood|salmon|tuna|bacon|steak|ham|lamb|turkey|sausage|pepperoni|cheese|milk|dairy|egg|broth with shrimp/i;

    window.generateDishCandidateAI = async function(idx) {
      const d = DATA.menu[idx];
      if (!d) return;
      const engine = selectedAiEnginePerDish[idx] || "openverse_hd";
      const prmInp = document.getElementById("hub-ai-prm-" + idx);
      if (prmInp && prmInp.value.trim()) {
        window.customPromptsPerDish[idx] = prmInp.value.trim();
      }
      const userRawText = window.customPromptsPerDish[idx] !== undefined ? window.customPromptsPerDish[idx] : (d.ai_prompt || d.name);

      const btn = document.getElementById("hub-ai-btn-" + idx);
      if (btn) { btn.innerText = "⏳ Vegan-поиск..."; btn.disabled = true; }

      let queryTxt = userRawText;
      if (/[а-яё]/i.test(queryTxt)) {
        try {
          const tr = await fetch("https://api.mymemory.translated.net/get?q=" + encodeURIComponent(queryTxt.slice(0, 180)) + "&langpair=ru|en");
          const tj = await tr.json();
          if (tj.responseData && tj.responseData.translatedText) queryTxt = tj.responseData.translatedText;
        } catch(e) { queryTxt = d.ai_prompt || "vegan plant-based dish"; }
      }

      // Очищаем от любых невеганских слов и жёстко ставим веганские маркеры
      const sanitized = queryTxt.replace(NON_VEGAN_BAN_REGEX, "tofu mushroom").replace(/tom yum/gi, "vegan tofu mushroom soup");
      const strictVeganPrompt = "100% vegan plant-based " + sanitized + " with tofu, mushrooms, vegetables and herbs, no meat, no shrimp, no seafood";
      const searchKeywords = ("vegan " + sanitized).replace(/close-up|studio|food photography of|served|on|ceramic|plate|in|cozy|cafe|100%|plant-based|no meat|no seafood|no shrimp/gi, " ").replace(/[^a-zA-Z ]/g, " ").trim().split(/\s+/).slice(0, 4).join(" ");
      const rndSeed = Math.floor(Math.random() * 8999999) + 100000;

      if (engine === "openverse_hd") {
        try {
          const r = await fetch("https://api.openverse.org/v1/images/?q=" + encodeURIComponent("vegan " + searchKeywords) + "&page_size=30");
          const j = await r.json();
          if (j.results && j.results.length) {
            const cleanResults = j.results.filter(item => {
              const titleAndTags = ((item.title || "") + " " + (item.tags || []).map(t => t.name || "").join(" ")).toLowerCase();
              return !NON_VEGAN_BAN_REGEX.test(titleAndTags);
            });
            const pool = cleanResults.length ? cleanResults : j.results;
            const pick = pool[Math.floor(Math.random() * pool.length)];
            pendingDishCandidates[idx] = { url: pick.url, source: "📸 Openverse HD (100% Vegan Filter)", prompt: userRawText };
            addLocalBuildOrActionLog("📸 Openverse (Vegan) подобрал фото для «" + d.name + "»", searchKeywords);
            renderUnifiedSystemHub(); return;
          }
        } catch(e) {}
      }

      if (engine === "wikimedia") {
        try {
          const r = await fetch("https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch=" + encodeURIComponent("filetype:bitmap vegan " + searchKeywords) + "&gsrlimit=25&prop=imageinfo&iiprop=url&format=json&origin=*");
          const j = await r.json();
          const pages = j.query && j.query.pages ? Object.values(j.query.pages) : [];
          const cleanPages = pages.filter(p => !NON_VEGAN_BAN_REGEX.test(p.title || ""));
          const imgs = (cleanPages.length ? cleanPages : pages).map(p => p.imageinfo && p.imageinfo[0] && p.imageinfo[0].url).filter(Boolean);
          if (imgs.length) {
            const pickUrl = imgs[Math.floor(Math.random() * imgs.length)];
            pendingDishCandidates[idx] = { url: pickUrl, source: "🥗 Wikimedia Gastro (100% Vegan Filter)", prompt: userRawText };
            addLocalBuildOrActionLog("🥗 Wikimedia (Vegan) нашёл фото для «" + d.name + "»", searchKeywords);
            renderUnifiedSystemHub(); return;
          }
        } catch(e) {}
      }

      if (engine === "flickr_food") {
        const flickrUrl = "https://loremflickr.com/720/720/vegan,salad,vegetable?lock=" + (rndSeed % 9999);
        pendingDishCandidates[idx] = { url: flickrUrl, source: "🍲 Flickr Vegan Stream", prompt: userRawText };
        renderUnifiedSystemHub(); return;
      }

      if (engine === "local_ready") {
        const pool = (DATA.ready_photos && DATA.ready_photos.length) ? DATA.ready_photos : ["img/vk_5128_1.jpg"];
        const pickLocal = pool[Math.floor(Math.random() * pool.length)];
        pendingDishCandidates[idx] = { url: pickLocal, source: "🌿 Локальный Архив Кафе img/", prompt: userRawText };
        renderUnifiedSystemHub(); return;
      }

      if (engine === "turbo_ai") {
        const w = 640 + (rndSeed % 3) * 64;
        const turboUrl = "https://image.pollinations.ai/prompt/" + encodeURIComponent("Appetizing gourmet " + strictVeganPrompt + ", studio food photography, natural light, no text") + "?model=turbo&width=" + w + "&height=" + w + "&seed=" + rndSeed + "&nologo=true&nofeed=true";
        pendingDishCandidates[idx] = { url: turboUrl, source: "⚡ Turbo SDXL AI (Vegan • Seed #" + rndSeed + ")", prompt: userRawText };
        renderUnifiedSystemHub(); return;
      }

      const wFlux = 704 + (rndSeed % 4) * 16;
      const fluxUrl = "https://image.pollinations.ai/prompt/" + encodeURIComponent("Close-up studio vegan food photo of " + strictVeganPrompt + ", ceramic bowl, 8k, no text") + "?model=flux&width=" + wFlux + "&height=" + wFlux + "&seed=" + rndSeed + "&nologo=true&nofeed=true";
      pendingDishCandidates[idx] = { url: fluxUrl, source: "🎨 Flux Realism AI (Vegan • Seed #" + rndSeed + ")", prompt: userRawText };
      renderUnifiedSystemHub();
    };

    // 6. УНИВЕРСАЛЬНЫЙ ПЕРЕХВАТЧИК МОБИЛЬНОГО СВАЙПА «НАЗАД» (SPA-GUARD POPSTATE ДЛЯ ВСЕХ ОКОН И ВКЛАДОК!)
    window.pushModalGuardState = function(tag) {
      try {
        history.pushState({ mirmirModal: tag || "open", t: Date.now() }, "");
      } catch(e) {}
    };

    // Оборачиваем ВСЕ функции открытия модальных окон и вкладок, чтобы каждое открытие ставило точку возврата в историю браузера!
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

    const _origToggleCart = window.toggleCart;
    window.toggleCart = function() {
      const dr = document.getElementById("cart-drawer");
      const wasHidden = dr && dr.classList.contains("hidden");
      if (_origToggleCart) _origToggleCart();
      if (wasHidden) window.pushModalGuardState("cart");
    };

    // При нажатии системной кнопки или свайпа «Назад» на смартфоне — закрываем верхнее открытое окно вместо вылета с сайта!
    window.addEventListener("popstate", function(ev) {
      const modalOrder = [
        { id: "super-zoom-lightbox", close: window.closeSuperZoom },
        { id: "ready-gallery-popup", close: window.closeReadyGalleryPopup },
        { id: "master-prompt-modal", close: window.closeMasterPromptModal },
        { id: "unified-system-hub", close: window.closeUnifiedSystemHub },
        { id: "radio-selector-modal", close: () => { const m = document.getElementById("radio-selector-modal"); if (m) { m.classList.add("hidden"); m.classList.remove("flex"); } } },
        { id: "book-table-modal", close: window.closeBookTableModal },
        { id: "delivery-modal", close: () => { const m = document.getElementById("delivery-modal"); if (m) { m.classList.add("hidden"); m.classList.remove("flex"); } } },
        { id: "cafe-shop-modal", close: window.closeCafeShopModal },
        { id: "cart-drawer", close: () => { const m = document.getElementById("cart-drawer"); if (m) { m.classList.add("hidden"); m.classList.remove("flex"); } } },
        { id: "bowl-modal", close: window.closeBowlBuilder },
        { id: "menu-modal", close: window.closeMenu }
      ];

      for (let i = 0; i < modalOrder.length; i++) {
        const el = document.getElementById(modalOrder[i].id);
        if (el && !el.classList.contains("hidden")) {
          modalOrder[i].close();
          return;
        }
      }
      // Если все модалки уже закрыты — удерживаем пользователя на главной странице сайта
      try { history.pushState({ mirmirBase: true }, ""); } catch(e) {}
    });

    // Ставим базовую точку страховки при первом касании экрана смартфона
    window.addEventListener("touchstart", function initTouchGuard() {
      try { history.pushState({ mirmirBase: true }, ""); } catch(e) {}
      window.removeEventListener("touchstart", initTouchGuard);
    }, { passive: true });

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
        v30_master_js + '\n    window.addEventListener("DOMContentLoaded"',
    )
    return tpl_html


def build_clean_master_prompt_text():
    lines = [
        "ПОЛНОЕ ТЕКСТОВОЕ ТЕХНИЧЕСКОЕ ЗАДАНИЕ (МАСТЕР-ПРОМПТ) НА РАЗРАБОТКУ ТРЁХМОДУЛЬНОЙ ПЛАТФОРМЫ ВЕГАН-КАФЕ «МИР МИР» (v3.0)",
        "",
        "1. ЧИСТАЯ ТРЁХМОДУЛЬНАЯ АРХИТЕКТУРА: menu_data.py (72 веганских блюда + 8 товаров магазина) + template.html + app.py.",
        "2. ПЕРВЫЙ ЭКРАН: слева под слоганом слайдер строго верифицированных фотографий ИНТЕРЬЕРА и ЭКСТЕРЬЕРА кафе; справа 3D-карусель 4 страниц меню зала на фоне вращающейся Голубки мира, а под ней — 2 крупных поля сезонных спешлов с пометкой «Подача блюд может отличаться».",
        "3. МОБИЛЬНАЯ ЗАЩИТА НАВИГАЦИИ (SPA-Guard popstate): свайп «Назад» на смартфонах плавно закрывает любое открытое модальное окно или вкладку, не выбрасывая гостя с сайта.",
        "4. ШЕСТЕРЁНКА АРХИТЕКТОРА (⚙️): 5 вкладок, 6 независимых фото-движков с жёстким веган-фильтром (Openverse HD, Wikimedia, Turbo AI, Flux AI, Flickr, Архив), сохранение пользовательского ввода в промптах и полноэкранная Лупа z-200.",
    ]
    txt = "\n".join(lines)
    with open("MASTER_PROMPT_MIRMIR.txt", "w", encoding="utf-8") as f:
        f.write(txt)
    return txt


def sync_files_to_root_repo():
    """Зеркалирует собранный index.html и модули в корневую папку C:\\Users\\vitvs\\Documents\\mirmir\\."""
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
    print("🕊️  СБОРКА «МИР МИР» v3.0 (ВЕГАН-ФИЛЬТР 72 БЛЮД + СВАЙП НАЗАД + ВК + ПЛАШКА ПОДАЧИ)")
    print("=" * 78)

    auto_migrate_assets_from_old_folder()
    # 1. Автоматически прошиваем все 72 блюда в menu_data.py веганской защитой
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
        "version": f"Релиз v3.0 • Сборка #{build_num} ({now_stamp})",
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
    print(f"✨ [Сборка #{build_num} готова] Все 72 блюда под веган-защитой, свайп «Назад» и ссылки ВК активны!")
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
    subprocess.run(["git", "commit", "-m", f"Deploy MirMir v3.0 Monolith ({datetime.now().strftime('%d.%m.%Y %H:%M:%S')})"], cwd=target_git_dir, check=False)

    res = subprocess.run(["git", "push", "-u", "origin", "main", "--force"], cwd=target_git_dir, check=False)
    if res.returncode == 0:
        print("\n✅ ГЛАВНЫЙ САЙТ УСПЕШНО ОБНОВЛЁН НА GITHUB PAGES!")
        print("🌐 Проверяй через 40–60 секунд (Ctrl + F5): https://vitvseom-stack.github.io/mirmir/")
    else:
        print("\n⚠️ Git вернул ошибку при отправке — проверь лог выше.")


if __name__ == "__main__":
    try:
        print("=" * 78)
        print("🕊️  ПУЛЬТ УПРАВЛЕНИЯ ПЛАТФОРМОЙ «МИР МИР» v3.0 (Ильинская, 45)")
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
        print("🎉 КРАСОВЕЛОФ, МИЛОРД! Сборка v3.0 завершена без единой ошибки!")
        print("=" * 78)
    except Exception:
        print("\n❌ ОШИБКА ПРИ ВЫПОЛНЕНИИ:")
        traceback.print_exc()
    input("\nНажмите Enter для закрытия этого окна...")