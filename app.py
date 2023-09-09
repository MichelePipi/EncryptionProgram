from flask import Flask, render_template
from api import sql_handlers

app = Flask(__name__)
connection = sql_handlers.create_connection()
alphabet = 'abcdefghijklmnopqrstuvwxyz'

# Status code constants
OK = 200
BAD_REQ = 400


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


def encode(word, key) -> str:
    if word is None or key is None:
        return ''
    if key == 0:
        return word

    result = ''
    for character in word:  # for each character
        if character not in alphabet:  # if the character is special
            result += character  # add the plain character
        else:
            number_for_letter = alphabet.index(character)  # get the number for the letter
            cipher_index = number_for_letter - 26 + key
            cipher_character = alphabet[cipher_index]
            result += cipher_character  # get the encoded letter
    return result  # give the result back


@app.route('/encrypt/')
@app.route('/encrypt/<text>')
@app.route('/encrypt/<text>/<key>')
def cipher_test(text=None, key=None):
    print(key)
    if text is None or key is None:
        return render_template('encrypt.html'), BAD_REQ
    return render_template('encrypt.html', text=text, ciphered=encode(text, key=int(key))), OK


if __name__ == '__main__':
    app.run(debug=True, port=5001)
