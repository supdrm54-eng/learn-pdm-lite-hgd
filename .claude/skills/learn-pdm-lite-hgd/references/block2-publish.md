# Block 2: 공개 — 그래프 한 장을 GitHub Pages로

> **Phase A 시작 시 그대로 출력한다:**
> ```
> 📖 공식 문서: https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site · https://cli.github.com/manual/gh_repo_create
> ```

## EXPLAIN

### 1. 정의

| 용어 | 뜻 |
|---|---|
| 저장소 | GitHub에 올린 폴더 |
| GitHub Pages | 저장소의 `index.html`을 `https://내아이디.github.io/저장소이름/` 주소로 보여 주는 무료 기능 |
| 공개 전 점검 | 올리기 전에 비밀값·개인정보·회사 자료가 섞였는지, '가상 데이터' 표시가 있는지 확인하는 것 |

### 2. 파일 첨부 vs 주소 공유

| 기준 | 파일 첨부 | 공개 주소 |
|---|---|---|
| 받는 사람 | 내려받아 열어야 한다 | 링크 하나로 휴대폰에서 바로 |
| 고칠 때 | 다시 보낸다 | 같은 주소가 새 판이 된다 |

### 3. 보안 수칙

- 공개는 되돌리기 어렵다. 점검 결과를 보고 내가 "공개해"라고 말한 뒤에만 올린다.
- 이 실습 데이터는 가상이라 공개해도 된다. 회사 설비 데이터는 넣지 않는다.
- 비밀번호·토큰을 채팅창이나 파일에 쓰지 않는다. 커밋 작성자는 개인 이메일 대신 GitHub noreply 주소를 쓴다.

## EXECUTE

아래 프롬프트를 붙여 넣으라고 안내한다.

```
pdm-lite 폴더의 그래프를 공개할 준비를 해 줘. 공개는 내가 "공개해"라고 말한 뒤에만 해.

1. 공개 전 점검: 비밀번호·토큰·이메일·전화번호 패턴이 있는지, index.html 에 "실습용 가상 데이터" 표시가 있는지, 올라갈 파일 목록. env_check.txt 는 올리지 마.
2. 점검 결과를 채팅에 보여 주고 멈춰.
3. 내가 "공개해"라고 하면: gh 로그인을 확인하고(안 되어 있으면 일회용 코드만 알려 줘), gh auth setup-git 을 한 뒤, git 작성자가 비어 있으면 GitHub noreply 주소를 이 저장소에만 설정하고, public 저장소 pdm-lite-dashboard 를 만들어 올리고, GitHub Pages(main, /)를 켜서 주소가 열릴 때까지 확인해 줘.
```

### 확인할 것 (Phase B)

- 공개 전 점검에서 비밀값·개인정보 패턴 0건, 올라간 파일에 `env_check.txt`가 없다.
- 수강생이 "공개해"라고 답한 경우에만: `https://내아이디.github.io/pdm-lite-dashboard/`가 열리고 그래프와 빨간 점 3개가 보인다.
- 공개하지 않기로 했다면 저장소를 만들지 않았다.

막히면 원인을 Claude Code에게 찾게 하는 후속 프롬프트를 준다. 정답은 "정답 보기" 요청이 있을 때만 연다.

```
Pages 주소가 3분이 지나도 404다. 저장소의 Pages 설정(브랜치·폴더)과 index.html 위치를 확인해서 원인을 찾아 줘.
```

## QUIZ

Block 2는 퀴즈가 없다(10분 수업 — 퀴즈는 Block 1의 1문항뿐). 정답·해설 대신 공개 주소가 열리는지 확인하는 것으로 마치고, AskUserQuestion으로 수업을 마칠지 묻는다.
