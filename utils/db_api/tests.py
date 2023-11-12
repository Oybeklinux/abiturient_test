from utils.db_api.sqlite import Database, Test, TestItem

db = Database("temp")


def test_test():
    question = TestItem(text='Kubning ostki asosidagi tomonlarining o‘rtalari ketma - ket tutashtirildi. Hosil bo‘lgan to‘rtburchakning uchlari kub ustki asosining markazi bilan tutashtirildi. Agar kubning qirrasi a ga teng bo‘lsa, hosil bo‘lgan piramidaning to‘la sirtini toping.')
    answer1 = TestItem(image='https://telegra.ph/file/5ba3115f9c88bdc9c23c0.png')
    answer2 = TestItem(image='https://telegra.ph/file/1fa04cbc207bd1e4021d1.png')
    answer3 = TestItem(image='https://telegra.ph/file/1fa04cbc207bd1e4021d1.png')
    answer4 = TestItem(image='https://telegra.ph/file/b4af0d186948c734dd09d.png')

    test = Test(question, answer1=answer1, answer2=answer2, answer3=answer3,
                answer4=answer4)
    db.insert_test(test)


def test():
    db.create_table_users()
    db.delete_all()
    users = db.select_all_users()
    print(f"Boshlang'ich holat: {users}")
    db.add_user(1, "Otabek", "otabek@gmail.com")
    db.add_user(2, "Bekzod", "bekzod@gmail.com")
    db.add_user(3, "Sherzod", "sherzod@gmail.com")
    db.add_user(4, "Anvar", "anvar@gmail.com")

    users = db.select_all_users()
    print(f"Keyingi holat: {users}")

    user = db.select_user(id=2)
    print(f"Tanlangan user: {user}")

test_test()
