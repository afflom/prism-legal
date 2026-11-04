const assert = require('node:assert/strict');
const test = require('node:test');
const {findVerifiedView} = require('../../tools/ci/find_verified_view.cjs');

function fixture() {
  const context = {repo: {owner: 'owner', repo: 'app'}, sha: 'merged'};
  const pull = {merged_at: '2026-11-04', base: {ref: 'main'}, merge_commit_sha: 'merged',
    head: {sha: 'tested', repo: {full_name: 'owner/app'}}};
  const run = {id: 10, workflow_id: 20, event: 'pull_request', status: 'completed',
    conclusion: 'success', head_sha: 'tested', head_repository: {full_name: 'owner/app'}};
  const artifact = {id: 30, name: 'exact-tree-sdk', expired: false};
  const calls = [];
  const github = {rest: {
    repos: {listPullRequestsAssociatedWithCommit: 'pulls'},
    actions: {getWorkflow: async args => {assert.equal(args.workflow_id, 'ci.yml'); return {data: {id: 20}};},
      listWorkflowRuns: 'runs', listWorkflowRunArtifacts: 'artifacts'},
  }, paginate: async (endpoint, args) => {
    calls.push(endpoint);
    assert.equal(args.owner, 'owner'); assert.equal(args.repo, 'app');
    if (endpoint === 'pulls') {assert.equal(args.commit_sha, 'merged'); return [pull];}
    if (endpoint === 'runs') {assert.equal(args.head_sha, 'tested'); assert.equal(args.status, 'success'); return [run];}
    assert.equal(args.run_id, 10); return [artifact];
  }};
  return {pull, run, artifact, calls, args: {github, context, artifactName: 'exact-tree-sdk'}};
}

test('exact successful same-repository PR artifact is reused', async () => {
  const f = fixture();
  assert.deepEqual(await findVerifiedView(f.args), {runId: 10, artifactId: 30});
  assert.deepEqual(f.calls, ['pulls', 'runs', 'artifacts']);
});

test('unmerged, unrelated and fork pull requests cannot supply a release', async () => {
  for (const mutate of [f => f.pull.merged_at = null, f => f.pull.base.ref = 'other',
    f => f.pull.merge_commit_sha = 'other', f => f.pull.head.repo.full_name = 'fork/app',
    f => f.pull.head.repo = null]) {
    const f = fixture(); mutate(f);
    assert.equal(await findVerifiedView(f.args), null);
    assert.deepEqual(f.calls, ['pulls']);
  }
});

test('failed, incomplete, wrong-source or wrong-workflow runs cannot supply a release', async () => {
  for (const mutate of [f => f.run.conclusion = 'failure', f => f.run.status = 'in_progress',
    f => f.run.head_sha = 'other', f => f.run.workflow_id = 21,
    f => f.run.event = 'workflow_dispatch', f => f.run.head_repository.full_name = 'fork/app']) {
    const f = fixture(); mutate(f);
    assert.equal(await findVerifiedView(f.args), null);
    assert.deepEqual(f.calls, ['pulls', 'runs']);
  }
});

test('changed-tree and expired artifacts fall back to full verification', async () => {
  for (const mutate of [f => f.artifact.name = 'different-tree-sdk', f => f.artifact.expired = true]) {
    const f = fixture(); mutate(f);
    assert.equal(await findVerifiedView(f.args), null);
  }
});

test('direct pushes use full verification; API failures are not success', async () => {
  const f = fixture();
  f.args.github.paginate = async () => [];
  assert.equal(await findVerifiedView(f.args), null);
  f.args.github.paginate = async () => {throw Error('API unavailable');};
  await assert.rejects(findVerifiedView(f.args), /API unavailable/);
});
