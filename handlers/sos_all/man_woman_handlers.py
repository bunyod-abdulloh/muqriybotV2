from aiogram import types

from keyboards.default.savol_dk import savol_ck
from loader import dp, sdb
from states.sos_states import Man_Woman_State

sos_javob = ('<b><i>Савол ва таклифларингизни юборишингиз мумкин. Админларимиз тез фурсатда жавоб беришга '
             'ҳаракат қиладилар</i></b>')

sos_five = ("Сиз 5 та савол юбориб бўлдингиз!\nАввалги саволларингизга админларимиз жавоб берганларидан сўнг яна "
            "савол юборишингиз мумкин!")


@dp.message_handler(text="❓ Савол ва таклифлар", state='*')
async def sos_func(message: types.Message):
    javob = '<b><i>Фақат ботга оид савол ва таклифларга жавоб берамиз!!!' \
            '\n\nДинимиз борасида саволларингиз бўлса қуйидаги манбалардан фойдаланишингиз мумкин:</i></b>' \
            '\n\nhttp://savollar.islom.uz/\n\nhttp://savollar.muslim.uz\n\nhttp://www.savollar.muslimaat.uz' \
            '\n\n<b><i>Тугмалардан бирини танланг:</i></b>'
    await message.answer(javob, reply_markup=savol_ck, disable_web_page_preview=True)
    # await Man_Woman_State.man_woman.set()


@dp.message_handler(text='Аёллар', state='*')
async def sos_woman_(message: types.Message):
    user_questions = await sdb.select_all_womanuser(user_id=message.from_user.id)

    if len(user_questions) == 5:
        await message.answer(
            text=sos_five
        )
    else:
        await message.answer(
            text=sos_javob
        )
    await Man_Woman_State.woman_one.set()


@dp.message_handler(text='Эркаклар', state='*')
async def sos_man_(message: types.Message):
    user_questions = await sdb.select_all_manuser(user_id=message.from_user.id)

    if len(user_questions) == 5:
        await message.answer(
            text=sos_five
        )
    else:
        await message.answer(
            text=sos_javob
        )
    await Man_Woman_State.man_one.set()
