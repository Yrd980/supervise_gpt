import os

from api import *


def test():
    rule = "在本市申请《⽹络预约出租汽⻋驾驶员证》的驾驶员，应当符合下列条件：取得本市核发的相应准驾⻋型机动⻋驾驶证并具有3年以上驾驶经历；"
    result = identify_rules(rule)
    # print(type(result))
    print(result['data'])


def test1():
    rule = "⽹约⻋平台条件）在本市申请从事⽹约⻋经营服务的，应当具备线上线下服务能⼒。具体条件除符合《⽹络预约出租汽⻋经营服务管理暂⾏办法》（以下简称《办法》）的规定外，还应当符合下列规定：（⼀）⾮本市注册的企业法⼈应当在本市设⽴分⽀机构；（⼆）⽹络服务平台数据接⼊市交通⾏政管理部⻔的⾏业监管平台；（三）在本市有与注册⻋辆数和驾驶员⼈数相适应的办公场所、服务⽹点和管理⼈员；（四）投保承运⼈责任险。"
    result = split_atomic_rules(rule)
    for item in result['ruleList']:
        print(item['atom_rule'])


def test2():
    file_path = r"D:\实验报告\大二下\实验室\04现代物流服务业\New folder\New folder\New folder\New Text Document.txt"

    try:
        if os.path.exists(file_path):

            os.chmod(file_path, 0o666)
            print("File permissions modified successfully!")
        else:
            print("File not found:", file_path)
    except PermissionError:
        print("Permission denied: You don't have the necessary permissions to change the permissions of this file.")

    with open(file_path, "w") as file:
        new_content = "New content to replace the existing content."
        file.write(new_content)

    print("File content modified successfully!")


if __name__ == '__main__':
    test2()
