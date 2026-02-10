# blog-poster 개발 계획서

## 1. 공유자원 마켓플레이스에서 가져갈 자원

| 자원 유형 | 자원명 | 복사 위치 | 용도 |
|----------|--------|----------|------|
| 도구 (MCP) | context7 | `gateway/mcp/context7.json` | 기술 문서 검색 (researcher 에이전트) |
| 도구 (커스텀 앱) | generate_image | `gateway/tools/generate_image.py` | AI 이미지 생성 (image-creator 에이전트) |
| 템플릿 | README-plugin-template | README.md 작성 참고 | 플러그인 README 작성 |

## 2. 커스텀 앱/CLI 개발 계획

추가 커스텀 개발 불필요. 공유자원의 `generate_image.py`를 그대로 활용.

generate_image 의존성:
- `pip install python-dotenv google-genai`
- 환경 변수: `GEMINI_API_KEY` (setup 스킬에서 안내)

## 3. 외부 자원 파악

블로그 콘텐츠 제작 관련 가이드/템플릿은 공유자원에 없음.
→ SEO 최적화 가이드라인을 seo-optimizer 에이전트의 AGENT.md에 직접 작성.
→ 블로그 글 작성 스타일 가이드를 writer 에이전트의 AGENT.md에 직접 작성.

## 4. 플러그인 구조 설계

### 4-1. 에이전트 구성

| 에이전트 | 티어 | 역할 | 추상 도구 |
|---------|------|------|----------|
| researcher | MEDIUM | 웹 검색, 기술 문서 조사, 트렌드 분석 | web_search, doc_search |
| writer | MEDIUM | 블로그 본문 작성, 구조화, Word 문서 생성 | file_read, file_write |
| seo-optimizer | MEDIUM | 키워드 분석, 메타 태그 생성, SEO 점수 평가 | file_read |
| image-creator | MEDIUM | AI 이미지 생성 (Gemini 기반) | image_generate, code_execute |

### 4-2. 스킬 구성

| 스킬 | 유형 | 실행 경로 | 설명 |
|------|------|----------|------|
| setup | Setup | 직결형 | 플러그인 설치 및 초기 설정 (install.yaml 기반) |
| core | Core | 위임형 | 시스템 행동 규범, 모호한 요청의 의도 판별 및 라우팅 |
| help | Utility | 직결형 | 사용 가능한 명령 및 자동 라우팅 안내 |
| write-post | Orchestrator | 위임형 | 블로그 글 작성 메인 워크플로우 (6단계 순차 진행) |

### 4-3. Gateway 설정

**install.yaml:**
- MCP: context7 (기술 문서 검색, scope: user, required: false)
- 커스텀 앱: generate_image (이미지 생성, required: false)

**runtime-mapping.yaml:**
- tier_mapping: default (HEAVY→opus, HIGH→opus, MEDIUM→sonnet, LOW→haiku)
- tool_mapping: web_search, doc_search, image_generate 매핑
- action_mapping: 표준 액션 카테고리 매핑

### 4-4. 디렉토리 구조

```
blog-poster/
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── skills/
│   ├── setup/
│   │   └── SKILL.md
│   ├── core/
│   │   └── SKILL.md
│   ├── help/
│   │   └── SKILL.md
│   └── write-post/
│       └── SKILL.md
├── agents/
│   ├── researcher/
│   │   ├── AGENT.md
│   │   ├── agentcard.yaml
│   │   └── tools.yaml
│   ├── writer/
│   │   ├── AGENT.md
│   │   ├── agentcard.yaml
│   │   └── tools.yaml
│   ├── seo-optimizer/
│   │   ├── AGENT.md
│   │   ├── agentcard.yaml
│   │   └── tools.yaml
│   └── image-creator/
│       ├── AGENT.md
│       ├── agentcard.yaml
│       └── tools.yaml
├── gateway/
│   ├── install.yaml
│   ├── runtime-mapping.yaml
│   ├── mcp/
│   │   └── context7.json
│   └── tools/
│       └── generate_image.py
├── commands/
│   ├── setup.md
│   ├── help.md
│   └── write-post.md
├── .gitignore
└── README.md
```

## 5. DMAP 표준 산출물 생성 순서

| 순서 | 산출물 | 설명 |
|------|--------|------|
| 1 | `.claude-plugin/plugin.json` | 플러그인 매니페스트 |
| 2 | `.claude-plugin/marketplace.json` | 마켓플레이스 매니페스트 |
| 3 | `.gitignore` | 보안/임시 파일 제외 |
| 4 | `gateway/install.yaml` | 설치 매니페스트 |
| 5 | `gateway/runtime-mapping.yaml` | 추상→구체 매핑 테이블 |
| 6 | `gateway/mcp/context7.json` | MCP 서버 설정 |
| 7 | `gateway/tools/generate_image.py` | 이미지 생성 커스텀 도구 (공유자원 복사) |
| 8 | `agents/researcher/` | researcher 에이전트 패키지 (3파일) |
| 9 | `agents/writer/` | writer 에이전트 패키지 (3파일) |
| 10 | `agents/seo-optimizer/` | seo-optimizer 에이전트 패키지 (3파일) |
| 11 | `agents/image-creator/` | image-creator 에이전트 패키지 (3파일) |
| 12 | `skills/setup/SKILL.md` | setup 스킬 (직결형, 필수) |
| 13 | `skills/core/SKILL.md` | core 스킬 (위임형, 필수) |
| 14 | `skills/help/SKILL.md` | help 스킬 (직결형, 권장) |
| 15 | `skills/write-post/SKILL.md` | write-post 스킬 (Orchestrator, 메인 워크플로우) |
| 16 | `commands/setup.md` | setup 슬래시 명령 진입점 |
| 17 | `commands/help.md` | help 슬래시 명령 진입점 |
| 18 | `commands/write-post.md` | write-post 슬래시 명령 진입점 |
| 19 | `README.md` | 플러그인 사용 가이드 |

**총 산출물**: 약 25개 파일
