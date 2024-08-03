# Setup GitFlic

<!-- ### Prerequises
- Предполагается, что вы используете git bash -->


- Open Git Bash and generate ssh key using ed25519, leave default paths and omit passphrase (press Enter)

```shell
$ ssh-keygen -t ed25519
```

- Find your key in `$HOME/.ssh/*.pub` 

- Enroll key to [gitflick](https://gitflic.ru/settings/keys) using nir_audit_ib@mail.ru account

- Setup git config (email, name)

```shell
git config --global user.name "User"
git config --global user.email "User.Mail"
```

- `git clone git@gitflic.ru:zov/compliance-audit.git`

- Try to push new commit to new branch (e.g. khandzhyan/test)