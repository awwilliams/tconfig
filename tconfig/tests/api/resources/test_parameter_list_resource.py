def test_parameters(api_client, api_prefix):
    url = f"{api_prefix}/parameters/"
    response = api_client.get(url)
    assert response.status_code == 200

    json_dict = response.json
    expected = {
        "parameter_List_url": f"{api_prefix}/parameters/",
        "parameter_list": [
            {
                "excluded": [],
                "excluded_by": [],
                "name": "Colour",
                "parameter_set": 1,
                "position": 0,
                "uid": 1,
                "values": [
                    {"name": "Red", "parameter": 1, "position": 0, "uid": 1},
                    {"name": "Green", "parameter": 1, "position": 1, "uid": 2},
                ],
            },
            {
                "excluded": [],
                "excluded_by": [],
                "name": "Pet",
                "parameter_set": 1,
                "position": 1,
                "uid": 2,
                "values": [
                    {"name": "Bird", "parameter": 2, "position": 0, "uid": 3},
                    {"name": "Cat", "parameter": 2, "position": 1, "uid": 4},
                    {"name": "Dog", "parameter": 2, "position": 2, "uid": 5},
                    {"name": "Fish", "parameter": 2, "position": 3, "uid": 6},
                ],
            },
            {
                "excluded": [],
                "excluded_by": [],
                "name": "Speed",
                "parameter_set": 1,
                "position": 2,
                "uid": 3,
                "values": [
                    {"name": "Fast", "parameter": 3, "position": 0, "uid": 7},
                    {"name": "Slow", "parameter": 3, "position": 1, "uid": 8},
                ],
            },
            {
                "excluded": [],
                "excluded_by": [],
                "name": "Music",
                "parameter_set": 1,
                "position": 3,
                "uid": 4,
                "values": [
                    {"name": "80s", "parameter": 4, "position": 0, "uid": 9},
                    {"name": "20s", "parameter": 4, "position": 1, "uid": 10},
                ],
            },
        ],
    }

    assert json_dict == expected


def test_parameter_add(api_client, api_prefix):
    request_data = {
        "name": "new_name",
    }
    url = f"{api_prefix}/parameters/"
    response = api_client.post(url, json=request_data)
    assert response.status_code == 201

    json_dict = response.json
    expected = {
        "message": "new parameter created",
        "new_parameter": {
            "excluded": [],
            "excluded_by": [],
            "name": "new_name",
            "parameter_set": 1,
            "position": 4,
            "uid": 5,
            "values": [],
        },
        "new_parameter_url": f"{api_prefix}/parameters/5",
        "parameter_list_url": f"{api_prefix}/parameters/",
        "parameter_set_url": f"{api_prefix}/parameterset/",
    }
    assert json_dict == expected


def test_parameter_add_with_values(api_client, api_prefix):
    request_data = {
        "name": "new_name",
        "values": ["new_val_1", "new_val_2"],
    }
    url = f"{api_prefix}/parameters/"
    response = api_client.post(url, json=request_data)
    assert response.status_code == 201

    json_dict = response.json
    expected = {
        "message": "new parameter created",
        "new_parameter": {
            "excluded": [],
            "excluded_by": [],
            "name": "new_name",
            "parameter_set": 1,
            "position": 4,
            "uid": 5,
            "values": [
                {"name": "new_val_1", "parameter": 5, "position": 0, "uid": 11},
                {"name": "new_val_2", "parameter": 5, "position": 1, "uid": 12},
            ],
        },
        "new_parameter_url": f"{api_prefix}/parameters/5",
        "parameter_list_url": f"{api_prefix}/parameters/",
        "parameter_set_url": f"{api_prefix}/parameterset/",
    }
    assert json_dict == expected


def test_parameter_add_400_no_data(api_client, api_prefix):
    request_data = {}
    url = f"{api_prefix}/parameters/"
    response = api_client.post(url, json=request_data)
    assert response.status_code == 400

    json_dict = response.json
    expected = {
        "message": "Validation error(s):  {'name': ['Missing data for required field.']}",
    }
    assert json_dict == expected


def test_parameter_add_400_wrong_attribute(api_client, api_prefix):
    request_data = {
        "name": "new_parameter",
        "wrong_attribute": "wrong_value",
    }
    url = f"{api_prefix}/parameters/"
    response = api_client.post(url, json=request_data)
    assert response.status_code == 400

    json_dict = response.json
    expected = {
        "message": "Validation error(s):  {'wrong_attribute': ['Unknown field.']}",
    }
    assert json_dict == expected


def test_parameter_add_400_name_is_none(api_client, api_prefix):
    request_data = {
        "name": None,
    }
    url = f"{api_prefix}/parameters/"
    response = api_client.post(url, json=request_data)
    assert response.status_code == 400

    json_dict = response.json
    expected = {
        "message": "Validation error(s):  {'name': ['Field may not be null.']}",
    }
    assert json_dict == expected


def test_parameter_add_400_name_is_empty(api_client, api_prefix):
    request_data = {
        "name": "",
    }
    url = f"{api_prefix}/parameters/"
    response = api_client.post(url, json=request_data)
    assert response.status_code == 400

    json_dict = response.json
    expected = {
        "message": "Validation error(s):  {'name': ['Shorter than minimum length 1.']}"
    }
    assert json_dict == expected


def test_parameter_move(api_client, api_prefix):
    request_data = {
        "oldIndex": 3,
        "newIndex": 1,
    }
    url = f"{api_prefix}/parameters/"
    response = api_client.put(url, json=request_data)
    assert response.status_code == 200

    json_dict = response.json
    expected = {
        "message": "parameter moved within list",
        "moved_parameter_url": f"{api_prefix}/parameters/4",
        "new_index": 1,
        "old_index": 3,
        "parameter_List_url": f"{api_prefix}/parameters/",
    }
    assert json_dict == expected

    response = api_client.get(f"{api_prefix}/parameters/4")
    assert response.status_code == 200

    json_dict = response.json
    expected = {
        "parameter": {
            "excluded": [],
            "excluded_by": [],
            "name": "Music",
            "parameter_set": 1,
            "position": 1,
            "uid": 4,
            "values": [
                {"name": "80s", "parameter": 4, "position": 0, "uid": 9},
                {"name": "20s", "parameter": 4, "position": 1, "uid": 10},
            ],
        },
        "parameter_set_url": f"{api_prefix}/parameterset/",
        "parameter_url": f"{api_prefix}/parameters/4",
    }
    assert json_dict == expected


def test_parameter_move_bad_old_index_low(api_client, api_prefix):
    request_data = {
        "oldIndex": -1,
        "newIndex": 1,
    }
    url = f"{api_prefix}/parameters/"
    response = api_client.put(url, json=request_data)
    assert response.status_code == 400

    json_dict = response.json
    expected = {
        "message": "Validation error(s):  {'oldIndex': ['Must be greater than or equal to 0.']}",
    }
    assert json_dict == expected


def test_parameter_move_bad_old_index_high(api_client, api_prefix):
    request_data = {
        "oldIndex": 5,
        "newIndex": 1,
    }
    url = f"{api_prefix}/parameters/"
    response = api_client.put(url, json=request_data)
    assert response.status_code == 400

    json_dict = response.json
    expected = {
        "message": "Validation error(s):  {'oldIndex': ['Must be less than or equal to 4.']}",
    }
    assert json_dict == expected


def test_parameter_move_bad_new_index_low(api_client, api_prefix):
    request_data = {
        "oldIndex": 3,
        "newIndex": -1,
    }
    url = f"{api_prefix}/parameters/"
    response = api_client.put(url, json=request_data)
    assert response.status_code == 400

    json_dict = response.json
    expected = {
        "message": "Validation error(s):  {'newIndex': ['Must be greater than or equal to 0.']}",
    }
    assert json_dict == expected


def test_parameter_move_bad_new_index_high(api_client, api_prefix):
    request_data = {
        "oldIndex": 3,
        "newIndex": 5,
    }
    url = f"{api_prefix}/parameters/"
    response = api_client.put(url, json=request_data)
    assert response.status_code == 400

    json_dict = response.json
    expected = {
        "message": "Validation error(s):  {'newIndex': ['Must be less than or equal to 4.']}",
    }
    assert json_dict == expected


def test_parameter_move_wrong_attribute(api_client, api_prefix):
    request_data = {
        "oldIndex": 3,
        "newIndex": 1,
        "wrongAttribute": 1,
    }
    url = f"{api_prefix}/parameters/"
    response = api_client.put(url, json=request_data)
    assert response.status_code == 400

    json_dict = response.json
    expected = {
        "message": "Validation error(s):  {'wrongAttribute': ['Unknown field.']}",
    }
    assert json_dict == expected


def test_parameter_move_missing_old_index(api_client, api_prefix):
    request_data = {
        "newIndex": 1,
    }
    url = f"{api_prefix}/parameters/"
    response = api_client.put(url, json=request_data)
    assert response.status_code == 400

    json_dict = response.json
    expected = {
        "message": "Validation error(s):  {'oldIndex': ['Missing data for required field.']}",
    }
    assert json_dict == expected


def test_parameter_move_missing_new_index(api_client, api_prefix):
    request_data = {
        "oldIndex": 3,
    }
    url = f"{api_prefix}/parameters/"
    response = api_client.put(url, json=request_data)
    assert response.status_code == 400

    json_dict = response.json
    expected = {
        "message": "Validation error(s):  {'newIndex': ['Missing data for required field.']}",
    }
    assert json_dict == expected
