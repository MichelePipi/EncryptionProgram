from flask import Flask, render_template, request
from api import sql_handlers


app = Flask(__name__)
ALPHABET = "abcdefghijklmnopqrstuvwxyz"
ALPHA_REGEX_PATTERN = "[a-z]"

# Create table
sql_handlers.create_table()

# Status code constants
OK = 200
BAD_REQ = 400
NOT_FOUND = 404

# Indexes for cipher data
ORIGINAL_TEXT = 1
CIPHER_TEXT = 2
SHIFT_VALUE = 3


def encode(plaintext, shift_value) -> str:
    ans = ""
    # iterate over the given text
    for i, ch in enumerate(plaintext):

        # check if space is there then simply add space
        if ch == " ":
            ans += " "
        # check if a character is uppercase then encrypt it accordingly
        elif ch.isupper():
            ans += chr((ord(ch) + shift_value - 65) % 26 + 65)
        # check if a character is lowercase then encrypt it accordingly
        else:
            ans += chr((ord(ch) + shift_value - 97) % 26 + 97)

    return ans


@app.route("/")
def index(methods=["GET"]):  # put application's code here
    return render_template("form_encrypt.html")


@app.route("/encrypt/", methods=["POST"])
def encrypt():
    # Collect data from form submission
    text_to_encrypt = request.form["text_to_encrypt"]
    shift_value = int(request.form["shift_value"])
    encrypted_text = encode(text_to_encrypt, shift_value)
    insert_id = sql_handlers.insert_entry(
        original=text_to_encrypt, ciphered=encrypted_text, key=shift_value
    )
    return (
        render_template(
            "result.html",
            original=text_to_encrypt,
            ciphered=encrypted_text,
            insert_id=insert_id,
        ),
        OK,
    )


@app.route("/retrieve_from_id/")
@app.route("/retrieve_from_id/<entry_id>")
def retrieve_from_id(entry_id=None):
    try:
        converted_entry_id = int(entry_id)
        data = sql_handlers.locate_entry_from_id(converted_entry_id)

        if data == (None, None):
            return render_template("locate_entry.html", found_entry=False), NOT_FOUND
        original = data[ORIGINAL_TEXT]  # Location in data tuple (original, cipher_text)
        cipher_text = data[CIPHER_TEXT]
        shift_value = data[SHIFT_VALUE]
        return (
            render_template(
                "locate_entry.html",
                original=original,
                cipher_text=cipher_text,
                id=entry_id,
                found_entry=True,
                key=shift_value,
                query=f"SELECT * FROM ciphers WHERE id='{entry_id}'",
            ),
            OK,
        )
    except TypeError:
        return render_template("locate_entry.html"), BAD_REQ
    except ValueError:
        return render_template("locate_entry.html"), BAD_REQ


if __name__ == "__main__":
    app.run(debug=True)
