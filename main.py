from collections import deque
import pygame
import asyncio


# Initialize Pygame
pygame.init()

# Screen & Grid Settings
WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Halloween Maze: BFS NPC vs. DFS NPC")

# Colors
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (220, 220, 220)
BLUE = (50, 120, 220)  # BFS Visitor / Path
RED = (220, 50, 50)  # DFS Visitor / Path
GREEN = (50, 180, 80)  # Goal (Candy)
ORANGE = (230, 120, 20)  # Start (Player)
WALL_COLOR = (40, 40, 60)

# Grid Configuration
ROWS, COLS = 25, 35
CELL_SIZE = 24
GRID_OFFSET_X = (WIDTH - (COLS * CELL_SIZE)) // 2
GRID_OFFSET_Y = 80

font = pygame.font.SysFont(None, 24)
font_large = pygame.font.SysFont(None, 32)

# Define Start and Goal
start = (1, 1)
goal = (COLS - 2, ROWS - 2)

# Simple static maze layout (0 = open path, 1 = wall)
# 1 = Wall, 0 = Open
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
for r in range(ROWS):
  for c in range(COLS):
    if r == 0 or r == 0 or r == ROWS - 1 or c == 0 or c == COLS - 1:
      grid[r][c] = 1

# Add some interior walls/obstacles
obstacles = [
    (5, 1),
    (5, 2),
    (5, 3),
    (5, 4),
    (5, 5),
    (2, 8),
    (3, 8),
    (4, 8),
    (5, 8),
    (6, 8),
    (7, 8),
    (10, 5),
    (10, 6),
    (10, 7),
    (10, 8),
    (10, 9),
    (15, 3),
    (15, 4),
    (15, 5),
    (15, 6),
    (12, 12),
    (13, 12),
    (14, 12),
    (15, 12),
    (16, 12),
    (8, 15),
    (9, 15),
    (10, 15),
    (11, 15),
    (12, 15),
]
for r, c in obstacles:
  if 0 < r < ROWS - 1 and 0 < c < COLS - 1:
    grid[r][c] = 1


def get_neighbors(node):
  r, c = node
  neighbors = []
  for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
    nr, nc = r + dr, c + dc
    if 0 <= nr < ROWS and 0 <= nc < COLS:
      if grid[nr][nc] == 0:
        neighbors.append((nr, nc))
  return neighbors


# --- Search State Initialization ---
def reset_searches():
  global bfs_queue, bfs_visited, bfs_parent, bfs_path, bfs_done
  global dfs_stack, dfs_visited, dfs_parent, dfs_path, dfs_done

  # BFS Setup (Queue -> FIFO -> Explores layer by layer)
  bfs_queue = deque([start])
  bfs_visited = {start}
  bfs_parent = {start: None}
  bfs_path = []
  bfs_done = False

  # DFS Setup (Stack -> LIFO -> Dives deep into one path first)
  dfs_stack = [start]
  dfs_visited = {start}
  dfs_parent = {start: None}
  dfs_path = []
  dfs_done = False


reset_searches()

# Main Game Loop
running = True
clock = pygame.time.Clock()

while running:
  screen.fill(WHITE)

  # Event Handling
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_r:
        reset_searches()

  # --- Step BFS Search (1 step per frame for smooth animation) ---
  if not bfs_done:
    if bfs_queue:
      current = bfs_queue.popleft()
      if current == goal:
        # Reconstruct path
        curr = goal
        while curr is not None:
          bfs_path.append(curr)
          curr = bfs_parent[curr]
        bfs_done = True
      else:
        for nxt in get_neighbors(current):
          if nxt not in bfs_visited:
            bfs_visited.add(nxt)
            bfs_parent[nxt] = current
            bfs_queue.append(nxt)
    else:
        bfs_done = True

  # --- Step DFS Search (1 step per frame) ---
  if not dfs_done:
    if dfs_stack:
      current = dfs_stack.pop()
      if current == goal:
        # Reconstruct path
        curr = goal
        while curr is not None:
          dfs_path.append(curr)
          curr = dfs_parent[curr]
        dfs_done = True
      else:
        for nxt in get_neighbors(current):
          if nxt not in dfs_visited:
            dfs_visited.add(nxt)
            dfs_parent[nxt] = current
            dfs_stack.append(nxt)
    else:
        dfs_done = True

  # --- Render Grid & Maze ---
  for r in range(ROWS):
    for c in range(COLS):
      rect = pygame.Rect(
          GRID_OFFSET_X + c * CELL_SIZE,
          GRID_OFFSET_Y + r * CELL_SIZE,
          CELL_SIZE - 1,
          CELL_SIZE - 1,
      )
      if grid[r][c] == 1:
        pygame.draw.rect(screen, WALL_COLOR, rect)
      else:
        pygame.draw.rect(screen, GRAY, rect)

  # Draw BFS Visited Nodes
  for r, c in bfs_visited:
    if (r, c) != start and (r, c) != goal:
      rect = pygame.Rect(
          GRID_OFFSET_X + c * CELL_SIZE + 4,
          GRID_OFFSET_Y + r * CELL_SIZE + 4,
          CELL_SIZE - 9,
          CELL_SIZE - 9,
      )
      pygame.draw.rect(screen, (150, 180, 240), rect)

  # Draw DFS Visited Nodes
  for r, c in dfs_visited:
    if (r, c) != start and (r, c) != goal and (r, c) not in bfs_visited:
      rect = pygame.Rect(
          GRID_OFFSET_X + c * CELL_SIZE + 8,
          GRID_OFFSET_Y + r * CELL_SIZE + 8,
          CELL_SIZE - 17,
          CELL_SIZE - 17,
      )
      pygame.draw.rect(screen, (240, 150, 150), rect)

  # Draw Final Paths
  for r, c in bfs_path:
    rect = pygame.Rect(
        GRID_OFFSET_X + c * CELL_SIZE + 6,
        GRID_OFFSET_Y + r * CELL_SIZE + 6,
        CELL_SIZE - 12,
        CELL_SIZE - 12,
    )
    pygame.draw.rect(screen, BLUE, rect)

  for r, c in dfs_path:
    rect = pygame.Rect(
        GRID_OFFSET_X + c * CELL_SIZE + 10,
        GRID_OFFSET_Y + r * CELL_SIZE + 10,
        CELL_SIZE - 20,
        CELL_SIZE - 20,
    )
    pygame.draw.rect(screen, RED, rect)

  # Draw Start and Goal Nodes
  start_rect = pygame.Rect(
      GRID_OFFSET_X + start[1] * CELL_SIZE,
      GRID_OFFSET_Y + start[0] * CELL_SIZE,
      CELL_SIZE - 1,
      CELL_SIZE - 1,
  )
  pygame.draw.rect(screen, ORANGE, start_rect)

  goal_rect = pygame.Rect(
      GRID_OFFSET_X + goal[1] * CELL_SIZE,
      GRID_OFFSET_Y + goal[0] * CELL_SIZE,
      CELL_SIZE - 1,
      CELL_SIZE - 1,
  )
  pygame.draw.rect(screen, GREEN, goal_rect)

  # HUD Display
  screen.blit(
      font_large.render(
          "Pathfinding Comparison: BFS (Blue) vs. DFS (Red)", True, BLACK
      ),
      (20, 15),
  )
  screen.blit(
      font.render(
          "Press [R] to Reset and restart the search animations.", True, BLACK
      ),
      (20, 45),
  )

  pygame.display.flip()
  clock.tick(30)

pygame.quit()
