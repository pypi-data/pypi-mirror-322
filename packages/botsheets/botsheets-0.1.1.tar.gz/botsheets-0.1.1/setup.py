from setuptools import setup, find_packages


setup(
    name="botsheets",
    version="0.1.1",
    description='Class integrate with google sheets for RPA',
    author='Ben-Hur P. B. Santos',
    author_email='botlorien@gmail.com',
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/botlorien/botsheets",  # Link para o repositório
    packages=find_packages(),  # Especifica que os pacotes estão na pasta src
    include_package_data=True,  # Inclui arquivos de dados especificados no MANIFEST.in
    package_data={
        '': ['assets/*'],  # Inclui todos os arquivos na pasta assets
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',  # Versão mínima do Python
    install_requires=[
        'pandas',
        'gspread',
        'oauth2client',
        'botenv'
        ],
    )
# pip install setuptools
# python setup.py sdist
# pip install twine
# twine upload dist/*
