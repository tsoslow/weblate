# -*- coding: utf-8 -*-
#
# Copyright © 2012 - 2019 Michal Čihař <michal@cihar.com>
#
# This file is part of Weblate <https://weblate.org/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.http.request import HttpRequest
from weblate.lang.models import Language
from weblate.trans.models import Component


class Command(BaseCommand):
    """
    Command for mass automatic translation.
    """
    help = 'adds a language to a project component'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--source',
            default='',
            help=(
                'Source component <project/component>'
            )
        )
        parser.add_argument(
            '--language',
            default='',
            help=(
                'Language to add'
            )
        )

    def handle(self, *args, **options):

        if options['source']:
            parts = options['source'].split('/')
            if len(parts) != 2:
                raise CommandError('Invalid source component specified!')
            try:
                component = Component.objects.get(
                    project__slug=parts[0],
                    slug=parts[1],
                )
            except Component.DoesNotExist:
                raise CommandError('No matching source component found!')
        else:
            raise CommandError('Source not passed!')

        if options['language']:
            try:
                language = Language.objects.get(code=options['language'])
            except:
                raise CommandError('Language not found!')
        else:
            raise CommandError('Language not passed!')

        component.add_new_language(language, None)
