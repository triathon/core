```doc
│  .gitignore
│  dev.Dockerfile
│  Directory.md
│  README.md
│  README_ZH.md
│  requirementsDev.txt
│
├─backend                                           django project
│  │  manage.py                                     django runserver file
│  │  pyproject.toml
│  │  requirements.txt                              pip pack
│  │
│  ├─api                                            view
│  │  │  admin.py
│  │  │  apps.py
│  │  │  models.py
│  │  │  serializers.py
│  │  │  tests.py
│  │  │  urls.py
│  │  │  views.py
│  │  │  __init__.py
│  │  │
│  │  ├─migrations
│  │  │  │  0001_initial.py
│  │  │  │  0002_auto_20220929_1003.py
│  │  │  │  0003_auto_20220929_1005.py
│  │  │  └─ __init__.py
│  │  │
│  │  └─tools
│  │     │  contract_helper.py                      download merge network contract
│  │     │  merge_contract.py                       merge local contract
│  │     │  pull_contract_pack.py                   download contract pack
│  │     │
│  │     └─multi_file_contract
│  │            01_04_RoundIdFetcher.sol
│  │            02_04_AggregatorV2V3Interface.sol
│  │            03_04_AggregatorInterface.sol
│  │            04_04_AggregatorV3Interface.sol
│  │
│  ├─backend
│  │  │  asgi.py
│  │  │  settings.py                                django setting
│  │  │  urls.py                                    route
│  │  │  wsgi.py
│  │  └─ __init__.py
│  │
│  ├─conf                                           config
│  │  │  conf.json                                  config file
│  │  └─ __init__.py
│  │
│  ├─t
│  │  │  config.py                                  parsing the configuration
│  │  └─ make_sign.py                               generating signature
│  │
│  └─upload_contracts
├─coreslither                                       slither
│  │  coreslither.yml
│  │
│  ├─build
│  │  └─coreslither
│  │      │  Dockerfile
│  │      │  index.py
│  │      │  requirements.txt
│  │      │  template.yml
│  │      │
│  │      └─function
│  │          │  config.conf
│  │          │  handler.py
│  │          │  handler_test.py
│  │          │  requirements.txt
│  │          │  tox.ini
│  │          │  __init__.py
│  │          │
│  │          ├─models
│  │          │  │  module.py
│  │          │  └─ __init__.py
│  │          │
│  │          └─token_audit
│  │             │  contract_helper.py
│  │             │  helper_test.py
│  │             └─ __init__.py
│  │
│  ├─coreslither
│  │  │  config.conf                                slither config
│  │  │  handler.py
│  │  │  handler_test.py
│  │  │  requirements.txt
│  │  │  tox.ini
│  │  │
│  │  ├─models
│  │  │  │  module.py
│  │  │  └─ __init__.py
│  │  │
│  │  └─token_audit
│  │     │  contract_helper.py
│  │     │  helper_test.py
│  │     └─ __init__.py
│  │
│  └─template
│      └─python3-flask-debian
│          │  Dockerfile
│          │  index.py
│          │  requirements.txt
│          │  template.yml
│          │
│          └─function
│                  handler.py
│                  handler_test.py
│                  requirements.txt
│                  tox.ini
│                  __init__.py
│
├─coresmartian                                      smartian
│  │  coresmartian.yml
│  │
│  ├─coresmartian
│  │  │  config.conf                                smartion config
│  │  │  handler.py
│  │  │  handler_test.py
│  │  │  requirements.txt
│  │  │  tox.ini
│  │  │  __init__.py
│  │  │
│  │  ├─models
│  │  │  │  module.py
│  │  │  └─ __init__.py
│  │  │
│  │  └─utils
│  │          get_contract.py
│  │          __init__.py
│  │
│  └─template
│      └─python3-flask-debian
│          │  Dockerfile
│          │  index.py
│          │  requirements.txt
│          │  template.yml
│          │
│          └─function
│                  handler.py
│                  handler_test.py
│                  requirements.txt
│                  tox.ini
│                  __init__.py
│
└─corethril                                         mythril
    │  corethril.yml
    │
    ├─corethril
    │  │  config.conf                               mythril config
    │  │  handler.py
    │  │  handler_test.py
    │  │  requirements.txt
    │  │  tox.ini
    │  │  __init__.py
    │  │
    │  ├─models
    │  │  └─ module.py
    │  │
    │  ├─utils
    │  │      get_contract.py
    │  └─     __init__.py
    │
    └─template
        └─python3-flask-debian
            │  Dockerfile
            │  index.py
            │  requirements.txt
            │  template.yml
            │
            └─function
                    handler.py
                    handler_test.py
                    requirements.txt
                    tox.ini
                    __init__.py
```