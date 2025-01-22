from setuptools import setup, find_packages

setup(
    name='package_joseph',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'scipy',
        'numpy',  # Ajoutez d'autres dépendances nécessaires ici
    ],
    author='Joseph Barreau',
    author_email='joseph.barreau@francetravail.fr',
    description='Un package pour calculer la taille nécessaire d’un échantillon pour une étude statistique',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://git-scm.pole-emploi.intra/IJBA1200/package-python',  # Remplacez par l'URL de votre dépôt
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)


