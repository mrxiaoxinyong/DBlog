# # # import re
# # # live_id = "live-v1:12143124aaa"
# # # RESOURCES_VERSION = "v1"
# # # RESOURCES_SIGN = "-"
# # # RESOURCES_TYPE = r"\w+{sign}{version}"
# # # RESOURCES_PATTERN = RESOURCES_TYPE.format(sign=RESOURCES_SIGN,
# # #                                           version=RESOURCES_VERSION)
# # # RESOURCES_ID = r"\d+"
# # # MATCH_LIVE = re.compile("""
# # #     (?P<resource_type>{resources_type}):
# # #     (?P<resource_id>{resources_id})$
# # # """.format(resources_type=RESOURCES_PATTERN, resources_id=RESOURCES_ID), re.VERBOSE)
# # # print("""
# # #     (?P<resource_type>{resources_type}):
# # #     (?P<resource_id>{resources_id})
# # # """.format(
# # #     resources_type=RESOURCES_TYPE, resources_id=RESOURCES_ID), re.VERBOSE)
# # # print(MATCH_LIVE.match(live_id).groupdict())
# #
# #
# # USERNAME = "Bob"
# # EMAIL = "bob@example.com"
# # PASSWORD = "edx"
# #
# # OTHER_USERNAME = "Jane"
# # OTHER_EMAIL = "jane@example.com"
# #
# # ENABLED_CACHES = ['default', 'mongo_metadata_inheritance', 'loc_cache']
# #
# # API_KEY = "PUT_YOUR_API_KEY_HERE"
# #
# # course_id = "exam-v1:1234"
# #
# # enrollment_attributes = {
# #     "Number": "aaa"
# # }
# # mode = "honor"
# # is_active = True
# # email_opt_in = None
# # expected_status = 200
# # username = "84112000"
# #
# # data = {
# #     'mode': mode,
# #     'resource_details': {
# #         'resource_id': course_id
# #     },
# #     'user': username,
# #     'enrollment_attributes': enrollment_attributes
# # }
# #
# # if is_active is not None:
# #     data['is_active'] = is_active
# #
# # if email_opt_in is not None:
# #     data['email_opt_in'] = email_opt_in
# #
# # extra = {}
# # as_server = True
# # if as_server:
# #     extra["X-EDX-API-KEY"] = API_KEY
# #
# # url = "https://elearningx.test.huawei.com/api/enrollment/v2/enrollment"
# #
# # import requests
# # res = requests.post(url, json=data, headers=extra)
# # print(res.text)
# # print(res.status_code)
# #
# #
# #
# #
# # user_uuid_hex = "72fa163e6b3920"
# # sql = """SELECT a.username,b.name,b.uuid FROM auth_user as a JOIN auth_userprofile as b ON (a.id=b.user_id and b.user_id in (SELECT user_id from auth_userprofile WHERE substr(uuid,19,32)='{user_uuid_hex}'))""".format(user_uuid_hex=user_uuid_hex)
# # print(sql)
# # print(len("831b2a5cade311e9b77"))
# # print("831b2a5cade311e9b772fa163e6b3920"[18:])
# # print(len("831b2a5cade311e9b772fa163e6b3920"[19:]))
# #
# # for i in range(1, 2):
# #     print(i)
# def a():
#    print("aaaaaaaaaa")
#    return True
#
# def b():
#    print("bbbbbbbbbbb")
#    return False
#
# def c():
#    print("ccccccccccc")
#    return False
#
# def is_live_p():
#     print("livevvvvvvvvvvv")
#     return False
#
# def is_play_p():
#     print("playbackkkkkkkk")
#     return False
#
# if a() and (
#         (is_play_p() and b()) or
#         (is_live_p() and c())
# ):
#     print("====================")
#
# def senstive_filter(message, keyword_chains):
#     start = 0
#     delimit = '\x00'
#     replace_message = ""
#     is_senstive = False
#     #message = message.strip().replace('\t', '').replace('\n', '').replace('\r','')
#     while start < len(message):
#         level = keyword_chains
#         step_ins = 0
#         step_str = ""
#         level_str = ""
#         for char in message[start:]:
#             level_str += char
#             if char in level:
#                 step_ins += 1
#                 step_str += "*"
#                 if delimit not in level[char]:
#                     level = level[char]
#                 else:
#                     replace_message += step_str
#                     start += step_ins - 1
#                     is_senstive = True
#                     break
#             else:
#                 start += step_ins
#                 replace_message += level_str
#                 break
#         start += 1
#     return replace_message, is_senstive
#
#
# class SB:
#
#     def __init__(self):
#         self.a = {"a": "c"}
# sb = SB()
# c = sb.a
# c["a"] = "fffffffffffff"
# print(c)
# print(sb.a)

print(any(_social=="a" for _social in ["a", "b"]))
