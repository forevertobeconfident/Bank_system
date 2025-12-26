import time
import random

# 定义一个欢迎界面类
class WelcomeLoginSystem:
    """欢迎界面类"""
    def __init__(self):
        self.admin_accounts = {"admin": "12345"}   # 使用字典存储账户和密码
        self.welcome_message = "欢迎登录银行管理系统"

# 创建一个自定义用户登录的异常类
class UserLoginError(Exception):
    pass
class Userinfo(WelcomeLoginSystem):
    def display_welcome_screen(self):
        """显示欢迎界面"""
        print("Please wait for refresh...")
        for i in range(11):
            time.sleep(0.2)
            print(f"\r[{'.' * i}{' ' * (10 - i)}]{i * 10}%", end="")
        print("\nRefresh completed！")
        time.sleep(1)
        print('*' * 30)
        print('***                        ***')
        print('***                        ***')
        print(f'***    {self.welcome_message}    ***')
        print('***                        ***')
        print('***                        ***')
        print('*' * 30)


class UserManager:
    """用户凭证验证类"""

    def __init__(self):
        # 在欢迎界面后显示登录信息
        print("请输入管理员账户和密码进行登录")
        self.account = None
        self.password = None
        # self.get_password()
        self.validate_credentials()


    # def get_account(self):
    #     print("请输入管理员账户:")
    #     self.get_account()
    # def get_password(self):
    #         self.password = input("请输入管理员的密码:")
    #         print("密码输入错误！")
    #         self.get_password()    # 获取用户输入的密码

    def validate_credentials(self):
        max_attempts = 3
        attempts = 0

        while attempts < max_attempts:
            try:
                # 获取账户名
                self.account = input("请输入管理员账户:")
                self.password = input("请输入管理员的密码:")

                # 验证账户和密码
                system = WelcomeLoginSystem()
                if self.account in system.admin_accounts and \
                        self.password == system.admin_accounts[self.account]:
                    print("登录成功，请稍后...")
                    return  # 登录成功，退出方法
                else:
                    attempts += 1
                    remaining = max_attempts - attempts
                    if remaining > 0:
                        print(f"管理员账户或密码输入错误！您还有{remaining}次机会")
                    else:
                        print("管理员账户或密码输入错误！")
            except UserLoginError:
                attempts += 1
                remaining = max_attempts - attempts
                if remaining > 0:
                    print(f"输入错误请重新输入！您还有{remaining}次机会")

        print("系统被关闭，程序退出！")
        exit()  # 三次机会用完，退出程序

    def display_menu(self):
        time.sleep(1)
        print('*' * 30)
        print('***                        ***')
        print('***  1.开户（1）  2.查询（2） ***')
        print('***  3.取款（3)） 4.存款（4） ***')
        print('***  5.转账（5）  6.锁定（6） ***')
        print('***  7.解锁（7）             ***')
        print('***                        ***')
        print('*** 退出（Q）                ***')
        print('***                        ***')
        print('*' * 30)


class BankAccountManager:
    """银行账户管理类"""
    # 用于存储所有已生成的卡号
    existing_cards = set()
    # 用于存储账户信息
    accounts = {}
    # 用于存储锁定的卡号
    locked_cards = set()

    def __init__(self, name=None, id_card=None, phone_number=None, balance=0, password=None, card=None):
        """
        初始化银行账户
        name: 用户姓名
        id_card: 身份证号
        phone_number: 手机号
        balance: 余额
        password: 密码
        card: 银行卡号
        """
        if name and id_card and phone_number and password and card:
            self.name = name
            self.id_card = id_card
            self.phone_number = phone_number
            self.balance = balance
            self.password = password
            self.card = card
            # 将账户信息存储到类变量中
            BankAccountManager.accounts[card] = {
                'name': name,
                'id_card': id_card,
                'phone_number': phone_number,
                'balance': balance,
                'password': password
            }

    def show_account_info(self):
        """显示开户信息"""
        time.sleep(1)
        str1 = "开户成功！以下是您的开户信息"
        str2 = str1
        print(f'********{str2}********')
        print(f"用户名：{self.name}")
        print(f"身份证号：{self.id_card}")
        print(f"手机号：{self.phone_number}")
        print(f"余额：{self.balance}")
        print(f"密码：{self.password}")
        print(f"已为您生成了一个6位数的银行卡号：{self.card}")
        print("请牢记并保存好您的开户信息！")
        print('*' * 39)

    @staticmethod
    def generate_unique_card():
        """生成不重复的6位数银行卡号"""
        while True:
            # 生成6位数字，确保是6位数
            card = random.randint(100000, 999999)  # 修正：确保是6位数
            # 检查是否重复
            if card not in BankAccountManager.existing_cards:
                BankAccountManager.existing_cards.add(card)
                return card

    @classmethod
    def create_account(cls):  # cls 代表的是类本身且更灵活  如果类名被修改，这行代码也不会被修改
        """创建新账户"""
        try:
            name = input("请输入用户名:")
            id_card = input("请输入身份证号:")
            phone_number = input("请输入手机号:")
            balance = float(input("请输入预存金额:"))
            password = input("请输入密码:")

            if name and id_card and phone_number and password:
                # 生成唯一的银行卡号
                card = cls.generate_unique_card()
                account = cls(name, id_card, phone_number, balance, password, card)
                account.show_account_info()
                return account
            else:
                print("请输入正确的信息！")
                return None
        except ValueError:
            print("输入格式错误，请仔细确认后再重新输入！")
            return None

    @classmethod
    def query_balance(cls):
        """查询余额功能，允许三次输入机会"""
        max_attempts = 3  # 设置三次机会
        attempts = 0  # 计数从零开始

        while attempts < max_attempts:
            try:
                card_input = int(input("请输入银行卡号:"))
                password_input = input("请输入密码:")

                # 检查卡号是否被锁定
                if card_input in cls.locked_cards:
                    print("该卡号已被锁定，请联系银行工作人员解锁！")
                    return False

                # 检查卡号是否存在
                if card_input not in cls.accounts:
                    print("卡号不存在！")
                    attempts += 1
                    remaining = max_attempts - attempts  # 剩余次数
                    if remaining > 0:
                        print(f"您还有{remaining}次机会")
                    continue

                # 验证密码
                account_info = cls.accounts[card_input]
                if str(password_input) == str(account_info['password']):
                    print('*' * 30)
                    print("查询成功！")
                    print(f"用户名：{account_info['name']}")
                    print(f"卡号：{card_input}")
                    print(f"余额：{account_info['balance']} 元")
                    print('*' * 30)
                    return True
                else:
                    attempts += 1
                    remaining = max_attempts - attempts
                    if remaining > 0:
                        print(f"密码错误！您还有{remaining}次机会")
                    else:
                        print("连续三次输入错误，你的卡号已被锁定！")
                        cls.locked_cards.add(card_input)
                        return False

            except ValueError:
                print("输入格式错误！")
                attempts += 1
                remaining = max_attempts - attempts
                if remaining > 0:
                    print(f"您还有{remaining}次机会")

        if attempts >= max_attempts:
            print("已达到最大尝试次数，操作已终止！")
            return False

    @classmethod
    def withdraw(cls):
        """取款功能"""
        max_attempts = 3
        attempts = 0

        while attempts < max_attempts:
            try:
                card_input = int(input("请输入银行卡号:"))
                password_input = input("请输入密码:")

                # 检查卡号是否被锁定
                if card_input in cls.locked_cards:
                    print("该卡号已被锁定，请联系银行工作人员解锁！")
                    return False

                # 检查卡号是否存在
                if card_input not in cls.accounts:
                    print("卡号不存在！")
                    attempts += 1
                    remaining = max_attempts - attempts
                    if remaining > 0:
                        print(f"您还有{remaining}次机会")
                    continue

                # 验证密码
                account_info = cls.accounts[card_input]
                if str(password_input) == str(account_info['password']):
                    try:
                        amount = float(input("请输入取款金额:"))
                        if amount <= 0:
                            print("取款金额必须大于0！")
                            return False
                        if amount > account_info['balance']:
                            print("余额不足！")
                            print(f"当前余额：{account_info['balance']} 元")
                            return False

                        # 执行取款
                        account_info['balance'] -= amount
                        print('*' * 30)
                        print("取款成功！")
                        print(f"卡号：{card_input}")
                        print(f"取款金额：{amount} 元")
                        print(f"剩余余额：{account_info['balance']} 元")
                        print('*' * 30)
                        return True
                    except ValueError:
                        print("输入金额格式错误！")
                        return False
                else:
                    attempts += 1
                    remaining = max_attempts - attempts
                    if remaining > 0:
                        print(f"密码错误！您还有{remaining}次机会")
                    else:
                        print("连续三次输入错误，你的卡号已被锁定！")
                        cls.locked_cards.add(card_input)
                        return False

            except ValueError:
                print("输入格式错误！")
                attempts += 1
                remaining = max_attempts - attempts
                if remaining > 0:
                    print(f"您还有{remaining}次机会")

        if attempts >= max_attempts:
            print("已达到最大尝试次数，操作已终止！")
            return False

    @classmethod
    def deposit(cls):
        """存款功能"""
        max_attempts = 3
        attempts = 0

        while attempts < max_attempts:
            try:
                card_input = int(input("请输入银行卡号:"))
                password_input = input("请输入密码:")

                # 检查卡号是否被锁定
                if card_input in cls.locked_cards:
                    print("该卡号已被锁定，请联系银行工作人员解锁！")
                    return False

                # 检查卡号是否存在
                if card_input not in cls.accounts:
                    print("卡号不存在！")
                    attempts += 1
                    remaining = max_attempts - attempts
                    if remaining > 0:
                        print(f"您还有{remaining}次机会")
                    continue

                # 验证密码
                account_info = cls.accounts[card_input]
                if str(password_input) == str(account_info['password']):
                    try:
                        amount = float(input("请输入存款金额:"))
                        if amount <= 0:
                            print("存款金额必须大于0！")
                            return False

                        # 执行存款
                        account_info['balance'] += amount
                        print('*' * 30)
                        print("存款成功！")
                        print(f"卡号：{card_input}")
                        print(f"存款金额：{amount} 元")
                        print(f"当前余额：{account_info['balance']} 元")
                        print('*' * 30)
                        return True
                    except ValueError:
                        print("输入金额格式错误！")
                        return False
                else:
                    attempts += 1
                    remaining = max_attempts - attempts
                    if remaining > 0:
                        print(f"密码错误！您还有{remaining}次机会")
                    else:
                        print("连续三次输入错误，你的卡号已被锁定！")
                        cls.locked_cards.add(card_input)
                        return False

            except ValueError:
                print("输入格式错误！")
                attempts += 1
                remaining = max_attempts - attempts
                if remaining > 0:
                    print(f"您还有{remaining}次机会")

        if attempts >= max_attempts:
            print("已达到最大尝试次数，操作已终止！")
            return False

    @classmethod
    def transfer(cls):
        """转账功能"""
        max_attempts = 3
        attempts = 0

        while attempts < max_attempts:
            try:
                sender_card = int(input("请输入转出卡号:"))
                sender_password = input("请输入转出卡密码:")

                # 检查转出卡号是否被锁定
                if sender_card in cls.locked_cards:
                    print("转出卡号已被锁定，请联系银行工作人员解锁！")
                    return False

                # 检查转出卡号是否存在
                if sender_card not in cls.accounts:
                    print("转出卡号不存在！")
                    attempts += 1
                    remaining = max_attempts - attempts
                    if remaining > 0:
                        print(f"您还有{remaining}次机会")
                    continue

                # 验证转出卡密码
                sender_info = cls.accounts[sender_card]
                if str(sender_password) != str(sender_info['password']):
                    attempts += 1
                    remaining = max_attempts - attempts
                    if remaining > 0:
                        print(f"转出卡密码错误！您还有{remaining}次机会")
                    else:
                        print("连续三次输入错误，你的卡号已被锁定！")
                        cls.locked_cards.add(sender_card)
                        return False
                    continue

                # 获取转入卡号
                try:
                    receiver_card = int(input("请输入转入卡号:"))
                    if receiver_card not in cls.accounts:
                        print("转入卡号不存在！")
                        return False

                    if receiver_card in cls.locked_cards:
                        print("转入卡号已被锁定，无法转账！")
                        return False

                    if receiver_card == sender_card:
                        print("不能向自己转账！")
                        return False

                    amount = float(input("请输入转账金额:"))
                    if amount <= 0:
                        print("转账金额必须大于0！")
                        return False

                    if amount > sender_info['balance']:
                        print("余额不足！")
                        print(f"当前余额：{sender_info['balance']} 元")
                        return False

                    # 执行转账
                    sender_info['balance'] -= amount
                    cls.accounts[receiver_card]['balance'] += amount
                    print('*' * 30)
                    print("转账成功！")
                    print(f"转出卡号：{sender_card}")
                    print(f"转入卡号：{receiver_card}")
                    print(f"转账金额：{amount} 元")
                    print(f"转出后余额：{sender_info['balance']} 元")
                    print('*' * 30)
                    return True

                except ValueError:
                    print("输入金额格式错误！")
                    return False

            except ValueError:
                print("输入格式错误！")
                attempts += 1
                remaining = max_attempts - attempts
                if remaining > 0:
                    print(f"您还有{remaining}次机会")

        if attempts >= max_attempts:
            print("已达到最大尝试次数，操作已终止！")
            return False

    @classmethod
    def lock_account(cls):
        """锁定账户功能"""
        max_attempts = 3
        attempts = 0

        while attempts < max_attempts:
            try:
                card_input = int(input("请输入要锁定的银行卡号:"))
                password_input = input("请输入密码:")

                # 检查卡号是否存在
                if card_input not in cls.accounts:
                    print("卡号不存在！")
                    attempts += 1
                    remaining = max_attempts - attempts
                    if remaining > 0:
                        print(f"您还有{remaining}次机会")
                    continue

                # 验证密码
                account_info = cls.accounts[card_input]
                if str(password_input) == str(account_info['password']):
                    if card_input in cls.locked_cards:
                        print("该卡号已被锁定！")
                        return False

                    cls.locked_cards.add(card_input)
                    print('*' * 30)
                    print("账户锁定成功！")
                    print(f"卡号：{card_input}")
                    print('*' * 30)
                    return True
                else:
                    attempts += 1
                    remaining = max_attempts - attempts
                    if remaining > 0:
                        print(f"密码错误！您还有{remaining}次机会")
                    else:
                        print("连续三次输入错误！")
                        return False

            except ValueError:
                print("输入格式错误！")
                attempts += 1
                remaining = max_attempts - attempts
                if remaining > 0:
                    print(f"您还有{remaining}次机会")

        if attempts >= max_attempts:
            print("已达到最大尝试次数，操作已终止！")
            return False

    @classmethod
    def unlock_account(cls):
        """解锁账户功能"""
        max_attempts = 3
        attempts = 0

        while attempts < max_attempts:
            try:
                card_input = int(input("请输入要解锁的银行卡号:"))
                password_input = input("请输入密码:")

                # 检查卡号是否存在
                if card_input not in cls.accounts:
                    print("卡号不存在！")
                    attempts += 1
                    remaining = max_attempts - attempts
                    if remaining > 0:
                        print(f"您还有{remaining}次机会")
                    continue

                # 验证密码
                account_info = cls.accounts[card_input]
                if str(password_input) == str(account_info['password']):
                    if card_input not in cls.locked_cards:
                        print("该卡号未被锁定！")
                        return False

                    cls.locked_cards.remove(card_input)
                    print('*' * 30)
                    print("账户解锁成功！")
                    print(f"卡号：{card_input}")
                    print('*' * 30)
                    return True
                else:
                    attempts += 1
                    remaining = max_attempts - attempts
                    if remaining > 0:
                        print(f"密码错误！您还有{remaining}次机会")
                    else:
                        print("连续三次输入错误！")
                        return False

            except ValueError:
                print("输入格式错误！")
                attempts += 1
                remaining = max_attempts - attempts
                if remaining > 0:
                    print(f"您还有{remaining}次机会")

        if attempts >= max_attempts:
            print("已达到最大尝试次数，操作已终止！")
            return False


def main():
    """主程序入口，处理用户选择"""
    # 显示欢迎界面
    user_info = Userinfo()
    user_info.display_welcome_screen()

    # 验证用户凭证
    user_manager = UserManager()

    # 创建银行账户管理器实例
    bank_manager = BankAccountManager()

    # 首次显示菜单
    user_manager.display_menu()
    menu_displayed = False  # 标记菜单是否已经显示过

    while True:
        if not menu_displayed:
            menu_displayed = True
        choice = input("请输入您的选择:").strip().lower()
        time.sleep(0.3)

        if choice == '1':
            bank_manager.create_account()
        elif choice == '2':
            bank_manager.query_balance()
        elif choice == '3':
            bank_manager.withdraw()
        elif choice == '4':
            bank_manager.deposit()
        elif choice == '5':
            bank_manager.transfer()
        elif choice == '6':
            bank_manager.lock_account()
        elif choice == '7':
            bank_manager.unlock_account()
        elif choice == 'q':
            print("感谢您使用建设银行，欢迎下次使用！")
            break
        else:
            print("无效的选择，请重新输入！")
        # 只在首次操作后显示菜单
        if not menu_displayed:
            user_manager.display_menu()


if __name__ == "__main__":
    main()

