import io
import unittest

import cmd


class TestParseEnvFile(unittest.TestCase):

    def test_parse_env_file(self):
        buffer = io.BytesIO()
        file = io.TextIOWrapper(buffer)
        file.write('FOO1=bar1\n')
        file.write('FOO2="bar2"\n')
        file.write("FOO3='bar3' \n")
        file.flush()
        file.seek(0)
        result = cmd.parse_env_file(file)
        self.assertEqual({
            'FOO1': 'bar1',
            'FOO2': 'bar2',
            'FOO3': 'bar3',
        }, result)
