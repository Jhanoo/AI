from queue import Queue


def bfs(n):
    f = open(str(n) + '_bfs_output.txt', 'w')

    if n == 1:
        f.write('1')
        f.close()
    elif n < 4:
        f.write('no solution')
        f.close()
    else:
        q = Queue()

        # (0 ~ N-1)번째 행에 queen이 위치, -1은 queen이 아직 위치하지 않음을 나타냄
        for i in range(n):
            queens = [i]
            for j in range(n - 1):
                queens.append(-1)
            q.put(queens)  # [0~(N-1), -1, ~, -1]를 enqueue

        # Queue의 맨 앞부터 dequeue하고 goal인지 판단 후 expand
        while not q.empty():
            queens = q.get()  # dequeue
            if queens[n - 1] != -1:  # select 한 것이 Goal 일 때 (마지막 열까지 queen이 다 놓인 경우)
                for i in range(n):
                    queens[i] += 1  # 편의상 index로 계산했기 때문에 행 시작번호를 0에서 1로 변경
                answer = " ".join(map(str, queens))  # 리스트를 문자열로 변환 및 출력형식 맞추기
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
    def calculate(queens):  # 현재 상태의 h값 계산
        h = 0
        for col, row in enumerate(queens):
            if col == n - 1:
                break
            for tmpCol, tmpRow in enumerate(queens):
                if tmpCol > col:
                    if row == tmpRow or abs(tmpCol - col) == abs(tmpRow - row):
                        h += 1
        return h

    f = open(str(n) + '_hc_output.txt', 'w')

    if n == 1:
        f.write('1')
        f.close()
    elif n < 4:
        f.write('no solution')
        f.close()
    else:
        while True:
            queens = []
            for i in range(n):  # 각 열마다 랜덤한 위치에 queen 생성
                queens.append(random.randrange(n))

            for move in range(4):  # 8-queens의 경우 약 4회의 움직임으로 해를 찾을 확률이 높아서 4회의 움직임으로 설정
                h = calculate(queens)  # 현재 상태의 h 계산
                hBoard = [[n * 3] * n for i in range(n)]  # 더 작은 h값을 찾기 위한 체스판(처음에는 가질 수 있는 h값의 최대인 h*3으로 초기화)
                for col in range(n):
                    for row in range(n):
                        tmp = queens[:]
                        tmp[col] = row
                        hBoard[row][col] = calculate(
                            tmp)  # queen을 이동했을 때 h값 계산하여 hBoard에 기록(queen을 움직였을 때 가장 작은 h를 찾기 위함)

                        if hBoard[row][col] == 0:
                            for i in range(n):
                                tmp[i] += 1  # 편의상 index로 계산했기 때문에 행 시작번호를 0에서 1로 변경
                            answer = " ".join(map(str, tmp))  # 리스트를 문자열로 변환 및 출력형식 맞추기
                            f.write(answer)
                            f.close()
                            return

                for col, row in enumerate(queens):
                    hBoard[row][col] = n * 3  # 현재 놓여있는 queen들의 위치를 구분하기 위해 가질 수 있는 h의 최대값을 넣어 선택하지 않게 함.

                minH = min(map(min, hBoard))  # hBoard에서 가장 작은 h값 구하기
                minPosList = []  # 가장 작은 h값이 여러개일 수 있으므로 리스트에 넣음
                for row, lis in enumerate(hBoard):
                    for col, tmpH in enumerate(lis):
                        if tmpH == minH:
                            minPosList.append((row, col))
                tmpIndex = random.randint(0, len(minPosList) - 1)  # 가장 작은 h값들 중 1개를 랜덤으로 선택
                tmpRow, tmpCol = minPosList[tmpIndex]

                if minH > h:  # 가장 작은 h값이 현재의 h값보다 클 경우(local maximum) 처음부터 랜덤한 위치에 queen 생성부터 반복
                    break
                queens[tmpCol] = tmpRow  # 가장 작은 h값으로 queen 이동


def csp(n):
    def forwardChecking(col, queens, answer):
        for row in queens[col]:  # 현재 열에서 놓을 수 있는 queen의 행
            if col == len(queens[0]) - 1:  # 마지막 열일 경우, empty가 아니면 성공
                answer.append(row)  # Backtracking 하면서 해 넣기(역순으로 들어감)
                return True

            tmpQueens = [item[:] for item in queens]  # Backtracking을 위해 현재 상태 보존하기 위함

            # queen을 둘 수 없는 곳 check
            for tmpCol in range(col + 1, n):
                diff = abs(tmpCol - col)

                # 대각 위
                if row - diff in tmpQueens[tmpCol]:
                    tmpQueens[tmpCol].remove(row - diff)

                # 같은 행
                if row in tmpQueens[tmpCol]:
                    tmpQueens[tmpCol].remove(row)

                # 대각 아래
                if row + diff in tmpQueens[tmpCol]:
                    tmpQueens[tmpCol].remove(row + diff)

                # Empty가 있으면 탐색 종료
                if not tmpQueens[tmpCol]:
                    return False

            success = forwardChecking(col + 1, tmpQueens, answer)
            if success:  # 해를 찾은 경우
                answer.append(row)  # Backtraking 하면서 해 넣기(역순으로 들어감)
                return True

        return False  # 해 발견 x

    f = open(str(n) + '_csp_output.txt', 'w')

    if n == 1:
        f.write('1')
        f.close()
    elif n < 4:
        f.write('no solution')
        f.close()
    else:
        queens = []
        for i in range(n):  # forward checking을 하기 위해 variable마다 모든 domain 표시
            queens.append([i for i in range(n)])  # ex) x1 = queens[0] = [0, 1, 2, ~ , N-1] (편의상 0부터 시작)

        tmp = []
        forwardChecking(0, queens, tmp)  # forward checking을 사용한 Backtracking
        tmp = tmp[::-1]  # Backtracking으로 인해 리스트에 거꾸로 추가되었으므로 순서 뒤집기

        for i in range(n):
            tmp[i] += 1  # 편의상 index로 계산했기 때문에 행 시작번호를 0에서 1로 변경
        answer = " ".join(map(str, tmp))  # 리스트를 문자열로 변환 및 출력형식 맞추기
        f.write(answer)
        print(answer)
        f.close()


if __name__ == '__main__':
    f = open('input.txt', 'r')
    for i in f:
        tmp = i.strip().split()
        func = tmp[1]
        N = int(tmp[0])

        if N < 1:
            print('Input number error(N =', N)
        if func == 'bfs':
            bfs(N)
        elif func == 'hc':
            hc(N)
        elif func == 'csp':
            csp(N)
        else:
            print('Input function error(func =', func)
    f.close()
