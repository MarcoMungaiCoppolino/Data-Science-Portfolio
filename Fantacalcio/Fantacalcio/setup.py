from setuptools import setup

VERSION = '0.0.1'
DESCRIPTION = 'A Classification Project'
LONG_DESCRIPTION = """The project is a comparison of the performance 
    of an SVM model and a MLP model"""

setup(
    name='AI_YoutubeComments_SentimentAnalysis',
    version=VERSION,
    author='Marco Mungai Coppolino',
    author_email="<marcomungaicoppolino@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    install_requires=['numpy', 'pandas', 'sklearn'],
    keywords=['python', 'data science', 'preprocessing', 'encoding'],
    packages=['AI_YoutubeComments_SentimentAnalysis']
    
)
