import logging
import os
import unittest
from unittest.mock import patch

import click
from click.testing import CliRunner

from cobo_cli.cli import cli
from cobo_cli.managers.config_manager import ConfigManager

logger = logging.getLogger(__name__)


class TestLoginCommands(unittest.TestCase):
    def setUp(self):
        logging.getLogger().setLevel(logging.DEBUG)

    @patch.object(ConfigManager, "get_config")
    @patch.object(ConfigManager, "set_config")
    def test_login_org_token(self, set_config, get_config):
        get_config.return_value = {
            "access_token": "sR2PzutxUwrMvbCoZf9uKq1uFQioFj5SU2us5g55aEh5PhwqVCMaE0fqRWK7xtN7",
            "token_type": "Bearer",
            "scope": "",
            "expires_in": 42810,
            "refresh_token": "agyn7yVtfyf3WkU1Vy3Kl2z4w5z422JHvG7dErixlCRhMTifrJs3CB8kTSWi7Rzv",
        }
        set_config.return_value = {
            "access_token": "sR2PzutxUwrMvbCoZf9uKq1uFQioFj5SU2us5g55aEh5PhwqVCMaE0fqRWK7xtN7",
            "token_type": "Bearer",
            "scope": "",
            "expires_in": 42810,
            "refresh_token": "agyn7yVtfyf3WkU1Vy3Kl2z4w5z422JHvG7dErixlCRhMTifrJs3CB8kTSWi7Rzv",
        }
        runner = CliRunner()

        assert isinstance(cli, click.Group)
        with runner.isolated_filesystem():
            cwd = os.getcwd()
            env_file = f"{cwd}/.cobo_cli.env"
            config_manager = ConfigManager(config_file=env_file)
            config_manager.set_config("CLIENT_ID", "aYkam0BPwJrduDU3Wqu89htGDHy4ATkV")
            config_manager.set_config(
                "APP_SECRET",
                "1b196b9f46249eb9281a92c8ae85076d2fb7dae74eaedc557387adaadeb419f6",
            )
            config_manager.set_config(
                "APP_KEY",
                "e5122fa07f0d32f3240052b89a1b2ea5f8e596ff6b2c0e22f9b16b3e55e6eaab",
            )

            result = runner.invoke(
                cli,
                [
                    "--enable-debug",
                    "--env-file",
                    env_file,
                    "--env",
                    "sandbox",
                    "login",
                    "-o",
                    "--org-uuid",
                    "02273047-5730-4b63-be0e-399e5d3a1054",
                ],
            )
            logger.info(f"command result: {result.output}")
            self.assertEqual(result.exit_code, 0)
            self.assertTrue(
                "Got token for org 02273047-5730-4b63-be0e-399e5d3a1054"
                in result.output
            )

            result = runner.invoke(
                cli,
                [
                    "--enable-debug",
                    "--env-file",
                    env_file,
                    "--env",
                    "sandbox",
                    "login",
                    "-o",
                    "--org-uuid",
                    "02273047-5730-4b63-be0e-399e5d3a1054",
                    "--refresh-token",
                ],
            )
            logger.info(f"command result: {result.output}")
            self.assertEqual(result.exit_code, 0)

            self.assertTrue(
                "Got token for org 02273047-5730-4b63-be0e-399e5d3a1054"
                in result.output
            )
