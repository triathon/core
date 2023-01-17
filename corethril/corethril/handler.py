import json
import time

import redis
from mythril.mythril import MythrilDisassembler, MythrilAnalyzer
from argparse import Namespace
from ast import literal_eval
from tempfile import NamedTemporaryFile
from models.module import Document, DATA


def is_dict(req: str) -> tuple:
    try:
        if type(literal_eval(req)) != dict:
            return False, req
        else:
            return True, literal_eval(req)
    except EOFError:
        return False, req


def analyzer(s_file):
    args = Namespace(
        solidity_files=[s_file], no_onchain_data=False, address=None, attacker_address=None,
        beam_search=None, bin_runtime=False, call_depth_limit=3, code=None, codefile=None,
        command='a', create_timeout=10, creator_address=None, custom_modules_directory=None,
        disable_dependency_pruning=False, enable_coverage_strategy=False, enable_iprof=False,
        enable_physics=False, epic=False, execution_timeout=86400, graph=None, infura_id=None,
        loop_bound=3, max_depth=128, modules=None, outform='text', parallel_solving=False, phrack=False,
        pruning_factor=1, query_signature=False, rpc='infura-mainnet', rpctls=False, solc_json=None, solv=None,
        solver_log=None, solver_timeout=10000, statespace_json=None, strategy='bfs', transaction_count=2,
        transaction_sequences=None, unconstrained_storage=False, v=2
    )
    disassembler = MythrilDisassembler()
    try:
        address, _ = disassembler.load_from_solidity([s_file])
        Analyzer = MythrilAnalyzer(
            disassembler=disassembler, strategy="bfs", address=address, cmd_args=args
        )
        data = Analyzer.fire_lasers(
            modules=[m.strip() for m in args.modules.strip().split(",")] if args.modules else None,
            transaction_count=1
        )
        return True, data.as_json()
    except Exception as err:
        if 'SolidityVersionMismatch' in err.__str__():
            return False, "Detection version mismatch"
        return False, err


def temporaryFile(data, s_id):
    with NamedTemporaryFile('w+t', suffix=".sol") as f:
        f.write(data)
        f.seek(0)
        print("filename:", f.name)
        state, result = analyzer(f.name)
    if state:
        issues_list = []
        issues = json.loads(result)["issues"]
        for sub_issues in issues:
            sub_issues.pop("tx_sequence")
            issues_list.append(sub_issues)
        data_db = Document.select().where(Document.id == s_id).first()
        if data_db:
            db_result = data_db.result
            db_result["corethril"] = issues_list
            data_db.result = db_result
            data_db.save()
        return "Detection succeeded"
    return result


def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    s_id = int(req)
    if s_id:
        data = Document.select().where(Document.id == s_id).first()
        if not data:
            return "There is no corresponding contract"
        result = temporaryFile(data.contract, s_id)
        return result


def save_error(error, did):
    data_db = Document.select().where(Document.id == did).first()
    if data_db:
        db_result = data_db.result
        db_result["coremythril_error"] = error
        data_db.result = db_result
        data_db.save()


def run():
    print("thril start of testing...")
    conn_pool = redis.ConnectionPool(
        host=DATA.redis_host,
        port=DATA.redis_port,
        password=DATA.redis_password,
        decode_responses=True,
        db=DATA.redis_db,
    )
    rc = redis.Redis(connection_pool=conn_pool)
    rcSetKey = DATA.task_queue+"Set"
    while True:
        id_list = rc.lrange(DATA.task_queue, 0, 4)
        if id_list:
            contract_id = rc.rpop(DATA.task_queue)
            try:
                print("db contract index {} :".format(contract_id))
                result = handle(contract_id)
                print("result: {}".format(result))
                if result != "Detection succeeded":
                    save_error(str(result), contract_id)
                    rc.hset(rcSetKey, f"{contract_id}error", str(result))
                    rc.hset(rcSetKey, f"{contract_id}status", "2")
                else:
                    rc.hset(rcSetKey, f"{contract_id}status", "1")
                time.sleep(2)
            except Exception as e:
                count = rc.hget(rcSetKey, f"{contract_id}count")
                if not count:
                    count = 0
                if int(count) >= 1:
                    continue
                # tautology
                save_error(str(e), contract_id)
                rc.hset(rcSetKey, f"{contract_id}count", str(int(count)+1))
                rc.hset(rcSetKey, f"{contract_id}error", str(e))
                rc.hset(rcSetKey, f"{contract_id}status", "2")

                rc.lpush(DATA.task_queue, contract_id)
                print("tautology:", contract_id)
        else:
            print("wait...")
            time.sleep(5)


if __name__ == '__main__':
    run()
