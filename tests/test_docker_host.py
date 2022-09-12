import unittest
from packaging.version import parse as parse_version

from uptime_kuma_api import DockerType, UptimeKumaException
from uptime_kuma_test_case import UptimeKumaTestCase


class TestDockerHost(UptimeKumaTestCase):
    def setUp(self):
        super(TestDockerHost, self).setUp()
        if parse_version(self.api.version) < parse_version("1.18"):
            super(TestDockerHost, self).tearDown()
            self.skipTest("Unsupported in this Uptime Kuma version")

    def test_docker_host(self):
        expected_docker_host = {
            "name": "name 1",
            "dockerType": DockerType.SOCKET,
            "dockerDaemon": "/var/run/docker.sock"
        }

        # test docker host
        with self.assertRaisesRegex(UptimeKumaException, r'connect ENOENT /var/run/docker.sock'):
            self.api.test_docker_host(**expected_docker_host)

        # add docker host
        r = self.api.add_docker_host(**expected_docker_host)
        self.assertEqual(r["msg"], "Saved")
        docker_host_id = r["id"]

        # get docker host
        docker_host = self.api.get_docker_host(docker_host_id)
        self.compare(docker_host, expected_docker_host)

        # get docker hosts
        docker_hosts = self.api.get_docker_hosts()
        docker_host = self.find_by_id(docker_hosts, docker_host_id)
        self.assertIsNotNone(docker_host)
        self.compare(docker_host, expected_docker_host)

        # edit docker host
        r = self.api.edit_docker_host(docker_host_id, name="name 2")
        self.assertEqual(r["msg"], "Saved")
        docker_host = self.api.get_docker_host(docker_host_id)
        expected_docker_host["name"] = "name 2"
        self.compare(docker_host, expected_docker_host)

        # delete docker host
        r = self.api.delete_docker_host(docker_host_id)
        self.assertEqual(r["msg"], "Deleted")
        with self.assertRaises(UptimeKumaException):
            self.api.get_docker_host(docker_host_id)


if __name__ == '__main__':
    unittest.main()