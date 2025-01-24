№ Вывод по порядку

from statyaUKRRF import statya

print(statya.statya[0]) № "Статья 7. Действие уголовного закона во времени"

№ Вывод рандом

from statyaUKRRF import statya
import random

RandStatya = random.choice(statya.statya)
print(RandStatya)