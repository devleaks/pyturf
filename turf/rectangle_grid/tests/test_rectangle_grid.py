import pytest
import os

from turf.bbox_polygon import bbox_polygon
from turf.rectangle_grid import rectangle_grid

from turf.utils.test_setup import get_fixtures


current_path = os.path.dirname(os.path.realpath(__file__))

fixtures = get_fixtures(current_path)


class TestRectangleGrid:
    @pytest.mark.parametrize(
        "fixture",
        [
            pytest.param(fixture, id=fixture_name)
            for fixture_name, fixture in fixtures.items()
        ],
    )
    def test_rectangle_grid(self, fixture):
        bbox = fixture["in"]["bbox"]
        cell_width = fixture["in"]["cellWidth"]
        cell_height = fixture["in"]["cellHeight"]

        options = dict(
            (key, fixture["in"][key])
            for key in ["units", "mask", "properties"]
            if key in fixture["in"]
        )

        result = rectangle_grid(bbox, cell_width, cell_height, options)

        result = prepare_output(result, bbox, options)

        assert result == fixture["out"]


def prepare_output(result, bbox, options):
    for i in range(len(result["features"])):
        coords = round_coordinates(result["features"][i])
        result["features"][i] = coords

    bbox_poly = bbox_polygon(bbox)
    bbox_poly["properties"] = {"stroke": "#F00", "stroke-width": 6, "fill-opacity": 0}

    result["features"].append(bbox_poly)

    if "mask" in options:
        options["mask"]["properties"] = {
            "stroke": "#00F",
            "stroke-width": 6,
            "fill-opacity": 0,
        }
        result["features"].append(options["mask"])

    return result


def round_coordinates(cell_poly):
    """
    Rounds the coords of the polygon
    Only implemented to pass tests.

    :param cell_poly: polygon feature

    :returns: polygon feature
    """

    coords = cell_poly["geometry"]["coordinates"]
    coords = [
        [[round(coord, 6) for coord in point] for point in line] for line in coords
    ]

    cell_poly["geometry"]["coordinates"] = coords

    return cell_poly
