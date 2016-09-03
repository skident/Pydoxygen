import os, time
import datetime

class GetFileList:
    def get_all_files(self, path, mask):
        file_list = []
        # traverse dir
        for root, dirs, files in os.walk(path):
            for name in files:
                if False == name.endswith(mask):
                    continue


                fullpath = os.path.join(root, name)
                # print(fullpath)
                file_list.append(fullpath)

        return file_list


class HeaderCreator:

    template_header = """
/*! \\file       {filename}
 *  \\brief      Brief description.
 *              Brief description continued.
 *
 *  Detailed description starts here.
 *
 *  \\author     {author}
 *  \\date       {date}
 *  \\copyright  Skident Inc.
 */
"""

    header_anchor = "/*! \\file"

    def __add_header(self, filename, line):
        with open(filename, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(line.lstrip('\r\n') + '\n' + content)

    def add_header(self, path, mask, author, copyright):
        file_list = GetFileList()
        files = file_list.get_all_files(path, mask)

        for file in files:
            f = open(file, 'r')

            # skip empty lines
            f.seek(0)
            line = f.readline().strip()

            while line == "":
                line = f.readline().strip()
            f.close()

            # insert new header
            if line.find(self.header_anchor) == -1:
                create_date = datetime.datetime.strptime(time.ctime(os.path.getctime(file)), "%a %b %d %H:%M:%S %Y")

                copy_header = self.template_header
                copy_header = copy_header.replace("{author}", author)
                copy_header = copy_header.replace("{date}", create_date.strftime("%d.%m.%Y"))
                copy_header = copy_header.replace("{filename}", file[file.rfind("/")+1:])
                copy_header = copy_header.replace("{copyright}", copyright)

                self.__add_header(file, copy_header)


def main():
    path = "/Users/skident/Documents/Projects/C++/CppHelpers/"
    mask = (".c", ".cpp", ".h", ".hpp")

    header_creator = HeaderCreator()
    header_creator.add_header(path, mask, "Skident", "Skident Inc.")

main()