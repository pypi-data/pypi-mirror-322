from setuptools import setup, find_packages

setup(
    name="DataElevate",
    version="1.0.6",
    packages=find_packages(),  
    install_requires=[
        'google-auth',
        'google-auth-oauthlib',
        'google-api-python-client',
        'requests',
        'pandas',
        'seaborn',
        'numpy',
        'matplotlib',
        'kagglehub',
        'gdown',
        'mysql',
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib',
        'openpyxl',
        'SQLAlchemy',
        'psycopg2',
        'python-dotenv',
        'tqdm'
    ],
    include_package_data=True,  
    author="Monal Bhiwgade",
    author_email="3051monal@gmail.com",
    description="DataElevate is a Python library designed to simplify and enhance data management and analysis workflows. It offers tools for seamless data access, transformation, and integration with external services like Google Drive, ensuring security and ease of use.",
    long_description=open("README.md").read(),  
    long_description_content_type="text/markdown",
    url="https://github.com/Monal-Bhiwgade/DataElevate", 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8', 
    keywords = ['DataElevate', 'Data', 'Data Management', 'Data Analysis', 'Data Transformation', 'Data Integration', 'Drive', 'Drive File', 'Folder', 'Downlaod', 'Elevate', 'Kaggle', 'Dataset Download', 'Dataset']
)