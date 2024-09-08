import json
import redis
from redis.asyncio import Redis
from config import REDIS_PASS, HOST

REDIS_PASS = REDIS_PASS
HOST = HOST


def start_sesion():
    r = redis.Redis(
        host=HOST,
        port=10798,
        password=REDIS_PASS)
    return r


def redis_fsm():
    r = Redis(
        host=HOST,
        port=10798,
        password=REDIS_PASS,
        decode_responses=True)
    return r


def get_variables():
    r = redis.Redis(
        host=HOST,
        port=10798,
        password=REDIS_PASS)

    variables = {key.decode('utf-8'): json.loads(val) for key, val in r.hgetall('VolleyBot').items()}
    return variables


def zero_variables():
    r = redis.Redis(
        host=HOST,
        port=10798,
        password=REDIS_PASS)
    variables = {'message_id': None,
                 'event_players_dict': dict(),
                 'message': None,
                 'guest': {'name': ''},
                 'topik_id': None,
                 'chat_id': None,
                 'callback_id': 0}
    for key, var in variables.items():
        variables[key] = json.dumps(var)

    r.hset(name='VolleyBot', mapping=variables)


def close_all_conection():
    connect = redis.Redis(host=HOST,
                          port=10798,
                          password=REDIS_PASS)

    # get list of clients
    clients_list = connect.client_list()

    # close all connections
    for client in clients_list:
        # exclude our connection
        if client['addr'] == '127.0.0.1:6379':  # Убедитесь, что пропускаете текущее соединение, если необходимо
            continue
        # Close by IP and port
        connect.client_kill(client['addr'])


if __name__ == '__main__':
    r = redis.Redis(
        host=HOST,
        port=10798,
        password=REDIS_PASS)

    variables = {key.decode('utf-8'): json.loads(val) for key, val in r.hgetall('VolleyBot').items()}
    client_list = r.client_list()

    print(len(client_list))
    print(client_list)
    print(variables)
