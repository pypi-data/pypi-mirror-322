# -*- coding: utf-8 -*-
# import io
import sdk_test


class TestAppIPList(sdk_test.TestSdk):
    def test_ip_list(self):
        # create
        rule_id = self.client.new_ip_list(name='ip_list_1', items=[{'ip': '127.0.0.1'}])
        self.assertIsInstance(rule_id, int)

        # get
        ip_list_1 = self.client.get_ip_list(rule_id)
        self.assertEqual(ip_list_1.get('name'), 'ip_list_1')

        # modify
        self.client.put_ip_list(rule_id=rule_id, items=[{'ip': '192.168.1.1'}])
        ip_list_1 = self.client.get_ip_list(rule_id)
        self.assertEqual(ip_list_1.get('items')[0].get('ip'), '192.168.1.1')

        # append
        self.client.append_to_ip_list(rule_id=rule_id, items=[{'ip': '192.168.1.2'}])
        ip_list_2 = self.client.get_ip_list(rule_id)
        self.assertEqual(ip_list_2.get('items')[0].get('ip'), '192.168.1.1')
        self.assertEqual(ip_list_2.get('items')[1].get('ip'), '192.168.1.2')

        # remove
        self.client.remove_from_ip_list(rule_id=rule_id, items=[{'ip': '192.168.1.2'}])
        ip_list_3 = self.client.get_ip_list(rule_id)
        self.assertEqual(ip_list_3.get('items')[0].get('ip'), '192.168.1.1')
        self.assertEqual(1, len(ip_list_3.get('items', [])))

        # delete
        ok = self.client.del_ip_list(rule_id=rule_id)
        self.assertTrue(ok)


    def test_ip_list2(self):
        # delete all global ip lists first
        ip_lists = self.client.get_all_ip_lists(detail=False)
        if ip_lists:
            for ip_list in ip_lists:
                self.client.del_ip_list(rule_id=ip_list['id'])

        # create the first ip list
        rule_id = self.client.new_ip_list(name='ip_list_1',
                                                 items=[{'ip': '127.0.0.2'}, {'ip': '127.0.0.3'}])
        self.assertIsInstance(rule_id, int)

        # create the second ip list
        rule_id2 = self.client.new_ip_list(name='ip_list_2',
                                                  items=[{'ip': '127.0.0.4'}])
        self.assertIsInstance(rule_id2, int)

        ip_lists = self.client.get_all_ip_lists()
        self.assertEqual(len(ip_lists), 2)
        self.assertEqual(ip_lists[0]['id'], rule_id)
        self.assertEqual(ip_lists[1]['id'], rule_id2)

        ip_list_1 = ip_lists[0]
        ip_list_2 = ip_lists[1]
        self.assertEqual(ip_list_1['items'][0]['ip'], '127.0.0.2')
        self.assertEqual(ip_list_1['items'][1]['ip'], '127.0.0.3')
        self.assertEqual(ip_list_2['items'][0]['ip'], '127.0.0.4')
