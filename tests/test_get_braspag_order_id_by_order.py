# -*- coding: utf8 -*-
from __future__ import absolute_import
from uuid import uuid4

from tornado.testing import gen_test

from braspag.consts import PAYMENT_METHODS

from .base import BraspagTestCase
from .vcrutils import replay


class GetTransactionDataTest(BraspagTestCase):

    @gen_test
    @replay
    def test_get_braspag_order_id_by_order(self):
        order_id = uuid4()
        response = yield self.braspag.authorize(**{
            'request_id': '782a56e2-2dae-11e2-b3ee-080027d29772',
            'order_id': order_id,
            'customer_id': '12345678900',
            'customer_name': u'José da Silva',
            'customer_email': 'jose123@dasilva.com.br',
            'transactions': [{
                'amount': 100000,
                'card_holder': 'Jose da Silva',
                'card_number': '0000000000000001',
                'card_security_code': '123',
                'card_exp_date': '05/2018',
                'save_card': True,
                'payment_method': PAYMENT_METHODS['Simulated']['BRL'],
                'soft_descriptor': u'Sax Alto Chinês',
            }],
        })
        assert response.success == True
        braspag_order_id = response.braspag_order_id
        braspag_transaction_id = response.transactions[0]['braspag_transaction_id']

        response = yield self.braspag.get_braspag_order_id_by_order(**{
            'request_id': '782a56e2-2dae-11e2-b3ee-080027d29772',
            'order_id': order_id,
        })

        assert response.success == True
        response.orders.reverse()
        assert response.orders[0]['braspag_transaction_id'] == braspag_transaction_id
        assert response.orders[0]['braspag_order_id'] == braspag_order_id
