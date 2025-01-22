from typing import Callable, Dict, Any, Awaitable, Optional, Type, Union

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject, User, Chat
from tonutils.tonconnect import TonConnect
from tonutils.tonconnect.models import Account, WalletInfo, WalletApp

from .manager import ATCManager
from .tonconnect.models import ATCUser, InfoWallet, AccountWallet
from .utils.keyboards import InlineKeyboardBase, InlineKeyboard
from .utils.qrcode import QRImageProviderBase, QRUrlProviderBase, QRImageProvider
from .utils.texts import TextMessageBase, TextMessage


class AiogramTonConnectMiddleware(BaseMiddleware):
    """
    Aiogram middleware for AiogramTonConnect integration.

    :param qrcode_provider: QRImageProviderBase or QRUrlProviderBase instance.
        Available default classes:
        - QRImageProvider: Generates QR codes locally using the library and
        displays message type as 'photo' with the QR code image.
        - QRUrlProvider: Generates QR codes using a third-party API and
        displays message type as 'text' with the image as 'web_page_preview'.
    :param inline_keyboard: InlineKeyboardBase class for managing inline keyboards.
    """

    def __init__(
            self,
            tonconnect: TonConnect,
            text_message: Optional[Type[TextMessageBase]] = None,
            inline_keyboard: Optional[Type[InlineKeyboardBase]] = None,
            qrcode_provider: Optional[Union[QRImageProviderBase, QRUrlProviderBase]] = None,
    ) -> None:
        self.tonconnect = tonconnect
        self.qrcode_provider = qrcode_provider or QRImageProvider()
        self.text_message = text_message or TextMessage
        self.inline_keyboard = inline_keyboard or InlineKeyboard

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        """
        Execute middleware

        :param handler: Wrapped handler in middlewares chain
        :param event: Incoming event (Subclass of :class:`aiogram.types.base.TelegramObject`)
        :param data: Contextual data. Will be mapped to handler arguments
        :return: :class:`Any`
        """
        user: User = data.get("event_from_user")
        chat: Chat = data.get("event_chat")

        if chat and chat.type == "private" and user and not user.is_bot:
            state: FSMContext = data.get("state")
            state_data = await state.get_data()

            account_wallet = state_data.get("account_wallet")
            account_wallet = AccountWallet.from_dict(account_wallet) if account_wallet else None
            data["account_wallet"] = account_wallet

            info_wallet = state_data.get("info_wallet")
            info_wallet = InfoWallet.from_dict(info_wallet) if info_wallet else None
            data["info_wallet"] = info_wallet

            app_wallet = state_data.get("app_wallet")
            app_wallet = WalletApp.from_dict(app_wallet) if app_wallet else None
            data["app_wallet"] = app_wallet

            language_code = state_data.get("language_code")
            language_code = language_code if language_code else user.language_code
            last_transaction_boc = state_data.get("last_transaction_boc")

            atc_user = ATCUser(
                id=user.id,
                language_code=language_code,
                last_transaction_boc=last_transaction_boc,
                info_wallet=info_wallet,
                app_wallet=app_wallet,
                account_wallet=account_wallet,
            )
            data["atc_user"] = atc_user

            connector = await self.tonconnect.init_connector(user.id)
            data["connector"] = connector

            atc_manager = ATCManager(
                connector=connector,
                tonconnect=self.tonconnect,
                text_message=self.text_message(atc_user.language_code),
                inline_keyboard=self.inline_keyboard(atc_user.language_code),
                qrcode_provider=self.qrcode_provider,
                user=atc_user,
                data=data,
            )
            data["atc_manager"] = atc_manager

        return await handler(event, data)
