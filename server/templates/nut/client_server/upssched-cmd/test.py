import io
import unittest

import cmd


class TestIsFalsePositive(unittest.TestCase):

    def test_false_positives(self):
        for case in [
            cmd.Info(85, set(['OL', 'LB', 'RB'])),
            cmd.Info(100, set(['OL', 'LB', 'RB'])),
            cmd.Info(100, set(['LB', 'OL', 'RB'])),
            cmd.Info(100, set(['LB', 'OL', 'RB', 'OTHER'])),
        ]:
            self.assertTrue(cmd.is_false_positive(case))

    def test_not_false_positives(self):
        for case in [
            cmd.Info(0, set(['OL', 'LB', 'RB'])),
            cmd.Info(-5, set(['OL', 'LB', 'RB'])),
            cmd.Info(100, set(['LB', 'RB'])),
        ]:
            self.assertFalse(cmd.is_false_positive(case))


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
