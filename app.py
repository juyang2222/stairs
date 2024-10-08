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
    result = []
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

    for j in range(1, n + 1):
        result.append(dp[j])
    result = [str(item) for item in result]

    return result, explanation


@app.route("/", methods=["GET"])
def index():
    result = []
    dp_process = []

    # 새로운 계단을 설정 (초기화되면 세션에 저장)
    if "stairs" not in session or request.args.get("reset"):
        stairs = [random.choice([10, 15, 20, 25]) for _ in range(6)]
        result, dp_process = stair_climbing_algorithm_with_explanation(stairs)
        session["stairs"] = stairs
        session["result"] = result
        session["dp_process"] = dp_process

    # 세션에서 계단, 결과, 해설을 가져오기
    stairs = session["stairs"]
    result = session["result"]
    dp_process = session["dp_process"]

    return render_template(
        "index.html", result=result, dp_process=dp_process, stairs=stairs
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 88))  # Qoddi가 지정하는 포트 사용
    app.run(host="0.0.0.0", port=port)
