# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['search_engine_cpp',
 'search_engine_cpp.helper',
 'search_engine_cpp.wrapper',
 'search_engine_cpp.wrapper.inverted_index',
 'search_engine_cpp.wrapper.page_rank']

package_data = \
{'': ['*'], 'search_engine_cpp': ['lib/*', 'preprocessing/*']}

install_requires = \
['beautifulsoup4>=4.12.3,<5.0.0',
 'cython>=3.0.11,<4.0.0',
 'requests>=2.32.3,<3.0.0']

setup_kwargs = {
    'name': 'search-engine-cpp',
    'version': '0.2.0',
    'description': 'Search Engine is a project that implements a basic search engine using C++, Python, and Cython. It builds a reverse index and ranks pages with the PageRank algorithm based on keyword relevance and page importance.',
    'long_description': '# Search Engine\n[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg)](code_of_conduct.md)\n[![CMake Build and Test](https://github.com/pedrobiqua/Search_Engine/actions/workflows/cmake-multi-platform.yml/badge.svg?branch=main)](https://github.com/pedrobiqua/Search_Engine/actions/workflows/cmake-multi-platform.yml)\n[![Pages Build Deployment](https://github.com/pedrobiqua/Search_Engine/actions/workflows/pages/pages-build-deployment/badge.svg?branch=main)](https://github.com/pedrobiqua/Search_Engine/actions/workflows/pages/pages-build-deployment)\n[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)\n[![PyPi](https://img.shields.io/pypi/v/search-engine-cpp)](https://pypi.org/project/search-engine-cpp)\n\n<p align="center">\n  <img src="https://github.com/user-attachments/assets/3d2be218-6aa2-45af-a956-f1d0fde5bf7e" alt="Logo da biblioteca" width="300">\n</p>\n\n---\n\n**Search Engine** is a simple, efficient engine that builds a reverse index for keyword searching and ranks results using the **PageRank** algorithm.\n\n## ⚙️ Installation\n\nPlease create a virtual environment using `venv`, as the project is still in alpha testing and in its initial implementations.  \n```bash\npython3 -m venv .env\nsource .env/bin/activate\npip install search-engine-cpp\n```\n\n## 🚀 Usage\n```python\nfrom search_engine.crawler import Crawler\n\ncrawler = Crawler("https://en.wikipedia.org", "/wiki/", "Cat", test_mode=True)\ngraph = crawler.run(limit=10)\nmy_dict = graph.compute_page_rank()\ntop = sorted(my_dict.items(), key=lambda item: item[1], reverse=True)[:3]\n\nprint(top)\n```\n\n## 📋 Requirements for Contributions\n\nBefore compiling the project, ensure your environment meets the following requirements:\n\n- **CMake 3.10** or higher\n- **Google Test** for unit testing\n- A **C++11** compatible compiler or higher\n\n## 📂 Project Structure\n\nThe project is organized as follows:\n\n- **`src/`**: Main implementation of the search engine, including reverse indexing and the PageRank algorithm.\n- **`tests/`**: Unit tests to verify the functionality of the system.\n- **`CMakeLists.txt`**: Configuration file for building the project with CMake.\n\n---\n\n## 🔧 Building the Project\n\nTo compile the project, follow these steps:\n\n1. Create a `build` directory and navigate into it:\n\n    ```bash\n    mkdir build && cd build\n    ```\n\n2. Run **CMake** to generate the build files:\n\n    ```bash\n    cmake ..\n    ```\n\n3. Compile the project using **make**:\n\n    ```bash\n    make\n    ```\n\n---\n\n## 🧪 Running Tests for Contributions\n\nRun unit tests to ensure the correctness of the system.\n\n1. After building the project, navigate to the `build` directory and execute:\n\n    ```bash\n    ./tests/unit-tests/LibUnitTests\n    ```\n\nThis will run the tests covering search engine functionality, reverse indexing, and the PageRank algorithm.\n\n---\n\n## 🏃 Running Examples for Contributions\n\nThe first step is building the project, for this to run:\n\n```bash\npoetry install\npoetry build\n```\n\nAfter building it, run this command to see the library working:\n\n```bash\npoetry run python Examples/graph_example.py\n```\n\n---\n\n## ⚙️ How It Works\n\n- **Reverse Indexing**: Maps keywords to the documents where they appear.\n- **PageRank**: An algorithm that assigns a relevance score to each document based on its links and structure.\n- **Querying**: Searches for documents related to a keyword and ranks them according to their PageRank score.\n\n---\n\n## 📄 License\n\nThis project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.\n\n---\n\n## 👥 Contributors\n\nWe welcome all contributions to this project! Please make sure to follow the guidelines outlined in the [CONTRIBUTING.md](CONTRIBUTING.md) file.<br>\nThanks to all [contributors](https://github.com/pedrobiqua/Search_Engine/graphs/contributors)\n\n[![Contributors](https://contrib.rocks/image?repo=pedrobiqua/Search_Engine)](https://github.com/pedrobiqua/Search_Engine/graphs/contributor)\n\n\nMade with [contrib.rocks](https://contrib.rocks).\n\n---\n\nKeep learning,<br>\n**Pedro;)**\n',
    'author': 'Pedro Bianchini de Quadros',
    'author_email': 'pedrobiqua@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pedrobiqua.github.io/Search_Engine/html/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
