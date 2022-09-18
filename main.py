import pygame
import neat
import time, os, random
from constants import *
from src.bird import Bird
from src.base import Base
from src.pipe import Pipe


def main(genomes, cfg):
    birds = []
    nets = []
    ge = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, cfg)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    base = Base(FLOOR)
    pipes = [Pipe(PIPE_DIST)]

    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    clock = pygame.time.Clock()

    run = True
    score = 0
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        base.move()

        pipe_idx = 0
        if len(birds) > 0:
            if (
                len(pipes) > 1
                and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width()
            ):
                pipe_idx = 1
        else:
            run = False
            break

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            output = nets[x].activate(
                (
                    bird.y,
                    abs(bird.y - pipes[pipe_idx].height),
                    abs(bird.y - pipes[pipe_idx].bottom),
                )
            )

            if output[0] > 0.5:
                bird.jump()

        rem = []
        add_pipe = False
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(PIPE_DIST))

        for r in rem:
            pipes.remove(r)

        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() > FLOOR or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        draw_window(win, birds, pipes, base, score)


def draw_window(win, birds, pipes, base, score):
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)
    base.draw(win)
    for bird in birds:
        bird.draw(win)

    text = STAT_FONT.render(f"Score: {score}", 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    pygame.display.update()


def run(cfg_path):
    cfg = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        cfg_path,
    )

    p = neat.Population(cfg)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    cfg_path = os.path.join(local_dir, "config_ffwd.txt")
    run(cfg_path)
