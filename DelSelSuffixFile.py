import os
import logging 
logging.basicConfig(level=logging.WARNING)

from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QListWidget, QListWidgetItem, QAbstractItemView
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile


class DelSelSuffixFile():
    
    def __init__(self):
        self.path = ''      # 需要操作的文件夹路径
        self.suffixes = []      # 文件夹下所有文件后缀
        logging.info(f'init path length = {len(self.path)}')

        # 从文件中加载UI定义
        qfile_stats = QFile('DelSelSuffixFile.ui')
        qfile_stats.open(QFile.ReadOnly)
        qfile_stats.close()

        # 从UI定义中动态创建一个相应的窗口对象
        self.ui = QUiLoader().load(qfile_stats)

        self.ui.button.clicked.connect(self.getAllSuffixD)
        self.ui.delButton.clicked.connect(self.delSelSuffix)

    # 获取指定文件夹的路径，得到文件夹下所有文件的后缀名 
    def getAllSuffixD(self):
        #获取指定文件夹的路径
        self.path = QFileDialog.getExistingDirectory(self.ui, './', 'C:/Users/ZH/Desktop')
        logging.info(f'SelPath = {self.path}, Path length = {len(self.path)}')

        # 遍历文件夹下的所有文件，提取所有后缀     
        if len(self.path) > 0:
            for _, _, files in os.walk(self.path):
                logging.info(type(files))
                for name in files:
                    logging.info(f'file name = {name}')
                    suffix = os.path.splitext(name)[1]      # 提取文件后缀
                    logging.info(f'file suffix = {suffix}')
                    if suffix not in self.suffixes:
                        self.suffixes.append(suffix)
            logging.info(f'suffixes = {self.suffixes}')

            self.ui.lst.setSelectionMode(QAbstractItemView.MultiSelection)  # 设置之后可以通过鼠标左键多选
            self.ui.lst.addItems(self.suffixes)     #显示所有后缀以供选择
        else:
            pass

    # 删除所选择后缀的文件
    def delSelSuffix(self):
        items = self.ui.lst.selectedItems()
        logging.info(str(self.ui.lst.selectedItems()))
        selSuffixes = [item.text() for item in items]       #所有选中的待删除后缀
        logging.info(selSuffixes)

        # 删除所有选中后缀的文件
        if len(self.path) > 0:
            for root, _, files in os.walk(self.path):
                for name in files:
                    for suffix in selSuffixes:
                        if name.endswith(suffix):
                            os.remove(os.path.join(root, name))
                            print ("Delete File: " + os.path.join(root, name))


if __name__ == '__main__':
    app = QApplication()
    DD = DelSelSuffixFile()
    DD.ui.show()
    app.exec_()