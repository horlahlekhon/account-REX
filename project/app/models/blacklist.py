from .. import database
import datetime


class BlackListToken(database.Model):
    """
    BlackListToken class for maanging tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    token = database.Column(database.String(500), unique=True, nullable=False)
    blacklisted_on = database.Column(database.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        """
        check_blacklist check if a token has been blacklisted

        Arguments:
            auth_token {string} -- the jwt auth token to be checked

        Returns:
            Boolean -- a boolean that indicates if it is blacklisted or not
        """
        res = BlackListToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False
