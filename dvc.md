# DVC Notes
Notes on how to accomplish various operation using DVC. Most of these are just distilled notes from the [DVC documentation](https://dvc.org/doc).

## Installation
DVC can be installed using `pip`, this will provide the basic CLI needed to execute commands with DVC:
```shell
$ pip install dvc
```
As well as the main package you will also need to install a package to work with the particular remote that is intended to store the data files tracked by dvc e.g. to work with dvc data stored in an S3 bucket:
```shell
$ pip install dvc[s3]
```
Hopefully if working with an existing repo the `requirements.txt` will contain the appropriate package for dvc tracked data.

## Setting up a new repository
To set up a git repository to track any data files using DVC use `dvc init` in the repository's directory, then `dvc remote add` to add a remote store to for your DVC tracked data e.g.
```shell
$ dvc init
$ dvc remote add -d storage s3://mybucket/dvcstore
```
This will initialise the repository for use with DVC and setup a `remote` called `storage` in the S3 bucket `s3://mybucket/dvcstore` and set it as the default remote to use `-d`.

You will also see a `.dvc/` directory and a `.dvcignore` file which you should add to you version controlled files.

## Cloning a repository
When cloning a repository that is set up with data tracked by dvc, use `dvc pull` to download the data files tracked by dvc from the remote:
```shell
$ git clone git@github.com:NERC-CEH/llm-eval.git
$ cd llm-eval
$ dvc pull
```

## Making changes
To make changes to your data use `dvc add` on the local file and then use `dvc push` to push to the remote store. It is then important to commit the `.dvc` object to git that is setup to track this file as well e.g.
```shell
$ dvc add data.csv
$ dvc push
$ git commit data.csv.dvc -m 'Updated data file'
```
`data.csv.dvc` is a place holder that dvc creates to tell it about the files/folder being tracked. This place holder will be tracked by git and the actual data tracked by dvc.

### Moving data from git to dvc
Any files or folders that you add to dvc must not be tracked by git. To switch from tracking a file with git to dvc, first untrack it with git:
```shell
$ git rm --cached data.csv
```
then follow the steps above to add the file(s) to be tracked by dvc.

> Note: Whilst `dvc` commands seem to somewhat mirror `git` commands, there doesn't seem to be quite the same concept of a staging area. I would suggest that `dvc add` is more like an amalgamation (in DVC) of `git add` + `git commit`.

## Checking out versions
To switch between versions of your data tracked by DVC you can simply use `git checkout` as you typically would to checkout a particular version of code and then follow this up with `dvc checkout` to checkout the corresponding version of the data e.g.
```shell
$ git checkout c474fcc
$ dvc checkout
```