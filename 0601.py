import random


class User:
    """
    man : True
    woman : False
    """
    def __init__(self, id=None, gender=None, prev_users=None, now_users=None):
        self.id = id
        self.gender = gender
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
        self.men_count = 0
        self.women_count = 0

    def add(self, men=None, women=None):
        genders = [True] * men + [False] * women
        for gender in genders:
            user = User(id=len(self.users), gender=gender)
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
            tmp_users = sorted(new_face_users, key=lambda x: len(x.now_users))[:quota]
            cls.__receive_users(user, tmp_users)
        users.sort(key=lambda x:x.id)

    def is_validation(self):
        """
        1. 내가 받은 카드를 상대도 받아야 됨
        2. 이전카드, 현재카드에 동성이 있으면 안됨
        3. 예전에 소개 받았던 이성이 현재 받으면 안됨
        """


g = Generator()
g.add(men=20, women=10)
for _ in range(3):
    Allocation.delivery(g.get_users(), 2)
for user in g.get_users():
    print(user)





