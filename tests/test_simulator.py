"""
Unit tests for IoT Telemetry Generator & Fleet Simulator
"""

from simulator.iot_simulator import IoTTelemetryFleet, ContainerSimulator
from simulator.config import ROUTES, COMMODITIES


def test_container_simulator_step():
    sim = ContainerSimulator("CONT-99", "SHP-001", ROUTES[0], "Avocados")
    telemetry = sim.step()

    assert telemetry["container_id"] == "CONT-99"
    assert telemetry["commodity"] == "Avocados"
    assert isinstance(telemetry["temperature"], float)
    assert isinstance(telemetry["humidity"], float)
    assert -90.0 <= telemetry["latitude"] <= 90.0
    assert -180.0 <= telemetry["longitude"] <= 180.0
    assert telemetry["battery"] > 0.0


def test_fleet_simulator_snapshot():
    fleet = IoTTelemetryFleet(fleet_size=10)
    snapshot = fleet.generate_fleet_snapshot()
    assert len(snapshot) == 10
    assert snapshot[0]["container_id"] == "CONT-1001"
