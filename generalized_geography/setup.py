import setuptools

setuptools.setup(
    name="generalized-geography", # Replace with your own username
    version="0.0.1",
    author="Hyomin",
    author_email="miamiq0000@gmail.com",
    description="Generalized Geography Game Solver",
    url="https://github.com/singrum/generalized-geography",
    install_requires=['networkx', 'matplotlib'],
    packages=setuptools.find_packages(),
    keywords=['generalized geography', 'word chain', 'game', 'graph theory'],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    setup_requires=['wheel'],
    python_requires='>=3.6',
)