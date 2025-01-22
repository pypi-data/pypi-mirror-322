import io
import json
import os
import re

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message
from vtarget.utils import normpath
from vtarget.utils.email_sender import EmailSender
from vtarget.utils.encrypter import DECRYPT_KEY, encrypter
from vtarget.utils.utilities import utilities


class Email:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []
        streams: list[dict] = []
        files: list[str] = []
        # ports: list[str] = [p for p in dict(settings).keys() if str(p).startswith("port_")]

        total_size: int = 0

        # * deploy mode habilitado
        deploy_enabled: bool = settings["deploy_enabled"] if "deploy_enabled" in settings else False
        attachments_ports: list[dict] = settings["attachments"] if "attachments" in settings else []
        
        for k in attachments_ports:
            port_id = k["port"] if "port" in k else None
            attach_file_name = k["alias"] if "alias" in k else None
            
            if not port_id:
                continue
            
            port_key = f"port_{port_id}"
            port_origin: str = settings[port_key] if port_key in settings else None
            
            if port_origin:
                # * Extraer key y puerto de salida del nodo
                sepIdx = len(port_origin) - port_origin[::-1].find("_")
                parent_key: str = port_origin[0 : sepIdx - 1]
                parent_port: str = port_origin[sepIdx:]
                
                if parent_key is not None and parent_port is not None:
                    # ? Obtener el df del padre desde cache
                    parent_settings = cache_handler.settings[flow_id][parent_key]
                    parent = cache_handler.cache[flow_id][parent_key]
                    
                    if parent_key.lower().startswith("excel"):  # * Nodos de tipo excel
                        # ? Obtener la ruta del archivo excel generado
                        parent_config: dict = json.loads(parent_settings["config"]) if "config" in parent_settings else {}
                        file_path: str = parent_config["file_path"] if "file_path" in parent_config else None
                        
                        if file_path is None:
                            output_name: str = parent_config["name"] if "name" in parent_config else None
                            output_path: str = parent_config["path"] if "path" in parent_config else None
                            
                            if deploy_enabled:
                                output_path = settings["deploy_path"] if "deploy_path" in settings else None
                                
                            if output_name and output_path:
                                file_path = output_path + os.path.sep + output_name + ".xlsx"
                                file_path = normpath(file_path)

                        # ? Agregar la ruta del archivo a la lista de archivos
                        if file_path is not None:
                            files.append(file_path)
                            # ? sumar peso del excel al total
                            size = os.path.getsize(file_path)
                            total_size += size
                            
                    else:  # * Cualquier otro tipo de nodos
                        # ? Convertir df del puerto de origen en un csv en memoria
                        df_in: pd.DataFrame = parent["pout"][parent_port] if "pout" in parent and parent_port in parent["pout"] else pd.DataFrame()
                        if len(df_in):
                            stream = io.StringIO()
                            df_in.to_csv(stream, index=False)
                            # ? sumar peso del csv al total
                            pos = stream.tell()
                            stream.seek(0, os.SEEK_END)
                            stream.seek(pos)
                            total_size += pos
                            filename = attach_file_name if attach_file_name else port_origin
                            # ? agregar el stream a la lista y asignarle un nombre por defecto
                            streams.append({"filename": f"{filename}.csv", "attachment": stream})

        # * Check if total size > 20Mb
        if total_size / (1024 * 1024) > 20:
            msg = app_message.dataprep["nodes"]["email"]["size_max"](node_key, str(requires_props))
            return bug_handler.default_node_log(flow_id, node_key, msg)

        script.append("\n# EMAIL")
        SERVER: str = settings["server"] if "server" in settings and settings["server"] else None
        PORT: str = settings["port"] if "port" in settings and settings["port"] else None
        FROM: str = settings["from"] if "from" in settings and settings["from"] else None
        PASS: str = settings["password"] if "password" in settings and settings["password"] else None

        if deploy_enabled:
            SERVER: str = settings["deploy_server"] if "deploy_server" in settings and settings["deploy_server"] else None
            PORT: str = settings["deploy_port"] if "deploy_port" in settings and settings["deploy_port"] else None
            FROM: str = settings["deploy_from"] if "deploy_from" in settings and settings["deploy_from"] else None
            PASS: str = settings["deploy_password"] if "deploy_password" in settings and settings["deploy_password"] else None

        to: list = settings["to"] if "to" in settings and settings["to"] else []
        subject = settings["subject"] if "subject" in settings else "-"
        message = settings["message"] if "message" in settings else ""
        requires_props = list(set(["server", "port", "from", "password", "to"]) - set([k for k in settings.keys() if settings[k]]))

        if len(requires_props) != 0:
            msg = app_message.dataprep["nodes"]["email"]["config_required"](node_key, str(requires_props))
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")
        
        # ** Encontrar posibles variables en el texto de entrada que hagan referencia a Dataframe
        message = utilities.check_and_add_flow_vars(flow_id, message, include_quotes=False)
        refs_vars = [str(x).replace("${", "").replace("}", "") for x in re.findall(r"\$\{.*?\}", message)] # ej: ${var_name}
        
        if len(refs_vars):
            # Crear un diccionario con los df de entrada
            for k, v in pin.items():
                globals()[f'df_{k}'] = v
            
            # actualiza texto con el valor de la variable
            for ref_var in refs_vars:
                try:
                    res = eval(ref_var)
                    message = message.replace("${" + ref_var + "}", f"{res}")
                    # message = message.replace("{{" + ref_var + "}}", res)
                except Exception as e:
                    msg = f"Variable reference Error: ${ref_var}\t" + str(e)
                    bug_handler.default_node_log(flow_id, node_key, msg, f"{e.__class__.__name__}({', '.join(map(str, e.args))})")
            
        DECRYPTEDPASS = encrypter.decrypt(PASS, DECRYPT_KEY) if PASS is not None and DECRYPT_KEY is not None else ""
        
        try:
            emailSender = EmailSender()
            emailSender.configure_server(SERVER, PORT, FROM, DECRYPTEDPASS)
            emailSender.send_email(",".join(to), subject, message, streams=streams, files=files)

        except Exception as e:
            msg = app_message.dataprep["nodes"]["email"]["failed_send"](node_key)
            bug_handler.default_node_log(flow_id, node_key, msg, f"{e.__class__.__name__}({', '.join(map(str, e.args))})")
            return {}

        cache_handler.update_node(
            flow_id,
            node_key,
            {
                "config": json.dumps(settings, sort_keys=True),
                "script": script,
            },
        )

        script_handler.script += script
        return {}
