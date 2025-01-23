from setuptools import find_packages, setup
import os

def parse_requirements(filename):
    with open(filename) as f:
        return f.read().splitlines()

requirements_path = os.path.join(os.path.dirname(__file__), 'requeriments.txt')
install_requires=parse_requirements(requirements_path)       
setup(
    name='monkai_agent',
    packages=find_packages(include=['AgentManager','MonkaiAgentCreator','TransferTriageAgentCreator','TriageAgentCreator', 'Agent','Response','Result']),
    version='0.0.3',
    description='Monkai Agent Library',
    author='Monkai Team',
    install_requires=install_requires
)