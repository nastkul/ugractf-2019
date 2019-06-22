# Сразу видно, олдскул: Write-up

В этом таске был предоставлен тот же самый дамп, что и в задании [Секретные архивы](../anonymous/). От участников требовалось достать второй флаг.

В TCP-стриме 0 видим, что кроме архива также предлагается получить CTF-флаги:

    1CTF Flags	/flags/list	ugractf.ru	5005

Но в трафике нигде запроса к данному ресурсу нет. Попробуем упростить себе задачу: все IP-адреса в задании публичные, так что просто попробуем зайти на тот же ресурс со своего компьютера. Можно было заметить, что IP-адрес сервера — `193.138.89.12`. Именно на этом же хосте расположен `ugractf.ru`, и это неспроста.

Удивительно, но ресурс доступен:

    $ nc -v ugractf.ru 5005
    Connection to ugractf.ru 5005 port [tcp/*] succeeded!

Осталось понять, какой протокол использовать для взаимодействия с сервером. На самом деле, этот протокол называется Gopher, но это знать не обязательно. Из стримов можно узнать, что достаточно отправить на сервер путь к ресурсу и получить ресурс в ответ. Поэтому можно решить таск с помощью утилиты `nc`:

    $ nc -v ugractf.ru 5005
    Connection to ugractf.ru 5005 port [tcp/*] succeeded!
    /flags/list
    iPlease use the following navigation to get the flag:
    
    1Position 0     /flags/880862219        ugractf.ru      5005
    1Position 1     /flags/441894432        ugractf.ru      5005
    1Position 2     /flags/801859882        ugractf.ru      5005
    1Position 3     /flags/364036117        ugractf.ru      5005
    1Position 4     /flags/674411178        ugractf.ru      5005
    1Position 5     /flags/737551777        ugractf.ru      5005
    1Position 6     /flags/768012196        ugractf.ru      5005
    1Position 7     /flags/949340140        ugractf.ru      5005
    1Position 8     /flags/181556015        ugractf.ru      5005
    1Position 9     /flags/121810545        ugractf.ru      5005
    1Position 10    /flags/188358394        ugractf.ru      5005
    1Position 11    /flags/491110286        ugractf.ru      5005
    1Position 12    /flags/287193782        ugractf.ru      5005
    1Position 13    /flags/423104753        ugractf.ru      5005
    1Position 14    /flags/700767134        ugractf.ru      5005
    1Position 15    /flags/125524583        ugractf.ru      5005
    1Position 16    /flags/948634601        ugractf.ru      5005
    1Position 17    /flags/350842878        ugractf.ru      5005
    1Position 18    /flags/217159199        ugractf.ru      5005
    1Position 19    /flags/907989366        ugractf.ru      5005
    1Position 20    /flags/199114314        ugractf.ru      5005
    1Position 21    /flags/163236934        ugractf.ru      5005
    1Position 22    /flags/963796280        ugractf.ru      5005
    1Position 23    /flags/738257149        ugractf.ru      5005

Какие-то позиции... Давайте узнаем, что внутри:

    $ nc -v ugractf.ru 5005
    Connection to ugractf.ru 5005 port [tcp/*] succeeded!
    /flags/880862219
    iLetter 0 is u

Похоже на первую букву флага. Собираем все позиции и получаем флаг.

Флаг: **ugra_i_like_gopher_links**
