from aiogram.fsm.context import FSMContext
from api.review_search.review_mixins import ReviewApiMixin
from api.review_search.review_processing import get_text_review
from api.utils.params import REVIEW_PARAMS
from config.settings import settings
from utils.constants.cache_keys import REVIEWS_CACHE


class ReviewSearch(ReviewApiMixin):
    @classmethod
    async def get_reviews_and_len_by_params(
        cls, cache: FSMContext, types: list[str], movie_id: int
    ) -> tuple[str, int] | None:
        """
        Делает запрос на получение отзывов.
        Записывает информацию в кэш

        :param cache: кэш с данными
        :param types: типы отзывов
        :param movie_id: id текущего фильма
        :return: текст отзыва, количество отзывов или None, если ничего не нашлось
        """
        params = {
            "page": 1,
            "limit": settings.API.NUMBER_REVIEWS,
            "type": types,
            "movieId": [movie_id],
            **REVIEW_PARAMS,
        }
        json_resp = await cls._make_request(params=params)
        if json_resp is None or cls._validate_response(json_resp) is False:
            return None
        data = [
            get_text_review(json)
            for json in json_resp["docs"]
            if len(json["review"]) < 4_000
        ][: settings.API.NUMBER_REVIEWS]
        if not data:
            return None
        await cache.update_data({REVIEWS_CACHE: data})
        return data[0], len(data)
