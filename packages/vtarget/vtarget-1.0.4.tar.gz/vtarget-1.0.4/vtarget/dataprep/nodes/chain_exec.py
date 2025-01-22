import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message


class ChainExec:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []
        script.append("\n# ChainExec")

        # * Validar que exista df de entrada en el puerto A
        if "InA" not in pin:
            msg = app_message.dataprep["nodes"]["missing_df"](node_key, "A")
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

        df: pd.DataFrame = pin["InA"].copy() if "InA" in pin else pd.DataFrame()
        df2: pd.DataFrame = pin["InB"].copy() if "InB" in pin else pd.DataFrame()
        df3: pd.DataFrame = pin["InC"].copy() if "InC" in pin else pd.DataFrame()
        df4: pd.DataFrame = pin["InD"].copy() if "InD" in pin else pd.DataFrame()

        # df_port: pd.DataFrame = pin[port].copy() if port in pin else pd.DataFrame()
        # # * Advertir si el dataframe está vacío
        # if df_port.empty:
        #     msg = app_message.dataprep["nodes"]["empty_df"](node_key, port)
        #     bug_handler.default_node_log(flow_id, node_key, msg, bug_level="warning", console_level="warn")

        cache_handler.update_node(
            flow_id,
            node_key,
            {
                "pout": {"OutA": df, "OutB": df2, "OutC": df3, "OutD": df4},
                "config": json.dumps(settings, sort_keys=True),
                "script": script,
            },
        )

        script_handler.script += script
        return {"OutA": df, "OutB": df2, "OutC": df3, "OutD": df4}
