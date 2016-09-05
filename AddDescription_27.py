##  \file       Agregator.cpp
#   \brief      Defines the entry point for the console application.
#   \author     Skident
#   \date       05.09.2016
#   \copyright  JSC "Bancomzvjazok"

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, time
import datetime


class GetFileList:
    def get_all_files(self, path, mask, skipped_folders):
        file_list = []
        # traverse dir
        for root, dirs, files in os.walk(path):
            # print(root)

            skip = False
            for skipped_dir in skipped_folders:
                if root.lower().find(skipped_dir) != -1:
                    skip = True
                    break

            if skip:
                continue

            for name in files:
                if False == name.endswith(mask):
                    continue

                fullpath = os.path.join(root, name)
                # print(fullpath)
                file_list.append(fullpath.replace("\\", "/"))

        return file_list


class ProgressBar:
    prev_progress = 0
    progress = 0
    step = 0

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


    def show(self):
        if self.progress - self.prev_progress >= 5:
            print("[" + "{0:.0f}".format(self.progress) + "%]")
            self.prev_progress = self.progress

        return self.prev_progress

    def reset(self):
        self.progress = 0
        self.prev_progress = 0


class HeaderCreator:
    template_header = """
/*!
 *  \\file       {filename}
 *  \\brief      Brief description.
 *  \\author     {author}
 *  \\date       {date}
 *  \\copyright  {copyright}
 */
"""

    header_anchor = "/*! \\file"

    def __add_header(self, filename, encode, line):
        with open(filename, 'r+', encoding=encode) as f:
            content = f.read()
            f.seek(0, 0)
            f.write(line.lstrip('\r\n') + '\n' + content)

    def is_header_exist(self, filename):
        encode = 'cp1251'
        f = open(filename, 'r', encoding=encode)

        # skip empty lines
        f.seek(0)
        line = ""
        while True:
            if line != "":
                break

            try:
                line = f.readline().strip()
            except:
                f.close()
                encode = 'utf-8'
                f = open(filename, 'r', encoding=encode)
                try:
                    line = f.readline().strip()
                except:
                    line = ""
                    break

        f.close()

        # another header not found
        if line == "" or line.find(self.header_anchor) == -1:
            return (False, encode)
        return (True, encode)


    def add_header(self, path, mask, skipped_dirs, author, copyright):
        file_list = GetFileList()
        files = file_list.get_all_files(path, mask, skipped_dirs)

        progressBar = ProgressBar(len(files))

        for file in files:
            (exists, encode) = self.is_header_exist(file)

            # insert new header if it doesn't exist
            if not exists:
                create_date = datetime.datetime.strptime(time.ctime(os.path.getctime(file)), "%a %b %d %H:%M:%S %Y")

                copy_header = self.template_header
                copy_header = copy_header.replace("{author}", author)
                copy_header = copy_header.replace("{date}", create_date.strftime("%d.%m.%Y"))
                copy_header = copy_header.replace("{filename}", file[file.rfind("/")+1:])
                copy_header = copy_header.replace("{copyright}", copyright)

                self.__add_header(file, encode, copy_header)

            progressBar.next_step()
            progress = progressBar.show()


# main function
def main():
    path = os.getcwd().replace("\\", "/")
    mask = (".c", ".cpp", ".h", ".hpp")
    skipped_dirs = ["boost", "poco", "pocolib", ".svn", ".metadata", "obj", "Bin", "Ant", "debug", "release", "doxygen"]

    header_creator = HeaderCreator()

    print("Start to add headers")
    header_creator.add_header(path, mask, skipped_dirs, "Skident", "JSC \"Bancomzvjazok\"")
    print("Process have finished")

main()
