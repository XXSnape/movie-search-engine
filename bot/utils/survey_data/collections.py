FILMS = {
    "guy_ritchie": "Фильмы Гая Ричи",
    "best_of_soyuzmultfilm": "Золотая коллекция «Союзмультфильма»",
    "theme_ww2": "Фильмы о Великой Отечественной войне",
    "theme_worlds_end": "Лучшие фильмы про апокалипсис и конец света",
    "theme_comics": "Лучшие фильмы, основанные на комиксах",
    "theme_kids_films": "Лучшие фильмы для детей",
    "theme_love": "Фильмы про любовь и страсть",
    "theme_romantic_comedy": "Романтические комедии",
    "theme_family_comedy": "Семейные комедии",
    "about_programmers": "Фильмы и сериалы про программистов",
    "theme_school": "Фильмы про школу",
    "theme_shark": "Фильмы про акул",
    "theme_catastrophe": "Фильмы-катастрофы",
    "theme_teenagers": "Фильмы про подростков",
    "theme_space": "Фильмы про космос",
    "theme_zombie": "Фильмы про зомби",
    "theme_vampire": "Фильмы про вампиров",
    "100_greatest_movies_XXI": "100 великих фильмов XXI века",
    "top500": "500 лучших фильмов",
    "top250": "250 лучших фильмов",
    "planned-to-watch-films": "Рейтинг ожидаемых фильмов",
}

SERIALS = {
    "series_about_vampires": "Сериалы про вампиров",
    "best_mini_serial": "Лучшие сериалы мини-формата",
    "popular-series": "Популярные сериалы",
    "100_greatest_TVseries": "100 великих сериалов XXI века",
    "hbo_best": "Шедевры HBO",
    "series-top250": "250 лучших сериалов",
}

ONLINE_CINEMAS = {
    "hd-must-see": "Фильмы, которые стоит посмотреть",
    "hd-revise": "Пересматриваем любимое",
    "hd-real-story": "Фильмы по реальным событиям",
    "hd-adaptation": "Лучшие экранизации",
    "hd-family": "Смотрим всей семьей",
    "hd-blockbusters": "Блокбастеры",
    "adventure_time": "Время приключений",
    "family_comedies": "Семейные комедии",
    "ny_family": "Новый год всей семьей",
    "magicstories": "Волшебные истории",
    "top20of2023": "Топ-20 фильмов и сериалов 2023 года",
    "best2023ed": "Лучшее за 2023 год: выбор редакции",
}

AWARDS = {
    "oscars_2022": "«Оскар»-2022: лауреаты",
    "golden_globes_2022_winners": "«Золотой глобус»-2022: Победители",
    "oscar_winners_2021": "«Оскар-2021»: победители",
    "golden_globe2021_winners": "«Золотой глобус 2021»: лауреаты",
    "oscar-best-film": "Лауреаты «Оскара» за лучший фильм",
    "oscar-best-film-nominees": "Номинанты «Оскара» за лучший фильм",
    "oscar-directing": "Лауреаты «Оскара» за лучшую режиссуру",
    "oscar-writing-original-screenplay": "Лауреаты «Оскара» за лучший оригинальный сценарий",
    "oscar-visual-effects": "Лауреаты «Оскара» за лучшие визуальные эффекты",
    "oscar-music-original-score": "Лауреаты «Оскара» за лучшую музыку",
    "bafta-best-film": "Лауреаты премии BAFTA за лучший фильм",
    "cesar-best-film": "Лауреаты премии «Сезар» за лучший фильм",
    "goya-best-film": "Лауреаты премии «Гойя» за лучший фильм",
}

FEES = {
    "box-offline-audience-ussr": "СССР: Самые кассовые фильмы",
    "most-expensive": "Самые дорогие фильмы",
    "most-profitable": "Самые прибыльные фильмы",
    "box-total": "Самые кассовые фильмы в мире",
    "box-russia-dollar": "Россия: Самые кассовые фильмы",
    "box-usa-all-time": "США: Самые кассовые фильмы",
}


ALL_COLLECTIONS = {**FILMS, **SERIALS, **FEES, **AWARDS, **ONLINE_CINEMAS}

COLLECTIONS = {
    0: FILMS,
    1: SERIALS,
    2: ONLINE_CINEMAS,
    3: AWARDS,
    4: FEES,
}
