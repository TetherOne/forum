Функционал сайта:

Сайт представляет собой форум для публикации статей (аналог Habr).

На главной странице сайта пользователи могут воспользоваться полем поиска для поиска статей по названию
и функцией фильтрации по категориям для поиска интересующих статей.

На сайте существуют различные категории статей: программирование, спорт, кулинария.
Планируется постоянное добавление новых категорий, чтобы удовлетворить различные интересы пользователей.

Новые пользователи могут просматривать профили других пользователей, чтобы видеть их статьи и информацию об авторе.
Однако, если пользователь хочет опубликовать свою собственную статью, он должен зарегистрироваться (после успешной
регистрации пользователя автоматически переводит в его профиль), указав никнейм,
электронную почту и пароль.

После регистрации и аутентификации пользователь получает возможность публиковать новые статьи,
редактировать или удалять уже существующие. Пользователи также могут установить или удалить себе аватарку,
что делает их профиль более персонализированным.

Также при разработке сайта было написанно API для взаимодействия с пользователями и статьями.


![Image alt](https://github.com/TetherOne/forum/raw/master/image.png)

-------------------------------------------------------------------------------------------------------------------------------------------

•	Сайт написан на Flask 3.0.0 с использованием базы данных PostgreSQL

•	Для работы с моделями базы данных были использованы SQLAlchemy 2.0.23 + alembic
