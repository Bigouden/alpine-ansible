#!/usr/bin/env python3
#coding: utf-8
'''entrypoint.py'''

import argparse
import os
import logging
import sys
from urllib.parse import urlparse
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError

def check_url(value):
    '''Check for legit HTTP(S) Git Repository URL'''
    url = urlparse(value)
    if url.scheme not in ['http', 'https']:
        msg = f"{url.scheme} is an invalid scheme for Git HTTP(S) Repository URL."
        raise argparse.ArgumentTypeError(msg)
    if not url.netloc:
        msg = "Invalid Git HTTP(S) Repository URL."
        raise argparse.ArgumentTypeError(msg)
    if not url.path:
        msg = "Git HTTP(S) Repository URL must contain a path."
        raise argparse.ArgumentTypeError(msg)
    return url

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    level=logging.INFO)

PARSER = argparse.ArgumentParser()
PARSER.add_argument("--url", help="Git HTTP(S) Repository URL",
                    default="https://gitlab.cer.ssaim.dnum.minint.fr/ansible/skeleton.git",
                    type=check_url)
PARSER.add_argument("--username", help="Git Username")
PARSER.add_argument("--password", help="Git Password")
PARSER.add_argument("--directory", help="Git Repository Directory", default="/etc/ansible/skeleton")
PARSER.add_argument("--shell", help="Unix Shell", default="/bin/sh")
PARSER.add_argument("--branch", help="Git Clone Branch", default="master")
ARGS = PARSER.parse_args()

def git(args):
    '''Manage Git Repository (configure, clone, ...)'''
    try:
        anonymous_url = f"{args.url.scheme}://{args.url.netloc}{args.url.path}"
        if args.username and args.password:
            git_url = f"{args.url.scheme}://{args.username}:{args.password}" \
                      f"@{args.url.netloc}{args.url.path}"
        else:
            git_url = anonymous_url
        Repo.clone_from(git_url, args.directory, branch=args.branch)
        msg = f"Cloning repository : {anonymous_url} ({args.branch}) into {args.directory}"
        logging.info(msg)
    except GitCommandError as exception:
        stderr = " ".join(exception.stderr.splitlines()[:-1])
        msg = f"Unable to clone repository: {git_url} ({stderr.strip()})"
        if "already exists and is not an empty directory." in stderr:
            os.chdir(args.directory)
            try:
                msg = f"Repository directory : {os.getcwd()} not empty"
                logging.info(msg)
                repo = Repo('.')
                if args.url.netloc in repo.remotes.origin.url:
                    repo.git.checkout(args.branch)
                    msg = f"Checkout branch : {args.branch}"
                    logging.info(msg)
                    msg = "Pulling origin"
                    logging.info(msg)
                    repo.remotes.origin.pull()
                    return
                msg = "git remote origin url mistmatch with git repository url:"
            except InvalidGitRepositoryError:
                msg = f"{os.getcwd()} is not empty and not a git repository."
            except GitCommandError as exception:
                msg = f"Unable to pull repository: {git_url} ({exception.stderr.strip()})"
        logging.critical(msg)
        sys.exit(1)

def shell(args):
    '''Change Directory and Start Shell'''
    msg = f"Changing directory: {args.directory}"
    logging.info(msg)
    os.chdir(args.directory)
    msg = f"Starting shell: {args.shell}"
    logging.info(msg)
    os.system(args.shell)

if __name__ == '__main__':
    git(ARGS)
    shell(ARGS)
