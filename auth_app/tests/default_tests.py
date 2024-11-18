from rest_framework.serializers import ValidationError
from rest_framework.test import APITestCase


class DefaultCases(APITestCase):
    def contains_fields_test(self, resp, fields, status):
        for field in fields:
            self.assertContains(resp, field, status_code=status)

    def error_tests(self, ser, data, status, msg):
        resp = self.client.post(self.url, data)
        self.http_status_test(resp=resp, status=status)
        self.message_test(ser=ser, data=data, msg=msg)

    def http_status_test(self, resp, status):
        self.assertEqual(resp.status_code, status)

    def message_test(self, ser, data, msg):
        serializer = ser(data=data)
        self.assertRaisesMessage(ValidationError, msg, serializer.is_valid, raise_exception=True)
