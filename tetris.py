import pygame
import random

# 画面サイズとレイアウト
pygame.init()

PLAY_WIDTH = 300
UI_WIDTH = 180
WIDTH, HEIGHT = PLAY_WIDTH + UI_WIDTH, 600

BLOCK = 30
COLS, ROWS = PLAY_WIDTH // BLOCK, HEIGHT // BLOCK

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
        self.shape = [list(row) for row in zip(*self.shape[::-1])]


# 衝突チェック


def valid_position(grid, block):
    for dy, row in enumerate(block.shape):
        for dx, cell in enumerate(row):
            if not cell:
                continue
            nx = block.x + dx
            ny = block.y + dy
            if nx < 0 or nx >= COLS or ny >= ROWS:
                return False
            if ny >= 0 and grid[ny][nx] != 0:
                return False
    return True


# ライン消去


def clear_lines(grid):
    new_grid = [row for row in grid if 0 in row]
    cleared = ROWS - len(new_grid)
    for _ in range(cleared):
        new_grid.insert(0, [0] * COLS)
    return new_grid, cleared


# ゲームループ
def main():
    grid = [[0] * COLS for _ in range(ROWS)]
    block = Block()
    fall_time = 0

    current_speed_name = "NORMAL"
    fall_interval = SPEEDS[current_speed_name]

    running = True

    font = pygame.font.Font(None, 24)

    # ---- 右側パネル内のボタン位置を決める ----
    button_width = 120
    button_height = 32
    margin_top = 80
    # margin_side = PLAY_WIDTH + 15

    # パネルの中央寄せ
    panel_left = PLAY_WIDTH
    panel_center_x = panel_left + UI_WIDTH // 2

    speed_buttons = {}
    y = margin_top

    for name in ["SLOW", "NORMAL", "FAST"]:
        rect = pygame.Rect(0, 0, button_width, button_height)
        rect.centerx = panel_center_x
        rect.y = y
        speed_buttons[name] = rect
        y += button_height + 15

    score = 0

    while running:
        dt = clock.tick(60)
        fall_time += dt

        # 操作
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # マウスクリックでスピード変更
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                for name, rect in speed_buttons.items():
                    if rect.collidepoint(mx, my):
                        current_speed_name = name
                        fall_interval = SPEEDS[name]

            # キー操作でブロック移動
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

                for dy, row in enumerate(block.shape):
                    for dx, cell in enumerate(row):
                        if cell:
                            ny = block.y + dy
                            nx = block.x + dx
                            if 0 <= ny < ROWS and 0 <= nx < COLS:
                                grid[ny][nx] = block.index + 1
                grid, cleared = clear_lines(grid)
                # score += cleared
                block = Block()
                if not valid_position(grid, block):
                    print("Game over")
                    running = False
            fall_time = 0

        screen.fill((10, 10, 10))

        # 描画、固定されたブロック
        for x in range(COLS + 1):
            pygame.draw.line(
                screen,
                (40, 40, 40),
                (x * BLOCK, 0),
                (x * BLOCK, HEIGHT),
            )

        for y in range(ROWS + 1):
            pygame.draw.line(
                screen,
                (40, 40, 40),
                (0, y * BLOCK),
                (PLAY_WIDTH, y * BLOCK),
            )

        # 描画、現在落下ブロック
        for y in range(ROWS):
            for x in range(COLS):
                idx = grid[y][x]
                if idx != 0:
                    color = COLORS[idx - 1]
                    pygame.draw.rect(
                        screen,
                        color,
                        (x * BLOCK, y * BLOCK, BLOCK, BLOCK),
                    )

        for dy, row in enumerate(block.shape):
            for dx, cell in enumerate(row):
                if cell:
                    bx = block.x + dx
                    by = block.y + dy
                    if 0 <= bx < COLS and 0 <= by < ROWS:
                        pygame.draw.rect(
                            screen,
                            block.color,
                            (bx * BLOCK, by * BLOCK, BLOCK, BLOCK),
                        )

        # 右側パネル背景
        panel_rect = pygame.Rect(PLAY_WIDTH, 0, UI_WIDTH, HEIGHT)
        pygame.draw.rect(screen, (30, 30, 30), panel_rect)

        # パネル内 縦のアクセントライン
        pygame.draw.line(
            screen,
            (50, 50, 50),
            (PLAY_WIDTH + UI_WIDTH // 1, 0),
            (PLAY_WIDTH + UI_WIDTH // 1, HEIGHT),
            2,
        )

        # SPEED タイトル
        title = font.render("SPEED", True, (255, 255, 255))
        title_rect = title.get_rect(center=(panel_center_x, 40))
        screen.blit(title, title_rect)

        # ---------- スピードボタン描画 ----------

        mouse_pos = pygame.mouse.get_pos()

        for name, rect in speed_buttons.items():
            is_hover = rect.collidepoint(mouse_pos)
            is_active = name == current_speed_name

            if is_active:
                bg_color = (255, 215, 0)
                text_color = (0, 0, 0)
            elif is_hover:
                bg_color = (100, 100, 100)
                text_color = (255, 255, 255)
            else:
                bg_color = (60, 60, 60)
                text_color = (220, 220, 220)

            pygame.draw.rect(screen, bg_color, rect, border_radius=8)

            label = font.render(name, True, text_color)
            label_pos = label.get_rect(center=rect.center)
            screen.blit(label, label_pos)

        # スコア表示（おまけ）
        # score_text = font.render(f"LINES: {score}", True, (255, 255, 255))
        # screen.blit(score_text, (PLAY_WIDTH + 20, HEIGHT - 40))

        # プレイエリアとパネルの境界線
        pygame.draw.line(
            screen,
            (80, 80, 80),
            (PLAY_WIDTH, 0),
            (PLAY_WIDTH, HEIGHT),
            2,
        )

        pygame.display.update()


# 実行

if __name__ == "__main__":
    main()
    pygame.quit()
