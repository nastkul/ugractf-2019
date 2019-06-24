# Леденящее дыхание: Write-up

[Видео](public/trump.mp4) состоит из 40 примерно равных по продолжительности сегментов с дыханием Трампа. С помощью поиска по картинкам можно выяснить, что это была речь 19 января 2019. Полное видео есть [на Ютубе](https://www.youtube.com/watch?v=_FqmGcERGrg), но там другие логотипы и, наверное, оно по-другому перекодировано. На видео из задания есть логотип сайта americanrhetoric.com, и там действительно [есть страница с оригинальным видео](https://americanrhetoric.com/speeches/donaldjtrumpbodersecurityplan.htm), а заодно текстом всей речи. Скачаем его.

В оригинальном видео Трамп не только дышит, но и говорит. Наверное, что-то важное. Попробуем найти те моменты, откуда вырезано дыхание. 

```python
import cv2
import numpy as np
import tqdm
import os
```

Для того, чтобы минимизировать влияние JPEG-сжатия на сравнение кадров, будем их предобрабатывать фильтром поиска границ — кадры будут превращаться в чёрно-белые контуры. Параметры взяты из [туториала про эдж-детект](https://blog.sicara.com/opencv-edge-detection-tutorial-7c3303f10788).

```python
def edge_filter(im):
    return cv2.Canny(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 60, 120)
```

Возьмём по одному кадру из каждого из 40 сегментов с дыханием, предобработаем и запомним их в переменную `samples`. 

```python
cap = cv2.VideoCapture('trump.mp4')
seg_positions = [int((cap.get(cv2.CAP_PROP_FRAME_COUNT) / 40) * (i + 0.5)) for i in range(40)]

samples = []
for n_frame in tqdm.tqdm(range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))):
    _, frame = cap.read()
    if n_frame in seg_positions:
        samples.append(edge_filter(frame))
```

Далее будем для каждого кадра оригинального видео считать расстояние до сэмплов (`np.linalg.norm` от поэлементной разницы двух кадров) и запоминать, где расстояние получилось наименьшим.

```python
ref_cap = cv2.VideoCapture('donaldjtrumpimmigrationcompromise.mp4')
best_frames = [(None, None) for _ in samples]
for n_frame in tqdm.tqdm_notebook(range(int(ref_cap.get(cv2.CAP_PROP_FRAME_COUNT)))):
    _, frame = ref_cap.read()
    frame = edge_filter(frame)

    for n_sample, sample in enumerate(samples):
        dist = np.linalg.norm(frame - sample)
        if best_frames[n_sample][1] is None or dist < best_frames[n_sample][1]:
            best_frames[n_sample] = (n_frame, dist)
```

Итак, у нас есть `best_frames`, в котором указаны номера кадров, наиболее похожих на оригинал:

```python
print([n for n, _ in best_frames])
```

```
[1921, 267, 8479, 2299, 24056, 23, 13929, 176, 2024, 1923, 2299, 24056, 2833, 2024, 12169, 24056, 10944, 13929, 15792, 24056, 2414, 15793, 2833, 2024, 24056, 2025, 15792, 175, 24056, 8480, 2299, 10944, 10943, 15792, 2832, 24056, 2413, 15792, 14059, 12169]
```

Отрежем, начиная с найденных позиций, сегменты по три секунды.

```python
for n_best, (best_frame, best_dist) in enumerate(best_frames):
    os.system("ffmpeg -ss %.3f -i donaldjtrumpimmigrationcompromise.mp4 -b:v 4096k -t 3 trump-part-%02d.mp4" %
              ((best_frame - 4) / 29.97, n_best))
```

Склеим их.

```bash
ffmpeg -f concat -safe 0 -i <(ls trump-part-*.mp4 | sed -E "s,.*,file '"$(pwd)"/&',") -map 0 -c copy trump-full.mp4
```

Получится [приблизительно такое видео](trump-full.mp4).

Просмотрим его и запишем первые буквы того, что Трамп произносит в каждом сегменте. Где он ничего не говорит и уходит, будем ставить подчёркивание. Получится флаг.

Флаг: **ugra\_joshua\_the\_boi\_with\_his\_rabbit\_wife**
