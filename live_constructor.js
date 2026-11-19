// ============================================================================
// АВТОНОМНЫЙ КОНСТРУКТОР ОКОН И ФОТО (live_constructor.js — v4.8)
// Без MutationObserver. Кнопки +/-, сдвиг, ресайз мышью и «✅ Применить».
// ============================================================================
(function() {
  const LS_STATE_KEY = "mirmir_lc_state_v48";
  const LS_ENABLED_KEY = "mirmir_lc_enabled_v48";
  const DEFAULT_SITE_WIDTH = 1320;

  window.lcActive = false;
  window.lcTargetImgEl = null;
  window.lcTargetImgId = "";

  window.isLcEnabledInHub = function() {
    try { return localStorage.getItem(LS_ENABLED_KEY) === "1"; } catch (e) { return false; }
  };

  window.setLcEnabledInHub = function(flag) {
    try { localStorage.setItem(LS_ENABLED_KEY, flag ? "1" : "0"); } catch (e) {}
    if (!flag && window.lcActive) {
      window.lcActive = false;
      document.body.classList.remove("lc-mode-on");
      window.decoratePageForConstructor();
    }
    window.renderLcFloatingControls();
    if (typeof window.renderUnifiedSystemHub === "function") {
      window.renderUnifiedSystemHub();
    }
  };

  function loadState() {
    try {
      const raw = localStorage.getItem(LS_STATE_KEY);
      const parsed = raw ? JSON.parse(raw) : {};
      return {
        siteWidth: Number(parsed.siteWidth) || DEFAULT_SITE_WIDTH,
        coverMode: Boolean(parsed.coverMode),
        images: parsed.images || {},
        boxes: parsed.boxes || {}
      };
    } catch (e) {
      return { siteWidth: DEFAULT_SITE_WIDTH, coverMode: false, images: {}, boxes: {} };
    }
  }

  function saveState(st) {
    try { localStorage.setItem(LS_STATE_KEY, JSON.stringify(st)); } catch (e) {}
  }

  window.lcState = loadState();

  function escHtml(s) {
    return String(s || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function normImgSrc(src) {
    if (!src) return "";
    const i = src.indexOf("img/");
    return i !== -1 ? src.slice(i) : src;
  }

  function getImgId(imgEl, idx) {
    if (imgEl.dataset.lcImgId) return imgEl.dataset.lcImgId;
    if (imgEl.id) {
      imgEl.dataset.lcImgId = "img_" + imgEl.id;
      return imgEl.dataset.lcImgId;
    }
    const card = imgEl.closest(".zoom-card, article, section");
    const h = card ? card.querySelector("h1, h2, h3, h4") : null;
    const slug = h
      ? h.textContent.trim().slice(0, 18).replace(/[^a-zA-Zа-яА-Я0-9]/g, "_")
      : ("im_" + idx);
    imgEl.dataset.lcImgId = "img_" + slug + "_" + idx;
    return imgEl.dataset.lcImgId;
  }

  function getBoxId(boxEl, idx) {
    if (boxEl.dataset.lcBoxId) return boxEl.dataset.lcBoxId;
    if (boxEl.id) {
      boxEl.dataset.lcBoxId = "box_" + boxEl.id;
      return boxEl.dataset.lcBoxId;
    }
    const h = boxEl.querySelector("h1, h2, h3, h4");
    const slug = h
      ? h.textContent.trim().slice(0, 18).replace(/[^a-zA-Zа-яА-Я0-9]/g, "_")
      : ("bx_" + idx);
    boxEl.dataset.lcBoxId = "box_" + slug + "_" + idx;
    return boxEl.dataset.lcBoxId;
  }

  function getInnerPhotoWrap(box) {
    return box.querySelector(
      ".mirmir-nocrop-wrap, .relative.overflow-hidden, .h-44, .h-40, .h-36, .h-32"
    );
  }

  function injectStyles() {
    let st = document.getElementById("mirmir-lc-v48-css");
    if (!st) {
      st = document.createElement("style");
      st.id = "mirmir-lc-v48-css";
      document.head.appendChild(st);
    }
    const w = window.lcState.siteWidth || DEFAULT_SITE_WIDTH;
    const css = `
      main.max-w-7xl, footer.max-w-7xl {
        max-width: ${w}px !important;
        width: 100% !important;
      }
      img.lc-custom-transformed {
        transform: translate(var(--lc-tx, 0px), var(--lc-ty, 0px)) scale(var(--lc-sc, 1)) !important;
        transition: transform 0.16s ease !important;
      }
      .lc-img-toolbar {
        display: none;
        position: absolute;
        top: 6px;
        left: 6px;
        right: 6px;
        z-index: 90 !important;
        background: rgba(18, 26, 15, 0.94);
        border: 1.5px solid #F2B880;
        border-radius: 12px;
        padding: 4px 6px;
        align-items: center;
        justify-content: space-between;
        gap: 3px;
        flex-wrap: wrap;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.55);
      }
      body.lc-mode-on .lc-img-toolbar { display: flex !important; }

      .lc-box-toolbar {
        display: none;
        position: absolute;
        top: -14px;
        left: 8px;
        z-index: 92 !important;
        background: #23311E;
        color: #FFFDF9;
        border: 1.5px solid #D48238;
        border-radius: 999px;
        padding: 2px 8px;
        font-size: 10px;
        font-weight: 800;
        align-items: center;
        gap: 4px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.45);
        white-space: nowrap;
      }
      body.lc-mode-on .lc-box-toolbar { display: inline-flex !important; }

      .lc-resize-handle {
        display: none;
        position: absolute;
        right: 4px;
        bottom: 4px;
        width: 24px;
        height: 24px;
        z-index: 93 !important;
        background: #D48238;
        color: #fff;
        border: 2px solid #FFFDF9;
        border-radius: 7px;
        font-size: 12px;
        font-weight: 900;
        align-items: center;
        justify-content: center;
        cursor: nwse-resize;
        user-select: none;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.45);
      }
      body.lc-mode-on .lc-resize-handle { display: flex !important; }

      body.lc-mode-on .lc-resizable-box:not(.lc-box-saved) {
        outline: 2px dashed rgba(212, 130, 56, 0.85) !important;
        outline-offset: 2px !important;
      }
      body.lc-mode-on .lc-resizable-box.lc-box-saved {
        outline: 2px solid #10B981 !important;
        outline-offset: 2px !important;
      }
    `;
    if (st.textContent !== css) st.textContent = css;
    document.body.classList.toggle("mirmir-crop-cover-mode", Boolean(window.lcState.coverMode));
  }

  function updateBoxDimLabel(box) {
    const lbl = box.querySelector(".lc-dim-label");
    if (!lbl) return;
    const r = box.getBoundingClientRect();
    const txt = Math.round(r.width) + "×" + Math.round(r.height);
    if (lbl.textContent !== txt) lbl.textContent = txt;
  }

  window.applyAllSavedConstructorStates = function() {
    injectStyles();
    const st = window.lcState;

    document.querySelectorAll("main img, [id$='-modal'] img").forEach((im, idx) => {
      if (im.closest("#lc-photo-picker-modal") || im.closest("#super-zoom-lightbox")) return;
      const id = getImgId(im, idx);
      const srcKey = normImgSrc(im.getAttribute("src") || "");
      const cfg = st.images[id] || st.images[srcKey];
      if (!cfg) return;

      if (cfg.src && im.getAttribute("src") !== cfg.src) {
        im.setAttribute("src", cfg.src);
        const bg = im.parentElement ? im.parentElement.querySelector(".mirmir-nocrop-bg") : null;
        if (bg) bg.style.backgroundImage = 'url("' + cfg.src + '")';
      }
      const tx = Number(cfg.tx) || 0;
      const ty = Number(cfg.ty) || 0;
      const sc = (cfg.scale !== undefined ? Number(cfg.scale) : 100) / 100;
      if (tx !== 0 || ty !== 0 || sc !== 1) {
        im.classList.add("lc-custom-transformed");
        im.style.setProperty("--lc-tx", tx + "px");
        im.style.setProperty("--lc-ty", ty + "px");
        im.style.setProperty("--lc-sc", sc.toFixed(2));
      } else {
        im.classList.remove("lc-custom-transformed");
      }
      if (cfg.fitMode === "cover") {
        im.style.setProperty("object-fit", "cover", "important");
      } else if (cfg.fitMode === "contain") {
        im.style.setProperty("object-fit", "contain", "important");
      }
    });

    document.querySelectorAll(".lc-resizable-box").forEach((box, idx) => {
      const bid = getBoxId(box, idx);
      const bCfg = st.boxes[bid] || (box.dataset.lcGroup && st.boxes["group_" + box.dataset.lcGroup]);
      if (bCfg) {
        if (bCfg.h) {
          box.style.setProperty("height", bCfg.h + "px", "important");
          box.style.setProperty("min-height", bCfg.h + "px", "important");
        }
        if (bCfg.w) {
          box.style.setProperty("width", bCfg.w + "px", "important");
          box.style.setProperty("max-width", bCfg.w + "px", "important");
        }
        if (bCfg.imgH) {
          const pic = getInnerPhotoWrap(box);
          if (pic && pic !== box) {
            pic.style.setProperty("height", bCfg.imgH + "px", "important");
            pic.style.setProperty("min-height", bCfg.imgH + "px", "important");
          }
        }
      }
      if (window.lcActive) updateBoxDimLabel(box);
    });
  };

  window.decoratePageForConstructor = function() {
    document.querySelectorAll("main h1, main h2, main h3, main h4, main p").forEach(el => {
      if (window.lcActive) el.setAttribute("contenteditable", "true");
      else el.removeAttribute("contenteditable");
    });
    if (!window.lcActive) return;

    document.querySelectorAll("main img, #menu-modal img, #cafe-shop-modal img").forEach((im, idx) => {
      if (im.closest("#lc-photo-picker-modal") || im.closest("#super-zoom-lightbox")) return;
      const parent = im.parentElement;
      if (!parent) return;
      if (window.getComputedStyle(parent).position === "static") parent.style.position = "relative";

      const imgId = getImgId(im, idx);
      if (!parent.querySelector(".lc-img-toolbar")) {
        const bar = document.createElement("div");
        bar.className = "lc-img-toolbar";
        bar.addEventListener("click", ev => { ev.preventDefault(); ev.stopPropagation(); });
        bar.innerHTML =
          '<button type="button" data-a="pick" class="px-2 py-1 rounded-lg bg-[#D48238] text-white text-[10px] font-extrabold cursor-pointer">📸 Фото</button>' +
          '<div class="flex items-center gap-1">' +
            '<button type="button" data-a="up" title="Вверх" class="w-6 h-6 rounded bg-white/15 hover:bg-white/30 text-white text-[10px] cursor-pointer">⬆️</button>' +
            '<button type="button" data-a="down" title="Вниз" class="w-6 h-6 rounded bg-white/15 hover:bg-white/30 text-white text-[10px] cursor-pointer">⬇️</button>' +
            '<button type="button" data-a="zout" title="Масштаб −" class="w-6 h-6 rounded bg-white/15 hover:bg-[#D48238] text-white text-[11px] font-extrabold cursor-pointer">➖</button>' +
            '<button type="button" data-a="zin" title="Масштаб +" class="w-6 h-6 rounded bg-white/15 hover:bg-[#D48238] text-white text-[11px] font-extrabold cursor-pointer">➕</button>' +
            '<button type="button" data-a="fit" title="Целиком / Обрезать" class="px-1.5 h-6 rounded bg-white/15 hover:bg-teal-700 text-[#F2B880] text-[9px] font-extrabold cursor-pointer">🖼️ Фон</button>' +
            '<button type="button" data-a="ok" title="Применить настройки фото" class="px-2 h-6 rounded bg-emerald-600 hover:bg-emerald-500 text-white text-[10px] font-extrabold cursor-pointer">✅ Применить</button>' +
          '</div>';
        bar.querySelectorAll("button").forEach(btn => {
          btn.addEventListener("click", function(ev) {
            ev.preventDefault();
            ev.stopPropagation();
            const a = this.getAttribute("data-a");
            if (a === "pick") window.lcOpenPhotoPicker(imgId);
            else if (a === "up") window.lcMoveOrZoomImg(imgId, 0, -14, 0);
            else if (a === "down") window.lcMoveOrZoomImg(imgId, 0, 14, 0);
            else if (a === "zout") window.lcMoveOrZoomImg(imgId, 0, 0, -8);
            else if (a === "zin") window.lcMoveOrZoomImg(imgId, 0, 0, 8);
            else if (a === "fit") window.lcToggleSingleImgFit(imgId);
            else if (a === "ok") window.lcFlashSaved(parent, "Фото применено!");
          });
        });
        parent.appendChild(bar);
      }
    });

    const specs = [
      { sel: "#v45-main-topbar", grp: "" },
      { sel: "#hero-interior-slide-img", parent: true, grp: "" },
      { sel: "#stage-3d-box", grp: "" },
      { sel: "#hero-specials-3rows .zoom-card", grp: "hero_specials" },
      { sel: "#posts-grid article", grp: "news_cards" },
      { sel: "#cat-showcase-grid .zoom-card", grp: "cat_cards" },
      { sel: "#menu-dishes-grid .zoom-card", grp: "menu_cards" },
      { sel: "#cafe-shop-grid .zoom-card", grp: "shop_cards" },
      { sel: "#menu-modal > div, #cafe-shop-modal > div, #bowl-modal > div", grp: "" }
    ];

    let bIdx = 0;
    specs.forEach(sp => {
      document.querySelectorAll(sp.sel).forEach(el => {
        const box = sp.parent ? el.parentElement : el;
        if (!box) return;
        bIdx++;
        box.classList.add("lc-resizable-box");
        if (sp.grp) box.dataset.lcGroup = sp.grp;
        if (window.getComputedStyle(box).position === "static") box.style.position = "relative";

        const bid = getBoxId(box, bIdx);
        if (!box.querySelector(".lc-box-toolbar")) {
          const tb = document.createElement("div");
          tb.className = "lc-box-toolbar";
          tb.addEventListener("click", ev => { ev.preventDefault(); ev.stopPropagation(); });
          tb.innerHTML =
            '<span class="lc-dim-label text-[#F2B880] font-mono">Размер</span>' +
            '<button type="button" data-b="hm" class="px-1.5 py-0.5 rounded bg-white/15 hover:bg-[#D48238] cursor-pointer">↕−</button>' +
            '<button type="button" data-b="hp" class="px-1.5 py-0.5 rounded bg-white/15 hover:bg-[#D48238] cursor-pointer">↕+</button>' +
            '<button type="button" data-b="wm" class="px-1.5 py-0.5 rounded bg-white/15 hover:bg-[#D48238] cursor-pointer">↔−</button>' +
            '<button type="button" data-b="wp" class="px-1.5 py-0.5 rounded bg-white/15 hover:bg-[#D48238] cursor-pointer">↔+</button>' +
            (sp.grp ? '<button type="button" data-b="grp" class="px-1.5 py-0.5 rounded bg-teal-700 text-white cursor-pointer">🔗 Всем</button>' : '') +
            '<button type="button" data-b="ok" class="px-2 py-0.5 rounded bg-emerald-600 text-white cursor-pointer">✅ Применить</button>' +
            '<button type="button" data-b="rst" class="px-1.5 py-0.5 rounded bg-rose-800 text-white cursor-pointer">✕</button>';

          tb.querySelectorAll("button").forEach(btn => {
            btn.addEventListener("click", function(ev) {
              ev.preventDefault();
              ev.stopPropagation();
              const b = this.getAttribute("data-b");
              if (b === "hm") window.lcStepBoxSize(bid, 0, -24);
              else if (b === "hp") window.lcStepBoxSize(bid, 0, 24);
              else if (b === "wm") window.lcStepBoxSize(bid, -30, 0);
              else if (b === "wp") window.lcStepBoxSize(bid, 30, 0);
              else if (b === "grp") window.lcApplyBoxToGroup(bid);
              else if (b === "ok") window.lcFlashSaved(box, "Размер блока применён!");
              else if (b === "rst") window.lcResetSingleBox(bid);
            });
          });
          box.appendChild(tb);
        }

        if (!box.querySelector(".lc-resize-handle")) {
          const hnd = document.createElement("div");
          hnd.className = "lc-resize-handle";
          hnd.title = "Тяните мышкой для изменения размера";
          hnd.innerHTML = "↘";
          hnd.addEventListener("mousedown", ev => {
            ev.preventDefault();
            ev.stopPropagation();
            startDragResize(ev, box, bid);
          });
          box.appendChild(hnd);
        }
        updateBoxDimLabel(box);
      });
    });
  };

  function findImg(id) {
    return Array.from(document.querySelectorAll("img")).find(i => i.dataset.lcImgId === id);
  }
  function findBox(id) {
    return Array.from(document.querySelectorAll(".lc-resizable-box")).find(b => b.dataset.lcBoxId === id);
  }

  window.lcMoveOrZoomImg = function(imgId, dx, dy, dScale) {
    const im = findImg(imgId);
    if (!im) return;
    const st = window.lcState;
    const srcKey = normImgSrc(im.getAttribute("src") || "");
    const cur = st.images[imgId] || st.images[srcKey] || { tx: 0, ty: 0, scale: 100 };
    cur.tx = Math.max(-180, Math.min(180, (Number(cur.tx) || 0) + dx));
    cur.ty = Math.max(-180, Math.min(180, (Number(cur.ty) || 0) + dy));
    cur.scale = Math.max(60, Math.min(220, (cur.scale !== undefined ? Number(cur.scale) : 100) + dScale));
    st.images[imgId] = cur;
    if (srcKey) st.images[srcKey] = cur;
    saveState(st);
    window.applyAllSavedConstructorStates();
  };

  window.lcToggleSingleImgFit = function(imgId) {
    const im = findImg(imgId);
    if (!im) return;
    const st = window.lcState;
    const srcKey = normImgSrc(im.getAttribute("src") || "");
    const cur = st.images[imgId] || st.images[srcKey] || { tx: 0, ty: 0, scale: 100 };
    cur.fitMode = cur.fitMode === "cover" ? "contain" : "cover";
    st.images[imgId] = cur;
    if (srcKey) st.images[srcKey] = cur;
    saveState(st);
    window.applyAllSavedConstructorStates();
  };

  window.lcStepBoxSize = function(bid, dw, dh) {
    const box = findBox(bid);
    if (!box) return;
    const r = box.getBoundingClientRect();
    const st = window.lcState;
    const cur = st.boxes[bid] || {};
    if (dw !== 0) cur.w = Math.max(180, Math.round((cur.w || r.width) + dw));
    if (dh !== 0) {
      cur.h = Math.max(90, Math.round((cur.h || r.height) + dh));
      const pic = getInnerPhotoWrap(box);
      if (pic && pic !== box) {
        cur.imgH = Math.max(70, Math.round((cur.imgH || pic.getBoundingClientRect().height) + dh));
      }
    }
    st.boxes[bid] = cur;
    saveState(st);
    window.applyAllSavedConstructorStates();
  };

  window.lcApplyBoxToGroup = function(bid) {
    const box = findBox(bid);
    if (!box || !box.dataset.lcGroup) return;
    const cfg = window.lcState.boxes[bid];
    if (!cfg) return;
    window.lcState.boxes["group_" + box.dataset.lcGroup] = Object.assign({}, cfg);
    saveState(window.lcState);
    window.applyAllSavedConstructorStates();
    if (typeof showToast === "function") showToast("🔗 Размер применён ко всем карточкам ряда");
  };

  window.lcResetSingleBox = function(bid) {
    const box = findBox(bid);
    delete window.lcState.boxes[bid];
    if (box) {
      if (box.dataset.lcGroup) delete window.lcState.boxes["group_" + box.dataset.lcGroup];
      ["height", "min-height", "width", "max-width"].forEach(p => box.style.removeProperty(p));
      const pic = getInnerPhotoWrap(box);
      if (pic) ["height", "min-height"].forEach(p => pic.style.removeProperty(p));
      updateBoxDimLabel(box);
    }
    saveState(window.lcState);
  };

  window.lcFlashSaved = function(el, msg) {
    saveState(window.lcState);
    if (el) {
      el.classList.add("lc-box-saved");
      setTimeout(() => el.classList.remove("lc-box-saved"), 1200);
    }
    if (typeof showToast === "function") showToast("✅ " + (msg || "Применено!"));
  };

  function startDragResize(startEv, box, bid) {
    const sx = startEv.clientX, sy = startEv.clientY;
    const r = box.getBoundingClientRect();
    const sw = r.width, sh = r.height;
    const pic = getInnerPhotoWrap(box);
    const sph = (pic && pic !== box) ? pic.getBoundingClientRect().height : 0;

    function onMove(ev) {
      const nw = Math.max(200, Math.round(sw + (ev.clientX - sx)));
      const nh = Math.max(90, Math.round(sh + (ev.clientY - sy)));
      box.style.setProperty("width", nw + "px", "important");
      box.style.setProperty("max-width", nw + "px", "important");
      box.style.setProperty("height", nh + "px", "important");
      box.style.setProperty("min-height", nh + "px", "important");
      window.lcState.boxes[bid] = window.lcState.boxes[bid] || {};
      window.lcState.boxes[bid].w = nw;
      window.lcState.boxes[bid].h = nh;
      if (pic && pic !== box) {
        const nph = Math.max(70, Math.round(sph + (ev.clientY - sy)));
        pic.style.setProperty("height", nph + "px", "important");
        pic.style.setProperty("min-height", nph + "px", "important");
        window.lcState.boxes[bid].imgH = nph;
      }
      updateBoxDimLabel(box);
    }
    function onUp() {
      window.removeEventListener("mousemove", onMove);
      window.removeEventListener("mouseup", onUp);
      saveState(window.lcState);
    }
    window.addEventListener("mousemove", onMove);
    window.addEventListener("mouseup", onUp);
  }

  window.lcOpenPhotoPicker = function(imgId) {
    const im = findImg(imgId);
    if (!im) return;
    window.lcTargetImgEl = im;
    window.lcTargetImgId = imgId;
    let modal = document.getElementById("lc-photo-picker-modal");
    if (!modal) {
      modal = document.createElement("div");
      modal.id = "lc-photo-picker-modal";
      modal.className = "fixed inset-0 z-[230] bg-black/85 backdrop-blur-md hidden items-center justify-center p-3";
      document.body.appendChild(modal);
    }
    const pool = ((window.DATA && DATA.ready_photos) ? DATA.ready_photos : [])
      .filter(p => !p.includes("ai_v") && !p.includes("ingr_") && !p.includes("yorg_"));
    modal.innerHTML =
      '<div class="bg-[#FDF8F2] rounded-3xl max-w-5xl w-full max-h-[88vh] flex flex-col overflow-hidden border-4 border-[#D48238]">' +
        '<div class="p-4 bg-[#2E3D28] text-white flex items-center justify-between">' +
          '<h3 class="font-serif text-xl font-bold">📸 Замена фото (' + pool.length + ' кадров)</h3>' +
          '<button type="button" onclick="document.getElementById(\'lc-photo-picker-modal\').classList.add(\'hidden\')" class="w-8 h-8 rounded-full bg-white/15 font-bold cursor-pointer">✕</button>' +
        '</div>' +
        '<div class="p-3 bg-[#F6E4CE] flex flex-wrap gap-2 text-xs">' +
          '<input id="lc-url-inp" type="text" value="' + escHtml(im.getAttribute("src") || "") + '" class="flex-1 min-w-[200px] px-3 py-1.5 rounded-xl bg-white border text-stone-900 font-bold">' +
          '<button type="button" onclick="window.lcApplyChosenPhoto(document.getElementById(\'lc-url-inp\').value)" class="px-3.5 py-1.5 rounded-xl bg-emerald-700 text-white font-extrabold cursor-pointer">✅ Применить URL</button>' +
          '<label class="px-3.5 py-1.5 rounded-xl bg-[#D48238] text-white font-extrabold cursor-pointer">📁 С ПК<input type="file" accept="image/*" class="hidden" onchange="window.lcUploadPcPhoto(event)"></label>' +
        '</div>' +
        '<div class="p-4 overflow-y-auto grid grid-cols-2 sm:grid-cols-5 gap-2.5 max-h-[64vh] custom-scroll">' +
          pool.map(ph =>
            '<div class="bg-white rounded-xl p-1.5 border flex flex-col gap-1">' +
              '<div class="h-24 rounded-lg overflow-hidden bg-stone-100"><img src="' + escHtml(ph) + '" loading="lazy" class="w-full h-full object-cover"></div>' +
              '<button type="button" onclick="window.lcApplyChosenPhoto(\'' + escHtml(ph) + '\')" class="w-full py-1 rounded-lg bg-emerald-700 text-white text-[10px] font-extrabold cursor-pointer">✅ Применить</button>' +
            '</div>'
          ).join("") +
        '</div>' +
      '</div>';
    modal.classList.remove("hidden");
    modal.classList.add("flex");
  };

  window.lcApplyChosenPhoto = function(newSrc) {
    newSrc = (newSrc || "").trim();
    if (!newSrc || !window.lcTargetImgEl) return;
    window.lcTargetImgEl.setAttribute("src", newSrc);
    const bg = window.lcTargetImgEl.parentElement
      ? window.lcTargetImgEl.parentElement.querySelector(".mirmir-nocrop-bg")
      : null;
    if (bg) bg.style.backgroundImage = 'url("' + newSrc + '")';
    window.lcState.images[window.lcTargetImgId] = window.lcState.images[window.lcTargetImgId] || { tx: 0, ty: 0, scale: 100 };
    window.lcState.images[window.lcTargetImgId].src = newSrc;
    saveState(window.lcState);
    const m = document.getElementById("lc-photo-picker-modal");
    if (m) { m.classList.add("hidden"); m.classList.remove("flex"); }
    if (typeof showToast === "function") showToast("✅ Фото применено!");
  };

  window.lcUploadPcPhoto = function(ev) {
    const f = ev.target.files && ev.target.files[0];
    if (!f) return;
    const rd = new FileReader();
    rd.onload = e => window.lcApplyChosenPhoto(e.target.result);
    rd.readAsDataURL(f);
  };

  window.lcStepSiteWidth = function(delta) {
    window.lcState.siteWidth = Math.max(1120, Math.min(1760, (window.lcState.siteWidth || DEFAULT_SITE_WIDTH) + delta));
    saveState(window.lcState);
    injectStyles();
    const l = document.getElementById("lc-site-width-lbl");
    if (l) l.textContent = window.lcState.siteWidth + " px";
  };

  window.lcToggleCoverMode = function() {
    window.lcState.coverMode = !window.lcState.coverMode;
    saveState(window.lcState);
    injectStyles();
    window.renderLcFloatingControls();
  };

  window.lcResetAll = function() {
    if (!confirm("Сбросить все настройки Конструктора к заводским (1320px)?")) return;
    localStorage.removeItem(LS_STATE_KEY);
    location.reload();
  };

  window.toggleLcMode = function(forceVal) {
    window.lcActive = forceVal !== undefined ? Boolean(forceVal) : !window.lcActive;
    if (window.lcActive && !window.isLcEnabledInHub()) window.setLcEnabledInHub(true);
    document.body.classList.toggle("lc-mode-on", window.lcActive);
    window.decoratePageForConstructor();
    window.applyAllSavedConstructorStates();
    window.renderLcFloatingControls();
  };

  window.renderLcFloatingControls = function() {
    let fab = document.getElementById("lc-main-toggle-fab");
    if (!fab) {
      fab = document.createElement("div");
      fab.id = "lc-main-toggle-fab";
      fab.className = "fixed bottom-4 right-4 z-[190] flex items-center gap-2";
      document.body.appendChild(fab);
    }
    if (!window.isLcEnabledInHub()) {
      fab.style.display = "none";
      fab.innerHTML = "";
      return;
    }
    fab.style.display = "flex";
    const w = window.lcState.siteWidth || DEFAULT_SITE_WIDTH;
    if (!window.lcActive) {
      fab.innerHTML =
        '<button type="button" onclick="window.toggleLcMode(true)" class="py-2.5 px-4 rounded-full bg-[#2E3D28] hover:bg-[#D48238] text-[#F2B880] hover:text-white border-2 border-[#F2B880]/70 font-extrabold text-xs shadow-2xl cursor-pointer">🎛️ Конструктор окон и фото</button>';
    } else {
      fab.innerHTML =
        '<div class="bg-[#1B2616]/95 text-white p-2.5 rounded-2xl border-2 border-[#D48238] shadow-2xl flex flex-wrap items-center gap-2 text-xs">' +
          '<button type="button" onclick="window.lcToggleCoverMode()" class="px-2.5 py-1 rounded-xl font-extrabold text-[11px] cursor-pointer ' +
            (!window.lcState.coverMode ? 'bg-teal-700 text-white' : 'bg-white/10 text-stone-200') + '">' +
            (!window.lcState.coverMode ? '🖼️ Фото: Умный фон без обрезки' : '🖼️ Фото: С обрезкой (Cover)') +
          '</button>' +
          '<div class="flex items-center gap-1 bg-white/10 px-2 py-1 rounded-xl">' +
            '<span class="text-[11px] text-stone-300">Ширина:</span>' +
            '<button type="button" onclick="window.lcStepSiteWidth(-40)" class="px-2 py-0.5 rounded bg-white/20 hover:bg-[#D48238] font-extrabold cursor-pointer">−</button>' +
            '<strong id="lc-site-width-lbl" class="font-mono text-[#F2B880] px-1">' + w + ' px</strong>' +
            '<button type="button" onclick="window.lcStepSiteWidth(40)" class="px-2 py-0.5 rounded bg-white/20 hover:bg-[#D48238] font-extrabold cursor-pointer">+</button>' +
          '</div>' +
          '<button type="button" onclick="saveState(window.lcState);window.toggleLcMode(false);if(typeof showToast===\'function\')showToast(\'✅ Изменения применены!\')" class="px-3.5 py-1.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-extrabold cursor-pointer shadow">✅ Применить</button>' +
          '<button type="button" onclick="window.lcResetAll()" class="px-2.5 py-1 rounded-xl bg-rose-800 text-white font-extrabold text-[11px] cursor-pointer">🔄 Сброс</button>' +
          '<button type="button" onclick="window.setLcEnabledInHub(false)" class="px-2 py-1 rounded-xl bg-white/10 text-stone-300 font-bold text-[11px] cursor-pointer">🔒 Выкл</button>' +
        '</div>';
    }
  };

  function hookRenders() {
    ["openMenu", "openCafeShopModal", "renderDishes", "renderRightTwoPictureFields", "renderCategoryShowcaseAndRail", "renderNewsPosts"].forEach(fn => {
      const orig = window[fn];
      if (typeof orig === "function" && !orig._lcV48) {
        const w = function() {
          const r = orig.apply(this, arguments);
          setTimeout(() => {
            if (window.lcActive) window.decoratePageForConstructor();
            window.applyAllSavedConstructorStates();
          }, 45);
          return r;
        };
        w._lcV48 = true;
        window[fn] = w;
      }
    });
  }

  function init() {
    injectStyles();
    window.renderLcFloatingControls();
    window.applyAllSavedConstructorStates();
    hookRenders();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => setTimeout(init, 160));
  } else {
    setTimeout(init, 160);
  }
})();
