from setuptools import setup, find_packages

# requirements.txt 읽기
with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="quizwiz",  # 패키지 이름
    version="1.0.0",  # 버전
    description="A quiz system for developers",  # 짧은 설명
    author="byoungwoo.yoon",  # 작성자 이름
    author_email="byoungwoo.yoon@samsung.com",  # 이메일
    include_package_data=True,  # package_data에 명시된 파일 포함
    # packages=find_packages(),  # 패키지 자동 탐색
    packages=find_packages(
        include=["quizwiz", "quizwiz.*"]
    ),  # quizwiz와 하위 패키지 포함
    install_requires=requirements,
    # install_requires=[
    #     # 의존성 패키지 예시
    #     "streamlit>=1.0.0",
    #     "fastapi>=0.70.0",
    # ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",  # Python 최소 버전
)
