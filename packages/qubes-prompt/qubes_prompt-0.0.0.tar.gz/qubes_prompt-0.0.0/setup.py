from setuptools import setup, find_packages

setup(
    name="qubes-prompt",
    vqersion="0.1.4",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
        ]
    },
    entry_points={
    'console_scripts': [
            'qubes-fzf=qubes_prompt.fzf:main',
            'qubes-rofi=qubes_prompt.rofi:main',
        ],
    },
    package_data={
        'qubes_prompt': ['db/*.json', 'icon.png'],
    },
    author="ubuntupunk",
    author_email="ubuntupunk@gmail.com",
    description="A Qubes OS command prompter and manual browser using rofi/fzf",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ubuntupunk/qubes-prompt",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.6",
)
