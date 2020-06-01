#!/usr/bin/env python
"""
Usage: manage.py {lms|cms} [--settings env] ...

Run django management commands. Because edx-platform contains multiple django projects,
the first argument specifies which project to run (cms [Studio] or lms [Learning Management System]).

By default, those systems run in with a settings file appropriate for development. However,
by passing the --settings flag, you can specify what environment specific settings file to use.

Any arguments not understood by this manage.py will be passed to django-admin.py
"""

# Patch the xml libs before anything else.
#from safe_lxml import defuse_xml_libs
#defuse_xml_libs()

import os
import sys
import importlib
from argparse import ArgumentParser
#import contracts


def parse_args():
    """Parse edx specific arguments to manage.py"""
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(title='system', description='edX service to run')

    blog_web = subparsers.add_parser(
        'blog-web',
        help='Learning Management System',
        add_help=False,
        usage='%(prog)s [options] ...'
    )
    blog_web.add_argument('-h', '--help', action='store_true', help='show this help message and exit')
    blog_web.add_argument(
        '--settings',
        help="Which django settings module to use under lms.envs. If not provided, the DJANGO_SETTINGS_MODULE "
             "environment variable will be used if it is set, otherwise it will default to lms.envs.dev")
    blog_web.add_argument(
        '--service-variant',
        choices=['lms', 'lms-xml', 'lms-preview'],
        default='lms',
        help='Which service variant to run, when using the aws environment')
    blog_web.add_argument(
        '--contracts',
        action='store_true',
        default=False,
        help='Turn on pycontracts for local development')
    blog_web.set_defaults(
        help_string=blog_web.format_help(),
        settings_base='blog_web/settings',
        default_settings='blog_web.settings.local',
        startup='blog_web.startup',
    )

    # blog-admin run args settings
    blog_admin = subparsers.add_parser(
        "blog-admin",
        help='API message of outer',
        add_help=False,
        usage='%(prog)s [options] ...'
    )
    blog_admin.add_argument('-h', '--help', action='store_true', help='show this help message and exit')
    blog_admin.add_argument(
        '--settings',
        help="Which django settings module to use under lms.envs. If not provided, the DJANGO_SETTINGS_MODULE "
             "environment variable will be used if it is set, otherwise it will default to lms.envs.dev")
    blog_admin.add_argument(
        '--service-variant',
        choices=['lms', 'lms-xml', 'lms-preview'],
        default='blog-admin',
        help='Which service variant to run, when using the aws environment')
    blog_admin.add_argument(
        '--contracts',
        action='store_true',
        default=False,
        help='Turn on pycontracts for local development')
    blog_admin.set_defaults(
        help_string=blog_admin.format_help(),
        settings_base='blog_admin/settings',
        default_settings='blog_admin.settings.local',
        startup='blog_admin.startup',
    )

    edx_args, django_args = parser.parse_known_args()

    if edx_args.help:
        print("edX:")
        print(edx_args.help_string)

    return edx_args, django_args


if __name__ == "__main__":
    edx_args, django_args = parse_args()

    if edx_args.settings:
        os.environ["DJANGO_SETTINGS_MODULE"] = edx_args.settings_base.replace('/', '.') + "." + edx_args.settings
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", edx_args.default_settings)

    os.environ.setdefault("SERVICE_VARIANT", edx_args.service_variant)

    enable_contracts = os.environ.get('ENABLE_CONTRACTS', False)
    # can override with '--contracts' argument
    #if not enable_contracts and not edx_args.contracts:
    #    contracts.disable_all()

    if edx_args.help:
        print("Django:")
        # This will trigger django-admin.py to print out its help
        django_args.append('--help')

    startup = importlib.import_module(edx_args.startup)
    startup.run()

    from django.core.management import execute_from_command_line
    print("""
                                                    │＼＿＿╭╭╭╭╭＿＿／│  
                                                    │　　　　　　　　　　　│　　　  
                                                    │　　　　　　　　　　　│　　　  
                                                    │　●　　　　　　　●　│  
                                                    │≡　　╰┬┬┬╯　　≡│  
                                                    │　　　　╰—╯　　　　│　  
                                                    ╰——┬Ｏ———Ｏ┬——╯ ╭—＾＿＿＾—
       """)
    execute_from_command_line([sys.argv[0]] + django_args)

