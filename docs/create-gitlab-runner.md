### Создание сети и хранилища кэша для бегунков gitlab-runner-а.

1. Создание сети:
```bash
docker network create gitlab-network
```
---------
2. Запуск minio, который будет хранилищем для кэша:
```bash
docker run -d --name minio \
  --restart unless-stopped \
  --network gitlab-network \
  -e "MINIO_ROOT_USER=<your user>" \
  -e "MINIO_ROOT_PASSWORD=<your password>" \
  -v minio_data:/data \
  minio/minio server /data
```
### ============================================================

### Создание Gitlab runner-а.

1. Создаем том для хранения сертификатов (_certs_) и настроек конфигураций (_config.toml_):
```bash
docker volume create gitlab-runner-config
```

Без создания тома, после перезапуска контейнера _gitlab-runner_ все настройки раннеров **потеряются** (_соотв-но и раннеры перестанут функционировать_).

-----------------------------------------------------------
2. Настраиваем, создаем и запускает контейнер gitlab-runner:
```bash
docker run -d --name gitlab-runner \
  --restart unless-stopped \
  --network gitlab-network \
  -v gitlab-runner-config:/etc/gitlab-runner \
  -v /var/run/docker.sock:/var/run/docker.sock gitlab/gitlab-runner:alpine
```

В этой команде ключевым моментом является указания **тома** _gitlab-runner-config_, куда контейнер будет записывать и читать все данные.

-----------------------------------------
3. Создаем раннеры:

Выберите либо флаг `--docker-privileged` либо укажите том `--docker-volumes "/var/run/docker.sock:/var/run/docker.sock"`, если хотите \
делать _build_ приложения на gitlab без **kaniko**.
```bash
  docker run --rm -it \
  -v gitlab-runner-config:/etc/gitlab-runner gitlab/gitlab-runner:alpine register \
  --non-interactive \
  --url <Runner registration URL> \
  --registration-token <Registration token> \
  --executor docker \
  --description "Описание для вашего раннера" \
  --tag-list "Тэг для вашего раннера" \
  --docker-image alpine:latest \
  --docker-privileged \
  --docker-volumes "/var/run/docker.sock:/var/run/docker.sock"
```

В этой команде так же указываем **том** _gitlab-runner-config_, туда будет помещён файл _config.toml_ в нём будет храниться конфигурация раннера. \
**Адрес** (_url_) gitlab и **токен** для регистрации раннера в gitlab найдете по пути: \
_Settings -> CI/CD -> Runners -> Specific runners_.

### ============================================================

### Создание bucket в minio (в нём будет храниться кэш):
1. Настройка соединения с _MinIO_:
```bash
mc alias set local http://localhost:9000 <your user> <your password>
```
2. Создание _bucket-а_:
```bash
mc mb local/gitlab-runner-cache
```
3. Проверка:
```bash
mc ls local
```
4. По пути _/etc/gitlab-runner_ отредактируем конфигурацию бегунка в файле **config.toml**:
```toml
[[runners]]
  name = "Your desciption runner"
  url = "Runner registration URL"
  id = 10
  token = "Registration token"
  token_obtained_at = 2024-10-31T12:44:44Z
  token_expires_at = 0001-01-01T00:00:00Z
  executor = "docker"
  [runners.custom_build_dir]
  [runners.cache]
    Type = "s3"
    Shared = true
    MaxUploadedArchiveSize = 0
    [runners.cache.s3]
      ServerAddress = "<address-minio>:9000"
      AccessKey = "your user"
      SecretKey = "your password"
      BucketName = "gitlab-runner-cache"
      BucketLocation = "us-east-1"
      Insecure = true
    [runners.cache.gcs]
    [runners.cache.azure]
  [runners.docker]
    tls_verify = false
    image = "alpine:latest"
    privileged = false
    disable_entrypoint_overwrite = false
    oom_kill_disable = false
    disable_cache = true
    volumes = []
    network_mode = "gitlab-network"
    shm_size = 0
    network_mtu = 0
```
> [!NOTE]
> Чтобы узнать какой адрес у MiNIO зайдите в его контейнер, раздел Files, путь etc/hosts, \
> последним в списке будет его адрес "address hash".

Этот бегунок отключен от локального кэша, так как мы используем _MinIO_. С помощью параметра "_disable_cache = true_" и \
удаления тома "_/cache_" оставив пустой список, это нужно, чтобы не возникало в логах предупреждения об отключении \
локального кэша.