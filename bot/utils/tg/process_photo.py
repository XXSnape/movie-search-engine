from logging import getLogger

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InputMediaDocument,
    InputMediaPhoto,
    Message,
)
from utils.constants.error_data import NO_PHOTO

logger = getLogger(name=__name__)


async def edit_photo(
    callback: CallbackQuery,
    text: str,
    photo: str,
    markup: InlineKeyboardMarkup,
) -> None:
    """
    Редактирует фото и текст.
    Если в предыдущем сообщении не было фото, оно удаляется и отправляется новое.
    Если фотография не валидна для отправки в телеграм, отправляется документ.
    Если произошла иная ошибка, выводится пустая фотография

    :param callback: CallbackQuery
    :param text: текст для отправки
    :param photo: фото для отправки
    :param markup: клавиатура для отправки
    :return: None
    """
    try:
        await callback.message.edit_media(
            InputMediaPhoto(media=photo, caption=text),
            reply_markup=markup,
        )
    except TelegramBadRequest as err:
        if err.message.endswith("there is no media in the message to edit"):
            message = callback.message
            await callback.message.delete()
            await send_photo(message=message, text=text, photo=photo, markup=markup)
        elif err.message.endswith("wrong type of the web page content"):
            await callback.message.edit_media(
                InputMediaDocument(media=photo, caption=text),
                reply_markup=markup,
            )
        else:
            logger.exception(err)
            await callback.message.edit_media(
                InputMediaPhoto(media=NO_PHOTO, caption=text),
                reply_markup=markup,
            )


async def send_photo(
    message: Message,
    text: str,
    photo: str,
    markup: InlineKeyboardMarkup,
) -> None:
    """
    Сразу отправляет фотографию в телеграм. В случае ошибки отправляет документ или пустую фотографию
    :param message: Message
    :param text: текст для отправки
    :param photo: фото для отправки
    :param markup: клавиатура для отправки
    :return: None
    """
    photo_data = {"photo": photo, "caption": text, "reply_markup": markup}
    try:
        await message.answer_photo(**photo_data)
    except TelegramBadRequest as err:
        if err.message.endswith("wrong file identifier/HTTP URL specified"):
            logger.exception(err)
            photo_data["photo"] = NO_PHOTO
            await message.answer_photo(**photo_data)
            return
        document_data = {"document": photo, "caption": text, "reply_markup": markup}
        try:
            await message.answer_document(**document_data)
        except TelegramBadRequest as e:
            logger.exception(e)
            photo_data["photo"] = NO_PHOTO
            await message.answer_photo(**photo_data)
