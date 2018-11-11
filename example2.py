from grid import GridGui

import random

width, height = 80, 50
g = GridGui((width, height), (20, 20))
g.set_fps(30)
player = (width // 2, height // 2)
opponent = (player[0] + random.randint(-width // 3, width // 3), player[1] + random.randint(-height // 3, height // 3))
direction = random.randrange(4)
motion_counter = 0
direction_change_counter = 0
while 1:
    g.fill("white")
    g.color_square(player, "green")
    g.color_square(opponent, "black")

    # If player has caught opponent then game over
    if player == opponent:
        break

    # This section of code handles the opponent motion
    motion_counter += 1
    if motion_counter == 5:
        motion_counter = 0
        if direction == 0:
            opponent = max(opponent[0] - 1, 0), opponent[1]
        elif direction == 1:
            opponent = min(width - 1, opponent[0] + 1), opponent[1]
        elif direction == 2:
            opponent = opponent[0], max(opponent[1] - 1, 0)
        elif direction == 3:
            opponent = opponent[0], min(opponent[1] + 1, height - 1)

        # If opponent is at edge change direction
        if opponent[0] in (0, width - 1) or opponent[1] in (0, height - 1):
            direction_change_counter += 10
        direction_change_counter += 1
        if direction_change_counter > 3:
            direction_change_counter = 0
            direction = random.randrange(4)

    # This section of code moves the player
    k = g.get_currently_pressed_keys()
    if "UP" in k:
        player = player[0], max(0, player[1] - 1)
    if "DOWN" in k:
        player = player[0], min(player[1] + 1, height - 1)
    if "LEFT" in k:
        player = max(player[0] - 1, 0), player[1]
    if "RIGHT" in k:
        player = min(player[0] + 1, width - 1), player[1]
    g.tick()

# Game over, start animation
g.fill("white")
selector = 0
while 1:
    for i in range(width):
        for j in range(height):
            g.color_square((i, j), "red" if (i + j) % 2 == selector else "white")
    selector = 1 - selector
    for i in range(5):
        g.tick()
