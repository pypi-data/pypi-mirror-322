from setuptools import setup, find_packages

setup(
    name="read_in_terminal",
    version="1.0.0",
    author="Cícero Higor",
    author_email="higormc2015@example.com",
    description="Um utilitário para ler comandos no terminal e executar scripts Python",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/higormcarnauba/read_in_terminal",
    packages=find_packages(),  # Encontra automaticamente todos os pacotes
    install_requires=[
        "pyttsx3",
        "keyboard"
    ],
    entry_points={
        "console_scripts": [
            "Read_In_Terminal=read_in_terminal.main:main",
            "RIT=read_in_terminal.main:main",
            "rit=read_in_terminal.main:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
