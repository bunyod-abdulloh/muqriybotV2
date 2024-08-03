from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

hamsafar_list = [
    '1. Shohi Zinda (Qusam ibn Abbos roziyallohu anhuning ziyoratlari)',
    '2. Hidoyat imomi (Imom Abu Mansur Moturidiyning ziyoratlari)',
    '3. Registon majmuasi - Samarqand gavhari',
    '4. Samarqand gavhari',
    '5. Mirzo Ulug'bek madrasasida ta'lim',
    '6. Sherdor madrasasi va Tillakori masjidi',
    '7. Amir Temur maqbarasi',
    '8. Xo\'ja Ahror Valiy ziyoratgohi',
    '9. Fotih Sulton',
    '10. Imom Buxoriy xalqaro ilmiy-tadqiqot markazi',
    '11. Sulton Ahmad va Shahzoda masjidi',
    '12. Mirzo Ulug'bek rasadxonasi',
    '13. Ayo Sofiya masjidi',
    '14. Bahouddin Naqshbandiy',
    '15. Abu Ayyub al-Ansoriy masjidi',
    '16. Sayid Amir Kulol va Chor Bakr majmualari',
    '17. Imom Abu Hafs Kabir maqbarasi',
    '18. Sayfiddin Boharziy maqbarasi',
    '19. Buxoro arki',
    '20. Abdulloh Yamaniy',
    '21. Masjidi Kalon',
    '22. Shayx Alouddin maqbarasi',
    '23. Pahlavon Mahmud maqbarasi',
    '24. Juma masjidi',
    '25. Arabxon madrasasi',
    '26. Sayyid Niyoz sholikor masjid-madrasasi',
    '27. Karvonsaroy',
    '28. Muhammad Aminxon madrasasi',
    '29. Toshhovli',
    '30. Qutlug\' Murod Inoq madrasasi',
    '31. Olloqulixon madrasasi',
    '32. Ogahiy uy-muzeyi',
    '33. Ko\'hna ark',
    '34. Nurillohboy saroyi',
    '35. Islomxo\'ja me\'moriy ansambli',
    '36. Badr jangi',
    '37. Abu Talha qudug\'i',
    '38. Uhud tog\'i',
    '39. Salmon Forsiy va hurmo bog\'i',
    '40. Qubo masjidi',
    '41. <NAME>',
    '42. <NAME>'
]
def hamsafar_inline_keyboards():

    markup = InlineKeyboardMarkup(row_width=5)
    markup.add(InlineKeyboardButton(text="Hamsafar", callback_data="hamsafar"))


# 5. Mirzo Ulug'bek madrasasida ta'lim
# 6. Sherdor madrasasi va Tillakori masjidi
# 7. Amir Temur maqbarasi
# 8. Xo'ja Ahror Valiy ziyoratgohi
# 9. Fotih Sulton
# 10. Imom Buxoriy xalqaro ilmiy-tadqiqot markazi
# 11. Sulton Ahmad va Shahzoda masjidi
# 12. Mirzo Ulug'bek rasadxonasi
# 13. Ayo Sofiya masjidi
# 14. Bahouddin Naqshbandiy
# 15. Abu Ayyub al-Ansoriy masjidi
# 16. Sayid Amir Kulol va Chor Bakr majmualari
# 17. Imom Abu Hafs Kabir maqbarasi
# 18. Sayfiddin Boharziy maqbarasi
# 19. Buxoro arki
# 20. Abdulloh Yamaniy
# 21. Masjidi Kalon
# 22. Shayx Alouddin maqbarasi
# 23. Pahlavon Mahmud maqbarasi
# 24. Juma masjidi
# 25. Arabxon madrasasi
# 26. Sayyid Niyoz Sholikor masjid-madrasasi
# 27. Karvonsaroy
# 28. Muhammad Aminxon madrasasi
# 29. Toshhovli
# 30. Qutlug' Murod Inoq madrasasi
# 31. Olloqulixon madrasasi
# 32. Ogahiy uy-muzeyi
# 33. Ko'hna ark
# 34. Nurillohboy saroyi
# 35. Islomxo\'ja me\'moriy ansambli
# 36. Badr jangi
# 37. Abu Talha qudug\'i
# 38. Uhud tog\'i
# 39. Salmon Forsiy va hurmo bog\'i
# 40. Qubo masjidi