import copy
import time
from hashlib import sha512
import sqlite3

import numpy as np
from matplotlib import pyplot as plt

from stats import UserStats, User
from multiprocessing import Process, SimpleQueue, Manager
from typing import Callable


def init_db(con: sqlite3.Connection):
    cur = con.cursor()
    cur.execute('create table if not exists users_out (login text, password text)')
    cur.execute('create table if not exists users_in (i int, login text, password text)')
    con.commit()


def fill_input_db(con: sqlite3.Connection, count=120):
    cur = con.cursor()
    for index in range(count):
        m = User()
        cur.execute(f'insert into users_in (i, login, password) values ({index}, "{m.login()}", "{m.password()}")')
    con.commit()


def get_list_size_from_db(con: sqlite3.Connection) -> int:
    cur = con.cursor()
    cur.execute('select count(*) from users_in')
    return cur.fetchone()[0]


def clear_db(con: sqlite3.Connection):
    cur = con.cursor()
    cur.execute('drop table if exists users_out')
    cur.execute('drop table if exists users_in')
    con.commit()


def generate_users(users_count: int) -> [UserStats]:
    users = []

    for i in range(users_count):
        users.append(UserStats(do_not_init=False))

    return users


def load_user(u: UserStats):
    con = sqlite3.connect('app.db')
    c = con.cursor()
    c.execute(f'select login, password from users_in where i = {u.get_number()}')
    login, password = c.fetchone()
    u.user = User(login, password)


def get_hashed(u: UserStats):
    u.current = u.user.login() + 'my secret key'

    for iter in range(2000):
        u.current = sha512((u.current + str(iter)).encode('Utf-8')).hexdigest()


def insert(u: UserStats):
    con = sqlite3.connect('app.db')
    c = con.cursor()
    c.execute(f"insert into users_out (login, password) values ('{u.user.login()}', '{u.current}')")
    con.commit()
    con.close()


def tex_table(stats, stages):
    print("\\hline")
    print('Stage N & Task M & Start Time & End Time\\\\')
    print("\\hline")

    for stat_num, stat in enumerate(stats):
        for stage in range(stages):
            times = stat.get_time(stage=stage)
            print(
                f'Stage: {stage + 1} & Task: {stat_num + 1} & {times[0] - start_time:.6f} & {times[1] - start_time:.6f} \\\\')

        print("\\hline")


def job(task: Callable, in_queue: SimpleQueue, out_queue: SimpleQueue, stage: int):
    while True:
        data: UserStats = in_queue.get()

        if data is None:
            out_queue.put(data)
            break

        data.set_time(time.time(), stage, True)
        task(data)
        data.set_time(time.time(), stage, False)
        out_queue.put(data)


def test_serial(users):
    for user in users:
        load_user(user)
        get_hashed(user)
        insert(user)


if __name__ == '__main__':
    stages_count = 3


    connection = sqlite3.connect('app.db')
    n = np.arange(3, 80, 12)
    p_time = []
    s_time = []
    clear_db(connection)
    init_db(connection)
    fill_input_db(connection)
    for amount in n:
        _users = generate_users(get_list_size_from_db(connection))
        UserStats.cnt=0
        _users = generate_users(amount)
        pipeline_time = 0
        serial_time = 0
        cnt = 10
        for i in range(cnt):
            passwords_queue = SimpleQueue()
            salt_queue = SimpleQueue()
            hash_queue = SimpleQueue()
            result_queue = SimpleQueue()

            add_salter = Process(target=job, args=(load_user, passwords_queue, salt_queue, 0))
            hasher = Process(target=job, args=(get_hashed, salt_queue, hash_queue, 1))
            inserter = Process(target=job, args=(insert, hash_queue, result_queue, 2))
            pipeline = [add_salter, hasher, inserter]

            for u in _users:
                passwords_queue.put(u)

            passwords_queue.put(None)
            start_time = time.time()
            for worker in pipeline:
                worker.start()

            for worker in pipeline:
                worker.join()
            end_time = time.time()
            pipeline_time += end_time - start_time

            start_time_ = time.time()
            workers = []
            users_len = len(_users)
            for j in range(stages_count):
                magic = users_len // stages_count
                worker = Process(target=test_serial, args=(_users[magic*i:magic*(i+1)],))
                worker.start()
                workers.append(worker)

            for j in range(3):
                workers[j].join()
            end_time_ = time.time()
            serial_time += end_time_ - start_time_


        pipeline_time /= cnt

        print(f'Pipeline time = {pipeline_time * 1e6} mks')

        serial_time /= cnt
        print(f'Serial time = {serial_time * 1e6} mks')

        p_time.append(pipeline_time * 1e6)
        s_time.append(serial_time * 1e6)
    connection.close()

    print('Press to get log')
    input()

    # stats = []
    # while not result_queue.empty():
    #     stats.append(result_queue.get())
    # stats.pop()
    #
    # deltas = [[], [], []]
    # for stat in stats:
    #     for stage in range(stages_count):
    #         stage_stat = stat.get_time(stage=stage)
    #         deltas[stage].append(stage_stat[1] - stage_stat[0])
    # #
    # for stage in range(stages_count):
    #     print(f'Max time on stage {stage + 1} = {max(deltas[stage]) * 1e6} mks')
    #     print(f'Min time on stage {stage + 1} = {min(deltas[stage]) * 1e6} mks')
    #     print(f'Avg time on stage {stage + 1} = {sum(deltas[stage]) / len(deltas[stage]) * 1e6} mks\n')
    #
    # tex_table(stats, stages_count)
    plt.plot(n, sorted(p_time), label='Конвейерная обработка')
    plt.plot(n, sorted(s_time), label='Последовательное выполнение')

    plt.legend(loc='upper left')
    plt.xlabel('Количество пользователей')
    plt.ylabel('Время работы (мrс)')
    # plt.title('Зависимость времени работы от размерности матрицы и количества потоков')
    plt.show()
