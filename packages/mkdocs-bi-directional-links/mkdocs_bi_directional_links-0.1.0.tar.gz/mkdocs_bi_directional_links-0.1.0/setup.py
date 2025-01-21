from setuptools import setup, find_packages

setup(
    name="mkdocs-bi-directional-links",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "mkdocs>=1.0",  # 依赖 MkDocs
    ],
    entry_points={
        "mkdocs.plugins": [
            "bi_directional_links = mkdocs_bi_directional_links.plugin:BiDirectionalLinksPlugin",
        ],
    },
)