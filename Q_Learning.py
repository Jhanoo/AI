import random

M = ''  # Map 5x5 size
r = [[-1] * 25 for _ in range(25)]  # action에 대한 reward
Q = [[0] * 25 for _ in range(25)]  # Q table

gamma = 0.9  # Decaying factor
T = 1  # Bonus reward
S = -1  # Start Position
G = -1  # Goal Position


def init():
    global S, G
    for a in range(25):
        # Set Start and Goal Position
        if M[a] == 'S':
            S = a
        elif M[a] == 'G':
            G = a

        # 오른쪽으로 이동할 때
        if a % 5 != 4:
            # Bomb => r = -100
            if M[a + 1] == 'B':
                r[a][a + 1] = -100

            # Normal Path, Start Point => r = 0
            elif M[a + 1] == 'P' or M[a + 1] == 'S':
                r[a][a + 1] = 0

            # Bonus Point => r = T
            elif M[a + 1] == 'T':
                r[a][a + 1] = T

            # Goal Point => r = 100
            elif M[a + 1] == 'G':
                r[a][a + 1] = 100

        # 왼쪽으로 이동할 때
        if a % 5 != 0:
            if M[a - 1] == 'B':
                r[a][a - 1] = -100

            elif M[a - 1] == 'P' or M[a - 1] == 'S':
                r[a][a - 1] = 0

            elif M[a - 1] == 'T':
                r[a][a - 1] = T

            elif M[a - 1] == 'G':
                r[a][a - 1] = 100

        # 아래로 이동할 때
        if int(a / 5) != 4:
            if M[a + 5] == 'B':
                r[a][a + 5] = -100

            elif M[a + 5] == 'P' or M[a + 5] == 'S':
                r[a][a + 5] = 0

            elif M[a + 5] == 'T':
                r[a][a + 5] = T

            elif M[a + 5] == 'G':
                r[a][a + 5] = 100

        # 위로 이동할 때
        if int(a / 5) != 0:
            if M[a - 5] == 'B':
                r[a][a - 5] = -100

            elif M[a - 5] == 'P' or M[a - 5] == 'S':
                r[a][a - 5] = 0

            elif M[a - 5] == 'T':
                r[a][a - 5] = T

            elif M[a - 5] == 'G':
                r[a][a - 5] = 100


def Q_Learning():
    S1 = S
    cnt = 0
    while cnt != 100000:
        cnt += 1
        actions = []
        for i in enumerate(r[S1]):
            # r == -1 이면 갈 수 없으므로 갈 수 있는 곳만 actions 리스트에 삽입
            if i[1] != -1:
                actions.append(i)

        # 갈 수 있는 action 들 중에서 랜덤으로 선택
        randomChoice = random.randrange(len(actions))
        # S2 = 이동할 State
        S2 = actions[randomChoice][0]
        # reward = r(s,a)
        reward = actions[randomChoice][1]

        # S2가 Goal 인 경우
        if reward == 100:
            Q[S1][S2] = reward
            continue

        # S2가 Bomb 인 경우, 처음 Start State 로 변경 후 다시 시작
        if reward == -100:
            S1 = S
            continue

        # Q(s,a) = r(s,a) + gamma * max( Q(s',a') )
        Q[S1][S2] = reward + gamma * max(Q[S2])

        S1 = S2


def printPath():
    p = ''
    S1 = S
    p += str(S1) + ' '

    isLoop = S1

    while S1 != G:
        S2 = Q[S1].index(max(Q[S1]))
        if isLoop == S2:
            p += 'Loop'
            break

        p += str(S2) + ' '

        isLoop = S1
        S1 = S2

    fw = open('output.txt', 'w')

    fw.write(p.strip() + '\n')
    fw.write(str(max(Q[S])))

    fw.close()


if __name__ == '__main__':
    fr = open('input.txt', 'r')
    for line in fr:
        M += (line.strip())
    fr.close()

    init()
    Q_Learning()
    printPath()
