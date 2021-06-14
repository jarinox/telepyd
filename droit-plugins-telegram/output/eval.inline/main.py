from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def keyboard(data, variables, db):
    kb = [[]]
    for i in range(1, len(data)):
        kb[0].append(InlineKeyboardButton(data[i], callback_data=data[0]+str(i)))
    db.temp["inline"] = InlineKeyboardMarkup(kb)
    return "", variables, db