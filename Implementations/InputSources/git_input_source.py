from Framework.input_source import InputSource
import os
from git import repo
import shutil

class GitInputSource(InputSource):

    def __init__(self, input_source):
        self.revisions = []
        self.branch_name = "master"
        self.input_source = input_source

    def get_files_with_revisions(self, input_source=None):
        #export GIT_REPO_PATH='/home/saurabc/Documents/work/SE/Temp'
        if input_source is None:
            input_source = self.input_source
        else:
            self.input_source = input_source
        input_url, path =  self.process_input(input_source, self.branch_name)
        working_directory = "/Users/kccowan/Documents/College/F19/CS5704/Project/Temp/pc" #os.path.join(os.getenv('GIT_REPO_PATH'), "pc")
        if os.path.exists(working_directory):
            shutil.rmtree(working_directory)
        #path = "Tests/GraphBuilderTests.py"
        cloned_repo = repo.Repo.clone_from(input_url, working_directory)
        self.revisions = self.get_revisions_from_repo(cloned_repo, path)
        return self.revisions

    def get_revisions_from_repo(self, repo, path):
        relevant_commits = list(repo.iter_commits(paths=path))
        revlist = (
            (commit, (commit.tree / path).data_stream.read())
            for commit in relevant_commits
        )

        revisions = []
        for commit, file_contents in revlist:
            str_file_contents = str(file_contents).split("\\n")
            revisions.append(str_file_contents)

        revisions = revisions[::-1]
        return revisions

    def process_input(self, input_source, branch_name):
        # assert input_source
        path_parts = input_source.split(branch_name)
        url_parts = path_parts[0].split("/blob")
        url = url_parts[0] + ".git"
        path = path_parts[1].lstrip("/")
        return url, path