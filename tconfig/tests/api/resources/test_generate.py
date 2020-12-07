
def test_gen_request_no_existing_configs(api_client, api_prefix):
    request_data = {
        'algorithm_name': 'recursive',
        'coverage_degree': 2,
        'existing_configurations': [],
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
                        {'name': 'Blue', 'parameter': 1, 'position': 2, 'uid': 3},
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
                        {'name': 'Bird', 'parameter': 2, 'position': 0, 'uid': 4},
                        {'name': 'Cat', 'parameter': 2, 'position': 1, 'uid': 5},
                        {'name': 'Dog', 'parameter': 2, 'position': 2, 'uid': 6},
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
                        {'name': 'Medium', 'parameter': 3, 'position': 1, 'uid': 8},
                        {'name': 'Slow', 'parameter': 3, 'position': 2, 'uid': 9}
                    ]
                },
                {
                    'excluded': [],
                    'excluded_by': [],
                    'name': 'Music',
                    'parameter_set': 1,
                    'position': 3,
                    'uid': 4,
                    'values': [
                        {'name': '70s', 'parameter': 4, 'position': 0, 'uid': 10},
                        {'name': '80s', 'parameter': 4, 'position': 1, 'uid': 11},
                        {'name': '20s', 'parameter': 4, 'position': 2, 'uid': 12},
                    ],
                },
            ],
            'position': None,
            'uid': 1,
        }
    }

    url = f'{api_prefix}/generate/'
    response = api_client.post(url, json=request_data)
    assert response.status_code == 200

    json_dict = response.json
    expected = {
        'configuration_set': {
            'configurations': [
                {
                    'Colour': {'name': 'Red', 'uid': 1},
                    'Music': {'name': '70s', 'uid': 10},
                    'Pet': {'name': 'Bird', 'uid': 4},
                    'Speed': {'name': 'Fast', 'uid': 7}
                },
                {
                    'Colour': {'name': 'Red', 'uid': 1},
                    'Music': {'name': '80s', 'uid': 11},
                    'Pet': {'name': 'Cat', 'uid': 5},
                    'Speed': {'name': 'Medium', 'uid': 8}
                },
                {
                    'Colour': {'name': 'Red', 'uid': 1},
                    'Music': {'name': '20s', 'uid': 12},
                    'Pet': {'name': 'Dog', 'uid': 6},
                    'Speed': {'name': 'Slow', 'uid': 9}
                },
                {
                    'Colour': {'name': 'Green', 'uid': 2},
                    'Music': {'name': '20s', 'uid': 12},
                    'Pet': {'name': 'Bird', 'uid': 4},
                    'Speed': {'name': 'Medium', 'uid': 8}
                },
                {
                    'Colour': {'name': 'Green', 'uid': 2},
                    'Music': {'name': '70s', 'uid': 10},
                    'Pet': {'name': 'Cat', 'uid': 5},
                    'Speed': {'name': 'Slow', 'uid': 9}
                },
                {
                    'Colour': {'name': 'Green', 'uid': 2},
                    'Music': {'name': '80s', 'uid': 11},
                    'Pet': {'name': 'Dog', 'uid': 6},
                    'Speed': {'name': 'Fast', 'uid': 7}
                },
                {
                    'Colour': {'name': 'Blue', 'uid': 3},
                    'Music': {'name': '80s', 'uid': 11},
                    'Pet': {'name': 'Bird', 'uid': 4},
                    'Speed': {'name': 'Slow', 'uid': 9}
                },
                {
                    'Colour': {'name': 'Blue', 'uid': 3},
                    'Music': {'name': '20s', 'uid': 12},
                    'Pet': {'name': 'Cat', 'uid': 5},
                    'Speed': {'name': 'Fast', 'uid': 7}
                },
                {
                    'Colour': {'name': 'Blue', 'uid': 3},
                    'Music': {'name': '70s', 'uid': 10},
                    'Pet': {'name': 'Dog', 'uid': 6},
                    'Speed': {'name': 'Medium', 'uid': 8}
                }
            ],
            'parameter_names': ['Colour', 'Pet', 'Speed', 'Music']
        },
        'message': 'test configurations generated',
        'parameter_set_url': f'{api_prefix}/parameterset/'
    }
    assert json_dict == expected
