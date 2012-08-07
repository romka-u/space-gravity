
import pygame

def fill_gradient(screen, rect, top_color, bottom_color):
    h = rect.height
    rate = [(bc - tc) * 1.0 / h
            for bc, tc in zip(bottom_color, top_color)]

    for line in xrange(h):
        cur_color = tuple(max(min(int(tc + line * r), 255), 0)
                          for tc, r in zip(top_color, rate))
        pygame.draw.line(screen, cur_color,
            (rect.left, rect.top + line),
            (rect.right, rect.top + line))
