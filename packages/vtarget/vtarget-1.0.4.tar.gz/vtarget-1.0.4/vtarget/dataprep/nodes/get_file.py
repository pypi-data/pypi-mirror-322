import json
import os
import shutil

import pandas as pd
import requests

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message


class GetFile:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# Get File")

        # field
        field: list = settings["field"] if "field" in settings and settings["field"] else []
        folder_path: str = settings["folder_path"] if "folder_path" in settings and settings["folder_path"] else None
        source: str = settings["source"] if "source" in settings and settings["source"] else None
        #
        folder_category: str = settings["folder_category"] if "folder_category" in settings and settings["folder_category"] else None
        image_name: str = settings["image_name"] if "image_name" in settings and settings["image_name"] else None

        if not field or not folder_path or not source:
            msg = app_message.dataprep["nodes"]["missing_column"](node_key)
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

        # Valido que la ruta exista
        if not os.path.exists(folder_path):
            # ! Devolver error
            print("La ruta no existe")

        try:
            if source == "local" or source == "url":
                df.apply(self.path_validate, axis=1, args=(folder_category, image_name, folder_path, field, source))
            else:
                pass
                # ! Devolver error

        except Exception as e:
            print("Error (get_file): ", e)
            msg = app_message.dataprep["nodes"]["exception"](node_key, str(e))
            return bug_handler.default_node_log(flow_id, node_key, msg, f"{e.__class__.__name__}({', '.join(map(str, e.args))})")

        cache_handler.update_node(
            flow_id,
            node_key,
            {
                "config": json.dumps(settings, sort_keys=True),
                "script": script,
            },
        )

        script_handler.script += script
        return df

    def path_validate(self, row, folder_category, image_name, folder_path, field, source):
        # Se genera ruta para subdirectorios en caso que existan
        _folder_category: str = row[folder_category] if folder_category else ""
        new_path: str = os.path.join(folder_path, _folder_category)
        if _folder_category != "" and not os.path.exists(new_path):
            os.makedirs(new_path)

        _image_name = ""
        # Obtengo la extensión del archivo original
        _, ext = os.path.splitext(row[field])

        # Viene o no el nombre del archivo
        if image_name:
            # Obtengo la extensión del nombre que trae en el dataframe para saber si el nombre viene con extensión
            _, extension = os.path.splitext(row[image_name])
            # En caso que el nombre del dataframe no traiga extensión, le agrego la extensión de la URL
            if extension == "":
                _image_name = row[image_name] + ext
            # De lo contrario, le dejo el original
            else:
                _image_name = row[image_name]
        else:
            _image_name = "file_" + str(row.name).zfill(6) + ext

        # Se crea la ruta del archivo
        file_path = os.path.join(new_path, _image_name)

        # Se obtienen y crean los archivos
        self.get_and_write_files(file_path, row[field], source)

    def get_and_write_files(self, file_path, url, source):
        try:
            if source == "url":
                response = requests.get(url)
                response.raise_for_status()
                with open(file_path, "wb") as file:
                    file.write(response.content)
            elif source == "local":
                shutil.copy(url, file_path)
            else:
                pass
        except Exception as e:
            print("Error (get_file): ", e)
