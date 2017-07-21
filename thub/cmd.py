#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: stdrickforce (Tengyuan Fan)
# Email: <stdrickforce@gmail.com> <fantengyuan@baixing.com>

import argparse
import base64
import requests
import json
import os
import sys

API_HOST = "https://gitlab.baixing.cn/api/v4"


class Gitlab(object):

    @property
    def token(self):
        if 'THUB_TOKEN' not in os.environ:
            print('THUB_TOKEN has not been set in env')
            sys.exit(1)
        return os.environ.get('THUB_TOKEN')

    @property
    def pid(self):
        if 'THUB_PID' not in os.environ:
            print('THUB_PID has not been set in env')
            sys.exit(1)
        return os.environ.get('THUB_PID')

gl = Gitlab()


class RepositoryFile(object):

    def __init__(self, filepath, content='', from_api=False):
        self._filepath = filepath
        self._content = content
        self._from_api = from_api

    @classmethod
    def _session(cls):
        s = requests.session()
        s.headers.update({'PRIVATE-TOKEN': gl.token})
        return s

    def save(self, content="", message="update", ref="thrifthub"):
        url = "%s/projects/%s/repository/files/%s" % (API_HOST, gl.pid, self._filepath)
        data = {
            "branch": ref or 'thrifthub',
            "content": content,
            "commit_message": "update",
        }
        if self._from_api:
            res = self._session().put(url, data=data)
        else:
            res = self._session().post(url, data=data)
        if res.status_code not in [200, 201]:
            print(res.content)
            raise Exception('internal error')

    @classmethod
    def get(cls, filepath, ref=None):
        url = "%s/projects/%s/repository/files/%s" % (API_HOST, gl.pid, filepath)
        params = {
            'ref': ref or 'thrifthub',
        }
        res = cls._session().get(url, params=params)
        if res.status_code == 404:
            return None
        elif res.status_code == 200:
            data = json.loads(res.content)
            content = data['content']
            return cls(filepath, content, from_api=True)
        else:
            raise Exception('internal error')

    def decode(self):
        return base64.b64decode(self._content)


def name2path(name):
    t = name.split(':')
    if len(t) == 2:
        name, tag = t
    elif len(t) == 1:
        tag = 'latest'
    return "thrift/%s/%s.thrift" % (name, tag)


def push(name, localpath, ref=None):
    with open(localpath) as f:
        content = f.read()
    filepath = name2path(name)

    f = RepositoryFile.get(filepath)
    if f is None:
        f = RepositoryFile(filepath)
    f.save(content=content)


def pull(name, ref=None):
    filepath = name2path(name)

    f = RepositoryFile.get(filepath)
    if f is None:
        print("Error response from gitlab: %s file not found" % filepath)
        sys.exit(1)
    print(f.decode())


def main():
    parser = argparse.ArgumentParser()

    sb = parser.add_subparsers(dest="command")

    # token command
    # p = sb.add_parser("config")
    # p.add_argument("pid", help="gitlab project id")
    # p.add_argument("token", help="gitlab api access token")

    # pull command
    p = sb.add_parser("pull")
    p.add_argument("name", help="name (with tag)")
    p.add_argument("-b", "--branch", help="ref branch")

    # push command
    p = sb.add_parser("push")
    p.add_argument("name", help="name")
    p.add_argument("file", help="thrift file")

    args = parser.parse_args()

    if args.command == "push":
        return push(args.name, args.file)
    elif args.command == "pull":
        return pull(args.name, ref=args.branch)


if __name__ == '__main__':
    push('user:69', 'user.thrift')
