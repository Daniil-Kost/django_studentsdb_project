from django.test import TestCase, Client, override_settings

from django.core.urlresolvers import reverse


@override_settings(LANGUAGE_CODE='en')
class TestStudentUpdateForm(TestCase):
    fixtures = ['students_test_data.json']

    def setUp(self):
        # remember test browser
        self.client = Client()

    # remember url to edit form
    # self.url = reverse_lazy('journal')

    def test_form(self):
        # login as admin to access student edit form
        self.client.login(username='admin', password='admin')

        # get form and check few fields there
        response = self.client.get(reverse('students_edit',
                                           kwargs={'pk': 1}))

        # check response status
        # self.assertEqual(response.status_code, 200)

        # check page title, few field titles and button on edit form
        self.assertIn('Middle Name', response.content)
        self.assertIn('Notes', response.content)
        self.assertIn('Form edit student', response.content)
        # self.assertIn('class="alert alert-warning"', response.content, response.content)
        self.assertIn('name="cancel_button"', response.content)
        self.assertIn('name="add_button"', response.content)
        self.assertIn('action="%s"' % reverse('students_edit',
                                              kwargs={'pk': 1}), response.content)
