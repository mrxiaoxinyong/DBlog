from django import template
from django.conf import settings
import re, os
from django.utils.safestring import mark_safe

register = template.Library()


def get_structure_data(request):
    """处理菜单结构"""
    menu = request.session[settings.SESSION_MENU_KEY]
    all_menu = menu[settings.ALL_MENU_KEY]
    permission_url = menu[settings.PERMISSION_MENU_KEY]

    # 定制数据结构
    all_menu_dict = {}
    for item in all_menu:
        item['status'] = False
        item['open'] = False
        item['children'] = []
        all_menu_dict[item['id']] = item

    request_rul = request.path_info

    for url in permission_url:
        # 添加两个状态：显示 和 展开
        url['status'] = True
        pattern = url['url']
        if re.match(pattern, request_rul):
            url['open'] = True
        else:
            url['open'] = False

        # 将url添加到菜单下
        all_menu_dict[url['menu_id']]["children"].append(url)

        # 显示菜单：url 的菜单及上层菜单 status: true
        pid = url['menu_id']
        while pid:
            all_menu_dict[pid]['status'] = True
            pid = all_menu_dict[pid]['parent_id']

        # 展开url上层菜单：url['open'] = True, 其菜单及其父菜单open = True
        if url['open']:
            ppid = url['menu_id']
            while ppid:
                all_menu_dict[ppid]['open'] = True
                ppid = all_menu_dict[ppid]['parent_id']

    # 整理菜单层级结构：没有parent_id 的为根菜单， 并将有parent_id 的菜单项加入其父项的chidren内
    menu_data = []
    for i in all_menu_dict:
        if all_menu_dict[i]['parent_id']:
            pid = all_menu_dict[i]['parent_id']
            parent_menu = all_menu_dict[pid]
            parent_menu['children'].append(all_menu_dict[i])
        else:
            menu_data.append(all_menu_dict[i])

    return menu_data


def get_menu_html(menu_data):
    """显示：菜单 + [子菜单] + 权限(url)"""
    option_str = """
         <li class='submenu'>
             <a href="javascript:;">
                 <span class="label radius-circle bg-danger float-right">{menu_icon}</span>
                 <i class="fa fa-fw fa-copy"></i>
                 <span>{menu_title}</span>
                 <span class="menu-arrow"></span>
             </a>

             <ul class="list-unstyled" style="display: block;">{sub_menu}</ul>

         </li>
    """

    url_str = """

        <li>
            <a href="javascript:;" href-url="{permission_url}" class="{active}"> 
                <i class="layui-icon">{permission_icon}</i> 
                {permission_title}
            </a>
        </li>

    """

    menu_html = ''

    for item in menu_data:
        if not item['status']:  # 如果用户权限不在某个菜单下，即item['status']=False, 不显示
            continue
        else:
            if item.get('url'):  # 说明循环到了菜单最里层的url
                menu_html += url_str.format(permission_url=item['url'],
                                            active="rbac-active" if item['open'] else "",
                                            permission_icon=item['icon'],
                                            permission_title=item['title'])
            else:
                if item.get('children'):
                    sub_menu = get_menu_html(item['children'])
                else:
                    sub_menu = ""

                menu_html += option_str.format(menu_icon=item['icon'],
                                               menu_title=item['title'],
                                               sub_menu=sub_menu,
                                               display="" if item['open'] else "rbac-hide",
                                               status="open" if item['open'] else "close")

    return menu_html


@register.simple_tag
def rbac_menu(request):
    """
    显示多级菜单：请求过来 -- 拿到session中的菜单，权限数据 -- 处理数据 -- 作显示
    返回多级菜单：数据处理部分抽象出来由单独的函数处理；渲染部分也抽象出来由单独函数处理
    :param request:
    :return:
    """
    print(request)
    print("-----------------")
    menu_data = get_structure_data(request)
    menu_html = get_menu_html(menu_data)

    return mark_safe(menu_html)
    # 因为标签无法使用safe过滤器，这里用mark_safe函数来实现