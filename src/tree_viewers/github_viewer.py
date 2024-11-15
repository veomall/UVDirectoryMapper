import requests
from src.tree_viewers.base_viewer import BaseViewer
from src.utils.tree_formatter import format_tree


class GitHubViewer(BaseViewer):
    def view(self, repo_url, config):
        owner, repo = self._parse_repo_url(repo_url)
        tree = self._build_tree(owner, repo, config)
        return format_tree(tree, f"{owner}/{repo}", config)
    
    def is_github_url(url):
        return url.startswith("https://github.com/") and url.count('/') >= 4


    def _parse_repo_url(self, repo_url):
        parts = repo_url.split('/')
        return parts[-2], parts[-1]

    def _build_tree(self, owner, repo, config, path=''):
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data from GitHub: {response.status_code}")
        
        contents = response.json()
        tree = {}
        for item in contents:
            if item['type'] == 'dir':
                tree[item['name']] = self._build_tree(owner, repo, config, item['path'])
            else:
                tree[item['name']] = None
        return tree
