# SLA Tracking Specification

## Purpose

Defines the core incident lifecycle, auditable SLA pause windows, and SLA target resolution calculation for `GuardiaCloud.Sla.Api`.

## Requirements

### Requirement: Incident Creation and Target SLA Assignment
The system SHALL create operational incidents associated with a `TenantId`, `Title`, and `IncidentPriority`, assigning the target resolution window based on priority (`CriticalP1` = 60 minutes, `HighP2` = 240 minutes, `StandardP3` = 1440 minutes).

#### Scenario: Create a Critical P1 incident
- **WHEN** a client sends `POST /api/incidents` with a valid `TenantId`, `Title`, and `Priority = CriticalP1`
- **THEN** the system creates the incident in `Open` status and sets `TargetResolutionMinutes` to `60`

### Requirement: Active SLA Evaluation
The system SHALL calculate `ElapsedActiveMinutes`, `TotalPausedMinutes`, `RemainingPauseBudgetMinutes`, `RemainingMinutes`, `EffectiveDeadlineUtc`, and `IsBreached` via `GET /api/incidents/{id}/sla`, freezing the clock at `ResolvedAtUtc` when the incident status is `Resolved` and capping credited pause time on `CriticalP1` incidents at 30 minutes unless a `SupervisorOverrideCode` is present.

#### Scenario: Query SLA for an open incident within target window
- **WHEN** 25 minutes have elapsed since `OpenedAtUtc` on a `CriticalP1` incident
- **THEN** `ElapsedActiveMinutes` is `25`, `RemainingMinutes` is `35`, and `IsBreached` is `false`

#### Scenario: Critical P1 pause exceeds 30-minute standard budget without supervisor override
- **WHEN** a `CriticalP1` incident is paused for 45 minutes without a `SupervisorOverrideCode` after 10 minutes of active work
- **THEN** `TotalPausedMinutes` is capped at `30`, `RemainingPauseBudgetMinutes` is `0`, and `ElapsedActiveMinutes` includes the 15 uncredited minutes (`25` minutes total)

### Requirement: Auditable SLA Pause and Resume Windows
The system SHALL allow operators to pause and resume the SLA clock with mandatory audit evidence (`Reason`, `RequestedBy`, `EvidenceNote`, `ResumedBy`), rejecting invalid state transitions with HTTP `409 Conflict`.

#### Scenario: Pause and resume an incident waiting for customer logs
- **WHEN** an operator pauses a `HighP2` incident for 90 minutes with valid audit fields and then resumes it
- **THEN** the 90 paused minutes are excluded from `ElapsedActiveMinutes` and added to `EffectiveDeadlineUtc`

### Requirement: Critical P1 Pause Budget Enforcement
The system SHALL reject new pause requests on `CriticalP1` incidents with HTTP `422 Unprocessable Entity` once cumulative pauses reach or exceed 30 minutes, unless a non-empty `SupervisorOverrideCode` is provided.

#### Scenario: Reject second pause on Critical P1 when 30-minute budget is exhausted
- **WHEN** a `CriticalP1` incident has already accumulated 30 minutes of pause and a client sends `POST /api/incidents/{id}/sla/pause` without `SupervisorOverrideCode`
- **THEN** the system responds with HTTP `422 Unprocessable Entity` (`application/problem+json`)

#### Scenario: Allow pause with SupervisorOverrideCode after budget exhaustion
- **WHEN** a `CriticalP1` incident has accumulated 30 minutes of pause and a client sends `POST /api/incidents/{id}/sla/pause` with `SupervisorOverrideCode = "SUP-2026-OK"`
- **THEN** the system responds with HTTP `200 OK` and transitions the incident to `WaitingForCustomer`
