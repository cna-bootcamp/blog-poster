# React Hooks 완벽 가이드 - 초보자도 쉽게! 🎣

## 들어가며

React를 배우기 시작했는데 Hook이라는 게 뭔가요? 클래스형 컴포넌트는 너무 복잡하다고 들었는데... 혹시 이런 고민을 하고 계신가요?

걱정하지 마세요! React Hooks는 2018년 React 16.8에서 처음 소개된 이후로 지금은 React 개발의 완전한 표준이 되었어요. 오늘은 가장 많이 쓰이는 `useState`와 `useEffect`를 중심으로 React Hooks의 핵심을 쉽게 알아보겠습니다.

## useState - 컴포넌트의 메모장 📝

### 기본 개념

`useState`는 컴포넌트가 기억해야 할 정보를 저장하는 Hook이에요. 마치 메모장에 중요한 내용을 적어두는 것처럼요!

```javascript
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>현재 카운트: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        증가
      </button>
    </div>
  );
}
```

여기서 `useState(0)`는 "초기값 0으로 메모장을 만들어줘"라는 뜻이고, `[count, setCount]`는 "현재 값을 읽을 때는 count, 값을 바꿀 때는 setCount를 사용할게"라는 약속이에요.

### 자주 하는 실수와 해결법

**❌ 이렇게 하면 안 돼요:**
```javascript
// 상태를 직접 수정하려고 시도
const [todos, setTodos] = useState([]);
todos.push(newTodo); // 이건 작동하지 않아요!
```

**✅ 이렇게 해야 해요:**
```javascript
const [todos, setTodos] = useState([]);
setTodos([...todos, newTodo]); // 새 배열을 만들어서 전달
```

React는 값이 바뀌었는지 확인할 때 "참조"를 비교해요. 기존 배열에 값을 추가만 하면 여전히 같은 배열이라고 생각해서 화면이 업데이트되지 않거든요.

## useEffect - 컴포넌트의 알람시계 ⏰

### 기본 개념

`useEffect`는 "특정 상황이 되면 이 작업을 실행해줘"라고 요청할 때 사용해요. 컴포넌트가 화면에 나타날 때, 상태가 바뀔 때, 사라질 때 등 다양한 타이밍에 작업을 실행할 수 있어요.

```javascript
import { useState, useEffect } from 'react';

function Timer() {
  const [seconds, setSeconds] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setSeconds(prev => prev + 1);
    }, 1000);

    // 정리 작업 (컴포넌트가 사라질 때 실행)
    return () => clearInterval(timer);
  }, []); // 빈 배열 = 컴포넌트가 처음 나타날 때만 실행

  return <div>경과 시간: {seconds}초</div>;
}
```

### 의존성 배열의 비밀

`useEffect`의 두 번째 매개변수인 의존성 배열이 가장 헷갈리는 부분이에요. 간단하게 정리하면:

- `[]` (빈 배열): 컴포넌트가 처음 나타날 때만 실행
- `[count]`: count 값이 바뀔 때마다 실행
- 배열 없음: 렌더링될 때마다 실행 (거의 사용하지 않음)

### 실용적인 예제 - API 데이터 가져오기

```javascript
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUser = async () => {
      setLoading(true);
      try {
        const response = await fetch(`/api/users/${userId}`);
        const userData = await response.json();
        setUser(userData);
      } catch (error) {
        console.error('사용자 정보를 가져오는데 실패했어요:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, [userId]); // userId가 바뀔 때마다 새로운 사용자 정보를 가져와요

  if (loading) return <div>로딩 중...</div>;

  return (
    <div>
      <h1>{user?.name}</h1>
      <p>{user?.email}</p>
    </div>
  );
}
```

## Hook 사용할 때 꼭 지켜야 할 규칙

React Hooks에는 반드시 지켜야 할 두 가지 황금 규칙이 있어요:

1. **컴포넌트나 커스텀 Hook의 최상위에서만 사용하기** - 반복문이나 조건문 안에서 사용하면 안 돼요
2. **매번 같은 순서로 호출하기** - React가 Hook들을 순서로 구분하거든요

**❌ 이렇게 하면 안 돼요:**
```javascript
function BadComponent() {
  if (someCondition) {
    const [state, setState] = useState(0); // 조건문 안에서 Hook 사용
  }
}
```

**✅ 이렇게 해야 해요:**
```javascript
function GoodComponent() {
  const [state, setState] = useState(0); // 최상위에서 Hook 사용

  if (someCondition) {
    // 여기서 state 사용
  }
}
```

## 마무리

React Hooks는 처음에는 어려울 수 있지만, `useState`와 `useEffect`만 제대로 이해해도 대부분의 프로젝트에서 필요한 작업들을 처리할 수 있어요.

핵심은 다음과 같아요:
- `useState`: 컴포넌트가 기억해야 할 값 저장
- `useEffect`: 특정 타이밍에 작업 실행
- Hook 규칙: 최상위에서 같은 순서로 사용

처음에는 의존성 배열 때문에 헷갈릴 수도 있지만, 몇 번 써보시면 금세 익숙해질 거예요. 무엇보다 직접 코드를 작성해보면서 익히는 것이 가장 좋은 방법이니까 작은 프로젝트부터 시작해보세요!

---
**참고 자료**
- [React Hooks 공식 문서](https://react.dev/reference/react/useState) - React.dev
- [리액트의 Hooks 완벽 정복하기](https://velog.io/@velopert/react-hooks) - 벨로퍼트 블로그
- [useEffect 완벽 가이드 번역](https://rinae.dev/posts/a-complete-guide-to-useeffect-ko/) - Rinae 블로그