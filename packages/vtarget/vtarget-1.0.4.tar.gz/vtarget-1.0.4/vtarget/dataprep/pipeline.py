class Pipeline:
    def __init__(self):
        from vtarget.dataprep.nodes.api_rest import ApiRest
        from vtarget.dataprep.nodes.chain_exec import ChainExec
        from vtarget.dataprep.nodes.code import Code
        from vtarget.dataprep.nodes.column import Column
        from vtarget.dataprep.nodes.concat import Concat
        from vtarget.dataprep.nodes.concat_multi import Concat_Multi
        from vtarget.dataprep.nodes.cross_join import CrossJoin
        from vtarget.dataprep.nodes.cumsum import Cumsum
        from vtarget.dataprep.nodes.cut import Cut
        from vtarget.dataprep.nodes.data_cleansing import DataCleansing
        from vtarget.dataprep.nodes.database import Database
        from vtarget.dataprep.nodes.database_write import DatabaseWrite
        from vtarget.dataprep.nodes.datetime_extract import DatetimeExtract
        from vtarget.dataprep.nodes.datetime_fill import DatetimeFill
        from vtarget.dataprep.nodes.datetime_formatter import DatetimeFormatter
        from vtarget.dataprep.nodes.datetime_range import DatetimeRange
        from vtarget.dataprep.nodes.dbscan import DbScan
        from vtarget.dataprep.nodes.describe import Describe
        from vtarget.dataprep.nodes.df_maker import DfMaker
        from vtarget.dataprep.nodes.drop_duplicates import DropDuplicates
        from vtarget.dataprep.nodes.dtype import Dtype
        from vtarget.dataprep.nodes.email import Email
        from vtarget.dataprep.nodes.excel import ExcelOutput
        from vtarget.dataprep.nodes.filter import Filter
        from vtarget.dataprep.nodes.formula import Formula
        from vtarget.dataprep.nodes.get_file import GetFile
        from vtarget.dataprep.nodes.get_web import GetWeb
        from vtarget.dataprep.nodes.groupby import Groupby
        from vtarget.dataprep.nodes.input_data import InputData
        from vtarget.dataprep.nodes.inter_row import InterRow
        from vtarget.dataprep.nodes.isin import IsIn
        from vtarget.dataprep.nodes.keep_col import KeepCol
        from vtarget.dataprep.nodes.kmeans import Kmeans
        from vtarget.dataprep.nodes.louvain import Louvain
        from vtarget.dataprep.nodes.melt import Melt
        from vtarget.dataprep.nodes.merge import Merge
        from vtarget.dataprep.nodes.output import Output
        from vtarget.dataprep.nodes.pivot import Pivot
        from vtarget.dataprep.nodes.quality import Quality
        from vtarget.dataprep.nodes.regex import Regex
        from vtarget.dataprep.nodes.replace import Replace
        from vtarget.dataprep.nodes.rolling import Rolling
        from vtarget.dataprep.nodes.sample import Sample
        from vtarget.dataprep.nodes.shape import Shape
        from vtarget.dataprep.nodes.sort import Sort
        from vtarget.dataprep.nodes.split import Split
        from vtarget.dataprep.nodes.switch import Switch
        from vtarget.dataprep.nodes.unique import Unique
        from vtarget.dataprep.nodes.v_output import VOutput
        from vtarget.dataprep.nodes.value_counts import ValueCounts

        self.decimal_round = False
        self.nodes_instances = {
            "API_Rest": ApiRest(),
            "Input_Data": InputData(),
            "Database": Database(),
            "Database_Write": DatabaseWrite(),
            "Sort": Sort(),
            "Filter": Filter(),
            "Formula": Formula(),
            "Merge": Merge(),
            "Group_By": Groupby(),
            "Cross_Join": CrossJoin(),
            "Concat": Concat(),
            "Concat_Multi": Concat_Multi(),
            "Pivot": Pivot(),
            "Shape": Shape(),
            "Melt": Melt(),
            "Output_Data": Output(),
            "Code": Code(),
            "Value_Counts": ValueCounts(),
            "Describe": Describe(),
            "Isin": IsIn(),
            "Cumsum": Cumsum(),
            "V_Output": VOutput(),
            "Inter_Row": InterRow(),
            "Unique": Unique(),
            "Drop_Duplicates": DropDuplicates(),
            "Data_Cleansing": DataCleansing(),
            "Datetime_Formatter": DatetimeFormatter(),
            "Datetime_Extract": DatetimeExtract(),
            "Switch": Switch(),
            "Select": Dtype(),
            "Dtype": Dtype(),
            "Column": Column(),
            "Excel": ExcelOutput(),
            "Email": Email(),
            "DF_Maker": DfMaker(),
            "Source": Code(),
            "Datetime_Range": DatetimeRange(),
            "Rolling": Rolling(),
            "Datetime_Fill": DatetimeFill(),
            "Sample": Sample(),
            "Split": Split(),
            "Cut": Cut(),
            "DBScan": DbScan(),
            "Kmeans": Kmeans(),
            "Louvain": Louvain(),
            "Replace": Replace(),
            "Quality": Quality(),
            "Keep_Column": KeepCol(),
            "Chain_Exec": ChainExec(),
            "Get_Web": GetWeb(),
            "Regex": Regex(),
            "Get_File": GetFile(),
        }

    def exec(self, flow_id: str, node: dict, input_port: dict):
        import gc
        import json
        from typing import Dict

        import pandas as pd

        from vtarget.dataprep.types import NodeType
        from vtarget.handlers.bug_handler import bug_handler
        from vtarget.handlers.cache_handler import cache_handler
        from vtarget.language.app_message import app_message
        from vtarget.utils.utilities import utilities

        settings = node["meta"]["config"] if "config" in node["meta"] else dict()
        max_rows: int = settings["max_rows"] if "max_rows" in settings else 0

        dict_pout: Dict[pd.DataFrame] = self.nodes_instances[node["type"]].exec(
            flow_id,
            node["key"],
            input_port,
            settings,
        )

        dict_pout = utilities.fix_dict_pout_df_columns(dict_pout, flow_id, node_key=node["key"])

        if max_rows > 0:
            for pout in dict_pout:
                if isinstance(dict_pout[pout], pd.DataFrame) and dict_pout[pout].shape[0] > max_rows:
                    msg = app_message.dataprep["builder"]["max_rows"](node["key"], max_rows)
                    bug_handler.default_node_log(flow_id, node["key"], msg, console_level="warn", bug_level="warning")
                    dict_pout[pout] = dict_pout[pout].head(max_rows)
                    # TODO: Pregunta, Debería actualizarse la cache de este nodo???

        if "STDOUT" in dict_pout:
            node["meta"]["STDOUT"] = dict_pout["STDOUT"]

        node["meta"]["script"] = (
            cache_handler.settings[flow_id][node["key"]]["script"]
            if node["key"] in cache_handler.settings[flow_id] and "script" in cache_handler.settings[flow_id][node["key"]]
            else []
        )

        # agregar ports_config a caché
        if "ports_config" in node["meta"]:
            cache_handler.update_node(
                flow_id,
                node["key"],
                {"ports_config": json.dumps(node["meta"]["ports_config"], sort_keys=True)},
                silence=True,
            )

        for port_name in node["meta"]["ports_map"]["pout"].keys():
            port_config: dict = utilities.get_table_config(node["meta"], port_name)
            port_df: pd.DataFrame = dict_pout[port_name]
            node["meta"]["ports_map"]["pout"][port_name]["head"] = utilities.get_head_of_df_as_list(port_df, port_config, flow_id, node["key"], port_name)
            # TODO: revisar si la referencia de dict_pout se actualiza al modificar cache por el sort_by del puerto
            node["meta"]["ports_map"]["pout"][port_name]["rows"] = port_df.shape[0]
            node["meta"]["ports_map"]["pout"][port_name]["cols"] = port_df.shape[1]
            prev_dtypes: dict = (
                node["meta"]["ports_map"]["pout"][port_name]["dtypes"]
                if port_name in node["meta"]["ports_map"]["pout"] and "dtypes" in node["meta"]["ports_map"]["pout"][port_name]
                else {}
            )
            new_dtypes: dict = utilities.get_dtypes_of_df(port_df)

            # * Merge dtypes previo con los nuevos, para conservar config de la tabla
            if prev_dtypes and new_dtypes:
                for k in new_dtypes:
                    if k in prev_dtypes:
                        if "visible" in prev_dtypes[k]:
                            new_dtypes[k]["visible"] = prev_dtypes[k]["visible"]
                        if "numberFormat" in prev_dtypes[k]:
                            new_dtypes[k]["numberFormat"] = prev_dtypes[k]["numberFormat"]
                        # TODO: Mejorar la forma en que se asigna el orden cuando hay nuevas columnas
                        # # * mantener orden seteado desde las opciones de la tabla (excepto para nodos Column, Dtypes y Select)
                        # if (
                        #     node["type"]
                        #     not in [
                        #         NodeType.COLUMN.value,
                        #         NodeType.DTYPE.value,
                        #         NodeType.SELECT.value,
                        #         NodeType.GROUPBY.value,
                        #         # NodeType.CUMSUM.value, # puede incluir groupby que ordena las columnas a agrupar
                        #         # NodeType.DESCRIBE.value, # puede incluir groupby que ordena las columnas a agrupar
                        #         # NodeType.INTERROW.value, # puede incluir groupby que ordena las columnas a agrupar
                        #         # NodeType.PIVOT.value, # puede incluir groupby que ordena las columnas a agrupar
                        #     ]
                        #     and "order" in prev_dtypes[k]
                        # ):
                        #     new_dtypes[k]["order"] = prev_dtypes[k]["order"]

            node["meta"]["ports_map"]["pout"][port_name]["dtypes"] = new_dtypes
            node["meta"]["ports_map"]["pout"][port_name]["summary"] = {}
            node["meta"]["ports_map"]["pout"][port_name]["describe"] = {}
            node["meta"]["readed_from_cache"] = False

        del dict_pout
        gc.collect()
        return node
