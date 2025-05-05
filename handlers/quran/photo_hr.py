# from aiogram import types
# from magic_filter import F
#
# from handlers.quran.muqriyrecitation_hr import quran_hasanxon_husaynxon_alert
# from loader import db, dp
# from utils.functions.all import extracter
#
#
# @dp.message_handler(F.text == "Qur'oni Karim (rasm)", state="*")
# async def quran_photos_rtr(message: types.Message):
#     all_photos = await db.select_quran_photos()
#
#     extract = extracter(
#         all_medias=all_photos, delimiter=16
#     )
#
#     current_page = 1
#     all_pages = len(extract)
#
#     items = extract[current_page - 1]
#
#     markup = key_returner_quran_photos(
#         items=items, current_page=current_page, all_pages=all_pages
#     )
#     await message.answer(
#         text="Sura tartib raqamini tanlang", reply_markup=markup
#     )
#
#
# @dp.callback_query_handler(F.data.startswith('prev_quranp:'))
# async def quranphoto_prev_rtr(call: types.CallbackQuery):
#     await call.answer(
#         cache_time=0
#     )
#     current_page = int(call.data.split(':')[1])
#     all_photos = await db.select_quran_photos()
#
#     extract = extracter(
#         all_medias=all_photos, delimiter=16
#     )
#
#     all_pages = len(extract)
#
#     if current_page == 1:
#         current_page = all_pages
#     else:
#         current_page -= 1
#
#     items = extract[current_page - 1]
#     markup = key_returner_quran_photos(
#         items=items, current_page=current_page, all_pages=all_pages
#     )
#     await call.message.edit_reply_markup(
#         reply_markup=markup
#     )
#
#
# @dp.callback_query_handler(F.data.startswith("next_quranp:"))
# async def quranphotos_next_rtr(call: types.CallbackQuery):
#     await call.answer(
#         cache_time=0
#     )
#     current_page = int(call.data.split(':')[1])
#     all_photos = await db.select_quran_photos()
#
#     extract = extracter(
#         all_medias=all_photos, delimiter=16
#     )
#
#     all_pages = len(extract)
#
#     if current_page == all_pages:
#         current_page = 1
#     else:
#         current_page += 1
#
#     items = extract[current_page - 1]
#
#     markup = key_returner_quran_photos(
#         items=items, current_page=current_page, all_pages=all_pages
#     )
#     await call.message.edit_reply_markup(
#         reply_markup=markup
#     )
#
#
# @dp.callback_query_handler(F.data.startswith("alert_quranp:"))
# async def husary_main_alert(call: types.CallbackQuery):
#     await quran_hasanxon_husaynxon_alert(
#         call=call
#     )
