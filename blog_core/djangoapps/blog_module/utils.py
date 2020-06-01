def getImagePath(model_instance=None):
    if model_instance:
        return "blog/article/image/{}".format(model_instance.title)
    else:
        return "blog/article/image/"


def getUploadPath(model_instance=None):
    if model_instance:
        return "blog/article/file/{}".format(model_instance.title)
    else:
        return "blog/article/file/"


# def iamge_base64():
#     try:
#         image = base64.b64decode(request.data.get("image").split(';base64,')[1])
#     except Exception:
#         return Response(
#             data=response_data,
#             status=status.HTTP_400_BAD_REQUEST
#         )
#
#     s = imghdr.what(None, image)
#     print(s)
#     f = BytesIO().write(image)
#     image = InMemoryUploadedFile(f, "test", 'png', None, len(image), None, None)
