import streamlit as st
import re

# --- 페이지 설정 및 스타일 ---
st.set_page_config(page_title="서논술형 자동 채점 시스템", layout="wide")
st.title("📝 2회 시험 대비 서논술형 자동 채점 시스템")
st.markdown("---")

# --- 유틸리티 채점 함수 정의 ---
def check_keywords_any(text, keywords):
    """지정된 키워드나 유사 표현 중 하나라도 포함되어 있는지 검사 (의미 기반 매칭)"""
    return any(kw in text.replace(" ", "") for kw in keywords)

def check_keywords_all(text, keywords):
    """지정된 필수 키워드가 모두 포함되어 있는지 검사 (결론 및 연출 호응 검증)"""
    return all(kw in text.replace(" ", "") for kw in keywords)

def extract_method_and_strip(text):
    """문장 끝 괄호에서 설명 방법을 추출하고 괄호 제거된 문장 반환"""
    match = re.search(r"\((정의|예시|인과|분석|비교와 대조|비교|대조|분류와 구분|분류|구분)\)\s*$", text)
    if match:
        method = match.group(1)
        # 괄호 부분 제거
        clean_text = re.sub(r"\((정의|예시|인과|분석|비교와 대조|비교|대조|분류와 구분|분류|구분)\)\s*$", "", text).strip()
        return method, clean_text
    return None, text.strip()

def verify_method_marker(method, text):
    """설명 방법 명칭에 맞는 구조 표지(형식 특성)가 문장에 실제로 드러나는지 확인"""
    markers = {
        "정의": ["란", "은", "는", "말한다", "이다"],
        "예시": ["예를들어", "예로는", "예가", "등이있다", "예시"],
        "인과": ["때문에", "하여서", "결과", "원인", "로인해"],
        "분석": ["이루어져", "구성", "요소", "부분으로"],
        "비교와 대조": ["반면", "달리", "차이", "공통", "비교", "대조"],
        "비교": ["공통", "마찬가지", "같다"],
        "대조": ["반면", "달리", "차이"],
        "분류와 구분": ["나뉘", "묶이", "기준에", "종류"]
    }
    target_markers = markers.get(method, [])
    return any(marker in text.replace(" ", "") for marker in target_markers)


# --- 사이드바: 세트 선택 ---
set_choice = st.sidebar.selectbox(
    "채점할 문항 세트를 선택하세요",
    ["[세트 1] 과제 난이도에 따른 학습 전략", 
     "[세트 2] 겨울철 불청객 '정전기'의 특징", 
     "[세트 3] 인공 지능 그림을 바라보는 시각"]
)

# ==========================================
# [세트 1] 과제 난이도에 따른 학습 전략
# ==========================================
if set_choice == "[세트 1] 과제 난이도에 따른 학습 전략":
    st.header("📚 [세트 1] 과제 난이도에 따른 학습 전략 채점")
    
    tab1, tab2, tab3 = st.tabs(["[서·논술형 1] 표 빈칸 채우기", "[서·논술형 2] 설명문 작성", "[서·논술형 3] 영상 기획안 및 효과"])
    
    with tab1:
        st.subheader("📌 [서·논술형 1] 표 빈칸 채우기")
        ans_1_g = st.text_input("㉠ 입력 (과제의 특성):", placeholder="예: 비교적 쉬운 과제")
        ans_1_n = st.text_input("㉡ 입력 (효율적인 환경 및 방법):", placeholder="예: 차분하게 혼자 집중하는 시간을 가짐")
        ans_1_d = st.text_input("㉢ 입력 (관련된 심리 현상):", placeholder="예: 사회적 억제")
        
        if st.button("㉠~㉢ 채점하기"):
            score = 0
            feedback = []
            
            # ㉠ 채점
            if check_keywords_any(ans_1_g, ["쉽", "노력이필요없는", "친숙", "수월"]):
                if check_keywords_any(ans_1_g, ["어려운", "도전적인"]):
                    feedback.append("㉠ 오답: 오개념 감지 (쉬운 과제 설명에 어려운 과제 특성 유입)")
                else:
                    score += 2
                    feedback.append("㉠ 정답 (+2점): 유사 표현 및 난이도 특성 반영 확인")
            else:
                feedback.append("㉠ 오답 (0점): '쉽다/친숙하다'의 의미적 핵심 키워드 결여")
                
            # ㉡ 채점
            if check_keywords_all(ans_1_n, ["혼자"]) and check_keywords_any(ans_1_n, ["집중", "차분"]):
                if "함께" in ans_1_n or "모임" in ans_1_n:
                    feedback.append("㉡ 오답: 오개념 감지 (혼자 집중하는 환경에 타인 협동 요소 유입)")
                else:
                    score += 2
                    feedback.append("㉡ 정답 (+2점): 결론 방향성(혼자 + 집중) 확인")
            else:
                feedback.append("㉡ 오답 (0점): 필수 조건('혼자' 및 '집중/차분') 누락")
                
            # ㉢ 채점
            if ans_1_d.replace(" ", "") in ["사회적억제", "사회적억제현상"]:
                score += 2
                feedback.append("㉢ 정답 (+2점): 정확한 용어 매칭 확인")
            else:
                feedback.append("㉢ 오답 (0점): 학술 용어 불일치")
                
            st.metric("최종 점수", f"{score} / 6 점")
            for fb in feedback:
                st.write(fb)
                
    with tab2:
        st.subheader("📌 [서·논술형 2] 설명문 작성")
        ans_2_1 = st.text_input("(1) 첫 번째 문장 입력:")
        ans_2_2 = st.text_input("(2) 두 번째 문장 입력:")
        
        if st.button("문장 채점하기"):
            m1, text1 = extract_method_and_strip(ans_2_1)
            m2, text2 = extract_method_and_strip(ans_2_2)
            
            if not m1 or not m2:
                st.error("❌ 조건 위반: 문장 끝 괄호 안에 설명 방법 명칭을 정확히 기재하세요. (예: (예시))")
            elif m1 == m2:
                st.error("❌ 조건 위반 (0점 처리): 두 문장에 서로 동일한 설명 방법을 중복 사용했습니다.")
            else:
                score = 0
                fb = []
                # 1번 문장 검증
                if verify_method_marker(m1, text1):
                    score += 2
                    fb.append(f"(1)문장 정답 (+2점): 선택한 [{m1}]의 서술 구조적 특징 확인.")
                else:
                    fb.append(f"(1)문장 오답 (0점): 괄호에는 [{m1}]을 적었으나 문장에 구조적 표지 결여.")
                    
                # 2번 문장 검증
                if verify_method_marker(m2, text2):
                    score += 2
                    fb.append(f"(2)문장 정답 (+2점): 선택한 [{m2}]의 서술 구조적 특징 확인.")
                else:
                    fb.append(f"(2)문장 오답 (0점): 괄호에는 [{m2}]을 적었으나 문장에 구조적 표지 결여.")
                
                # 외부 지식 차단 확인
                if check_keywords_any(text1 + text2, ["뇌과학", "호르몬", "도파민", "스트레스"]):
                    score = 0
                    fb.append("🚨 전면 오답 처리 (0점): 지문에 없는 외부 배경지식이 검출되었습니다.")
                    
                st.metric("최종 점수", f"{score} / 4 점")
                for f in fb: st.write(f)
                
                st.markdown("💡 **선택지별 모범 답안 예시**")
                st.info("**예시+대조 조합:**\n(1) 예를 들어 친숙한 과목을 공부할 때는 도서관에서 타인과 함께하는 것이 효과적이다. (예시)\n(2) 이와 달리 어려운 과제는 차분하게 혼자 집중하는 시간을 가져야 효율적이다. (비교와 대조)")

    with tab3:
        st.subheader("📌 [서·논술형 3] 영상 기획안 및 효과")
        vis_ans = st.text_area("시각 요소 Ⓐ 연출 계획 및 효과 서술:")
        aud_ans = st.text_area("청각 요소 Ⓑ 연출 계획 및 효과 서술:")
        
        if st.button("기획안 채점하기"):
            score = 0
            fb = []
            
            # 시각 요소 채점 (총 3점: 연출 1점, 효과 2점)
            if check_keywords_any(vis_ans, ["혼자", "독서실", "방안", "1인"]):
                score += 1
                fb.append("Ⓐ 연출 계획 정답 (+1점): '어려운 과제'에 알맞은 독립 공간 시각화 확인.")
                if check_keywords_all(vis_ans, ["어려운과제"]) and check_keywords_any(vis_ans, ["집중", "차분"]):
                    score += 2
                    fb.append("Ⓐ 효과 서술 정답 (+2점): 본문에 기반한 환경적 특성 근거 매칭 완료.")
                else:
                    fb.append("Ⓐ 효과 서술 감점 (0점): 본문 근거('어려운 과제', '집중') 누락 또는 주관적 기술.")
            else:
                fb.append("Ⓐ 시각 요소 전면 오답 (0점): 혼자 있는 차분한 환경적 특성 연출 결여.")
                
            # 청각 요소 채점 (총 3점: 연출 1점, 효과 2점)
            if check_keywords_any(aud_ans, ["무음", "조용한", "고요", "잔잔", "소거"]):
                score += 1
                fb.append("Ⓑ 연출 계획 정답 (+1점): 청각적 자극을 최소화한 조용한 분위기 연출 확인.")
                if check_keywords_any(aud_ans, ["차분", "소음차단", "집중"]):
                    score += 2
                    fb.append("Ⓑ 효과 서술 정답 (+2점): 본문에 근거한 청각 연출 효과 호응 확인.")
                else:
                    fb.append("Ⓑ 효과 서술 감점 (0점): 차분함과 집중 관련 본문 핵심 근거 누락.")
            else:
                fb.append("Ⓑ 청각 요소 전면 오답 (0점): 고요하고 정형화된 분위기 조성 소리 연출 결여.")
                
            st.metric("최종 점수", f"{score} / 6 점")
            for f in fb: st.write(f)


# ==========================================
# [세트 2] 겨울철 불청객 '정전기'의 특징
# ==========================================
elif set_choice == "[세트 2] 겨울철 불청객 '정전기'의 특징":
    st.header("⚡ [세트 2] 겨울철 불청객 '정전기'의 특징 채점")
    
    tab1, tab2, tab3 = st.tabs(["[서·논술형 1] 표 빈칸 채우기", "[서·논술형 2] 설명문 작성", "[서·논술형 3] 영상 기획안 및 효과"])
    
    with tab1:
        st.subheader("📌 [서·논술형 1] 표 빈칸 채우기")
        ans_2_g = st.text_input("㉠ 입력 (물의 상태 비유):", placeholder="예: 고여 있는 물")
        ans_2_n = st.text_input("㉡ 입력 (전하의 상태):", placeholder="예: 전하가 이동하지 않고 머물러 있음")
        ans_2_d = st.text_input("㉢ 입력 (위험성):", placeholder="예: 위험하지 않음")
        
        if st.button("정전기 표 채점"):
            score = 0
            fb = []
            
            if check_keywords_any(ans_2_g, ["고여있는물", "고인물"]):
                score += 2
                fb.append("㉠ 정답 (+2점): 정전기의 비유적 표현 일치.")
            else:
                fb.append("㉠ 오답 (0점): '고여 있는 물' 의미 미포함.")
                
            if check_keywords_any(ans_2_n, ["이동하지않", "머물러", "정지"]):
                if "이동함" in ans_2_n.replace(" ", "") and "않" not in ans_2_n:
                    fb.append("㉡ 오답: 오개념 감지 (실생활 전하의 이동 특성을 기재)")
                else:
                    score += 2
                    fb.append("㉡ 정답 (+2점): 정지 전하 특성 의미 매칭 완료.")
            else:
                fb.append("㉡ 오답 (0점): '이동하지 않고 머무름' 개념 누락.")
                
            if check_keywords_any(ans_2_d, ["위험하지않", "피해가없", "안전"]):
                score += 2
                fb.append("㉢ 정답 (+2점): 위험성 결론 방향성 일치.")
            else:
                fb.append("㉢ 오답 (0점): 위험하지 않다는 명확한 결론 누락.")
                
            st.metric("최종 점수", f"{score} / 6 점")
            for f in fb: st.write(f)

    with tab2:
        st.subheader("📌 [서·논술형 2] 설명문 작성")
        ans_2_txt1 = st.text_input("(1) 첫 문장 입력:")
        ans_2_txt2 = st.text_input("(2) 두 문장 입력:")
        
        if st.button("정전기 설명문 채점"):
            m1, text1 = extract_method_and_strip(ans_2_txt1)
            m2, text2 = extract_method_and_strip(ans_2_txt2)
            
            if check_keywords_any(text1 + text2, ["마찰", "건조", "습도", "옷"]):
                st.error("🚨 전면 오답 처리 (0점): 조건 위반! 지문에 제시되지 않은 과학적 배경지식(마찰, 습도 등)이 사용되었습니다.")
            elif m1 == m2:
                st.error("❌ 조건 위반: 설명 방법 중복 허용 불가.")
            elif not m1 or not m2:
                st.error("❌ 조건 위반: 각 문장 끝에 사용한 설명 방법을 괄호 안에 기재하세요.")
            else:
                score = 0
                fb = []
                if verify_method_marker(m1, text1): score += 2; fb.append(f"(1)문장 [{m1}] 표지 통과 (+2점)")
                else: fb.append(f"(1)문장 [{m1}] 명칭-서술 불일치 (0점)")
                
                if verify_method_marker(m2, text2): score += 2; fb.append(f"(2)문장 [{m2}] 표지 통과 (+2점)")
                else: fb.append(f"(2)문장 [{m2}] 명칭-서술 불일치 (0점)")
                
                st.metric("최종 점수", f"{score} / 4 점")
                for f in fb: st.write(f)

    with tab3:
        st.subheader("📌 [서·논술형 3] 영상 기획안 및 효과")
        vis_ans = st.text_area("시각 요소 Ⓐ 연출 계획 및 효과 서술:")
        aud_ans = st.text_area("청각 요소 Ⓑ 연출 계획 및 효과 서술:")
        
        if st.button("정전기 기획안 채점"):
            score = 0
            fb = []
            
            if check_keywords_any(vis_ans, ["고여", "멈춰", "잔잔"]):
                score += 1
                if check_keywords_any(vis_ans, ["전하가이동하지않", "머물러있", "정지 상태"]):
                    score += 2
                    fb.append("Ⓐ 시각 요소 만점 (+3점): 비유적 시각화 및 본문 근거 일치.")
                else:
                    fb.append("Ⓐ 연출은 인정되나 효과 서술에 본문 근거(전하 이동 안 함) 미비 (+1점).")
            else:
                fb.append("Ⓐ 시각 요소 오답 (0점): 흐르지 않는 고인 물의 특성 연출 누락.")
                
            if check_keywords_any(aud_ans, ["무음", "조용", "정적", "소거"]):
                score += 1
                if check_keywords_any(aud_ans, ["정(靜)", "위험하지않", "피해가없"]):
                    score += 2
                    fb.append("Ⓑ 청각 요소 만점 (+3점): 청각적 정적 연출 및 '조용하다/위험 없음' 근거 연결 성공.")
                else:
                    fb.append("Ⓑ 연출은 인정되나 효과 서술에 본문 근거(정의 한자 뜻 또는 위험 없음) 누락 (+1점).")
            else:
                fb.append("Ⓑ 청각 요소 오답 (0점): 조용하고 멈춰 있는 청각적 특성 표현 실패.")
                
            st.metric("최종 점수", f"{score} / 6 점")
            for f in fb: st.write(f)


# ==========================================
# [세트 3] 인공 지능 그림을 바라보는 시각
# ==========================================
elif set_choice == "[세트 3] 인공 지능 그림을 바라보는 시각":
    st.header("🤖 [세트 3] 인공 지능 그림을 바라보는 시각 채점")
    
    tab1, tab2, tab3 = st.tabs(["[서·논술형 1] 표 빈칸 채우기", "[서·논술형 2] 설명문 작성", "[서·논술형 3] 영상 기획안 및 세부 배점"])
    
    with tab1:
        st.subheader("📌 [서·논술형 1] 표 빈칸 채우기")
        ans_3_g = st.text_input("㉠ 입력 (올림픽 경기에 비유):", placeholder="예: 완벽하지만 감동을 주지 못하는 로봇의 피겨 스케이팅")
        ans_3_n = st.text_input("㉡ 입력 (예술로 볼 수 있는가):", placeholder="예: 감정이 없고 독자적 철학이 없으므로 예술이 아니다")
        ans_3_d = st.text_input("㉢ 입력 (예술로서의 가치):", placeholder="예: 미술계에 큰 변화를 주고 범주를 확장하는 상징적 가치")
        
        if st.button("AI 그림 표 채점"):
            score = 0
            fb = []
            
            if check_keywords_all(ans_3_g, ["로봇", "피겨"]) and check_keywords_any(ans_3_g, ["울리지", "감동", "완벽"]):
                score += 2
                fb.append("㉠ 정답 (+2점): 로봇 피겨 비유 맥락 매칭 성공.")
            else:
                fb.append("㉠ 오답 (0점): 필수 비유 요소(로봇의 실수 없는 스케이팅/감동 없음) 결여.")
                
            if check_keywords_any(ans_3_n, ["감정", "철학", "이야기"]) and check_keywords_any(ans_3_n, ["어렵", "아니다", "예술이아닌"]):
                score += 2
                fb.append("㉡ 정답 (+2점): 근거(감정/철학 없음)와 결론 방향성(예술로 보기 어려움) 동시 충족.")
            else:
                fb.append("㉡ 오답 (0점): '예술로 보기 어렵다'는 명확한 최종 결론 또는 핵심 근거 누락.")
                
            if check_keywords_any(ans_3_d, ["변화", "범주", "확장", "상징"]):
                if "낙찰가" in ans_3_d and not check_keywords_any(ans_3_d, ["변화", "범주"]):
                    fb.append("㉢ 오답: 단순 금액(낙찰가)만 적은 패턴 차단.")
                else:
                    score += 2
                    fb.append("㉢ 정답 (+2점): 본문 내용 기반 가치 규명 성공.")
            else:
                fb.append("㉢ 오답 (0점): 미술계 변화 또는 범주 확장이라는 상징적 가치 누락.")
                
            st.metric("최종 점수", f"{score} / 6 점")
            for f in fb: st.write(f)

    with tab2:
        st.subheader("📌 [서·논술형 2] 설명문 작성")
        ans_3_txt1 = st.text_input("(1) 첫 문장 입력:")
        ans_3_txt2 = st.text_input("(2) 두 문장 입력:")
        
        if st.button("AI 그림 설명문 채점"):
            m1, text1 = extract_method_and_strip(ans_3_txt1)
            m2, text2 = extract_method_and_strip(ans_3_txt2)
            
            if m1 == m2:
                st.error("❌ 조건 위반: 동일 설명 방법 중복 불가.")
            elif not m1 or not m2:
                st.error("❌ 조건 위반: 문장 끝 괄호 안에 설명 방법 표기 필수.")
            else:
                score = 0
                fb = []
                if verify_method_marker(m1, text1): score += 2; fb.append(f"(1)문장 [{m1}] 형식 조건 통과 (+2점)")
                else: fb.append(f"(1)문장 [{m1}] 명칭-실제 서술 불일치 (0점)")
                
                if verify_method_marker(m2, text2): score += 2; fb.append(f"(2)문장 [{m2}] 형식 조건 통과 (+2점)")
                else: fb.append(f"(2)문장 [{m2}] 명칭-실제 서술 불일치 (0점)")
                
                if check_keywords_any(text1 + text2, ["미학", "포스트모더니즘", "개념미술"]):
                    score = 0
                    fb.append("🚨 전면 오답 처리 (0점): 외부 미학 이론 기재 확인.")
                    
                st.metric("최종 점수", f"{score} / 4 점")
                for f in fb: st.write(f)

    with tab3:
        st.subheader("📌 [서·논술형 3] 영상 기획안 정밀 세부 배점 채점 (총 6점)")
        vis_plan = st.text_input("시각 요소 Ⓐ 연출 계획 입력 (1점 배점):")
        vis_eff = st.text_input("시각 요소 Ⓐ 연출 효과 서술 입력 (2점 배점):")
        aud_plan = st.text_input("청각 요소 Ⓑ 연출 계획 입력 (1점 배점):")
        aud_eff = st.text_input("청각 요소 Ⓑ 연출 효과 서술 입력 (2점 배점):")
        
        if st.button("기획안 정밀 세부 채점 실행"):
            total_score = 0.0
            fb = []
            
            # (1) 시각 연출 계획 (1점)
            if check_keywords_any(vis_plan, ["인간", "선수", "화가", "사람"]) and check_keywords_any(vis_plan, ["땀", "노력", "열정", "고뇌", "눈물"]):
                total_score += 1.0
                fb.append("• Ⓐ 연출 계획: 만점 (+1점) - 인간의 노력 및 열정 시각화 조건 충족.")
            else:
                fb.append("• Ⓐ 연출 계획: 오답 (0점) - 인간 선수의 땀/노력적 요소 누락.")
                
            # (2) 시각 연출 효과 (2점)
            if check_keywords_any(vis_eff, ["감정", "철학", "경험", "관점", "인간의예술"]):
                total_score += 2.0
                fb.append("• Ⓐ 연출 효과: 만점 (+2점) - 고유한 감정/철학 등 본문 근거 정확히 연결.")
            else:
                fb.append("• Ⓐ 연출 효과: 오답 (0점) - 본문 근거 단어 누락 또는 영상미 위주의 주관적 기술.")
                
            # (3) 청각 연출 계획 (1점)
            if check_keywords_any(aud_plan, ["숨소리", "환호", "따뜻", "오케스트라", "풍부"]):
                total_score += 1.0
                fb.append("• Ⓑ 연출 계획: 만점 (+1점) - 기계음과 대조되는 인간적/따뜻한 소리 설계 확인.")
            else:
                fb.append("• Ⓑ 연출 계획: 오답 (0점) - 메트로놈과 대조되는 청각 요소 누락.")
                
            # (4) 청각 연출 효과 (2점)
            if check_keywords_any(aud_eff, ["울림", "감동"]):
                total_score += 2.0
                fb.append("• Ⓑ 연출 효과: 만점 (+2점) - 마음에 주는 울림과 남다른 감동 본문 문구 매칭 완료.")
            else:
                fb.append("• Ⓑ 연출 효과: 오답 (0점) - '울림/감동' 결론 방향성 누락.")
                
            st.metric("최종 정밀 점수", f"{total_score} / 6.0 점")
            for f in fb: st.write(f)