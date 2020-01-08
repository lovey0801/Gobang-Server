def in_list(src, *var_list):
    for item in var_list:
        if item not in src:
            return False

    return True


def five(play_history, index, count=0):
    if index in play_history:
        count = count + 1
    else:
        count = 0
    return count

