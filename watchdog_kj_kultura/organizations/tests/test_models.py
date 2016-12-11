from django.test import TestCase

from ..factories import OrganizationFactory
from ..models import Organization


class OrganizationQuerySetTestCase(TestCase):

    def test_switch_visibility(self):
        visible = OrganizationFactory(visible=True)
        unvisible = OrganizationFactory(visible=False)
        Organization.objects.switch_visibility()

        visible.refresh_from_db()
        unvisible.refresh_from_db()

        self.assertEqual(visible.visible, False)
        self.assertEqual(unvisible.visible, True)
