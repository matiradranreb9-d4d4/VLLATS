class Config:
    SECRET_KEY = 'secret-key'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://flaskuser:flaskpassword@localhost/virtual_lab_logbook'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
