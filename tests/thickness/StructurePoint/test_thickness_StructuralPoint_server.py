from map2loop.thickness_calculator import StructuralPoint
from map2loop.project import Project
from map2loop.m2l_enums import VerboseLevel
import pathlib

import map2loop


def test_from_aus_state():

    bbox_3d = {
        "minx": 515687.31005864,
        "miny": 7493446.76593407,
        "maxx": 562666.860106543,
        "maxy": 7521273.57407786,
        "base": -3200,
        "top": 3000,
    }
    loop_project_filename = "wa_output.loop3d"
    module_path = map2loop.__file__.replace("__init__.py", "")

    proj = Project(
        use_australian_state_data="WA",
        working_projection="EPSG:28350",
        bounding_box=bbox_3d,
        config_filename=pathlib.Path(module_path)
        / pathlib.Path('_datasets')
        / pathlib.Path('config_files')
        / pathlib.Path('WA.json'),
        clut_filename=pathlib.Path(module_path)
        / pathlib.Path('_datasets')
        / pathlib.Path('clut_files')
        / pathlib.Path('WA_clut.csv'),
        # clut_file_legacy=False,
        verbose_level=VerboseLevel.NONE,
        loop_project_filename=loop_project_filename,
        overwrite_loopprojectfile=True,
    )

    proj.set_thickness_calculator(StructuralPoint())
    proj.run_all()
    print("from the test", proj.stratigraphic_column.stratigraphicUnits.columns)
    assert (
        proj.thickness_calculator.sorter_label == "StructuralPoint"
    ), 'Thickness_calc structural point not being set properly'
    assert (
        "ThicknessMedian" in proj.stratigraphic_column.stratigraphicUnits.columns
    ), 'Thickness not being calculated in StructuralPointCalculator'
    assert (
        "ThicknessStdDev" in proj.stratigraphic_column.stratigraphicUnits.columns
    ), 'Thickness std not being calculated in StructuralPointCalculator'
