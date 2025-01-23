# ✨QuizWiz
QuizWiz(Quiz Wizard) is a platform that provides users with engaging quizzes to test their knowledge and skills. Users can enjoy learning and competing through a variety of topics and difficulty levels.

![QuizWiz architecture](./docs/images/fig_quizwiz_architecure.png)


## 💦먼저 QuizWiz를 체험해보세요!  
Quiz Wizard는 간단한 퀴즈를 통해 앱의 주요 기능을 체험할 수 있는 최고의 방법입니다. 지금 바로 퀴즈를 풀어보며 학습과 재미를 모두 경험해보세요!

[📣 Go to QuizWiz](https://pando.samsungds.net/quiz/) 

<img src="./docs/images/fig_quizwiz_hello_page.png" alt="이벤트 참여 페이지" style="width: 60%;">



## 0️⃣ Pre-condition
- python3.9
- `가상환경` 사용 권장
- venv 환경에서 pip install -r requirements.txt

#### 가상 환경 설정 및 패키지 설치 방법

1. 프로젝트 디렉토리로 이동합니다.
    ``` bash
    git clone https://github.samsungds.net/SLSISE/QuizWiz.git
    cd /path/to/your/project
    ```

2. .venv 가상 환경을 생성합니다.
    ``` bash
    python3 -m venv .venv
    ```

3. 가상 환경을 활성화합니다.
   - **Windows**
     ```bash
     .venv\Scripts\activate
     ```
   - **Linux / macOS**
     ```bash
     source .venv/bin/activate
     ```

4. 필요 패키지를 설치합니다.
   ```bash
   pip install -r requirements.txt
   ```

## 🔱Usecase
- 퀴즈 주제 범위는 자유, TE 그룹원 누구나 제출 가능 (Author 권한 필요)
- 관리자 페이지를 이용해서 퀴즈 생성 가능
- 한 개 이상의 퀴즈를 하나의 묶음으로 만들어서 이벤트 생성 가능
- 사용자는 등록된 이벤트 코드를 통해서 퀴즈 풀이 확인

## ✅How to make Quiz & Event
#### 
### 1. Quiz 생성
<details>
  <summary> 1) Connect to QuizWiz </summary>

* 📣  [Go to QuizWiz](https://pando.samsungds.net/quiz/) 클릭해서 접속 후, `Login` 하세요.

![Fig.Login](./docs/images/howToMakeQuiz_step1_login.png)

</details>

<details>
  <summary> 2) Go to `Settings`(관리자 설정 화면) </summary>

* 관리자로 등록되어 있는 분들에게만 보이는 화면입니다.
* 관리자는 Backend Database에서 관리되며, 등록을 원하시면 [VOC](https://github.samsungds.net/SLSISE/QuizWiz/issues)를 남겨주세요.

![Fig.Settings](./docs/images/howToMakeQuiz_step2_settings.png)

</details>

<details>
  <summary> 3) Create/Read/Update/Delete Quiz </summary>

* Quiz 관련 `CRUD` 버튼을 누르세요.

![Fig.Quiz_CRUD](./docs/images/howToMakeQuiz_step3_Quiz_CRUD.png)

* Question field 는 text-area widget으로 Multi-line 으로 작성가능합니다.
  * 유익한 퀴즈를 자유롭게 작성하세요.
  * 마크다운 문법을 지원해요.
  * `Preview` 버튼으로 문제 출력화면을 미리 확인할 수 있어요.

![Fig.Quiz question](./docs/images/howToMakeQuiz_step4_Quiz_question.png)

* 선택지를 작성하고, Answer field에는 선택지의 값을 동일하게 작성하세요.

![Fig.Quiz contents answer](./docs/images/howToMakeQuiz_step5_Quiz_contents_answer.png)

* 나머지 필드를 채워주세요.
* 제일 중요한 필드는 `label` 입니다.
* 이벤트 생성시, `label`과 일치하는 퀴즈를 출제합니다.

![Fig.Quiz label](./docs/images/howToMakeQuiz_step6_Quiz_label.png)

</details>

### 2. Event 생성
* `이벤트 운영`은 특별 행사, 뉴스레터 등과 연계하여 자유롭게 부담없이 준비하세요.

<details>
  <summary> 1) Create Event </summary>

#### Event Code: 사용자들에게 제공될 기억하기 쉬운 단어이면 좋겠죠?
#### Label: ❗❗ 파이썬 dict 형태로 작성해야합니다. (💦조금 불편하지만, 나중에 개선할게요.)
  * {label_name: [quiz_count, "random | fix"]}
    * label_name: Quiz 생성시 등록한 label 필드입니다. 이벤트는 label과 일치하는 퀴즈를 생성해요.
    * quiz_count: label과 일치하는 퀴즈를 몇 문제 생성하고 싶으세요?
    * "random" or "fix": 퀴즈를 랜덤하게 or 데이터베이스에 저장된 순서대로 고정(fix)
    * Ex. 파이썬 관련 3문제와 C++ 관련 2문제를 생성하고 싶은 이벤트의 라벨은?
      * {"python":[3,"random"], "cpp":[2,"random"]}

![Fig.Creat Event](./docs/images/howToMakeEvent_step1_event.png)

</details>

<details>
  <summary> 2) Example Event </summary>

* `Event Code`를 입력하고 경험해보세요.
  * Just try it. why not?: `review8`, `ddcon24`

![Fig.Hello page](./docs/images/howToMakeEvent_step2_event_code.png)

* `문제 풀이` 클릭

![Fig.Intro page](./docs/images/howToMakeEvent_step3_intro.png)

* 퀴즈를 풀어보세요.

![Fig.Problem page](./docs/images/howToMakeEvent_step4_problem.png)

</details>

## ▶How To Run
Backend REST API 서버 - FASTAPI

```bash
$python entrypoint.py
```

Frontend Web 서버 - Streamlit

```bash
$streamlit run quizwiz/frontend/app.py
```

DS AD 로그인 아이디를 설정해서 실행하는 경우 환경변수로 `DEBUG_ID`를 설정 후 실행
```
$DEBUG_ID=admin streamlit run quizwiz/frontend/app.py
```

브라우저에서 접속하되 관리자와 일반 사용자는 다른 url로 접근

- 퀴즈 생성(관리자) - /quiz 로 접속
- 이벤트 생성(관리자) - /event 로 접속
- 퀴즈 풀기(일반 사용자) - / 로 접속


## 🔃Deploy with docker container
Build with expose port.

```
$ docker build -t quizwiz-api:dev --build-arg port=8000 -f DockerfileApi .
$ docker build -t quizwiz-app:dev --build-arg port=8501 -f DockerfileApp .
$ docker build -t quizwiz-auth:dev --build-arg port=8080 -f DockerfileAuth .
```

Run with `API_HOST`, `API_PORT` environment variables.

```
$ docker run -d --name quizwiz-api --net quizwiz --net-alias quizwiz-api quizwiz-api:dev -v quizwiz-dev:/database
$ docker run -d --name quizwiz-app --net quizwiz \
--env API_HOST=quizwiz-api \
--env API_PORT=8000 \
--env AUTH_URL=https://pando.samsungds.net:8080 \
--env MODE=PROD \
-p 8501:8501 quizwiz-app:dev
$ docker run -d --name quizwiz-auth --net quizwiz -p 8080:8080 --env SERVICE_URL=https://12.36.187.217:8501 quizwiz-auth:dev
```

개발 서버에서 auth 서버를 운영할 경우 self-signed certificate를 사용해야 합니다. 인증서가 있는 위치를 `-v [호스트 경로]:[컨테이너 내부 경로]`로 마운트하고 환경 변수 `CERT_KEY`, `CERT`에 각각의 파일 패스를 설정해서 실행합니다.

```
# 예를 들어 /app/cert/localhost.dev.key /app/cert/localhost.dev.cert 파일이 있을 경우
$ docker run -d --name quizwiz-auth --net quizwiz -p 8888:8080 -v /app/cert:/etc/cert --env MODE=DEV --env CERT_KEY=/etc/cert/localhost.dev.key --env CERT=/etc/cert/localhost.dev.crt --env SERVICE_URL=https://12.36.187.217:8501 quizwiz-auth:dev
```

#### FYI. Dev Server 운영
dev-server 브랜치에 push하면 docker container 빌드해서 `http://10.229.19.168:8501/` 여기에 배포됩니다.


## 🙋‍♀️🙋‍♂️Contributing
* [How to contribute❓](https://github.samsungds.net/SLSISE/QuizWiz/blob/main/CONTRIBUTING.md)

## 👉Developer Information & Contacts

S.LSI S/W Engineering Team

* Byoungwoo Yoon (byoungwoo.yoon@samsung.com)
* Dongseok Yi (dseok.yi@samsung.com)
* Jeong Seong-moon (salt.jeong@samsung.com)
* KIMYoukyoung (ylarvine.kim@samsung.com)

> We welcome your feedback and questions! Feel free to contact each developer via their GitHub profile or email.

## ❗Reference
* [python](https://www.python.org/): Python is a programming language that lets you work quickly
and integrate systems more effectively.
* [streamlit](https://streamlit.io/): A faster way to build and share data apps.
* [pandas](https://pandas.pydata.org/): pandas is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool, built on top of the Python programming language.
* [plotly](https://plotly.com/python/): Plotly Open Source Graphing Library for Python.
* [FastAPI](https://fastapi.tiangolo.com/): FastAPI framework, high performance, easy to learn, fast to code, ready for production
* [sqlite](https://www.sqlite.org/): QLite is a C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine.