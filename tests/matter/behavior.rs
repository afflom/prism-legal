use prism_legal_matter::*;

fn node(id: u64, dependencies: &[u64]) -> Node {
    Node {
        id, revision: 1, facet: "Event".into(), value: "notice received".into(),
        origin: if dependencies.is_empty() { Origin::Reviewed } else { Origin::Inferred },
        accepted: true, citations: vec![],
        dependencies: dependencies.iter().map(|id| Reference { id: *id, revision: 1 }).collect(),
    }
}

fn chain() -> State {
    State { revision: 7, sources: vec![],
        nodes: vec![node(3, &[2]), node(2, &[1]), node(1, &[]), node(4, &[])], changes: vec![] }
}

#[test]
fn edit_retains_history_and_invalidates_only_dependent_context() {
    let original = chain();
    assert_eq!(current(&original.nodes, &[]).unwrap().references.len(), 4);
    let revised = commitEdit(&original, 7, Reference { id: 1, revision: 1 },
        "Notice".into(), "receipt is disputed".into(), true).unwrap().unwrap();
    assert_eq!(revised.revision, 8);
    assert_eq!(revised.changes.len(), 1);
    assert_eq!(revised.changes[0].before, original.nodes[2]);
    assert_eq!(revised.changes[0].after.value, "receipt is disputed");
    let admitted = current(&revised.nodes, &[]).unwrap().references;
    assert_eq!(admitted, vec![Reference { id: 1, revision: 2 }, Reference { id: 4, revision: 1 }]);
    assert_eq!(original.nodes[2].revision, 1, "the prior snapshot must remain intact");
    let next = commitEdit(&revised, 8, Reference { id: 4, revision: 1 },
        "Goal".into(), "resolve the dispute".into(), true).unwrap().unwrap();
    assert_eq!(next.changes.len(), 2);
    assert_eq!(next.changes[1], revised.changes[0]);
}

#[test]
fn stale_matter_and_node_edits_are_rejected_without_losing_context() {
    let original = chain();
    for (matter_revision, node_revision) in [(6, 1), (7, 0), (8, 1)] {
        assert!(commitEdit(&original, matter_revision, Reference { id: 1, revision: node_revision },
            "Event".into(), "stale input".into(), true).unwrap().is_none());
    }
    assert_eq!(original.revision, 7);
    assert!(original.changes.is_empty());
}

#[test]
fn changed_source_bytes_and_revisions_invalidate_the_whole_dependency_chain() {
    let source = Source { id: 8, revision: 1, content: "Zoë: no notice".as_bytes().to_vec() };
    let citation = Citation { source: 8, revision: 1, start: 0,
        size: source.content.len() as u64, quote: source.content.clone() };
    assert!(matchesSource(&source, &citation));
    let mut quoted = node(1, &[]);
    quoted.origin = Origin::Extracted;
    quoted.citations.push(citation.clone());
    let nodes = vec![node(3, &[2]), node(2, &[1]), quoted, node(4, &[])];
    assert_eq!(current(&nodes, &[source.clone()]).unwrap().references.len(), 4);
    for changed in [Source { content: b"notice admitted".to_vec(), ..source.clone() },
        Source { revision: 2, ..source.clone() }] {
        assert_eq!(current(&nodes, &[changed]).unwrap().references,
            vec![Reference { id: 4, revision: 1 }]);
    }
    for forged in [Citation { start: u64::MAX, ..citation.clone() },
        Citation { size: 0, ..citation.clone() }, Citation { quote: b"notice admitted".to_vec(), ..citation }] {
        assert!(!matchesSource(&source, &forged));
    }
    assert!(current(&nodes, &[source.clone(), source]).unwrap().references.is_empty());
}

#[test]
fn missing_unreviewed_and_circular_support_never_establish_a_conclusion() {
    for nodes in [vec![node(1, &[1])], vec![node(1, &[2]), node(2, &[1])],
        vec![node(1, &[99])], vec![node(1, &[]), node(1, &[])]] {
        assert!(current(&nodes, &[]).unwrap().references.is_empty());
    }
    let mut premise = node(1, &[]);
    premise.accepted = false;
    assert!(current(&[premise, node(2, &[1])], &[]).unwrap().references.is_empty());
}

#[test]
fn conflicting_attention_abstains_and_repetition_does_not_inflate_evidence() {
    let mut first = node(1, &[]);
    first.facet = "Notice".into();
    let mut second = node(2, &[]);
    second.facet = "Evidence".into();
    let tokens = words("notice received".into());
    let attention = attend(&tokens.values, &[first, second], &emptyAttention()).unwrap();
    assert!(attention.ambiguous);
    assert_eq!(inferredFacet(&attention), "Unassigned");
    assert_eq!(words("notice notice notice".into()).values, vec!["notice"]);
    assert_eq!(inferredFacet(&attend(&tokens.values, &[], &emptyAttention()).unwrap()), "Unassigned");
}

#[test]
fn bounded_rust_revision_overflow_is_an_error_not_a_wrapped_revision() {
    let mut state = chain();
    state.revision = u64::MAX;
    assert_eq!(commitEdit(&state, u64::MAX, Reference { id: 1, revision: 1 },
        "Event".into(), "correction".into(), true), Err(ComputeError::AddOverflow));
}
