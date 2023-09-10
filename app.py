from flask import Flask, render_template
from api import sql_handlers


app = Flask(__name__)
ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALPHA_REGEX_PATTERN = '[a-z]'

# Create table
sql_handlers.create_table()

# Status code constants
OK = 200
BAD_REQ = 400
NOT_FOUND = 404


@app.route('/')
def hello_world(methods=['GET']):  # put application's code here
    return render_template('index.html')


def encode(word, key) -> str:
    if word is None or key is None:
        return ''
    if key == 0:
        return word

    result = ''
    for character in word:  # for each character
        if character not in ALPHABET:  # if the character is special
            result += character  # add the plain character
        else:
            number_for_letter = ALPHABET.index(character)  # get the number for the letter
            cipher_index = number_for_letter - 26 + key
            cipher_character = ALPHABET[cipher_index]
            result += cipher_character  # get the encoded letter
    return result  # give the result back


@app.route('/encrypt/')
@app.route('/encrypt/<text>')
@app.route('/encrypt/<text>/<key>')
def cipher_test(text=None, key=None, methods=['GET', 'POST']):
    if not text.isalpha(): # Text is not alphabetical
        return render_template('encrypt.html'), BAD_REQ
    try:
        cipher_text = encode(text, int(key))
        insert_id = sql_handlers.insert_entry(original=text, ciphered=cipher_text, key=key)
        return render_template('encrypt.html', text=text, ciphered=cipher_text, insert_id=insert_id), OK
    except ValueError:
        return render_template('encrypt.html'), BAD_REQ
    except TypeError:
        return render_template('encrypt.html'), BAD_REQ


@app.route('/retrieve_from_id/<id>')
def retrieve_from_id(entry_id=None):
    try:
        data = sql_handlers.locate_entry_from_id(int(entry_id))
        if data is None:
            return render_template('locate_entry.html', found_entry=False), NOT_FOUND
        return render_template('locate_entry.html', original=data[0], cipher_text=data[1], id=entry_id), OK
    except TypeError:
        return render_template('locate_entry.html'), BAD_REQ


if __name__ == '__main__':
    app.run(debug=True, port=5001)
