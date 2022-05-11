# Публикация комиксов

Данный проект скачивает комиксы с сайта [xkcd.com](https://xkcd.com/) и автоматически выкладывает их на стену сообщества Вконтакте.

### Как установить

После скачивания архива с кодом его необходимо распаковать в пустую папку. После этого необходимо скачать все сторонние библиотеки, открыв папку в консоли и написав в неё:
```
pip install -r requirements.txt
```
После установки сторонних библиотек, необходимо создать в корневой папке файл с названием `.env` и записать в него данные в виде:

```
CLIENT_ID=id вашего приложения
ACCESS_TOKEN=ваш ключ доступа пользоватея
GROUP_ID=id вашего сообщества
USER_ID=id вашего пользователя
```

Приложение Вконтакте можно создать [тут](https://dev.vk.com/)

Получить ключ доступа пользователя можно следуя инструкции написаной [тут](https://dev.vk.com/api/access-token/implicit-flow-user)

Узнать id вашего сообщества и пользователя можно [тут](https://regvk.com/id/)

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
