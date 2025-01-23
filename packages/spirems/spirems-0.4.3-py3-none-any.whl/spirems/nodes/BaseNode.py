#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: renjin@bit.edu.cn
# @Date  : 2024-08-06

from spirems import Subscriber, Publisher, Parameter, Logger, def_msg
import os
import json
from typing import Union


def update_parameter_dict(json_params: dict, node_name: str, job_name: str):
    n_name = '/' + node_name + '/'
    r_name = '/' + node_name + '_' + job_name + '/'
    g_name = '/_global/'
    dict_params = dict()
    for param_key, param_val in json_params.items():
        if param_key.startswith(n_name):
            param_key = param_key[len(n_name):]
            dict_params.update({param_key: param_val})
        if param_key.startswith(r_name):
            param_key = param_key[len(r_name):]
            dict_params.update({param_key: param_val})
        if param_key.startswith(g_name):
            param_key = '/' + param_key[len(g_name):]
            dict_params.update({param_key: param_val})
    return dict_params


def load_parameter_file(parameter_file: str, node_name: str, job_name: str):
    assert os.path.isfile(parameter_file) and parameter_file.endswith('.json'), \
        "The input parameter_file must be a JSON file."
    with open(parameter_file, 'r') as f:
        json_params = json.load(f)
    dict_params = update_parameter_dict(json_params, node_name, job_name)
    return dict_params


class BaseNode:
    def __init__(
        self,
        node_name: str,
        job_name: str,
        ip: str = '127.0.0.1',
        port: int = 9094,
        param_dict_or_file: Union[dict, str] = None,
        multi_instance_node: bool = True,
        sms_shutdown: bool = False,
        sms_logger: bool = False
    ):
        self._shutdown = False
        self.node_name = node_name
        self.job_name = job_name
        self._ip = ip
        self._port = port
        self.queue_pool = []
        if multi_instance_node:
            self._param_server = Parameter(
                node_name + "_" + job_name,
                self.params_changed,
                ip=ip,
                port=port
            )
        else:
            self._param_server = Parameter(
                node_name,
                self.params_changed,
                ip=ip,
                port=port
            )
        self.sms_shutdown  = sms_shutdown
        if self.sms_shutdown and len(self.job_name):
            self._shutdown_reader = Subscriber(
                '/' + self.job_name + '/shutdown',
                'std_msgs::Boolean',
                self._shutdown_callback,
                ip=ip,
                port=port
            )
        if param_dict_or_file:
            if isinstance(param_dict_or_file, str):
                dict_params = load_parameter_file(param_dict_or_file, self.node_name, self.job_name)
                if len(dict_params):
                    self._param_server.set_params(dict_params)
            elif isinstance(param_dict_or_file, dict):
                dict_params = update_parameter_dict(param_dict_or_file, self.node_name, self.job_name)
                if len(dict_params):
                    self._param_server.set_params(dict_params)
        self.sms_logger = sms_logger
        if self.sms_logger:
            self.logger = Logger(node_name + "_" + job_name)

    def get_param(self, param_name: str, default: any) -> any:
        if param_name in self._param_server.sync_params:
            return self._param_server.sync_params[param_name]
        else:
            self._param_server.set_param(param_name, default)
            return default
    
    def set_param(self, param_name: str, value: any) -> any:
        self._param_server.set_param(param_name, value)
        return value

    def release(self):
        if self.sms_shutdown:
            self._shutdown_reader.kill()
        if self.sms_logger:
            self.logger.quit()
        self._param_server.kill()

    def shutdown(self):
        self._shutdown = True
        for q in self.queue_pool:
            q.put(None)

    def emit_shutdown(self):
        if len(self.job_name):
            shutdown_writer = Publisher(
                '/' + self.job_name + '/shutdown', 'std_msgs::Boolean',
                ip=self._ip, port=self._port
            )
            msg = def_msg('std_msgs::Boolean')
            msg['data'] = True
            shutdown_writer.publish(msg)
            shutdown_writer.kill()

    def is_running(self) -> bool:
        return not self._shutdown

    def _shutdown_callback(self, msg):
        if msg['data']:
            self.shutdown()

    def params_changed(self, params):
        member_variables = dir(self)
        for param_key, param_val in params.items():
            if param_key in member_variables:
                setattr(self, param_key, param_val)
            global_key = param_key.replace('/', 'g_')
            if global_key in member_variables:
                setattr(self, global_key, param_val)


if __name__ == '__main__':
    bn = BaseNode(
        'COCODatasetLoaderNode',
        'EvalJob',
        parameter_file=r'C:\deep\SpireCV\params\spirecv2\default_params.json'
    )
