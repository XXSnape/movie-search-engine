import datetime

from database.models import RequestModel
from database.repository.request import RequestRepository
from sqlalchemy.ext.asyncio import AsyncSession
from utils.response_formats import present_data

from .request_data import get_data_from_params


async def save_new_request(
    session: AsyncSession,
    user_id: int,
    params: dict,
    command: str,
    page: int = 1,
    index: int = 0,
) -> int:
    """
    Сохраняет в базу информацию о сделанном запросе

    :param session: сессия для работы с базой
    :param user_id: id пользователя
    :param params: параметры запроса
    :param command: выбранная команда
    :param page: номер страницы api
    :param index: индекс в кэше
    :return: int
    """
    if "page" in params:
        params.pop("page")
    return await RequestRepository.create_object(
        session=session,
        data={
            "user_tg_id": user_id,
            "params": params,
            "page": page,
            "index": index,
            "command": command,
        },
    )


async def update_request(session: AsyncSession, id: int, page: int, index: int) -> None:
    """
    Обновляет данные о запросе

    :param session: сессия для работы с базой
    :param id: id запроса
    :param page: номер страницы api
    :param index: индекс в кэше
    :return: None
    """
    await RequestRepository.update_object_by_params(
        session=session,
        filter_data={"id": id},
        update_data={
            "page": page,
            "index": index,
            "date": datetime.datetime.now(datetime.UTC),
        },
    )


async def resume_request(session: AsyncSession, request: RequestModel) -> int:
    """
    Удаляет старый запрос и делает новый
    :param session: сессия для работы с базой
    :param request: RequestModel
    :return: int
    """
    await delete_request(session=session, id=request.id)

    return await save_new_request(
        session=session,
        user_id=request.user_tg_id,
        params=request.params,
        command=request.command,
    )


async def delete_request(session: AsyncSession, id: int) -> None:
    """
    Удаляет запрос по id
    :param session: сессия для работы с базой
    :param id: id запроса
    :return: None
    """
    await RequestRepository.delete_object_by_params(session=session, data={"id": id})


async def get_requests(session: AsyncSession, user_id: int) -> list[RequestModel]:
    """
    Получает запросы по id пользователя
    :param session: сессия для работы с базой
    :param user_id: id пользователя
    :return: list[RequestModel]
    """

    all_requests = await RequestRepository.get_requests(
        session=session, data={"user_tg_id": user_id}
    )
    for request in all_requests:  # type: RequestModel
        data = present_data(get_data_from_params(request=request))
        request.text = data
    return all_requests
