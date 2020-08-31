import setuptools

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()


def _get_version():
    with open('rlcard_thousand_schnapsen/__init__.py') as f:
        for line in f:
            if line.startswith('__version__'):
                g = {}
                exec(line, g)
                return g['__version__']
        raise ValueError('`__version__` not defined')


VERSION = _get_version()

setuptools.setup(
    name="rlcard_thousand_schnapsen",
    version=VERSION,
    author="Andżelika Domańska",
    author_email="domanskaa@student.mini.pw.edu.pl",
    description="RLCard extension for Thousand Schnapsen game.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adomanska/rlcard-thousand-schnapsen",
    keywords=[
        "Reinforcement Learning", "game", "RL", "AI", "Thousand Schnapsen",
        "Russian Schnapsen"
    ],
    packages=setuptools.find_packages(exclude=('tests', )),
    install_requires=[
        'rlcard>=0.2.5',
        'rlcard[tensorflow]>=0.2.5',
        'Flask-RESTful>=0.3.8',
        'click>=7.1.2',
    ],
    requires_python='>=3.5',
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
)
