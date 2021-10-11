from queue import Queue


def bfs(n):
    f = open(str(n) + '_bfs_output.txt', 'w')

    if n == 1:
        f.write('1')
    elif n < 4:
        f.write('no solution')
    else:
        q = Queue()

        # init - [0~(N-1), -1, ~, -1]를 enqueue ((0 ~ N-1)번째 행에 queen이 위치, -1은 queen이 위치하지 않음)
        for i in range(n):
            queens = [i]
            for j in range(n - 1):
                queens.append(-1)
            q.put(queens)

        # expand - 맨 앞부터 dequeue하고 goal인지 판단 후 expand
        while not q.empty():
            queens = q.get()  # dequeue
            if queens[n - 1] != -1:  # select 한 것이 Goal 일 때
                for i in range(n):
                    queens[i] += 1  # index로 계산했기 때문에 행 번호를 0시작에서 1시작으로 변경
                answer = ", ".join(map(str, queens))  # 리스트를 문자열로 형변환 및 출력형식 맞추기
                f.write(answer)
                f.close()
                return

            check = False  # queen을 연속으로 놓지 않기 위해 check
            for tmpCol in range(n):
                if queens[tmpCol] == -1 and not check:
                    check = True
                    tmp = queens[0:tmpCol]
                    for tmpRow in range(n):
                        for col, row in enumerate(tmp):
                            if tmpRow == row or abs(tmpCol - col) == abs(tmpRow - row):
                                break
                        else:
                            newTmp = queens[:]
                            newTmp[tmpCol] = tmpRow
                            q.put(newTmp)
                            continue
                        continue


import random


def hc(n):
    def calculate(q):
        h = 0
        for col, row in enumerate(q):
            if col == n - 1:
                break
            for tmpCol, tmpRow in enumerate(q):
                if tmpCol > col:
                    if row == tmpRow or abs(tmpCol - col) == abs(tmpRow - row):
                        h += 1
        return h

    f = open(str(n) + '_hc_output.txt', 'w')

    if n == 1:
        f.write('1')
    elif n < 4:
        f.write('no solution')
    else:
        queens = random.sample(range(n), n)  # 각 열마다 행이 겹치지 않는 랜덤한 위치에 queen 생성
        queens = [5, 4, 1, 3, 0, 2]

        for move in range(4):
            h = calculate(queens)
            hBoard = [[n * 3] * n for i in range(n)]
            for col in range(n):
                for row in range(n):
                    tmp = queens[:]
                    tmp[col] = row
                    hBoard[row][col] = calculate(tmp)
            for col, row in enumerate(queens):
                hBoard[row][col] = 9

            print('queens=',queens,' h=',h)
            print("\n".join(map(str, hBoard)))

            tmpRow = hBoard.index(min(hBoard))
            tmpCol = hBoard[tmpRow].index(min(hBoard[tmpRow]))

            queens[tmpCol] = tmpRow


        print(queens)
        print(hBoard)
        # print("\n".join(map(str, hBoard)))
        print(h)

    f.close()


def csp(n):
    f = open(str(n) + '_csp_output.txt', 'w')

    if n == 1:
        f.write('1')
    elif n < 4:
        f.write('no solution')
    else:
        pass

    f.close()


if __name__ == '__main__':
    f = open('input.txt', 'r')
    for i in f:
        tmp = i.strip().split()
        func = tmp[1]
        N = int(tmp[0])

        if func == 'bfs':
            bfs(N)
        elif func == 'hc':
            hc(N)
        # elif func == 'csp':
        #     csp(N)
        # else:
        #     print('Input error')
    f.close()
