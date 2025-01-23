import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.let_it_rain import rain
from streamlit_extras.markdownlit import mdlit
from streamlit_extras.mention import mention

from data.quizwiz_session import QuizwizSession


class TextElem:
    # blue, red, orange, violet, green, yellow, etc
    # [blue]contents[/blue]
    @staticmethod
    def md_colored(contents):
        mdlit(contents)

    @staticmethod
    def display_github_voc():
        mention(
            label="QuizWiz VoC",
            icon="github",
            url="https://github.samsungds.net/SLSISE/QuizWiz/issues",
        )

    @staticmethod
    def display_rain_icons(
        emoji="🎈", font_size=54, falling_speed=5, animation_length="infinite"
    ):
        rain(
            emoji=emoji,
            font_size=font_size,
            falling_speed=falling_speed,
            animation_length=animation_length,
        )

    @staticmethod
    def draw_headerline(
        label="",
        description=None,
        color="violet-70",
    ):
        colored_header(
            label=label,
            description=description,
            color_name=color,
        )

    @staticmethod
    def show_question_field(idx, quiz):
        # 이미지 넣는 것은 생각보다 이쁘지 않다. ❗
        # col2, col3 = st.columns([1, 11])
        # image = get_image("frontend_quiz_icon.png", (0.7, 0.7))
        # col1.image(image, caption="", use_container_width=False)
        st.markdown(f"###### 【문제{idx}】")
        st.markdown(f"{quiz['question']}")

    @staticmethod
    def display_crud_page_title(crud, page_name):
        crud_actions = {"C": "생성 & 수정", "R": "조회", "U": "수정", "D": "삭제"}

        if crud in crud_actions:
            st.title(f"{page_name.upper()} record {crud_actions[crud]}")
        else:
            st.error(f"Invalid CRUD operation: {crud}")

    @staticmethod
    def welcome_event_message(event):
        TextElem.md_colored(event["description"])
        TextElem.draw_headerline(color="blue-green-70")

    @staticmethod
    def show_upcoming_event(event):
        TextElem.md_colored(
            f"### 📣[blue]Coming soon……[/blue] Event('[green]{event['event_code']}[/green]')"
        )
        TextElem.md_colored(f"it will take place starting from {event['started_at']}")
        TextElem.draw_headerline(color="blue-green-70")

    @staticmethod
    def show_expired_event(event):
        TextElem.md_colored(
            f"### 😏[red]Oops expired[/red] event_code={event['event_code']}"
        )
        TextElem.md_colored(
            f"it was opened from {event['started_at']} to {event['expired_at']}, But you[green]can try it[/green]. 😁"
        )
        TextElem.draw_headerline(color="blue-green-70")

    @staticmethod
    def show_ongoing_event(event):
        message = f"🤞Event('[green]{event['event_code']}[/green]') will[green]take place[/green] from {event['started_at']} through {event['expired_at']}."
        TextElem.md_colored(message)

    @staticmethod
    def show_unknown_event():
        message = "### 😥[red]Oops unknown[/red] event…"
        TextElem.md_colored(message)

    @staticmethod
    def translate_message(msg_key, focus_words=None, use_key=True):
        # focus_words는 (단어, 색상) 튜플의 리스트로 받습니다.
        if focus_words is None:
            focus_words = []

        if use_key:
            message = QuizwizSession.get().i18n_instance().translate(msg_key)
        else:
            message = msg_key

        # focus_words 리스트를 순회하며, 각 단어에 색상을 적용합니다.
        for word_key, word_color in focus_words:
            word = QuizwizSession.get().i18n_instance().translate(word_key)
            message = message.replace(
                word,
                f"[{word_color}]{word}[/{word_color}]",
            )

        # 메시지에 색상 적용 후 출력
        TextElem.md_colored(message)
