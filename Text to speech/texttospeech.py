from gTTS import gTTS
import os


text = "Hello guys, how are you? All fine?"


language = "en"


speech = gTTS(text=text, lang=language, slow=False)


speech.save("hello.mp3")

os.system("start hello.mp3")
