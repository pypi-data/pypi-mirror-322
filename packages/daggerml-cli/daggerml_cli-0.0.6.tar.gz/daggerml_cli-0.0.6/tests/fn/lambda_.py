#!/usr/bin/env python3
import json
# import sys
# from uuid import uuid4

# from util import SimpleApi

# from daggerml_cli import repo
# from daggerml_cli.repo import Error


def handler(event, context):
    # fndag, dag_dump = repo.from_json(event)
    # with SimpleApi.begin('test', 'test', dag_dump=dag_dump) as d0:
    #     _, *args = d0.unroll(d0.get_expr())
    #     try:
    #         n0 = d0.put_literal([uuid4().hex, sum(args)])
    #     except Exception as e:
    #         n0 = Error(e)
    #     dag_dump = d0.commit(n0)
    # return {"status": 200, "payload": dag_dump}
    return {"statusCode": 200, "body": "asdf----asdf"}
