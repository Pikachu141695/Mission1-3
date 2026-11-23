import json # JSON 파일 읽기/쓰기용 라이브러리, 데이터 로드에 사용
import time # 연산 시간 측정용 라이브러리, 성능 분석에 필수
import os # 파일 경로 처리용 라이브러리, 파일 존재 확인에 사용

EPSILON = 1e-9 # 부동소수점 비교 허용오차, 동점 판정에 사용

def normalize_label(label): # 라벨 표준화 함수, 다양한 입력 형식을 통일하기 위함
    if isinstance(label, str): # 문자열인지 확인, 타입 검증
        label = label.strip().lower() # 공백 제거 및 소문자 변환, 정규화 전처리
    if label == '+' or label == 'cross': # '+' 또는 'cross' 입력 처리, 십자가 패턴 통일
        return 'Cross' # 표준 라벨로 변환
    elif label == 'x': # 'x' 입력 처리, X 패턴 통일
        return 'X' # 표준 라벨로 변환
    return None # 인식 불가 라벨 반환

def mac_operation(pattern, filter_matrix): # MAC 연산 함수, 패턴과 필터의 유사도 계산
    score = 0.0 # 누적 점수 초기화, 연산 결과 저장용
    n = len(pattern) # 패턴 크기 확인, 반복 범위 설정
    for i in range(n): # 행 반복, 각 행을 순회
        for j in range(n): # 열 반복, 각 열을 순회
            score += pattern[i][j] * filter_matrix[i][j] # 위치별 곱셈 및 누적, MAC 연산의 핵심
    return score # 최종 점수 반환

def measure_mac_time(pattern, filter_matrix, repeat=10): # MAC 연산 시간 측정 함수, 성능 분석용
    times = [] # 측정값 저장 리스트, 여러 번 반복 측정용
    for _ in range(repeat): # 반복 측정 루프, 편차 감소 목적
        start = time.time() # 시작 시간 기록, 정확한 측정용
        mac_operation(pattern, filter_matrix) # MAC 연산 실행
        end = time.time() # 종료 시간 기록, 소요 시간 계산용
        times.append((end - start) * 1000) # ms 단위로 변환 및 저장, 가독성 향상
    return sum(times) / len(times) # 평균 시간 계산 및 반환

def get_3x3_input(): # 3×3 필터/패턴 입력 함수, 사용자 모드 1에서 사용
    while True: # 입력 재시도 루프, 오류 처리용
        lines = [] # 입력값 저장 리스트, 파싱 전 임시 저장
        for i in range(3): # 3행 입력받음, 3×3 크기 고정
            line = input() # 사용자 입력 받음, 한 행씩 처리
            try: # 파싱 오류 처리, 안전한 입력 처리
                values = [float(x) for x in line.split()] # 공백 구분 파싱, 숫자 변환
                if len(values) != 3: # 열 개수 검증, 3×3 크기 확인
                    raise ValueError # 오류 발생, 재입력 유도
                lines.append(values) # 유효한 행 저장
            except (ValueError, IndexError): # 파싱/인덱싱 오류 처리
                print("입력 형식 오류: 각 줄에 3개의 숫자를 공백으로 구분해 입력하세요.") # 오류 메시지 출력
                return get_3x3_input() # 재귀적 재입력, 사용자 편의성
        return lines # 유효한 입력 반환

def load_json_data(filepath): # JSON 데이터 로드 함수, 모드 2 데이터 처리
    try: # 파일 접근 오류 처리, 안전한 로드
        with open(filepath, 'r') as f: # 파일 읽기 모드 오픈, 경로 지정
            return json.load(f) # JSON 파싱 및 반환, 딕셔너리 형태
    except FileNotFoundError: # 파일 없음 오류 처리
        print(f"오류: {filepath} 파일을 찾을 수 없습니다.") # 에러 메시지 출력
        return None # None 반환, 호출자가 처리
    except json.JSONDecodeError: # JSON 형식 오류 처리
        print(f"오류: {filepath} JSON 형식이 올바르지 않습니다.") # 형식 오류 메시지
        return None # None 반환

def mode1_user_input(): # 모드 1: 사용자 입력 처리 함수
    print("#---------------------------------------") # 구분선 출력
    print("# [1] 필터 입력") # 단계 표시
    print("#---------------------------------------") # 구분선 출력
    print("필터 A (3줄 입력, 공백 구분)") # 필터 A 입력 안내
    filter_a = get_3x3_input() # 필터 A 입력받음

    print("\n필터 B (3줄 입력, 공백 구분)") # 필터 B 입력 안내
    filter_b = get_3x3_input() # 필터 B 입력받음

    print("\n#---------------------------------------") # 구분선 출력
    print("# [2] 패턴 입력") # 단계 표시
    print("#---------------------------------------") # 구분선 출력
    print("패턴 (3줄 입력, 공백 구분)") # 패턴 입력 안내
    pattern = get_3x3_input() # 패턴 입력받음

    print("\n#---------------------------------------") # 구분선 출력
    print("# [3] MAC 결과") # 단계 표시
    print("#---------------------------------------") # 구분선 출력

    score_a = mac_operation(pattern, filter_a) # 필터 A와의 점수 계산
    score_b = mac_operation(pattern, filter_b) # 필터 B와의 점수 계산
    avg_time = measure_mac_time(pattern, filter_a) # 성능 측정 (필터 A 기준)

    print(f"A 점수: {score_a}") # A 점수 출력
    print(f"B 점수: {score_b}") # B 점수 출력
    print(f"연산 시간(평균/10회): {avg_time:.3f} ms") # 평균 연산 시간 출력

    if abs(score_a - score_b) < EPSILON: # 동점 판정 (epsilon 기반)
        result = "판정 불가 (동점)" # 동점 메시지
    elif score_a > score_b: # A가 더 높은지 확인
        result = "A" # A 판정
    else: # 그 외
        result = "B" # B 판정

    print(f"판정: {result}") # 최종 판정 출력

def mode2_json_analysis(): # 모드 2: JSON 데이터 분석 함수
    json_path = os.path.join(os.path.dirname(__file__), 'data.json') # JSON 파일 경로 설정, 스크립트 디렉토리 기준
    data = load_json_data(json_path) # JSON 데이터 로드

    if data is None: # 로드 실패 처리
        return # 함수 종료

    print("#---------------------------------------") # 구분선 출력
    print("# [1] 필터 로드") # 단계 표시
    print("#---------------------------------------") # 구분선 출력

    filters = {} # 필터 저장 딕셔너리, 크기별 저장
    for size_key in ['size_5', 'size_13', 'size_25']: # 각 크기 필터 처리, 반복
        if size_key in data['filters']: # 필터 존재 확인
            filter_dict = {} # 라벨별 필터 저장, 정규화된 라벨 사용
            for label_key, filter_matrix in data['filters'][size_key].items(): # 각 라벨의 필터 처리
                normalized = normalize_label(label_key) # 라벨 정규화
                if normalized: # 유효한 라벨 확인
                    filter_dict[normalized] = filter_matrix # 정규화된 라벨로 저장
            filters[size_key] = filter_dict # 크기별 필터 저장
            labels = ', '.join(filter_dict.keys()) # 라벨 목록 생성
            print(f"✓ {size_key}  필터 로드 완료 ({labels})") # 로드 완료 메시지

    print("\n#---------------------------------------") # 구분선 출력
    print("# [2] 패턴 분석 (라벨 정규화 적용)") # 단계 표시
    print("#---------------------------------------") # 구분선 출력

    test_results = [] # 테스트 결과 저장 리스트, 최종 리포트용
    performance_data = {} # 성능 데이터 저장, 크기별 시간 측정

    for pattern_key, pattern_data in data['patterns'].items(): # 각 패턴 처리
        size_match = None # 크기 추출용 변수
        for size_key in ['size_25', 'size_13', 'size_5', 'size_3']: # 크기 역순 확인 (긴 문자 먼저)
            if size_key in pattern_key: # 패턴 키에 크기 포함 확인
                size_match = size_key # 크기 저장
                break # 첫 매칭으로 종료

        if size_match is None or size_match not in filters: # 크기 불일치 처리
            test_results.append({'key': pattern_key, 'status': 'FAIL', 'reason': '크기 불일치'}) # FAIL 기록
            print(f"- -- {pattern_key} ---") # 패턴 키 출력
            print("FAIL (크기 불일치)") # FAIL 메시지
            continue # 다음 패턴으로

        input_pattern = pattern_data['input'] # 입력 패턴 추출
        expected = normalize_label(pattern_data['expected']) # expected 라벨 정규화

        if expected is None: # 유효하지 않은 라벨 처리
            test_results.append({'key': pattern_key, 'status': 'FAIL', 'reason': '유효하지 않은 라벨'}) # FAIL 기록
            print(f"- -- {pattern_key} ---") # 패턴 키 출력
            print("FAIL (유효하지 않은 라벨)") # FAIL 메시지
            continue # 다음 패턴으로

        print(f"- -- {pattern_key} ---") # 패턴 키 출력

        filter_dict = filters[size_match] # 해당 크기의 필터 가져옴
        scores = {} # 각 라벨별 점수 저장, 비교용
        for label in ['Cross', 'X']: # 각 라벨에 대해 처리
            if label in filter_dict: # 필터 존재 확인
                score = mac_operation(input_pattern, filter_dict[label]) # MAC 연산
                scores[label] = score # 점수 저장
                print(f"{label} 점수: {score}") # 점수 출력

        if 'Cross' in scores and 'X' in scores: # 두 점수 모두 존재 확인
            score_cross = scores['Cross'] # Cross 점수
            score_x = scores['X'] # X 점수

            if abs(score_cross - score_x) < EPSILON: # 동점 판정
                decision = 'UNDECIDED' # 판정 불가
            elif score_cross > score_x: # Cross가 더 높은지 확인
                decision = 'Cross' # Cross 판정
            else: # 그 외
                decision = 'X' # X 판정
        else: # 한쪽 점수 누락
            decision = 'UNDECIDED' # 판정 불가

        pass_fail = 'PASS' if decision == expected else 'FAIL' # PASS/FAIL 판정
        reason = None if pass_fail == 'PASS' else f"판정={decision}, 예상={expected}" # 실패 사유

        print(f"판정: {decision} | expected: {expected} | {pass_fail}") # 결과 출력

        test_results.append({'key': pattern_key, 'status': pass_fail, 'reason': reason}) # 결과 기록

        if size_match not in performance_data: # 성능 데이터 초기화
            performance_data[size_match] = [] # 리스트 생성
        avg_time = measure_mac_time(input_pattern, filter_dict.get('Cross', filter_dict.get('X'))) # 성능 측정
        performance_data[size_match].append(avg_time) # 성능 데이터 저장

    print("\n#---------------------------------------") # 구분선 출력
    print("# [3] 성능 분석 (평균/10회)") # 단계 표시
    print("#---------------------------------------") # 구분선 출력
    print("크기       평균 시간(ms)    연산 횟수") # 표 헤더
    print("-------------------------------------") # 표 구분선

    size_order = ['size_3', 'size_5', 'size_13', 'size_25'] # 크기 순서 정의
    for size_key in size_order: # 각 크기별 출력
        if size_key in performance_data and performance_data[size_key]: # 성능 데이터 존재 확인
            n = int(size_key.split('_')[1]) # 크기 추출
            avg_time = sum(performance_data[size_key]) / len(performance_data[size_key]) # 평균 계산
            ops = n * n # 연산 횟수 계산
            print(f"{n}×{n}            {avg_time:.3f}           {ops}") # 성능 데이터 출력

    print("\n#---------------------------------------") # 구분선 출력
    print("# [4] 결과 요약") # 단계 표시
    print("#---------------------------------------") # 구분선 출력

    total = len(test_results) # 전체 테스트 수
    passed = sum(1 for r in test_results if r['status'] == 'PASS') # 통과 수
    failed = total - passed # 실패 수

    print(f"총 테스트: {total}개") # 전체 출력
    print(f"통과: {passed}개") # 통과 출력
    print(f"실패: {failed}개") # 실패 출력

    if failed > 0: # 실패 케이스 존재 확인
        print("\n실패 케이스:") # 실패 케이스 헤더
        for result in test_results: # 각 결과 순회
            if result['status'] == 'FAIL': # FAIL만 출력
                print(f"- {result['key']}: {result['reason']}") # 케이스 및 사유 출력

def main(): # 메인 함수, 프로그램 진입점
    while True: # 메인 루프, 종료 선택까지 반복
        print("\n=== Mini NPU Simulator ===\n") # 프로그램 타이틀 출력
        print("[모드 선택]\n") # 모드 선택 안내
        print("1. 사용자 입력 (3x3)") # 모드 1 설명
        print("2. data.json 분석") # 모드 2 설명
        print("0. 종료") # 종료 옵션

        while True: # 선택 입력 루프, 유효한 입력까지 반복
            choice = input("\n선택: ").strip().lstrip('﻿') # 사용자 선택 입력받음, BOM 제거
            if choice == '1': # 모드 1 선택 확인
                mode1_user_input() # 모드 1 실행
                break # 선택 루프 종료 → 메뉴로 복귀
            elif choice == '2': # 모드 2 선택 확인
                mode2_json_analysis() # 모드 2 실행
                break # 선택 루프 종료 → 메뉴로 복귀
            elif choice == '0': # 종료 선택 확인
                print("\n프로그램을 종료합니다.") # 종료 메시지
                return # 프로그램 종료
            else: # 유효하지 않은 선택
                print("0, 1, 2 중 하나를 입력하세요.") # 오류 메시지

if __name__ == '__main__': # 스크립트 직접 실행 확인, 모듈 import 시 실행 방지
    main() # 메인 함수 호출, 프로그램 시작
