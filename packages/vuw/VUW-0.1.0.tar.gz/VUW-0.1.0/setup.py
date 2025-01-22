from setuptools import setup, find_packages
import os

# README 파일 읽기
def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), encoding="utf-8") as f:
        return f.read()

setup(
    name="VUW",  # 패키지 이름
    version="0.1.0",  # 패키지 버전
    author="Jiwon Chae",  # 작성자 이름
    author_email="jwchae106@gmail.com",  # 작성자 이메일
    description="A brief description of the package",  # 패키지 설명
    long_description=read_file("README.md"),  # 상세 설명
    long_description_content_type="text/markdown",  # README 파일 형식
    packages=find_packages(),  # 포함할 패키지 자동 탐색
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",  # 최소 Python 버전
    install_requires=[
        "requests>=2.25.1",  # 필수 의존성
        "numpy>=1.21.6",  # 필수 의존성
	"joblib>=1.3.2",
	"pandas>=1.1.5",
	"dateutil>=0.20.1"
    ]
)

