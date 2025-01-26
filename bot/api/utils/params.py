MOVIE_PARAMS = {
    "selectFields": [
        "id",
        "name",
        "year",
        "shortDescription",
        "countries",
        "genres",
        "rating",
        "ageRating",
        "seriesLength",
        "movieLength",
        "watchability",
        "poster",
        "description",
        "fees",
        "budget",
        "audience",
        "slogan",
        "type",
        "premiere",
        "sequelsAndPrequels",
        "persons",
        "networks",
        "lists",
    ],  # Параметры, которые нужно вытащить из api, связанные с фильмами
    "notNullFields": [
        "name",
        "description",
    ],  # Необходимые параметры, связанные с фильмами
}

REVIEW_PARAMS = {
    "selectFields": [
        "title",
        "type",
        "review",
        "date",
        "author",
    ],  # Параметры, которые нужно вытащить из api, связанные с отзывами
    "notNullFields": ["review"],  # Необходимые параметры, связанные с отзывами
}
