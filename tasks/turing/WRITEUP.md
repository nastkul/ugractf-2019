# Turing Complete: Write-up

Существует много способов решить это задание — нужно было запрограммировать ровно то, что 
описано в условии.

Например, можно делать так:

1. Поставить в начале и конце числа маркеры (в коде это символы `s` и `e`)
2. Затем брать по одной цифре с конца числа и дописывать её после `e`
3. Как только встретится маркер начала `s`, стереть маркеры и завершить работу.

На данном в условии языке это записывается следующим образом:

```
start 0 -> put 0 <
start 1 -> put 1 <

put _ -> goend s >

goend 0 -> goend 0 >
goend 1 -> goend 1 >
goend _ -> take e <

take _ -> take _ <
take 0 -> move0 _ >
take 1 -> move1 _ >
take s -> cleane _ >

move0 _ -> move0 _ >
move0 e -> put0 e >

move1 _ -> move1 _ >
move1 e -> put1 e >

put0 0 -> put0 0 >
put0 1 -> put0 1 >
put0 _ -> goback 0 <

put1 0 -> put1 0 >
put1 1 -> put1 1 >
put1 _ -> goback 1 <

goback 0 -> goback 0 <
goback 1 -> goback 1 <
goback e -> take e <

cleane _ -> cleane _ >
cleane e -> finish _ !
```

Флаг: **ugra\_turing_code\_magic**
