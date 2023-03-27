# Fetch Arte

> *Download `mp4` videos from a list of links from the ARTE website*


## Installation & Setup

- clone the git repository:
    ```
    git clone https://github.com/yzerlaut/Fetch-Arte --recurse-submodules
    ```

- install dependencies (have a look at the required modules in in the [./setup.py](setup.py) file)
    ```
    cd Fetch-Arte # or chdir in Windows
    pip install .
    ```

- *Build your "arte.txt" file*

    Just copy-paste the links one by one from the Arte website (one per line).

    Example of the "arte.txt" file content, see the file: https://github.com/yzerlaut/Fetch-Arte/blob/master/arte.txt

    By default, you should just modify this file in the `Fetch-Arte` folder (remove the current links and put the one you want).

-  Run the program:
    ```
    python -m fetch-arte
    ```

    ** output

    the script runs and downloads the videos one by one to the destination folder (the `~/Videos` directory if it exists otherwise the `Fetch-Arte` folder)

### Run the script with options

Run the following to see the available options:
```
python -m fetch-arte --help
```

### In progress ...


- to deal with prefered languages, maybe one should use the different APIs, not the french one, to be discussed...

- More sophisticated/automated workflow using Web scraping 

    *not woking yet* 

    *but the jupyter notebook `notebook.ipynb` provides fragments of code to fetch the content of the Arte website using [[https://pypi.org/project/beautifulsoup4/][BeautifulSoup]] and thus automates the download (not needing to manually build the `arte.txt` file)*

- Organize your collection

