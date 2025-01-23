import unittest


class TestConstsAtImport(unittest.TestCase):
    def test_constants_cannot_be_mutable(self):
        with self.assertRaises(TypeError) as context:
            from constantia.tests.decorators.check_at_import.cases.constants_cannot_be_mutable import func  # noqa

        self.assertEqual('Assignment of non-immutable type to constant "x" detected on line 3 (x = [1, 2, 3]).', str(context.exception))

    def test_constants_cannot_be_reassigned(self):
        with self.assertRaises(ValueError) as context:
            from constantia.tests.decorators.check_at_import.cases.constants_cannot_be_reassigned import func  # noqa

        self.assertEqual('Reassignment of constant "x" detected on line 4 (x = 20).', str(context.exception))

    def test_class_constants_cannot_be_reassigned_in_class_method(self):
        with self.assertRaises(ValueError) as context:
            from constantia.tests.decorators.check_at_import.cases.class_constants_cannot_be_reassigned_in_class_method import Example  # noqa

        self.assertEqual(
            'Reassignment of class constant "X" detected on line 7 (cls.X = 8888).',
            str(context.exception)
        )

    def test_class_constants_cannot_be_reassigned_in_static_method(self):
        with self.assertRaises(ValueError) as context:
            from constantia.tests.decorators.check_at_import.cases.class_constants_cannot_be_reassigned_in_static_method import Example  # noqa

        self.assertEqual(
            'Static reassignment of class constant "X" detected on line 7 (Example.X = 8888).',
            str(context.exception)
        )

    def test_constants_ok(self):
        from constantia.tests.decorators.check_at_import.cases.ok import func

        self.assertEqual((1, 2, 3), func())

    def test_class_constants_cannot_be_reassigned(self):
        with self.assertRaises(ValueError) as context:
            from constantia.tests.decorators.check_at_import.cases.class_constants_cannot_be_reassigned import Example  # noqa

        self.assertEqual('Reassignment of constant "X" detected on line 4 (X = 9999).', str(context.exception))

    def test_class_constants_ok(self):
        from constantia.tests.decorators.check_at_import.cases.class_constants_ok import Example

        Example()
