from table_loader import _GET, _LOAD, _TOLIST, _GET_ALL, _GET_ALL_VALUES, _ADD

#Constants
CSVFILE = "conf/csv/users.csv"
CSVFILE_PRETEST = "conf/csv/users-pretest.csv"
KEY_ID = "id"
KEY_SETUP = "setup"
KEY_POSITION = "position"

class Users:
    # LOAD USERS DATASET
    def __init__(self,pretest=False):
        self.pretest = pretest
        if self.pretest:
            self.table = _LOAD(CSVFILE_PRETEST)
        else:
            self.table = _LOAD(CSVFILE)

    # Return all users id
    def get_users_id_list(self):
        return self.table[KEY_ID].tolist()

    def get_setup(self, id):
        return _GET(self.table,id, KEY_SETUP, keyId=KEY_ID)

    def get_position(self, id):
        return _GET(self.table,id, KEY_POSITION, keyId=KEY_ID)

    #
    def print_user_info(self,id):
        print()
        print("User ID: %d" % int(id))
        print("\tPosition ID : %d" % self.get_position(id))
        print("\tSetup ID : %d" % self.get_setup(id))

    def print_all_users_info(self):
        for id in self.get_users_id_list():
            self.print_user_info(id)
