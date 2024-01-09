import numpy as np
import itertools
import pygame
import random
import time
import collections

def to_piece(tuple_defintion):
    returned = set()
    for y, row in enumerate(tuple_defintion):
        for x, value in enumerate(row):
            if value == 1: returned.add((x, y))   
    return returned

class Solver:
    def __init__(self, width, height, pieces):
        self.width, self.height = width, height
        self.pieces = pieces

    def solve(self, grid = None, counts = None):
        if grid is None: grid = np.zeros((self.width, self.height), dtype=np.int32)
        if counts is None: counts = np.ones((len(self.pieces),), dtype=np.int32)
        next_available = self.get_next_available(grid)
        if next_available is None: 
            self.draw(grid, 0)
            return grid
        for p_index, count in enumerate(counts):
            if count == 0: continue
            piece = self.pieces[p_index]
            for rotation in piece:
                for coord in rotation:
                    new_grid = self.place_piece(grid, next_available, rotation, coord, p_index)
                    if new_grid is None: continue
                    solution = self.solve(new_grid, counts - np.array([1 if i == p_index else 0 for i in range(len(counts))]))
                    if not solution is None: return solution
        
    def get_next_available(self, grid):
        for y in range(self.height):
            for x in range(self.width):
                if grid[x, y] == 0: return (x, y)

    def place_piece(self, grid, available, piece, coord, p_index):
        ## we want coord + offset = available => offset = available - coord
        offset = available[0] - coord[0], available[1] - coord[1]
        new_grid = grid.copy()
        for (px, py) in piece:
            tx, ty = px + offset[0], py + offset[1]
            if tx < 0 or ty < 0 or tx >= self.width or ty >= self.height or grid[tx, ty] != 0: return None
            new_grid[tx, ty] = 1 + p_index

        return new_grid
    
    def draw(self, grid, sleep = 1):
        BLOCK_SIZE = 100
        screen_width, screen_height = BLOCK_SIZE * self.width, BLOCK_SIZE * self.height
        screen = pygame.display.set_mode((screen_width, screen_height))
        screen.fill((0, 0, 0))

        def random_colour():
            return (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
        
        colours = collections.defaultdict(random_colour)

        for (x, y) in itertools.product(range(self.width), range(self.height)):
            piece_num = grid[x, y]
            if piece_num > 0:
                rect = pygame.Rect(x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, colours[piece_num], rect)

        pygame.display.update()
        if sleep > 0:
            time.sleep(sleep)
    
if __name__ == "__main__":
    SQUARE1 = to_piece(((1, 1), (1, 1)))
    SQUARE = (SQUARE1,)

    CROSS_D = to_piece(((1, 1, 1), (0, 1, 0)))
    CROSS_U = to_piece(((0, 1, 0), (1, 1, 1)))
    CROSS_L = to_piece(((0, 1), (1, 1), (0, 1)))
    CROSS_R = to_piece(((1, 0), (1, 1), (1, 0)))
    CROSS = (CROSS_D, CROSS_U, CROSS_L, CROSS_R)

    LINE_H = to_piece(((1, 1, 1, 1),))
    LINE_V = to_piece(((1,), (1,), (1,), (1,)))
    LINE = (LINE_H, LINE_V)

    L1 = to_piece(((1, 1, 1), (1, 0, 0)))
    L2 = to_piece(((1, 1), (0, 1), (0, 1)))
    L3 = to_piece(((0, 0, 1), (1, 1, 1)))
    L4 = to_piece(((1, 0), (1, 0), (1, 1)))
    L = (L1, L2, L3, L4)

    Z1 = to_piece(((0, 1, 1), (1, 1, 0)))
    Z2 = to_piece(((1, 0), (1, 1), (0, 1)))
    Z1 = (Z1, Z2)

    Z3 = to_piece(((1, 1, 0), (0, 1, 1)))
    Z4 = to_piece(((0, 1), (1, 1), (1, 0)))
    Z2 = (Z3, Z4)


    def easy():
        solver = Solver(4, 2, (SQUARE, SQUARE))
        return solver, solver.solve()

    def medium():    
        solver = Solver(4, 4, (LINE, L, L, Z1))
        return solver, solver.solve()
    
    def hard():
        solver = Solver(5, 8, (LINE, LINE, SQUARE, CROSS, CROSS, L, L, Z2, Z2, Z1))#, (2, 1, 2, 2, 2, 1))
        return solver, solver.solve()
    
    def hardest():
        solver = Solver(8, 7, (LINE, LINE, SQUARE, SQUARE, SQUARE, SQUARE, CROSS, CROSS, CROSS, CROSS, L, L, Z2, Z1))#, (2, 1, 2, 2, 2, 1))
        return solver, solver.solve()
    
    pygame.init()
    #solver, result = easy()
    #solver, result = medium()
    #solver, result = hard()
    solver, result = hardest()

    if result is None: print("Failed")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
        pygame.display.update()
    pygame.quit()

