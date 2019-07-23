import re
import os


class EdlSeparator(object):
    pattern = r'[\d]{6} .*[C] +[\d\w:]+ +[\d\w:]+( +[\d\w:]+ +[\d\w:]+)'

    def __init__(self):
        """
        Define base values for the edl separator class...
        """
        self.title = str()
        self.str_data = str()
        self.file_path = str()

        self._edl_main = list()
        self._edl_list = list()

        self._file_prefix = '_edl'

    def _extract_data(self, open_file_path):
        """
        Extract the edl data from the file...
        :param BinaryOI open_file_path:
        :return list:
        """

        for i, line in enumerate(open_file_path):

            if i < 2:
                self.title += line
                continue

            self.str_data += line

            if '*SOURCE FILE:' in line:
                self._edl_list.append(self.str_data)
                self.str_data = str()

        return self._edl_list

    def _split_data(self):
        """
        Split the edl file data into a list
        :return bool:
        """

        with open(self.file_path, 'r') as open_file_path:
            self._extract_data(open_file_path)

        return True

    def _separate_edl_data(self):
        """
        Could be nicer...
        :return:
        """

        _temp_list = list()
        for i, x in enumerate(self._edl_list):
            time_code = re.findall(pattern=self.pattern, string=x)[0]
            for ii, y in enumerate(self._edl_list):
                if i != ii and time_code in y:
                    _temp_list.append(x)
                    break
            else:
                self._edl_main.append(x)

        if self._edl_main:
            data = '\n'.join(self._edl_main)
            self._write_by_list(data, '_main.edl')

        if _temp_list:
            self._write_by_list(_temp_list)

        return True

    def _write_by_list(self, data, name=''):
        """

        :param data:
        :param name:
        :return:
        """
        if isinstance(data, str):
            data = [data]

        for i, data in enumerate(data):
            if not name:
                prefix = '_L{:02d}.edl'.format(i+1)
            else:
                prefix = name

            new_edl_path = self.file_path.replace('.edl', prefix)
            self._write(new_edl_path, data)

        return True

    def _write(self, path, data):
        """
        Create a new directory in the file base directory and addes the new split edl file...
        :param str path:
        :param str data:
        :return bool:
        """
        base_dir, basename = os.path.split(path)
        path = os.path.join(base_dir, self._file_prefix, basename)

        try:
            os.makedirs(os.path.join(base_dir, self._file_prefix))
        except WindowsError:
            pass

        with open(path, 'w') as open_edl_file:
            data = self.title + data
            open_edl_file.write(data)

        return True

    def run(self):
        self._split_data()
        self._separate_edl_data()


if __name__ == '__main__':
    edl_file_path = r'Z:\JOBS\_XFER_FOLDERS\Rob\TB_103_MRWOLF_09.11.18.edl'
    # edl_file_path = r'Z:\JOBS\_XFER_FOLDERS\Rob\LAF_106_002_025_20190201.edl'

    e = EdlSeparator()
    e.file_path = edl_file_path
    e.run()