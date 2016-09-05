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
                file_list.append(fullpath.replace("\\", "/"))

        return file_list

class ProgressBar:
    def __init__(self, count):
        if count > 0:
            self.step = 100 / count
        else:
            self.step = 100
        self.progress = 0

    def next_step(self):
        if self.progress < 100:
            self.progress += self.step

        if self.progress > 100:
            self.progress = 100

        return self.progress

    def reset(self):
        self.progress = 0

class HeaderCreator:

    template_header = """
/*! \\file       {filename}
 *  \\brief      Brief description.
 *  \\author     {author}
 *  \\date       {date}
 *  \\copyright  {copyright}
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

        progressBar = ProgressBar(len(files))

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

            progress = progressBar.next_step()
            print("[" + str(progress) + "%]")

def main():
    path = os.getcwd().replace("\\", "/")
    mask = (".c", ".cpp", ".h", ".hpp")

    header_creator = HeaderCreator()

    print("Start to add headers")
    header_creator.add_header(path, mask, "Skident", "Skident inc.")
    print("Process have finished")

main()