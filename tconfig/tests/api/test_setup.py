"""
Flask client test cases for the /tconfig/setup route that creates a sample
parameter set and puts it in the database for use by other API routes.
"""
from tconfig.orm.parmset import ParameterSetDao


def test_setup_response(client, api_prefix):
    """
    Check that after calling the 'setup' route, the JSON return content has
    the expected parameter and value definitions.

    :param client: Flask client test fixture.

    """
    response = client.get(f'{api_prefix}/setup')
    assert response.status_code == 200

    # Check JSON response is the entire parameter set.

    json_dict = response.json
    expected = {
        'parameter_set': {
            'name': None,
            'parameters': [
                {
                    'excluded': [],
                    'excluded_by': [],
                    'name': 'Colour',
                    'parameter_set': 1,
                    'position': 0,
                    'uid': 1,
                    'values': [
                        {'name': 'Red', 'parameter': 1, 'position': 0, 'uid': 1},
                        {'name': 'Green', 'parameter': 1, 'position': 1, 'uid': 2},
                    ],
                },
                {
                    'excluded': [],
                    'excluded_by': [],
                    'name': 'Pet',
                    'parameter_set': 1,
                    'position': 1,
                    'uid': 2,
                    'values': [
                        {'name': 'Bird', 'parameter': 2, 'position': 0, 'uid': 3},
                        {'name': 'Cat', 'parameter': 2, 'position': 1, 'uid': 4},
                        {'name': 'Dog', 'parameter': 2, 'position': 2, 'uid': 5},
                        {'name': 'Fish', 'parameter': 2, 'position': 3, 'uid': 6},
                    ],
                },
                {
                    'excluded': [],
                    'excluded_by': [],
                    'name': 'Speed',
                    'parameter_set': 1,
                    'position': 2,
                    'uid': 3,
                    'values': [
                        {'name': 'Fast', 'parameter': 3, 'position': 0, 'uid': 7},
                        {'name': 'Slow', 'parameter': 3, 'position': 1, 'uid': 8},
                    ],
                },
                {
                    'excluded': [],
                    'excluded_by': [],
                    'name': 'Music',
                    'parameter_set': 1,
                    'position': 3,
                    'uid': 4,
                    'values': [
                        {'name': '80s', 'parameter': 4, 'position': 0, 'uid': 9},
                        {'name': '20s', 'parameter': 4, 'position': 1, 'uid': 10},
                    ],
                },
            ],
            'position': None,
            'uid': 1,
        },
        'parameter_set_url': f'{api_prefix}/parameterset/',
    }
    assert json_dict == expected


def test_setup_db(client, api_prefix):
    """
    Check that after calling the 'setup' route, the database has one
    parameter set with expected parameter names and values names.

    :param client: Flask client test fixture.

    """
    response = client.get(f'{api_prefix}/setup')
    assert response.status_code == 200

    ps_list = ParameterSetDao.query.all()  # @UndefinedVariable
    assert len(ps_list) == 1
    ps = ps_list[0]
    parm_names = [parm.name for parm in ps]
    assert parm_names == ['Colour', 'Pet', 'Speed', 'Music']

    expected_values = {
        "Colour": ["Red", "Green"],
        "Pet": ["Bird", "Cat", "Dog", "Fish"],
        "Speed": ["Fast", "Slow"],
        "Music": ["80s", "20s"],
    }
    for parm in ps:
        assert [v.name for v in parm.values] == expected_values[parm.name]
