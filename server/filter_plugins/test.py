import unittest

from ansible.errors import AnsibleError

from filters import FilterModule


class TestGetDictKeyContains(unittest.TestCase):

    def setUp(self):
        self.filters = FilterModule()

    def test_single_match(self):
        result = self.filters.get_dict_key_contains({"foo_bar": 1, "baz": 2}, "_bar")
        self.assertEqual(1, result)

    def test_no_match_raises(self):
        with self.assertRaises(AnsibleError):
            self.filters.get_dict_key_contains({"foo": 1, "baz": 2}, "_bar")

    def test_multiple_matches_raises(self):
        with self.assertRaises(AnsibleError):
            self.filters.get_dict_key_contains({"foo_bar": 1, "baz_bar": 2}, "_bar")


class TestNetconfigDeriveFilename(unittest.TestCase):

    def setUp(self):
        self.filters = FilterModule()

    def test_default_suffix(self):
        self.assertEqual("10-eth0.network", self.filters.netconfig_derive_filename(10, "eth0"))

    def test_custom_suffix(self):
        self.assertEqual("20-vlan-11wifi.netdev", self.filters.netconfig_derive_filename(20, "vlan-11wifi", "netdev"))


class TestNetconfigEnrich(unittest.TestCase):

    def setUp(self):
        self.filters = FilterModule()

    def test_basic_interface(self):
        interfaces = [{"name": "eth0", "priority": 10, "type": "dhcp"}]
        result = self.filters.netconfig_enrich(interfaces, [])
        self.assertEqual([{
            "name": "eth0",
            "priority": 10,
            "type": "dhcp",
            "filename": "10-eth0.network",
            "name_is_wildcard_prefix": False,
            "override_dns": [],
            "vlans": {},
            "vlan_names": [],
        }], result)

    def test_invalid_priority_raises(self):
        interfaces = [{"name": "eth0", "priority": 100, "type": "dhcp"}]
        with self.assertRaises(AnsibleError):
            self.filters.netconfig_enrich(interfaces, [])

    def test_dhcp_fallback_prefixes(self):
        result = self.filters.netconfig_enrich([], ["en"])
        self.assertEqual([{
            "name": "en",
            "name_is_wildcard_prefix": True,
            "priority": 99,
            "filename": "99-en.network",
            "type": "dhcp",
            "vlans": {},
            "vlan_names": [],
        }], result)

    def test_attaches_vlan_names(self):
        interfaces = [{
            "name": "enp3s0",
            "priority": 10,
            "type": "dhcp",
            "vlans": {11: {"suffix": "wifi"}, 50: {"suffix": "srv"}},
        }]
        result = self.filters.netconfig_enrich(interfaces, [])
        self.assertEqual(["enp3s0.11", "enp3s0.50"], result[0]["vlan_names"])


class TestNetconfigEnrichVlans(unittest.TestCase):

    def setUp(self):
        self.filters = FilterModule()

    def test_single_interface_multiple_vlans(self):
        interfaces = [{
            "name": "enp3s0",
            "priority": 10,
            "type": "none",
            "vlans": {11: {"suffix": "wifi"}, 50: {"suffix": "srv"}},
        }]
        result = self.filters.netconfig_enrich_vlans(interfaces)
        self.assertEqual([
            {
                "interface": "enp3s0",
                "vlan_id": 11,
                "vlan_name": "enp3s0.11",
                "bridge_name": "br-11wifi",
                "vlan_netdev_filename": "20-vlan-11wifi.netdev",
                "vlan_network_filename": "21-vlan-11wifi.network",
                "bridge_netdev_filename": "30-br-11wifi.netdev",
                "bridge_network_filename": "31-br-11wifi.network",
            },
            {
                "interface": "enp3s0",
                "vlan_id": 50,
                "vlan_name": "enp3s0.50",
                "bridge_name": "br-50srv",
                "vlan_netdev_filename": "20-vlan-50srv.netdev",
                "vlan_network_filename": "21-vlan-50srv.network",
                "bridge_netdev_filename": "30-br-50srv.netdev",
                "bridge_network_filename": "31-br-50srv.network",
            },
        ], result)

    def test_no_vlans(self):
        self.assertEqual([], self.filters.netconfig_enrich_vlans([{"name": "enp3s0", "priority": 10, "type": "dhcp"}]))


class TestRemoveNewlines(unittest.TestCase):

    def setUp(self):
        self.filters = FilterModule()

    def test_removes_literal_backslash_n(self):
        self.assertEqual("foobar", self.filters.remove_newlines("foo\\nbar"))

    def test_no_newlines(self):
        self.assertEqual("foobar", self.filters.remove_newlines("foobar"))


class TestToCaddyHeaderValues(unittest.TestCase):

    def setUp(self):
        self.filters = FilterModule()

    def test_replace_action(self):
        result = self.filters.to_caddy_header_values({"X-Foo": "bar"}, "replace")
        self.assertEqual("X-Foo `bar`", result)

    def test_default_action(self):
        result = self.filters.to_caddy_header_values({"X-Foo": "bar"}, "default")
        self.assertEqual("?X-Foo `bar`", result)

    def test_multiple_headers(self):
        result = self.filters.to_caddy_header_values({"X-Foo": "bar", "X-Baz": "qux"}, "replace")
        self.assertEqual("X-Foo `bar`\nX-Baz `qux`", result)

    def test_invalid_action_raises(self):
        with self.assertRaises(AnsibleError):
            self.filters.to_caddy_header_values({"X-Foo": "bar"}, "invalid")


if __name__ == "__main__":
    unittest.main()
