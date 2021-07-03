def test_value_list(api_client, api_prefix):
    response = api_client.get(f"{api_prefix}/values/")
    assert response.status_code == 200

    json_dict = response.json
    expected = {
        "value_List_url": f"{api_prefix}/values/",
        "value_list": [
            {"name": "Red", "parameter": 1, "position": 0, "uid": 1},
            {"name": "Green", "parameter": 1, "position": 1, "uid": 2},
            {"name": "Bird", "parameter": 2, "position": 0, "uid": 3},
            {"name": "Cat", "parameter": 2, "position": 1, "uid": 4},
            {"name": "Dog", "parameter": 2, "position": 2, "uid": 5},
            {"name": "Fish", "parameter": 2, "position": 3, "uid": 6},
            {"name": "Fast", "parameter": 3, "position": 0, "uid": 7},
            {"name": "Slow", "parameter": 3, "position": 1, "uid": 8},
            {"name": "80s", "parameter": 4, "position": 0, "uid": 9},
            {"name": "20s", "parameter": 4, "position": 1, "uid": 10},
        ],
    }
    assert json_dict == expected


def test_value_list_add(api_client, api_prefix):
    request_data = {
        "name": "new_name",
    }
    url = f"{api_prefix}/values/"
    response = api_client.post(url, json=request_data)
    assert response.status_code == 201

    json_dict = response.json
    expected = {
        "message": "new value created",
        "new_value": {
            "name": "new_name",
            "parameter": None,
            "position": None,
            "uid": 11,
        },
        "new_value_url": f"{api_prefix}/values/11",
        "value_List_url": f"{api_prefix}/values/",
    }
    assert json_dict == expected


def test_value_list_add_400_name_missing(api_client, api_prefix):
    request_data = {}
    url = f"{api_prefix}/values/"
    response = api_client.post(url, json=request_data)
    assert response.status_code == 400

    json_dict = response.json
    expected = {
        "message": "Validation error(s):  {'name': ['Missing data for required field.']}",
    }
    assert json_dict == expected


def test_value_list_add_400_wrong_attribute(api_client, api_prefix):
    request_data = {
        "name": "new_name",
        "wrong_attribute": "wrong_value",
    }
    url = f"{api_prefix}/values/"
    response = api_client.post(url, json=request_data)
    assert response.status_code == 400

    json_dict = response.json
    expected = {
        "message": "Validation error(s):  {'wrong_attribute': ['Unknown field.']}",
    }
    assert json_dict == expected


def test_value_list_add_400_name_is_none(api_client, api_prefix):
    request_data = {
        "name": None,
    }
    url = f"{api_prefix}/values/"
    response = api_client.post(url, json=request_data)
    assert response.status_code == 400

    json_dict = response.json
    expected = {
        "message": "Validation error(s):  {'name': ['Field may not be null.']}",
    }
    assert json_dict == expected


def test_value_list_add_400_name_is_empty(api_client, api_prefix):
    request_data = {
        "name": "",
    }
    url = f"{api_prefix}/values/"
    response = api_client.post(url, json=request_data)
    assert response.status_code == 400

    json_dict = response.json
    expected = {
        "message": "Validation error(s):  {'name': ['Shorter than minimum length 1.']}",
    }
    assert json_dict == expected
