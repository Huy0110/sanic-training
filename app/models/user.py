import time


class User:
    def __init__(self, _id=''):
        self._id = _id
        self.username = ''
        self.password = ''
        self.created_at = int(time.time())
        self.last_updated_at = int(time.time())

    def to_dict(self):
        return {
            '_id': self._id,
            'username': self.username,
            'password': self.password,
            'createdAt': self.created_at,
            'lastUpdatedAt': self.last_updated_at
        }

    def from_dict(self, json_dict: dict):
        self._id = json_dict.get('_id', self._id)
        self.username = json_dict.get('username', '')
        self.password = json_dict.get('password', '')
        self.created_at = json_dict.get('createdAt', int(time.time()))
        self.last_updated_at = json_dict.get('lastUpdatedAt', int(time.time()))
        return self


create_user_json_schema = {
    'type': 'object',
    'properties': {
        'username': {'type': 'string'},
        'password': {'type': 'string'},
    },
    'required': ['username', 'password']
}
