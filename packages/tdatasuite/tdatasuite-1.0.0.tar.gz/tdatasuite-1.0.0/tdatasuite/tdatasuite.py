import csv
import logging
from datetime import datetime, timedelta

import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TDataSuite:

    def __init__(self, app):
        self.app = app

    async def is_joined(self, chat_id):
        async for dialog in self.app.get_dialogs():
            if dialog.chat.username == chat_id.lstrip('@'):
                return True
        try:
            await self.app.join_chat(chat_id)
            logger.info(f"Joined chat successfully: {chat_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to join chat: {chat_id}. Error: {e}")
            return False

    async def fetch_messages(self, chat_id, days=1):
        messages = []
        row_num = 1

        cutoff_date = datetime.now() - timedelta(days=days)

        async for msg in self.app.get_chat_history(chat_id):
            if msg.date < cutoff_date:
                break

            if msg.from_user and msg.text:
                messages.append({
                    'row': row_num,
                    'full_name': msg.from_user.first_name,
                    'user_id': msg.from_user.id,
                    'user_name': msg.from_user.username,
                    'message': msg.text,
                    'date': msg.date
                })
                row_num += 1
        return messages

    @staticmethod
    async def export_csv(data, chat_id, base_filename='data'):
        filename = f"{base_filename}_{chat_id}.csv"
        df = pd.DataFrame(data)
        df.to_csv(
            filename,
            index=False,
            quoting=csv.QUOTE_MINIMAL,
            escapechar='\\',
            lineterminator='\n'
        )
        logger.info(f"Exported data to file: {filename}")

    async def collect_data(self, chat_id, days=1):
        if not await self.is_joined(chat_id):
            return

        messages = await self.fetch_messages(chat_id, days)
        if messages:
            chat = await self.app.get_chat(chat_id)

            if chat.username:
                cleaned_chat_id = chat.username.lstrip('@')
            else:
                cleaned_chat_id = str(abs(chat.id))

            await self.export_csv(messages, cleaned_chat_id)
