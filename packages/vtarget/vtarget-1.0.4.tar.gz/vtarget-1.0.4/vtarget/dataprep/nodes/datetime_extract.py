import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message


class DatetimeExtract:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# Datetime Extract")

        items: list[str] = settings["items"] if ("items" in settings and settings["items"]) else None

        if items:
            for item in items:
                # column_to_convert, new_column_name, to_extract
                column_to_convert: str = item["column_to_convert"] if ("column_to_convert" in item and item["column_to_convert"]) else ""
                to_extract: str = item["to_extract"] if ("to_extract" in item and item["to_extract"]) else ""
                new_column_name: str = item["new_column_name"] if "new_column_name" in item and item["new_column_name"] else to_extract.replace("()", "")

                if not to_extract or not column_to_convert:
                    msg = app_message.dataprep["nodes"]["missing_column"](node_key)
                    return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

                try:

                    if to_extract.startswith('to_period("W")'):
                        to_extract = "to_period(\"W\").dt.strftime('%Y-%m-%d')"
                    elif to_extract == "date":
                        to_extract = "strftime('%Y-%m-%d')"
                    elif to_extract == "time":
                        to_extract = "strftime('%H:%M:%S')"
                    elif to_extract == "month_start_day":
                        to_extract = "strftime('%Y-%m-01')"

                    df[new_column_name] = eval(f"df[column_to_convert].dt.{to_extract}")
                    script.append(f'df["{new_column_name}"] = df["{column_to_convert}"].dt.{to_extract}')

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
        else:
            msg = app_message.dataprep["nodes"]["missing_column"](node_key)
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")
