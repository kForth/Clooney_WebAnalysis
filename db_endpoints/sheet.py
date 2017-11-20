from flask import jsonify, make_response, request

from models import ScoutingSheetConfig


class SheetDatabaseEndpoints:
    def __init__(self, db_interactor, add_route):
        self._db_interactor = db_interactor

        add_route('/get/sheet/<int:id>', self.get_sheet)
        add_route('/get/sheets', self.get_sheets)
        add_route('/get/default_fields', self.get_default_fields)
        add_route('/save/sheet', self.save_sheet, methods=('POST',))

    def get_sheet(self, id):
        sheet = self._db_interactor.get_sheet_by_id(id)
        if sheet:
            return make_response(jsonify(sheet.to_dict()), 200)
        else:
            return make_response(jsonify(), 404)

    def get_sheets(self):
        return make_response(jsonify([s.to_dict() for s in self._db_interactor.get_sheets()]), 200)

    def get_default_fields(self):
        return make_response(jsonify(self._db_interactor.default_fields), 200)

    def save_sheet(self):
        sheet = request.json
        if 'id' not in sheet.keys():
            sheet['id'] = self._db_interactor.get_next_sheet_id()
        sheet = ScoutingSheetConfig.from_json(request.json)
        if sheet:
            self._db_interactor.set_sheet(sheet)
            return make_response(jsonify(), 200)
        return make_response(jsonify(), 400)
