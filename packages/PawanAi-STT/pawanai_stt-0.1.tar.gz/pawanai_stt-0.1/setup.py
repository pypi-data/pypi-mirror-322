from setuptools import setup,find_packages

setup(
    name='PawanAi_STT',
    version='0.1',
    author='Pawan Kumar',
    author_email='pawanku.sbp@gmail.com',
    description='this is speech to text package created by pawan kumar'
)
packages = find_packages(),
install_requirements = [
    'selenium',
    'webdriver_manager'
]
