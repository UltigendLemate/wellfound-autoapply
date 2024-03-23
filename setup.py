from setuptools import setup, find_packages

setup(
    name='autoply',
    version='1.0.0',
    description='Just as the name implies, auto apply on wellfound with a custom cover letter for every role. Sit back and let AI help you get the job :)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author=['Anupam Maurya', 'Chaitanya Anand'],
    author_email=['anupammaurya981@gmail.com'],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.11',
    ],
    packages=find_packages(),
    python_requires='>=3.11',  # Updated version specifier
    install_requires=[
        'selenium',
        'tk',
        'python-dotenv',
        'google-generativeai',
        'webdriver_manager',
        'PyPDF2',
        'openpyxl',
    ],
    setup_requires=['wheel'],
)
