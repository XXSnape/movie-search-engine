from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from api import MovieSearch
from cache.get_data import get_data_from_cache
from keyboards.inline import InlineKbForMovie as InlineMovie
from keyboards.inline.callback_factory.movie_factory import MovieBackCbData
from utils.enums.movie_data import ViewingMovieDetails
from utils.tg.router_assistants.movie import send_pictures

router = Router(name=__name__)


@router.callback_query(
    MovieBackCbData.filter(F.options == ViewingMovieDetails.MOVIE_DETAILS)
)
async def handle_detail_of_movie(
    callback: CallbackQuery, callback_data: MovieBackCbData, state: FSMContext
) -> None:
    """
    Обрабатывает детали фильма

    :param callback: CallbackQuery
    :param callback_data: MovieBackCbData
    :param state: FSMContext
    :return: None
    """
    movie = await MovieSearch.get_movie_by_id(
        movie_id=callback_data.movie_id, cache=state
    )
    await callback.message.delete()
    await callback.message.answer(
        text=movie.text,
        reply_markup=await InlineMovie.get_kb_for_movie_details(
            data_for_back=callback_data, movie=movie, cache=state
        ),
    )


@router.callback_query(MovieBackCbData.filter(F.options == ViewingMovieDetails.WATCH))
async def handle_cinemas_of_movie(
    callback: CallbackQuery, callback_data: MovieBackCbData, state: FSMContext
) -> None:
    """
    Обрабатывает доступные онлайн-кинотеатры
    :param callback: CallbackQuery
    :param callback_data: MovieBackCbData
    :param state: FSMContext
    :return: None
    """
    movie = await get_data_from_cache(str(callback_data.movie_id), cache=state)
    await callback.answer()
    await callback.message.edit_reply_markup(
        reply_markup=InlineMovie.get_kb_for_cinemas(
            data_for_back=callback_data, movie=movie
        )
    )


@router.callback_query(
    MovieBackCbData.filter(F.options == ViewingMovieDetails.PICTURES)
)
async def handle_pictures_of_movie(
    callback: CallbackQuery, callback_data: MovieBackCbData, state: FSMContext
) -> None:
    """
    Обрабатывает картинки фильма

    :param callback: CallbackQuery
    :param callback_data: MovieBackCbData
    :param state: FSMContext
    :return: None
    """
    await send_pictures(callback=callback, cache=state, callback_data=callback_data)
