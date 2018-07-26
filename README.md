# GT (鸡腿🍗谐音，同时致敬 ET）

Slack app，统计被加的 🍗 数（reaction）。

Inspired by [HeyTaco](https://www.heytaco.chat/), follow [Slack-Python-Onboarding-Tutorial: a simple python onboarding bot and tutorial for Slack](https://github.com/slackapi/Slack-Python-Onboarding-Tutorial).

## Setup Database
```bash
DB_NAME="gt" DB_USER="root" DB_HOST="localhost" DB_PORT=3307 DB_PASSWORD=""  pipenv run python commands/create_db_and_tables.py
```


## Run
```bash
> SM_SLACK_API_TOKEN="xxxxxxx" DB_NAME="gt" DB_USER="root" DB_HOST="localhost" DB_PORT=3307 DB_PASSWORD="" ./run
```

## Setup Development Environment
```bash
> pipenv update
```

## Development
参考 `gt/plugins/chickens.py`，增加新的 plugin。然后将新写的 plugin 增加到 `local_settings.py` 即可。

参考文档： http://slack-machine.readthedocs.io/en/latest/plugins/basics.html
