"""
1. csv 파일 저장하기
2. csv 파일 읽어오기
3. 현재 내용 콘솔 출력
4. 연락처 설계

회원정보:
이름/휴대폰번호/집주소/등록일/
"""

import datetime
import csv


def writeCSV(database):
    try:
        CSV_PATH = './hw01/data_new.csv'
        with open(CSV_PATH, 'w', newline='') as datafile:
            fieldnames = ['id','name','phone_number','address','created_at','is_member']
            writer = csv.DictWriter(datafile, fieldnames=fieldnames)
            writer.writeheader()
            for i in database:
                writer.writerow(
                    {
                        'id': i.id,
                        'name': i.name,
                        'phone_number': i.phone_number,
                        'address': i.address,
                        'created_at': i.created_at if i.created_at else datetime.date.today(),
                        'is_member': i.is_member
                    }
                )

    finally:
        datafile.close()


def getCSV(database):
    try:
        CSV_PATH = './hw01/data.csv'
        with open(CSV_PATH) as datafile:
            reader = csv.DictReader(datafile)
            for row in reader:
                member = Member(
                    row['id'].strip(),
                    row['name'].strip(),
                    row['phone_number'].strip(),
                    row['address'].strip(),
                    row['created_at'].strip() if row['created_at'].strip() else datetime.date.today(),
                    True if row['is_member'].strip() == '1' else False
                )
                database.append(member)

    finally:
        datafile.close()


def showDatabase(database):
    for i in database:
        print(i.id, i.name, i.phone_number, i.address, i.created_at, i.is_member)


member_database = []


class Member:
    def __init__(self, id, name, phone_number, address, created_at, is_member=True):
        self.id = id
        self.name = name
        self.phone_number = phone_number
        self.address = address
        self.created_at = created_at
        self.is_member = is_member


getCSV(member_database)
writeCSV(member_database)
showDatabase(member_database)


