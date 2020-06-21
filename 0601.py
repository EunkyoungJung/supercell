import random


"""
4,  

1. 남자가 동갑이거나 여자보다 최대 6살 가
2. 1번 조건은 필수가 아니며, 없으면 나이 상관없는 사람을 할당
3. 유효성체크에 추

"""

class User:
    """
    man : True
    woman : False
    """

    def __init__(self, id=None, gender=None, age=None, prev_users=None, now_users=None):
        self.id = id
        self.gender = gender
        self.age = age
        self.prev_users = prev_users if prev_users else list()
        self.now_users = now_users if now_users else list()

    def reset_now(self):
        self.now_users = list()

    def receive(self, others):
        others_ids = [other.id for other in others]
        self.prev_users += others_ids
        self.now_users += others_ids

    def __str__(self):
        return f"{self.__dict__}"


class Generator:
    def __init__(self):
        self.users = list()

    def add(self, man_count=None, woman_count=None, man_age=None, woman_age=None):
        genders = [True] * man_count + [False] * woman_count
        for gender in genders:
            age = random.randrange(*man_age) if gender else random.randrange(*woman_age)
            user = User(id=len(self.users), gender=gender, age=age)
            self.users.append(user)

    def get_users(self):
        return self.users


class Allocation:
    @classmethod
    def __prepare_users(cls, users):
        for user in users:
            user.reset_now()

    @classmethod
    def __receive_users(cls, user, opposite_users):
        for opposite_user in opposite_users:
            opposite_user.receive([user])
        user.receive(opposite_users)

    @classmethod
    def __shuffle(cls, users):
        random.shuffle(users)

    @classmethod
    def delivery(cls, users, quota):
        cls.__shuffle(users)
        cls.__prepare_users(users)
        for user in users:
            opposite_genders = list(filter(lambda x: x.gender != user.gender, users))
            new_face_users = list(filter(lambda x: x.id not in user.prev_users and user.id not in x.prev_users, opposite_genders))
            if user.gender:
                tmp_users = sorted(new_face_users, key=lambda woman: (not bool(0 <= user.age - woman.age < 6), len(woman.now_users)))[:quota]
            else:
                tmp_users = sorted(new_face_users, key=lambda man: (not bool(0 <= man.age - user.age < 6), len(man.now_users)))[:quota]
            cls.__receive_users(user, tmp_users)
        users.sort(key=lambda x: x.id)

    @classmethod
    def is_validate(cls, users):
        gender_error_cnt = 0
        match_error_cnt = 0
        duplicate_match_error_cnt = 0
        for user in users:
            gender_error_cnt += len(list(filter(lambda x: x.id in user.prev_users and x.gender == user.gender, users)))
            match_error_cnt += len(list(filter(lambda x: x.id in user.prev_users and user.id not in x.prev_users, users)))
            duplicate_match_error_cnt += len(user.prev_users) - len(set(user.prev_users))
        print(f"gender_error_cnt={gender_error_cnt} match_error_cnt={match_error_cnt} duplicate_match_error_cnt={duplicate_match_error_cnt}")



g = Generator()
g.add(man_count=100, woman_count=100, man_age=(20, 60), woman_age=(20, 60))
for _ in range(3):
    Allocation.delivery(g.get_users(), 2)
Allocation.is_validate(g.get_users())
for user in g.get_users():
    print(user)
# g = Generator()
# g.add(men=20, women=10)
# for _ in range(3):
#     Allocation.delivery(g.get_users(), 2)
# for user in g.get_users():
#     print(user)





