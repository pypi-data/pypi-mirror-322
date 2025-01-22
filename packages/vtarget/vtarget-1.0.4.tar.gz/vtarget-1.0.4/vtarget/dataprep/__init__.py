from typing import Any, Dict


def run_flow(path: str, enable_dump=False) -> Dict[str, Any]:
    import gc
    import json
    import os

    from vtarget.dataprep.builder import Builder
    from vtarget.handlers.bug_handler import bug_handler
    from vtarget.handlers.cache_handler import cache_handler
    from vtarget.handlers.log_handler import log_handler

    with open(path, "r") as content:
        data = json.loads(content.read())

    builder = Builder()

    builder.init_pipeline()

    flow_id = data["id"]

    deploy_enabled = data["deployEnabled"] if "deployEnabled" in data else False

    cache_handler.dump_enabled = enable_dump

    builder.analyzer(
        data["model"],
        True,
        flow_id,
        os.path.basename(path),
        False,
        False,
        deploy_enabled,
    )

    del builder.pipeline

    result = {
        "status": True,
        "flow_id": flow_id,
        "nodes": {
            # node_key: {
            #     "status": True/False
            #     "bugs":
            # }
        },
        "logs": [],
        "bugs": [],
        "v_output": {
            # node_key: dataframe
        },
        "message": "",
    }

    cache_handler.load_settings(flow_id)

    for node_key in cache_handler.settings[flow_id]:
        if node_key not in result["nodes"]:
            result["nodes"][node_key] = dict()
        result["nodes"][node_key]["status"] = True
        result["nodes"][node_key]["bugs"] = []
        result["nodes"][node_key]["logs"] = []
        if "type" not in cache_handler.settings[flow_id][node_key]:
            continue
        if cache_handler.settings[flow_id][node_key]["type"] != "V_Output":
            continue
        if node_key not in result["v_output"]:
            result["v_output"][node_key] = dict()
        for port_name in cache_handler.settings[flow_id][node_key]["pout"]:
            cache_handler.load(flow_id, node_key, port_name)
            port = cache_handler.cache[flow_id][node_key]["pout"][port_name]
            result["v_output"][node_key][port_name] = port

    cache_handler.reset(flow_id)

    gc.collect()

    for bug in bug_handler.bug:
        node_key = bug["node_key"] if "node_key" in bug and node_key in result["nodes"] else None
        level = bug["level"] if "level" in bug else None
        error = level == "error"
        if node_key:
            result["status"] = result["status"] and not error
            result["nodes"][node_key]["status"] = not error
            result["nodes"][node_key]["bugs"].append(bug)
        else:
            result["bugs"].append(bug)

    for log in log_handler.log:
        node_key = log["node_key"] if "node_key" in log and node_key in result["nodes"] else None
        if node_key:
            result["nodes"][node_key]["logs"].append(log)
        else:
            result["logs"].append(log)

    return result
