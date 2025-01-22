from aiogram import Router

from . import support, create_ticket

dialog_router = Router()

dialog_router.include_routers(
    support.dialog,
    create_ticket.dialog,
)
