mock_grid = range(1,92)

player_loc = 17
bear_loc = 43

transformations = ()
player_row = (player_loc-1)//13
bear_row = (bear_loc-1)//13
player_col = //
# Determining which location is closest to the player
if bear_row != player_row:
    #Transformations is a list of all possible grid locations to move to. Any locations that aren't between 1
    # and 91 are invalid
    transformations = (bear_loc-12,bear_loc-13,bear_loc-14,bear_loc+12,bear_loc+13,bear_loc+14)
    transformations = tuple((x for x in transformations if (x > 1 and x < 91)))
    closest_loc = 100 #arbitrary large number
    if bear_row > player_row:
        for j in transformations:
            if (j - player_loc) < closest_loc:
                closest_loc = j

    if bear_row < player_row:
        for j in transformations:
            if (j - player_loc) > closest_loc:
                closest_loc = (j - player_loc) + 1

    print(closest_loc)