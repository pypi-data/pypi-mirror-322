import inspect
from dataclasses import dataclass
from pollination_dsl.function import Function, script, Inputs, Outputs

from .scripts import incident_radiation


@dataclass
class IncidentRadiation(Function):
    """Calculate incident radiation."""

    north = Inputs.int(
        description='An angle for north direction. Default is 0.',
        default=0, spec={'type': 'integer', 'maximum': 360, 'minimum': 0}
    )

    high_sky_density = Inputs.bool(
        description='A boolean to indicate if a sky with high density should be used.',
        default=False
    )

    average_irradiance = Inputs.bool(
        description='A boolean to display the radiation results in units of average '
        'irradiance (W/m2) over the time period instead of units of cumulative '
        'radiation (kWh/m2).', default=False
    )

    radiation_benefit = Inputs.bool(
        description='Check to run a radiation benefit study that weighs helpful '
        'winter-time radiation against harmful summer-time radiation.',
        default=False
    )

    balance_temp = Inputs.float(
        description='Number for the balance temperature in (C) around which radiation '
        'switches from being helpful to harmful. Hours where the temperature is below '
        'this will contribute positively to the benefit (eg. passive solar heating) '
        'while hours above this temperature will contribute negatively (eg. increased '
        'cooling load). This should usually be the balance temperature of the building '
        'being studied.', default=16.,
        spec={'type': 'number', 'maximum': 26.0, 'minimum': 2.0}
    )

    ground_reflectance = Inputs.float(
        description='Number between 0 and 1 for the average ground reflectance. This is '
        'used to build an emissive ground hemisphere that influences points with an '
        'unobstructed view to the ground.', default=0.2,
        spec={'type': 'number', 'maximum': 1.0, 'minimum': 0}
    )

    offset_dist = Inputs.float(
        description='Number in model units for the distance to move points from '
        'the surfaces of the input geometry.', default=0.01,
        spec={'type': 'number', 'maximum': 1.0, 'minimum': 0.001}
    )

    run_period = Inputs.str(
        description='Analysis period as a string. The string must be formatted as '
        '{start-month}/{start-day} to {end-month}/{end-day} between {start-hour} and {end-hour} @{time-step} '
        'Default is 1/1 to 12/31 between 0 and 23 @1 for the whole year.',
        default='1/1 to 12/31 between 0 and 23 @1'
    )

    epw = Inputs.file(
        description='Path to epw weather file.', extensions=['epw'], path='weather.epw'
    )

    study_mesh = Inputs.file(
        description='Path to a JSON file for input study mesh in Ladybug Geometry '
        'format.', path='input_geo.json'
    )

    context_mesh = Inputs.file(
        description='Path to a JSON file for input context mesh in Ladybug Geometry '
        'format.', path='context_geo.json', optional=True
    )

    display_context = Inputs.bool(
        description='Boolean to note whether the context geometry should be included '
        'in the output visualization.',
        default=False
    )

    @script
    def run_incident_radiation(self):
        return inspect.getsource(incident_radiation)

    radiation_values = Outputs.file(
        description='Radiation values', path='results/results.json'
    )

    visualization_set = Outputs.file(
        description='Results visualization set', path='results/output.vsf'
    )
