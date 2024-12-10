import unittest
from assistente import *

class TestAssistenteVirtual(unittest.TestCase):
    def setUp(self):
        self.ativo, self.capturador_audio, self.funcoes_dispositivos = inicializar_assistente()
        self.assertTrue(self.ativo)
        self.reconhecedor = self.capturador_audio
        self.acoes = self.funcoes_dispositivos

    def processar_audio_arquivo(self, caminho_audio, reconhecedor):
        try:
            with sr.AudioFile(caminho_audio) as fonte_de_audio:
                print(f"\nProcessando o arquivo de áudio: {caminho_audio}")
                audio = reconhecedor.record(fonte_de_audio)
                return interpretar_audio(audio, reconhecedor)
        except FileNotFoundError:
            print(f"Arquivo de áudio não encontrado: {caminho_audio}")
            return False, None
        except Exception as e:
            print(f"Erro ao processar o arquivo de áudio: {e}")
            return False, None

    def test_ligar_projetor(self):
        caminho_audio = r".\\audios\\ligar projetor.wav"
        tem_transcricao, transcricao = self.processar_audio_arquivo(caminho_audio, self.reconhecedor)
        
        self.assertTrue(tem_transcricao)
        self.assertIsNotNone(transcricao)
        
        valido, dispositivo, funcao, mensagem = identificar_acao(filtrar_comando(transcricao))
        
        self.assertTrue(valido)
        self.assertEqual(dispositivo, "projetor")
        self.assertEqual(funcao, "ligar")
        print(f"Comando detectado no áudio: {dispositivo}, {funcao}, {mensagem}")

    def test_desligar_projetor(self):
        caminho_audio = r".\\audios\\desligar projetor.wav"
        tem_transcricao, transcricao = self.processar_audio_arquivo(caminho_audio, self.reconhecedor)
        
        self.assertTrue(tem_transcricao)
        self.assertIsNotNone(transcricao)
        
        valido, dispositivo, funcao, mensagem = identificar_acao(filtrar_comando(transcricao))
        
        self.assertTrue(valido)
        self.assertEqual(dispositivo, "projetor")
        self.assertEqual(funcao, "desligar")
        print(f"Comando detectado no áudio: {dispositivo}, {funcao}, {mensagem}")
        
    def test_ativar_impressora(self):
        caminho_audio = r".\\audios\\ativar_impressora.wav"
        tem_transcricao, transcricao = self.processar_audio_arquivo(caminho_audio, self.reconhecedor)
        
        self.assertTrue(tem_transcricao)
        self.assertIsNotNone(transcricao)
        
        valido, dispositivo, funcao, mensagem = identificar_acao(filtrar_comando(transcricao))
        
        self.assertTrue(valido)
        self.assertEqual(dispositivo, "impressora")
        self.assertEqual(funcao, "ativar")
        print(f"Comando detectado no áudio: {dispositivo}, {funcao}, {mensagem}")
        
    def test_desativar_impressora(self):
        caminho_audio = r"audios\desativar_impressora.wav"
        tem_transcricao, transcricao = self.processar_audio_arquivo(caminho_audio, self.reconhecedor)
        
        self.assertTrue(tem_transcricao)
        self.assertIsNotNone(transcricao)
        
        valido, dispositivo, funcao, mensagem = identificar_acao(filtrar_comando(transcricao))
        
        self.assertTrue(valido)
        self.assertEqual(dispositivo, "impressora")
        self.assertEqual(funcao, "desativar")
        print(f"Comando detectado no áudio: {dispositivo}, {funcao}, {mensagem}")
        
    def test_exibir_agenda(self):
        caminho_audio = r".\\audios\\exibir agenda.wav"
        tem_transcricao, transcricao = self.processar_audio_arquivo(caminho_audio, self.reconhecedor)
        
        self.assertTrue(tem_transcricao)
        self.assertIsNotNone(transcricao)
        
        valido, dispositivo, funcao, mensagem = identificar_acao(filtrar_comando(transcricao))
        
        self.assertTrue(valido)
        self.assertEqual(dispositivo, "agenda")
        self.assertEqual(funcao, "exibir")
        print(f"Comando detectado no áudio: {dispositivo}, {funcao}, {mensagem}")
        
    def test_ajustar_temperatura(self):
        caminho_audio = r"C:\Users\Fernanda\Downloads\assistente_virtual_escritorio\audios\ajustar temperatura.wav"
        tem_transcricao, transcricao = self.processar_audio_arquivo(caminho_audio, self.reconhecedor)
        
        self.assertTrue(tem_transcricao)
        self.assertIsNotNone(transcricao)
        
        valido, dispositivo, funcao, mensagem = identificar_acao(filtrar_comando(transcricao))
        
        self.assertTrue(valido)
        self.assertEqual(dispositivo, "temperatura")
        self.assertEqual(funcao, "ajustar")
        print(f"Comando detectado no áudio: {dispositivo}, {funcao}, {mensagem}")

if __name__ == '__main__':
    unittest.main()

