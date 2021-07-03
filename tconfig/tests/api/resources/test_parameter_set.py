def test_parameters(api_client, api_prefix):
    url = f"{api_prefix}/parameterset/"
    response = api_client.get(url)
    assert response.status_code == 200

    json_dict = response.json
    expected = {
        "parameter_list_url": f"{api_prefix}/parameters/",
        "parameter_set": {
            "name": None,
            "parameters": [
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
            "position": None,
            "uid": 1,
        },
        "parameter_set_url": f"{api_prefix}/parameterset/",
    }

    assert json_dict == expected
