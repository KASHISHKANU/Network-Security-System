'''Made in order to have info about the project and install dependencies'''
from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
    requirements_lst: List[str] = []
    '''
    This function will return the list of requirements
    ''' 
    try :
        with open("requirements.txt", 'r') as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                if requirement and requirement!='-e .':
                    requirements_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found.")
    return requirements_lst

setup(
    name='Network_Security_System',
    version='0.1.0',
    author='Kashish',
    author_email="lunakanu085@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)

