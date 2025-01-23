import os

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from pygwalker.api.streamlit import StreamlitRenderer
import numpy as np
from data.quizwiz_session import QuizwizSession


class GraphElem:
    @classmethod
    def draw_barplot_quiz_pass_rate(cls, df, idx, quiz_id):
        # Pass Rate 계산
        pass_count, fail_count, user_count = cls._get_answer_table_result(df, quiz_id)
        total = pass_count + fail_count
        pass_rate = (pass_count / total) * 100 if total else 0

        # 가로 막대 그래프 그리기
        color_map = px.colors.sequential.Rainbow_r
        figure = go.Figure(
            data=[
                go.Bar(
                    x=[pass_rate],
                    y=[f"Quiz {idx}"],
                    orientation="h",
                    marker=dict(
                        color=color_map[cls._get_score_index(pass_rate, len(color_map))]
                    ),
                )
            ]
        )

        figure.update_layout(
            height=100,
            width=650,
            margin=dict(l=60, r=5, b=50, t=20, pad=4),
            shapes=[
                dict(
                    type="rect",
                    xref="paper",
                    yref="paper",
                    x0=0,
                    y0=0,
                    x1=1,
                    y1=1,
                    line=dict(
                        color="Black",
                        width=1,
                    ),
                )
            ],
        )  # 그래프 크기 조절

        figure.update_xaxes(range=[0, 101])  # X축 범위 0~100으로 고정

        figure.add_annotation(
            x=pass_rate / 2,
            y=0,
            text=f"{pass_rate:.2f}%",
            showarrow=False,
            font=dict(size=16, color="black", family=cls._get_plotly_cjk_font_prop()),
            xanchor="center",
            yanchor="middle",
        )

        xaxis_title = (
            QuizwizSession.get()
            .i18n_instance()
            .translate("xaxis_title")
            .format(user_count=user_count, total=total, pass_rate=pass_rate)
        )

        figure.update_layout(
            xaxis_title=xaxis_title,
            font=dict(size=13, color="black", family=cls._get_plotly_cjk_font_prop()),
        )

        figure.update_xaxes(fixedrange=True)
        figure.update_yaxes(fixedrange=True)

        return figure

    @classmethod
    def display_ticket_statistics_bubble_chart(cls, df: pd.DataFrame):
        # 1. grade의 점수별 분포도 시각화
        # 점수 범위를 정의합니다.
        bins = range(0, 111, 1)  # 0부터 100까지 1점 간격으로 범위 설정
        bubble_chart_labels = [f"{i}" for i in bins[:-1]]  # 레이블 생성

        # 점수에 대한 빈을 계산합니다.
        df["grade_bins"] = pd.cut(
            df["grade"].dropna(), bins=bins, labels=bubble_chart_labels, right=False
        )
        grade_counts = df["grade_bins"].value_counts().sort_index()

        # Ticket ID에 해당하는 점수 정보 찾기
        my_score = df.loc[df["id"] == QuizwizSession.get().ticket["id"], "grade"]
        if not my_score.empty:
            my_score_bin = pd.cut(
                my_score, bins=bins, labels=bubble_chart_labels, right=False
            ).values[0]
            my_score_count = grade_counts[my_score_bin]
        else:
            my_score_bin = None
            my_score_count = 0

        # # Bubble 차트를 그립니다.
        # 0인 값들을 제외한 데이터로 Scatter 플롯을 그립니다.
        non_zero_grade_counts = grade_counts[grade_counts > 0]
        df_non_zero_grade_counts = pd.DataFrame(
            {
                "grade": non_zero_grade_counts.index,
                "count": non_zero_grade_counts.values,
                "size": non_zero_grade_counts.values * 200,
                "text": [
                    f"{count}{QuizwizSession.get().i18n_instance().translate('word_person')}"
                    for count in non_zero_grade_counts.values
                ],
            }
        )

        figure = px.scatter(
            df_non_zero_grade_counts,
            x="grade",
            y="count",
            size="size",
            color_continuous_scale=px.colors.sequential.Rainbow,
            opacity=0.4,
            color="count",
            size_max=50,
        )

        # Bubble 가운데에 grade 점수를 표시
        for _, row in df_non_zero_grade_counts.iterrows():
            figure.add_annotation(
                x=row["grade"],
                y=row["count"],
                text=row["text"],
                showarrow=False,
                font=dict(
                    size=9, color="black", family=cls._get_plotly_cjk_font_prop()
                ),
            )

        # 특정 ticket_id의 점수를 빨간 점으로 추가
        if my_score_bin:
            my_score_bin = [my_score_bin] if np.isscalar(my_score_bin) else my_score_bin
            my_score_count = (
                [my_score_count] if np.isscalar(my_score_count) else my_score_count
            )
            figure.add_trace(
                go.Scatter(
                    x=my_score_bin,
                    y=my_score_count,
                    mode="markers",
                    marker=dict(
                        size=[20] * len(my_score_bin),  # 빨간 점의 크기
                        color="red",
                        line=dict(width=2, color="DarkSlateGrey"),
                    ),
                    name="You™",
                )
            )

        # x축과 y축 레이블 설정
        # x축과 y축 레이블 설정
        y_min = round(np.min(non_zero_grade_counts.values), -1) - 10
        y_max = round(np.max(non_zero_grade_counts.values), -1) + 10
        figure.update_layout(
            xaxis_title="Grade",
            yaxis_title="Users",
            title="Distribution of Grades",  # 제목 설정
            xaxis=dict(tickangle=45),  # x축 레이블 회전
            yaxis=dict(
                dtick=(int((y_max - y_min) / 10) if y_max > y_min + 100 else 10),
                range=(
                    [y_min - 10, y_max + 10] if y_min >= 10 else [y_min, y_max + 10]
                ),
            ),
        )
        return figure

    @staticmethod
    def _convert_to_hashable(item):
        if isinstance(item, list):
            return tuple(item)
        if isinstance(item, dict):
            return {k: GraphElem._convert_to_hashable(v) for k, v in item.items()}
        return item

    @staticmethod
    def visualize_table_records_with_pyg(table_records):
        if not table_records or not isinstance(table_records, (list, dict)):
            st.error(f"{type(table_records)=} or {table_records=}")
            return

        st.subheader("📌Table Data Visualization with PygWalker")

        table_records = [
            GraphElem._convert_to_hashable(record) for record in table_records
        ]
        df = pd.DataFrame(table_records)
        pyg_app = StreamlitRenderer(df)
        pyg_app.explorer(default_tab="data")

    @classmethod
    def display_pie(cls, df_tickets, value_key, name_key):
        df = cls._get_counts_per_grade(df_tickets)
        return px.pie(
            df,
            values=df[value_key].tolist(),
            names=df[name_key].sort_values().tolist(),
            category_orders={"names": df[name_key].sort_values().tolist()},
            color_discrete_sequence=px.colors.qualitative.Set3,
        )

    @classmethod
    def _get_answer_table_result(cls, df, quiz_id: int) -> tuple:
        """
        주어진 quiz_id에 해당하는 'ticket_id', 'result', 'knox_id' 열만을 추출하여
        Pass와 Fail의 개수를 계산하고, 고유한 'knox_id'의 집합을 반환하는 함수입니다.

        Parameters:
        - df (pd.DataFrame): 입력 DataFrame
        - quiz_id (int): 특정 quiz_id 값

        Returns:
        - tuple: (pass_count, fail_count, unique_ticket_ids)
          - pass_count (int): Pass의 개수
          - fail_count (int): Fail의 개수
          - unique_knox_ids (set): 고유한 unique_knox_ids의 집합, 1명이 N번 try 가능
        """
        # 특정 quiz_id에 해당하는 'ticket_id', 'result', 'knox_id' 열만 추출
        quiz_results = df[df["quiz_id"] == quiz_id][["ticket_id", "result", "knox_id"]]

        # 'result' 열에서 'Pass'와 'Fail'의 개수를 계산
        result_counts = quiz_results["result"].value_counts()
        pass_count = result_counts.get("Pass", 0)
        fail_count = result_counts.get("Fail", 0)

        # 'knox_id' 열에서 고유한 값들의 집합을 생성
        unique_knox_ids = set(quiz_results["knox_id"])

        return pass_count, fail_count, len(unique_knox_ids)

    @classmethod
    def _get_counts_per_grade(cls, df):
        counts = (
            df["grade"]
            .sort_index()
            .value_counts()
            .sort_index(ascending=False)
            .reset_index()
        )
        counts.columns = ["grade", "count"]
        counts = counts.sort_values(by="grade")
        return counts

    @classmethod
    def _get_plotly_cjk_font_prop(cls):
        return f"{os.getcwd()}/resources/fonts/NotoSansCJK-Regular.ttc"

    @classmethod
    def _get_score_index(cls, score, steps):
        if steps < 0:
            return 0

        bins = np.linspace(0, 100, steps)
        return min(np.digitize(score, bins, right=True), steps - 1)
