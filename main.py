import os
import sys
from pathlib import Path
import pyperclip

import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton, QMessageBox, QDesktopWidget
from PyQt5.QtCore import QTime, QCoreApplication, QEventLoop

from faker import Faker
from mimesis import Address, Generic, Person
from mimesis.locales import Locale

from interface import Ui_MainWindow

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.fspath(
    Path(PyQt5.__file__).resolve().parent / "Qt5" / "plugins"
)


def center(self):
    # geometry of the main window
    qr = self.frameGeometry()
    # center point of screen
    cp = QDesktopWidget().availableGeometry().center()
    # move rectangle's center point to screen's center point
    qr.moveCenter(cp)
    # top left of rectangle becomes top left of window centering it
    self.move(qr.topLeft())


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
center(MainWindow)
MainWindow.show()

fake = Faker("ru_RU")
locale = Locale.RU
person = Person(locale)
generic = Generic(locale)
generic_en = Generic(Locale.EN)
ru = Address(locale)


def delay():  # задержка для обновления интерфейса
    die_time = QTime.currentTime().addSecs(1)
    while QTime.currentTime() < die_time:
        QCoreApplication.processEvents(QEventLoop.AllEvents, 100)


class Objects:
    objects = []

    def __init__(self):
        self.genAll()
        ui.buttonGenAll.clicked.connect(self.genAll)

    def genAll(self):
        for object in self.objects:
            object.genByName()

    def getObj(self):
        print('{')
        for object in self.objects:
            print('\t' + object.label.text())
        print('}')


class RowObj(Objects):
    def __init__(self, textbox, label, buttonGen, buttonCopy, generator):
        self.textbox: QtWidgets.QLineEdit = textbox
        self.label: QtWidgets.QLabel = label
        self.buttonGen: QtWidgets.QPushButton = buttonGen
        self.buttonCopy: QtWidgets.QPushButton = buttonCopy
        self.generator = generator
        buttonGen.clicked.connect(self.genByName)
        buttonCopy.clicked.connect(self.copyText)
        super().objects.append(self)

    def copyText(self) -> None:
        pyperclip.copy(self.textbox.text())

    def genByName(self) -> None:
        self.textbox.setText(str(self.generator(globals)))


class Persone:
    Surname: str
    Name: str
    SecName: str

    def fioUpdate(self) -> str:
        self.Surname = fake.last_name()
        ui.Surname.setText(self.Surname)
        self.Name = fake.first_name()
        ui.Name.setText(self.Name)
        self.SecName = fake.middle_name()
        ui.SecName.setText(self.SecName)
        return ui.Surname.text() + ' ' + ui.Name.text() + ' ' + ui.SecName.text()

    def updateSurname(self) -> str:
        tmp = fake.last_name()
        ui.FullName.setText(ui.FullName.text().replace(self.Surname, tmp, 1))
        self.Surname = tmp
        return self.Surname

    def updateName(self) -> str:
        tmp = fake.first_name()
        ui.FullName.setText(ui.FullName.text().replace(self.Name, tmp, 1))
        self.Name = tmp
        return self.Name

    def updateSecName(self) -> str:
        tmp = fake.middle_name()
        ui.FullName.setText(ui.FullName.text().replace(self.SecName, tmp, 1))
        self.SecName = tmp
        return self.SecName


Persone = Persone()

Company = RowObj(ui.Company, ui.labelCompany, ui.buttonGenCompany, ui.buttonCopyCompany, lambda x: fake.company())
WebLink = RowObj(ui.WebLink, ui.labelWebLink, ui.buttonGenWebLink, ui.buttonCopyWebLink, lambda x: fake.uri())
WordEn = RowObj(ui.WordEn, ui.labelWordEn, ui.buttonGenWordEn, ui.buttonCopyWordEn, lambda x: generic_en.text.word())
WordRu = RowObj(ui.WordRu, ui.labelWordRu, ui.buttonGenWordRu, ui.buttonCopyWordRu, lambda x: generic.text.word())
Username = RowObj(ui.Username, ui.labelUsername, ui.buttonGenUsername, ui.buttonCopyUsername, lambda x: generic.person.username())
FullName = RowObj(ui.FullName, ui.labelFullName, ui.buttonGenFullName, ui.buttonCopyFullName, lambda x: Persone.fioUpdate())
Surname = RowObj(ui.Surname, ui.labelSurname, ui.buttonGenSurname, ui.buttonCopySurname, lambda x: Persone.updateSurname())
Name = RowObj(ui.Name, ui.labelName, ui.buttonGenName, ui.buttonCopyName, lambda x: Persone.updateName())
SecName = RowObj(ui.SecName, ui.labelSecName, ui.buttonGenSecName, ui.buttonCopySecName, lambda x: Persone.updateSecName())
Email = RowObj(ui.Email, ui.labelEmail, ui.buttonGenEmail, ui.buttonCopyEmail, lambda x: fake.ascii_free_email())
Phone = RowObj(ui.Phone, ui.labelPhone, ui.buttonGenPhone, ui.buttonCopyPhone, lambda x: fake.phone_number())
Birthday = RowObj(ui.Birthday, ui.labelBirthday, ui.buttonGenBirthday, ui.buttonCopyBirthday, lambda x: generic.datetime.date())
Post = RowObj(ui.Post, ui.labelPost, ui.buttonGenPost,  ui.buttonCopyPost, lambda x: fake.job())
Bool = RowObj(ui.Bool, ui.labelBool, ui.buttonGenBool, ui.buttonCopyBool, lambda x: fake.pybool())
City = RowObj(ui.City, ui.labelCity, ui.buttonGenCity, ui.buttonCopyCity, lambda x: fake.city_name())
Country = RowObj(ui.Country, ui.labelCountry, ui.buttonGenCountry, ui.buttonCopyCountry, lambda x: fake.country())
Postcode = RowObj(ui.Postcode, ui.labelPostcode, ui.buttonGenPostcode, ui.buttonCopyPostcode, lambda x: fake.postcode())
Street = RowObj(ui.Street, ui.labelStreet, ui.buttonGenStreet, ui.buttonCopyStreet, lambda x: fake.street_title())
Ipv4 = RowObj(ui.Ipv4, ui.labelIpv4, ui.buttonGenIpv4, ui.buttonCopyIpv4, lambda x: fake.ipv4())

Object = Objects()

sys.exit(app.exec_())
