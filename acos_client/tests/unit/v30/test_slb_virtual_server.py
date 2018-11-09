# Copyright 2014-2016, A10 Networks.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from __future__ import absolute_import
from __future__ import unicode_literals

try:
    import unittest
    from unittest import mock
except ImportError:
    import mock
    import unittest2 as unittest

from acos_client import client
import acos_client.errors as acos_errors
import json
import responses


HOSTNAME = 'fake_a10'
BASE_URL = 'https://{}:443/axapi/v3'.format(HOSTNAME)
AUTH_URL = '{}/auth'.format(BASE_URL)
VSERVER_NAME = 'test'
CREATE_URL = '{}/slb/virtual-server/'.format(BASE_URL)
OBJECT_URL = '{}/slb/virtual-server/{}'.format(BASE_URL, VSERVER_NAME)
STATS_URL = '{}/slb/virtual-server/{}/port/stats'.format(BASE_URL, VSERVER_NAME)
OPER_URL = '{}/slb/virtual-server/{}/oper'.format(BASE_URL, VSERVER_NAME)


class TestVirtualServer(unittest.TestCase):

    def setUp(self):
        self.client = client.Client(HOSTNAME, '30', 'fake_username', 'fake_password')

    @mock.patch('acos_client.v30.slb.virtual_server.VirtualServer.get')
    @responses.activate
    def test_virtual_server_create_no_params(self, mocked_get):
        mocked_get.side_effect = acos_errors.NotFound
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {"foo": "bar"}
        responses.add(responses.POST, CREATE_URL, json=json_response, status=200)
        params = {
            'virtual-server': {
                'ip-address': '192.168.2.254',
                'name': VSERVER_NAME,
                'arp-disable': 0,
            }
        }

        resp = self.client.slb.virtual_server.create('test', '192.168.2.254')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, CREATE_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @mock.patch('acos_client.v30.slb.virtual_server.VirtualServer.get')
    @responses.activate
    def test_virtual_server_create_with_params(self, mocked_get):
        mocked_get.side_effect = acos_errors.NotFound
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {"foo": "bar"}
        responses.add(responses.POST, CREATE_URL, json=json_response, status=200)
        params = {
            'virtual-server': {
                'ip-address': '192.168.2.254',
                'name': VSERVER_NAME,
                'arp-disable': 1,
                'vrid': 1,
                'template_virtual_server': 'TEST_VIP_TEMPLATE',
            }
        }

        resp = self.client.slb.virtual_server.create(
            name='test',
            ip_address='192.168.2.254',
            arp_disable=1,
            vrid=1,
            template_virtual_server='TEST_VIP_TEMPLATE',
        )

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, CREATE_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @mock.patch('acos_client.v30.slb.virtual_server.VirtualServer.get')
    @responses.activate
    def test_virtual_server_create_already_exists(self, mocked_get):
        mocked_get.return_value = {"foo": "bar"}

        with self.assertRaises(acos_errors.Exists):
            self.client.slb.virtual_server.create('test', '192.168.2.254')

    @responses.activate
    def test_virtual_server_update_no_params(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {"foo": "bar"}
        responses.add(responses.POST, OBJECT_URL, json=json_response, status=200)
        params = {
            'virtual-server': {
                'ip-address': '192.168.2.254',
                'name': VSERVER_NAME,
                'arp-disable': 0,
            }
        }

        resp = self.client.slb.virtual_server.update('test', '192.168.2.254')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, OBJECT_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_virtual_server_update_with_params(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {"foo": "bar"}
        responses.add(responses.POST, OBJECT_URL, json=json_response, status=200)
        params = {
            'virtual-server': {
                'name': VSERVER_NAME,
                'ip-address': '192.168.2.254',
                'arp-disable': 1,
                'vrid': 1,
                'template_virtual_server': 'TEST_VIP_TEMPLATE',
            }
        }

        resp = self.client.slb.virtual_server.update(
            name='test',
            ip_address='192.168.2.254',
            arp_disable=1,
            vrid=1,
            template_virtual_server='TEST_VIP_TEMPLATE',
        )

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, OBJECT_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_virtual_server_delete(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {"foo": "bar"}
        responses.add(responses.DELETE, OBJECT_URL, json=json_response, status=200)

        resp = self.client.slb.virtual_server.delete('test')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.DELETE)
        self.assertEqual(responses.calls[1].request.url, OBJECT_URL)

    @responses.activate
    def test_virtual_server_delete_not_found(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            "response": {"status": "fail", "err": {"code": 67239937, "msg": " No such Virtual Server"}}
        }
        responses.add(responses.DELETE, OBJECT_URL, json=json_response, status=200)

        with self.assertRaises(acos_errors.ACOSException):
            self.client.slb.virtual_server.delete('test')

        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.DELETE)
        self.assertEqual(responses.calls[1].request.url, OBJECT_URL)

    @responses.activate
    def test_virtual_server_search(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {"foo": "bar"}
        responses.add(responses.GET, OBJECT_URL, json=json_response, status=200)

        resp = self.client.slb.virtual_server.get('test')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.GET)
        self.assertEqual(responses.calls[1].request.url, OBJECT_URL)

    @responses.activate
    def test_virtual_server_search_not_found(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            "response": {"status": "fail", "err": {"code": 67239937, "msg": " No such Virtual Server"}}
        }
        responses.add(responses.GET, OBJECT_URL, json=json_response, status=200)

        with self.assertRaises(acos_errors.ACOSException):
            self.client.slb.virtual_server.get('test')

        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.GET)
        self.assertEqual(responses.calls[1].request.url, OBJECT_URL)

    @responses.activate
    def test_virtual_server_stats(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {"foo": "bar"}
        responses.add(responses.GET, STATS_URL, json=json_response, status=200)

        resp = self.client.slb.virtual_server.stats('test')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.GET)
        self.assertEqual(responses.calls[1].request.url, STATS_URL)

    @responses.activate
    def test_virtual_server_oper(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {"foo": "bar"}
        responses.add(responses.GET, OPER_URL, json=json_response, status=200)

        resp = self.client.slb.virtual_server.oper('test')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.GET)
        self.assertEqual(responses.calls[1].request.url, OPER_URL)


class TestIPv6VirtualServer(unittest.TestCase):

    def setUp(self):
        self.client = client.Client(HOSTNAME, '30', 'fake_username', 'fake_password')

    @mock.patch('acos_client.v30.slb.virtual_server.VirtualServer.get')
    @responses.activate
    def test_virtual_server_create_no_params(self, mocked_get):
        mocked_get.side_effect = acos_errors.NotFound
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {"foo": "bar"}
        responses.add(responses.POST, CREATE_URL, json=json_response, status=200)
        params = {
            'virtual-server': {
                'ipv6-address': '2001:dbef:1111:feed:beef:8000:1d01:200f',
                'name': VSERVER_NAME,
                'arp-disable': 0,
            }
        }

        resp = self.client.slb.virtual_server.create('test', '2001:dbef:1111:feed:beef:8000:1d01:200f')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, CREATE_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @mock.patch('acos_client.v30.slb.virtual_server.VirtualServer.get')
    @responses.activate
    def test_virtual_server_create_with_params(self, mocked_get):
        mocked_get.side_effect = acos_errors.NotFound
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {"foo": "bar"}
        responses.add(responses.POST, CREATE_URL, json=json_response, status=200)
        params = {
            'virtual-server': {
                'ipv6-address': '2001:dbef:1111:feed:beef:8000:1d01:200f',
                'name': VSERVER_NAME,
                'arp-disable': 1,
                'vrid': 1,
                'template_virtual_server': 'TEST_VIP_TEMPLATE',
            }
        }

        resp = self.client.slb.virtual_server.create(
            name='test',
            ip_address='2001:dbef:1111:feed:beef:8000:1d01:200f',
            arp_disable=1,
            vrid=1,
            template_virtual_server='TEST_VIP_TEMPLATE',
        )

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, CREATE_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @mock.patch('acos_client.v30.slb.virtual_server.VirtualServer.get')
    @responses.activate
    def test_virtual_server_create_already_exists(self, mocked_get):
        mocked_get.return_value = {"foo": "bar"}

        with self.assertRaises(acos_errors.Exists):
            self.client.slb.virtual_server.create('test', '2001:dbef:1111:feed:beef:8000:1d01:200f')

    @responses.activate
    def test_virtual_server_update_no_params(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {"foo": "bar"}
        responses.add(responses.POST, OBJECT_URL, json=json_response, status=200)
        params = {
            'virtual-server': {
                'ipv6-address': '2001:dbef:1111:feed:beef:8000:1d01:200f',
                'name': VSERVER_NAME,
                'arp-disable': 0,
            }
        }

        resp = self.client.slb.virtual_server.update('test', '2001:dbef:1111:feed:beef:8000:1d01:200f')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, OBJECT_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_virtual_server_update_with_params(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {"foo": "bar"}
        responses.add(responses.POST, OBJECT_URL, json=json_response, status=200)
        params = {
            'virtual-server': {
                'name': VSERVER_NAME,
                'ipv6-address': '2001:dbef:1111:feed:beef:8000:1d01:200f',
                'arp-disable': 1,
                'vrid': 1,
                'template_virtual_server': 'TEST_VIP_TEMPLATE',
            }
        }

        resp = self.client.slb.virtual_server.update(
            name='test',
            ip_address='2001:dbef:1111:feed:beef:8000:1d01:200f',
            arp_disable=1,
            vrid=1,
            template_virtual_server='TEST_VIP_TEMPLATE',
        )

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.POST)
        self.assertEqual(responses.calls[1].request.url, OBJECT_URL)
        self.assertEqual(json.loads(responses.calls[1].request.body), params)

    @responses.activate
    def test_virtual_server_delete(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {"foo": "bar"}
        responses.add(responses.DELETE, OBJECT_URL, json=json_response, status=200)

        resp = self.client.slb.virtual_server.delete('test')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.DELETE)
        self.assertEqual(responses.calls[1].request.url, OBJECT_URL)

    @responses.activate
    def test_virtual_server_delete_not_found(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            "response": {"status": "fail", "err": {"code": 67239937, "msg": " No such Virtual Server"}}
        }
        responses.add(responses.DELETE, OBJECT_URL, json=json_response, status=200)

        with self.assertRaises(acos_errors.ACOSException):
            self.client.slb.virtual_server.delete('test')

        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.DELETE)
        self.assertEqual(responses.calls[1].request.url, OBJECT_URL)

    @responses.activate
    def test_virtual_server_search(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {"foo": "bar"}
        responses.add(responses.GET, OBJECT_URL, json=json_response, status=200)

        resp = self.client.slb.virtual_server.get('test')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.GET)
        self.assertEqual(responses.calls[1].request.url, OBJECT_URL)

    @responses.activate
    def test_virtual_server_search_not_found(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {
            "response": {"status": "fail", "err": {"code": 67239937, "msg": " No such Virtual Server"}}
        }
        responses.add(responses.GET, OBJECT_URL, json=json_response, status=200)

        with self.assertRaises(acos_errors.ACOSException):
            self.client.slb.virtual_server.get('test')

        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.GET)
        self.assertEqual(responses.calls[1].request.url, OBJECT_URL)

    @responses.activate
    def test_virtual_server_stats(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {"foo": "bar"}
        responses.add(responses.GET, STATS_URL, json=json_response, status=200)

        resp = self.client.slb.virtual_server.stats('test')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.GET)
        self.assertEqual(responses.calls[1].request.url, STATS_URL)

    @responses.activate
    def test_virtual_server_oper(self):
        responses.add(responses.POST, AUTH_URL, json={'session_id': 'foobar'})
        json_response = {"foo": "bar"}
        responses.add(responses.GET, OPER_URL, json=json_response, status=200)

        resp = self.client.slb.virtual_server.oper('test')

        self.assertEqual(resp, json_response)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(responses.calls[1].request.method, responses.GET)
        self.assertEqual(responses.calls[1].request.url, OPER_URL)
