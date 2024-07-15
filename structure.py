def trans(row: list, col: list, r, c, player: str):
    row[int(r)][int(c)] = player
    col[int(c)][int(r)] = player
    return row, col


def sublist_to_list(sublist: list):
    new_list = []
    for i in sublist:
        new_list.append("".join(i))
    return new_list


def change(player: str):
    if player == "X":
        return "O"
    return "X"


def check_dia(as_list):
    l_to_r = ""
    r_to_l = ""
    l = 0
    r = len(as_list) - 1
    for i in as_list:
        l_to_r += i[l]
        r_to_l += i[r]
        l += 1
        r -= 1
    l_to_r = list(set(l_to_r))
    r_to_l = list(set(r_to_l))
    return l_to_r, r_to_l


def check_winner(row: list, col: list):
    row = sublist_to_list(row)
    col = sublist_to_list(col)
    all_list = row + col
    if "XXX" in all_list or "OOO" in all_list:
        return True
    else:
        l_to_r_row, r_to_l_rpw = check_dia(row)
        l_to_r_col, r_to_l_col = check_dia(col)
        check_list = [l_to_r_row, r_to_l_rpw, l_to_r_col, r_to_l_col]
        if ["X"] in check_list or ["O"] in check_list:
            return True
        return False
