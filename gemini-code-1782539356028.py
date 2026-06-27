import streamlit as st
import re

# --- 페이지 설정 및 스타일 ---
st.set_page_config(page_title="서논술형 자동 채점 시스템", layout="wide")
st.title("📝 2회 시험 대비 서논술형 자동 채점 시스템 (오답노트 기능 추가)")
st.markdown("---")

# --- 세션 상태(Session State) 초기화 (오답 및 복습 데이터 저장용) ---
if "review_data" not in st.session_state:
    st.session_state.review_data = {
        "set1": {"q1": None, "q2": None, "q3": None},
        "set2": {"q1": None, "q2": None, "q3": None},
        "set3": {"q1": None, "q2": None, "q3": None}
    }

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
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "[서·논술형 1] 표 빈칸 채우기", 
        "[서·논술형 2] 설명문 작성", 
        "[서·논술형 3] 영상 기획안 및 효과",
        "🔍 복습할 내용"
    ])
    
    with tab1:
        st.subheader("📌 [서·논술형 1] 표 빈칸 채우기")
        ans_1_g = st.text_input("㉠ 입력 (과제의 특성):", placeholder="예: 비교적 쉬운 과제")
        ans_1_n = st.text_input("㉡ 입력 (효율적인 환경 및 방법):", placeholder="예: 차분하게 혼자 집중하는 시간을 가짐")
        ans_1_d = st.text_input("㉢ 입력 (관련된 심리 현상):", placeholder="예: 사회적 억제")
        
        if st.button("㉠~㉢ 채점하기"):
            score = 0
            feedback = []
            missing = []
            
            if check_keywords_any(ans_1_g, ["쉽", "노력이필요없는", "친숙", "수월"]):
                if check_keywords_any(ans_1_g, ["어려운", "도전적인"]):
                    missing.append("㉠ 오개념 발견: 쉬운 과제 기술 칸에 어려운 과제 특성을 혼입함.")
                else:
                    score += 2
                    feedback.append("㉠ 정답 (+2점): 유사 표현 및 난이도 특성 반영 확인.")
            else:
                missing.append("㉠ 필수 키워드 누락: '쉽다/노력이 적다'의 의미적 표현이 없음.")
                
            if check_keywords_all(ans_1_n, ["혼자"]) and check_keywords_any(ans_1_n, ["집중", "차분"]):
                if "함께" in ans_1_n or "모임" in ans_1_n:
                    missing.append("㉡ 오개념 발견: 혼자 집중해야 하는 환경에 타인 협동 요소를 유입함.")
                else:
                    score += 2
                    feedback.append("㉡ 정답 (+2점): 결론 방향성(혼자 + 집중) 일치 확인.")
            else:
                missing.append("㉡ 필수 조건 미달: '혼자' 및 '집중/차분' 조건이 동시에 충족되지 않음.")
                
            if ans_1_d.replace(" ", "") in ["사회적억제", "사회적억제현상"]:
                score += 2
                feedback.append("㉢ 정답 (+2점): 정확한 용어 매칭 확인.")
            else:
                missing.append("㉢ 필수 학술어 오류: 정확한 개념어 '사회적 억제' 미기재.")
                
            st.metric("최종 점수", f"{score} / 6 점")
            for fb in feedback: st.write(fb)
            for ms in missing: st.write(f"❌ {ms}")
            
            # 세션 상태에 저장
            st.session_state.review_data["set1"]["q1"] = {
                "title": "[서·논술형 1] 표 빈칸 채우기",
                "score": score,
                "max_score": 6,
                "missing": missing,
                "points": "과제의 난이도에 따라 학습 효율을 높이는 환경이 다릅니다. 쉬운 과제는 타인의 존재가 능률을 높이지만, 어렵고 복잡한 과제는 자극을 줄여야 합니다."
            }
                
    with tab2:
        st.subheader("📌 [서·논술형 2] 설명문 작성")
        ans_2_1 = st.text_input("(1) 첫 번째 문장 입력:")
        ans_2_2 = st.text_input("(2) 두 번째 문장 입력:")
        
        if st.button("문장 채점하기"):
            m1, text1 = extract_method_and_strip(ans_2_1)
            m2, text2 = extract_method_and_strip(ans_2_2)
            score = 0
            feedback = []
            missing = []
            
            if not m1 or not m2:
                missing.append("형식 조건 위배: 문장 끝 괄호 안에 설명 방법 명칭 기재 누락.")
            elif m1 == m2:
                missing.append("형식 조건 위배: 서로 다른 2가지 방법을 쓰지 않고 중복 사용함.")
            else:
                if verify_method_marker(m1, text1):
                    score += 2
                    feedback.append(f"(1)문장 정답 (+2점): 선택한 [{m1}]의 구조적 특징 확인.")
                else:
                    missing.append(f"(1)문장 표현 오류: 괄호에 기재한 [{m1}]의 구조적 표지(특성)가 문장 내에 드러나지 않음.")
                    
                if verify_method_marker(m2, text2):
                    score += 2
                    feedback.append(f"(2)문장 정답 (+2점): 선택한 [{m2}]의 구조적 특징 확인.")
                else:
                    missing.append(f"(2)문장 표현 오류: 괄호에 기재한 [{m2}]의 구조적 표지(특성)가 문장 내에 드러나지 않음.")
                
            if check_keywords_any(ans_2_1 + ans_2_2, ["뇌과학", "호르몬", "도파민", "스트레스"]):
                score = 0
                missing.append("지문 근거 위배: 본문에 제시되지 않은 외부 배경지식을 사용하여 전면 0점 처리됨.")
                    
            st.metric("최종 점수", f"{score} / 4 점")
            for f in feedback: st.write(f)
            for m in missing: st.write(f"❌ {m}")
            
            st.session_state.review_data["set1"]["q2"] = {
                "title": "[서·논술형 2] 설명문 작성",
                "score": score,
                "max_score": 4,
                "missing": missing,
                "points": "설명문의 문장을 구성할 때는 괄호에 적은 방법 명칭(예: 예시, 인과 등)에 부합하는 언어 표지(예를 들어, ~때문에 등)가 명확히 결합되어야 서술 방식의 특성이 드러납니다."
            }

    with tab3:
        st.subheader("📌 [서·논술형 3] 영상 기획안 및 효과")
        vis_ans = st.text_area("시각 요소 Ⓐ 연출 계획 및 효과 서술:")
        aud_ans = st.text_area("청각 요소 Ⓑ 연출 계획 및 효과 서술:")
        
        if st.button("기획안 채점하기"):
            score = 0
            missing = []
            
            if check_keywords_any(vis_ans, ["혼자", "독서실", "방안", "1인"]):
                score += 1
                if check_keywords_all(vis_ans, ["어려운과제"]) and check_keywords_any(vis_ans, ["집중", "차분"]):
                    score += 2
                else:
                    missing.append("Ⓐ 시각 효과 서술 미달: 어려운 과제를 수행할 때 필요한 본문 핵심 근거('어려운 과제', '집중')가 불명확함.")
            else:
                missing.append("Ⓐ 시각 연출 계획 오류: '어려운 과제'의 환경 특성에 부합하는 독립 공간(혼자) 연출이 드러나지 않음.")
                
            if check_keywords_any(aud_ans, ["무음", "조용한", "고요", "잔잔", "소거"]):
                score += 1
                if check_keywords_any(aud_ans, ["차분", "소음차단", "집중"]):
                    score += 2
                else:
                    missing.append("Ⓑ 청각 효과 서술 미달: 소리 연출이 집중과 차분함에 기여한다는 본문 기반 논리 연결 부족.")
            else:
                missing.append("Ⓑ 청각 연출 계획 오류: 소음을 최소화하여 정형화된 분위기를 깨뜨리는 고요한 청각적 연출 부족.")
                
            st.metric("최종 점수", f"{score} / 6 점")
            if score == 6: st.success("🎉 만점입니다!")
            for m in missing: st.write(f"❌ {m}")
            
            st.session_state.review_data["set1"]["q3"] = {
                "title": "[서·논술형 3] 영상 기획안 및 효과",
                "score": score,
                "max_score": 6,
                "missing": missing,
                "points": "복합양식성 자료를 연출할 때는 시각·청각 요소가 지문의 개념 방향과 일치해야 합니다. 어려운 과제 환경은 시각적으로 자극을 차단하고(혼자), 청각적으로 고요함을 제공해야 효율적입니다."
            }

    with tab4:
        st.subheader("🔍 세트 1 오답 노트 및 복습 가이드")
        has_review = False
        for q_key, q_val in st.session_state.review_data["set1"].items():
            if q_val and q_val["score"] < q_val["max_score"]:
                has_review = True
                with st.expander(f"⚠️ {q_val['title']} ({q_val['score']}/{q_val['max_score']}점)", expanded=True):
                    st.error("내 답안의 부족한 부분 (조건 미충족 요인)")
                    for err in q_val["missing"]:
                        st.write(f"• {err}")
                    st.info("💡 해당 개념 핵심 복습 포인트")
                    st.write(q_val["points"])
        if not has_review:
            st.success("✨ 세트 1에서 조건 미충족 혹은 오답 문제가 없습니다. 완벽합니다!")


# ==========================================
# [세트 2] 겨울철 불청객 '정전기'의 특징
# ==========================================
elif set_choice == "[세트 2] 겨울철 불청객 '정전기'의 특징":
    st.header("⚡ [세트 2] 겨울철 불청객 '정전기'의 특징 채점")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "[서·논술형 1] 표 빈칸 채우기", 
        "[서·논술형 2] 설명문 작성", 
        "[서·논술형 3] 영상 기획안 및 효과",
        "🔍 복습할 내용"
    ])
    
    with tab1:
        st.subheader("📌 [서·논술형 1] 표 빈칸 채우기")
        ans_2_g = st.text_input("㉠ 입력 (물의 상태 비유):", placeholder="예: 고여 있는 물")
        ans_2_n = st.text_input("㉡ 입력 (전하의 상태):", placeholder="예: 전하가 이동하지 않고 머물러 있음")
        ans_2_d = st.text_input("㉢ 입력 (위험성):", placeholder="예: 위험하지 않음")
        
        if st.button("정전기 표 채점"):
            score = 0
            missing = []
            
            if check_keywords_any(ans_2_g, ["고여있는물", "고인물"]):
                score += 2
            else:
                missing.append("㉠ 비유 오류: 실생활 전기(흐르는 물)와 구별되는 정전기 고유의 비유 표현('고여 있는 물') 누락.")
                
            if check_keywords_any(ans_2_n, ["이동하지않", "머물러", "정지"]):
                if "이동함" in ans_2_n.replace(" ", "") and "않" not in ans_2_n:
                    missing.append("㉡ 오개념 발견: 전하가 이동하는 것은 실생활 전기의 특징입니다.")
                else:
                    score += 2
            else:
                missing.append("㉡ 과학적 개념 누락: 정전기 전하의 핵심적 특성인 '정지/이동하지 않음' 기술 부족.")
                
            if check_keywords_any(ans_2_d, ["위험하지않", "피해가없", "안전"]):
                score += 2
            else:
                missing.append("㉢ 결론 방향성 오류: 높은 전압에도 불구하고 전하 이동이 없어 '위험하지 않다'는 명확한 결론이 드러나지 않음.")
                
            st.metric("최종 점수", f"{score} / 6 점")
            for m in missing: st.write(f"❌ {m}")
            
            st.session_state.review_data["set2"]["q1"] = {
                "title": "[서·논술형 1] 표 빈칸 채우기",
                "score": score,
                "max_score": 6,
                "missing": missing,
                "points": "정전기(靜)는 한자 뜻 그대로 '움직이지 않고 조용히 머물러 있는 전기'입니다. 전하가 이동하지 않으므로 높은 곳에 '고여 있는 물'에 비유되며, 실생활 전기와 달리 우리에게 위험을 주지 않습니다."
            }

    with tab2:
        st.subheader("📌 [서·논술형 2] 설명문 작성")
        ans_2_txt1 = st.text_input("(1) 첫 문장 입력:")
        ans_2_txt2 = st.text_input("(2) 두 문장 입력:")
        
        if st.button("정전기 설명문 채점"):
            m1, text1 = extract_method_and_strip(ans_2_txt1)
            m2, text2 = extract_method_and_strip(ans_2_txt2)
            score = 0
            missing = []
            
            if check_keywords_any(text1 + text2, ["마찰", "건조", "습도", "옷"]):
                missing.append("지문 조건 위반: 본문에 명시되지 않은 외부 과학 지식('마찰력', '습도' 등)을 가공하여 유입함.")
            elif m1 == m2:
                missing.append("형식 조건 위배: 동일한 설명 방법을 연달아 중복 사용함.")
            elif not m1 or not m2:
                missing.append("형식 조건 위배: 문장 끝 괄호 안에 정형화된 설명 방법 명칭 기재 누락.")
            else:
                if verify_method_marker(m1, text1): score += 2
                else: missing.append(f"(1)문장 불일치: 기재한 방법 [{m1}]에 걸맞은 문장 표지 구조가 드러나지 않음.")
                
                if verify_method_marker(m2, text2): score += 2
                else: missing.append(f"(2)문장 불일치: 기재한 방법 [{m2}]에 걸맞은 문장 표지 구조가 드러나지 않음.")
                
            st.metric("최종 점수", f"{score} / 4 점")
            for m in missing: st.write(f"❌ {m}")
            
            st.session_state.review_data["set2"]["q2"] = {
                "title": "[서·논술형 2] 설명문 작성",
                "score": score,
                "max_score": 4,
                "missing": missing,
                "points": "문제 조건에 '윗글에 제시된 내용만을 활용할 것'이 있다면 본인의 상식(예: 정전기는 마찰 때문에 생긴다)을 전면 배제하고 지문 속 텍스트 데이터(전하의 정지 상태, 물의 비유)만으로 문장을 엮어야 통과됩니다."
            }

    with tab3:
        st.subheader("📌 [서·논술형 3] 영상 기획안 및 효과")
        vis_ans = st.text_area("시각 요소 Ⓐ 연출 계획 및 효과 서술:")
        aud_ans = st.text_area("청각 요소 Ⓑ 연출 계획 및 효과 서술:")
        
        if st.button("정전기 기획안 채점"):
            score = 0
            missing = []
            
            if check_keywords_any(vis_ans, ["고여", "멈춰", "잔잔"]):
                score += 1
                if check_keywords_any(vis_ans, ["전하가이동하지않", "머물러있", "정지 상태"]):
                    score += 2
                else:
                    missing.append("Ⓐ 시각 효과 서술 미달: 고여 있는 물 연출이 '전하의 부이동(멈춤)'을 드러낸다는 지문 근거 연결 부족.")
            else:
                missing.append("Ⓐ 시각 연출 계획 오류: 흐르는 폭포수와 대조되는 '흐르지 않고 가만히 고인 물'의 상태 시각화 누락.")
                
            if check_keywords_any(aud_ans, ["무음", "조용", "정적", "소거"]):
                score += 1
                if check_keywords_any(aud_ans, ["정(靜)", "위험하지않", "피해가없"]):
                    score += 2
                else:
                    missing.append("Ⓑ 청각 효과 서술 미달: 고요함 연출이 '위험하지 않음/피해 없음' 또는 한자 '정(靜)'의 의미를 반영한다는 근거 누락.")
            else:
                missing.append("Ⓑ 청각 연출 계획 오류: 폭포 부딪히는 큰 소리와 대비되는 정적인 '무음/고요함'의 청각 설계 부족.")
                
            st.metric("최종 점수", f"{score} / 6 점")
            for m in missing: st.write(f"❌ {m}")
            
            st.session_state.review_data["set2"]["q3"] = {
                "title": "[서·논술형 3] 영상 기획안 및 효과",
                "score": score,
                "max_score": 6,
                "missing": missing,
                "points": "정전기 영상화의 핵심은 폭포수(실생활 전기)와의 '대조'입니다. 시각적으로는 멈춘 물을, 청각적으로는 고요함을 연출하여 전하가 머물러 있기에 피해가 없다는 결론 방향성을 확립해야 합니다."
            }

    with tab4:
        st.subheader("🔍 세트 2 오답 노트 및 복습 가이드")
        has_review = False
        for q_key, q_val in st.session_state.review_data["set2"].items():
            if q_val and q_val["score"] < q_val["max_score"]:
                has_review = True
                with st.expander(f"⚠️ {q_val['title']} ({q_val['score']}/{q_val['max_score']}점)", expanded=True):
                    st.error("내 답안의 부족한 부분 (조건 미충족 요인)")
                    for err in q_val["missing"]: st.write(f"• {err}")
                    st.info("💡 해당 개념 핵심 복습 포인트")
                    st.write(q_val["points"])
        if not has_review:
            st.success("✨ 세트 2에서 조건 미충족 혹은 오답 문제가 없습니다. 완벽합니다!")


# ==========================================
# [세트 3] 인공 지능 그림을 바라보는 시각
# ==========================================
elif set_choice == "[세트 3] 인공 지능 그림을 바라보는 시각":
    st.header("🤖 [세트 3] 인공 지능 그림을 바라보는 시각 채점")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "[서·논술형 1] 표 빈칸 채우기", 
        "[서·논술형 2] 설명문 작성", 
        "[서·논술형 3] 영상 기획안 및 세부 배점",
        "🔍 복습할 내용"
    ])
    
    with tab1:
        st.subheader("📌 [서·논술형 1] 표 빈칸 채우기")
        ans_3_g = st.text_input("㉠ 입력 (올림픽 경기에 비유):", placeholder="예: 완벽하지만 감동을 주지 못하는 로봇의 피겨 스케이팅")
        ans_3_n = st.text_input("㉡ 입력 (예술로 볼 수 있는가):", placeholder="예: 감정이 없고 독자적 철학이 없으므로 예술이 아니다")
        ans_3_d = st.text_input("㉢ 입력 (예술로서의 가치):", placeholder="예: 미술계에 큰 변화를 주고 범주를 확장하는 상징적 가치")
        
        if st.button("AI 그림 표 채점"):
            score = 0
            missing = []
            
            if check_keywords_all(ans_3_g, ["로봇", "피겨"]) and check_keywords_any(ans_3_g, ["울리지", "감동", "완벽"]):
                score += 2
            else:
                missing.append("㉠ 비유 매칭 오류: 기술은 완벽하나 마음을 울리지 못하는 '로봇의 피겨 스케이팅' 비유 속성 누락.")
                
            if check_keywords_any(ans_3_n, ["감정", "철학", "이야기"]) and check_keywords_any(ans_3_n, ["어렵", "아니다", "예술이아닌"]):
                score += 2
            else:
                missing.append("㉡ 결론 방향성 미달: '감정/철학 결여'라는 지문 속 근거와 '예술로 보기 어렵다'는 명확한 결론 구조 미비.")
                
            if check_keywords_any(ans_3_d, ["변화", "범주", "확장", "상징"]):
                if "낙찰가" in ans_3_d and not check_keywords_any(ans_3_d, ["변화", "범주"]):
                    missing.append("㉢ 오개념 발견: 단순히 높은 경매가(낙찰 대금)를 기재한 패턴 필터링 차단됨.")
                else:
                    score += 2
            else:
                missing.append("㉢ 본질적 가치 규명 오류: 본문 후반부에 명시된 '미술계 변화' 및 '예술 범주 확장(상징적 가치)' 단어 미검출.")
                
            st.metric("최종 점수", f"{score} / 6 점")
            for m in missing: st.write(f"❌ {m}")
            
            st.session_state.review_data["set3"]["q1"] = {
                "title": "[서·논술형 1] 표 빈칸 채우기",
                "score": score,
                "max_score": 6,
                "missing": missing,
                "points": "인공지능의 그림은 감정과 독자적 철학이 없어 진정한 의미의 예술로 보기는 어렵지만, 기존 미술계에 변화를 촉발하고 범주를 넓히는 '상징적 가치'를 가진다는 양면성을 명확히 인지해야 합니다."
            }

    with tab2:
        st.subheader("📌 [서·논술형 2] 설명문 작성")
        ans_3_txt1 = st.text_input("(1) 첫 문장 입력:")
        ans_3_txt2 = st.text_input("(2) 두 문장 입력:")
        
        if st.button("AI 그림 설명문 채점"):
            m1, text1 = extract_method_and_strip(ans_3_txt1)
            m2, text2 = extract_method_and_strip(ans_3_txt2)
            score = 0
            missing = []
            
            if m1 == m2:
                missing.append("형식 조건 위배: 동일한 기술 방법을 (1), (2) 문장에 중복 적용함.")
            elif not m1 or not m2:
                missing.append("형식 조건 위배: 문장 끝 명칭 괄호 표기 누락.")
            else:
                if verify_method_marker(m1, text1): score += 2
                else: missing.append(f"(1)문장 오류: 선택한 설명 방식 [{m1}]의 고유 문장 구조 표지 결여.")
                
                if verify_method_marker(m2, text2): score += 2
                else: missing.append(f"(2)문장 오류: 선택한 설명 방식 [{m2}]의 고유 문장 구조 표지 결여.")
                
            if check_keywords_any(text1 + text2, ["미학", "포스트모더니즘", "개념미술", "튜링테스트"]):
                score = 0
                missing.append("지문 외 내용 개입: 본문에 명시되지 않은 철학/미학적 외부 학술 용어를 유입하여 0점 처리됨.")
                    
            st.metric("최종 점수", f"{score} / 4 점")
            for m in missing: st.write(f"❌ {m}")
            
            st.session_state.review_data["set3"]["q2"] = {
                "title": "[서·논술형 2] 설명문 작성",
                "score": score,
                "max_score": 4,
                "missing": missing,
                "points": "논리적 흐름을 구축할 때는 앞 문장과 뒤 문장이 자연스럽게 이어지며, '인간의 예술적 요소(감정, 철학, 삶의 경험)'와 '인공지능의 한계'라는 지문 데이터가 충실하게 연계되어야 합니다."
            }

    with tab3:
        st.subheader("📌 [서·논술형 3] 영상 기획안 정밀 세부 배점 채점 (총 6점)")
        vis_plan = st.text_input("시각 요소 Ⓐ 연출 계획 입력 (1점 배점):")
        vis_eff = st.text_input("시각 요소 Ⓐ 연출 효과 서술 입력 (2점 배점):")
        aud_plan = st.text_input("청각 요소 Ⓑ 연출 계획 입력 (1점 배점):")
        aud_eff = st.text_input("청각 요소 Ⓑ 연출 효과 서술 입력 (2점 배점):")
        
        if st.button("기획안 정밀 세부 채점 실행"):
            total_score = 0.0
            missing = []
            
            if check_keywords_any(vis_plan, ["인간", "선수", "화가", "사람"]) and check_keywords_any(vis_plan, ["땀", "노력", "열정", "고뇌", "눈물"]):
                total_score += 1.0
            else:
                missing.append("Ⓐ 연출 계획 오류: 기계와 대조되는 '인간 선수의 땀, 노력, 열정, 고뇌'의 시각적 속성 묘사 부족 (0점).")
                
            if check_keywords_any(vis_eff, ["감정", "철학", "경험", "관점", "인간의예술"]):
                total_score += 2.0
            else:
                missing.append("Ⓐ 연출 효과 미달: 단순 영상미나 화려함을 기술함. 본문 근거('작가의 고유한 감정, 철학, 경험') 명시 누락 (0점).")
                
            if check_keywords_any(aud_plan, ["숨소리", "환호", "따뜻", "오케스트라", "풍부"]):
                total_score += 1.0
            else:
                missing.append("Ⓑ 연출 계획 오류: 메트로놈 소리와 대조되는 '역동적인 숨소리, 관객 환호성, 따뜻한 음악' 배치 누락 (0점).")
                
            if check_keywords_any(aud_eff, ["울림", "감동"]):
                total_score += 2.0
            else:
                missing.append("Ⓑ 연출 효과 미달: 소리 연출이 감상자의 마음에 자아내는 최종 결론 방향성('마음의 울림', '남다른 감동') 기술 부족 (0점).")
                
            st.metric("최종 정밀 점수", f"{total_score} / 6.0 점")
            for m in missing: st.write(f"❌ {m}")
            
            st.session_state.review_data["set3"]["q3"] = {
                "title": "[서·논술형 3] 영상 기획안 및 효과",
                "score": total_score,
                "max_score": 6.0,
                "missing": missing,
                "points": "진정한 예술의 가치를 영상 매체로 변환할 때는 주관적 감상('영상이 다채롭다', '세련되어 보인다')을 전면 배제해야 합니다. 지문 근거에 명시된 '인간 선수의 노력과 열정', '마음의 울림과 감동'이 연출 효과 서술에 계량적으로 연결되어야 정답 처리됩니다."
            }

    with tab4:
        st.subheader("🔍 세트 3 오답 노트 및 복습 가이드")
        has_review = False
        for q_key, q_val in st.session_state.review_data["set3"].items():
            if q_val and q_val["score"] < q_val["max_score"]:
                has_review = True
                with st.expander(f"⚠️ {q_val['title']} ({int(q_val['score'])}/{int(q_val['max_score'])}점)", expanded=True):
                    st.error("내 답안의 부족한 부분 (조건 미충족 요인)")
                    for err in q_val["missing"]: st.write(f"• {err}")
                    st.info("💡 해당 개념 핵심 복습 포인트")
                    st.write(q_val["points"])
        if not has_review:
            st.success("✨ 세트 3에서 조건 미충족 혹은 오답 문제가 없습니다. 완벽합니다!")
