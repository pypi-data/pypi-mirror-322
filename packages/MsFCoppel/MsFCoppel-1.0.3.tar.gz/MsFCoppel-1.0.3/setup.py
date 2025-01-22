import setuptools
from MsFCoppel import version

with open("README.md", "r") as fh:
    long_description = ''  # fh.read()

setuptools.setup(
    name="MsFCoppel",
    version=version,
    author="Damian Rosado",
    author_email="damian.uriel@coppel.com",
    description="Libreria para microservicios REST",
    long_description=long_description,

    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    install_requires=[
        'kafka-python==2.0.1',
        'Logbook',
        'asyncio-nats-client==0.10.0',
        'jaeger-client==4.3.0',
        'fluent-logger==0.9.6',
        # 'Flask==1.1.1',
        'bottle==0.12.18',
        'coloredlogs==14.0',
        'colorama==0.4.3',
        'Pygments==2.6.1',
        # 'event-signal==1.8.0',
        'waitress==1.4.4',
        "redis==3.5.3",
        'contextvars==2.4',
        "requests==2.20.0",
        "autodynatrace==1.0.75"
    ]
)
