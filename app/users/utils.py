import secrets, os
from PIL import Image
from flask import url_for, current_app
from app import mail
from flask_mail import Message

def update_image(form_picture):
    random_hex = secrets.token_hex(8)
    _ ,f_ext = os.path.splitext(form_picture.filename)
    new_file_name = random_hex + f_ext
    new_file_path = os.path.join(current_app.root_path, 'static/profile_pics', new_file_name)
    output_size = (125, 125)

    '''
    ADD CROP FUNCUNALITY INSTEAD OF THUMBNAILS
    '''
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(new_file_path)

    return new_file_name

def sendResetEmail(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='reset.password@example.com', recipients=[user.email])
    msg.body = f'''To Reset your Password, visit this link: {url_for('users.reset_token', token=token, _external=True)}'''
    mail.send(msg)