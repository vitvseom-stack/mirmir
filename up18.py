# -*- coding: utf-8 -*-
"""МИКРО-АПДЕЙТЕР v18.0: ИНТЕРАКТИВНЫЙ БОУЛ + SPA HISTORY GUARD + ТОЧНЫЙ ЯНДЕКС GO"""
import os

print("=" * 60)
print("🕊️ ЗАПУСК АВТОМАТИЧЕСКОГО ИНЖЕНЕРНОГО АПДЕЙТЕРА v18.0...")
print("=" * 60)

# 1. Проверяем и правим menu_data.py (Пицца и чистые макро-картинки)
if os.path.exists("menu_data.py"):
    with open("menu_data.py", "r", encoding="utf-8") as f:
        m_code = f.read()
    m_code = m_code.replace("photo-1626700051175-6818013e1d4f", "photo-1513104890138-7c749659a591").replace("ingr_rolls_wraps.jpg", "ingr_pizza_mushrooms.jpg")
    with open("menu_data.py", "w", encoding="utf-8") as f:
        f.write(m_code)
    print("   ✅ menu_data.py: Фото пиццы и макро-ингредиенты успешно обновлены.")

# 2. Проверяем и инжектим свайп-защиту и Конструктор Боула в app.py
if os.path.exists("app.py"):
    with open("app.py", "r", encoding="utf-8") as f:
        a_code = f.read()

    # Точный прицел Яндекс Go строго на нечётную сторону (дом №45)
    a_code = a_code.replace("end-lat=56.321685&end-lon=43.990762", "end-lat=56.321475&end-lon=43.990240")
    a_code = a_code.replace("v16.0", "v18.0").replace("v17.0", "v18.0")

    BOWL_AND_GUARD_JS = r"""
// === 🛡️ ЗАЩИТА ОТ ВЫЛЕТА ПРИ СВАЙПЕ НАЗАД НА СМАРТФОНЕ (SPA HISTORY GUARD) ===
let lastBackSwipe = 0;
function pushGuard() { try { history.pushState({g:1}, ''); } catch(e){} }
window.addEventListener('load', () => { pushGuard(); pushGuard(); });
window.addEventListener('popstate', () => {
  const lb = document.getElementById('lightbox');
  if (lb && !lb.classList.contains('hidden')) { lb.classList.add('hidden'); lb.classList.remove('flex'); pushGuard(); return; }
  const bm = document.getElementById('bowl-modal');
  if (bm && !bm.classList.contains('hidden')) { bm.classList.add('hidden'); bm.classList.remove('flex'); pushGuard(); return; }
  const cm = document.getElementById('cart-modal');
  if (cm && !cm.classList.contains('hidden')) { cm.classList.add('hidden'); cm.classList.remove('flex'); pushGuard(); return; }
  const dm = document.getElementById('dev-modal');
  if (dm && !dm.classList.contains('hidden')) { dm.classList.add('hidden'); dm.classList.remove('flex'); pushGuard(); return; }
  const mm = document.getElementById('menu-modal');
  if (mm && !mm.classList.contains('hidden')) {
    if (typeof curCat !== 'undefined' && curCat !== 'Все') { curCat = 'Все'; renderTabs(); renderDishes(); pushGuard(); return; }
    closeMenu(); pushGuard(); return;
  }
  if (Date.now() - lastBackSwipe > 2200) {
    lastBackSwipe = Date.now(); pushGuard();
    const t = document.createElement('div');
    t.innerText = '🛡️ Защита от вылета! Свайпните ещё раз, если хотите выйти';
    t.className = 'fixed bottom-16 left-1/2 -translate-x-1/2 z-[90] bg-[#2E3D28] text-[#F2B880] border-2 border-[#D48238] px-4 py-2.5 rounded-2xl shadow-2xl font-extrabold text-xs whitespace-nowrap';
    document.body.appendChild(t); setTimeout(() => t.remove(), 2000);
  }
});

// === 🥗 ИНТЕРАКТИВНЫЙ КОНСТРУКТОР БОУЛА (БЛАНК №1: 225 г / 450 г) ===
let bState = { sz:0, gr:'Зелёная гречка', pr:'Тофу печёный', sc:'Ореховый', ex:{} };
const B_CFG = {
  sizes:[{n:'Большой Боул 450 г',p:540},{n:'Полбоул 225 г',p:350}],
  grains:['Зелёная гречка','Бурый рис','Киноа','Кус-кус'],
  prots:['Тофу печёный','Фалафель','Сейтан пряный','Нут томлёный'],
  sauces:['Ореховый','Тахини','Зелёный песто','Манго-чили'],
  extras:[{id:'e1',n:'Авокадо 45 г',p:120},{id:'e2',n:'Вторая основа (мал.)',p:90},{id:'e3',n:'Вторая основа (бол.)',p:120},{id:'e4',n:'Доп. соус',p:60},{id:'e5',n:'Крафт. хлеб',p:60}]
};
function openBowlBuilder() {
  pushGuard();
  let m = document.getElementById('bowl-modal');
  if (!m) {
    m = document.createElement('div'); m.id = 'bowl-modal';
    m.className = 'fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-end sm:items-center justify-center p-0 sm:p-4';
    document.body.appendChild(m);
  }
  m.classList.remove('hidden'); m.classList.add('flex');
  renderBowlUI();
}
function renderBowlUI() {
  const m = document.getElementById('bowl-modal');
  const sObj = B_CFG.sizes[bState.sz];
  let sum = sObj.p, exList = [];
  B_CFG.extras.forEach(x => { if(bState.ex[x.id]) { sum += x.p; exList.push(x.n); } });
  const btnCls = (act) => act ? 'bg-[#556432] text-white border-[#556432]' : 'bg-white text-stone-800 border-stone-200';
  m.innerHTML = `<div class="bg-[#FDF8F2] rounded-t-[2rem] sm:rounded-[2rem] max-w-xl w-full max-h-[90vh] flex flex-col justify-between overflow-hidden border-4 border-[#556432] shadow-2xl">
    <div class="p-4 bg-[#2E3D28] text-white flex justify-between items-center"><div><span class="text-[10px] uppercase text-[#F2B880] font-extrabold">Бланк №1 • Тарелка-конструктор</span><h3 class="font-serif text-2xl font-bold">🥗 Соберите свой Боул</h3></div><button onclick="document.getElementById('bowl-modal').classList.add('hidden')" class="w-8 h-8 rounded-full bg-white/15 font-bold">✕</button></div>
    <div class="p-4 overflow-y-auto space-y-4 text-xs">
      <div class="p-2.5 rounded-xl bg-emerald-900/10 text-[#2E3D28] font-semibold">✨ Уже в тарелке: Запечённые овощи • Салат коул слоу • Ферментированные овощи</div>
      <div><b class="block mb-1.5">1. Размер:</b><div class="grid grid-cols-2 gap-2">${B_CFG.sizes.map((s,i)=>`<button onclick="bState.sz=${i};renderBowlUI()" class="p-2.5 rounded-xl border font-extrabold ${btnCls(bState.sz===i)}">${s.n} — ${s.p} ₽</button>`).join('')}</div></div>
      <div><b class="block mb-1.5">2. Гарнир:</b><div class="grid grid-cols-2 sm:grid-cols-4 gap-1.5">${B_CFG.grains.map(g=>`<button onclick="bState.gr='${g}';renderBowlUI()" class="p-2.5 rounded-xl border font-bold ${btnCls(bState.gr===g)}">${g}</button>`).join('')}</div></div>
      <div><b class="block mb-1.5">3. Белковая основа:</b><div class="grid grid-cols-2 sm:grid-cols-4 gap-1.5">${B_CFG.prots.map(p=>`<button onclick="bState.pr='${p}';renderBowlUI()" class="p-2.5 rounded-xl border font-bold ${btnCls(bState.pr===p)}">${p}</button>`).join('')}</div></div>
      <div><b class="block mb-1.5">4. Авторский соус:</b><div class="grid grid-cols-2 sm:grid-cols-4 gap-1.5">${B_CFG.sauces.map(s=>`<button onclick="bState.sc='${s}';renderBowlUI()" class="p-2.5 rounded-xl border font-bold ${btnCls(bState.sc===s)}">${s}</button>`).join('')}</div></div>
      <div><b class="block mb-1.5">5. Дополнительно:</b><div class="grid grid-cols-2 gap-1.5">${B_CFG.extras.map(x=>`<button onclick="bState.ex['${x.id}']=!bState.ex['${x.id}'];renderBowlUI()" class="p-2.5 rounded-xl border font-bold flex justify-between ${btnCls(!!bState.ex[x.id])}"><span>${bState.ex[x.id]?'☑':'☐'} ${x.n}</span><b>+${x.p}₽</b></button>`).join('')}</div></div>
    </div>
    <div class="p-4 bg-[#2E3D28] text-white flex justify-between items-center"><strong class="text-xl text-[#F2B880]">${sum} ₽</strong><button onclick="saveCustomBowl(${sum})" class="px-5 py-2.5 rounded-xl bg-[#D48238] text-white font-extrabold text-xs cursor-pointer">+ Добавить Боул в заказ 🛒</button></div>
  </div>`;
}
function saveCustomBowl(sum) {
  const sObj = B_CFG.sizes[bState.sz], exList = [];
  B_CFG.extras.forEach(x => { if(bState.ex[x.id]) exList.push(x.n); });
  const title = `${sObj.n} [${bState.gr}, ${bState.pr}, соус ${bState.sc}${exList.length?', +'+exList.join(', +'):''}]`;
  cart.push({key:'bowl_'+Date.now(), idx:0, sIdx:0, name:title, price:sum, category:'Боулы и Омлеты', qty:1});
  updateCart(); document.getElementById('bowl-modal').classList.add('hidden');
}
window.addEventListener('DOMContentLoaded', () => {
  const rail = document.getElementById('sticky-rail');
  if (rail) rail.insertAdjacentHTML('afterbegin', `<button onclick="openBowlBuilder()" class="px-3.5 py-1.5 rounded-full bg-[#D48238] text-white text-xs font-extrabold whitespace-nowrap cursor-pointer shadow">🥗 Собрать Боул</button>`);
});
"""

    if "openBowlBuilder" not in a_code:
        a_code = a_code.replace("</script>\n</body>", BOWL_AND_GUARD_JS)
        with open("app.py", "w", encoding="utf-8") as f:
            f.write(a_code)
        print("   ✅ app.py: Свайп-защита и Конструктор Боула успешно вшиты.")

print("=" * 60)
print("✨ ВСЁ ГОТОВО, МИЛОРД! Запускай run.bat")
print("=" * 60)
input("Нажмите Enter для выхода...")