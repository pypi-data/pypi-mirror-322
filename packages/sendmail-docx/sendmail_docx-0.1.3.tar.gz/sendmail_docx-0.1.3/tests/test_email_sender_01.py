"""
Para ejecutar el ejemplo:
python -m unittest tests.test_email_sender_01
"""


import unittest
from sendmail-docx import enviar_correo_electronico
import os

class TestEnviarCorreoElectronico(unittest.TestCase):
    def test_enviar_correo_electronico(self):
        # Enviar un mail de prueba
        resultado = enviar_correo_electronico(
            template_path=os.path.join("tests", "templates", "plantilla-ejemplo.docx"),
            datos={"nombre": "John Doe", "saldo": "1.235,50 €"},
            asunto="Comunicación de saldo",
            destinatarios=["jmsanchez.ibiza@gmail.com"],
            cc=None,
            cco=None,
            adjuntos=['README.md', 'LICENSE']
        )

        print(f"TEST_EMAIL_SENDER_01.PY: {resultado=}")
        self.assertEqual(resultado['status'], 'success')  # Cambié de 1 a 'success'
        self.assertEqual(resultado['message'], 'Correo enviado con éxito.')  # Cambié de [] a 'Correo enviado con éxito.'


if __name__ == '__main__':
    unittest.main()
