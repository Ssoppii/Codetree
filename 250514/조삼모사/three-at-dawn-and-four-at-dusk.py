n = int(input().rstrip())
matrix = []
for _ in range(n):
    tmp = list(map(int, input().rstrip().split()))
    matrix.append(tmp)

def combine(n, k):
    result = []

    def backtrack(start, path):
        if len(path) == k:
            result.append(path[:])  # 복사해서 저장
            return

        for i in range(start, n + 1):
            path.append(i)               # 1. 선택
            backtrack(i + 1, path)       # 2. 다음 숫자부터 재귀 탐색
            path.pop()                   # 3. 백트래킹 (되돌리기)

    backtrack(1, [])
    return result

candidate = combine(n, n//2)

MIN = 4001
for c in range(len(candidate)):
    work = combine(len(candidate[0]), 2)
    morning = 0
    evening = 0 
    for w in work:
        i_m = candidate[c][w[0]-1]-1
        j_m = candidate[c][w[1]-1]-1
        i_e = candidate[len(candidate)-c-1][w[0]-1]-1
        j_e = candidate[len(candidate)-c-1][w[1]-1]-1
        morning += matrix[i_m][j_m] + matrix[j_m][i_m]
        evening += matrix[i_e][j_e] + matrix[j_e][i_e]
    workload = abs(morning-evening)
    if MIN > workload:
        MIN = workload

print(MIN)