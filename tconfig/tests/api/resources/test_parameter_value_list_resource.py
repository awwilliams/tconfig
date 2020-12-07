def test_parameter_values(api_client, api_prefix):
    response = api_client.get(f'{api_prefix}/parameters/1/values/')
    assert response.status_code == 200

    json_dict = response.json
    expected = {
        'message': 'value list for parameter 1',
        'parameter_url': f'{api_prefix}/parameters/1',
        'parameter_value_list_url': f'{api_prefix}/parameters/1/values/',
        'values': [
            {'name': 'Red', 'parameter': 1, 'position': 0, 'uid': 1},
            {'name': 'Green', 'parameter': 1, 'position': 1, 'uid': 2}
        ]
    }
    assert json_dict == expected


def test_parameter_values_404(api_client, api_prefix):
    response = api_client.get(f'{api_prefix}/parameters/99/values/')
    assert response.status_code == 404

    json_dict = response.json
    expected = {
        'message': "No parameter with uid '99' was found in the parameter set. You "
                   f'have requested this URI [{api_prefix}/parameters/99/values/] '
                   f'but did you mean {api_prefix}/parameters/<int:uid>/values/ or '
                   f'{api_prefix}/parameterset/ or '
                   f'{api_prefix}/parameters/<int:uid> ?'
    }
    assert json_dict == expected


def test_value_add(api_client, api_prefix):
    request_data = {
        "name": "new_name",
    }
    url = f'{api_prefix}/parameters/1/values/'
    response = api_client.post(url, json=request_data)
    assert response.status_code == 201

    json_dict = response.json
    expected = {
        'message': 'new value created',
        'new_value': {'name': 'new_name', 'parameter': 1, 'position': 2, 'uid': 11},
        'new_value_url': f'{api_prefix}/values/11',
        'parameter_url': f'{api_prefix}/parameters/1',
        'parameter_value_list_url': f'{api_prefix}/parameters/1/values/',
    }
    assert json_dict == expected


def test_value_add_404_bad_parameter(api_client, api_prefix):
    request_data = {
        "name": "new_name",
    }
    url = f'{api_prefix}/parameters/98/values/'
    response = api_client.post(url, json=request_data)
    assert response.status_code == 404

    json_dict = response.json
    expected = {
        'message': "No parameter with uid '98' was found in the parameter set. You "
                   f'have requested this URI [{api_prefix}/parameters/98/values/] '
                   f'but did you mean {api_prefix}/parameters/<int:uid>/values/ or '
                   f'{api_prefix}/parameterset/ or '
                   f'{api_prefix}/parameters/<int:uid> ?'
    }
    assert json_dict == expected


def test_value_add_400_wrong_attribute(api_client, api_prefix):
    request_data = {
        "name": "new_name",
        "wrong_attribute": "wrong_value",
    }
    url = f'{api_prefix}/parameters/1/values/'
    response = api_client.post(url, json=request_data)
    assert response.status_code == 400

    json_dict = response.json
    expected = {'message': "Validation error(s):  {'wrong_attribute': ['Unknown field.']}", }
    assert json_dict == expected


def test_value_add_400_name_no_data(api_client, api_prefix):
    request_data = {}
    url = f'{api_prefix}/parameters/1/values/'
    response = api_client.post(url, json=request_data)
    assert response.status_code == 400

    json_dict = response.json
    expected = {
        'message': "Validation error(s):  {'name': ['Missing data for required field.']}",
    }
    assert json_dict == expected


def test_value_add_400_name_is_empty(api_client, api_prefix):
    request_data = {
        "name": "",
        "parameter": 1,
    }
    url = f'{api_prefix}/parameters/1/values/'
    response = api_client.post(url, json=request_data)
    assert response.status_code == 400

    json_dict = response.json
    expected = {
        'message': "Validation error(s):  {'name': ['Shorter than minimum length 1.']}",
    }
    assert json_dict == expected


def test_value_move(api_client, api_prefix):
    request_data = {
        "oldIndex": 3,
        "newIndex": 1,
    }
    url = f'{api_prefix}/parameters/2/values/'
    response = api_client.put(url, json=request_data)
    assert response.status_code == 200

    json_dict = response.json
    expected = {
        'message': 'value moved within list',
        'moved_value_uri': f'{api_prefix}/values/6',
        'new_index': 1,
        'old_index': 3,
    }
    assert json_dict == expected

    response = api_client.get(f'{api_prefix}/values/6')
    assert response.status_code == 200

    json_dict = response.json
    expected = {
        'message': 'value found',
        'parameter_url': f'{api_prefix}/parameters/2',
        'value': {'name': 'Fish', 'parameter': 2, 'position': 1, 'uid': 6},
        'value_url': f'{api_prefix}/values/6'
    }
    assert json_dict == expected


def test_value_move_bad_old_index_low(api_client, api_prefix):
    request_data = {
        "oldIndex": -1,
        "newIndex": 1,
    }
    url = f'{api_prefix}/parameters/2/values/'
    response = api_client.put(url, json=request_data)
    assert response.status_code == 400

    json_dict = response.json
    expected = {
        'message': "Validation error(s):  {'oldIndex': ['Must be greater than or equal to 0.']}",
    }
    assert json_dict == expected


def test_value_move_bad_old_index_high(api_client, api_prefix):
    request_data = {
        "oldIndex": 5,
        "newIndex": 1,
    }
    url = f'{api_prefix}/parameters/2/values/'
    response = api_client.put(url, json=request_data)
    assert response.status_code == 400

    json_dict = response.json
    expected = {
        'message': "Validation error(s):  {'oldIndex': ['Must be less than or equal to 4.']}",
    }
    assert json_dict == expected


def test_value_move_bad_new_index_low(api_client, api_prefix):
    request_data = {
        "oldIndex": 3,
        "newIndex": -1,
    }
    url = f'{api_prefix}/parameters/2/values/'
    response = api_client.put(url, json=request_data)
    assert response.status_code == 400

    json_dict = response.json
    expected = {
        'message': "Validation error(s):  {'newIndex': ['Must be greater than or equal to 0.']}",
    }
    assert json_dict == expected


def test_value_move_bad_new_index_high(api_client, api_prefix):
    request_data = {
        "oldIndex": 3,
        "newIndex": 5,
    }
    url = f'{api_prefix}/parameters/2/values/'
    response = api_client.put(url, json=request_data)
    assert response.status_code == 400

    json_dict = response.json
    expected = {
        'message': "Validation error(s):  {'newIndex': ['Must be less than or equal to 4.']}",
    }
    assert json_dict == expected


def test_value_move_wrong_attribute(api_client, api_prefix):
    request_data = {
        "oldIndex": 3,
        "newIndex": 1,
        "wrongAttribute": 0
    }
    url = f'{api_prefix}/parameters/2/values/'
    response = api_client.put(url, json=request_data)
    assert response.status_code == 400

    json_dict = response.json
    expected = {'message': "Validation error(s):  {'wrongAttribute': ['Unknown field.']}", }
    assert json_dict == expected


def test_value_move_missing_old_index(api_client, api_prefix):
    request_data = {
        "newIndex": 1,
    }
    url = f'{api_prefix}/parameters/2/values/'
    response = api_client.put(url, json=request_data)
    assert response.status_code == 400

    json_dict = response.json
    expected = {
        'message': "Validation error(s):  {'oldIndex': ['Missing data for required field.']}",
    }
    assert json_dict == expected


def test_value_move_missing_new_index(api_client, api_prefix):
    request_data = {
        "oldIndex": 3,
    }
    url = f'{api_prefix}/parameters/2/values/'
    response = api_client.put(url, json=request_data)
    assert response.status_code == 400

    json_dict = response.json
    expected = {
        'message': "Validation error(s):  {'newIndex': ['Missing data for required field.']}",
    }
    assert json_dict == expected
