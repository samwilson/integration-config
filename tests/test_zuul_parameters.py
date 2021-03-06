import os
import unittest

from fakes import FakeJob

set_parameters = None  # defined for flake8

# Import function
execfile(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '../zuul/parameter_functions.py'))


class TestZuulSetParameters(unittest.TestCase):

    def test_debian_glue_default_to_no_network(self):
        job = FakeJob('debian-glue')
        params = {'ZUUL_PROJECT': 'some/project'}
        set_parameters(None, job, params)
        self.assertNotIn('PBUILDER_USENETWORK', params)

    def test_zuul_debian_glue_with_network(self):
        job = FakeJob('debian-glue')
        params = {'ZUUL_PROJECT': 'integration/zuul'}
        set_parameters(None, job, params)
        self.assertIn('PBUILDER_USENETWORK', params)
