#!/bin/bash
# ============================================================
# blog-poster DMAP Plugin - GitHub 배포 스크립트
# ============================================================
# 사용법: bash publish.sh
#
# 이 스크립트는 blog-poster 플러그인을 GitHub에 배포합니다.
# 실행 전 gh CLI가 설치되어 있어야 합니다.
#   - macOS: brew install gh
#   - Windows: winget install --id GitHub.cli
#   - Linux: https://cli.github.com/
# ============================================================

set -e

# --- 설정 ---
PLUGIN_NAME="blog-poster"
GITHUB_OWNER="cna-bootcamp"
REPO_NAME="blog-poster"
DESCRIPTION="기술/IT 블로그 글을 주제 리서치부터 최종 Word 문서 출력까지 자동화하는 블로그 작성 에이전트"

echo ""
echo "============================================"
echo "  blog-poster DMAP Plugin 배포"
echo "============================================"
echo ""

# --- Step 1: gh CLI 확인 ---
echo "[1/4] gh CLI 확인 중..."
if ! command -v gh &> /dev/null; then
    echo "❌ gh CLI가 설치되어 있지 않습니다."
    echo "   설치 방법:"
    echo "   - macOS: brew install gh"
    echo "   - Windows: winget install --id GitHub.cli"
    echo "   - Linux: https://cli.github.com/"
    exit 1
fi
echo "✅ gh CLI 확인 완료: $(gh --version | head -1)"

# --- Step 2: gh 인증 확인 ---
echo ""
echo "[2/4] GitHub 인증 확인 중..."
if ! gh auth status &> /dev/null; then
    echo "GitHub에 로그인되어 있지 않습니다. 로그인을 진행합니다..."
    gh auth login
fi
echo "✅ GitHub 인증 확인 완료"

# --- Step 3: 원격 저장소 생성 ---
echo ""
echo "[3/4] 원격 저장소 확인 중..."
if gh repo view "${GITHUB_OWNER}/${REPO_NAME}" &> /dev/null; then
    echo "✅ 저장소가 이미 존재합니다: ${GITHUB_OWNER}/${REPO_NAME}"
else
    echo "저장소를 생성합니다: ${GITHUB_OWNER}/${REPO_NAME}"
    gh repo create "${GITHUB_OWNER}/${REPO_NAME}" --public --description "${DESCRIPTION}"
    echo "✅ 저장소 생성 완료"
fi

# --- Step 4: Push ---
echo ""
echo "[4/4] 코드를 Push합니다..."

# remote 설정
REMOTE_URL="https://github.com/${GITHUB_OWNER}/${REPO_NAME}.git"
if git remote get-url origin &> /dev/null; then
    git remote set-url origin "${REMOTE_URL}"
else
    git remote add origin "${REMOTE_URL}"
fi

git push -u origin main

echo ""
echo "============================================"
echo ""
echo "🎉 축하합니다!"
echo ""
echo "당신의 플러그인 '${PLUGIN_NAME}'이 세상에 첫 발을 내딛었습니다."
echo "아이디어에서 시작해 요구사항 정의, 설계, 개발, 그리고 배포까지 —"
echo "모든 여정을 함께 해서 기뻤습니다."
echo ""
echo "이제 당신이 허락하는 누구나 이 플러그인을 설치하고 사용할 수 있습니다."
echo ""
echo "============================================"
echo ""
echo "📦 플러그인 설치 방법 (사용자에게 공유하세요)"
echo ""
echo "  # 1. GitHub 저장소를 마켓플레이스로 등록"
echo "  claude plugin marketplace add ${GITHUB_OWNER}/${REPO_NAME}"
echo ""
echo "  # 2. 플러그인 설치"
echo "  claude plugin install ${PLUGIN_NAME}@${REPO_NAME}"
echo ""
echo "  # 3. 설치 확인"
echo "  claude plugin list"
echo ""
echo "📖 자세한 설치·사용법은 README.md를 참고하세요:"
echo "   https://github.com/${GITHUB_OWNER}/${REPO_NAME}/blob/main/README.md"
echo ""
