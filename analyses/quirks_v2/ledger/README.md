# Job ledger

- `jobs.tsv`: one line per job: job id, campaign, mechanism (argo/ssh), node, status, CPU time, max RSS, output
  sha256, bytes. Written by the runner (built by the Phase-1 feasibility executor).
- `markers/`: one marker per output file, written only after the atomic rename on cajuela. A file without a marker
  does not exist for the analysis.
