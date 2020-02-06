from googletrans import Translator

translator = Translator()
#print(googletrans.LANGUAGES)

result = translator.translate("Kya hua" ,dest='en' , src = 'auto')
result2 = translator.translate("What happened" ,dest='hi' , src = 'en')
print(result2.text)


    