def test_parameter_select(api_client, api_prefix):
    response = api_client.get(f'{api_prefix}/parameters/1')
    assert response.status_code == 200

    json_dict = response.json
    expected = {
        'parameter': {
            'excluded': [],
            'excluded_by': [],
            'name': 'Colour',
            'parameter_set': 1,
            'position': 0,
            'uid': 1,
            'values': [
                {'name': 'Red', 'parameter': 1, 'position': 0, 'uid': 1},
                {'name': 'Green', 'parameter': 1, 'position': 1, 'uid': 2}
            ]
        },
        'parameter_set_url': f'{api_prefix}/parameterset/',
        'parameter_url': f'{api_prefix}/parameters/1',
    }
    assert json_dict == expected


def test_parameter_select_404_json(api_client, api_prefix):
    response = api_client.get(f'{api_prefix}/parameters/98')
    assert response.status_code == 404

    json_dict = response.json
    expected = {
        'message': "No parameter with uid '98' was found in the parameter set. You "
                   f'have requested this URI [{api_prefix}/parameters/98] but did '
                   f'you mean {api_prefix}/parameters/<int:uid> or '
                   f'{api_prefix}/parameterset/ or {api_prefix}/parameters/<int:uid>/values/ '
                   '?'
    }
    assert json_dict == expected


def test_parameter_edit(api_client, api_prefix):
    request_data = {
        "name": "Flavour",
    }
    response = api_client.patch(f'{api_prefix}/parameters/1', json=request_data)
    assert response.status_code == 200

    json_dict = response.json
    expected = {
        'message': 'parameter updated',
        'parameter': {
            'excluded': [],
            'excluded_by': [],
            'name': 'Flavour',
            'parameter_set': 1,
            'position': 0,
            'uid': 1,
            'values': [
                {'name': 'Red', 'parameter': 1, 'position': 0, 'uid': 1},
                {'name': 'Green', 'parameter': 1, 'position': 1, 'uid': 2},
            ],
        },
        'parameter_set_url': f'{api_prefix}/parameterset/',
        'parameter_url': f'{api_prefix}/parameters/1',
    }
    assert json_dict == expected


def test_parameter_edit_404(api_client, api_prefix):
    request_data = {
        "name": "Flavour",
    }
    response = api_client.patch(f'{api_prefix}/parameters/98',
                                json=request_data)
    assert response.status_code == 404

    json_dict = response.json
    expected = {
        'message': "No parameter with uid '98' was found in the parameter set. You "
                   f'have requested this URI [{api_prefix}/parameters/98] but did '
                   f'you mean {api_prefix}/parameters/<int:uid> or '
                   f'{api_prefix}/parameterset/ or '
                   f'{api_prefix}/parameters/<int:uid>/values/ ?'
    }
    assert json_dict == expected


def test_parameter_edit_400_missing_attribute(api_client, api_prefix):
    request_data = {
        "colour": "Pink",
    }
    response = api_client.patch(f'{api_prefix}/parameters/1', json=request_data)
    assert response.status_code == 400

    json_dict = response.json
    expected = {'message': "Validation error(s):  {'colour': ['Unknown field.']}", }
    assert json_dict == expected


def test_parameter_edit_400_name_none(api_client, api_prefix):
    request_data = {
        "name": None,
    }
    response = api_client.patch(f'{api_prefix}/parameters/1', json=request_data)
    assert response.status_code == 400

    json_dict = response.json
    expected = {'message': "Validation error(s):  {'name': ['Field may not be null.']}", }
    assert json_dict == expected


def test_parameter_edit_400_name_empty(api_client, api_prefix):
    request_data = {
        "name": "",
    }
    response = api_client.patch(f'{api_prefix}/parameters/1', json=request_data)
    assert response.status_code == 400

    json_dict = response.json
    expected = {
        'message': "Validation error(s):  {'name': ['Shorter than minimum length 1.']}",
    }
    assert json_dict == expected


def test_parameter_delete(api_client, api_prefix):
    response = api_client.delete(f'{api_prefix}/parameters/1')
    assert response.status_code == 200
    json_dict = response.json
    expected = {
        'deleted_parameter_name': 'Colour',
        'message': 'parameter 1 deleted',
        'parameter_set_url': f'{api_prefix}/parameterset/',
    }
    assert json_dict == expected


def test_parameter_delete_404(api_client, api_prefix):
    response = api_client.delete(f'{api_prefix}/parameters/98')
    assert response.status_code == 404
    json_dict = response.json
    expected = {
        'message': "No parameter with uid '98' was found in the parameter set. You "
                   f'have requested this URI [{api_prefix}/parameters/98] but did '
                   f'you mean {api_prefix}/parameters/<int:uid> or '
                   f'{api_prefix}/parameterset/ or '
                   f'{api_prefix}/parameters/<int:uid>/values/ ?'
    }
    assert json_dict == expected
