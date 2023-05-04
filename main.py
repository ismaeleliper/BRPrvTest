import random


class Player:
    def __init__(self,
                 profile: str,
                 player_data: dict,
                 property_data: dict):
        self.profile = profile
        self.player_data = player_data
        self.property_data = property_data

    def action_buy(self):
        if self.profile == "impulsivo":
            return True

        if self.profile == "exigente":
            if self.property_data["rent_price"] > 50:
                return True

        if self.profile == "cauteloso":
            if (self.player_data["balance"] - self.property_data["sale_price"]) >= 80:
                return True

        if self.profile == "aleatorio":
            prob_percetange = 100 * (1 / 2)  # comprar = 1 || não comprar = 1 / sum(comprar + não comprar)
            if prob_percetange == 50.0:
                return True

        return False


def play():
    board = [
        "START",
        {
            "sale_price": 200,
            "rent_price": 95,
            "owner": None
        },
        {
            "sale_price": 180,
            "rent_price": 12,
            "owner": None
        },
        {
            "sale_price": 400,
            "rent_price": 35,
            "owner": None
        },
        {
            "sale_price": 1000,
            "rent_price": 250,
            "owner": None
        },
        {
            "sale_price": 700,
            "rent_price": 59,
            "owner": None
        },
        {
            "sale_price": 850,
            "rent_price": 60,
            "owner": None
        },
        {
            "sale_price": 950,
            "rent_price": 78,
            "owner": None
        },
        {
            "sale_price": 620,
            "rent_price": 45,
            "owner": None
        },
        {
            "sale_price": 500,
            "rent_price": 97,
            "owner": None
        },
        {
            "sale_price": 1100,
            "rent_price": 100,
            "owner": None
        },
        {
            "sale_price": 690,
            "rent_price": 44,
            "owner": None
        },
        {
            "sale_price": 350,
            "rent_price": 13,
            "owner": None
        },
        {
            "sale_price": 1480,
            "rent_price": 600,
            "owner": None
        },
        {
            "sale_price": 200,
            "rent_price": 120,
            "owner": None
        },
        {
            "sale_price": 170,
            "rent_price": 11,
            "owner": None
        },
        {
            "sale_price": 111,
            "rent_price": 90,
            "owner": None
        },
        {
            "sale_price": 850,
            "rent_price": 90,
            "owner": None
        },
        {
            "sale_price": 788,
            "rent_price": 55,
            "owner": None
        },
        {
            "sale_price": 320,
            "rent_price": 58,
            "owner": None
        },
        {
            "sale_price": 100,
            "rent_price": 10,
            "owner": None
        }
    ]

    players = [
        {"Player": "impulsivo", "balance": 300, "last_position": 0, "turn_around": 0},
        {"Player": "cauteloso", "balance": 300, "last_position": 0, "turn_around": 0},
        {"Player": "aleatorio", "balance": 300, "last_position": 0, "turn_around": 0},
        {"Player": "exigente", "balance": 300, "last_position": 0, "turn_around": 0},
    ]

    timeout = 0

    wins_by_player_profile = {
        "impulsivo": 0,
        "exigente": 0,
        "cauteloso": 0,
        "aleatorio": 0
    }

    players_var = players
    random.shuffle(players_var)  # random sequence

    router = 1

    while len(players_var) > 1 or router >= 1000:
        router += 1

        if router > 1000:
            timeout += 1

            players_sorted = sorted(players_var, key=lambda d: d["balance"], reverse=True)
            balance = players_sorted[0]["balance"]
            list_of_final_players = []
            for i in players_var:
                if i["balance"] == balance:
                    list_of_final_players.append(i)

            if len(list_of_final_players) > 1:
                list_of_final_players_sorted = sorted(list_of_final_players, key=lambda d: d["turn_around"],
                                                      reverse=True)

            champ = list_of_final_players_sorted[0]
            wins_by_player_profile[champ["Player"]] = wins_by_player_profile[champ["Player"]] + 1

        for i in players_var:
            value_of_dice_returned = random.randint(1, 6)

            if i["last_position"] == 0:
                i["last_position"] = value_of_dice_returned

            else:
                sum_of_places_to_walk = i["last_position"] + value_of_dice_returned

                if sum_of_places_to_walk > 20:
                    i["last_position"] = sum_of_places_to_walk - 20
                    i["balance"] = i["balance"] + 100
                    i["turn_around"] = i["turn_around"] + 1

                else:
                    i["last_position"] = sum_of_places_to_walk

            if not board[value_of_dice_returned]["owner"]:
                player = Player(profile=i["Player"],
                                player_data=i,
                                property_data=board[value_of_dice_returned]).action_buy()
                if player:
                    board[value_of_dice_returned]["owner"] = i["Player"]
                    i["balance"] = i["balance"] - board[value_of_dice_returned]["sale_price"]
                    if i["balance"] <= 0:
                        for it in board:
                            if type(it) == dict:
                                if it["owner"] == i["Player"]:
                                    it["owner"] = None

                        players_var.remove(i)

            else:
                i["balance"] = i["balance"] - board[value_of_dice_returned]["rent_price"]
                if i["balance"] <= 0:
                    for it in board:
                        if type(it) == dict:
                            if it["owner"] == i["Player"]:
                                it["owner"] = None
                    players_var.remove(i)

    if len(players) == 1:
        profile = players_var[0]["Player"]
        wins_by_player_profile[profile] = wins_by_player_profile[profile] + 1

    how_many_rounds_end = router

    return timeout, how_many_rounds_end, sorted(wins_by_player_profile)


if __name__ == '__main__':
    timeout_total = 0
    turns_around_to_end_total = 0
    win_total_by_profile = {
        "impulsivo": 0,
        "exigente": 0,
        "cauteloso": 0,
        "aleatorio": 0
    }
    winner_profile = None

    for i in range(30):
        each_play = play()
        timeout_total += each_play[0]
        turns_around_to_end_total += each_play[1]
        win_total_by_profile[each_play[2][0]] += 1

    print(f"How many games end by timeout: -> {timeout_total}")
    print(f"Avarage of turn around by game: -> {(turns_around_to_end_total/300)}")
    print(f"""\n
    Wins percentage of each player: \n
        impulsivo: {win_total_by_profile["impulsivo"]/300}%\n
        exigente: {win_total_by_profile["exigente"]/300}%\n
        cauteloso: {win_total_by_profile["cauteloso"]/300}%\n
        aleatorio: {win_total_by_profile["aleatorio"]/300}%\n
    """)
    print(f"The winner is {sorted(win_total_by_profile)[0]}")