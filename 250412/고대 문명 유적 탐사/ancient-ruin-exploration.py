from collections import deque

# ✅ 입력 받기
K, m = map(int, input().rstrip().split())
board = [list(map(int, input().rstrip().split())) for _ in range(5)]
M = list(map(int, input().rstrip().split()))

# ✅ BFS: 유물 탐색
# 중복 제거 버전
def bfs(board):
    visited = [[False]*5 for _ in range(5)]
    score = 0
    all_coords = set()

    for i in range(5):
        for j in range(5):
            if visited[i][j]:
                continue
            queue = deque([(i, j)])
            visited[i][j] = True
            group = [(i, j)]
            while queue:
                x, y = queue.popleft()
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 5 and 0 <= ny < 5 and not visited[nx][ny] and board[nx][ny] == board[x][y]:
                        visited[nx][ny] = True
                        queue.append((nx, ny))
                        group.append((nx, ny))
            if len(group) >= 3:
                score += len(group)
                all_coords.update(group)  # set에 넣기

    return score, list(all_coords)

# ✅ exploration: 최대 점수 회전 탐색
def exploration(board):
    best_score = 0
    best_r = best_c = best_d = 0
    for r in range(3):
        for c in range(3):
            backup = [row[c:c+3] for row in board[r:r+3]]
            sub = [row[c:c+3] for row in board[r:r+3]]
            for k in range(3):  # 90, 180, 270도
                rotated = [[0]*3 for _ in range(3)]
                for i in range(3):
                    for j in range(3):
                        rotated[i][j] = sub[2-j][i]
                sub = [row[:] for row in rotated]
                for i in range(3):
                    for j in range(3):
                        board[r+i][c+j] = rotated[i][j]
                score, _ = bfs(board)
                if score > best_score or (score == best_score and k+1 < best_d) or (score == best_score and k+1 == best_d and c < best_c) or (score == best_score and k+1 == best_d and c == best_c and r < best_r):
                    best_score = score
                    best_r, best_c, best_d = r, c, k+1
            for i in range(3):
                board[r+i][c:c+3] = backup[i]
    return [best_score, best_r, best_c, best_d]

# ✅ 유물 채움
def fill_new_artifacts(board, coords):
    # ✅ 중복 제거 + 우선순위 정렬
    coords = list(set(coords))
    coords.sort(key=lambda x: (x[1], -x[0]))
    for x, y in coords:
        if M:
            board[x][y] = M.pop(0)
        else:
            board[x][y] = -1

# ✅ 회전 + 유물 연쇄 처리
def picknfill(board, explore_detail):
    _, r, c, d = explore_detail
    sub = [row[c:c+3] for row in board[r:r+3]]
    for _ in range(d):
        sub = [[sub[2-j][i] for j in range(3)] for i in range(3)]
    for i in range(3):
        for j in range(3):
            board[r+i][c+j] = sub[i][j]

    score = 0
    while True:
        s, group = bfs(board)
        if s == 0:
            break
        score += s
        fill_new_artifacts(board, group)
    return score

# ✅ 메인 실행
for turn in range(K):
    explore_detail = exploration(board)
    score = 0
    if explore_detail[0] > 0:
        score = picknfill(board, explore_detail)
        # ✅ 최종 점수 출력
        print(score, end = " ")