import unittest


class TestConstsAtRuntime(unittest.TestCase):
    def test_constants_cannot_be_mutable(self):
        from constantia.tests.decorators.check_at_runtime.cases.constants_cannot_be_mutable import func

        with self.assertRaises(TypeError) as context:
            func()

        self.assertEqual('Assignment of non-immutable type to constant "x" detected on line 3 (x = [1, 2, 3]).',
                         str(context.exception))

    def test_constants_cannot_be_reassigned(self):
        from constantia.tests.decorators.check_at_runtime.cases.constants_cannot_be_reassigned import func

        with self.assertRaises(ValueError) as context:
            func()

        self.assertEqual('Reassignment of constant "x" detected on line 4 (x = 20).', str(context.exception))

    def test_constants_ok(self):
        from constantia.tests.decorators.check_at_runtime.cases.ok import func

        self.assertEqual((1, 2, 3), func())

    def test_class_constants_cannot_be_reassigned(self):
        from constantia.tests.decorators.check_at_runtime.cases.class_constants_cannot_be_reassigned import Example

        with self.assertRaises(ValueError) as context:
            Example()

        self.assertEqual('Reassignment of constant "X" detected on line 4 (X = 8888).', str(context.exception))

    def test_class_constants_cannot_be_reassigned_in_class_method(self):
        from constantia.tests.decorators.check_at_runtime.cases.class_constants_cannot_be_reassigned_in_class_method import Example

        with self.assertRaises(ValueError) as context:
            e = Example()
            e.change_x()

        self.assertEqual('Reassignment of class constant "X" detected on line 7 (cls.X = 8888).', str(context.exception))

    def test_class_constants_cannot_be_reassigned_in_instance_method(self):
        from constantia.tests.decorators.check_at_runtime.cases.class_constants_cannot_be_reassigned_in_instance_method import Example

        with self.assertRaises(ValueError) as context:
            e = Example()
            e.change_x()

        self.assertEqual(
            'Reassignment of class constant "X" detected on line 6 (self.__class__.X = 8888).',
            str(context.exception)
        )

    def test_class_constants_cannot_be_reassigned_in_static_method(self):
        from constantia.tests.decorators.check_at_runtime.cases.class_constants_cannot_be_reassigned_in_static_method import Example

        with self.assertRaises(ValueError) as context:
            Example()

        self.assertEqual(
            'Static reassignment of class constant "X" detected on line 7 (Example.X = 8888).',
            str(context.exception)
        )

    def test_class_constants_ok(self):
        from constantia.tests.decorators.check_at_runtime.cases.class_constants_ok import Example

        Example()
