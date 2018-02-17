class User:
    def __init__(self, username, password, first_name, last_name, id, role="Guest", role_index=0, permissions=[]):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.id = id
        self.role = role
        self.role_index = role_index
        self.permissions = permissions

    def to_dict(self):
        return {
            'username':     self.username,
            'password':     self.password,
            'first_name':   self.first_name,
            'last_name':    self.last_name,
            'id':           self.id,
            'role':         self.role,
            'role_index':   self.role_index,
            'permissions':  self.permissions
        }

    def to_dict_no_pwd(self):
        return {
            'username':     self.username,
            'first_name':   self.first_name,
            'last_name':    self.last_name,
            'id':           self.id,
            'role':         self.role,
            'role_index':   self.role_index,
            'permissions':  self.permissions
        }

    @staticmethod
    def verify_json(data):
        req_keys = ['username', 'password', 'first_name', 'last_name', 'id']
        opt_keys = ['role', 'role_index', 'permissions']
        return all([k in data.keys() for k in req_keys]) and all([k in opt_keys or k in req_keys for k in data.keys()])

    @staticmethod
    def from_json(data):
        return User(**data) if User.verify_json(data) else None


class UserSettings:
    def __init__(self, headers={}):
        self.headers = headers

    def to_dict(self):
        return {
            'headers': self.headers
        }

    @staticmethod
    def verify_json(data):
        req_keys = []
        opt_keys = ['headers']
        return all([k in data.keys() for k in req_keys]) and all([k in opt_keys or k in req_keys for k in data.keys()])

    @staticmethod
    def from_json(data):
        return UserSettings(**data) if UserSettings.verify_json(data) else None


class ScoutingEntry:
    def __init__(self, id, event, data, filename=""):
        self.id = id
        self.event = event
        self.data = data
        self.filename = filename

    def to_dict(self):
        return {
            'id':       self.id,
            'event':    self.event,
            'data':     self.data,
            'filename': self.filename
        }

    @staticmethod
    def verify_json(data):
        req_keys = ['id', 'event', 'data']
        opt_keys = ['filename']
        return all([k in data.keys() for k in req_keys]) and all([k in opt_keys or k in req_keys for k in data.keys()])

    @staticmethod
    def from_json(data):
        return ScoutingEntry(**data) if ScoutingEntry.verify_json(data) else None


class ScoutingSheetConfig:
    def __init__(self, id, name, data, date_created="", date_modified="", scan_data=[]):
        self.id = id
        self.name = name
        self.data = data
        self.date_created = date_created
        self.date_modified = date_modified
        self.scan_data = scan_data

    def to_dict(self):
        return {
            'id':            self.id,
            'name':          self.name,
            'data':          self.data,
            'date_created':  self.date_created,
            'date_modified': self.date_modified,
            'scan_data':     self.scan_data
        }

    @staticmethod
    def verify_json(data):
        req_keys = ['id', 'name', 'data']
        opt_keys = ['date_created', 'date_modified', 'scan_data']
        return all([k in data.keys() for k in req_keys]) and all([k in opt_keys or k in req_keys for k in data.keys()])

    @staticmethod
    def from_json(data):
        return ScoutingSheetConfig(**data) if ScoutingSheetConfig.verify_json(data) else None


class Event:
    def __init__(self, key, info, teams=[], matches=[]):
        self.key = key
        self.info = info
        self.teams = teams
        self.matches = matches

    def to_dict(self):
        return {
            'key':     self.key,
            'info':    self.info.to_dict(),
            'teams':   self.teams,
            'matches': self.matches
        }

    @staticmethod
    def verify_json(data):
        if 'info' in data.keys() and type(data['info']) == EventInfo:
            data = dict(data)
            data['info'] = data['info'].to_dict()
        req_keys = ['key', 'info']
        opt_keys = ['teams', 'matches']
        return all([k in data.keys() for k in req_keys]) and all([k in opt_keys or k in req_keys for k in data.keys()])

    @staticmethod
    def from_json(data):
        if Event.verify_json(data):
            data = dict(data)
            data['info'] = EventInfo.from_json(data['info']) if EventInfo.verify_json(data['info']) else None
            if data['info']:
                return Event(**data)
        return None


class EventInfo:
    def __init__(self, is_tba, data):
        self.is_tba = is_tba
        self.data = data

    def to_dict(self):
        return {
            'is_tba': self.is_tba,
            'data':   self.data
        }

    @staticmethod
    def verify_json(data):
        req_keys = ['is_tba', 'data']
        opt_keys = []
        return all([k in data.keys() for k in req_keys]) and all([k in opt_keys or k in req_keys for k in data.keys()])

    @staticmethod
    def from_json(data):
        return EventInfo(**data) if EventInfo.verify_json(data) else None


class HeaderGroup:
    def __init__(self, name, creator_id, path, data, id):
        self.name = name
        self.creator_id = creator_id
        self.path = path
        self.data = data
        self.id = id

    def to_dict(self):
        return {
            'name': self.name,
            'creator_id': self.creator_id,
            'path': self.path,
            'data': self.data,
            'id': self.id
        }

    @staticmethod
    def verify_json(data):
        req_keys = ['name', 'creator_id', 'path', 'data', 'id']
        opt_keys = []
        return all([k in data.keys() for k in req_keys]) and all([k in opt_keys or k in req_keys for k in data.keys()])

    @staticmethod
    def from_json(data):
        return HeaderGroup(**data) if HeaderGroup.verify_json(data) else None
