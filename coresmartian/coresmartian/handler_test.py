from handler import handle
from models.module import DATA
import redis


# Test your handler here

# To disable testing, you can set the build_arg `TEST_ENABLED=false` on the CLI or in your stack.yml
# https://docs.openfaas.com/reference/yaml/#function-build-args-build-args

def test_handle():
    conn_pool = redis.ConnectionPool(
        host=DATA.redis_host,
        port=DATA.redis_port,
        password=DATA.redis_password,
        decode_responses=True,
        db=DATA.redis_db,
    )
    rc = redis.Redis(connection_pool=conn_pool)
    # rc.lpush(DATA.task_queue, 35)
    print("start \n" + "-" * 30 + "\nqueue: ", rc.lrange(DATA.task_queue, 0, 10))

    contract_id = rc.rpop(DATA.task_queue)
    result = handle(contract_id)
    print("db contract index: {} \nresult: {}".format(contract_id, result))

    print("queue: ", rc.lrange(DATA.task_queue, 0, 10), "\n end \n" + "-" * 30)


if __name__ == '__main__':
    test_handle()
