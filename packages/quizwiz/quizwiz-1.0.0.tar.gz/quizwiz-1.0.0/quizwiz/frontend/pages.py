import streamlit as st

pages = [
    st.Page("hello.py", title="Hello QuizWiz", icon=":material/quiz:", default=True),
    st.Page("intro.py", title="Introduce Event", icon=":material/info:"),
    st.Page("problem.py", title="Solve Quiz", icon=":material/help:"),
    st.Page("problem_step.py", title="Solve Quiz", icon=":material/help:"),
    st.Page("answer.py", title="Check Answer", icon=":material/mood:"),
    st.Page("review.py", title="Review Statistics", icon=":material/star:"),
]

admin_pages = [
    # Entrance of setup page
    st.Page("admins/setup.py", title="QuizWiz Setup", icon=":material/list:"),
    # LuckyDraw winners page
    st.Page(
        "admins/lucky_draw_winners.py",
        title="Lucky Draw winners",
        icon=":material/list:",
    ),
    # Quiz table
    st.Page("admins/quiz.py", title="Create Quiz", icon=":material/add_circle:"),
    st.Page("admins/quizlist.py", title="Read Quiz", icon=":material/list:"),
    st.Page("admins/quiz_del.py", title="Delete Quiz", icon=":material/list:"),
    st.Page(
        "admins/default_quizlist.py",
        title="Create default quiz list",
        icon=":material/list:",
    ),
    # Event table
    st.Page("admins/event.py", title="Create Event", icon=":material/add_circle:"),
    st.Page("admins/eventlist.py", title="Read Event", icon=":material/list:"),
    st.Page("admins/event_del.py", title="Delete Event", icon=":material/list:"),
    st.Page(
        "admins/default_eventlist.py",
        title="Create default event list",
        icon=":material/list:",
    ),
    # Ticket table
    st.Page("admins/ticket.py", title="Create Ticket", icon=":material/add_circle:"),
    st.Page("admins/ticketlist.py", title="Read Ticket", icon=":material/list:"),
    st.Page("admins/ticket_del.py", title="Delete ticket", icon=":material/list:"),
    st.Page(
        "admins/default_ticketlist.py",
        title="Create default ticket list",
        icon=":material/list:",
    ),
    # Answer table
    st.Page("admins/answers.py", title="Create Answer", icon=":material/add_circle:"),
    st.Page("admins/answerlist.py", title="Read Answer", icon=":material/list:"),
    st.Page("admins/answer_del.py", title="Delete Answer ", icon=":material/list:"),
    st.Page(
        "admins/default_answerlist.py",
        title="Create default answer list",
        icon=":material/list:",
    ),
]
