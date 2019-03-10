from stuctures import *


running = True

background = Background()
title = Word('uno', (100, 100), (100, 100))
undertitle = Word('space', (100, 200), (60, 60))
info = Word('press space to start the game', (0, 450), (17, 17))
run_out = False
sun = load_image('sun.png', (0, 0, 0))

planets = ['mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uran', 'neptune', 'pluto']
population = {
    'mercury': 0,
    'venus': 0,
    'earth': 0,
    'mars': 0,
    'jupiter': 0,
    'saturn': 0,
    'uran': 0,
    'neptune': 0,
    'pluto': 0
}
info_all = ['name=', 'radius=', 'T K=', 'area=']
info_planet = {
    'mercury': ['mercury', '2400km', '440', 'small'],
    'venus': ['venus', '6100km', '730', 'small'],
    'earth': ['earth', '6400km', '287', 'small'],
    'mars': ['mars', '3400km', '218', 'small'],
    'jupiter': ['jupiter', '71000km', '120', 'big'],
    'saturn': ['saturn', '60000km', '88', 'big'],
    'uran': ['uranus', '26000km', '59', 'middle'],
    'neptune': ['neptune', '25000km', '48', 'middle'],
    'pluto': ['pluto', '1187km', '40', 'very small']
}
current_pos = (0, 0)

planets_ob = []
planets_population = {
    'mercury': Life(7, 7),
    'venus': Life(10, 10),
    'earth': Life(15, 15),
    'mars': Life(12, 12),
    'jupiter': Life(40, 40),
    'saturn': Life(35, 35),
    'uran': Life(30, 30),
    'neptune': Life(25, 25),
    'pluto': Life(5, 5)
}
tooltips = []
planet_range = 40
planet_info_temps = []
for i in range(9):
    planet = Planet(system, planets[i], 10 + i * planet_range, 200)
    planets_ob.append(planet)
    if i > 3:
        planet_range = 50
    if i > 4:
        planet_range = 58
    info_temp = ''
    for j in range(4):
        info_temp += info_all[j] + info_planet[planets[i]][j] + '/'
    planet_info_temps.append(info_temp)
    info_temp += 'population=' + str(population[planets[i]])
    fl = 0
    if i > 4:
        fl = 1
    tooltip_planet = Tooltip(planet.rect, current_pos, info_temp, screen, fl)
    tooltips.append(tooltip_planet)

gameplay_start = False
tooltip = Tooltip(pygame.Rect(0, 0, 50, 50), current_pos, 'run away/save your life/lol', screen)
gaming = False
total_pop = 0
total = Word('total population ' + str(total_pop), (0, 480), (20, 20))
start = load_image('start.png', (0, 0, 0))
start = pygame.transform.smoothscale(start, (50, 50))
count_fl = False
while running:
    screen.fill((0, 0, 0))
    if not gameplay_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run_out = True
            if event.type == pygame.MOUSEMOTION:
                current_pos = event.pos
        background.draw(screen)
        background.update()
        title.draw(screen)
        undertitle.draw(screen)
        undertitle.update(run_out)
        title.update(run_out)
        info.draw(screen)
        info.update(run_out, 0)
        tooltip.update(current_pos)
        if info.y < -20:
            gameplay_start = True
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run_out = True
            if event.type == pygame.MOUSEMOTION:
                current_pos = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                current_planet = -1
                for i in planets_ob:
                    if i.rect.collidepoint(event.pos):
                        current_planet = i
                        gaming = True
                        break
                if event.pos[0] > 450 and event.pos[1] < 50:
                    count_fl = not count_fl
        if gaming:
            play = True
            fl = 0
            arrow = load_image('arrow.png', (0, 0, 0))
            arrow = pygame.transform.smoothscale(arrow, (50, 50))
            rect = arrow.get_rect()
            button_down = False
            while play:
                screen.fill((0, 0, 0))
                background.draw(screen)
                background.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        play = False
                        running = False
                        gaming = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            planets_population[i.planet_name].get_click(event.pos)
                            if event.pos[0] > 450 and event.pos[1] < 50:
                                play = False
                                gaming = False
                            button_down = True
                        elif event.button == 3:
                            fl = 1 - fl
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            fl = 1 - fl
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            button_down = False
                    elif event.type == pygame.MOUSEMOTION:
                        if button_down:
                            planets_population[i.planet_name].get_click(event.pos)
                if fl:
                    planets_population[i.planet_name].next_move()
                population[i.planet_name] = planets_population[i.planet_name].alive_count()
                planets_population[i.planet_name].render()
                screen.blit(arrow, (450, 0))
                prev_pop = total_pop - 1 + 1
                total_pop = 0
                for j in population.keys():
                    total_pop += population[j]
                if prev_pop != total_pop:
                    total = Word('total population ' + str(total_pop), (0, 480), (20, 20))
                pygame.display.flip()
                pygame.time.delay(50)
            tooltips[planets.index(i.planet_name)].update_popul(planet_info_temps[planets.index(i.planet_name)]
                                                                + 'population=' + str(population[i.planet_name]))
        else:
            if count_fl:
                total_pop = 0
                for i in planets:
                    planets_population[i].next_move()
                    total_pop += planets_population[i].alive_count()
                total = Word('total population ' + str(total_pop), (0, 480), (20, 20))
            background.draw(screen)
            background.update()
            system.draw(screen)
            total.draw(screen)
            screen.blit(start, (450, 0))
            for i in tooltips:
                i.update(current_pos)
    pygame.display.flip()
    pygame.time.delay(50)
pygame.quit()
