// GitHub Actions orchestration only. Reuse is limited to successful same-repo
// PR CI associated with this merged commit and an exact tree/SDK artifact name.
async function findVerifiedView({github, context, artifactName}) {
  const {owner, repo} = context.repo;
  const workflow = (await github.rest.actions.getWorkflow({owner, repo, workflow_id: 'ci.yml'})).data;
  const pulls = await github.paginate(github.rest.repos.listPullRequestsAssociatedWithCommit,
    {owner, repo, commit_sha: context.sha, per_page: 100});
  for (const pr of pulls) {
    if (!pr.merged_at || pr.base.ref !== 'main' || pr.merge_commit_sha !== context.sha ||
        pr.head.repo?.full_name !== `${owner}/${repo}`) continue;
    // Paginate: an expired recent attempt must not hide an available successful one.
    const runs = await github.paginate(github.rest.actions.listWorkflowRuns, {
      owner, repo, workflow_id: workflow.id, head_sha: pr.head.sha,
      event: 'pull_request', status: 'success', per_page: 100,
    });
    for (const run of runs) {
      if (run.workflow_id !== workflow.id || run.event !== 'pull_request' ||
          run.status !== 'completed' || run.conclusion !== 'success' ||
          run.head_sha !== pr.head.sha || run.head_repository?.full_name !== `${owner}/${repo}`) continue;
      const artifacts = await github.paginate(github.rest.actions.listWorkflowRunArtifacts,
        {owner, repo, run_id: run.id, per_page: 100});
      const artifact = artifacts.find(item => item.name === artifactName && !item.expired);
      if (artifact) return {runId: run.id, artifactId: artifact.id};
    }
  }
  return null; // Direct pushes, changed merge trees and misses use full verification.
}
module.exports = {findVerifiedView};
