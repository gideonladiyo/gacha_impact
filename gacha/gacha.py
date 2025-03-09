import random
from datetime import datetime

class User:
    def __init__(self, uid, username, pity, four_star_pity, four_star_rate_on, is_rate_on):
        self.uid = uid
        self.username = username
        self.primogems = 0
        self.pity = pity
        self.four_star_pity = four_star_pity
        self.four_star_rate_on = four_star_rate_on
        self.is_rate_on = is_rate_on

class Item:
    def __init__(self, name, rarity, item_type, type, image_url):
        self.name = name
        self.rarity = rarity
        self.item_type = item_type
        self.type = type
        self.image_url = image_url

class Character(Item):
    def __init__(self, name, rarity, item_type, type, is_rate_up, image_url):
        super().__init__(name, rarity, item_type, type, image_url)
        self.is_rate_up = is_rate_up

# Probabilitas sesuai rarity
rarity_choices = ["3-star", "4-star", "5-star"]
rarity_weights = {
    "3-star": 94,
    "4-star": 5,
    "5-star": 1
}
rate_up_choices = [True, False]
rate_up_weights = [50, 50]

def item_return(arr):
    return random.choice(arr)

def reset_persentage(updated_4star, updated_5star, four_star, five_star):
    if updated_5star== 0:
        if five_star >= 70:
            rarity_weights["3-star"] += 13
            rarity_weights['5-star'] -= 13
        elif five_star >= 50:
            rarity_weights['3-star'] += 1
            rarity_weights['5-star'] -= 1

    if updated_4star == 0:
        if four_star >= 8:
            rarity_weights['3-star'] +=30
            rarity_weights['4-star'] -=30
        elif four_star >= 5:
            rarity_weights['3-star'] += 10
            rarity_weights['4-star'] -= 10

def change_persentage(user):
    # 5 star pity
    if user.pity == 70:
        rarity_weights["3-star"] -= 12
        rarity_weights["5-star"] += 12
    elif user.pity == 50:
        rarity_weights['3-star'] -= 1
        rarity_weights["5-star"] += 1

    # 4 star pity
    if user.four_star_pity == 8:
        rarity_weights['3-star'] -= 20
        rarity_weights['4-star'] += 20
    elif user.four_star_pity == 5:
        rarity_weights['3-star'] -= 10
        rarity_weights['4-star'] += 10

def determine_status(items):
    count = {
        "3-star": 0,
        "4-star": 0,
        "5-star": 0
    }

    for item in items:
        if item['rarity'] in count:
            count[item['rarity']] += 1

    if count['5-star'] >= 1:
        return "emas"
    elif count['4-star'] >= 1:
        return "ungu"
    else:
        return "biru"

# gacha system
def gacha_system(rarity, user, gacha_pool):
    user = user
    if rarity != "3-star":
        if rarity == "4-star" and user.four_star_rate_on == False:
            four_star_rateup = random.choices(rate_up_choices, weights=rate_up_weights, k=1)[0]
            if four_star_rateup:
                item = item_return([item for item in gacha_pool[rarity] if item.is_rate_up])
            else:
                item = item_return([item for item in gacha_pool[rarity] if not item.is_rate_up])
        elif rarity == "4-star" and user.four_star_rate_on == True:
            item = item_return([item for item in gacha_pool[rarity] if item.is_rate_up])
        elif rarity == "5-star" and user.is_rate_on == False:
            five_star_rateup = random.choices(rate_up_choices, weights=[value for value in rate_up_weights], k=1)[0]
            if five_star_rateup:
                item = item_return([item for item in gacha_pool[rarity] if item.is_rate_up])
            else:
                item = item_return([item for item in gacha_pool[rarity] if not item.is_rate_up])
        elif rarity == "5-star" and user.is_rate_on == True:
            item = item_return([item for item in gacha_pool[rarity] if item.is_rate_up])
    else:
        item = item_return(gacha_pool[rarity])
    return item

# 1 pull
def gacha(user, gacha_pool):
    user.four_star_pity += 1
    user.pity += 1

    change_persentage(user)
    if user.four_star_pity == 10:
        rarity = "4-star"
        item = gacha_system(rarity, user, gacha_pool)

    elif user.pity == 90:
        rarity = "5-star"
        item = gacha_system(rarity, user, gacha_pool)

    else:
        rarity = random.choices(rarity_choices, weights=[value for value in rarity_weights.values()], k=1)[0]
        item = gacha_system(rarity, user, gacha_pool)

    if item.rarity != "3-star":
        if item.rarity == "4-star":
            if item.is_rate_up:
                user.four_star_rate_on = False
            else:
                user.four_star_rate_on = True
            reset_persentage(0, user.pity, user.four_star_pity, user.pity)
            user.four_star_pity = 0
        else:
            user.four_star_pity += 1
            if item.is_rate_up:
                user.is_rate_on = False
            else:
                user.is_rate_on = True
            reset_persentage(user.four_star_pity, 0, user.four_star_pity, user.pity)
            user.pity = 0

    result = {
        "item_name": item.name,
        "rarity": rarity,
        "user_pity": user.pity,
        "user_4star_pity": user.four_star_pity,
        "image_url": item.image_url,
        "date": datetime.now(),
    }
    return result

# 10 gacha
def pull(type, user, gacha_pool):
    result = {
        "gacha_result": [],
        "current_pity": 0,
        "current_4star_pity": 0,
        "five_star_rateon": False,
        "four_star_rateon": False,
        "gacha_color": "Blue",
        "uid": user.uid
    }

    if type == "ten_pull":
        for _ in range(10):
            result["gacha_result"].append(gacha(user, gacha_pool))
    elif type == "one_pull":
        result["gacha_result"].append(gacha(user, gacha_pool))

    result["current_pity"] = user.pity
    result["current_4star_pity"] = user.four_star_pity
    result["five_star_rateon"] = user.is_rate_on
    result["four_star_rateon"] = user.four_star_rate_on
    result["gacha_color"] = determine_status(result["gacha_result"])

    return result