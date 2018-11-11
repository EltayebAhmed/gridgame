from grid import GridGui

n = 70
g = GridGui((n, n), (30, 30))
g.set_fps(5)
initial_pos = 0
over = False
while 1:
    for pos, button in g.get_clicks():
        print(button)
        if pos == (initial_pos % n, initial_pos // n) and button == "LEFT":
            over = True

    if not over:
        g.fill("white")
        initial_pos = (initial_pos + 1) % n ** 2
        g.color_square((initial_pos % n, initial_pos // n), "green")
    else:
        g.fill("white")
    g.tick()