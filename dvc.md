# DVC Notes
Notes on how to accomplish various operation using DVC. Most of these are just distilled notes from the [DVC documentation](https://dvc.org/doc).

## Setting up the repository
To set up a git repository to track any data files using DVC use `dvc init` in the repository's directory, then `dvc remote add` to add a remote store to for your DVC tracked data e.g.
```shell
$ dvc init
$ dvc remote add -d storage s3://mybucket/dvcstore
```
This will initialise the repository for use with DVC and setup a `remote` called `storage` in the S3 bucket `s3://mybucket/dvcstore` and set it as the default remote to use `-d`.

You will also see a `.dvc/` directory and a `.dvcignore` file which you should add to you version controlled files.

## Making changes
To make changes to your data use `dvc add` on the local file and then use `dvc push` to push to the remote store. It is then important to commit the `.dvc` object to git that is setup to track this file as well e.g.
```shell
$ dvc add data.csv
$ dvc push
$ git commit data.csv.dvc -m 'Updated data file'
```
> Note: Whilst `dvc` commands seem to somewhat mirror `git` commands, there doesn't seem to be quite the same concept of a staging area. I would suggest that `dvc add` is more like an amalgamation (in DVC) of `git add` + `git commit`.

## Checking out versions
To switch between versions of your data tracked by DVC you can simply use `git checkout` as you typically would to checkout a particular version of code and then follow this up with `dvc checkout` to checkout the corresponding version of the data e.g.
```shell
$ git checkout c474fcc
$ dvc checkout
```