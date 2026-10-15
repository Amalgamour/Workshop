"""Build the proposal's data and isolated demonstration. Not a kernel installer."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent


def save(name, value):
    path = ROOT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


def command(purpose, requires, hold, basis):
    return dict(purpose=purpose, requires=requires, hold=hold, basis=basis)


commands = {
    'point': command(
        'Request an exact source/section relationship or a correction to that relationship.',
        ['relationship', 'proposed_destination', 'local_difference'],
        'Do not copy the governing body, invent a missing source, or treat routing as permission to change a seat.',
        'Proposal informed by 05.09 and law 0033.point (signed test, not authority to execute).'),
    'note': command(
        'Request preservation of a specific explanation, uncertainty, or Director decision.',
        ['record_text', 'record_destination', 'reason_to_preserve'],
        'Preserve history; a note does not approve a draft or release another item.',
        'Proposal informed by face 06 and 05.08/05.09 usage; placement/append mechanic still needs law.'),
    'redraft': command(
        'Request a coherent replacement draft from named current material and decisions.',
        ['input_faces', 'decisions', 'output_plan', 'preserve', 'alignment_checks'],
        'No seat replacement, signature, approval, or lock. Read named predecessors and governing sources first.',
        'Law 0021.write Order/Name and 05.09. Unsigned amendment versus a new version is stated in output_plan.'),
    'fix': command(
        'Request a bounded correction to a demonstrated defect.',
        ['defect', 'desired_behavior', 'output_plan', 'verification'],
        'Not a general redesign; name patch versus draft and its authority before acting.',
        'Law 0021.write Fix. Current local dev exceptions must be reopened, not inferred from this contract.'),
    'patch': command(
        'Request a small dated change where an explicit current rule allows that edit.',
        ['exact_change', 'patch_basis', 'verification'],
        'No broad rewrite. A stated patch_basis is a claim to review, not verified authorization.',
        'Law 0021.write Patch and current dev exceptions; prototype does not choose between conflicting policies.'),
    'check': command(
        'Request inspection against named criteria and a report of the differences.',
        ['criteria', 'inspection_scope', 'report_destination'],
        'Read-only inspection. No automatic correction or approval.',
        'Proposal inspection contract; checker README is mechanics, not a grant of permission.'),
    'strike': command(
        'Request marking an exact obsolete sentence while preserving the record.',
        ['exact_sentence', 'reason_obsolete', 'replacement_reference'],
        'No deletion of history; do not expand a strike into a rewrite.',
        'Law 0026.strike Job.'),
    'sign': command(
        'Request a signature decision for explicitly identified draft files.',
        ['draft_files', 'readiness_evidence', 'requested_actor'],
        'No signing by this tool. Signature does not seat or approve. Assigned role requires current governing authority.',
        'Law 0021.write Name and current axioms Hats/Marks. Repository AGENTS prohibits this worker signing.'),
    'approve': command(
        'Request the Director approval decision for named signed drafts and their transition plan.',
        ['signed_files', 'readiness_evidence', 'transition_plan', 'requested_actor'],
        'No approval or renames by this tool. No inferred approval from a reply or signature.',
        'Law 0022.approve Seat/Halt; Director decision.'),
    'clean': command(
        'Request a bounded cleanup review with recoverable evidence and named exclusions.',
        ['snapshot', 'cleanup_scope', 'preserve', 'open_work_check'],
        'No deletion or cleanup by this tool; no snapshot means no clean; open higher drafts require a hold.',
        'Law 0025.clean Snapshot/Open/Notes.'),
}
save('commands.json', {'status': 'proposal', 'revision': '0.1',
    'boundary': 'These are request-construction contracts. They do not replace behavior law or execute verbs.',
    'common_requires': ['id', 'title', 'command', 'issue', 'recommend', 'ask', 'target', 'scale', 'sources', 'done'],
    'commands': commands})

demo = ROOT / 'example-project'
page = demo / '10.demo/10.work/10.lib/1001.jobs'
page.mkdir(parents=True, exist_ok=True)
(page.parent / '00.md').write_text('# Demonstration book\nNot a live Librarian desk.\n', encoding='utf-8')
(demo / 'source.md').write_text('# Evidence\n\n## Routing\nThe demonstration points to source.md, section Routing.\n\n## Record\nPreserve the why beside the decision.\n', encoding='utf-8')
save('routing.example.json', {'status': 'proposal', 'routes': [{
    'book': '10.demo/10.work/10.lib', 'jobs_page': '1001.jobs',
    'work_min': 1001, 'work_max': 1999,
    'routing_basis': 'Isolated demonstration only. Director must choose the live book job page and allocation policy.'}]})
save('request.example.json', {
    'who': 'example-worker', 'why': 'Make the request reviewable before a model acts.',
    'cite': '2.8', 'overview': 'Two demonstration requests; neither is released or executed.',
    'items': [
        {'id': 1, 'title': 'Decide the source pointer.', 'command': 'point',
         'issue': 'The route needs an exact section, rather than a remembered description.',
         'recommend': 'Point to the existing Routing section.',
         'ask': 'Confirm the exact destination for the proposed pointer.',
         'target': 'source.md', 'scale': 3,
         'sources': [{'path': 'source.md', 'section': 'Routing'}],
         'parameters': {'relationship': 'Example destination owns the routing explanation.',
                        'proposed_destination': 'source.md — section Routing',
                        'local_difference': 'Only the pointer is proposed; do not duplicate the source body.'},
         'done': 'After a Director decision, the resulting pointer resolves to Routing; this batch alone changes no pointer.'},
        {'id': 2, 'title': 'Preserve the routing decision.', 'command': 'note',
         'issue': 'A future worker needs the reason for the selected pointer.',
         'recommend': 'Keep the Director decision and its why in the eventual designated record.',
         'ask': 'Confirm the proposed note and preservation destination.',
         'target': 'source.md', 'scale': 4, 'depends_on': [1],
         'sources': [{'path': 'source.md', 'section': 'Record'}],
         'parameters': {'record_text': 'Proposed note: the exact source remains authoritative; the local page points.',
                        'record_destination': 'source.md — section Record (demo only; append mechanic requires a later release).',
                        'reason_to_preserve': 'Retain the reasoning, not merely a completed checkbox.'},
         'done': 'The Director confirms the destination and decision to preserve; record creation is a later released act.'}
    ]})
print('Built commands, routing and request examples; no live files touched.')
