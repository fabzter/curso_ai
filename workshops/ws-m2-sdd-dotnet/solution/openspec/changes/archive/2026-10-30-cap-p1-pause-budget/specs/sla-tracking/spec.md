# Spec Delta: `sla-tracking` (`cap-p1-pause-budget`)

## MODIFIED Requirements

### Requirement: Active SLA Evaluation
The system SHALL calculate `ElapsedActiveMinutes`, `TotalPausedMinutes`, `RemainingPauseBudgetMinutes`, `RemainingMinutes`, `EffectiveDeadlineUtc`, and `IsBreached` via `GET /api/incidents/{id}/sla`, freezing the clock at `ResolvedAtUtc` when the incident status is `Resolved` and capping credited pause time on `CriticalP1` incidents at 30 minutes unless a `SupervisorOverrideCode` is present.

#### Scenario: Critical P1 pause exceeds 30-minute standard budget without supervisor override
- **WHEN** a `CriticalP1` incident is paused for 45 minutes without a `SupervisorOverrideCode` after 10 minutes of active work
- **THEN** `TotalPausedMinutes` is capped at `30`, `RemainingPauseBudgetMinutes` is `0`, and `ElapsedActiveMinutes` includes the 15 uncredited minutes (`25` minutes total)

## ADDED Requirements

### Requirement: Critical P1 Pause Budget Enforcement
The system SHALL reject new pause requests on `CriticalP1` incidents with HTTP `422 Unprocessable Entity` once cumulative pauses reach or exceed 30 minutes, unless a non-empty `SupervisorOverrideCode` is provided.

#### Scenario: Reject second pause on Critical P1 when 30-minute budget is exhausted
- **WHEN** a `CriticalP1` incident has already accumulated 30 minutes of pause and a client sends `POST /api/incidents/{id}/sla/pause` without `SupervisorOverrideCode`
- **THEN** the system responds with HTTP `422 Unprocessable Entity` (`application/problem+json`)

#### Scenario: Allow pause with SupervisorOverrideCode after budget exhaustion
- **WHEN** a `CriticalP1` incident has accumulated 30 minutes of pause and a client sends `POST /api/incidents/{id}/sla/pause` with `SupervisorOverrideCode = "SUP-2026-OK"`
- **THEN** the system responds with HTTP `200 OK` and transitions the incident to `WaitingForCustomer`
