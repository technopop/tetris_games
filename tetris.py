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

SPEEDS = {"SLOW": 800, "NORMAL": 500, "FAST": 200}

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

    current_speed_name = "NORMAL"
    fall_interval = SPEEDS[current_speed_name]

    running = True

    font = pygame.font.Font(None, 24)

    # スピードボタンの配置
    button_width = 80
    button_height = 30
    margin = 15

    speed_buttons = {}
    x = margin
    for name in ["SLOW", "NORMAL", "FAST"]:
        speed_buttons[name] = pygame.Rect(x, margin, button_width, button_height)
        x += button_width + margin

    while running:
        screen.fill((0, 0, 0))
        dt = clock.tick(60)
        fall_time += dt

        # fall_time += clock.get_rawtime()
        # clock.tick(60)

        # 操作
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                for name, rect in speed_buttons.items():
                    if rect.collidepoint(mx, my):
                        current_speed_name = name
                        fall_interval = SPEEDS[name]
            elif event.type == pygame.KEYDOWN:
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
        if fall_time > fall_interval:
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
                if grid[y][x] != 0:
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

            # labels = [("SLOW", "1"), ("NORMAL", "2"), ("FAST", "3")]
            #    x = 10
            #    y = 10

            # ---------- スピードボタン描画 ----------
            for name, rect in speed_buttons.items():
                if name == current_speed_name:
                    bg_color = (255, 100, 50)
                    text_color = (255, 255, 255)
                else:
                    bg_color = (60, 60, 60)
                    text_color = (255, 255, 255)

                pygame.draw.rect(screen, bg_color, rect)

                label = font.render(name, True, text_color)

                label_pos = label.get_rect(center=rect.center)
                screen.blit(label, label_pos)

                # x += text_surface.get_width() + 20

            pygame.display.update()


# 実行

if __name__ == "__main__":
    main()
    pygame.quit()
