# save as warehouse_sim.py
import pygame, sys, heapq, random, time
from collections import deque, defaultdict, namedtuple

# ---------- Config ----------
GRID_W, GRID_H = 20, 12
CELL = 40
FPS = 10
NUM_ROBOTS = 4
NUM_TASKS = 6

# ---------- Utils ----------
def manhattan(a,b): return abs(a[0]-b[0]) + abs(a[1]-b[1])

# ---------- A* ----------
def astar(grid_w, grid_h, start, goal, occupied=set()):
    def neighbors(n):
        x,y = n
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx,ny = x+dx, y+dy
            if 0 <= nx < grid_w and 0 <= ny < grid_h:
                yield (nx,ny)
    openq = []
    heapq.heappush(openq,(0+manhattan(start,goal),0,start,None))
    came_from = {}
    gscore = {start:0}
    while openq:
        f,g,node,par = heapq.heappop(openq)
        if node==goal:
            path=[node]
            while par:
                path.append(par)
                par=came_from.get(par)
            path.reverse()
            return path
        for nb in neighbors(node):
            if nb in occupied and nb!=goal: continue
            ng = g+1
            if ng < gscore.get(nb, 1e9):
                gscore[nb]=ng
                came_from[nb]=node
                heapq.heappush(openq,(ng+manhattan(nb,goal), ng, nb, node))
    return None

# ---------- Entities ----------
Task = namedtuple('Task',['id','src','dst','assigned','status'])
class Robot:
    def __init__(self, rid, pos):
        self.rid = rid
        self.pos = pos
        self.path = []
        self.task = None
        self.status = 'idle'  # idle, to_pick, to_drop
        self.reservations = []

    def step(self):
        if self.path:
            self.pos = self.path.pop(0)

# ---------- Auction allocator ----------
def auction_allocate(robots, tasks):
    unassigned = [t for t in tasks if t.assigned is None]
    for t in unassigned:
        bids=[]
        for r in robots:
            if r.task is None:
                cost = manhattan(r.pos, t.src)
                bids.append((cost, r.rid))
        if not bids: continue
        bids.sort()
        winner_rid = bids[0][1]
        for r in robots:
            if r.rid==winner_rid:
                r.task = t
                t = t._replace(assigned=r.rid)
                break

# ---------- Reservation planner ----------
# Simple time-step reservation of grid cells to avoid collisions
def build_time_reservations(robots):
    res = defaultdict(set)  # time -> set(cells)
    # we will simulate only next K steps
    K = 20
    for r in robots:
        t = 0
        cur = r.pos
        res[t].add(cur)
        for p in r.path[:K]:
            t+=1
            res[t].add(p)
    return res

# ---------- Initialize ----------
pygame.init()
screen = pygame.display.set_mode((GRID_W*CELL, GRID_H*CELL))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 20)

robots = []
for i in range(NUM_ROBOTS):
    robots.append(Robot(i, (random.randint(0,GRID_W-1), random.randint(0,GRID_H-1))))

tasks = []
for i in range(NUM_TASKS):
    s = (random.randint(0,GRID_W-1), random.randint(0,GRID_H-1))
    d = (random.randint(0,GRID_W-1), random.randint(0,GRID_H-1))
    tasks.append(Task(i,s,d,None,'pending'))

# ---------- Main loop ----------
tick = 0
while True:
    tick += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
    # allocate every few ticks
    if tick % 6 == 0:
        auction_allocate(robots, tasks)

    # Plan / replan for robots with assigned tasks
    # Build reservations from currently planned paths
    reservations = build_time_reservations(robots)
    for r in robots:
        if r.task:
            # pick up stage
            if r.status == 'idle':
                path = astar(GRID_W, GRID_H, r.pos, r.task.src, occupied=set())
                if path:
                    r.path = path[1:]
                    r.status = 'to_pick'
            elif r.status == 'to_pick' and not r.path:
                # reached pick, plan to drop
                r.status = 'to_drop'
                path = astar(GRID_W, GRID_H, r.pos, r.task.dst, occupied=set())
                if path:
                    r.path = path[1:]
            elif r.status == 'to_drop' and not r.path:
                # done
                for i,t in enumerate(tasks):
                    if t.id==r.task.id:
                        tasks[i] = t._replace(status='done')
                r.task = None
                r.status = 'idle'
        else:
            # roam or stay idle
            pass

    # Step robots
    # naive collision check: don't step into a cell another robot currently occupies
    occupied_now = {tuple(r.pos):r.rid for r in robots}
    for r in robots:
        if r.path:
            nxt = r.path[0]
            # if next cell currently occupied by peer, wait (simple)
            if nxt in occupied_now.values():
                # wait
                pass
            else:
                r.step()

    # DRAW
    screen.fill((30,30,30))
    # grid
    for x in range(GRID_W):
        for y in range(GRID_H):
            rect = pygame.Rect(x*CELL, y*CELL, CELL, CELL)
            pygame.draw.rect(screen, (50,50,50), rect, 1)
    # tasks
    for t in tasks:
        color = (0,200,0) if t.status!='done' else (80,80,80)
        pygame.draw.rect(screen, color, pygame.Rect(t.src[0]*CELL+8, t.src[1]*CELL+8, CELL-16, CELL-16), 2)
        pygame.draw.rect(screen, (200,0,0), pygame.Rect(t.dst[0]*CELL+12, t.dst[1]*CELL+12, CELL-24, CELL-24), 2)
        screen.blit(font.render(f"T{t.id}", True, (200,200,200)), (t.src[0]*CELL+2, t.src[1]*CELL+2))
    # robots
    for r in robots:
        pygame.draw.circle(screen, (0,120,255), (r.pos[0]*CELL+CELL//2, r.pos[1]*CELL+CELL//2), CELL//3)
        screen.blit(font.render(f"R{r.rid}", True, (255,255,255)), (r.pos[0]*CELL+2, r.pos[1]*CELL+2))
        # path preview
        for i,p in enumerate(r.path[:8]):
            pygame.draw.circle(screen, (150,150,255), (p[0]*CELL+CELL//2, p[1]*CELL+CELL//2), 5)
    # status panel
    y = 4
    for r in robots:
        txt = f"R{r.rid} pos:{r.pos} task:{r.task.id if r.task else 'None'} status:{r.status}"
        screen.blit(font.render(txt, True, (220,220,220)), (4, GRID_H*CELL - 80 + y))
        y += 18
    pygame.display.flip()
    clock.tick(FPS)
