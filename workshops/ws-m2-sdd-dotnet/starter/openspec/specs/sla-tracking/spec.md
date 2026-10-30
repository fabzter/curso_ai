# SLA Tracking Specification

## Purpose

Defines the core incident lifecycle and SLA target resolution calculation for `GuardiaCloud.Sla.Api`.

## Requirements

### Requirement: Incident Creation and Target SLA Assignment
The system SHALL create operational incidents associated with a `TenantId`, `Title`, and `IncidentPriority`, assigning the target resolution window based on priority (`CriticalP1` = 60 minutes, `HighP2` = 240 minutes, `StandardP3` = 1440 minutes).

#### Scenario: Create a Critical P1 incident
- **WHEN** a client sends `POST /api/incidents` with a valid `TenantId`, `Title`, and `Priority = CriticalP1`
- **THEN** the system creates the incident in `Open` status and sets `TargetResolutionMinutes` to `60`

### Requirement: Active SLA Evaluation
The system SHALL calculate `ElapsedActiveMinutes`, `RemainingMinutes`, `EffectiveDeadlineUtc`, and `IsBreached` via `GET /api/incidents/{id}/sla`.

#### Scenario: Query SLA for an open incident within target window
- **WHEN** 25 minutes have elapsed since `OpenedAtUtc` on a `CriticalP1` incident
- **THEN** `ElapsedActiveMinutes` is `25`, `RemainingMinutes` is `35`, and `IsBreached` is `false`
