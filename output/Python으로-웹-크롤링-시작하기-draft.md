# Python으로 웹 크롤링 시작하기

## 웹 크롤링이 뭔가요?

안녕하세요! 혹시 인터넷에서 필요한 정보를 일일이 복사-붙여넣기 하느라 지친 적 있으신가요? 웹 크롤링을 배우면 이런 반복 작업을 자동화할 수 있어요. 웹 크롤링은 웹사이트에서 데이터를 자동으로 추출하는 기술인데요, Python으로 시작하면 생각보다 어렵지 않답니다.

요즘 웹 크롤링 시장이 엄청 성장하고 있어요. 2023년에 49억 달러 규모였던 시장이 2025년에는 72억 달러까지 커질 예정이고, Python 개발자의 65% 이상이 웹 크롤링에 BeautifulSoup을 사용하고 있어요.

## 필요한 도구 준비하기

웹 크롤링을 시작하려면 두 가지 라이브러리만 있으면 돼요:

```bash
pip install requests beautifulsoup4
```

- **Requests**: 웹사이트에 요청을 보내는 라이브러리
- **BeautifulSoup**: HTML에서 원하는 정보를 추출하는 라이브러리

## 간단한 예시로 시작해보기

뉴스 사이트에서 제목을 가져오는 간단한 예시를 만들어볼게요:

```python
import requests
from bs4 import BeautifulSoup

# 웹페이지 가져오기
url = 'https://example.com'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # 제목 추출하기
    titles = soup.find_all('h1')
    for title in titles:
        print(title.get_text().strip())

except requests.exceptions.ConnectionError:
    print('연결에 실패했어요')
except requests.exceptions.Timeout:
    print('시간이 너무 오래 걸려요')
```

여기서 `User-Agent`를 설정하는 건 웹사이트에게 "저는 일반적인 브라우저예요"라고 알려주는 거예요. 이렇게 하면 차단당할 확률이 줄어들죠.

## 꼭 지켜야 할 크롤링 예의

웹 크롤링을 할 때는 몇 가지 지켜야 할 예의가 있어요:

**1. robots.txt 확인하기**
웹사이트 주소 뒤에 `/robots.txt`를 붙여서 크롤링 허용 범위를 확인해주세요.

**2. 요청 간격 조절하기**
너무 빠르게 요청을 보내면 서버에 부담이 돼요. `time.sleep(1)` 같은 코드로 1초씩 쉬어가며 크롤링하는 게 좋아요.

**3. 법적 고려사항**
2024년 Meta v. Bright Data 판례에서 공개 데이터 스크래핑의 합법성이 재확인됐지만, 개인정보나 저작권이 있는 콘텐츠는 주의해야 해요.

## 이제 시작해보세요!

웹 크롤링은 데이터 수집부터 자동화까지 다양하게 활용할 수 있는 유용한 기술이에요. 2025년에는 AI 기반 스크래핑 기술도 나오고 있지만, 기초인 BeautifulSoup과 Requests를 먼저 익혀두시면 어떤 기술이 나와도 쉽게 적응할 수 있을 거예요.

작은 프로젝트부터 시작해서 점차 복잡한 크롤링에 도전해보세요. 윤리적 크롤링만 지킨다면 정말 많은 일을 자동화할 수 있답니다!

