"""
Test the apps' template tags
"""

# Django
from django.template import Context, Template
from django.test import TestCase

# AA Fleet Finder
from fleetfinder import __version__
from fleetfinder.helper.static_files import calculate_integrity_hash


class TestVersionedStatic(TestCase):
    """
    Test the `fleetfinder_static` template tag
    """

    def test_versioned_static(self):
        """
        Test should return the versioned static

        :return:
        :rtype:
        """

        context = Context(dict_={"version": __version__})
        template_to_render = Template(
            template_string=(
                "{% load fleetfinder %}"
                "{% fleetfinder_static 'css/fleetfinder.min.css' %}"
            )
        )

        rendered_template = template_to_render.render(context)

        expected_static_src = (
            f'/static/fleetfinder/css/fleetfinder.min.css?v={context["version"]}'
        )
        expected_static_src_integrity = calculate_integrity_hash(
            "css/fleetfinder.min.css"
        )

        self.assertIn(member=expected_static_src, container=rendered_template)
        self.assertIn(member=expected_static_src_integrity, container=rendered_template)
