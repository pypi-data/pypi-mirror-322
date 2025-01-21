#  hasnainkk - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of hasnainkk.
#
#  hasnainkk is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  hasnainkk is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with hasnainkk.  If not, see <http://www.gnu.org/licenses/>.

from uuid import uuid4

import hasnainkk
from hasnainkk import types
from ..object import Object


class InlineQueryResult(Object):
    """One result of an inline query.

    - :obj:`~hasnainkk.types.InlineQueryResultCachedAudio`
    - :obj:`~hasnainkk.types.InlineQueryResultCachedDocument`
    - :obj:`~hasnainkk.types.InlineQueryResultCachedAnimation`
    - :obj:`~hasnainkk.types.InlineQueryResultCachedPhoto`
    - :obj:`~hasnainkk.types.InlineQueryResultCachedSticker`
    - :obj:`~hasnainkk.types.InlineQueryResultCachedVideo`
    - :obj:`~hasnainkk.types.InlineQueryResultCachedVoice`
    - :obj:`~hasnainkk.types.InlineQueryResultArticle`
    - :obj:`~hasnainkk.types.InlineQueryResultAudio`
    - :obj:`~hasnainkk.types.InlineQueryResultContact`
    - :obj:`~hasnainkk.types.InlineQueryResultDocument`
    - :obj:`~hasnainkk.types.InlineQueryResultAnimation`
    - :obj:`~hasnainkk.types.InlineQueryResultLocation`
    - :obj:`~hasnainkk.types.InlineQueryResultPhoto`
    - :obj:`~hasnainkk.types.InlineQueryResultVenue`
    - :obj:`~hasnainkk.types.InlineQueryResultVideo`
    - :obj:`~hasnainkk.types.InlineQueryResultVoice`
    """

    def __init__(
        self,
        type: str,
        id: str,
        input_message_content: "types.InputMessageContent",
        reply_markup: "types.InlineKeyboardMarkup"
    ):
        super().__init__()

        self.type = type
        self.id = str(uuid4()) if id is None else str(id)
        self.input_message_content = input_message_content
        self.reply_markup = reply_markup

    async def write(self, client: "hasnainkk.Client"):
        pass
