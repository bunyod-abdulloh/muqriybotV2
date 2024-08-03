from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

PAGE_COUNT = 15
FIRST_POST = 315
LATEST_POST = 353
MENU_POST = ["\n1. Umra safariga boruvchilar uchun maslahatlar", "\n2. Uhud tog'i",
             "\n3. Ehromga kirish va umraga niyat qilish", "\n4. Savr tog'i", "\n5. Ikki qiblali masjid",
             "\n6. Qizil tog'", "\n7. Masjidul-haromga borishdan oldin nimalarni bilish kerak?",
             "\n8. Masjidul-haromdagi joiz va nojoiz amallar", "\n9. Ehromdan chiqishning sharti",
             "\n10. Safo va Marva", "\n11. Abdulloh ibn Abbos roziyallohu anhuning masjidlari", "\n12. Azaq qudug'i",
             "\n13. Juma masjidi", "\n14. Ka'b ibn Ashraf qasri", "\n15. Ijoba masjidi", "\n16. Sajda masjidi",
             "\n17. Banu So'ida saqifasi", "\n18. Rahmat tog'i", "\n19. Zubaydaxonim qudug'i", "\n20. Mino vodiysi",
             "\n21. Salmon Forsiy qudug'i", "\n22. Hazrat Usmon qudug'i",
             "\n23. Rasululloh sollallohu alayhi vasallam tavallud topgan uy", "\n24. Hiro g'ori | Tavsiyalar",
             "\n25. G'omama masjidi", "\n26. Qubo masjidi", "\n27. Salmon Forsiy va hurmo bog'i", "\n28. Uhud tog'i",
             "\n29. Abu Talha qudug'i", "\n30. Badr jangi", "\n31. Hiro g'ori | Ilk vahiy nozil bo'lishi haqida",
             "\n32. Masjidun Nabaviy odoblari", "\n33. Janoza namozi", "\n34. Aris qudug'i",
             "\n35. Abdulloh ibn Ravoha", "\n36. Mo'ta g'azoti | Ja'far ibn abu Tolib", "\n37. Zayd ibn Horisa",
             "\n38. Kahf sohiblari | 1 - qism", "\n39. Kahf sohiblari | 2 - qism"]

# POST_ID = [315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335,
#            336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353]
#
# DECENT_NUMBER = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18',
#                  '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35',
#                  '36', '37', '38', '39']

# ALL_POSTS = dict(zip(DECENT_NUMBER, POST_ID))
# print(ALL_POSTS)


LATEST_RESULT = {'1': 315, '2': 316, '3': 317, '4': 318, '5': 319, '6': 320, '7': 321, '8': 322, '9': 323, '10': 324,
                 '11': 325, '12': 326, '13': 327, '14': 328, '15': 329, '16': 330, '17': 331, '18': 332, '19': 333,
                 '20': 334, '21': 335, '22': 336, '23': 337, '24': 338, '25': 339, '26': 340, '27': 341, '28': 342,
                 '29': 343, '30': 344, '31': 345, '32': 346, '33': 347, '34': 348, '35': 349, '36': 350, '37': 351,
                 '38': 352, '39': 353}


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


async def key_returner(items, current_page, all_pages):
    keys = InlineKeyboardMarkup(
        row_width=5
    )
    for i in items:
        keys.insert(
            InlineKeyboardButton(
                text=f"{i}",
                callback_data=f"{i}"
            )
        )
    keys.row(
        InlineKeyboardButton(
            text="⬅️ Ortga",
            callback_data="-1"
        ),
        InlineKeyboardButton(
            text=f"{current_page}/{all_pages}",
            callback_data=f"alertmessage_{current_page}"
        ),
        InlineKeyboardButton(
            text="Oldinga ➡️",
            callback_data="+1"
        )
    )
    keys.add(
        InlineKeyboardButton(
            text="🎞 Barchasini YouTubeda ko'rish",
            web_app=WebAppInfo(
                url='https://www.youtube.com/playlist?list=PLys356tU5j5RVPua1DIeVh8JL0Z0RhvHi'
            )
        )
    )
    keys.add(
        InlineKeyboardButton(
            text="🏡 Bosh sahifa",
            callback_data="main_menu"
        )
    )
    return keys

qadamjolar_back_button = InlineKeyboardMarkup(row_width=1)
qadamjolar_back_button.add(
    InlineKeyboardButton(
        text="⬅️ Ortga",
        callback_data="qadamjolar_back_button"
    )
)
