def test_parameter_exclusion_empty(api_client, api_prefix):
    response = api_client.get(f'{api_prefix}/parameters/1/exclusions/')
    assert response.status_code == 200

    json_dict = response.json
    expected = {
        'message': 'exclusions for parameter 1',
        'parameter': {'excluded': [], 'excluded_by': [], 'name': 'Colour', 'uid': 1},
        'parameter_url': f'{api_prefix}/parameters/1',
        'parameter_exclusion_url': f'{api_prefix}/parameters/1/exclusions/',
    }
    assert json_dict == expected


def test_parameter_exclusion_non_empty(api_client, api_prefix):
    request_data = {
        'excluded': [3, ],
    }
    response = api_client.post(f'{api_prefix}/parameters/1/exclusions/', json=request_data)
    assert response.status_code == 201

    response = api_client.get(f'{api_prefix}/parameters/1/exclusions/')
    assert response.status_code == 200

    json_dict = response.json
    expected = {
        'message': 'exclusions for parameter 1',
        'parameter': {
            'name': 'Colour',
            'uid': 1,
            'excluded': [{'name': 'Speed', 'uid': 3}],
            'excluded_by': [],
        },
        'parameter_url': f'{api_prefix}/parameters/1',
        'parameter_exclusion_url': f'{api_prefix}/parameters/1/exclusions/',
    }
    assert json_dict == expected


def test_parameter_exclusion_post(api_client, api_prefix):
    request_data = {
        'excluded': [3, 4],
    }

    response = api_client.post(f'{api_prefix}/parameters/1/exclusions/', json=request_data)
    assert response.status_code == 201

    json_dict = response.json
    expected = {
        'message': 'parameter exclusion created',
        'parameter': {
            'uid': 1,
            'name': 'Colour',
            'excluded': [
                {'name': 'Speed', 'uid': 3},
                {'name': 'Music', 'uid': 4},
            ],
            'excluded_by': [],
        },
        'parameter_url': '/tconfig/api/v1/parameters/1',
    }
    assert json_dict == expected
