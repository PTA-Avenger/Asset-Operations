def build_prompt(sensor_data: dict) -> str:
    prompt = """
    Analyze the following real-time sensor data for anomalies. List any values that deviate significantly from the norm and explain briefly.

    Temperature: {temperature}
    Vibration: {vibration}
    Pressure: {pressure}

    Return a summary of any anomalies found.
    """.strip().format(
        temperature=sensor_data["temperature"],
        vibration=sensor_data["vibration"],
        pressure=sensor_data["pressure"]
    )
    return prompt
