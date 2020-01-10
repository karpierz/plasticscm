# Copyright (c) 2019-2020 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/licenses/zlib

import unittest
from unittest import mock
import io

from plasticscm import config


valid_config = """\
[global]
default = one
ssl_verify = true
timeout = 2

[one]
url = http://one.url
private_token = ABCDEF

[two]
url = https://two.url
private_token = GHIJKL
ssl_verify = false
timeout = 10

[three]
url = https://three.url
private_token = MNOPQR
ssl_verify = /path/to/CA/bundle.crt
per_page = 50

[four]
url = https://four.url
oauth_token = STUV
"""

no_default_config = """\
[global]
[there]
url = http://there.url
private_token = ABCDEF
"""

missing_attr_config = """\
[global]
[one]
url = http://one.url

[two]
private_token = ABCDEF

[three]
meh = hem

[four]
url = http://four.url
private_token = ABCDEF
per_page = 200
"""


class TestConfigParser(unittest.TestCase):

    @mock.patch("pathlib.Path.is_file")
    def test_missing_config(self, path_isfile):
        path_isfile.return_value = False
        with self.assertRaises(config.PlasticConfigMissingError):
            config.PlasticConfigParser("test")

    @mock.patch("pathlib.Path.is_file")
    @mock.patch("builtins.open")
    def test_invalid_id(self, m_open, path_isfile):
        fd = io.StringIO(no_default_config)
        fd.close = mock.Mock(return_value=None)
        m_open.return_value = fd
        path_isfile.return_value = True
        config.PlasticConfigParser("there")
        with self.assertRaises(config.PlasticIDError):
            config.PlasticConfigParser()

        fd = io.StringIO(valid_config)
        fd.close = mock.Mock(return_value=None)
        m_open.return_value = fd
        with self.assertRaises(config.PlasticDataError):
            config.PlasticConfigParser(plastic_id="not_there")

    @mock.patch("pathlib.Path.is_file")
    @mock.patch("builtins.open")
    def test_invalid_data(self, m_open, path_isfile):
        fd = io.StringIO(missing_attr_config)
        fd.close = mock.Mock(return_value=None, side_effect=lambda: fd.seek(0))
        m_open.return_value = fd
        path_isfile.return_value = True

        config.PlasticConfigParser("one")
        config.PlasticConfigParser("one")
        with self.assertRaises(config.PlasticDataError):
            config.PlasticConfigParser(plastic_id="two")
        with self.assertRaises(config.PlasticDataError):
            config.PlasticConfigParser(plastic_id="three")
        with self.assertRaises(config.PlasticDataError) as emgr:
            config.PlasticConfigParser("four")
        self.assertEqual("Unsupported per_page number: 200", emgr.exception.args[0])

    @mock.patch("pathlib.Path.is_file")
    @mock.patch("builtins.open")
    def test_valid_data(self, m_open, path_isfile):
        fd = io.StringIO(valid_config)
        fd.close = mock.Mock(return_value=None)
        m_open.return_value = fd
        path_isfile.return_value = True

        cp = config.PlasticConfigParser()
        self.assertEqual("one", cp.plastic_id)
        self.assertEqual("http://one.url", cp.url)
        self.assertEqual("ABCDEF", cp.private_token)
        self.assertEqual(None, cp.oauth_token)
        self.assertEqual(2, cp.timeout)
        self.assertEqual(True, cp.ssl_verify)
        self.assertIsNone(cp.per_page)

        fd = io.StringIO(valid_config)
        fd.close = mock.Mock(return_value=None)
        m_open.return_value = fd
        cp = config.PlasticConfigParser(plastic_id="two")
        self.assertEqual("two", cp.plastic_id)
        self.assertEqual("https://two.url", cp.url)
        self.assertEqual("GHIJKL", cp.private_token)
        self.assertEqual(None, cp.oauth_token)
        self.assertEqual(10, cp.timeout)
        self.assertEqual(False, cp.ssl_verify)

        fd = io.StringIO(valid_config)
        fd.close = mock.Mock(return_value=None)
        m_open.return_value = fd
        cp = config.PlasticConfigParser(plastic_id="three")
        self.assertEqual("three", cp.plastic_id)
        self.assertEqual("https://three.url", cp.url)
        self.assertEqual("MNOPQR", cp.private_token)
        self.assertEqual(None, cp.oauth_token)
        self.assertEqual(2, cp.timeout)
        self.assertEqual("/path/to/CA/bundle.crt", cp.ssl_verify)
        self.assertEqual(50, cp.per_page)

        fd = io.StringIO(valid_config)
        fd.close = mock.Mock(return_value=None)
        m_open.return_value = fd
        cp = config.PlasticConfigParser(plastic_id="four")
        self.assertEqual("four", cp.plastic_id)
        self.assertEqual("https://four.url", cp.url)
        self.assertEqual(None, cp.private_token)
        self.assertEqual("STUV", cp.oauth_token)
        self.assertEqual(2, cp.timeout)
        self.assertEqual(True, cp.ssl_verify)
