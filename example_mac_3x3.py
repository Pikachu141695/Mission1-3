# 이 함수의 목적:
# - pattern(입력 패턴)과 fltr(비교 대상 필터)의 유사도를 숫자로 계산한다.
# - 과제의 핵심 개념인 MAC(Multiply-Accumulate)를 가장 작은 형태로 연습하기 위해 만든다.
# - Multiply는 같은 위치의 숫자끼리 곱하는 것이고, Accumulate는 그 결과를 계속 더하는 것이다.
def compute_mac(pattern, fltr):
    # score 변수의 목적:
    # - 각 칸에서 곱한 결과를 누적해서 최종 MAC 점수를 저장한다.
    score = 0

    # row 반복문의 목적:
    # - 3x3 리스트에서 각 행(세로 방향)을 순서대로 방문하기 위해 사용한다.
    for row in range(3):
        # col 반복문의 목적:
        # - 현재 행 안에서 각 열(가로 방향)을 순서대로 방문하기 위해 사용한다.
        for col in range(3):
            # 이 한 줄의 목적:
            # - pattern과 fltr의 같은 위치 값을 곱해서 score에 누적한다.
            # - 즉, MAC의 핵심 계산을 수행하는 가장 중요한 줄이다.
            score += pattern[row][col] * fltr[row][col]

    # return의 목적:
    # - 최종적으로 계산된 MAC 점수를 함수 바깥으로 돌려준다.
    return score


# 이 함수의 목적:
# - 2차원 리스트(행렬)를 콘솔에 보기 좋게 출력한다.
# - 디버깅하거나, 내가 입력한 데이터 모양이 맞는지 확인할 때 도움된다.
def print_matrix(name, matrix):
    # 이름을 먼저 출력하는 목적:
    # - 지금 출력하는 행렬이 Filter A인지, Filter B인지, Pattern인지 구분하기 쉽게 만든다.
    print(f"\n[{name}]")

    # 각 행을 한 줄씩 출력하는 목적:
    # - 2차원 리스트를 사람이 보기 쉬운 형태로 보여주기 위함이다.
    for row in matrix:
        print(row)


# 아래 3개의 리스트를 직접 코드에 써두는 목적:
# - 아직 사용자 입력을 받기 전에, MAC 계산 원리가 맞는지 가장 작은 예제로 먼저 검증하기 위함이다.
# - 초보자는 입력 처리와 계산 로직을 동시에 만들면 헷갈리기 쉬워서,
#   먼저 "고정된 데이터로 계산이 맞는지" 확인하는 단계가 필요하다.

# filter_a의 목적:
# - A라는 기준 패턴 역할을 하는 3x3 필터다.
# - 현재 예제에서는 대각선과 가운데가 1인 모양으로 두었다.
filter_a = [
    [1, 0, 1],
    [0, 1, 0],
    [1, 0, 1]
]

# filter_b의 목적:
# - A와 다른 모양을 가진 비교 대상 필터를 하나 더 만들기 위함이다.
# - 이렇게 해야 같은 pattern을 두 필터와 비교해서 어느 쪽이 더 비슷한지 확인할 수 있다.
filter_b = [
    [0, 1, 0],
    [1, 0, 1],
    [0, 1, 0]
]

# pattern의 목적:
# - 실제로 분류 대상이 되는 입력 패턴이다.
# - 현재는 filter_a와 같은 모양으로 두어서, A 점수가 더 크게 나오도록 예제를 구성했다.
pattern = [
    [1, 0, 1],
    [0, 1, 0],
    [1, 0, 1]
]


# 제목을 출력하는 목적:
# - 이 프로그램이 무엇을 실행하는지 시작부터 바로 알 수 있게 한다.
print("=== 3x3 MAC 연산 작은 예제 ===")

# 각 행렬을 출력하는 목적:
# - 계산 전에 데이터 모양을 직접 눈으로 확인할 수 있게 한다.
print_matrix("Filter A", filter_a)
print_matrix("Filter B", filter_b)
print_matrix("Pattern", pattern)

# score_a 계산의 목적:
# - pattern이 Filter A와 얼마나 비슷한지 숫자로 구한다.
score_a = compute_mac(pattern, filter_a)

# score_b 계산의 목적:
# - pattern이 Filter B와 얼마나 비슷한지 숫자로 구한다.
score_b = compute_mac(pattern, filter_b)

# 점수 출력의 목적:
# - 어떤 필터와의 점수가 더 큰지 사람이 바로 비교할 수 있도록 보여준다.
print(f"\nFilter A MAC score: {score_a}")
print(f"Filter B MAC score: {score_b}")

# 아래 조건문의 목적:
# - 두 점수를 비교해서 어떤 필터가 더 유사한지 판정한다.
# - 점수가 더 큰 쪽이 더 비슷한 패턴이라고 해석한다.
if score_a > score_b:
    print("판정 결과: A")
elif score_b > score_a:
    print("판정 결과: B")
else:
    # 점수가 같다면 한쪽이 더 낫다고 말하기 어려우므로 UNDECIDED를 출력한다.
    print("판정 결과: UNDECIDED")
