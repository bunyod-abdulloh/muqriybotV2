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
    javob = ('Assalomu alaykum!\n\nFaqat botga oid savol va takliflarga javob beramiz!\n\nDinimiz borasida '
             'savollaringiz bo\'lsa quyidagi manbalardan foydalanishingiz mumkin:\n\nhttp://savollar.islom.uz/'
             '\n\nhttp://savollar.muslim.uz\n\nhttp://www.savollar.muslimaat.uz'
             '\n\nHasanxon qori akaga savollaringiz bo\'lsa facebookdagi \nhttps://www.facebook.com/Muqriy.Hasan '
             'sahifalariga yuborishingiz yoki haftaning juma kunlari quyidagi manzilda Juma namozidan keyin qabullariga '
             'borishingiz mumkin:'
             '\nhttps://yandex.com/navi/org/200830407398')
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
