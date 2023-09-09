from flask import Flask, render_template, request

app = Flask(__name__)
alphabet = 'abcdefghijklmnoprstuwxyz'


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


def encode(word: str, key=2) -> str:
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
def cipher_test(text=None):
    if text is None:
        return render_template('encrypt.html')
    return render_template('encrypt.html', text=text, ciphered=encode(text, key=3))


if __name__ == '__main__':
    app.run()
