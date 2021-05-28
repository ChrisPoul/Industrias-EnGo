from EnGo.models import raw_material
from . import RawMaterialTest
from EnGo.models.raw_material import RawMaterial


class TestValidateEmptyValues(RawMaterialTest):

    def test_should_not_return_error_given_valid_raw_material(self):
        raw_material = RawMaterial(
            material_name="Valid Name"
        )
        error = raw_material.validation.validate()

        self.assertEqual(error, None)