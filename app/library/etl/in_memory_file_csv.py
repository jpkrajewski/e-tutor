from app.models import Student


class InMemoryFileCSVHandler:
    """
    Handler for csv files. Must have mapped fields in first row of a file
    """

    def __init__(self, csv_file, model_in_csv, uploader_model, msg_fail=None, msg_success=None) -> None:
        self._csv = csv_file
        self._model = model_in_csv
        self._uploader = uploader_model
        self._log = []
        self._data = None
        self._msg_fail = '{} not loaded to data base.' if not msg_fail else msg_fail
        self._msg_success = '{} loaded to data base.' if not msg_success else msg_success

    @property
    def log(self):
        return self._log

    def etl(self):
        self._extract()
        self._clean()
        self._transform()
        self._filter()
        self._load()

    def _extract(self):
        self._data = [line.decode('utf-8').split(',') for line in self._csv.readlines()]

    def _clean(self):
        cleaned = []
        for row in self._data:
            cleaned.append(list(map(lambda x: x.strip(), row)) + [row[-1].replace('\r\n', '').rstrip()])
        self._data = cleaned

    def _transform(self):
        clean_data = []
        fields = self._data[0]
        for values in self._data[1:]:
            clean_data.append(self._map_values_to_fields(fields, values))
        self._data = clean_data

    def _map_values_to_fields(self, fields: list, values: list) -> dict:
        return {x[0]: x[1] for x in zip(fields, values)}

    def _filter(self):
        filtered = []
        for mapped_obj in self._data:
            if self._filter_func(mapped_obj):
                self._log.append({'status': 'fail', 'msg': self._msg_fail.format(self._model(**mapped_obj))})
                continue
            filtered.append(mapped_obj)
        self._data = filtered

    def _filter_func(self, mapped_obj):
        return False

    def _load(self):
        for mapped_obj in self._data:
            if self._uploader:
                mapped_obj[self._uploader._meta.model_name] = self._uploader
            added_obj = self._model.objects.create(**mapped_obj)
            self._log.append({'status': 'success', 'msg': self._msg_success.format(self._model(**mapped_obj))})
    
    

class InMemoryStudentCSVHandler(InMemoryFileCSVHandler):
    def _filter_func(self, student):
        for arg in ['facebook_profile','discord_nick', 'email', 'phone_number']:
            if self._model.objects.filter(**{arg:student[arg]}).exclude(**{arg:''}).exists():
                return True
        return False

