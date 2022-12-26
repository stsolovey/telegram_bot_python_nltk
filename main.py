import os
import random
import telebot
import nltk

nltk.data.path.append('/function/code/nltk_data')
bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))


# ---------------- dialog params ----------------
dialog = {
    'hello': {
        'in': ['/hello'],
        'out': ['Привет!']
    }
}


# --------------------- bot ---------------------
@bot.message_handler(commands=['help', 'start'])
def say_welcome(message):
    bot.send_message(message.chat.id,
                     'Я возвращаю грамматическую маску предложения.',
                     parse_mode='markdown')


@bot.message_handler(func=lambda message: True)
def echo(message):
    for t, resp in dialog.items():
        if sum([e in message.text.lower() for e in resp['in']]):
            bot.send_message(message.chat.id, random.choice(resp['out']))
            return
    
    tokenized = nltk.tokenize.word_tokenize(message.text)
    tagged = nltk.pos_tag(tokenized)
    result = " ".join([i[1] for i in tagged])
    
    bot.send_message(message.chat.id, result) 


# ---------------- local testing ----------------
if __name__ == '__main__':
    bot.infinity_polling()
