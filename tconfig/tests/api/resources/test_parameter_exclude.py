def test_parameter_exclusion_delete(api_client, api_prefix):
    request_data = {
        "excluded": [
            3,
        ],
    }
    response = api_client.post(
        f"{api_prefix}/parameters/1/exclusions/", json=request_data
    )
    assert response.status_code == 201

    response = api_client.delete(f"{api_prefix}/parameters/1/exclusions/3")
    assert response.status_code == 200

    json_dict = response.json
    expected = {
        "message": "parameter exclusion deleted",
        "parameter_excludes": {
            "name": "Colour",
            "uid": 1,
            "excluded": [],
            "excluded_by": [],
        },
        "parameter_excluded_by": {
            "name": "Speed",
            "uid": 3,
            "excluded": [],
            "excluded_by": [],
        },
        "parameter_url": f"{api_prefix}/parameters/1",
        "excluded_parameter_url": f"{api_prefix}/parameters/3",
    }
    assert json_dict == expected


def test_parameter_exclusion_delete_404_puid(api_client, api_prefix):
    response = api_client.delete(f"{api_prefix}/parameters/99/exclusions/3")
    assert response.status_code == 404

    json_dict = response.json
    expected = {
        "message": "No parameter with uid '99' was found in the parameter set. You "
        "have requested this URI "
        f"[{api_prefix}/parameters/99/exclusions/3] but did you mean "
        f"{api_prefix}/parameters/<int:uid>/exclusions/ or "
        f"{api_prefix}/parameters/<int:uid>/values/ or "
        f"{api_prefix}/parameterset/ ?"
    }
    assert json_dict == expected


def test_parameter_exclusion_delete_404_euid(api_client, api_prefix):
    response = api_client.delete(f"{api_prefix}/parameters/1/exclusions/99")
    assert response.status_code == 404

    json_dict = response.json
    expected = {
        "message": "No parameter with uid '99' was found in the parameter set. You "
        "have requested this URI "
        f"[{api_prefix}/parameters/1/exclusions/99] but did you mean "
        f"{api_prefix}/parameters/<int:uid>/exclusions/ or "
        f"{api_prefix}/parameters/<int:uid>/values/ or "
        f"{api_prefix}/parameterset/ ?"
    }
    assert json_dict == expected


def test_parameter_exclusion_delete_400_not_excluded(api_client, api_prefix):
    response = api_client.delete(f"{api_prefix}/parameters/1/exclusions/3")
    assert response.status_code == 400

    json_dict = response.json
    expected = {
        "message": "Parameter with uid=3 is not in the exclusion list of parameter with uid=1",
    }
    assert json_dict == expected
