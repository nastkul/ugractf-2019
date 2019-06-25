# Публичные секреты: Write-up

Подключившись на указанный хост и порт, мы видим, что нам выдаются параметры *n*, *e* — публичный ключ RSA и зашифрованное сообщение.

По всей видимости, каждый раз шифруется одно и то же сообщение, но разными публичными ключами. При этом во всех ключах публичная экспонента *e* равна 17.

Погуглив информацию о данном алгоритме, находим [статью в Википедии](https://en.wikipedia.org/wiki/RSA_%28cryptosystem%29#Attacks_against_plain_RSA), в которой рассказывается про различные виды атак на RSA. Одна из атак:

> If the same clear text message is sent to e or more recipients in an encrypted way, and the receivers share the same exponent e, but different p, q, and therefore n, then it is easy to decrypt the original clear text message via the Chinese remainder theorem. Johan Håstad noticed that this attack is possible even if the cleartexts are not equal, but the attacker knows a linear relation between them. This attack was later improved by Don Coppersmith.

Также гуглятся и утилиты для автоматического расшифровывания текстов, но почему-то многие из них написаны для `e = 3`. Поэтому придется самостоятельно разобраться, как работает эта атака.

<!-- TODO: LaTeX formulas -->

Атака Хастада основана на [Китайской теореме об остатках](https://en.wikipedia.org/wiki/Chinese_remainder_theorem), которая гласит, что если у нас есть число *M*, которое при делении на попарно взаимно простые модули ![p\_1, p\_2, ..., p\_n](https://latex.codecogs.com/svg.latex?p_1%2C%20p_2%2C%20%5Cldots%2C%20p_n) даёт остатки ![m\_1, m\_2, ...m\_n](https://latex.codecogs.com/svg.latex?m_1%2C%20m_2%2C%20%5Cldots%2C%20m_n), то мы можем найти остаток от деления *M* на ![p\_1p\_2...p\_n](https://latex.codecogs.com/svg.latex?p_1p_2%7B%5Cldots%7Dp_n).

Шифрование в RSA происходит по формуле: ![m = c^e (mod n)](https://latex.codecogs.com/svg.latex?m%20%3D%20c%5Ee%20%5Cmod%20n). Пусть у нас есть хотя бы e сообщений, то есть остатки от деления ![c^e](https://latex.codecogs.com/svg.latex?c%5Ee) на ![n\_1, n\_2, ..., n\_e](https://latex.codecogs.com/svg.latex?n_1%2C%20n_2%2C%20%5Cldots%2C%20n_e). Все ![n\_i](https://latex.codecogs.com/svg.latex?n_i) взаимно просты, иначе мы бы смогли быстро найти НОД двух модулей и разложить их на делители. Следовательно, мы сможем найти остаток от деления ![c^e](https://latex.codecogs.com/svg.latex?c%5Ee) на ![n\_1n\_2...n\_e](https://latex.codecogs.com/svg.latex?n_1n_2%7B%5Cldots%7Dn_e) по данной теореме.

Осталось заметить, что поскольку ![для всех i c &lt; n\_i](https://latex.codecogs.com/svg.latex?%5Cforall%20i%3A%20c%20%3C%20n_i), то ![c^e &lt; n\_1n\_2...n\_e](https://latex.codecogs.com/svg.latex?c%5Ee%20%3C%20n_1n_2%7B%5Cldots%7Dn_e). Но тогда остаток от деления ![c^e](https://latex.codecogs.com/svg.latex?c%5Ee) на ![n\_1n\_2...n\_e](https://latex.codecogs.com/svg.latex?n_1n_2%7B%5Cldots%7Dn_e), который мы уже знаем, и будет в точности равен ![c^e](https://latex.codecogs.com/svg.latex?c%5Ee). Останется просто извлечь корень степени e.

Для поиска остатка воспользуемся [алгоритмом Гарнера](https://ru.wikipedia.org/wiki/Китайская_теорема_об_остатках#Алгоритм_Гарнера).

> [Код эксплоита](exploit.py)

Флаг: **ugra_in_elliptic_we_trust**
