from flask import Flask, render_template, request, session
import random
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # 세션을 위한 시크릿 키 설정


# DP 알고리즘 구현 (계단 별 설명 추가)
def stair_climbing_algorithm_with_explanation(stairs):
    n = len(stairs)
    dp = [0] * (n + 1)
    explanation = []  # 각 계단별 설명을 담을 리스트

    # 첫 번째 계단
    dp[1] = stairs[0]
    explanation.append(f"1 번째 계단:\n   - 1 번째 계단 점수 = {stairs[0]}")

    if n > 1:
        dp[2] = stairs[0] + stairs[1]
        explanation.append(f"2 번째 계단:\n   - 2 번째 계단 점수 = {dp[2]}")

    if n > 2:
        dp[3] = max(stairs[0] + stairs[2], stairs[1] + stairs[2])
        explanation.append(
            f"3 번째 계단:\n   - 1 번째 계단 점수 + 3 번째 계단 점수 = {stairs[0] + stairs[2]}\n"
            f"   - 2 번째 계단 점수 + 3 번째 계단 점수 = {stairs[1] + stairs[2]}\n"
            f"   - 선택된 최댓값: {stairs[0] + stairs[2]} vs {stairs[1] + stairs[2]} → {dp[3]}"
        )

    for i in range(4, n + 1):
        option1 = dp[i - 3] + stairs[i - 2] + stairs[i - 1]
        option2 = dp[i - 2] + stairs[i - 1]
        dp[i] = max(option1, option2)

        explanation.append(
            f"- {i}번째 계단:\n"
            f"  -{i - 3}번째 계단의 최댓값 + {i - 1}번째 계단 점수 + {i}번째 계단 점수 = {option1}\n"
            f"  -{i - 2}번째 계단의 최댓값 + {i}번째 계단 점수 = {option2}\n"
            f"- 선택된 최댓값: {option1} vs {option2} → {dp[i]}\n"
        )

        # explanation.append(f"   -{i}번째 계단

        #                    선택된 최댓값: {option1} vs {option2} → {dp[i]}")

    return dp[n], explanation


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    dp_process = []

    # 새로운 계단을 설정 (초기화되면 세션에 저장)
    if "stairs" not in session or request.args.get("reset"):
        # 초기화 시점에서 계단 재설정
        stairs = [random.choice([5, 10, 15, 20, 25, 30]) for _ in range(6)]
        session["stairs"] = stairs
        session.pop("result", None)  # 초기화할 때 이전 최댓값 제거
        session.pop("dp_process", None)  # 초기화할 때 이전 해설 제거
    else:
        stairs = session["stairs"]

    # POST 요청이 들어왔을 때 (정답 확인 버튼을 눌렀을 때)
    if request.method == "POST":
        # 최댓값과 알고리즘 과정을 계산하여 세션에 저장
        result, dp_process = stair_climbing_algorithm_with_explanation(stairs)
        session["result"] = result
        session["dp_process"] = dp_process

    # 세션에 저장된 값을 가져옴 (최댓값과 해설)
    result = session.get("result")
    dp_process = session.get("dp_process")

    return render_template(
        "index.html", result=result, dp_process=dp_process, stairs=stairs
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 88))  # Qoddi가 지정하는 포트 사용
    app.run(host="0.0.0.0", port=port)
