import unittest

from uhppote_rfid import SerialNumber, SerialNumberException


class TestSerialNumber(unittest.TestCase):
    """
    Tests the SerialNumber class and related classes.
    """


    # SerialNumber.__init__()

    def test_constructor_Integer_NegativeException(self):
        with self.assertRaises(SerialNumberException):
            SerialNumber(-1)

    def test_constructor_Integer_TooLargeException(self):
        with self.assertRaises(SerialNumberException):
            SerialNumber(1000000000)

    def test_constructor_StringInteger_NegativeException(self):
        with self.assertRaises(SerialNumberException):
            SerialNumber("-1")

    def test_constructor_StringInteger_TooLargeException(self):
        with self.assertRaises(SerialNumberException):
            SerialNumber("1000000000")

    def test_constructor_Hexadecimal_NegativeException(self):
        with self.assertRaises(SerialNumberException):
            SerialNumber(-0x1)

    def test_constructor_Hexadecimal_TooLargeException(self):
        with self.assertRaises(SerialNumberException):
            SerialNumber(0x3b9aca00)

    def test_constructor_StringHexadecimal_BadCharacterException(self):
        with self.assertRaises(SerialNumberException):
            SerialNumber("0x1pa42345")

    def test_constructor_StringHexadecimal_NegativeException(self):
        with self.assertRaises(SerialNumberException):
            SerialNumber("-0x1")

    def test_constructor_StringHexadecimal_TooLargeException(self):
        with self.assertRaises(SerialNumberException):
            SerialNumber("0x3b9aca00")

    def test_constructor_String_BadCharacterException(self):
        with self.assertRaises(SerialNumberException):
            SerialNumber("1pa42345")

    def test_constructor_String_TooShortException(self):
        with self.assertRaises(SerialNumberException):
            SerialNumber("1abcdef")

    def test_constructor_String_TooLongException(self):
        with self.assertRaises(SerialNumberException):
            SerialNumber("123abcdef")

    def test_constructor_String_NegativeException(self):
        with self.assertRaises(SerialNumberException):
            SerialNumber("-12b2cac")

    def test_constructor_String_TooLargeException(self):
        with self.assertRaises(SerialNumberException):
            SerialNumber("3b9aca00")

    def test_constructor_ByteArray_TooShortException(self):
        with self.assertRaises(SerialNumberException):
            SerialNumber(bytearray([0x1, 0x2, 0x3]))

    def test_constructor_ByteArray_TooLongException(self):
        with self.assertRaises(SerialNumberException):
            SerialNumber(bytearray([0x1, 0x2, 0x3, 0x4, 0x5]))

    def test_constructor_Float_Exception(self):
        with self.assertRaises(SerialNumberException):
            SerialNumber(1.1)

    def test_constructor_Complex_Exception(self):
        with self.assertRaises(SerialNumberException):
            SerialNumber(complex(1, 2))

    def test_constructor_Bytes_Exception(self):
        with self.assertRaises(SerialNumberException):
            SerialNumber(bytes(1))

    def test_constructor_List_Exception(self):
        with self.assertRaises(SerialNumberException):
            SerialNumber([1, 2, 3, 4])

    def test_constructor_Dict_Exception(self):
        with self.assertRaises(SerialNumberException):
            SerialNumber({
                'a': 1,
                'b': 2,
                'c': 3,
                'd': 4,
            })

    def test_constructor_Tuple_Exception(self):
        with self.assertRaises(SerialNumberException):
            SerialNumber((1, 2))

    def test_constructor_Set_Exception(self):
        with self.assertRaises(SerialNumberException):
            SerialNumber(set("test"))

    def test_constructor_FrozenSet_Exception(self):
        with self.assertRaises(SerialNumberException):
            SerialNumber(frozenset("test"))


    # SerialNumber.getInteger()

    def test_getInteger_NormalValue_IsEqual(self):
        self.assertEqual(SerialNumber(112233445).getInteger(), 112233445)
        self.assertEqual(SerialNumber("112233445").getInteger(), 112233445)
        self.assertEqual(SerialNumber(0x6b08be5).getInteger(), 112233445)
        self.assertEqual(SerialNumber("0x6b08be5").getInteger(), 112233445)
        self.assertEqual(SerialNumber("06b08be5").getInteger(), 112233445)
        self.assertEqual(SerialNumber(bytearray([0x6, 0xb0, 0x8b, 0xe5])).getInteger(), 112233445)

    def test_getInteger_MinimumValue_IsEqual(self):
        self.assertEqual(SerialNumber(0).getInteger(), 0)
        self.assertEqual(SerialNumber("000000000").getInteger(), 0)
        self.assertEqual(SerialNumber(0x0).getInteger(), 0)
        self.assertEqual(SerialNumber("0x0").getInteger(), 0)
        self.assertEqual(SerialNumber("00000000").getInteger(), 0)
        self.assertEqual(SerialNumber(bytearray([0x0, 0x0, 0x0, 0x0])).getInteger(), 0)

    def test_getInteger_MaximumValue_IsEqual(self):
        self.assertEqual(SerialNumber(999999999).getInteger(), 999999999)
        self.assertEqual(SerialNumber("999999999").getInteger(), 999999999)
        self.assertEqual(SerialNumber(0x3b9ac9ff).getInteger(), 999999999)
        self.assertEqual(SerialNumber("0x3b9ac9ff").getInteger(), 999999999)
        self.assertEqual(SerialNumber("3b9ac9ff").getInteger(), 999999999)
        self.assertEqual(SerialNumber(bytearray([0x3b, 0x9a, 0xc9, 0xff])).getInteger(), 999999999)


    # SerialNumber.getIntegerString()


    def test_getIntegerString_NormalValue_IsEqual(self):
        self.assertEqual(SerialNumber(112233445).getIntegerString(), "112233445")
        self.assertEqual(SerialNumber("112233445").getIntegerString(), "112233445")
        self.assertEqual(SerialNumber(0x6b08be5).getIntegerString(), "112233445")
        self.assertEqual(SerialNumber("0x6b08be5").getIntegerString(), "112233445")
        self.assertEqual(SerialNumber("06b08be5").getIntegerString(), "112233445")
        self.assertEqual(SerialNumber(bytearray([0x6, 0xb0, 0x8b, 0xe5])).getIntegerString(), "112233445")

    def test_getIntegerString_MinimumValue_IsEqual(self):
        self.assertEqual(SerialNumber(0).getIntegerString(), "000000000")
        self.assertEqual(SerialNumber("000000000").getIntegerString(), "000000000")
        self.assertEqual(SerialNumber(0x0).getIntegerString(), "000000000")
        self.assertEqual(SerialNumber("0x0").getIntegerString(), "000000000")
        self.assertEqual(SerialNumber("00000000").getIntegerString(), "000000000")
        self.assertEqual(SerialNumber(bytearray([0x0, 0x0, 0x0, 0x0])).getIntegerString(), "000000000")

    def test_getIntegerString_MaximumValue_IsEqual(self):
        self.assertEqual(SerialNumber(999999999).getIntegerString(), "999999999")
        self.assertEqual(SerialNumber("999999999").getIntegerString(), "999999999")
        self.assertEqual(SerialNumber(0x3b9ac9ff).getIntegerString(), "999999999")
        self.assertEqual(SerialNumber("0x3b9ac9ff").getIntegerString(), "999999999")
        self.assertEqual(SerialNumber("3b9ac9ff").getIntegerString(), "999999999")
        self.assertEqual(SerialNumber(bytearray([0x3b, 0x9a, 0xc9, 0xff])).getIntegerString(), "999999999")

    def test_getIntegerString_FirstOrder_IsEqual(self):
        self.assertEqual(SerialNumber(1).getIntegerString(), "000000001")
        self.assertEqual(SerialNumber("000000001").getIntegerString(), "000000001")
        self.assertEqual(SerialNumber(0x1).getIntegerString(), "000000001")
        self.assertEqual(SerialNumber("0x1").getIntegerString(), "000000001")
        self.assertEqual(SerialNumber("00000001").getIntegerString(), "000000001")
        self.assertEqual(SerialNumber(bytearray([0x0, 0x0, 0x0, 0x1])).getIntegerString(), "000000001")

    def test_getIntegerString_MaxFirstOrder_IsEqual(self):
        self.assertEqual(SerialNumber(15).getIntegerString(), "000000015")
        self.assertEqual(SerialNumber("000000015").getIntegerString(), "000000015")
        self.assertEqual(SerialNumber(0xf).getIntegerString(), "000000015")
        self.assertEqual(SerialNumber("0xf").getIntegerString(), "000000015")
        self.assertEqual(SerialNumber("0000000f").getIntegerString(), "000000015")
        self.assertEqual(SerialNumber(bytearray([0x0, 0x0, 0x0, 0xf])).getIntegerString(), "000000015")

    def test_getIntegerString_SecondOrder_IsEqual(self):
        self.assertEqual(SerialNumber(16).getIntegerString(), "000000016")
        self.assertEqual(SerialNumber("000000016").getIntegerString(), "000000016")
        self.assertEqual(SerialNumber(0x10).getIntegerString(), "000000016")
        self.assertEqual(SerialNumber("0x10").getIntegerString(), "000000016")
        self.assertEqual(SerialNumber("00000010").getIntegerString(), "000000016")
        self.assertEqual(SerialNumber(bytearray([0x0, 0x0, 0x0, 0x10])).getIntegerString(), "000000016")


    # SerialNumber.getHexadecimal()


    def test_getHexadecimal_NormalValue_IsEqual(self):
        self.assertEqual(SerialNumber(112233445).getHexadecimal(), "0x6b08be5")
        self.assertEqual(SerialNumber("112233445").getHexadecimal(), "0x6b08be5")
        self.assertEqual(SerialNumber(0x6b08be5).getHexadecimal(), "0x6b08be5")
        self.assertEqual(SerialNumber("0x6b08be5").getHexadecimal(), "0x6b08be5")
        self.assertEqual(SerialNumber("06b08be5").getHexadecimal(), "0x6b08be5")
        self.assertEqual(SerialNumber(bytearray([0x6, 0xb0, 0x8b, 0xe5])).getHexadecimal(), "0x6b08be5")

    def test_getHexadecimal_MinimumValue_IsEqual(self):
        self.assertEqual(SerialNumber(0).getHexadecimal(), "0x0")
        self.assertEqual(SerialNumber("000000000").getHexadecimal(), "0x0")
        self.assertEqual(SerialNumber(0x0).getHexadecimal(), "0x0")
        self.assertEqual(SerialNumber("0x0").getHexadecimal(), "0x0")
        self.assertEqual(SerialNumber("00000000").getHexadecimal(), "0x0")
        self.assertEqual(SerialNumber(bytearray([0x0, 0x0, 0x0, 0x0])).getHexadecimal(), "0x0")

    def test_getHexadecimal_MaximumValue_IsEqual(self):
        self.assertEqual(SerialNumber(999999999).getHexadecimal(), "0x3b9ac9ff")
        self.assertEqual(SerialNumber("999999999").getHexadecimal(), "0x3b9ac9ff")
        self.assertEqual(SerialNumber(0x3b9ac9ff).getHexadecimal(), "0x3b9ac9ff")
        self.assertEqual(SerialNumber("0x3b9ac9ff").getHexadecimal(), "0x3b9ac9ff")
        self.assertEqual(SerialNumber("3b9ac9ff").getHexadecimal(), "0x3b9ac9ff")
        self.assertEqual(SerialNumber(bytearray([0x3b, 0x9a, 0xc9, 0xff])).getHexadecimal(), "0x3b9ac9ff")

    def test_getHexadecimal_FirstOrder_IsEqual(self):
        self.assertEqual(SerialNumber(1).getHexadecimal(), "0x1")
        self.assertEqual(SerialNumber("000000001").getHexadecimal(), "0x1")
        self.assertEqual(SerialNumber(0x1).getHexadecimal(), "0x1")
        self.assertEqual(SerialNumber("0x1").getHexadecimal(), "0x1")
        self.assertEqual(SerialNumber("00000001").getHexadecimal(), "0x1")
        self.assertEqual(SerialNumber(bytearray([0x0, 0x0, 0x0, 0x1])).getHexadecimal(), "0x1")

    def test_getHexadecimal_MaxFirstOrder_IsEqual(self):
        self.assertEqual(SerialNumber(15).getHexadecimal(), "0xf")
        self.assertEqual(SerialNumber("000000015").getHexadecimal(), "0xf")
        self.assertEqual(SerialNumber(0xf).getHexadecimal(), "0xf")
        self.assertEqual(SerialNumber("0xf").getHexadecimal(), "0xf")
        self.assertEqual(SerialNumber("0000000f").getHexadecimal(), "0xf")
        self.assertEqual(SerialNumber(bytearray([0x0, 0x0, 0x0, 0xf])).getHexadecimal(), "0xf")

    def test_getHexadecimal_SecondOrder_IsEqual(self):
        self.assertEqual(SerialNumber(16).getHexadecimal(), "0x10")
        self.assertEqual(SerialNumber("000000016").getHexadecimal(), "0x10")
        self.assertEqual(SerialNumber(0x10).getHexadecimal(), "0x10")
        self.assertEqual(SerialNumber("0x10").getHexadecimal(), "0x10")
        self.assertEqual(SerialNumber("00000010").getHexadecimal(), "0x10")
        self.assertEqual(SerialNumber(bytearray([0x0, 0x0, 0x0, 0x10])).getHexadecimal(), "0x10")


    # SerialNumber.getHexadecimalString()


    def test_getHexadecimalString_NormalValue_IsEqual(self):
        self.assertEqual(SerialNumber(112233445).getHexadecimalString(), "06b08be5")
        self.assertEqual(SerialNumber("112233445").getHexadecimalString(), "06b08be5")
        self.assertEqual(SerialNumber(0x6b08be5).getHexadecimalString(), "06b08be5")
        self.assertEqual(SerialNumber("0x6b08be5").getHexadecimalString(), "06b08be5")
        self.assertEqual(SerialNumber("06b08be5").getHexadecimalString(), "06b08be5")
        self.assertEqual(SerialNumber(bytearray([0x6, 0xb0, 0x8b, 0xe5])).getHexadecimalString(), "06b08be5")

    def test_getHexadecimalString_MinimumValue_IsEqual(self):
        self.assertEqual(SerialNumber(0).getHexadecimalString(), "00000000")
        self.assertEqual(SerialNumber("000000000").getHexadecimalString(), "00000000")
        self.assertEqual(SerialNumber(0x0).getHexadecimalString(), "00000000")
        self.assertEqual(SerialNumber("0x0").getHexadecimalString(), "00000000")
        self.assertEqual(SerialNumber("00000000").getHexadecimalString(), "00000000")
        self.assertEqual(SerialNumber(bytearray([0x0, 0x0, 0x0, 0x0])).getHexadecimalString(), "00000000")

    def test_getHexadecimalString_MaximumValue_IsEqual(self):
        self.assertEqual(SerialNumber(999999999).getHexadecimalString(), "3b9ac9ff")
        self.assertEqual(SerialNumber("999999999").getHexadecimalString(), "3b9ac9ff")
        self.assertEqual(SerialNumber(0x3b9ac9ff).getHexadecimalString(), "3b9ac9ff")
        self.assertEqual(SerialNumber("0x3b9ac9ff").getHexadecimalString(), "3b9ac9ff")
        self.assertEqual(SerialNumber("3b9ac9ff").getHexadecimalString(), "3b9ac9ff")
        self.assertEqual(SerialNumber(bytearray([0x3b, 0x9a, 0xc9, 0xff])).getHexadecimalString(), "3b9ac9ff")

    def test_getHexadecimalString_FirstOrder_IsEqual(self):
        self.assertEqual(SerialNumber(1).getHexadecimalString(), "00000001")
        self.assertEqual(SerialNumber("000000001").getHexadecimalString(), "00000001")
        self.assertEqual(SerialNumber(0x1).getHexadecimalString(), "00000001")
        self.assertEqual(SerialNumber("0x1").getHexadecimalString(), "00000001")
        self.assertEqual(SerialNumber("00000001").getHexadecimalString(), "00000001")
        self.assertEqual(SerialNumber(bytearray([0x0, 0x0, 0x0, 0x1])).getHexadecimalString(), "00000001")

    def test_getHexadecimalString_MaxFirstOrder_IsEqual(self):
        self.assertEqual(SerialNumber(15).getHexadecimalString(), "0000000f")
        self.assertEqual(SerialNumber("000000015").getHexadecimalString(), "0000000f")
        self.assertEqual(SerialNumber(0xf).getHexadecimalString(), "0000000f")
        self.assertEqual(SerialNumber("0xf").getHexadecimalString(), "0000000f")
        self.assertEqual(SerialNumber("0000000f").getHexadecimalString(), "0000000f")
        self.assertEqual(SerialNumber(bytearray([0x0, 0x0, 0x0, 0xf])).getHexadecimalString(), "0000000f")

    def test_getHexadecimalString_SecondOrder_IsEqual(self):
        self.assertEqual(SerialNumber(16).getHexadecimalString(), "00000010")
        self.assertEqual(SerialNumber("000000016").getHexadecimalString(), "00000010")
        self.assertEqual(SerialNumber(0x10).getHexadecimalString(), "00000010")
        self.assertEqual(SerialNumber("0x10").getHexadecimalString(), "00000010")
        self.assertEqual(SerialNumber("00000010").getHexadecimalString(), "00000010")
        self.assertEqual(SerialNumber(bytearray([0x0, 0x0, 0x0, 0x10])).getHexadecimalString(), "00000010")

    def test_getHexadecimalString_ReverseNormalValue_IsEqual(self):
        self.assertEqual(SerialNumber(112233445).getHexadecimalString(True), "e58bb006")
        self.assertEqual(SerialNumber("112233445").getHexadecimalString(True), "e58bb006")
        self.assertEqual(SerialNumber(0x6b08be5).getHexadecimalString(True), "e58bb006")
        self.assertEqual(SerialNumber("0x6b08be5").getHexadecimalString(True), "e58bb006")
        self.assertEqual(SerialNumber("06b08be5").getHexadecimalString(True), "e58bb006")
        self.assertEqual(SerialNumber(bytearray([0x6, 0xb0, 0x8b, 0xe5])).getHexadecimalString(True), "e58bb006")

    def test_getHexadecimalString_ReverseMinimumValue_IsEqual(self):
        self.assertEqual(SerialNumber(0).getHexadecimalString(True), "00000000")
        self.assertEqual(SerialNumber("000000000").getHexadecimalString(True), "00000000")
        self.assertEqual(SerialNumber(0x0).getHexadecimalString(True), "00000000")
        self.assertEqual(SerialNumber("0x0").getHexadecimalString(True), "00000000")
        self.assertEqual(SerialNumber("00000000").getHexadecimalString(True), "00000000")
        self.assertEqual(SerialNumber(bytearray([0x0, 0x0, 0x0, 0x0])).getHexadecimalString(True), "00000000")

    def test_getHexadecimalString_ReverseMaximumValue_IsEqual(self):
        self.assertEqual(SerialNumber(999999999).getHexadecimalString(True), "ffc99a3b")
        self.assertEqual(SerialNumber("999999999").getHexadecimalString(True), "ffc99a3b")
        self.assertEqual(SerialNumber(0x3b9ac9ff).getHexadecimalString(True), "ffc99a3b")
        self.assertEqual(SerialNumber("0x3b9ac9ff").getHexadecimalString(True), "ffc99a3b")
        self.assertEqual(SerialNumber("3b9ac9ff").getHexadecimalString(True), "ffc99a3b")
        self.assertEqual(SerialNumber(bytearray([0x3b, 0x9a, 0xc9, 0xff])).getHexadecimalString(True), "ffc99a3b")

    def test_getHexadecimalString_ReverseFirstOrder_IsEqual(self):
        self.assertEqual(SerialNumber(1).getHexadecimalString(True), "01000000")
        self.assertEqual(SerialNumber("000000001").getHexadecimalString(True), "01000000")
        self.assertEqual(SerialNumber(0x1).getHexadecimalString(True), "01000000")
        self.assertEqual(SerialNumber("0x1").getHexadecimalString(True), "01000000")
        self.assertEqual(SerialNumber("00000001").getHexadecimalString(True), "01000000")
        self.assertEqual(SerialNumber(bytearray([0x0, 0x0, 0x0, 0x1])).getHexadecimalString(True), "01000000")

    def test_getHexadecimalString_ReverseMaxFirstOrder_IsEqual(self):
        self.assertEqual(SerialNumber(15).getHexadecimalString(True), "0f000000")
        self.assertEqual(SerialNumber("000000015").getHexadecimalString(True), "0f000000")
        self.assertEqual(SerialNumber(0xf).getHexadecimalString(True), "0f000000")
        self.assertEqual(SerialNumber("0xf").getHexadecimalString(True), "0f000000")
        self.assertEqual(SerialNumber("0000000f").getHexadecimalString(True), "0f000000")
        self.assertEqual(SerialNumber(bytearray([0x0, 0x0, 0x0, 0xf])).getHexadecimalString(True), "0f000000")

    def test_getHexadecimalString_ReverseSecondOrder_IsEqual(self):
        self.assertEqual(SerialNumber(16).getHexadecimalString(True), "10000000")
        self.assertEqual(SerialNumber("000000016").getHexadecimalString(True), "10000000")
        self.assertEqual(SerialNumber(0x10).getHexadecimalString(True), "10000000")
        self.assertEqual(SerialNumber("0x10").getHexadecimalString(True), "10000000")
        self.assertEqual(SerialNumber("00000010").getHexadecimalString(True), "10000000")
        self.assertEqual(SerialNumber(bytearray([0x0, 0x0, 0x0, 0x10])).getHexadecimalString(True), "10000000")


    # SerialNumber.getByteArray()


    def test_getByteArray_NormalValue_IsEqual(self):
        self.assertEqual(SerialNumber(112233445).getByteArray(), bytearray([0x6, 0xb0, 0x8b, 0xe5]))
        self.assertEqual(SerialNumber("112233445").getByteArray(), bytearray([0x6, 0xb0, 0x8b, 0xe5]))
        self.assertEqual(SerialNumber(0x6b08be5).getByteArray(), bytearray([0x6, 0xb0, 0x8b, 0xe5]))
        self.assertEqual(SerialNumber("0x6b08be5").getByteArray(), bytearray([0x6, 0xb0, 0x8b, 0xe5]))
        self.assertEqual(SerialNumber("06b08be5").getByteArray(), bytearray([0x6, 0xb0, 0x8b, 0xe5]))
        self.assertEqual(SerialNumber(bytearray([0x6, 0xb0, 0x8b, 0xe5])).getByteArray(), bytearray([0x6, 0xb0, 0x8b, 0xe5]))

    def test_getByteArray_MinimumValue_IsEqual(self):
        self.assertEqual(SerialNumber(0).getByteArray(), bytearray([0x0, 0x0, 0x0, 0x0]))
        self.assertEqual(SerialNumber("000000000").getByteArray(), bytearray([0x0, 0x0, 0x0, 0x0]))
        self.assertEqual(SerialNumber(0x0).getByteArray(), bytearray([0x0, 0x0, 0x0, 0x0]))
        self.assertEqual(SerialNumber("0x0").getByteArray(), bytearray([0x0, 0x0, 0x0, 0x0]))
        self.assertEqual(SerialNumber("00000000").getByteArray(), bytearray([0x0, 0x0, 0x0, 0x0]))
        self.assertEqual(SerialNumber(bytearray([0x0, 0x0, 0x0, 0x0])).getByteArray(), bytearray([0x0, 0x0, 0x0, 0x0]))

    def test_getByteArray_MaximumValue_IsEqual(self):
        self.assertEqual(SerialNumber(999999999).getByteArray(), bytearray([0x3b, 0x9a, 0xc9, 0xff]))
        self.assertEqual(SerialNumber("999999999").getByteArray(), bytearray([0x3b, 0x9a, 0xc9, 0xff]))
        self.assertEqual(SerialNumber(0x3b9ac9ff).getByteArray(), bytearray([0x3b, 0x9a, 0xc9, 0xff]))
        self.assertEqual(SerialNumber("0x3b9ac9ff").getByteArray(), bytearray([0x3b, 0x9a, 0xc9, 0xff]))
        self.assertEqual(SerialNumber("3b9ac9ff").getByteArray(), bytearray([0x3b, 0x9a, 0xc9, 0xff]))
        self.assertEqual(SerialNumber(bytearray([0x3b, 0x9a, 0xc9, 0xff])).getByteArray(), bytearray([0x3b, 0x9a, 0xc9, 0xff]))

    def test_getByteArray_FirstOrder_IsEqual(self):
        self.assertEqual(SerialNumber(1).getByteArray(), bytearray([0x0, 0x0, 0x0, 0x1]))
        self.assertEqual(SerialNumber("000000001").getByteArray(), bytearray([0x0, 0x0, 0x0, 0x1]))
        self.assertEqual(SerialNumber(0x1).getByteArray(), bytearray([0x0, 0x0, 0x0, 0x1]))
        self.assertEqual(SerialNumber("0x1").getByteArray(), bytearray([0x0, 0x0, 0x0, 0x1]))
        self.assertEqual(SerialNumber("00000001").getByteArray(), bytearray([0x0, 0x0, 0x0, 0x1]))
        self.assertEqual(SerialNumber(bytearray([0x0, 0x0, 0x0, 0x1])).getByteArray(), bytearray([0x0, 0x0, 0x0, 0x1]))

    def test_getByteArray_MaxFirstOrder_IsEqual(self):
        self.assertEqual(SerialNumber(15).getByteArray(), bytearray([0x0, 0x0, 0x0, 0xf]))
        self.assertEqual(SerialNumber("000000015").getByteArray(), bytearray([0x0, 0x0, 0x0, 0xf]))
        self.assertEqual(SerialNumber(0xf).getByteArray(), bytearray([0x0, 0x0, 0x0, 0xf]))
        self.assertEqual(SerialNumber("0xf").getByteArray(), bytearray([0x0, 0x0, 0x0, 0xf]))
        self.assertEqual(SerialNumber("0000000f").getByteArray(), bytearray([0x0, 0x0, 0x0, 0xf]))
        self.assertEqual(SerialNumber(bytearray([0x0, 0x0, 0x0, 0xf])).getByteArray(), bytearray([0x0, 0x0, 0x0, 0xf]))

    def test_getByteArray_SecondOrder_IsEqual(self):
        self.assertEqual(SerialNumber(16).getByteArray(), bytearray([0x0, 0x0, 0x0, 0x10]))
        self.assertEqual(SerialNumber("000000016").getByteArray(), bytearray([0x0, 0x0, 0x0, 0x10]))
        self.assertEqual(SerialNumber(0x10).getByteArray(), bytearray([0x0, 0x0, 0x0, 0x10]))
        self.assertEqual(SerialNumber("0x10").getByteArray(), bytearray([0x0, 0x0, 0x0, 0x10]))
        self.assertEqual(SerialNumber("00000010").getByteArray(), bytearray([0x0, 0x0, 0x0, 0x10]))
        self.assertEqual(SerialNumber(bytearray([0x0, 0x0, 0x0, 0x10])).getByteArray(), bytearray([0x0, 0x0, 0x0, 0x10]))

    def test_getByteArray_ReverseNormalValue_IsEqual(self):
        self.assertEqual(SerialNumber(112233445).getByteArray(True), bytearray([0xe5, 0x8b, 0xb0, 0x6]))
        self.assertEqual(SerialNumber("112233445").getByteArray(True), bytearray([0xe5, 0x8b, 0xb0, 0x6]))
        self.assertEqual(SerialNumber(0x6b08be5).getByteArray(True), bytearray([0xe5, 0x8b, 0xb0, 0x6]))
        self.assertEqual(SerialNumber("0x6b08be5").getByteArray(True), bytearray([0xe5, 0x8b, 0xb0, 0x6]))
        self.assertEqual(SerialNumber("06b08be5").getByteArray(True), bytearray([0xe5, 0x8b, 0xb0, 0x6]))
        self.assertEqual(SerialNumber(bytearray([0x6, 0xb0, 0x8b, 0xe5])).getByteArray(True), bytearray([0xe5, 0x8b, 0xb0, 0x6]))

    def test_getByteArray_ReverseMinimumValue_IsEqual(self):
        self.assertEqual(SerialNumber(0).getByteArray(True), bytearray([0x0, 0x0, 0x0, 0x0]))
        self.assertEqual(SerialNumber("000000000").getByteArray(True), bytearray([0x0, 0x0, 0x0, 0x0]))
        self.assertEqual(SerialNumber(0x0).getByteArray(True), bytearray([0x0, 0x0, 0x0, 0x0]))
        self.assertEqual(SerialNumber("0x0").getByteArray(True), bytearray([0x0, 0x0, 0x0, 0x0]))
        self.assertEqual(SerialNumber("00000000").getByteArray(True), bytearray([0x0, 0x0, 0x0, 0x0]))
        self.assertEqual(SerialNumber(bytearray([0x0, 0x0, 0x0, 0x0])).getByteArray(True), bytearray([0x0, 0x0, 0x0, 0x0]))

    def test_getByteArray_ReverseMaximumValue_IsEqual(self):
        self.assertEqual(SerialNumber(999999999).getByteArray(True), bytearray([0xff, 0xc9, 0x9a, 0x3b]))
        self.assertEqual(SerialNumber("999999999").getByteArray(True), bytearray([0xff, 0xc9, 0x9a, 0x3b]))
        self.assertEqual(SerialNumber(0x3b9ac9ff).getByteArray(True), bytearray([0xff, 0xc9, 0x9a, 0x3b]))
        self.assertEqual(SerialNumber("0x3b9ac9ff").getByteArray(True), bytearray([0xff, 0xc9, 0x9a, 0x3b]))
        self.assertEqual(SerialNumber("3b9ac9ff").getByteArray(True), bytearray([0xff, 0xc9, 0x9a, 0x3b]))
        self.assertEqual(SerialNumber(bytearray([0x3b, 0x9a, 0xc9, 0xff])).getByteArray(True), bytearray([0xff, 0xc9, 0x9a, 0x3b]))

    def test_getByteArray_ReverseFirstOrder_IsEqual(self):
        self.assertEqual(SerialNumber(1).getByteArray(True), bytearray([0x1, 0x0, 0x0, 0x0]))
        self.assertEqual(SerialNumber("000000001").getByteArray(True), bytearray([0x1, 0x0, 0x0, 0x0]))
        self.assertEqual(SerialNumber(0x1).getByteArray(True), bytearray([0x1, 0x0, 0x0, 0x0]))
        self.assertEqual(SerialNumber("0x1").getByteArray(True), bytearray([0x1, 0x0, 0x0, 0x0]))
        self.assertEqual(SerialNumber("00000001").getByteArray(True), bytearray([0x1, 0x0, 0x0, 0x0]))
        self.assertEqual(SerialNumber(bytearray([0x0, 0x0, 0x0, 0x1])).getByteArray(True), bytearray([0x1, 0x0, 0x0, 0x0]))

    def test_getByteArray_ReverseMaxFirstOrder_IsEqual(self):
        self.assertEqual(SerialNumber(15).getByteArray(True), bytearray([0xf, 0x0, 0x0, 0x0]))
        self.assertEqual(SerialNumber("000000015").getByteArray(True), bytearray([0xf, 0x0, 0x0, 0x0]))
        self.assertEqual(SerialNumber(0xf).getByteArray(True), bytearray([0xf, 0x0, 0x0, 0x0]))
        self.assertEqual(SerialNumber("0xf").getByteArray(True), bytearray([0xf, 0x0, 0x0, 0x0]))
        self.assertEqual(SerialNumber("0000000f").getByteArray(True), bytearray([0xf, 0x0, 0x0, 0x0]))
        self.assertEqual(SerialNumber(bytearray([0x0, 0x0, 0x0, 0xf])).getByteArray(True), bytearray([0xf, 0x0, 0x0, 0x0]))

    def test_getByteArray_ReverseSecondOrder_IsEqual(self):
        self.assertEqual(SerialNumber(16).getByteArray(True), bytearray([0x10, 0x0, 0x0, 0x0]))
        self.assertEqual(SerialNumber("000000016").getByteArray(True), bytearray([0x10, 0x0, 0x0, 0x0]))
        self.assertEqual(SerialNumber(0x10).getByteArray(True), bytearray([0x10, 0x0, 0x0, 0x0]))
        self.assertEqual(SerialNumber("0x10").getByteArray(True), bytearray([0x10, 0x0, 0x0, 0x0]))
        self.assertEqual(SerialNumber("00000010").getByteArray(True), bytearray([0x10, 0x0, 0x0, 0x0]))
        self.assertEqual(SerialNumber(bytearray([0x0, 0x0, 0x0, 0x10])).getByteArray(True), bytearray([0x10, 0x0, 0x0, 0x0]))


    # SerialNumber.__str__


    def test_String_NormalValue_IsEqual(self):
        self.assertEqual(str(SerialNumber(112233445)), "06b08be5")
        self.assertEqual(str(SerialNumber("112233445")), "06b08be5")
        self.assertEqual(str(SerialNumber(0x6b08be5)), "06b08be5")
        self.assertEqual(str(SerialNumber("0x6b08be5")), "06b08be5")
        self.assertEqual(str(SerialNumber("06b08be5")), "06b08be5")
        self.assertEqual(str(SerialNumber(bytearray([0x6, 0xb0, 0x8b, 0xe5]))), "06b08be5")

    def test_String_MinimumValue_IsEqual(self):
        self.assertEqual(str(SerialNumber(0)), "00000000")
        self.assertEqual(str(SerialNumber("000000000")), "00000000")
        self.assertEqual(str(SerialNumber(0x0)), "00000000")
        self.assertEqual(str(SerialNumber("0x0")), "00000000")
        self.assertEqual(str(SerialNumber("00000000")), "00000000")
        self.assertEqual(str(SerialNumber(bytearray([0x0, 0x0, 0x0, 0x0]))), "00000000")

    def test_String_MaximumValue_IsEqual(self):
        self.assertEqual(str(SerialNumber(999999999)), "3b9ac9ff")
        self.assertEqual(str(SerialNumber("999999999")), "3b9ac9ff")
        self.assertEqual(str(SerialNumber(0x3b9ac9ff)), "3b9ac9ff")
        self.assertEqual(str(SerialNumber("0x3b9ac9ff")), "3b9ac9ff")
        self.assertEqual(str(SerialNumber("3b9ac9ff")), "3b9ac9ff")
        self.assertEqual(str(SerialNumber(bytearray([0x3b, 0x9a, 0xc9, 0xff]))), "3b9ac9ff")

    def test_String_FirstOrder_IsEqual(self):
        self.assertEqual(str(SerialNumber(1)), "00000001")
        self.assertEqual(str(SerialNumber("000000001")), "00000001")
        self.assertEqual(str(SerialNumber(0x1)), "00000001")
        self.assertEqual(str(SerialNumber("0x1")), "00000001")
        self.assertEqual(str(SerialNumber("00000001")), "00000001")
        self.assertEqual(str(SerialNumber(bytearray([0x0, 0x0, 0x0, 0x1]))), "00000001")

    def test_String_MaxFirstOrder_IsEqual(self):
        self.assertEqual(str(SerialNumber(15)), "0000000f")
        self.assertEqual(str(SerialNumber("000000015")), "0000000f")
        self.assertEqual(str(SerialNumber(0xf)), "0000000f")
        self.assertEqual(str(SerialNumber("0xf")), "0000000f")
        self.assertEqual(str(SerialNumber("0000000f")), "0000000f")
        self.assertEqual(str(SerialNumber(bytearray([0x0, 0x0, 0x0, 0xf]))), "0000000f")

    def test_String_SecondOrder_IsEqual(self):
        self.assertEqual(str(SerialNumber(16)), "00000010")
        self.assertEqual(str(SerialNumber("000000016")), "00000010")
        self.assertEqual(str(SerialNumber(0x10)), "00000010")
        self.assertEqual(str(SerialNumber("0x10")), "00000010")
        self.assertEqual(str(SerialNumber("00000010")), "00000010")
        self.assertEqual(str(SerialNumber(bytearray([0x0, 0x0, 0x0, 0x10]))), "00000010")




if __name__ == '__main__':
    unittest.main()
