import random
import time
from collections import OrderedDict


# -----------Клас LRUCache----------------

class LRUCache:
   
    def __init__(self, capacity: int = 1000):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)  # робимо ключ «найновішим»
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # видаляємо найстаріший елемент


# -------------Функції без кешу----------------

def range_sum_no_cache(array, left, right):
    """Повертає суму елементів без кешування"""
    return sum(array[left:right + 1])


def update_no_cache(array, index, value):
    """Оновлює елемент без кешування"""
    array[index] = value


# -----------Функції з кешем----------------

cache = LRUCache(capacity=1000)

def range_sum_with_cache(array, left, right):
    """Обчислює суму з використанням LRU-кешу"""
    key = (left, right)
    cached_value = cache.get(key)
    if cached_value != -1:
        return cached_value
    # cache miss
    result = sum(array[left:right + 1])
    cache.put(key, result)
    return result


def update_with_cache(array, index, value):
    """
    Оновлює масив і видаляє з кешу всі діапазони, які містять цей index.
    Інвалідація кешу — лінійний прохід по ключах
    """
    array[index] = value
    keys_to_delete = [k for k in cache.cache if k[0] <= index <= k[1]]
    for k in keys_to_delete:
        del cache.cache[k]


# ---------Генератор запитів----------------

def make_queries(n, q, hot_pool=30, p_hot=0.95, p_update=0.03):
    hot = [(random.randint(0, n // 2), random.randint(n // 2, n - 1))
           for _ in range(hot_pool)]
    queries = []
    for _ in range(q):
        if random.random() < p_update:  # ~3% Update
            idx = random.randint(0, n - 1)
            val = random.randint(1, 100)
            queries.append(("Update", idx, val))
        else:  # ~97% Range
            if random.random() < p_hot:
                left, right = random.choice(hot)
            else:
                left = random.randint(0, n - 1)
                right = random.randint(left, n - 1)
            queries.append(("Range", left, right))
    return queries


# -------------Тестування продуктивності----------------

def process_queries_no_cache(array, queries):
    for q in queries:
        if q[0] == "Range":
            range_sum_no_cache(array, q[1], q[2])
        else:
            update_no_cache(array, q[1], q[2])


def process_queries_with_cache(array, queries):
    for q in queries:
        if q[0] == "Range":
            range_sum_with_cache(array, q[1], q[2])
        else:
            update_with_cache(array, q[1], q[2])


# ------Основна частина----------

if __name__ == "__main__":
    N = 100_000
    Q = 50_000
    array = [random.randint(1, 100) for _ in range(N)]
    queries = make_queries(N, Q)

    print("Виконується тестування...\n")

    # ---Без кешу---
    start = time.time()
    process_queries_no_cache(array.copy(), queries)
    time_no_cache = time.time() - start

    # ---З кешем---
    start = time.time()
    process_queries_with_cache(array.copy(), queries)
    time_with_cache = time.time() - start

    # ---Результати---
    speedup = round(time_no_cache / time_with_cache, 2) if time_with_cache > 0 else float('inf')

    print(f"Без кешу : {time_no_cache:6.2f} c")
    print(f"LRU-кеш  : {time_with_cache:6.2f} c  (прискорення ×{speedup})")