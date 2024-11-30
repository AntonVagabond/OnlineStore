# ========= СОЗДАНИЕ GITLAB RUNNER =======

1. Создаем том для хранения сертификатов (_certs_) и настроек конфигураций (_config.toml_):
```bash
docker volume create gitlab-runner-config
```

Без создания тома, после перезапуска контейнера _gitlab-runner_ все настройки раннеров **потеряются** (_соотв-но и раннеры перестанут функционировать_).

-----------------------------------------------------------
2. Настраиваем, создаем и запускает контейнер gitlab-runner:
```bash
docker run -d --name gitlab-runner --restart always -v gitlab-runner-config:/etc/gitlab-runner -v /var/run/docker.sock:/var/run/docker.sock gitlab/gitlab-runner:alpine
```

В этой команде ключевым моментом является указания **тома** _gitlab-runner-config_, куда контейнер будет записывать и читать все данные.

-----------------------------------------
3. Создаем раннеры:
# Настройка бегунка (runner) не идеальная.
# Устанавливаете флаг --docker-privileged либо --docker-volumes "/var/run/docker.sock:/var/run/docker.sock".
```bash
  docker run --rm -it -v gitlab-runner-config:/etc/gitlab-runner gitlab/gitlab-runner:alpine register \
  --non-interactive \
  --url <Runner registration URL> \
  --registration-token <Registration token> \
  --executor docker \
  --description "Описание для вашего раннера" \
  --tag-list "Тэг для вашего раннера" \
  --docker-image alpine:latest \
  --docker-privileged \
  --docker-volumes "gitlab-runner-cache:/cache" \
  --docker-volumes "/var/run/docker.sock:/var/run/docker.sock"
```

В этой команде так же указываем **том** _gitlab-runner-config_, туда будет помещён файл _config.toml_ в нём будет храниться конфигурация раннера.
**Адрес** (_url_) gitlab и **токен** для регистрации раннера в gitlab найдете по пути: _Settings -> CI/CD -> Runners -> Specific runners_.

Источник информации [тут](https://habr.com/ru/articles/764568/).

# =========================================
