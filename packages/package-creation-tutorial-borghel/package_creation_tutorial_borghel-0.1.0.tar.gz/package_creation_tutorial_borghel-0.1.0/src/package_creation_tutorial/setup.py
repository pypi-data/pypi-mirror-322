
# setup.py    :  Fichier pour la configuration et l'installation du package.
# README.md   : Documentation ou instructions du projet.


#  debut si setup.py sur la racine 
# from setuptools import setup, find_packages

#setup(
#    name="package_creation_tutorial",  # Nom du package
#    version="0.1.0",                   # Version
#    packages=find_packages(),          # Trouve automatiquement les packages
#    install_requires=[],               # Ajoutez des dépendances ici si nécessaire
#    description="Un tutoriel pour créer des packages Python",
#    author="Borghel",
#    author_email="borghelborghel3.@gmail.com",
#    url="https://github.com/borghel/package_creation_tutorial",
#)
#  fin si setup.py sur la racine 

from setuptools import setup, find_packages

setup(
    name="package_creation_tutorial",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},  # Indique que le code source est dans "src"
    install_requires=[],
    description="Un tutoriel pour créer des packages Python",
    author="Borghel",
    author_email="borghelborghel3.@gmail.com",
    url="https://github.com/borghel/package_creation_tutorial",
)
