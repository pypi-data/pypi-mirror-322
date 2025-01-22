def find(arr: list, prop: str, value: any):
    for x in arr:
        if x[prop] == value:
            return x


class __AutoMLCache:
    from typing import Any, Dict, List, Union

    import pandas as pd

    from evalml.automl.automl_search import AutoMLSearch
    from woodwork.table_schema import TableSchema
    from woodwork.column_schema import ColumnSchema

    X_schema: TableSchema
    y_schema: ColumnSchema

    def __load(self, name: str, obj: Union[Any, None] = None) -> Any:
        import os

        import cloudpickle

        from vtarget.utils import TEMP_DIR

        if os.path.exists(f"{TEMP_DIR}/cache") and os.path.exists(f"{TEMP_DIR}/cache/automl_{name}"):
            try:
                with open(f"{TEMP_DIR}/cache/automl_{name}", "rb") as file:
                    return cloudpickle.load(file)
            except:
                pass
        if obj is not None:
            return obj()

    def __dump(self, name: str, obj: Any) -> None:
        import os

        import cloudpickle

        from vtarget.utils import TEMP_DIR

        if not os.path.exists(f"{TEMP_DIR}/cache"):
            os.mkdir(f"{TEMP_DIR}/cache")
        if os.path.exists(f"{TEMP_DIR}/cache/automl_{name}"):
            os.remove(f"{TEMP_DIR}/cache/automl_{name}")
        with open(f"{TEMP_DIR}/cache/automl_{name}.tmp", "wb") as file:
            cloudpickle.dump(obj, file)
        os.rename(f"{TEMP_DIR}/cache/automl_{name}.tmp", f"{TEMP_DIR}/cache/automl_{name}")

    # NOTE: Getters and setters

    def get_df(self) -> pd.DataFrame:
        import pandas as pd

        return self.__load("df", pd.DataFrame)

    def set_df(self, df: pd.DataFrame):
        self.__dump("df", df)

    def get_target(self) -> str:
        return self.__load("target", str)

    def set_target(self, target: str):
        self.__dump("target", target)

    def get_problem_type(self) -> str:
        return self.__load("problem_type", str)

    def set_problem_type(self, problem_type: str):
        self.__dump("problem_type", problem_type)

    def get_models(self) -> List[Dict[str, Any]]:
        return self.__load("models", list)

    def set_models(self, models: List[Dict[str, Any]]):
        import json

        from vtarget.handlers.event_handler import event_handler

        self.__dump("models", models)
        event_handler.emit_queue.put(
            {
                "name": "automl.set_models",
                "data": json.dumps(models, default=str),
            }
        )

    def get_current_model_name(self) -> str:
        return self.__load("current_model_name", str)

    def set_current_model_name(self, current_model_name: str):
        self.__dump("current_model_name", current_model_name)

    def get_partition_data(self) -> Dict[str, Any]:
        from typing import Dict, Any
        from evalml.utils.woodwork_utils import infer_feature_types

        partition_data: Dict[str, Any] = self.__load("partition_data", dict)
        for key in partition_data:
            if key.startswith("X"):
                partition_data[key] = infer_feature_types(partition_data[key], self.X_schema.logical_types)
            elif key.startswith("y"):
                partition_data[key] = infer_feature_types(partition_data[key], self.y_schema.logical_type)
        return partition_data

    def set_partition_data(self, partition_data: Dict[str, Any]):
        self.__dump("partition_data", partition_data)

    def get_automl_search(self) -> Union[AutoMLSearch, None]:
        import os

        from evalml.automl.automl_search import AutoMLSearch
        from vtarget.utils import TEMP_DIR

        pickle_path = f"{TEMP_DIR}/cache/automl_automl_search"

        if os.path.exists(pickle_path):
            try:
                return AutoMLSearch.load(pickle_path)
            except:
                pass

    def set_automl_search(self, automl_search: AutoMLSearch):
        import os

        from vtarget.utils import TEMP_DIR

        pickle_path = f"{TEMP_DIR}/cache/automl_automl_search"
        pickle_temp_path = f"{TEMP_DIR}/cache/automl_automl_search.tmp"

        if not os.path.exists(f"{TEMP_DIR}/cache"):
            os.mkdir(f"{TEMP_DIR}/cache")
        if os.path.exists(pickle_path):
            os.remove(pickle_path)
        automl_search.save(pickle_temp_path)
        os.rename(pickle_temp_path, pickle_path)

    # NOTE: Methods

    def find_model(self, model_name: str) -> Dict[str, Any]:
        models = self.get_models()
        return find(models, "name", model_name)

    def prepend_model(self, model: Dict[str, Any]):
        models = self.get_models()
        models.insert(0, model)
        self.set_models(models)

    def append_model(self, model: Dict[str, Any]):
        models = self.get_models()
        models.append(model)
        self.set_models(models)

    def replace_model(self, model: Dict[str, Any]):
        models = self.get_models()
        for i in range(len(models)):
            if models[i]["name"] == model["name"]:
                models[i] = {**models[i], **model}
        self.set_models(models)

    def is_a_model(self, model_name: str):
        model = self.find_model(model_name)
        return model is not None

    def update_model(self, props: Dict[str, Any] = {}, model_name: str = None):
        import json

        from vtarget.handlers.event_handler import event_handler

        if model_name is None:
            model_name = self.get_current_model_name()

        models = self.get_models()

        for i in range(len(models)):
            if models[i]["name"] == model_name:
                models[i].update(props)
                event_handler.emit_queue.put(
                    {
                        "name": "automl.update_model",
                        "data": json.dumps(models[i], default=str),
                    }
                )
                break
        self.set_models(models)


automl_cache = __AutoMLCache()
