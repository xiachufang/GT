# GT (鸡腿🍗谐音，同时致敬 ET）

Slack app，统计被加的 🍗 数（reaction）。

Inspired by [HeyTaco](https://www.heytaco.chat/), follow [Slack-Python-Onboarding-Tutorial: a simple python onboarding bot and tutorial for Slack](https://github.com/slackapi/Slack-Python-Onboarding-Tutorial).

## Setup Database
```bash
> GT_DB_NAME="gt" GT_DB_USER="root" GT_DB_HOST="localhost" GT_DB_PORT=3307 GT_DB_PASSWORD=""  pipenv run python commands/create_db_and_tables.py
```


## Setup Environment
```bash
> pipenv install -d
```

## Run
```bash
> SM_SLACK_API_TOKEN="xxxxxxx" GT_DB_NAME="gt" GT_DB_USER="root" GT_DB_HOST="localhost" GT_DB_PORT=3307 DB_PASSWORD="" ./run
```

## Development
参考 `gt/plugins/chickens.py`，增加新的 plugin。然后将新写的 plugin 增加到 `local_settings.py` 即可。

参考文档： http://slack-machine.readthedocs.io/en/latest/plugins/basics.html

## Docker
```bash
# docker build . -t wg
# docker run wg
```
