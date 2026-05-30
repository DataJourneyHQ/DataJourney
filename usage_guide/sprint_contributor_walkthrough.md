# DataJourney Sprint Contributor Walkthrough

Use this as the short contributor path during a sprint. The goal is to get everyone into a working environment, run the discovery CLI, and make a small useful contribution.

## 1. Get Set Up

Install Git and Pixi, then fork or clone the repository:

```shell
git clone https://github.com/DataJourneyHQ/DataJourney.git
cd DataJourney
```

Create the Pixi environment and install DataJourney locally:

```shell
pixi run DJ_package
```

Smoke-test the contributor-facing CLI:

```shell
pixi run DJ_list
pixi run DJ_explain
pixi run DJ_explain DJ_RAG_without_memory
pixi run DJ_explain --category RAG
pixi run datajourney explain --validate
```

For model-backed workflows only, export the needed credentials first. For GitHub Models:

```shell
export GITHUB_TOKEN="your-token"
pixi run GIT_TOKEN_CHECK
```

## 2. Read The Contributor Notes

Before choosing work, open these links:

- [Contributor guidelines](../CONTRIBUTING.md)
- [Contribution Guidelines (AI-Aware)](<https://github.com/DataJourneyHQ/DataJourney/wiki/Contribution-Guidelines-(AI%E2%80%90Aware)>)
- [Contribute to DataJourney](https://github.com/DataJourneyHQ/DataJourney/wiki/Contribute-to-DataJourney)
- [Open DataJourney issues](https://github.com/DataJourneyHQ/DataJourney/issues)
- [Good first issues](https://github.com/DataJourneyHQ/DataJourney/issues?q=is%3Aissue%20state%3Aopen%20label%3A%22good%20first%20issue%22)

If the good-first-issue queue is empty, pick a small docs or workflow-catalog improvement and mention in the PR that it came from the sprint.

## 3. Pick A First Contribution

The easiest first contribution is improving the explanation layer:

- Open `analytics_framework/workflows/workflow_catalog.json`.
- Pick one workflow from `pixi run DJ_list`.
- Improve the prerequisites, expected output, common errors, next steps, or related files.
- Run `pixi run datajourney explain --validate`.
- Run `pixi run DJ_explain WORKFLOW_NAME` to inspect your change in the CLI.

Good starter areas:

- Clarify what credentials a workflow needs.
- Add common errors and fixes from your setup experience.
- Improve expected output so users know what success looks like.
- Connect a workflow to a useful next step.

## 4. Submit The Change

Create a branch, commit the small improvement, and open a pull request:

```shell
git checkout -b docs/improve-workflow-explanation
git status
git add analytics_framework/workflows/workflow_catalog.json
git commit -m "Improve workflow explanation"
git push origin docs/improve-workflow-explanation
```

In the pull request, include the workflow you changed and the validation command you ran.

## Sprint Maintainer Preflight

Before sharing this walkthrough, confirm the current branch includes `analytics_framework/workflows/`, the workflow catalog is valid JSON, and the README setup commands match the smoke-test commands above.
