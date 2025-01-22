import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message


class ValueCounts:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []
        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# VALUE_COUNTS")

        field: str = settings["field"] if "field" in settings else None
        ascending: bool = settings["ascending"] if "ascending" in settings else True
        drop_na: bool = settings["drop_na"] if "drop_na" in settings else False
        
        if not field:
            msg = app_message.dataprep["nodes"]["missing_column"](node_key)
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

        try:
            df_pct = df.value_counts(subset=field, normalize=True, ascending=ascending, dropna=drop_na)
            df_pct = df_pct.reset_index(name="value_pct")

            df_count = df.value_counts(subset=field, normalize=False, ascending=ascending, dropna=drop_na)
            df_count = df_count.reset_index(name="value_count")

            df = pd.merge(df_count, df_pct)

            script.append("\n# pct data")
            script.append("df_pct = df.value_counts(subset={}, normalize=True, ascending={}, dropna={})".format(field, ascending, drop_na))
            script.append("df_pct = df_pct.reset_index(name='value_pct')")

            script.append("\n# count data")
            script.append("df_count = df.value_counts(subset={}, normalize=False, ascending={}, dropna={})".format(field, ascending, drop_na))
            script.append("df_count = df_count.reset_index(name='value_count')")

            script.append("\n# merge data")
            script.append("df = pd.merge(df_count, df_pct)")

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
