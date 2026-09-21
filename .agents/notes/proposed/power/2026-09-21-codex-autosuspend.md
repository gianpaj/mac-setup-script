# Codex activity and automatic suspend

## Decision

Use an autosuspend ExternalCommand check against the existing app-server's
Unix WebSocket. Active turns block sleep regardless of their last output time.
New persisted updates and transitions out of active reset the idle timer once.
The prepared configuration uses 900 seconds for the general idle timeout.
Other activity checks retain their thresholds. Polling runs every 30 seconds.

A separate 15-minute busy window would stack with autosuspend's idle timeout,
so the check records a change rather than applying its own grace timer.
Process existence cannot distinguish active work from an idle app-server.
Rollout-file modification times cannot reliably identify a long silent turn.

Live inspection on Codex 0.155.1 found that ephemeral idle threads can report
the current time in thread/read. Only persisted thread/list timestamps count
as updates. All loaded threads are checked for activity, including remote work.
The monitor reads metadata, does not subscribe, and never resumes a thread.
API failures keep the machine awake. Missing sockets mean no work on that daemon.
Separate Codex processes outside the configured daemon are not monitored.

## Verification and rollout

Ten tests passed, including a local Unix WebSocket fixture, pagination, active
remote work, stale timestamps, error handling, and timer-reset behavior.
A live metadata query found this remote session active. No suspend was invoked.
The installer passes bash syntax validation and backs up the live config.

The live /etc/autosuspend.conf still uses 1800 seconds and has no Codex check.
Installation requires interactive sudo authentication unavailable to this agent.
Run ubuntu/install-autosuspend.sh with sudo, then inspect the check and service logs. Keep this
note proposed until the configuration is installed and verified on the host.
