from setuptools import setup, find_packages
from django_starter.version.__version__ import __version__

setup(
    name='django_starter',                 # Le nom de ton package
    version=__version__,                       # La version initiale de ton package
    packages=find_packages(),              # Trouve automatiquement tous les packages
    install_requires=[                    # Les dépendances nécessaires
        'django',
        'djangorestframework',
    ],
    entry_points={                        # Point d'entrée pour exécuter le script
        'console_scripts': [
            'django-starter=django_starter.cli:main',  # commande `django-starter` appelle la fonction main dans cli.py
        ],
    },
    include_package_data=True,             # Inclut les fichiers supplémentaires (README, LICENSE, etc.)
    author='Vens',                     # Ton nom
    author_email='vens.dev.freelance@gmail.com',  # Ton email
    url='https://github.com/v-alex-dev/django_starter',  # Lien vers le dépôt GitHub (si tu en as un)
    classifiers=[                          # Classificateurs pour décrire ton package
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',               # Version minimale de Python
)
