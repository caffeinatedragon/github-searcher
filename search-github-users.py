import pandas as pd
import requests
import json
import urllib.parse


class DataFrameFromDict:
    '''
    A very helpful utility to clean up unwanted columns from pandas DataFrames.
    Temporarily imports data frame columns and deletes them afterwards.

    Usage:
        with DataFrameFromDict(JSON_TO_NORMALIZE) as df:
            df['key1'] = df['thing-to-keep-from-json']
            df['key2'] = df['another-thing-to-keep-from-json']

        after exiting Context Manager (with/as):
        df is only the remapped 'key1' & 'key2' columns from original DataFrame

    From: https://karllorey.medium.com/keeping-pandas-dataframes-clean-when-importing-json-348d3439ed67
    '''

    def __init__(self, data):
        self.df = pd.json_normalize(data)
        self.columns = list(self.df.columns.values)

    def __enter__(self):
        return self.df

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.df.drop([c for c in self.columns], axis=1, inplace=True)


class UserSearcher:
    BASE_URL = 'https://api.github.com'
    GITHUB_HEADER = {
        'Accept': 'application/vnd.github.v3+json'
    }

    def __init__(self, min_followers: int = None, min_repos: int = None, language: str = None):
        '''
        If no search parameters are specified, will raise ValueError.

        Keyword Arguments:
            min_followers - user's minimum follower count (default: None)
            min_repos     - user's minimum number of repos (default: None)
            language      - programming language in user's repos (default: None)

        Attributes:
            _search_query - the query string used to search for users matching
                            the input criteria from Keyword Arguments
        '''
        # check for missing args
        if all(v is None for v in {min_followers, min_repos, language}):
            raise ValueError('Must specify at least one search parameter.')

        # Build a query string to search GitHub Users based on input
        # parameters. If any parameter is unspecified (left as None),
        # it will not be included in the search query.
        query = []

        if min_followers:
            query.append(f'followers:>={min_followers}')
        if min_repos:
            query.append(f'repos:>={min_repos}')
        if language:
            query.append(f'language:{language}')

        self._search_query = '+'.join(query)

    def search(self, num_results: int) -> pd.DataFrame:
        '''
        Search for all GitHub Users matching specified criteria.

        Keyword Arguments:
            num_results    - total search results to return

        Returns:
            search_results - pandas DataFrame of User info in the format:
                             [{"username": str, "github_url": str}]

        If num_results is greater than 100, GitHub requires multiple calls
        to the API to get all results. This function will make all calls and
        return all search results.
        '''
        # GitHub Search API limits to 100 results per page
        max_results = 100
        num_pages = self._get_pages(num_results, max_results)

        # placeholder for response
        search_results = pd.DataFrame({'username': pd.Series(dtype='str'),
                                       'github_url': pd.Series(dtype='str')})

        for i in range(num_pages):
            # you can manually specify the sort order by uncommenting the
            # 'sort' and 'order' keys below, but GitHub's default behavior
            # seems pretty good.
            # (https://docs.github.com/en/rest/reference/search#ranking-search-results)
            #     "Unless another sort option is provided as a query parameter,
            #     results are sorted by best match in descending order."
            payload = {
                'q': self._search_query,
                'page': i + 1,
                'per_page': min(num_results, max_results),
                'type': 'user',
                # 'sort': 'followers',
                # 'order': 'desc'
            }

            # encoding the special characters in the query string (q)
            # causes requests to fail. urlencode lets us bypass
            payload_str = urllib.parse.urlencode(payload, safe=':+=')
            resp = requests.get(f'{UserSearcher.BASE_URL}/search/users',
                                headers=UserSearcher.GITHUB_HEADER,
                                params=payload_str)

            # read the GitHub response, grab only what we need
            records = json.loads(resp.text)
            with DataFrameFromDict(records['items']) as df:
                df['username'] = df['login']
                df['github_url'] = df['html_url']

            # how many results should be grabbed from the last page?
            if i + 1 == num_pages:
                final_res = num_results % max_results or max_results
                df = df.iloc[0:final_res, :]

            # add the new info to the final search_results DataFrame
            # by using concat with ignore_index, each page should
            # be added in the correct order to maintain GitHub's best match
            search_results = pd.concat([search_results, df],
                                       ignore_index=True,
                                       copy=False)

        return search_results

    def _get_pages(self, num_results: int, max_results: int) -> int:
        '''
        Utility to figure out how many pages of max_results length
        need to be found in order to get the total num_results.

        Keyword Arguments:
            num_results - the total results to get across all pages
            max_results - the maximum results allowed per page

        Returns:
            num_pages - how many pages are required to view all results

        Examples:
            10 results  / 100 max results = 1 page
            100 results / 100 max results = 1 page
            150 results / 100 max results = 2 pages
            201 results / 100 max results = 3 pages
            200 results / 100 max results = 2 pages
        '''
        # the total number of pages should be (num_results / max_results).
        # +1 if there's a remainder.
        return (num_results // max_results) + (num_results % max_results > 0)


if __name__ == '__main__':
    searcher = UserSearcher(
        min_followers=1000, min_repos=None, language=None)
    users = searcher.search(1000)
    print(users)
