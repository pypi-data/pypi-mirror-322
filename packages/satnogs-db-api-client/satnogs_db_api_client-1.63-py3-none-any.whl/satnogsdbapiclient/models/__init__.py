# flake8: noqa

# import all models into this package
# if you have many models here with many references from one model to another this may
# raise a RecursionError
# to avoid this, import only the models that you directly need like:
# from from satnogsdbapiclient.model.pet import Pet
# or import this package, but before doing it, use:
# import sys
# sys.setrecursionlimit(n)

from satnogsdbapiclient.model.artifact import Artifact
from satnogsdbapiclient.model.iaru_coordination_enum import IaruCoordinationEnum
from satnogsdbapiclient.model.latest_tle_set import LatestTleSet
from satnogsdbapiclient.model.mode import Mode
from satnogsdbapiclient.model.new_artifact import NewArtifact
from satnogsdbapiclient.model.optical_identification import OpticalIdentification
from satnogsdbapiclient.model.optical_observation import OpticalObservation
from satnogsdbapiclient.model.optical_observation_create import OpticalObservationCreate
from satnogsdbapiclient.model.paginated_artifact_list import PaginatedArtifactList
from satnogsdbapiclient.model.paginated_telemetry_list import PaginatedTelemetryList
from satnogsdbapiclient.model.satellite import Satellite
from satnogsdbapiclient.model.service_enum import ServiceEnum
from satnogsdbapiclient.model.status_enum import StatusEnum
from satnogsdbapiclient.model.telemetry import Telemetry
from satnogsdbapiclient.model.telemetry_request import TelemetryRequest
from satnogsdbapiclient.model.transmitter import Transmitter
from satnogsdbapiclient.model.transmitter_request import TransmitterRequest
from satnogsdbapiclient.model.type_enum import TypeEnum
