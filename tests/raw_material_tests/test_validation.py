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
    
    def test_should_return_erro_given_empty_value(self):
        raw_material = RawMaterial(
            material_name=""
        )
        error = raw_material.validation.validate()
        
        self.assertNotEqual(error, None)
    

class TestValidateUniqueValues(RawMaterialTest):

    def test_should_not_return_error_given_valid_raw_material(self):
        raw_material = RawMaterial(
            material_name="Valid Name"
        )
        error = raw_material.validation.validate()

        self.assertEqual(error, None)
    
    def test_should_return_error_given_repeated_value(self):
        raw_material = RawMaterial(
            material_name="Test Material"
        )
        error = raw_material.validation.validate()

        self.assertNotEqual(error, None)
    
    def test_should_not_return_error_given_raw_material_already_in_db(self):
        error = self.raw_material.validation.validate()

        self.assertEqual(error, None)