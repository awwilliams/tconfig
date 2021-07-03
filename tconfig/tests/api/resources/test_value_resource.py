def test_value_select(api_client, api_prefix):
    response = api_client.get(f"{api_prefix}/values/1")
    assert response.status_code == 200

    # Check JSON response is the 'Red' parameter value.

    json_dict = response.json
    expected = {
        "message": "value found",
        "parameter_url": f"{api_prefix}/parameters/1",
        "value": {"name": "Red", "parameter": 1, "position": 0, "uid": 1},
        "value_url": f"{api_prefix}/values/1",
    }
    assert json_dict == expected


def test_value_select_404(api_client, api_prefix):
    response = api_client.get(
        f"{api_prefix}/values/98", headers={"Accept": "application/json"}
    )
    assert response.status_code == 404

    # Check JSON response contains an error message explaining that there
    # is no parameter with the requested name.

    json_dict = response.json
    expected = {
        "message": "No value with uid '98' was found in the parameter set. You have "
        f"requested this URI [{api_prefix}/values/98] but did you mean "
        f"{api_prefix}/values/<int:uid> or {api_prefix}/ or "
        f"{api_prefix}/parameters/<int:uid> ?"
    }
    assert json_dict == expected


def test_value_edit(api_client, api_prefix):
    request_data = {
        "name": "Pink",
    }
    response = api_client.patch(f"{api_prefix}/values/1", json=request_data)
    assert response.status_code == 200

    json_dict = response.json
    expected = {
        "message": "value updated",
        "value": {"name": "Pink", "parameter": 1, "position": 0, "uid": 1},
        "value_url": f"{api_prefix}/values/1",
        "parameter_url": f"{api_prefix}/parameters/1",
    }
    assert json_dict == expected


def test_value_edit_404(api_client, api_prefix):
    request_data = {
        "name": "Pink",
    }
    response = api_client.patch(f"{api_prefix}/values/98", json=request_data)
    assert response.status_code == 404

    json_dict = response.json
    expected = {
        "message": "No value with uid '98' was found in the parameter set. You have "
        f"requested this URI [{api_prefix}/values/98] but did you mean "
        f"{api_prefix}/values/<int:uid> or {api_prefix}/ or "
        f"{api_prefix}/parameters/<int:uid> ?"
    }
    assert json_dict == expected


def test_value_edit_400_wrong_attribute(api_client, api_prefix):
    request_data = {
        "colour": "Pink",
    }
    response = api_client.patch(f"{api_prefix}/values/1", json=request_data)
    assert response.status_code == 400

    json_dict = response.json
    expected = {
        "message": "Validation error(s):  {'colour': ['Unknown field.']}",
    }
    assert json_dict == expected


def test_value_edit_400_empty_request(api_client, api_prefix):
    request_data = {}
    response = api_client.patch(f"{api_prefix}/values/1", json=request_data)
    assert response.status_code == 400

    json_dict = response.json
    expected = {"message": "No updates provided with request"}
    assert json_dict == expected


def test_value_edit_400_name_is_none(api_client, api_prefix):
    request_data = {
        "name": None,
    }
    response = api_client.patch(f"{api_prefix}/values/1", json=request_data)
    assert response.status_code == 400

    json_dict = response.json
    expected = {
        "message": "Validation error(s):  {'name': ['Field may not be null.']}",
    }
    assert json_dict == expected


def test_value_edit_400_name_is_empty(api_client, api_prefix):
    request_data = {
        "name": "",
    }
    response = api_client.patch(f"{api_prefix}/values/1", json=request_data)
    assert response.status_code == 400

    json_dict = response.json
    expected = {
        "message": "Validation error(s):  {'name': ['Shorter than minimum length 1.']}",
    }
    assert json_dict == expected


def test_value_delete(api_client, api_prefix):
    response = api_client.delete(f"{api_prefix}/values/1")
    assert response.status_code == 200
    json_dict = response.json
    expected = {
        "deleted_value": {"name": "Red", "parameter": 1, "position": 0, "uid": 1},
        "message": "value 1 deleted",
        "parameter_url": f"{api_prefix}/parameters/1",
    }
    assert json_dict == expected


def test_value_delete_404(api_client, api_prefix):
    response = api_client.delete(f"{api_prefix}/values/98")
    assert response.status_code == 404
    json_dict = response.json
    expected = {
        "message": "No value with uid '98' was found in the parameter set. You have "
        f"requested this URI [{api_prefix}/values/98] but did you mean "
        f"{api_prefix}/values/<int:uid> or {api_prefix}/ or "
        f"{api_prefix}/parameters/<int:uid> ?"
    }
    assert json_dict == expected
