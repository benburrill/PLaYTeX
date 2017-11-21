from setuptools import setup

setup(
    name="playtex",
    version="0.1.0",
    description="Render Python objects in LaTeX documents",
    license="MIT",
    author="Ben Burrill",
    author_email="bburrill98+playtex@gmail.com",
    url="https://github.com/benburrill/playtex",
    packages=["playtex"],
    entry_points={
        "console_scripts": [
            "playtex-render = playtex.tool:main"
        ]
    },
    install_requires=["PyYAML", "click"]
)
