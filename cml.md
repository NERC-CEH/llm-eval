# CML

## Self-hosted runner
To setup a self-hosted runner to perform github actions with CML on a local machine with a GPU access. You will need to make sure that `docker` and `node` are installed, then run:
```shell
$ sudo npm install --location=global @dvcorg/cml
```
### Starting the runner
To start the runner you will need to create gh access token with `repo` and `workflow` permissions. Then run:
```shell
$ cml runner launch \
  --repo=$REPO_URL \
  --token=$ACCESS_TOKEN \
  --labels="cml,gpu" \
  --idle-timeout=3000
```
replacing `REPO_URL` with your github repository url and `ACCESS_TOKEN` with you gh access token (created via `<USER> > Settings > Developer settings > Personal access tokens > Tokens (classic) > Generate new token (classic)`). Note that `REPO_URL` should **not** include the `.git` suffix. 

The runner should provide a confirmation message when it is started, but you can check that it is available to your repository by going to github `<REPOSITORY> > Settings > Actions > Runners` and you should see the runner listed.

To ensure that the runner can also write back to gh actions you must set read/write permissions on the repository via `<REPOSITORY> > Settings > Actions > General > Workflow permissions > Read and write permissions`.

### GH Action
With the runner available you should now be able to create a workflow to utilise it. Below is an example of a basic action to use the local runner and print the available GPU spec and details:
```yaml
name: test_gpu
on: [push]
jobs:
  run:
    runs-on: [self-hosted,cml,gpu]
    steps:
      - uses: actions/checkout@v3
      - uses: iterative/setup-cml@v1
      - name: Chek GPU spec
        env:
          REPO_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          nvidia-smi
```
Save this into `.github/workflows/test_gpu.yaml` and open a pull request. The action should execute and the output should provide you details about the available GPU.
