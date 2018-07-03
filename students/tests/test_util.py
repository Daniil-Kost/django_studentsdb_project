# -*- coding: utf-8 -*-

from django.test import TestCase
from ..models import Group
from django.http import HttpRequest
from ..util import get_groups, get_current_group


class UtilsTestCase(TestCase):
    """Test funcions from util module"""

    def setUp(self):
        # create set of users and groups in database
        group1, created = Group.objects.get_or_create(
            id=1, title='Group1')

    def test_get_current_group(self):
        # prepare request object to pass to utility function
        request = HttpRequest()

        # test with no group in cookie
        request.COOKIES['current_group'] = ''
        self.assertEqual(None, get_current_group(request))

        # test with invalid group id
        request.COOKIES['current_group'] = '12345'
        self.assertEqual(None, get_current_group(request))

        # test with proper group  identificator
        group = Group.objects.filter(title='Group1')[0]
        request.COOKIES['current_group'] = str(group.id)
        self.assertEqual(group, get_current_group(request))

    def test_get_groups(self):
        # prepare request object to pass to utility function
        request = HttpRequest()

        # test with no group in cookie
        cur_group = get_current_group(request)

        groups = None

        self.assertFalse(groups, get_groups(request))

        groups = []
        for group in Group.objects.all().order_by('title'):
            groups.append({
                'id': group.id,
                'title': group.title,
                'leader': group.leader and (u'%s %s' % (
                    group.leader.first_name,
                    group.leader.last_name)) or None,
                'selected': cur_group and cur_group.id == group.id and True or False
            })

        self.assertEqual(groups, get_groups(request))
