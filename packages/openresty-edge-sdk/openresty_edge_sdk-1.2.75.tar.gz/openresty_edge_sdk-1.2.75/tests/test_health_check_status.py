# -*- coding: utf-8 -*-
# import io
import sdk_test
import random
import time

class TestUpstream(sdk_test.TestSdk):
    def test_upstream_healthcheck_status(self):
        up_id = self.client.new_upstream(
            name='origin-upstream',
            servers=[
                {'domain': 'test.com', 'port': 80},
                {'ip': '172.22.31.2', 'port': 80, 'weight': 2}
            ],
            health_checker={
                'http_req_uri': '/status',
                'http_req_host': 'test.com',
                'interval': 3,
                'interval_unit': 'sec',
                'timeout': 1,
                'fall': 3,
                'rise': 2,
                'valid_statuses': [200, 302],
                'report_interval': 3,
                'report_interval_unit': 'min'
            })
        self.assertIs(type(up_id), int)
        self.assertGreater(up_id, 0)

        data = self.client.get_upstream_healthcheck_status(self.app_id, up_id)
        self.assertIs(type(data), dict)
        data = data['data']
        self.assertIs(type(data), list)
        self.assertEqual(len(data), 0)


    def test_global_upstream_healthcheck_status(self):
        now = random.randint(1, int(time.time()))
        up_id = self.client.new_global_upstream(
            name='origin-upstream' + str(now),
            servers=[
                {'domain': 'test.com', 'port': 80},
                {'ip': '172.22.31.2', 'port': 80, 'weight': 2}
            ],
            health_checker={
                'http_req_uri': '/status',
                'http_req_host': 'test.com',
                'interval': 3,
                'interval_unit': 'sec',
                'timeout': 1,
                'fall': 3,
                'rise': 2,
                'valid_statuses': [200, 302],
                'report_interval': 3,
                'report_interval_unit': 'min'
            })
        self.assertIs(type(up_id), int)
        self.assertGreater(up_id, 0)

        data = self.client.get_global_upstream_healthcheck_status(up_id)
        self.assertIs(type(data), dict)
        data = data['data']
        self.assertIs(type(data), list)
        self.assertEqual(len(data), 0)
