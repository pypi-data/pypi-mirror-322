import json
import re

import numpy as np
import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message


class Regex:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# Regex")

        # field
        items: list = settings["items"] if "items" in settings and settings["items"] else []

        try:
            for i, item in enumerate(items):
                print(item)
                field = item["field"]
                pattern = item["pattern"]
                separateToColumn = item["separateToColumn"] if "separateToColumn" in item else False

                if not field:
                    msg = app_message.dataprep["nodes"]["missing_column"](node_key)
                    return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

                if not pattern:
                    msg = app_message.dataprep["nodes"]["missing_column"](node_key)
                    return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

                # Validar que la columna existe
                if field not in df.columns:
                    msg = app_message.dataprep["nodes"]["missing_column"](node_key)
                    return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

                # Validar que tiene grupos de captura
                if re.search(r"\((?!\?:)", pattern):
                    extracted_columns = df[field].str.extract(pattern, expand=True)
                else:
                    extracted_columns = df[field].str.extractall(f"({pattern})").reset_index(drop=True)

                # ! Caso extraño cuando no hayan grupos de control pero se seleccione separar en columnas. Tener cuidado con ese caso
                
                # Validar si va en columnas separadas o juntas
                if separateToColumn:
                    extracted_columns.columns = [f"regex_{i}_col_{j}" for j in range(extracted_columns.shape[1])]
                else:
                    extracted_columns = extracted_columns.apply(lambda row: "".join(row.dropna()) if not row.isnull().all() else np.nan, axis=1)
                    extracted_columns = pd.DataFrame(extracted_columns, columns=[f"regex_{i}_combined"])

                # Transformo para que quede todo como object
                extracted_columns = extracted_columns.astype(object)
                # Agrego las columnas trabajadas al dataframe original
                df = pd.concat([df, extracted_columns], axis=1).reset_index(drop=True)

        except Exception as e:
            msg = app_message.dataprep["nodes"]["exception"](node_key, str(e))
            return bug_handler.default_node_log(flow_id, node_key, msg, f"{e.__class__.__name__}({', '.join(map(str, e.args))})")

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
