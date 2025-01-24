# -*- coding: utf-8 -*-
# import io
import sdk_test


class TestIPList(sdk_test.TestSdk):
    def test_global_ip_list(self):
        # create
        global_rule_id = self.client.new_global_ip_list(name='g_ip_list_1',
                                                        items=[{'ip': '127.0.0.2'}])
        self.assertIsInstance(global_rule_id, int)

        # get
        g_ip_list_1 = self.client.get_global_ip_list(global_rule_id)
        self.assertEqual(g_ip_list_1.get('name'), 'g_ip_list_1')

        # modify
        self.client.put_global_ip_list(rule_id=global_rule_id,
                                       items=[{'ip': '192.168.1.2'}])
        g_ip_list_1 = self.client.get_global_ip_list(global_rule_id)
        self.assertEqual(g_ip_list_1.get('items')[0].get('ip'), '192.168.1.2')

        # append
        self.client.append_to_global_ip_list(rule_id=global_rule_id, items=[{'ip': '192.168.1.3'}])
        g_ip_list_2 = self.client.get_global_ip_list(global_rule_id)
        self.assertEqual(g_ip_list_2.get('items')[0].get('ip'), '192.168.1.2')
        self.assertEqual(g_ip_list_2.get('items')[1].get('ip'), '192.168.1.3')

        # remove
        self.client.remove_from_global_ip_list(rule_id=global_rule_id,
                                        items=[{'ip': '192.168.1.2'}])
        g_ip_list_3 = self.client.get_global_ip_list(global_rule_id)
        self.assertEqual(g_ip_list_3.get('items')[0].get('ip'), '192.168.1.3')
        self.assertEqual(1, len(g_ip_list_3.get('items', [])))

        # delete
        ok = self.client.del_global_ip_list(rule_id=global_rule_id)
        self.assertTrue(ok)

    def test_global_ip_list2(self):
        # delete all global ip lists first
        ip_lists = self.client.get_all_global_ip_lists(detail=False)
        if ip_lists:
            for ip_list in ip_lists:
                self.client.del_global_ip_list(rule_id=ip_list['id'])

        # create the first ip list
        global_rule_id = self.client.new_global_ip_list(name='g_ip_list_1',
                                                        items=[{'ip': '127.0.0.2'}, {'ip': '127.0.0.3'}])
        self.assertIsInstance(global_rule_id, int)

        # create the second ip list
        global_rule_id2 = self.client.new_global_ip_list(name='g_ip_list_2',
                                                        items=[{'ip': '127.0.0.4'}])
        self.assertIsInstance(global_rule_id2, int)

        ip_lists = self.client.get_all_global_ip_lists()
        self.assertEqual(len(ip_lists), 2)
        self.assertEqual(ip_lists[0]['id'], global_rule_id)
        self.assertEqual(ip_lists[1]['id'], global_rule_id2)

        ip_list_1 = ip_lists[0]
        ip_list_2 = ip_lists[1]
        self.assertEqual(ip_list_1['items'][0]['ip'], '127.0.0.2')
        self.assertEqual(ip_list_1['items'][1]['ip'], '127.0.0.3')
        self.assertEqual(ip_list_2['items'][0]['ip'], '127.0.0.4')

        # delete
        ok = self.client.del_global_ip_list(rule_id=global_rule_id)
        self.assertTrue(ok)

        # delete
        ok = self.client.del_global_ip_list(rule_id=global_rule_id2)
        self.assertTrue(ok)
