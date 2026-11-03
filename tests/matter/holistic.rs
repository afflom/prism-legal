use prism_legal_matter::*;

fn accepted(outcome: Outcome) -> Session {
    assert_eq!(outcome.code, "");
    outcome.session
}
fn assert_fact(session: &Session, facet: &str, value: &str) -> Session {
    accepted(recordAssertion(session, session.matter.revision, Role::Client,
        "client".into(), facet.into(), value.into()).unwrap())
}
fn node_ref(session: &Session, facet: &str) -> Reference {
    nodeReference(session.matter.nodes.iter().find(|n| n.facet == facet).unwrap())
}
fn reviewed_matter() -> Session {
    let s = initial("Notice dispute".into());
    let s = accepted(ingest(&s, 0, Role::Client, "client".into(), "Notice".into(),
        b"notice received\nnotice disputed".to_vec()).unwrap());
    let s = accepted(review(&s, 1, Role::Client, "client".into(), Reference {id:1,revision:1},
        "notice.receipt".into(), "received".into(), true).unwrap());
    let s = assert_fact(&s, "goal", "resolve the dispute");
    let s = assert_fact(&s, "jurisdiction", "reviewed jurisdiction");
    let s = accepted(ingest(&s, s.matter.revision, Role::Lawyer, "lawyer".into(),
        "Governing source".into(), b"A received notice permits a response unless withdrawn.".to_vec()).unwrap());
    let latest=s.matter.nodes.iter().max_by_key(|n|n.id).unwrap();
    let s = accepted(review(&s, s.matter.revision, Role::Lawyer, "lawyer".into(),
        nodeReference(latest), "authority".into(), "Reviewable notice provision".into(), true).unwrap());
    let rule=Rule {definition:Reference{id:0,revision:0}, authority:node_ref(&s,"authority"),
        jurisdiction:node_ref(&s,"jurisdiction"), goal:node_ref(&s,"goal"),
        premises:vec![Requirement{facet:"notice.receipt".into(),value:"received".into(),question:"Was the notice received?".into()}],
        exceptions:vec![Requirement{facet:"notice.withdrawal".into(),value:"withdrawn".into(),question:"Was the notice withdrawn?".into()}],
        conclusionFacet:"response.available".into(),conclusionValue:"response may be prepared".into(),action:"Prepare a response grounded in the notice.".into()};
    accepted(commitRule(&s,s.matter.revision,Role::Lawyer,"lawyer".into(),&rule).unwrap())
}
#[test]
fn multiple_resources_keep_exact_identity_and_old_source_versions() {
    let s=reviewed_matter();
    assert_eq!(s.matter.sources.len(),2);
    assert!(distinctNodes(&s.matter.nodes));
    assert!(distinctSources(&s.matter.sources));
    let old=s.matter.sources.iter().find(|s|s.id==1).unwrap().clone();
    let updated=accepted(reviseSource(&s,s.matter.revision,Role::Client,"client".into(),
        Reference{id:1,revision:1},b"notice never received".to_vec()).unwrap());
    assert_eq!(updated.sourceHistory,vec![old]);
    assert!(!current(&updated.matter.nodes,&updated.matter.sources).unwrap().references.contains(&Reference{id:1,revision:2}));
    let stale=reviseSource(&updated,updated.matter.revision,Role::Client,"client".into(),
        Reference{id:1,revision:1},b"stale".to_vec()).unwrap();
    assert_eq!(stale.code,"source-conflict");assert_eq!(stale.session,updated);
}
#[test]
fn authority_and_rule_content_are_bound_to_review_and_exact_dependencies() {
    let s=reviewed_matter(); let rule=&s.rules[0];
    let a=assess(rule,&s.matter.nodes,&s.matter.sources).unwrap();
    assert_eq!(a.status,ReasoningStatus::Supported);assert_eq!(a.dependencies.len(),5);
    let mut forged=rule.clone();forged.conclusionValue="unreviewed substitution".into();
    assert_eq!(assess(&forged,&s.matter.nodes,&s.matter.sources).unwrap().status,ReasoningStatus::Inactive);
    assert_eq!(commitRule(&s,s.matter.revision,Role::Client,"client".into(),&forged).unwrap().session,s);
    let next=accepted(propose(&s,s.matter.revision,Role::Lawyer,"lawyer".into(),rule.definition).unwrap());
    let candidate=next.matter.nodes.iter().max_by_key(|n|n.id).unwrap();
    assert!(!candidate.accepted);assert_eq!(candidate.dependencies,a.dependencies);
}
#[test]
fn a_new_exception_retracts_previously_accepted_reasoning() {
    let s=reviewed_matter();
    let s=accepted(propose(&s,s.matter.revision,Role::Lawyer,"lawyer".into(),s.rules[0].definition).unwrap());
    let candidate=s.matter.nodes.iter().max_by_key(|n|n.id).unwrap().clone();
    let denied=review(&s,s.matter.revision,Role::Client,"client".into(),nodeReference(&candidate),candidate.facet.clone(),candidate.value.clone(),true).unwrap();
    assert_eq!(denied.code,"lawyer-review-required");
    let s=accepted(review(&s,s.matter.revision,Role::Lawyer,"lawyer".into(),nodeReference(&candidate),candidate.facet,candidate.value,true).unwrap());
    assert!(current(&s.matter.nodes,&s.matter.sources).unwrap().references.contains(&Reference{id:candidate.id,revision:2}));
    let changed=assert_fact(&s,"notice.withdrawal","withdrawn");
    assert_eq!(assess(&changed.rules[0],&changed.matter.nodes,&changed.matter.sources).unwrap().status,ReasoningStatus::Excepted);
    let retracted=changed.matter.nodes.iter().find(|n|n.id==candidate.id).unwrap();
    assert!(!retracted.accepted);assert_eq!(retracted.revision,3);
    assert_eq!(retracted.citations,candidate.citations);
    assert!(changed.matter.changes.iter().any(|c|c.before.id==candidate.id && c.before.accepted && !c.after.accepted));
}
#[test]
fn learned_network_has_no_seeded_labels_and_discards_stale_training() {
    let empty=train(&[],&[]).unwrap(); assert_eq!(suggestedFacet(&infer(&empty,"notice received".into()).unwrap()),"");
    let mut s=initial("Learning".into());
    s=assert_fact(&s,"receipt","NOTICE RECEIVED");
    s=assert_fact(&s,"dispute","notice disputed");
    let model=train(&s.matter.nodes,&s.matter.sources).unwrap();
    assert_eq!(suggestedFacet(&infer(&model,"notice received".into()).unwrap()),"receipt");
    assert_eq!(suggestedFacet(&infer(&model,"notice".into()).unwrap()),"");
    assert_eq!(model.neurons.len(),2);
    let original=node_ref(&s,"receipt");
    let corrected=accepted(review(&s,s.matter.revision,Role::Client,"client".into(),original,
        "receipt".into(),"payment completed".into(),true).unwrap());
    let retrained=train(&corrected.matter.nodes,&corrected.matter.sources).unwrap();
    assert_ne!(suggestedFacet(&infer(&retrained,"notice received".into()).unwrap()),"receipt");
    assert_eq!(features("not received".into()).unwrap().values.len(),3);
    assert_ne!(features("not received".into()).unwrap(),features("received not".into()).unwrap());
}
#[test]
fn reader_and_conflicting_commands_leave_the_complete_session_unchanged() {
    let s=reviewed_matter();
    for (revision,role) in [(s.matter.revision-1,Role::Client),(s.matter.revision,Role::Reader)] {
        let rejected=recordAssertion(&s,revision,role,"reader".into(),"goal".into(),"overwrite".into()).unwrap();
        assert_eq!(rejected.session,s);assert!(!rejected.code.is_empty());
    }
    let rejected=recordAssertion(&s,s.matter.revision,Role::Client,"client".into(),"authority".into(),"invented source".into()).unwrap();
    assert_eq!(rejected.session,s);
}

#[test]
fn journal_replay_is_exact_and_failed_transactions_do_not_advance_it() {
    let journal=initialJournal("Unicode Zoë".into());
    let command=encodeJournalFields(&vec!["ingest".into(),"0".into(),"client".into(),"client".into(),"Source".into(),"Zoë: notice\nline two\u{001f}raw\0bytes".into()]);
    let applied=transact(journal.clone(),command.clone()).unwrap();
    assert_eq!(applied.code,"");
    let replayed=replay(applied.journal.clone()).unwrap();assert_eq!(replayed.code,"");assert_eq!(replayed.session,applied.session);
    assert_eq!(replayed.session.matter.sources[0].content,"Zoë: notice\nline two\u{001f}raw\0bytes".as_bytes());
    let stale=transact(applied.journal.clone(),command).unwrap();
    assert!(!stale.code.is_empty());assert_eq!(stale.journal,applied.journal);assert_eq!(stale.session,applied.session);
    let corrupt=replay(format!("{}1:x",applied.journal)).unwrap();
    assert!(!corrupt.code.is_empty());assert_eq!(corrupt.session.matter.revision,0);assert!(corrupt.session.matter.sources.is_empty());
    for malformed in ["01:a","2:ëx","1:ë","1:xgarbage","4294967296:x"] {
        assert!(decodeJournalFields(malformed.into(),32).unwrap().is_none(),"{malformed}");
    }
}
#[test]
fn focused_journey_and_draft_follow_the_current_matter() {
    let blank=initial("".into());assert_eq!(overview(&blank,Role::Client).unwrap().stage,"intake");
    let s=reviewed_matter();let rule=s.rules[0].definition.id;
    let view=select(&s,Role::Lawyer,0,rule).unwrap();assert_eq!(view.stage,"strategy");
    assert_eq!(view.explanation,"Prepare a response grounded in the notice.");
    let draft=goalDraft(&s,rule).unwrap().unwrap();assert!(draftCurrent(&draft,&s).unwrap());
    assert!(draft.body.contains("A received notice permits a response unless withdrawn."));
    let changed=assert_fact(&s,"notice.withdrawal","withdrawn");assert!(!draftCurrent(&draft,&changed).unwrap());
    assert_eq!(select(&changed,Role::Lawyer,0,rule).unwrap().stage,"exception");
}

#[test]
fn ambiguous_rule_actions_never_select_an_arbitrary_rule() {
    let session = reviewed_matter();
    let rule = session.rules[0].clone();
    assert!(selectedRule(&vec![rule.clone(); 3], rule.action.clone()).unwrap().is_none());
    assert!(selectedRule(&vec![rule.clone(); 2], "".into()).unwrap().is_none());
    assert_eq!(selectedRule(&vec![rule.clone()], "".into()).unwrap(), Some(rule));
}

#[test]
fn lawyer_cannot_reaccept_a_conclusion_after_an_observed_exception() {
    let session = reviewed_matter();
    let rule = session.rules[0].definition.clone();
    let session = accepted(propose(&session, session.matter.revision, Role::Lawyer, "lawyer".into(), rule).unwrap());
    let conclusion = session.matter.nodes.iter().find(|n| n.facet == "response.available").unwrap().clone();
    let session = assert_fact(&session, "notice.withdrawal", "withdrawn");
    let refused = review(&session, session.matter.revision, Role::Lawyer, "lawyer".into(),
        nodeReference(&conclusion), conclusion.facet, conclusion.value, true).unwrap();
    assert_eq!(refused.code, "support-is-stale");
    assert_eq!(refused.session, session);
}

#[test]
fn reviewed_source_language_extracts_new_values_without_inventing_labels() {
    let s = accepted(ingest(&initial("Payment".into()), 0, Role::Client, "client".into(),
        "Receipt".into(), b"Payment: 50 USD.\nPayment: 75 USD.".to_vec()).unwrap());
    let s = accepted(review(&s, s.matter.revision, Role::Client, "client".into(),
        Reference { id: 1, revision: 1 }, "payment.amount".into(), "50".into(), true).unwrap());
    let learned = inferMeaning(&s.matter.nodes, &s.matter.sources, "Payment: 75 USD.".into()).unwrap();
    assert!(usableMeaning(&learned));
    assert_eq!((learned.facet.as_str(), learned.value.as_str()), ("payment.amount", "75"));
    assert_eq!(learned.examples, vec![Reference { id: 1, revision: 2 }]);
    let network = train(&s.matter.nodes, &s.matter.sources).unwrap();
    assert_eq!(suggestedFacet(&infer(&network, "Payment: 125 USD.".into()).unwrap()), "payment.amount",
        "the reviewed source vocabulary must train the facet, not just the normalized meaning 50");
    assert!(!usableMeaning(&inferMeaning(&s.matter.nodes, &s.matter.sources, "Payment disputed: 75 USD.".into()).unwrap()));
    assert!(transferMeaning("50".into(), "50".into(), "arbitrary".into()).unwrap().is_none(),
        "an unanchored whole-value example cannot classify arbitrary new content");
    assert!(transferMeaning("50 and 50".into(), "50".into(), "60 and 70".into()).unwrap().is_none());
    let changed = accepted(review(&s, s.matter.revision, Role::Client, "client".into(),
        Reference { id: 1, revision: 2 }, "payment.dispute".into(), "unverified".into(), true).unwrap());
    assert!(!usableMeaning(&inferMeaning(&changed.matter.nodes, &changed.matter.sources, "Payment: 75 USD.".into()).unwrap()));
}

#[test]
fn competing_reviewed_meanings_abstain_and_keep_their_provenance() {
    let s = accepted(ingest(&initial("Ambiguity".into()), 0, Role::Client, "client".into(),
        "Receipt".into(), b"Payment: 50 USD.".to_vec()).unwrap());
    let s = accepted(review(&s, 1, Role::Client, "client".into(), Reference { id: 1, revision: 1 },
        "payment.amount".into(), "50".into(), true).unwrap());
    let s = accepted(annotate(&s, 2, Role::Client, "client".into(), Reference { id: 1, revision: 2 },
        "claimed.amount".into(), "50".into()).unwrap());
    let suggestion = inferMeaning(&s.matter.nodes, &s.matter.sources, "Payment: 75 USD.".into()).unwrap();
    assert!(suggestion.matched && suggestion.ambiguous);
    assert!(!usableMeaning(&suggestion));
    assert_eq!(suggestion.examples.len(), 2);
    assert_eq!(s.matter.nodes[0].citations, s.matter.nodes[1].citations);
}

#[test]
fn a_lawyer_cannot_substitute_a_different_conclusion_under_old_support() {
    let s = reviewed_matter();
    let s = accepted(propose(&s, s.matter.revision, Role::Lawyer, "lawyer".into(), s.rules[0].definition).unwrap());
    let n = s.matter.nodes.iter().max_by_key(|n| n.id).unwrap();
    for (facet, value) in [(n.facet.as_str(), "a different legal finding"), ("unrelated.conclusion", n.value.as_str())] {
        let refused = review(&s, s.matter.revision, Role::Lawyer, "lawyer".into(), nodeReference(n),
            facet.into(), value.into(), true).unwrap();
        assert_eq!(refused.code, "support-is-stale");
        assert_eq!(refused.session, s);
    }
}

#[test]
fn withdrawing_one_interpretation_retains_other_facets_and_does_not_requeue_it() {
    let s = accepted(ingest(&initial("Review".into()), 0, Role::Client, "client".into(),
        "Receipt".into(), b"Amount: 50; date: Monday.".to_vec()).unwrap());
    let s = accepted(review(&s, 1, Role::Client, "client".into(), Reference { id: 1, revision: 1 },
        "amount".into(), "50".into(), true).unwrap());
    let s = accepted(annotate(&s, 2, Role::Client, "client".into(), Reference { id: 1, revision: 2 },
        "date".into(), "Monday".into()).unwrap());
    let s = accepted(withdraw(&s, 3, Role::Client, "client".into(), Reference { id: 2, revision: 1 }).unwrap());
    let s = accepted(ingest(&s, 4, Role::Client, "client".into(), "Another source".into(), b"New context".to_vec()).unwrap());
    let withdrawn = s.matter.nodes.iter().find(|n| n.id == 2).unwrap();
    assert!(isWithdrawn(&s.audit, withdrawn), "source IDs and node IDs share a number space but not audit identity");
    assert_eq!(nextReview(&s).unwrap().unwrap().value, "New context");
    assert_eq!(current(&s.matter.nodes, &s.matter.sources).unwrap().references, vec![Reference { id: 1, revision: 2 }]);
    assert_eq!(s.matter.changes[0].before.value, "Monday");
    assert!(!s.matter.changes[0].after.accepted);
}

#[test]
fn impact_follows_new_exception_edges_as_well_as_existing_support_references() {
    let s = reviewed_matter();
    let s = accepted(propose(&s, s.matter.revision, Role::Lawyer, "lawyer".into(), s.rules[0].definition).unwrap());
    let conclusion = s.matter.nodes.iter().max_by_key(|n| n.id).unwrap().clone();
    let s = accepted(review(&s, s.matter.revision, Role::Lawyer, "lawyer".into(), nodeReference(&conclusion),
        conclusion.facet, conclusion.value, true).unwrap());
    let s = assert_fact(&s, "notice.withdrawal", "withdrawn");
    let affected = latestImpact(&s).unwrap().references;
    assert!(affected.iter().any(|r| r.id == s.rules[0].definition.id));
    assert!(affected.iter().any(|r| r.id == conclusion.id));
    assert!(!affected.iter().any(|r| r.id == node_ref(&s, "goal").id), "consequences do not invalidate their upstream goal");
}

#[test]
fn pending_source_attention_follows_unresolved_matter_conditions() {
    let s = reviewed_matter();
    let s = accepted(ingest(&s, s.matter.revision, Role::Client, "client".into(), "Status".into(), b"Case status: pending".to_vec()).unwrap());
    let status = s.matter.nodes.iter().max_by_key(|n| n.id).unwrap();
    let s = accepted(review(&s, s.matter.revision, Role::Client, "client".into(), nodeReference(status),
        "case.status".into(), "pending".into(), true).unwrap());
    let mut rule = s.rules[0].clone(); rule.definition = Reference { id: 0, revision: 0 };
    rule.premises = vec![Requirement { facet: "case.status".into(), value: "confirmed".into(), question: "Has the status been confirmed?".into() }];
    let s = accepted(commitRule(&s, s.matter.revision, Role::Lawyer, "lawyer".into(), &rule).unwrap());
    let s = accepted(ingest(&s, s.matter.revision, Role::Client, "client".into(), "Update".into(),
        b"Unrelated context\nCase status: confirmed".to_vec()).unwrap());
    assert_eq!(nextReview(&s).unwrap().unwrap().value, "Case status: confirmed");
    let selected = attentionAssessment(&assessAll(&s.rules, &s.matter.nodes, &s.matter.sources).unwrap().values).unwrap();
    assert_eq!(selected.status, ReasoningStatus::Missing);
}

#[test]
fn one_passage_can_supply_separate_facets_without_cross_facet_ambiguity() {
    let s = accepted(ingest(&initial("Receipt".into()), 0, Role::Client, "client".into(), "Receipt".into(), b"Amount: 50; day: Monday.".to_vec()).unwrap());
    let s = accepted(review(&s, 1, Role::Client, "client".into(), Reference { id: 1, revision: 1 }, "amount".into(), "50".into(), true).unwrap());
    let s = accepted(annotate(&s, 2, Role::Client, "client".into(), Reference { id: 1, revision: 2 }, "day".into(), "Monday".into()).unwrap());
    for (facet, text, expected) in [("amount", "Amount: 75; day: Monday.", "75"), ("day", "Amount: 50; day: Tuesday.", "Tuesday")] {
        let candidate = inferFacetMeaning(&s.matter.nodes, &s.matter.sources, text.into(), facet.into()).unwrap();
        assert!(usableMeaning(&candidate));
        assert_eq!(candidate.value, expected);
        assert_eq!(candidate.examples.len(), 1);
    }
    let candidate = inferFacetMeaning(&s.matter.nodes, &s.matter.sources, "Amount: 75; day: Tuesday.".into(), "amount".into()).unwrap();
    assert!(!usableMeaning(&candidate), "unreviewed changes to the anchor must abstain");
    let s = accepted(annotate(&s, 3, Role::Client, "client".into(), Reference { id: 1, revision: 2 }, "amount".into(), "not confirmed".into()).unwrap());
    let candidate = inferFacetMeaning(&s.matter.nodes, &s.matter.sources, "Amount: 50; day: Monday.".into(), "amount".into()).unwrap();
    assert!(candidate.ambiguous);
    assert_eq!(candidate.examples.len(), 2);
}

#[test]
fn competing_meanings_of_one_passage_suspend_support_until_resolved() {
    let s = reviewed_matter();
    let s = accepted(propose(&s, s.matter.revision, Role::Lawyer, "lawyer".into(), s.rules[0].definition).unwrap());
    let conclusion = s.matter.nodes.iter().max_by_key(|n| n.id).unwrap().clone();
    let s = accepted(review(&s, s.matter.revision, Role::Lawyer, "lawyer".into(), nodeReference(&conclusion), conclusion.facet, conclusion.value, true).unwrap());
    let s = accepted(annotate(&s, s.matter.revision, Role::Client, "client".into(), node_ref(&s,"notice.receipt"), "notice.receipt".into(), "not received".into()).unwrap());
    let alternative = s.matter.nodes.iter().max_by_key(|n| n.id).unwrap().clone();
    let assessment = assess(&s.rules[0], &s.matter.nodes, &s.matter.sources).unwrap();
    assert_eq!(assessment.status, ReasoningStatus::Missing);
    assert!(assessment.questions.iter().any(|q| q.contains("competing interpretations")));
    assert!(!s.matter.nodes.iter().find(|n| n.id == conclusion.id).unwrap().accepted);
    let s = accepted(withdraw(&s, s.matter.revision, Role::Client, "client".into(), nodeReference(&alternative)).unwrap());
    assert_eq!(assess(&s.rules[0], &s.matter.nodes, &s.matter.sources).unwrap().status, ReasoningStatus::Supported);
    assert!(!s.matter.nodes.iter().find(|n| n.id == conclusion.id).unwrap().accepted, "resolving a conflict does not silently accept the old conclusion");
}

#[test]
fn contested_exceptions_cannot_be_treated_as_absent_and_authority_must_be_uncontested() {
    let s = reviewed_matter();
    let receipt = node_ref(&s,"notice.receipt");
    let s = accepted(annotate(&s, s.matter.revision, Role::Client, "client".into(), receipt, "notice.withdrawal".into(), "withdrawn".into()).unwrap());
    assert_eq!(assess(&s.rules[0], &s.matter.nodes, &s.matter.sources).unwrap().status, ReasoningStatus::Excepted);
    let s = accepted(annotate(&s, s.matter.revision, Role::Client, "client".into(), receipt, "notice.withdrawal".into(), "still in force".into()).unwrap());
    let assessment = assess(&s.rules[0], &s.matter.nodes, &s.matter.sources).unwrap();
    assert_eq!(assessment.status, ReasoningStatus::Missing);
    assert!(assessment.questions[0].contains("notice.withdrawal"));
    let s = reviewed_matter();
    let s = accepted(annotate(&s, s.matter.revision, Role::Lawyer, "lawyer".into(), node_ref(&s,"authority"), "authority".into(), "a competing construction".into()).unwrap());
    assert_eq!(assess(&s.rules[0], &s.matter.nodes, &s.matter.sources).unwrap().status, ReasoningStatus::Inactive);
}

#[test]
fn separate_passages_with_different_values_are_not_assumed_mutually_exclusive() {
    let s = reviewed_matter();
    let s = accepted(ingest(&s, s.matter.revision, Role::Client, "client".into(), "Other notice".into(), b"A different notice was disputed.".to_vec()).unwrap());
    let latest = s.matter.nodes.iter().max_by_key(|n| n.id).unwrap();
    let s = accepted(review(&s, s.matter.revision, Role::Client, "client".into(), nodeReference(latest), "notice.receipt".into(), "disputed".into(), true).unwrap());
    assert_eq!(assess(&s.rules[0], &s.matter.nodes, &s.matter.sources).unwrap().status, ReasoningStatus::Supported);
}
