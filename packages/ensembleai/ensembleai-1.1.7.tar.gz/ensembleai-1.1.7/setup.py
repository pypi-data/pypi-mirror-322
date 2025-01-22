from setuptools import setup, find_packages

setup(
    name='ensembleai',
    version='1.1.7',
    summary='A Python package for AI-MultiModal MultiAgents methods and tools.',
    home_page='',
    author='Shreyas Jain, Prakhar Jain, Kushagra Jain',
    author_email=' shreyasjain.feb@gmail.com, prakharjain2004@gmail.com, kushagrajain.feb@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'groq',
        'wikipedia-api',
        'youtube_transcript_api',
        'PyPDF2',
        'faiss-cpu',
        'langchain_community',
        'requests',
        'beautifulsoup4',
        'pandas',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)
