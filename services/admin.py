from aiogram import types

from keyboards.inline.admin import key_returner
from loader import statdb


def extracter(all_medias, delimiter):
    empty_list = []
    for e in range(0, len(all_medias), delimiter):
        empty_list.append(all_medias[e:e + delimiter])
    return empty_list


async def send_page(call: types.CallbackQuery, current_page, all_pages, extracted_data):
    text = "\n".join(
        f"{n['created_at']} | {n['chapter_name']} - {n['view_count']}" for n in extracted_data
    )

    try:
        await call.message.edit_text(
            text=text,
            reply_markup=key_returner(
                current_page=current_page,
                all_pages=all_pages
            )
        )
        await call.answer(cache_time=0)
    except Exception as err:
        await call.answer(text=f"Xatolik: {err}", show_alert=True)


async def process_page(call: types.CallbackQuery, direction: str):
    all_statistics = await statdb.get_all_statistics()

    extract = extracter(all_medias=all_statistics, delimiter=10)
    current_page = int(call.data.split(":")[1])
    all_pages = len(extract)

    if direction == "prev":
        current_page = current_page - 1 if current_page > 1 else all_pages
    elif direction == "next":
        current_page = current_page + 1 if current_page < all_pages else 1

    extracted_data = extract[current_page - 1]

    await send_page(call=call, current_page=current_page, all_pages=all_pages, extracted_data=extracted_data)
