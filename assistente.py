import speech_recognition as sr
from nltk import word_tokenize, corpus
import json

IDIOMA_PADRAO = "portuguese"
IDIOMA_AUDIO = "pt-BR"
ARQUIVO_CONFIGURACAO = "./config.json"


def ler_arquivo_configuracao():
    try:
        with open(ARQUIVO_CONFIGURACAO, "r", encoding="utf-8") as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print("Configuração não encontrada!")
        return None
    except json.JSONDecodeError:
        print("Erro ao interpretar o arquivo de configuração!")
        return None


def inicializar_assistente():
    global capturador_audio, palavras_ignoradas, funcoes_dispositivos

    capturador_audio = sr.Recognizer()
    capturador_audio.dynamic_energy_threshold = True
    capturador_audio.energy_threshold = 4000

    palavras_ignoradas = set(corpus.stopwords.words(IDIOMA_PADRAO))

    
    configuracao = ler_arquivo_configuracao()
    if configuracao:
        funcoes_dispositivos = {
            dispositivo["nome"]: dispositivo["funcoes"]
            for dispositivo in configuracao["acoes"]
        }
    else:
        funcoes_dispositivos = {}

    
    return True, capturador_audio, funcoes_dispositivos



def captar_audio(reconhecedor):
    with sr.Microphone() as microfone:
        print("\n***************************************************")
        print("Capturando comando... Por favor, fale!")
        try:
            reconhecedor.adjust_for_ambient_noise(microfone, duration=1)
            audio = reconhecedor.listen(microfone, timeout=5, phrase_time_limit=5)
            print("Áudio capturado!")
            return True, audio
        except (sr.UnknownValueError, sr.WaitTimeoutError):
            print("Nenhuma entrada detectada.")
            return False, None


def interpretar_audio(audio, reconhecedor):
    try:
        texto = reconhecedor.recognize_google(audio, language=IDIOMA_AUDIO)
        print(f"Comando capturado: {texto}")
        return True, texto.lower()
    except sr.UnknownValueError:
        print("Não entendi o comando. Por favor, tente novamente.")
        return False, None


def filtrar_comando(texto):
    palavras = word_tokenize(texto)
    palavras_filtradas = [palavra for palavra in palavras if palavra not in palavras_ignoradas]
    
    return palavras_filtradas


def identificar_acao(palavras):
    for dispositivo, comandos in funcoes_dispositivos.items():
        if dispositivo in palavras:
            for comando, mensagem in comandos.items():
                if comando in palavras:
                    return True, dispositivo, comando, mensagem
    return False, None, None, None


def processar_acao(dispositivo, comando, mensagem):
    print(f"Executando ação: {dispositivo} - {comando}")
    print(mensagem)


if __name__ == "__main__":
    ativo, capturador_audio, funcoes_dispositivos = inicializar_assistente()
    
    print("\nAssistente de Escritório Ativado!")
    print("")
    print("Lista de comandos suportados:")
    for dispositivo, comandos in funcoes_dispositivos.items():
        print(f"- {dispositivo}: {', '.join(comandos.keys())}")
    
    while True:
        sucesso_audio, audio = captar_audio(capturador_audio)
        if sucesso_audio:
            sucesso_texto, texto = interpretar_audio(audio, capturador_audio)
            if sucesso_texto:
                palavras_processadas = filtrar_comando(texto)
                valido, dispositivo, comando, mensagem = identificar_acao(palavras_processadas)
                
                if valido:
                    processar_acao(dispositivo, comando, mensagem)
                else:
                    print("Comando não identificado. Por favor, tente novamente.")
