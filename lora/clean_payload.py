class CleanPayload:
    def __init__(self, _data):
        self._data = _data

    def clean_data(self):
        """
        cleans the payload data removes '\n' from the string
        :param self: 'AAB296C4E5094228BA0000EC0000009A2D64\r'
        :return: string
        """
        d = self._data
        dl = len(self._data)
        if dl % 2 == 1 and (d[dl - 1] == '\r' or d[dl - 1] == '\n'):
            d = d[0:dl - 1]
            return d
        elif d[dl - 2:dl] == '\r\n':
            d = d[0:dl - 2]
            return d
        else:
            return d
