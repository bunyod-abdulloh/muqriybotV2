from typing import List

from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp


@dp.message_handler(is_media_group=True, state="*", content_types=types.ContentTypes.ANY)
async def get_media_id(message: types.Message, album: List[types.Message], state: FSMContext):
    print("salom")
    try:
        media_group = types.MediaGroup()

        for obj in album:
            file_id = obj.photo[-1].file_id if obj.photo else obj[obj.content_type].file_id
            media_group.attach(
                {"media": file_id, "type": obj.content_type, "caption": obj.caption}
            )
        print(media_group)
    except Exception as err:
        await message.answer(f"Media qo'shishda xatolik!: {err}")
        return
