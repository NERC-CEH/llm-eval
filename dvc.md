# DVC Notes
Notes on how to accomplish various operation using [DVC](https://dvc.org/). Most of these are just distilled notes from the [DVC documentation](https://dvc.org/doc).

This document guides you through working with the `llm-eval` repo and working with DVC backed by a [JASMIN object store](https://help.jasmin.ac.uk/docs/short-term-project-storage/using-the-jasmin-object-store/). The instruction can then be taken and applied to any other repository that you may want to setup to work with DVC

# Working with this repository
## Setup
### Clone this repo
```shell
$ git clone git@github.com:NERC-CEH/llm-eval.git
$ cd llm-eval
```

### Installing DVC
DVC can be installed using `pip`, this will provide the basic CLI needed to execute commands with DVC. The recomended way if working with this repository is to create a new python virtual environment and then install the appropriate DVC packages via the `requirements.txt` file:
```shell
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```
If you are working on a different repository the packages can be installed seperately:
```shell
$ pip install dvc
$ pip install dvc[s3]
```
> DVC remotes backed by various other technologies (besides s3) can be used. See the [DVC documentation](https://dvc.org/doc/user-guide/data-management/remote-storage#supported-storage-types) for details.

### Connecting to JASMIN object storage
#### Request access to JASMIN object store
This repository has a corresponding object store on JASMIN `llm-eval-o`. To work with the data in this repository managed by DVC you must request access to the object store from the object store manager [Matt Coole](mailto:matcoo@ceh.ac.uk).

Once you have been granted `USER` access, log in through the [JASMIN Object Store Portal](https://s3-portal.jasmin.ac.uk/object-store/) and create an access key for the `llm-eval-o` object store. Instructions for creating keys can be found in the [JASMIN Documentation](https://help.jasmin.ac.uk/docs/short-term-project-storage/using-the-jasmin-object-store/#creating-an-access-key-and-secret).
> Make sure you store your secret somewhere safe as you will not be able to view it again after the initial creation of your key.

#### Configure Credentials
Once you have access to the object store and have created a key you will need to setup your credentials:
```shell
$ dvc remote modify --local jasmin access_key_id '<ACCES_KEY_ID>'
$ dvc remote modify --local jasmin secret_access_key '<KEY_SECRET>'
```
> **Note:** The configuration for DVC is tracked in `.dvc/config` but your credentials should be stored in a seperate file (`.dvc/config.local`) which should not be tracked by version control to avoid secrets being leaked. Make sure to use `--local` when configuring credentials.

> **WARNING:** There appears to be a subtle bug in DVC credentials management where any kind of quote character `'"` in your secret key will invalidate your credentials and you will receive a `403: Forbidden` error when attempting to access the JASMIN object store. The only way I've found around this so far is to keep generating new access keys until you get one without any quote characters...

## Pulling data
Assuming that configuration and credentials have been set up correctly you should now be able to pull the data that is tracked by DVC from the JASMIN object store. This is done using the `dvc pull` command.
```shell
$ dvc pull
```
You should now be able to see the `data` folder and contents:
```
data
├── evaluation-sets
│   ├── eidc-eval.csv
│   └── eidc-eval-sample.csv
└── synthetic-datasets
    └── eidc_rag_test_set.csv
```

## Making changes
To make changes to your data use `dvc add` on the local file and then use `dvc push` to push to the remote store. It is then important to commit the `.dvc` files to git as well e.g.
```shell
$ dvc add my-data-file.csv
$ dvc push
$ git commit my-data-file.csv.dvc -m 'Updated data file'
```
`my-data-file.csv.dvc` is a place holder that DVC creates to tell it about the files/folder being tracked. This place holder will be tracked by git and the actual data tracked by DVC.

DVC should also automatically add the file/directory to `.gitignore` so it won't end up being accidentally tracked in git as well.

### Moving data from git to DVC
Any files or folders that you add to DVC must not be tracked by git. To switch from tracking a file with git to DVC, first untrack it with git:
```shell
$ git rm --cached data-file-in-git.csv
```
then follow the steps [above](#Making changes) to add the file(s) to be tracked by DVC.

> Note: Whilst `dvc` commands seem to somewhat mirror `git` commands, there doesn't seem to be quite the same concept of a staging area. I would suggest that `dvc add` is more like an amalgamation (in DVC) of `git add` + `git commit`.

## Checking out versions
To switch between versions of your data tracked by DVC you can simply use `git checkout` as you typically would to checkout a particular version of code and then follow this up with `dvc checkout` to checkout the corresponding version of the data e.g.
```shell
$ git checkout c474fcc
$ dvc checkout
```

# Setting up a new repository
Up until here it was assumed you were working with a repository already setup with DVC, but to setup DVC on your own git repository there are just a few initial steps to configure:
## Initialise
To set up your own git repository to track any data files using DVC use `dvc init` in the repository's directory.
```shell
$ dvc init
```
You will see a `.dvc/` directory and a `.dvcignore` file which you should add to you version controlled files.

## Add remote
Now add a bucket to be used as a remote (make sure you create the bucket in your object store first):
```shell
dvc remote add jasmin s3://test-dvc
```
This will initially set up the remote to use the `test-dvc` bucket (check the config in `.dvc/config`).

Next you need to add the endpoint URL, if you are using a JASMIN object store this should look something like this:
```shell
dvc remote modify myremote endpointurl https://my-test-store-o.s3-ext.jc.rl.ac.uk
```
Where your object store is called `my-test-store`.

## Configure Credentials
Finally you can configure your credentials as described [above](#Connecting to JASMIN object storage).
