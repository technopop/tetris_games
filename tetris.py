import pygame
import random

# テトリス基本設定
pygame.init()

WIDTH, HEIGHT = 300, 600
BLOCK = 30
COLS, ROWS = WIDTH // BLOCK, HEIGHT // BLOCK

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()


# 7種類のテトリスブロック
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
]

COLORS = [
    (0, 255, 255),
    (255, 255, 0),
    (128, 0, 128),
    (0, 0, 255),
    (255, 127, 0),
    (0, 255, 0),
    (255, 0, 0),
]

SPEEDS = {"SLOW": 800, "NOMAL": 500, "FAST": 200}

# ブロッククラス


class Block:
    def __init__(self):
        self.index = random.randrange(len(SHAPES))
        self.shape = SHAPES[self.index]
        self.color = COLORS[self.index]
        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))


# 衝突チェック


def valid_position(grid, block):
    for y, row in enumerate(block.shape):
        for x, cell in enumerate(row):
            if cell:
                nx = block.x + x
                ny = block.y + y
                if nx < 0 or nx >= COLS or ny >= ROWS:
                    return False
                if grid[ny][nx]:
                    return False
    return True


# ライン消去


def clear_lines(grid):
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    cleared = ROWS - len(new_grid)
    for _ in range(cleared):
        new_grid.insert(0, [0] * COLS)
    return new_grid


# ゲームループ
def main():
    grid = [[0] * COLS for _ in range(ROWS)]
    block = Block()
    fall_time = 0

    running = True

    while running:
        screen.fill((0, 0, 0))
        fall_time += clock.get_rawtime()
        clock.tick(60)

        # 操作
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                old_x, old_y = block.x, block.y
                if event.key == pygame.K_LEFT:
                    block.x -= 1
                    if not valid_position(grid, block):
                        block.x += 1
                elif event.key == pygame.K_RIGHT:
                    block.x += 1
                    if not valid_position(grid, block):
                        block.x -= 1
                elif event.key == pygame.K_DOWN:
                    block.y += 1
                    if not valid_position(grid, block):
                        block.y -= 1
                elif event.key == pygame.K_UP:
                    old_shape = block.shape
                    block.rotate()
                    if not valid_position(grid, block):
                        block.shape = old_shape

        # 自動落下
        if fall_time > 500:
            block.y += 1
            if not valid_position(grid, block):
                block.y -= 1
                for y, row in enumerate(block.shape):
                    for x, cell in enumerate(row):
                        if cell:
                            grid[block.y + y][block.x + x] = block.index
                grid = clear_lines(grid)
                block = Block()
                if not valid_position(grid, block):
                    print("Game over")
                    running = False
            fall_time = 0

        screen.fill((0, 0, 0))

        # 描画、固定されたブロック
        for y in range(ROWS):
            for x in range(COLS):
                if grid[y][x]:
                    color = COLORS[grid[y][x]]
                    pygame.draw.rect(
                        screen, color, (x * BLOCK, y * BLOCK, BLOCK, BLOCK)
                    )

        # 描画、現在落下ブロック

        for y, row in enumerate(block.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        screen,
                        block.color,
                        ((block.x + x) * BLOCK, (block.y + y) * BLOCK, BLOCK, BLOCK),
                    )
        pygame.display.update()


# 実行

if __name__ == "__main__":
    main()
    pygame.quit()
