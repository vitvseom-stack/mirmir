# -*- coding: utf-8 -*-
"""
ЭТАЛОННАЯ БАЗА ДАННЫХ КАФЕ «МИР МИР» (menu_data.py)
Содержит все 63 позиции зала с парными порциями (S/L), сезонные спешлы от Шефа и витрину Магазина кафе.
"""

MENU_DATABASE = [
    # --- СЕЗОННЫЕ СПЕШЛЫ ОТ ШЕФА (9 позиций) ---
    {
        "id": "sp_1",
        "category": "Сезонные спешлы от Шефа",
        "name": "Салат «Тропикал Кубана»",
        "weight": "280 г",
        "price": 440,
        "photo": "img/vk_5128_1.jpg",
        "photo_type": "real",
        "desc": "Свежий тропический салат с ананасом, спелым авокадо, миксом зелени и цитрусовой заправкой.",
        "ai_prompt": "Fresh tropical vegan salad with pineapple, avocado, cherry tomatoes, mixed greens and citrus dressing"
    },
    {
        "id": "sp_2",
        "category": "Сезонные спешлы от Шефа",
        "name": "Карибский плов «Арос кон каморонос»",
        "weight": "350 г",
        "price": 460,
        "photo": "img/vk_5122_1.jpg",
        "photo_type": "real",
        "desc": "Ароматный карибский жёлтый рис с овощами, нутом, специями и травами.",
        "ai_prompt": "Aromatic Caribbean spiced yellow rice pilaf with vegetables, chickpeas and herbs"
    },
    {
        "id": "sp_3",
        "category": "Сезонные спешлы от Шефа",
        "name": "Ямайские пирожки «Патти мит»",
        "weight": "240 г",
        "price": 380,
        "photo": "img/vk_5121_0.jpg",
        "photo_type": "real",
        "desc": "Золотистые запечённые ямайские пирожки с пряной растительной начинкой.",
        "ai_prompt": "Golden baked Jamaican turnovers patties with savory spiced filling on wooden board"
    },
    {
        "id": "sp_4",
        "category": "Сезонные спешлы от Шефа",
        "name": "Кубинская пицца «Революция»",
        "weight": "420 г",
        "price": 590,
        "photo": "img/vk_5118_0.jpg",
        "photo_type": "real",
        "desc": "Ремесленная пицца на тонком тесте с запечёнными овощами и веганским сыром.",
        "ai_prompt": "Artisan thin-crust vegan pizza with roasted vegetables, plant-based cheese and herbs"
    },
    {
        "id": "sp_5",
        "category": "Сезонные спешлы от Шефа",
        "name": "Сэндвич «Елена Руз» с вешенками и дайкири",
        "weight": "320 г",
        "price": 450,
        "photo": "img/vk_5118_1.jpg",
        "photo_type": "real",
        "desc": "Объёмный поджаристый сэндвич с карамелизированными вешенками, луком и зеленью.",
        "ai_prompt": "Toasted gourmet artisan sandwich with roasted oyster mushrooms, caramelized onions and greens"
    },
    {
        "id": "sp_6",
        "category": "Сезонные спешлы от Шефа",
        "name": "«Раста-паста» с печеными джерками",
        "weight": "340 г",
        "price": 450,
        "photo": "img/vk_5118_2.jpg",
        "photo_type": "real",
        "desc": "Яркая паста со сладким перцем, полосками пряного соевого джерки и кокосовым соусом.",
        "ai_prompt": "Colorful Rasta pasta with bell peppers, jerk-spiced soy jerky strips and creamy coconut sauce"
    },
    {
        "id": "sp_7",
        "category": "Сезонные спешлы от Шефа",
        "name": "Пицца «Том Ям» с лисичками и эдамаме",
        "weight": "450 г",
        "price": 620,
        "photo": "img/vk_5085_1.jpg",
        "photo_type": "real",
        "desc": "Авторская пицца с соусом Том Ям, лисичками, соевыми бобами эдамаме и тофу.",
        "ai_prompt": "Artisan whole-wheat pizza with chanterelle mushrooms, edamame beans, tofu and tom yum sauce"
    },
    {
        "id": "sp_8",
        "category": "Сезонные спешлы от Шефа",
        "name": "Завертон «Роти Ныа» с сейтаном и битым огурцом",
        "weight": "290 г",
        "price": 430,
        "photo": "img/vk_5094_1.jpg",
        "photo_type": "real",
        "desc": "Тёплый тайский пшеничный блинчик роти с пряным сейтаном и хрустящим битым огурцом.",
        "ai_prompt": "Warm flaky Thai roti flatbread wrap filled with spiced seitan strips and smashed cucumbers"
    },
    {
        "id": "sp_9",
        "category": "Сезонные спешлы от Шефа",
        "name": "Пад Тай (рисовая лапша с тофу и сейтаном)",
        "weight": "360 г",
        "price": 490,
        "photo": "img/vk_5094_0.jpg",
        "photo_type": "real",
        "desc": "Традиционная рисовая лапша во wok-соусе с золотистым тофу, сейтаном, арахисом и лаймом.",
        "ai_prompt": "Authentic Pad Thai rice noodles stir-fried with golden tofu, seitan, peanuts, lime and bean sprouts"
    },

    # --- СУПЫ (7 позиций) ---
    {
        "id": "m_1",
        "category": "Супы",
        "name": "Суп дня",
        "weight": "300 мл",
        "price": 320,
        "photo": "img/vk_5057_1.jpg",
        "photo_type": "real",
        "desc": "Сытный домашний овощной суп с ароматными специями и зеленью.",
        "ai_prompt": "Hearty homemade vegetable soup with herbs and artisan bread in a ceramic bowl"
    },
    {
        "id": "m_2",
        "category": "Супы",
        "name": "Суп выходного дня",
        "weight": "300 мл",
        "price": 350,
        "photo": "img/macro_mushrooms_raw.jpg",
        "photo_type": "ai_ingr",
        "desc": "Особый суп шеф-повара по секретному рецепту выходного дня.",
        "ai_prompt": "Rich aromatic mushroom and vegetable soup with fresh herbs in a stoneware bowl"
    },
    {
        "id": "m_3",
        "category": "Супы",
        "name": "Том Ям",
        "weight": "350 мл",
        "price": 480,
        "photo": "img/macro_tomyum_bowl.jpg",
        "photo_type": "ai_ingr",
        "desc": "Пряный тайский суп на кокосовом молоке с лемонграссом, вешенками, тофу и томатами черри.",
        "ai_prompt": "Spicy Thai Tom Yum soup in coconut broth with mushrooms, tofu, cherry tomatoes and lime"
    },
    {
        "id": "m_4",
        "category": "Супы",
        "name": "Крем-суп из зелёного горошка и авокадо",
        "weight": "300 мл",
        "price": 390,
        "photo": "img/vk_5057_1.jpg",
        "photo_type": "real",
        "desc": "Бархатный крем-суп из нежного зеленого горошка и спелого авокадо с тыквенными семечками.",
        "ai_prompt": "Velvety emerald green pea and avocado cream soup topped with microgreens and pumpkin seeds"
    },
    {
        "id": "m_5",
        "category": "Супы",
        "name": "Мисо-суп",
        "weight": "250 мл",
        "price": 280,
        "photo": "img/macro_miso_tofu.jpg",
        "photo_type": "ai_ingr",
        "desc": "Классический японский мисо-суп с кубиками шелкового тофу, водорослями вакаме и кунжутом.",
        "ai_prompt": "Traditional Japanese Miso soup with silken tofu cubes, wakame seaweed and sesame seeds"
    },
    {
        "id": "m_6",
        "category": "Супы",
        "name": "Ватапа",
        "weight": "320 мл",
        "price": 420,
        "photo": "img/vk_5053_0.jpg",
        "photo_type": "real",
        "desc": "Питательный бразильский суп на кокосовом молоке с нотками арахиса и водорослей нори.",
        "ai_prompt": "Creamy Brazilian Vatapa soup with coconut milk, nori seaweed, peanuts and spices"
    },
    {
        "id": "m_7",
        "category": "Супы",
        "name": "Дополнительно к супу: Крафтовый хлеб / Рис",
        "weight": "45 г",
        "price": 60,
        "photo": "img/vk_5121_0.jpg",
        "photo_type": "real",
        "desc": "Порция свежего бездрожжевого хлеба на закваске или рассыпчатого риса к вашему супу.",
        "ai_prompt": "Freshly baked artisan dark sourdough bread slices and a small ceramic bowl of fluffy steamed white rice"
    },

    # --- БОУЛЫ И ОМЛЕТЫ (5 позиций) ---
    {
        "id": "m_8",
        "category": "Боулы и Омлеты",
        "name": "Боул (Сытная тарелка-конструктор)",
        "sizes": [{"label": "Полбоул 225 г", "price": 350}, {"label": "Большой Боул 450 г", "price": 540}],
        "photo": "img/macro_avocado_greens.jpg",
        "photo_type": "ai_ingr",
        "desc": "Сытный конструктор: злаковая основа, запечённые овощи, протеин на выбор, салат и авторский соус.",
        "ai_prompt": "Colorful nourishing vegan buddha bowl with quinoa, roasted vegetables, falafel, avocado and tahini dressing"
    },
    {
        "id": "m_9",
        "category": "Боулы и Омлеты",
        "name": "Омлет из тофу (3 вкуса на выбор)",
        "weight": "260 г",
        "price": 410,
        "photo": "img/vk_5087_1.jpg",
        "photo_type": "real",
        "desc": "Нежный омлет из нутовой муки и тофу с овощами и зеленью. 3 вкуса на выбор.",
        "ai_prompt": "Fluffy golden chickpea and tofu omelet with cherry tomatoes, spinach and melted vegan cheese"
    },
    {
        "id": "m_10",
        "category": "Боулы и Омлеты",
        "name": "Шакшука",
        "weight": "280 г",
        "price": 420,
        "photo": "img/vk_5055_0.jpg",
        "photo_type: ": "real",
        "desc": "Пряная ближневосточная шакшука с тофу-скрэмблом в насыщенном томатном соусе с перцем.",
        "ai_prompt": "Middle eastern Shakshuka with tofu scramble in rich spiced tomato and bell pepper sauce in cast iron skillet"
    },
    {
        "id": "m_11",
        "category": "Боулы и Омлеты",
        "name": "Киприда (Средиземноморский омлет)",
        "weight": "270 г",
        "price": 440,
        "photo": "img/macro_tomatoes_olives.jpg",
        "photo_type": "ai_ingr",
        "desc": "Средиземноморский омлет с маслинами, вялеными томатами, зелёным маслом и тостом.",
        "ai_prompt": "Mediterranean chickpea omelet with olives, sun-dried tomatoes, green herb oil and crusty bread"
    },
    {
        "id": "m_12",
        "category": "Боулы и Омлеты",
        "name": "Дополнительно: тост / авокадо / соус",
        "weight": "40 г",
        "price": 120,
        "photo": "img/vk_5121_0.jpg",
        "photo_type": "real",
        "desc": "Любимые добавки к вашему завтраку или обеду.",
        "ai_prompt": "Fresh avocado slices and artisan toast on a small ceramic plate"
    },

    # --- САЛАТЫ (5 позиций) ---
    {
        "id": "m_13",
        "category": "Салаты",
        "name": "Цезарь",
        "weight": "240 г",
        "price": 450,
        "photo": "img/macro_caesar_romaine.jpg",
        "photo_type": "ai_ingr",
        "desc": "Хрустящий салат романо с золотистыми крутонами, томатами черри, нори и соусом Цезарь.",
        "ai_prompt": "Classic vegan Caesar salad with crisp romaine lettuce, golden croutons, cherry tomatoes, nori and creamy dressing"
    },
    {
        "id": "m_14",
        "category": "Салаты",
        "name": "Греческий салат с льняными чипсами и авокадо",
        "weight": "270 г",
        "price": 430,
        "photo": "img/macro_greek_olives.jpg",
        "photo_type": "ai_ingr",
        "desc": "Свежие овощи, оливки каламата, тофу-фета, авокадо и хрустящие льняные чипсы.",
        "ai_prompt": "Fresh Greek salad with tomatoes, cucumbers, kalamata olives, tofu feta, avocado and flaxseed crisps"
    },
    {
        "id": "m_15",
        "category": "Салаты",
        "name": "Салат Туна",
        "weight": "250 г",
        "price": 420,
        "photo": "img/macro_tuna_chickpea.jpg",
        "photo_type": "ai_ingr",
        "desc": "Сытный салат с нутовым «тунцом», нори, пикантным огурчиком и миксом зелени.",
        "ai_prompt": "Hearty vegan Tuna salad with mashed chickpeas, nori seaweed, pickled cucumbers and mixed greens"
    },
    {
        "id": "m_16",
        "category": "Салаты",
        "name": "Сезам",
        "weight": "210 г",
        "price": 380,
        "photo": "img/macro_cacao_nuts.jpg",
        "photo_type": "ai_ingr",
        "desc": "Лёгкий витаминный салат с кунжутной заправкой, орешками и сухофруктами.",
        "ai_prompt": "Fresh vegetable salad with sun-dried apricots, pine nuts, sesame seeds and cold-pressed oil"
    },
    {
        "id": "m_17",
        "category": "Салаты",
        "name": "Пай Хуан Гуа",
        "weight": "200 г",
        "price": 340,
        "photo": "img/macro_cucumbers_sesame.jpg",
        "photo_type": "ai_ingr",
        "desc": "Азиатские битые огурцы с чесноком, кунжутным маслом, соевым соусом и древесными грибами.",
        "ai_prompt": "Chinese smashed cucumber salad with garlic, sesame oil, soy sauce, wood ear mushrooms and cilantro"
    },

    # --- ЛАПША (4 позиции) ---
    {
        "id": "m_18",
        "category": "Лапша",
        "name": "Сливочная лапша с сосисками",
        "sizes": [{"label": "Порция 280 г", "price": 420}, {"label": "Большая 420 г", "price": 580}],
        "photo": "img/macro_creamy_pasta.jpg",
        "photo_type": "ai_ingr",
        "desc": "Нежная паста феттуччине в сливочном соусе с растительными сосисками и зеленью.",
        "ai_prompt": "Creamy vegan fettuccine pasta with roasted plant-based sausage slices and fresh herbs in a ceramic bowl"
    },
    {
        "id": "m_19",
        "category": "Лапша",
        "name": "Лапша Зии Дан",
        "sizes": [{"label": "Порция 270 г", "price": 430}, {"label": "Большая 400 г", "price": 590}],
        "photo": "img/macro_rice_noodles.jpg",
        "photo_type": "ai_ingr",
        "desc": "Пряная азиатская лапша во wok-соусе с обжаренным тофу и овощами.",
        "ai_prompt": "Asian stir-fried noodles with crispy tofu, vegetables, sesame seeds and teriyaki glaze"
    },
    {
        "id": "m_20",
        "category": "Лапша",
        "name": "Лапша Туна",
        "sizes": [{"label": "Порция 290 г", "price": 440}, {"label": "Большая 430 г", "price": 610}],
        "photo": "img/macro_tomatoes_olives.jpg",
        "photo_type": "ai_ingr",
        "desc": "Паста с соусом на основе нутового тунца, каперсов и пряных трав.",
        "ai_prompt": "Savory pasta noodles with chickpea-nori vegan tuna sauce, capers and herbs"
    },
    {
        "id": "m_21",
        "category": "Лапша",
        "name": "Лапша Том Ям",
        "sizes": [{"label": "Порция 310 г", "price": 460}, {"label": "Большая 450 г", "price": 640}],
        "photo": "img/vk_5057_0.jpg",
        "photo_type": "real",
        "desc": "Острая рисовая лапша в соусе Том Ям с вешенками, тофу и кинзой.",
        "ai_prompt": "Spicy Thai Tom Yum noodle soup with mushrooms, tofu, cherry tomatoes, lime and cilantro"
    },

    # --- БУРГЕРЫ И ИЗ ПЕЧИ (9 позиций) ---
    {
        "id": "m_22",
        "category": "Бургеры и Из печи",
        "name": "Мир-Бургер",
        "weight": "320 г",
        "price": 490,
        "photo": "img/macro_vegan_burger.jpg",
        "photo_type": "ai_ingr",
        "desc": "Фирменный бургер в мягкой булочке с сочной коттой, вяленой курагой, свежими овощами и соусом.",
        "ai_prompt": "Signature gourmet vegan burger in artisan bun with plant patty, caramelized dried apricots, pickles and sauces"
    },
    {
        "id": "m_23",
        "category": "Бургеры и Из печи",
        "name": "Авокадо-Фиш",
        "weight": "300 г",
        "price": 460,
        "photo": "img/macro_avocado_burger.jpg",
        "photo_type": "ai_ingr",
        "desc": "Бургер с хрустящим тофу в нори-кляре, спелым авокадо и тартаром.",
        "ai_prompt": "Crispy nori-battered tofu fillet burger with fresh avocado slices, lettuce and tartar sauce"
    },
    {
        "id": "m_24",
        "category": "Бургеры и Из печи",
        "name": "Неряха Джо",
        "weight": "340 г",
        "price": 420,
        "photo": "img/vk_5118_1.jpg",
        "photo_type": "real",
        "desc": "Сытный бургер с рубленым соевым рагу в богатом томатном соусе и маринованным луком.",
        "ai_prompt": "Hearty Sloppy Joe burger with rich minced soy ragu in tomato sauce, pickled onions and greens"
    },
    {
        "id": "m_25",
        "category": "Бургеры и Из печи",
        "name": "Спайси Тамаго",
        "weight": "310 г",
        "price": 560,
        "photo": "img/macro_spicy_burger.jpg",
        "photo_type": "ai_ingr",
        "desc": "Острый бургер с омлетом тамаго, веганским сыром чеддер и соусом кимчи-майо.",
        "ai_prompt": "Japanese-style spicy burger with tamago tofu omelet, melted vegan cheese, kimchi mayo and greens"
    },
    {
        "id": "m_26",
        "category": "Бургеры и Из печи",
        "name": "Пицца Грибная (на цельнозерновом тесте)",
        "sizes": [{"label": "Маленькая 22 см", "price": 320}, {"label": "Большая 25 см", "price": 650}],
        "photo": "img/vk_5085_1.jpg",
        "photo_type": "real",
        "desc": "Пицца из печи на цельнозерновом тесте с грибами, карамелизированным луком и моцареллой.",
        "ai_prompt": "Artisan whole-grain crust pizza with roasted mushrooms, caramelized onions, vegan mozzarella and thyme"
    },
    {
        "id": "m_27",
        "category": "Бургеры и Из печи",
        "name": "Пицца Пепперони (на цельнозерновом тесте)",
        "sizes": [{"label": "Маленькая 22 см", "price": 340}, {"label": "Большая 25 см", "price": 670}],
        "photo": "img/macro_pepperoni_pizza.jpg",
        "photo_type": "ai_ingr",
        "desc": "Пицца с растительными колбасками пепперони, томатным соусом и пряными травами.",
        "ai_prompt": "Artisan whole-grain pizza with smoky vegan wheat pepperoni slices, tomato sauce and melted plant cheese"
    },
    {
        "id": "m_28",
        "category": "Бургеры и Из печи",
        "name": "Лахмаджун (25 см)",
        "weight": "330 г",
        "price": 740,
        "photo": "img/vk_5062_1.jpg",
        "photo_type": "real",
        "desc": "Армянская тонкая лепешка из печи с пряным растительным фаршем, зеленью и гранатовым соусом.",
        "ai_prompt": "Crispy Turkish Lahmacun flatbread topped with spiced plant-based minced ragu, fresh parsley, lemon and pomegranate sauce"
    },
    {
        "id": "m_29",
        "category": "Бургеры и Из печи",
        "name": "Чебурек Ван Танс",
        "weight": "210 г",
        "price": 490,
        "photo": "img/vk_4783_0.jpg",
        "photo_type": "real",
        "desc": "Золотистый хрустящий чебурек с сочной растительной начинкой и зеленью.",
        "ai_prompt": "Golden crispy baked turnover cheburek filled with juicy plant meat and herbs, served with tomato salsa"
    },
    {
        "id": "m_30",
        "category": "Бургеры и Из печи",
        "name": "Кутаб Сабзи",
        "weight": "190 г",
        "price": 550,
        "photo": "img/vk_5017_0.jpg",
        "photo_type": "real",
        "desc": "Тонкий пирожок-кутаб с обильной начинкой из горных трав, шпината и тофу-феты.",
        "ai_prompt": "Traditional thin flatbread Qutab stuffed with abundant fresh mountain herbs, spinach, cilantro and tofu"
    },

    # --- ДЕСЕРТЫ БЕЗ САХАРА (6 позиций) ---
    {
        "id": "m_31",
        "category": "Десерты без сахара",
        "name": "Сырники из тофу",
        "sizes": [{"label": "3 шт.", "price": 310}, {"label": "5 шт.", "price": 480}],
        "photo": "img/macro_syrniki_berries.jpg",
        "photo_type": "ai_ingr",
        "desc": "Нежные сырники из домашнего тофу без белого сахара, подаются с ягодным соусом.",
        "ai_prompt": "Golden pan-seared vegan tofu syrniki pancakes served with berry coulis and coconut cream"
    },
    {
        "id": "m_32",
        "category": "Десерты без сахара",
        "name": "Безглютеновая шарлотка из деревенских яблок",
        "weight": "170 г",
        "price": 330,
        "photo": "img/vk_5005_0.jpg",
        "photo_type": "real",
        "desc": "Ароматная воздушная шарлотка с яблоками и корицей без глютена и сахара.",
        "ai_prompt": "Warm gluten-free apple charlotte cake with caramelized country apples and cinnamon"
    },
    {
        "id": "m_33",
        "category": "Десерты без сахара",
        "name": "Десерт «Пика» с печеным пеканом и шоколадом",
        "weight": "150 г",
        "price": 360,
        "photo": "img/vk_5069_0.jpg",
        "photo_type": "real",
        "desc": "Изысканный шоколадный десерт с печёным пеканом, финиковой карамелью и кэробом.",
        "ai_prompt": "Decadent sugar-free chocolate pecan tart dessert with roasted pecans and date caramel"
    },
    {
        "id": "m_34",
        "category": "Десерты без сахара",
        "name": "Теплая лепешка «Роти Клуай» с бананом и ананасом",
        "weight": "210 г",
        "price": 380,
        "photo": "img/vk_5103_1.jpg",
        "photo_type": "real",
        "desc": "Хрустящий жареный тайский блинчик с карамелизированным бананом и ананасом.",
        "ai_prompt": "Warm crispy Thai roti pancake with caramelized banana, pineapple and chocolate drizzle"
    },
    {
        "id": "m_35",
        "category": "Десерты без сахара",
        "name": "Мороженое растительное",
        "weight": "120 г",
        "price": 290,
        "photo": "img/macro_vegan_icecream.jpg",
        "photo_type": "ai_ingr",
        "desc": "Домашнее кокосовое мороженое с ягодами и мятой без лактозы и сахара.",
        "ai_prompt": "Artisan scoops of plant-based coconut ice cream with berries and mint leaf"
    },
    {
        "id": "m_36",
        "category": "Десерты без сахара",
        "name": "Ремесленный батончик «Нутс» в шоколаде",
        "weight": "75 г",
        "price": 240,
        "photo": "img/vk_5069_0.jpg",
        "photo_type": "real",
        "desc": "Полезный сытный батончик ручной работы с орехами, финиками и тёмным шоколадом.",
        "ai_prompt": "Handcrafted raw vegan chocolate bar filled with date caramel, hazelnuts and peanuts"
    },

    # --- БАРНОЕ МЕНЮ: СМУЗИ И КОФЕ (14 позиций) ---
    {
        "id": "m_37",
        "category": "Барное меню: Смузи и Кофе",
        "name": "Смузи «Сникерс»",
        "weight": "350 мл",
        "price": 360,
        "photo": "img/macro_cacao_nuts.jpg",
        "photo_type": "ai_ingr",
        "desc": "Густой орехово-шоколадный смузи с арахисовой пастой, бананом и кэробом.",
        "ai_prompt": "Thick chocolate peanut butter banana smoothie in a glass topped with crushed nuts"
    },
    {
        "id": "m_38",
        "category": "Барное меню: Смузи и Кофе",
        "name": "Смузи «Клубника со сливками»",
        "weight": "350 мл",
        "price": 360,
        "photo": "img/macro_strawberry_banana.jpg",
        "photo_type": "ai_ingr",
        "desc": "Нежный кокосово-клубничный смузи с бананом без добавления сахара.",
        "ai_prompt": "Creamy pink strawberry banana coconut cream smoothie in a tall glass"
    },
    {
        "id": "m_39",
        "category": "Барное меню: Смузи и Кофе",
        "name": "Зелёный смузи",
        "weight": "350 мл",
        "price": 340,
        "photo": "img/macro_berry_smoothie.jpg",
        "photo_type": "ai_ingr",
        "desc": "Освежающий смузи со шпинатом, зелёным яблоком, бананом и семенами чиа.",
        "ai_prompt": "Vibrant green spinach banana apple smoothie with chia seeds"
    },
    {
        "id": "m_40",
        "category": "Барное меню: Смузи и Кофе",
        "name": "Ягодный смузи",
        "weight": "350 мл",
        "price": 360,
        "photo": "img/macro_berry_smoothie.jpg",
        "photo_type": "ai_ingr",
        "desc": "Витаминный микс лесных ягод, смородины, черники и растительного молока.",
        "ai_prompt": "Deep purple forest berry smoothie with blueberries, raspberries and chia seeds"
    },
    {
        "id": "m_41",
        "category": "Барное меню: Смузи и Кофе",
        "name": "Смузи «Ананасовый экспресс»",
        "weight": "350 мл",
        "price": 350,
        "photo": "img/macro_pineapple_mint.jpg",
        "photo_type": "ai_ingr",
        "desc": "Тропический коктейль с ананасом, бананом и освежающей мятой.",
        "ai_prompt": "Tropical yellow pineapple banana mint smoothie in a glass"
    },
    {
        "id": "m_42",
        "category": "Барное меню: Смузи и Кофе",
        "name": "Фреш Морковь / Яблоко",
        "sizes": [{"label": "250 мл", "price": 260}, {"label": "350 мл", "price": 340}],
        "photo": "img/macro_carrots_apples.jpg",
        "photo_type": "ai_ingr",
        "desc": "Свежевыжатый витаминный сок из отборных морковок или яблок.",
        "ai_prompt": "Freshly squeezed vibrant orange carrot apple juice in a glass"
    },
    {
        "id": "m_43",
        "category": "Барное меню: Смузи и Кофе",
        "name": "Фреш Апельсин",
        "sizes": [{"label": "250 мл", "price": 310}, {"label": "350 мл", "price": 410}],
        "photo": "img/macro_oranges_fresh.jpg",
        "photo_type": "ai_ingr",
        "desc": "Яркий апельсиновый фреш, богатый витамином C.",
        "ai_prompt": "Freshly squeezed sunny orange juice with orange slice"
    },
    {
        "id": "m_44",
        "category": "Барное меню: Смузи и Кофе",
        "name": "Фреш Грейпфрут",
        "sizes": [{"label": "250 мл", "price": 330}, {"label": "350 мл", "price": 430}],
        "photo": "img/macro_grapefruit_red.jpg",
        "photo_type": "ai_ingr",
        "desc": "Освежающий грейпфрутовый фреш с лёгкой благородной горчинкой.",
        "ai_prompt": "Freshly squeezed ruby red grapefruit juice in a glass"
    },
    {
        "id": "m_45",
        "category": "Барное меню: Смузи и Кофе",
        "name": "Американо / Капучино на растительном молоке",
        "sizes": [{"label": "Американо 200 мл", "price": 210}, {"label": "Капучино 300 мл", "price": 290}],
        "photo": "img/macro_coffee_pine.jpg",
        "photo_type": "ai_ingr",
        "desc": "Классический кофе на зерне свежей обжарки с кокосовым, миндальным или овсяным молоком.",
        "ai_prompt": "Velvety plant-milk cappuccino with latte art foam in a ceramic cup"
    },
    {
        "id": "m_46",
        "category": "Барное меню: Смузи и Кофе",
        "name": "Кедровый капучино",
        "weight": "300 мл",
        "price": 360,
        "photo": "img/macro_coffee_pine.jpg",
        "photo_type": "ai_ingr",
        "desc": "Авторский капучино на кедровом молоке с нежной пенкой и ореховым ароматом.",
        "ai_prompt": "Creamy cappuccino on pine nut milk topped with roasted pine nuts"
    },
    {
        "id": "m_47",
        "category": "Барное меню: Смузи и Кофе",
        "name": "Желудёвый кофе / Цикорий",
        "weight": "250 мл",
        "price": 220,
        "photo": "img/macro_coffee_pine.jpg",
        "photo_type": "ai_ingr",
        "desc": "Полезный горячий напиток из обжаренных желудей или алтайского цикория.",
        "ai_prompt": "Warm roasted acorn and chicory herbal coffee drink in a rustic mug"
    },
    {
        "id": "m_48",
        "category": "Барное меню: Смузи и Кофе",
        "name": "Кэроб | Какао / Чили-какао",
        "weight": "300 мл",
        "price": 280,
        "photo": "img/macro_cacao_nuts.jpg",
        "photo_type": "ai_ingr",
        "desc": "Согревающий густой напиток из натурального какао или сладкого кэроба со специями.",
        "ai_prompt": "Warm frothy carob and cacao drink with spices in a ceramic mug"
    },
    {
        "id": "m_49",
        "category": "Барное меню: Смузи и Кофе",
        "name": "Домашняя кола (с Саган Дайля и пряностями)",
        "weight": "350 мл",
        "price": 290,
        "photo": "img/macro_citrus_mint.jpg",
        "photo_type": "ai_ingr",
        "desc": "Крафтовая безалкогольная кола по рецепту кафе с травой Саган Дайля и пряными специями.",
        "ai_prompt": "Craft botanical herbal cola drink with ice, lemon slice and rosemary sprig in a glass"
    },
    {
        "id": "m_50",
        "category": "Барное меню: Смузи и Кофе",
        "name": "Цитрусовый лимонад / Малина ТГ (с улуном)",
        "weight": "350 мл",
        "price": 310,
        "photo": "img/macro_citrus_mint.jpg",
        "photo_type": "ai_ingr",
        "desc": "Освежающий лимонад с цитрусами или малиной на основе тайваньского улуна.",
        "ai_prompt": "Refreshing sparkling citrus raspberry oolong lemonade with mint and ice"
    },

    # --- ЧАЙНАЯ КАРТА (13 позиций) ---
    {
        "id": "m_51",
        "category": "Чайная карта",
        "name": "Ягодный чай",
        "sizes": [{"label": "Стакан 300 мл", "price": 260}, {"label": "Чайник 900 мл", "price": 490}],
        "photo": "img/macro_berries_mix.jpg",
        "photo_type": "ai_ingr",
        "desc": "Согревающий чай с брусникой, смородиной, мёдом и травами.",
        "ai_prompt": "Ruby red forest berry herbal tea in a transparent teapot with candle warmer"
    },
    {
        "id": "m_52",
        "category": "Чайная карта",
        "name": "Прана-чай",
        "sizes": [{"label": "Стакан 300 мл", "price": 280}, {"label": "Чайник 900 мл", "price": 520}],
        "photo": "img/macro_herbal_infusion.jpg",
        "photo_type": "ai_ingr",
        "desc": "Аюрведический пряный чай с имбирём, кардамоном и травами.",
        "ai_prompt": "Spiced Ayurvedic Prana herbal tea with ginger, lemon and herbs in a teapot"
    },
    {
        "id": "m_53",
        "category": "Чайная карта",
        "name": "Брусничный глинтвейн",
        "sizes": [{"label": "Стакан 300 мл", "price": 290}, {"label": "Чайник 900 мл", "price": 540}],
        "photo": "img/macro_oranges_fresh.jpg",
        "photo_type": "ai_ingr",
        "desc": "Безалкогольный согревающий глинтвейн на брусничном соке с гвоздикой, апельсином и корицей.",
        "ai_prompt": "Hot ruby lingonberry non-alcoholic mulled wine with cinnamon sticks, cloves and orange slices"
    },
    {
        "id": "m_54",
        "category": "Чайная карта",
        "name": "Нижегородский Иван-чай / Ассам / Сенча",
        "sizes": [{"label": "Стакан 300 мл", "price": 220}, {"label": "Чайник 900 мл", "price": 390}],
        "photo": "img/macro_herbs_tea.jpg",
        "photo_type": "ai_ingr",
        "desc": "Классический листовой чай на выбор: местный кипрейный иван-чай, индийский ассам или зелёная сенча.",
        "ai_prompt": "Traditional fermented willowherb Ivan-tea in a ceramic teapot"
    },
    {
        "id": "m_55",
        "category": "Чайная карта",
        "name": "Копчёный Иван-чай",
        "sizes": [{"label": "Стакан 300 мл", "price": 240}, {"label": "Чайник 900 мл", "price": 420}],
        "photo": "img/macro_herbal_infusion.jpg",
        "photo_type": "ai_ingr",
        "desc": "Особый дымный иван-чай с глубоким костровым ароматом.",
        "ai_prompt": "Smoky campfire-aroma fermented willowherb herbal tea in a ceramic teapot"
    },
    {
        "id": "m_56",
        "category": "Чайная карта",
        "name": "Ройбуш / Травяной сбор",
        "sizes": [{"label": "Стакан 300 мл", "price": 240}, {"label": "Чайник 900 мл", "price": 420}],
        "photo": "img/macro_herbal_infusion.jpg",
        "photo_type": "ai_ingr",
        "desc": "Мягкий южноафриканский ройбуш без кофеина или ароматный алтайский горный сбор.",
        "ai_prompt": "Warm South African red Rooibos herbal infusion in a glass teapot"
    },
    {
        "id": "m_57",
        "category": "Чайная карта",
        "name": "Гречишный чай / Матэ в калабасе",
        "sizes": [{"label": "Стакан 300 мл", "price": 250}, {"label": "Чайник 900 мл", "price": 450}],
        "photo": "img/macro_herbs_tea.jpg",
        "photo_type": "ai_ingr",
        "desc": "Полезный татарский гречишный чай с ароматом печенья или аргентинский мате в калабасе.",
        "ai_prompt": "Traditional Yerba Mate in a calabash gourd with metal bombilla straw"
    },
    {
        "id": "m_58",
        "category": "Чайная карта",
        "name": "Китайский чай: Пуэр / Да Хун Пао",
        "sizes": [{"label": "Порция 300 мл", "price": 310}, {"label": "Церемония 900 мл", "price": 590}],
        "photo": "img/vk_5122_0.jpg",
        "photo_type": "real",
        "desc": "Элитный китайский выдержанный пуэр или утёсный сильноферментированный Да Хун Пао.",
        "ai_prompt": "Authentic Chinese Gongfu tea ceremony with dark Shu Puerh tea in a clay Yixing teapot and small cups"
    },
    {
        "id": "m_59",
        "category": "Чайная карта",
        "name": "Китайский чай: Габа Улун (Тайвань)",
        "sizes": [{"label": "Порция 300 мл", "price": 340}, {"label": "Церемония 900 мл", "price": 640}],
        "photo": "img/vk_5122_0.jpg",
        "photo_type": "real",
        "desc": "Тайваньский улун с высоким содержанием гамма-аминомасляной кислоты, нотками мёда и фруктов.",
        "ai_prompt": "Taiwanese amber GABA Oolong tea in a glass gongfu teapot on a wooden tea tray"
    },
    {
        "id": "m_60",
        "category": "Чайная карта",
        "name": "Китайский чай: Те Гуань Инь / Золотые Брови",
        "sizes": [{"label": "Порция 300 мл", "price": 320}, {"label": "Церемония 900 мл", "price": 610}],
        "photo": "img/macro_herbs_tea.jpg",
        "photo_type": "ai_ingr",
        "desc": "Ароматный зелёный улун Те Гуань Инь с цветочными нотами или красный чай Цзинь Цзюнь Мэй.",
        "ai_prompt": "Fragrant jade-green Tie Guan Yin Oolong tea in a porcelain gaiwan"
    },
    {
        "id": "m_61",
        "category": "Чайная карта",
        "name": "Масала",
        "sizes": [{"label": "Стакан 300 мл", "price": 270}, {"label": "Чайник 900 мл", "price": 510}],
        "photo": "img/vk_5122_0.jpg",
        "photo_type": "real",
        "desc": "Пряный индийский чай на растительном молоке с кардамоном, имбирём и гвоздикой.",
        "ai_prompt": "Traditional Indian Masala chai tea brewed on plant milk with cardamom, cinnamon and star anise"
    },
    {
        "id": "m_62",
        "category": "Чайная карта",
        "name": "Облепиховый чай",
        "sizes": [{"label": "Стакан 300 мл", "price": 280}, {"label": "Чайник 900 мл", "price": 520}],
        "photo": "img/vk_5122_0.jpg",
        "photo_type": "real",
        "desc": "Яркий витаминный облепиховый чай с апельсином, имбирём и розмарином.",
        "ai_prompt": "Bright golden sea buckthorn berry tea with ginger and orange slices in a glass teapot"
    },
    {
        "id": "m_63",
        "category": "Чайная карта",
        "name": "Пуэр на гранатовом соке",
        "sizes": [{"label": "Стакан 300 мл", "price": 320}, {"label": "Чайник 900 мл", "price": 610}],
        "photo": "img/vk_5115_2.jpg",
        "photo_type": "real",
        "desc": "Насыщенный шу пуэр, сваренный на натуральном гранатовом соке со специями.",
        "ai_prompt": "Deep ruby ripe Shu Puerh tea brewed on rich pomegranate juice with spices in a glass teapot"
    }
]

# --- ВИТРИНА МАГАЗИНА КАФЕ (8 позиций крафта домой) ---
CAFE_SHOP_ITEMS = [
    {
        "id": "sh1",
        "name": "Классический ремесленный Тофу «Мир Мир»",
        "weight": "400 г",
        "price": 280,
        "photo": "img/vk_5087_1.jpg",
        "desc": "Нежный домашний тофу собственного производства на чистой воде. Идеален для жарки, омлетов, супов и салатов."
    },
    {
        "id": "sh2",
        "name": "Пряный печёный / Копчёный Тофу от Шефа",
        "weight": "300 г",
        "price": 340,
        "photo": "img/vk_5055_0.jpg",
        "desc": "Ароматный тофу в фирменном маринаде со специями и травами — готов к подаче и сэндвичам."
    },
    {
        "id": "sh3",
        "name": "Крафтовый бездрожжевой хлеб на закваске (буханка)",
        "weight": "550 г",
        "price": 290,
        "photo": "img/vk_5121_0.jpg",
        "desc": "Тот самый домашний ремесленный хлеб из печи «Мир Мир» с хрустящей корочкой на живой закваске."
    },
    {
        "id": "sh4",
        "name": "Домашнее Кимчи & Ферментированные овощи (банка)",
        "weight": "400 г",
        "price": 360,
        "photo": "img/vk_5128_1.jpg",
        "desc": "Живые пробиотические ферментированные овощи с имбирём и пряностями по рецепту кафе."
    },
    {
        "id": "sh5",
        "name": "Пшеничные колбаски & Сейтан ручной работы",
        "weight": "350 г",
        "price": 420,
        "photo": "img/vk_5118_0.jpg",
        "desc": "Сочный растительный белок со специями — для домашних бургеров, пиццы и пасты."
    },
    {
        "id": "sh6",
        "name": "Фирменный соус в баночке (Ореховый / Тахини / Чимичурри)",
        "weight": "200 мл",
        "price": 260,
        "photo": "img/vk_5057_1.jpg",
        "desc": "Густой авторский соус из боулов и салатов «Мир Мир» для заправки домашних блюд."
    },
    {
        "id": "sh7",
        "name": "Бокс ремесленных батончиков «Нутс» в шоколаде (5 шт.)",
        "weight": "375 г",
        "price": 1050,
        "photo": "img/vk_5069_0.jpg",
        "photo_type": "real",
        "desc": "Набор из 5 сытных батончиков ручной работы с финиковой карамелью и орехами без белого сахара."
    },
    {
        "id": "sh8",
        "name": "Коллекционный чай «Унесённые Чаем» домой (Шу Пуэр / Габа / Да Хун Пао)",
        "weight": "50 г",
        "price": 450,
        "photo": "img/vk_5122_0.jpg",
        "desc": "Отборный листовой китайский чай из нашей чайной карты для домашних чаепитий."
    }
]