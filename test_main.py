import unittest
from unittest.mock import patch
from io import StringIO
import string
from main import get_user_preferences, generate_password, assess_password_strength, main


class TestUserPreferences(unittest.TestCase):

    @patch('builtins.input', side_effect=['12', 'да', 'да', 'да', 'нет'])
    def test_get_user_preferences(self, mock_input):
        length, include_letters, include_digits, include_special, mask_password = get_user_preferences()
        self.assertEqual(length, 12)
        self.assertTrue(include_letters)
        self.assertTrue(include_digits)
        self.assertTrue(include_special)
        self.assertFalse(mask_password)

    def test_generate_password(self):
        length = 12
        password = generate_password(length, True, True, True)
        self.assertEqual(len(password), length)
        self.assertTrue(any(c.isalpha() for c in password))
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertTrue(any(c in string.punctuation for c in password))

    def test_assess_password_strength(self):
        password = 'Aamwx056!/'
        score = assess_password_strength(password)
        self.assertEqual(score, 4)

        password = 'Apq45!'
        score = assess_password_strength(password)
        self.assertEqual(score, 3)

        password = '34!/'
        score = assess_password_strength(password)
        self.assertEqual(score, 2)

        password = '/!.'
        score = assess_password_strength(password)
        self.assertEqual(score, 1)

        password = ''
        score = assess_password_strength(password)
        self.assertEqual(score, 0)

    @patch('builtins.input', side_effect=['12', 'да', 'да', 'да', 'нет', 'да', 'да'])
    def test_main_without_masked_password(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            output = fake_out.getvalue().strip()
            # Мы проверяем, что пароль отображается полностью, а не замаскирован
            self.assertNotIn('Ваш сгенерированный пароль: ************\n', output)
            self.assertIn("Успешно! Пароль сохранен в файл 'password.log'.\n", output)
            self.assertIn('Сложность пароля: Очень сложный (4/4)', output)

    @patch('builtins.input', side_effect=['12', 'да', 'да', 'да', 'да', 'нет', 'да'])
    def test_main_with_masked_password(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            output = fake_out.getvalue().strip()
            output = fake_out.getvalue().strip()
            self.assertIn('Готово! Ваш сгенерированный пароль: ************\n', output)
            self.assertIn('Сложность пароля: Очень сложный (4/4)', output)


if __name__ == "__main__":
    unittest.main()
