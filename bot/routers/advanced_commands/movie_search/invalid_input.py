from aiogram import Router
from aiogram.types import Message
from keyboards.inline.keyboards.command_kb import InlineKbForCommand
from states.movie_search import SearchMovieByTitleFSM

router = Router(name=__name__)


@router.message(SearchMovieByTitleFSM.title)
async def handle_invalid_name_of_movie(message: Message) -> None:
    """
    Обрабатывает невалидное название фильма
    :param message: Message
    :return: None
    """
    await message.reply(
        text="Пожалуйста, введите текст",
        reply_markup=InlineKbForCommand.get_kb_to_exit_command(),
    )
