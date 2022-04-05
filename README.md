# GitHub User Searcher

## What is This Project?
This project shows how to search for popular GitHub Users using GitHub's public API.

Specifically, it supports searching for:
* The minimum number of followers a user has
* The minimum number of public repos a user has
* The programming language in a user’s public repos

For more information, including a walkthrough of how to use GitHub's Search API, check out the [Project Wiki](** LINK GOES HERE **).


## Getting Started
This project was developed using [Python 3.9.7](https://www.python.org/downloads/release/python-397/).

It is highly recommended to use a Python virtual environment to manage the project and its dependencies to avoid version conflicts with any other projects on your computer. I recommend using [conda](https://docs.conda.io/en/latest/), although [venv](https://docs.python.org/3/library/venv.html) or any other Python package management solution should work just as well.

The instructions in this README will use conda.

## How to Run the Code
1. Create a new virtual environment using Python 3.9.7 & install dependencies:
    ```bash
    $ conda create -n github-search python=3.9 requests pandas
    $ conda activate github-search
    ```

2. To check that you're using the correct version of Python, use this command:
    ```bash
    $ python --version
    ```
    Expected Output:
    ```
    Python 3.9.7
    ```

3. Set the search criteria (Lines 162-164):
    ```python
    searcher = UserSearcher(
        min_followers=1000, min_repos=None, language=None)
    users = searcher.search(1000)
    ```

4. Run the code:
    ```bash
    $ python search-github-users.py
    ```

Expected Output:
```
username                       github_url
0        torvalds      https://github.com/torvalds
1       yyx990803     https://github.com/yyx990803
2         gaearon       https://github.com/gaearon
3          ruanyf        https://github.com/ruanyf
4     JakeWharton   https://github.com/JakeWharton
..            ...                              ...
995          dlew          https://github.com/dlew
996  algorithmzuo  https://github.com/algorithmzuo
997        ireade        https://github.com/ireade
998  rafaelfranca  https://github.com/rafaelfranca
999      dinosoid      https://github.com/dinosoid

[1000 rows x 2 columns]
```

### Troubleshooting

#### Common Python Problems
* Make sure you've activated the virtual environment.
    ```bash
    $ conda activate github-search
    ```
* Make sure you're using Python 3.9.
    * To check your Python version:
        ```bash
        $ python --version
        ```
* Make sure you've installed the `requests` and `pandas` packages before running the code.
    * To list all installed packages:
        ```bash
        $ conda list
        ```
    * To check specifically for requests and pandas:
        ```bash
        $ conda list | grep 'requests\|pandas'
        ```

#### Common GitHub Problems
* Make sure your Internet connection is stable.
* Make sure you’re using https not http.
* Make sure you’re not encoding the `:` and `+` characters in your query string.
* Make sure you haven’t exceeded GitHub’s hourly rate limit.

Check out GitHub’s [Search API Troubleshooting](https://docs.github.com/en/search-github/getting-started-with-searching-on-github/troubleshooting-search-queries) and [Searching Users](https://docs.github.com/en/search-github/searching-on-github/searching-users) documentation for more information and tips.
