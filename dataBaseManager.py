"""
Модуль общения с базой данных, непосредственно 
направляющий и обрабатывающий запросы к бд

TODO:
  [ ] !!! Написать все запросы
  [+] !!! Разработать и реализовать интерфейс модуля
"""
import sqlite3
from sqlite3 import Error

import dataBaseReqs as dbr
from models import User, Offer, Assessment


database = None  # Используемая база данных
cursor = None    # Объект взаимодействия с database
databaseName = 'truejob_database.db'


"""
DataBaseManager Interface
"""
# Общие функции


def connect():
  """
  Подключиться к базе данных

  return: True, если подключение успешно, False иначе
  """
  global database
  global cursor
  database = sqlite3.connect('truejob_database.db')
  cursor = database.cursor()
  if database is None or cursor is None:
    return False
  return True

def closeConnect():
  """
  Закрыть соединение с базой данных.
  """
  global database
  database.close()

def initNewConnect():
  """
  Инициировать новую бд и подключиться к ней

  return: True, если создание и подключение успешно, False иначе
  """
  result = connect()
  if result:
    cursor.execute(dbr.create_assessments_table)
    cursor.execute(dbr.create_liked_offers_table)
    cursor.execute(dbr.create_offers_table)
    cursor.execute(dbr.create_reports_table)
    cursor.execute(dbr.create_users_table)
    database.commit()
    return True
  return False


# Функции связанные с User
def addUser(user: User):
  """
  Добавить пользователя в бд

  return: True добавление пользователя с новым vkid успешно, иначе False 
  """
  with sqlite3.connect(databaseName) as db:
    cursor = db.cursor()
    cursor.execute("SELECT vkid FROM users WHERE vkid = (?)", (user.vkid, ))
    if cursor.fetchone() is None:
      cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)",
                    (user.vkid, user.type, user.employer_rating,
                      user.worker_rating, user.status, user.is_blocked))
      db.commit()
      return True
    return False


def updateUser(user: User):
  """
  Обновить существующего пользователя в бд

  return: True пользователь есть в бд и успешно обновлен, иначе False 
  """
  with sqlite3.connect(databaseName) as db:
    cursor = db.cursor()
    cursor.execute("SELECT vkid FROM users WHERE vkid = (?)", (user.vkid, ))
    if cursor.fetchone() is not None:
      cursor.execute("UPDATE users SET \
          vkid = (?), \
          type = (?), \
          employer_rating = (?), \
          worker_rating = (?), \
          status = (?), \
          is_blocked = (?) \
          WHERE vkid = (?)",
          (user.vkid, user.type, user.employer_rating,
          user.worker_rating, user.status, user.is_blocked,
          user.vkid))
      db.commit()
      return True
    return False


def getUser(vkid: str):
  """
  Получить пользователя по vkid

  return:  User с id == vkid, иначе None
  """
  with sqlite3.connect(databaseName) as db:
    cursor = db.cursor()
    user = None

    cursor.execute("SELECT * FROM users WHERE vkid = (?)", (vkid, ))
    row = cursor.fetchone()
    if row is not None:
      """
      cursor.description возвращает имена столбцов из последнего запроса.
      он возвращает кортеж из 7 значений, где последние 6 = None.
      на нулевой позиции лежит название столбца, поэтому его и используем для
      формирования словаря.
      """
      rowDict = dict(zip([column[0] for column in cursor.description], row))
      print("User", rowDict)
      user = User(**rowDict)
    return user


def deleteUser(vkid: str):
  """
  Удалить пользователя из бд

  return: True, если успешно, иначе False
  """
  with sqlite3.connect(databaseName) as db:
    cursor = db.cursor()
    cursor.execute("SELECT vkid FROM users WHERE vkid = (?)", (vkid, ))
    if cursor.fetchone() is not None:
      cursor.execute("DELETE FROM users WHERE vkid = (?)", (vkid, ))
      database.commit()
      return True
    return False


# Функции связанные с Offer
def addOffer(offer: Offer):
  """
  Добавить объявление в бд

  return: True добавление успешно, иначе False 
  """

  return False


def updateOffer(offer: Offer):
  """
  Обновить существующее объявление в бд

  return: True пользователь есть в бд и успешно обновлен, иначе False 
  """

  return False


def getOffer(id: int):
  """
  Получить объявление по id

  return:  User с id == vkid, иначе None
  """

  return None


def deleteOffer(id: int):
  """
  Удалить объявление из бд

  return: True, если успешно, иначе False
  """

  return False


def getOffersByUser(vkid: str):
  """
  Получить объявления опубликованные пользователм с vkid

  return: [Offer, ...] если такие есть, иначе None
  """
  req = "SELECT * FROM Offers WHERE owner=vkid"

  return None


def getLikedOffersByUser(vkid: str):
  """
  Получить лайкнутые пользователем с vkid объявления 
  """

  req = "SELECT Offers.* FROM LikedOffers, Offers \
          WHERE LikedOffers.user = vkid \
          AND LikedOffers.offer_id = Offers.offer_id"

  return [None]


def getAllOffers():
  """
  Получить все объявления

  return: [Offer, ...] Все объявления, если есть, иначе None
  """

  return [None]


# Функции связанные с Like & Report & Assessment
def addOfferLike(vkid: str, offer_id: int):
  """
  Добвить запись о лайке в таблицу TABLE-3 LikedOffers

  return: True, если добавление успешно, иначе False
  """

  return False


def deleteOfferLike(vkid: str, offer_id: int):
  """
  Удалить запись о лайке в таблицу TABLE-3 LikedOffers

  return: True, если запись была и успешно удалена, иначе False
  """

  return False


def addReport(vkid: str, reported_vkid: str):
  """
  Добавить запись о репорте в таблицу TABLE-5 Reports

  return: True, если добавление успешно, иначе False
  """

  return False


def addAssessment(assessment: Assessment):
  """
  Добавить запись об оценке в таблицу TABLE-4 Assessments

  return: True, если добавление успешно, иначе False
  """
  with sqlite3.connect(databaseName) as db:
    cursor.execute("SELECT user, assessed_user FROM assessments \
        WHERE user = (?) AND assessed_user = (?)", (assessment.user, assessment.assessed_user))
    if cursor.fetchone() is None:
      cursor.execute("INSERT INTO assessments VALUES (?, ?, ?, ?)",
          (assessment.user, assessment.assessed_user,
           assessment.assessment_as_worker, assessment.assessment_as_employer))
      db.commit()
      return True
  return False


def getAssessment(vkid: str, assessed_vkid: str):
  """
  Получить существующую оценку

  return: Assesment, если такая оценка есть, иначе None
  """
  with sqlite3.connect(databaseName) as db:
    cursor.execute("SELECT * FROM assessments \
        WHERE user = (?) AND assessed_user = (?)",
        (vkid, assessed_vkid))
    row = cursor.fetchone()
    if row is not None:
      """
      cursor.description возвращает имена столбцов из последнего запроса.
      он возвращает кортеж из 7 значений, где последние 6 = None.
      на нулевой позиции лежит название столбца, поэтому его и используем для
      формирования словаря.
      """
      rowDict = dict(zip([column[0] for column in cursor.description], row))
      assessment = Assessment(**rowDict)
      return assessment
  return None


def updateAsssessment(assessment: Assessment):
  """
  Обновить запись об оценке, если такая есть

  return: True, если такая есть и обновление успешно, иначе False
  """
  with sqlite3.connect(databaseName) as db:
    cursor.execute("SELECT user, assessed_user FROM assessments \
        WHERE user = (?) AND assessed_user = (?)",
        (assessment.user, assessment.assessed_user))
    if cursor.fetchone() is not None:
      cursor.execute("UPDATE assessments SET \
          user = (?), assessed_user = (?), \
          assessment_as_worker = (?), assessment_as_employer = (?) \
          WHERE user = (?) AND assessed_user = (?)",
          (assessment.user, assessment.assessed_user,
           assessment.assessment_as_worker, assessment.assessment_as_employer,
           assessment.user, assessment.assessed_user))
          db.commit()
          return True
  return False


def getAllAssessments(assessed_vkid: str):
  """
  Получить все оценки оцененного пользователя

  return: [Assessment, ...] все оценки, если есть, иначе None
  """
  with sqlite3.connect(databaseName) as db:
    cursor.execute("SELECT * FROM assessments \
        WHERE assessed_user = (?)",
        (assessed_vkid, ))
    if cursor.fetchall() is not None:
      list_of_assessment = [list(assessment) for assessment in cursor.fetchall()]
      return list_of_assessment
  return None

# def printResult():
#   cursor = database.cursor()
#   for value in cursor.execute(f"SELECT * FROM users"):
#     print(value)


# if __name__ == "__main__":
#   user_dict_1 = {"vkid": "kdator", "type": "user", "employer_rating": 5.0, 
#             "worker_rating": 4.5, "status": "regular", "is_blocked": 0}
#   user_dict_2 = {"vkid": "kdator", "type": "admin", "employer_rating": 3.3, 
#             "worker_rating": 2.2, "status": "super", "is_blocked": 1}
#   user_dict_3 = {"vkid": "_kr.alex_", "type": "admin", "employer_rating": 5.0,
#             "worker_rating": 5.0, "status": "Gold", "is_blocked": 0}
#   first_user = User(user_dict_1)
#   second_user = User(user_dict_2)
#   third_user = User(user_dict_3)
#   initNewConnect()
#   addUser(first_user)
#   addUser(third_user)
#   printResult()
#   print("------------------------")
#   updateUser(second_user)
#   printResult()
#   deleteUser("kdator")
#   print("------------------------")
#   printResult()
#   closeConnect()
