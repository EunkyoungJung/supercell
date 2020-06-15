import random


class User:
    """
    개별 회원
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
    """
    회원 기록부
    """
    def __init__(self):
        self.users = list()
        self.men_count = 0
        self.women_count = 0

    def add(self, men=None, women=None):
        """
        회원 전체 등록
        """
        genders = [True] * men + [False] * women
        for gender in genders:
            user = User(id=len(self.users), gender=gender)
            self.users.append(user)

    def get_users(self):
        return self.users


class Allocation:
    """
    매칭 프로세스
    """
    @classmethod
    def __prepare_users(cls, users):
        for user in users:
            user.reset_now()

    @classmethod
    def __receive_users(cls, user, opposite_users):
        for opposite_user in opposite_users:
            opposite_user.receive([user]) # 상대방의 매칭기록에 user를 추가
        user.receive(opposite_users) # user의 매칭기록에 opposite_users를 추가

    @classmethod
    def __shuffle(cls, users):
        random.shuffle(users) # users 리스트의 user들의 위치를 shuffle

    @classmethod
    def delivery(cls, users, quota):
        cls.__shuffle(users)   # 균등하게 기회를 갖을 수 있도록 shuffle
        cls.__prepare_users(users)  # 각 user의 now_users정보 초기화
        for user in users:
            opposite_genders = list(filter(lambda x: x.gender != user.gender, users))
            new_face_users = list(filter(lambda x: x.id not in user.prev_users and user.id not in x.prev_users, opposite_genders))
            tmp_users = sorted(new_face_users, key=lambda x: len(x.now_users))[:quota]
            cls.__receive_users(user, tmp_users)
        users.sort(key=lambda x: x.id)

    @classmethod
    def is_validate(self):
        """
        1. 내가 받은 카드를 상대도 받아야 됨
        2. 이전카드, 현재카드에 동성이 있으면 안됨
        3. 예전에 소개 받았던 이성이 현재 받으면 안됨
        """
        g = Generator()
        g.add(men=20, women=10)
        Allocation.delivery(g.get_users(), 2)
        for user in g.get_users():
            for now_user in user.now_users:
                if user not in now_user.now_users:
                    return False
        print("Pass Case #1: 내가 받은 카드를 상대도 받아야 됨")

        Allocation.__prepare_users(g.get_users())



Allocation.is_validate()
# g = Generator()
# g.add(men=20, women=10)
# for _ in range(3):
#     Allocation.delivery(g.get_users(), 2)
# for user in g.get_users():
#     print(user)





