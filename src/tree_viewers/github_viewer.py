import requests
from src.tree_viewers.base_viewer import BaseViewer
from src.utils.tree_formatter import format_tree

class GitHubViewer(BaseViewer):
    def view(self, repo_url, config):
        owner, repo = self._parse_repo_url(repo_url)
        tree = self._build_tree(owner, repo, config)
        contents = self._get_contents(owner, repo, config) if config.show_file_contents else {}
        return format_tree(tree, f"{owner}/{repo}", config), contents
    
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

    def _get_contents(self, owner, repo, config, path=''):
        contents = {}
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
        response = requests.get(url)
        
        if response.status_code == 200:
            items = response.json()
            for item in items:
                if item['type'] == 'dir':
                    if not config.is_excluded(item['name']):
                        contents.update(self._get_contents(owner, repo, config, item['path']))
                else:
                    if not any(config.is_excluded(p) for p in item['path'].split('/')):
                        content_response = requests.get(item['download_url'])
                        if content_response.status_code == 200:
                            contents[item['path']] = content_response.text
                        else:
                            contents[item['path']] = "[Unable to fetch file content]"
        return contents
