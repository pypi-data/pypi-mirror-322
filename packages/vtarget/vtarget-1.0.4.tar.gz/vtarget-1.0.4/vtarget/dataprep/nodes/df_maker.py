import json

import numpy as np
import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message
from vtarget.utils.dtype_optimizer import dtype_optimizer


class DfMaker:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []
        script.append("\n# DFMAKER")
        data: list = settings["data"] if "data" in settings and settings["data"] else []
        df = pd.DataFrame()
        
        try:
            columns = []
            rows = []
            if len(data):
                columns = [c["value"] if "value" in c else f"col_{idx+1}" for idx, c in enumerate(data[0])]
                if len(data) > 1:
                    rows = [[c["value"] for c in r] for r in data[1:]]

            df = pd.DataFrame(np.array(rows), columns=columns)
            script.append(f"rows = {rows}")
            script.append(f"columns = {columns}")
            script.append("df = pd.DataFrame(np.array(rows), columns=columns)")

            for col in df.columns:
                try:
                    df[col] = pd.to_numeric(df[col])
                except Exception as e:
                    print(col, e)

        except Exception as e:
            msg = app_message.dataprep["nodes"]["exception"](node_key, str(e))
            return bug_handler.default_node_log(flow_id, node_key, msg, f"{e.__class__.__name__}({', '.join(map(str, e.args))})")
        
        # # remove duplicated columns
        # df = utilities.fix_df_columns(df, flow_id, node_key)
        
        # Intenta optmizar los tipos de datos
        try:
            dtype_optimizer.optimize(df)
        except Exception as e:
            print("Error al intentar optimizar tipo de datos", str(e))

        cache_handler.update_node(
            flow_id,
            node_key,
            {
                "pout": {"Out": df},
                "config": json.dumps(settings, sort_keys=True),
                "script": script,
            },
        )

        script_handler.script += script
        return {"Out": df}
