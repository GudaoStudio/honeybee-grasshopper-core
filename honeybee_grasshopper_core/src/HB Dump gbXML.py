# Honeybee: A Plugin for Environmental Analysis (GPL)
# This file is part of Honeybee.
#
# Copyright (c) 2021, Ladybug Tools.
# You should have received a copy of the GNU General Public License
# along with Honeybee; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>


"""
Dump a Honyebee Model to a gbXML file.
_
The gbXML format is a common open standard used to transfer energy model geometry
and (some) energy simulation properties from one simulation environment to another.
_
The forward translators within the OpenStudio SDK are used to export all Honeybee
model geometry and properties.
-

    Args:
        _model: A Honeybee Model object to be written to a gbXML file.
        _name_: A name for the file to which the honeybee objects will be
            written. (Default: 'unnamed').
        _folder_: An optional directory into which the honeybee objects will be
            written.  The default is set to the default simulation folder.
        _dump: Set to "True" to save the honeybee model to a gbXML file.

    Returns:
        report: Errors, warnings, etc.
        hb_file: The location of the file where the honeybee JSON is saved.
"""

ghenv.Component.Name = 'HB Dump gbXML'
ghenv.Component.NickName = 'DumpGBXML'
ghenv.Component.Message = '1.2.0'
ghenv.Component.Category = 'Honeybee'
ghenv.Component.SubCategory = '3 :: Serialize'
ghenv.Component.AdditionalHelpFromDocStrings = '4'

try:  # import the core honeybee dependencies
    from honeybee.model import Model
    from honeybee.config import folders
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))

try:  # import the honeybee_energy dependencies
    from honeybee_energy.run import to_gbxml_osw, run_osw
except ImportError as e:
    raise ImportError('\nFailed to import honeybee_energy:\n\t{}'.format(e))

try:  # import the core ladybug_rhino dependencies
    from ladybug_rhino.grasshopper import all_required_inputs
except ImportError as e:
    raise ImportError('\nFailed to import ladybug_rhino:\n\t{}'.format(e))

import os


if all_required_inputs(ghenv.Component) and _dump:
    # check the input and set the component defaults
    assert isinstance(_model, Model), \
        'Excpected Honeybee Model object. Got {}.'.format(type(_model))
    name = _name_ if _name_ is not None else 'unnamed'
    gbxml_file = '{}.gbxml'.format(name)
    folder = _folder_ if _folder_ is not None else folders.default_simulation_folder
    gbxml = os.path.join(folder, gbxml_file)

    # write out the HBJSON and OpenStudio Workflow (OSW) that translates models to gbXML
    out_directory = os.path.join(folders.default_simulation_folder, 'temp_translate')
    if not os.path.isdir(out_directory):
        os.makedirs(out_directory)
    hb_file = _model.to_hbjson(name, out_directory, included_prop=['energy'])
    osw = to_gbxml_osw(hb_file, gbxml, out_directory)

    # run the measure to translate the model JSON to an openstudio measure
    osm, idf = run_osw(osw, silent=True)
    if idf is None:
        raise Exception('Running OpenStudio CLI failed.')