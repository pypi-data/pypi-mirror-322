import os
import time

import streamlit as st
from PIL import Image

from config import Config
from data.quizwiz_session import QuizwizSession
from utils import TextElem


class ImageElem:
    @classmethod
    def show_title_image(cls, page_name):
        title_src = Config.IMAGE_URL["title"]

        if page_name in Config.IMAGE_URL:
            page_src = Config.IMAGE_URL[page_name]
            html = f'<p><img src="{title_src}"><span style="float: right"><img src="{page_src}"></span></p>'
        else:
            html = f'<p><img src="{title_src}"></p>'

        st.html(html)
        # show the top of the page
        st.write("######")

    @classmethod
    def display_setup_page_button(cls, table_name):
        cls._check_is_admin()

        with st.container(border=True):
            cls._display_home_setup_button()
            if table_name not in ["setup", "lucky_draw_winners"]:
                TextElem.draw_headerline(color="blue-green-30")
                cls._display_crud_button(table_name)

    @classmethod
    def get_image(cls, image_name: str, size: tuple[float, float]):
        """
        Retrieve and resize an image. (원하는 크기의 이미지 return)

        Parameters:
            image_name (str): The name of the image file to retrieve.
            size (Tuple[float, float]): A tuple containing the width and height in centimeters.

        Returns:
            PIL image

        Comment:
            아래 위치에 이미지를 저장하세요. (친절하다 친절해. 😜)

            ├── resources
            │         └── images
            │         │         └── your_image_is_here.png 📌
            ├── quizwiz
            │         └── backend
            │         │         └── ...
            │         └── frontend
            │         │         └── ...
        """
        image = Image.open(cls._get_image_path(image_name))  # 이미지 로드

        # 이미지 크기 조정
        fixed_width = size[0] * 37.7952755906  # 10 cm to pixels
        fixed_height = size[1] * 37.7952755906  # 2 cm to pixelss
        image = image.resize((int(fixed_width), int(fixed_height)))
        return image

    @classmethod
    def _get_image_path(cls, image_file_name):
        return f"{os.getcwd()}/resources/images/{image_file_name}"

    @classmethod
    def _check_is_admin(cls):
        if QuizwizSession.get().is_admin():
            st.write("⭕ 당신은 허가받은 관리자입니다!")
        else:
            with st.spinner("🚫 허가 받은 사용자만 접근할 수 있습니다."):
                time.sleep(2)
            st.switch_page("hello.py")

    @classmethod
    def _display_home_setup_button(cls):
        image_home = cls.get_image("fig_frontend_setup_home.png", (1, 1))
        image_setup = cls.get_image("fig_frontend_setup_configuration.png", (1, 1))
        # 이미지 컬럼이 더 작게 설정
        (
            col_home_image,
            col_home_button,
            col_setup_image,
            col_setup_button,
        ) = st.columns([1, 8, 1, 8])
        with col_home_image:
            st.image(image_home, caption="", use_container_width=False)
        with col_setup_image:
            # 참고: use_container_width=False 옵션을 사용하여 이미지를 원본 크기로 표시합니다.
            st.image(image_setup, caption="", use_container_width=False)
        with col_setup_button:
            if st.button(label="Setup Configuration"):
                st.switch_page("admins/setup.py")
        with col_home_button:
            if st.button("Home"):
                st.switch_page("hello.py")

    @classmethod
    def _display_crud_button(cls, table_name):
        image_create = cls.get_image("frontend_create_button.png", (1, 1))
        image_read = cls.get_image("frontend_read_button.png", (1, 1))
        image_update = cls.get_image("frontend_update_button.png", (1, 1))
        image_delete = cls.get_image("frontend_delete_button.png", (1, 1))
        # 이미지 컬럼이 더 작게 설정
        (
            col_create_image,
            col_create_button,
            col_read_image,
            col_read_button,
            col_update_image,
            col_update_button,
            col_delete_image,
            col_delete_button,
        ) = st.columns([1, 3, 1, 3, 1, 3, 1, 3])

        create_page = f"admins/{table_name}.py"
        read_page = f"admins/{table_name}list.py"
        update_page = f"admins/{table_name}.py"
        delete_page = f"admins/{table_name}_del.py"

        col_create_image.image(image_create, caption="", use_container_width=False)
        if col_create_button.button(label="create"):
            st.switch_page(f"{create_page}")

        col_read_image.image(image_read, caption="", use_container_width=False)
        if col_read_button.button(label="read"):
            st.switch_page(f"{read_page}")

        col_update_image.image(image_update, caption="", use_container_width=False)
        if col_update_button.button(label="update"):
            st.switch_page(f"{update_page}")

        col_delete_image.image(image_delete, caption="", use_container_width=False)
        if col_delete_button.button(label="delete"):
            st.switch_page(f"{delete_page}")
