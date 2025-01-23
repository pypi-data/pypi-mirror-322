from typing import Optional

import requests
from utils import DOMAIN, ACCESS_TOKEN


class GerenciadorApi:

    def __init__(self) -> None:
        self.__DOMAIN = DOMAIN

    def __get_headers(self) -> dict:
        return {'Content-Type': 'application/json', 'Authorization': f'Bearer {ACCESS_TOKEN}'}

    def __response(self, url: str, method: str, data: str | None = None) -> dict:
        try:
            if data is None:
                data = {}

            if method == 'GET':
                response = requests.get(url, headers=self.__get_headers())

            elif method == 'POST':
                response = requests.post(url, headers=self.__get_headers(), data=data)

            elif method == 'PUT':
                response = requests.put(url, headers=self.__get_headers(), data=data)

            else:
                return {}

            if response.status_code == 200 or response.status_code == 201:

                data = response.json()

                if data.get('content', None) is not None:
                    return data.get('content')

                return response.json()['data']
            else:
                return {}

        except requests.exceptions.RequestException as e:
            return {}
        except Exception as e:
            return {}

    # Busca todas as filas vinculadas ao server rodando, para ativar.
    def find_filas_by_application(self, site: str, server_process: Optional[str], container_id: Optional[str]) -> dict:

        __url = f'{self.__DOMAIN}/fila?site={site}'

        if server_process is not None:
            __url += f'&server_process={server_process}'

        if container_id is not None:
            __url += f'&container_id={container_id}'

        return self.__response(__url, 'GET')

    # Atualizar a fila, informando o status de processamento.
    def update_fila(self, payload: str) -> dict:
        __url = f'{self.__DOMAIN}/fila'
        return self.__response(__url, 'PUT', payload)

    # Busca todos os dados do site para processar algum dado.
    def find_all_applications_by_application_name(self, name: str) -> dict:
        __url = f'{self.__DOMAIN}/site?name={name}'
        return self.__response(__url, 'GET')

    # Atualiza a senha do site.
    def update_password_site(self, id: int, password: str) -> dict:
        __url = f'{self.__DOMAIN}/site?id={id}&password={password}'
        return self.__response(__url, 'PUT')

    # Busca a ultima sessão gerado no site.
    def find_last_session_site(self, siteName: str) -> dict:
        __url = f'{self.__DOMAIN}/sessao?siteName={siteName}'
        return self.__response(__url, 'GET')

    # Permite cadastrar a sessão.
    def create_session_by_user(self, payload: str) -> dict:
        __url = f'{self.__DOMAIN}/sessao'
        return self.__response(__url, 'POST', payload)

    # Busca todas as filas vinculadas ao server rodando.
    def find_all_fila_playlist_by_application(self, application: str) -> dict:
        __url = f'{self.__DOMAIN}/fila/playlist?application={application}'
        return self.__response(__url, 'GET')

    # Atualiza a fila, informando o status de processamento.
    def update_fila_playlist(self, payload: str) -> dict:
        __url = f'{self.__DOMAIN}/fila/playlist'
        return self.__response(__url, 'PUT', payload)

    # Atualiza o site e tipo do container.
    def update_container(self, container_identifier: str, configuration_type: str, site_name: str,
                         server_ip: str) -> dict:
        __url = f'{self.__DOMAIN}/container/sync-website?container_identifier={container_identifier}&configuration_type={configuration_type}&site_name={site_name}&server_ip={server_ip}'
        return self.__response(__url, 'POST')

    # Filtra as filas para transferir macs
    def filter_queue_transfer_mac(self, site: str) -> dict:
        __url = f'{self.__DOMAIN}/transfer-mac/filter?site={site}&processed=false'
        return self.__response(__url, 'GET')

    # Filtra as filas para transferir macs
    def update_queue_transfer_mac(self, payload: str) -> dict:
        __url = f'{self.__DOMAIN}/transfer-mac'
        return self.__response(__url, 'PUT', payload)

    def find_queue_super_play(self, payload: str, processed: bool) -> dict:
        __url = f'{self.__DOMAIN}/super-play?processed={processed}'
        return self.__response(__url, 'GET', payload)

    def update_queue_super_play(self, super_play_id: str) -> dict:
        __url = f'{self.__DOMAIN}/super-play/{super_play_id}'
        return self.__response(__url, 'PUT')
