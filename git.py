#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 19:22:04 2020

@author: mrlittle
"""


from github import Github
import secrets, time

class Git():
    INFO = """#Repo for gitpalette Usage
\nProject Link - https://github.com/dmrlittle/gitpalette/
\nAuthor - **@dmrlittle**
"""
    
    def __init__(self,*args):
        self.obj=Github(*args)
        self.usr=self.obj.get_user()
                
    def check(self):
        try:
            for repo in self.usr.get_repos():
                pass
            return 0
        except Exception as e:
            return str(e.data['message'])
        
    def create(self):
        for repo in self.usr.get_repos():
            if(repo.name == 'gitpalette_'):
                self.repo = repo
                break
        else:
            self.repo = self.usr.create_repo(name='gitpalette_')
            self.repo.create_file("GenFile.txt", "init commit", secrets.token_hex(16))
            self.repo.create_file("README.md", "info commit", self.INFO)
        
    def commit(self):
        file = self.repo.get_contents("/GenFile.txt")
        self.repo.update_file("GenFile.txt", "first commit", secrets.token_hex(16), file.sha)
        