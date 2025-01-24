# setup.py
from setuptools import setup, Extension
import os

# 设置 SDL2 的路径（确保 SDL2 库已安装）
sdl2_include = os.getenv("SDL2_INCLUDE", "/usr/include/SDL2")
sdl2_lib = os.getenv("SDL2_LIB", "/usr/lib/x86_64-linux-gnu")

# 定义模块
module = Extension(
    'CreateWorld.CreateWorld',  # 注意模块路径
    sources=['CreateWorld/CreateWorld.cpp'],
    include_dirs=[sdl2_include],
    library_dirs=[sdl2_lib],
    libraries=['SDL2', 'SDL2_image']
)

# 配置 setup
setup(
    name='CreateWorld',
    version='0.2.0',
    description='A simple SDL2-based module to simulate Pygame functionality',
    author='Zhengzheng',
    author_email='snake.666@qq.com',
    packages=['CreateWorld'],  # 包含 Python 包
    ext_modules=[module],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

