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
    assert!(usableMeaning(&candidate), "both changing values have independently reviewed slots");
    assert_eq!(candidate.value, "75");
    assert_eq!(candidate.examples.len(), 2);
    let candidate = inferFacetMeaning(&s.matter.nodes, &s.matter.sources, "Amount: 75; unreviewed day: Tuesday.".into(), "amount".into()).unwrap();
    assert!(!usableMeaning(&candidate), "changes to unreviewed literal anchors must abstain");
    let s = accepted(annotate(&s, 3, Role::Client, "client".into(), Reference { id: 1, revision: 2 }, "amount".into(), "not confirmed".into()).unwrap());
    let candidate = inferFacetMeaning(&s.matter.nodes, &s.matter.sources, "Amount: 50; day: Monday.".into(), "amount".into()).unwrap();
    assert!(candidate.ambiguous);
    assert_eq!(candidate.examples.len(), 2);
    let candidate = inferFacetMeaning(&s.matter.nodes, &s.matter.sources, "Amount: 75; day: Monday.".into(), "amount".into()).unwrap();
    assert!(candidate.matched && candidate.ambiguous, "a single matching template cannot resolve disputed training");
    assert_eq!(candidate.examples.len(), 2, "retain the competing interpretation that prevents transfer");
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

#[test]
fn joint_slots_preserve_utf8_and_all_training_provenance() {
    let s = accepted(ingest(&initial("Records".into()), 0, Role::Client, "client".into(), "Record".into(),
        "Person: Zoë; amount: 50; day: Monday.".as_bytes().to_vec()).unwrap());
    let s = accepted(review(&s, 1, Role::Client, "client".into(), Reference { id: 1, revision: 1 }, "day".into(), "Monday".into(), true).unwrap());
    let s = accepted(annotate(&s, 2, Role::Client, "client".into(), Reference { id: 1, revision: 2 }, "person".into(), "Zoë".into()).unwrap());
    let s = accepted(annotate(&s, 3, Role::Client, "client".into(), Reference { id: 1, revision: 2 }, "amount".into(), "50".into()).unwrap());
    let text = "Person: 李明; amount: 75; day: Tuesday.";
    for (facet, value) in [("person", "李明"), ("amount", "75"), ("day", "Tuesday")] {
        let candidate = inferFacetMeaning(&s.matter.nodes, &s.matter.sources, text.into(), facet.into()).unwrap();
        assert!(usableMeaning(&candidate)); assert_eq!(candidate.value, value);
        assert_eq!(candidate.examples.len(), 3);
        for node in &s.matter.nodes { assert!(candidate.examples.contains(&nodeReference(node))); }
    }
    assert!(inferMeaning(&s.matter.nodes, &s.matter.sources, text.into()).unwrap().ambiguous,
        "a multi-facet passage does not invent a single preferred facet");
    let s = accepted(annotate(&s, s.matter.revision, Role::Client, "client".into(), node_ref(&s, "amount"), "claimed.amount".into(), "50".into()).unwrap());
    for facet in ["amount", "claimed.amount"] {
        let candidate = inferFacetMeaning(&s.matter.nodes, &s.matter.sources, text.into(), facet.into()).unwrap();
        assert!(usableMeaning(&candidate), "identical source spans can carry independently reviewed facets");
        assert_eq!(candidate.value, "75"); assert_eq!(candidate.examples.len(), 4);
    }
    let s = accepted(withdraw(&s, s.matter.revision, Role::Client, "client".into(), node_ref(&s, "day")).unwrap());
    assert!(!usableMeaning(&inferFacetMeaning(&s.matter.nodes, &s.matter.sources, text.into(), "amount".into()).unwrap()),
        "withdrawn anchors cannot train a joint template");
}

#[test]
fn joint_templates_refuse_ambiguous_anchors_overlaps_and_conflicting_training() {
    let s = accepted(ingest(&initial("Receipt".into()), 0, Role::Client, "client".into(), "Receipt".into(), b"Amount: 50; day: Monday.".to_vec()).unwrap());
    let s = accepted(review(&s, 1, Role::Client, "client".into(), Reference { id: 1, revision: 1 }, "amount".into(), "50".into(), true).unwrap());
    let s = accepted(annotate(&s, 2, Role::Client, "client".into(), Reference { id: 1, revision: 2 }, "day".into(), "Monday".into()).unwrap());
    for text in ["Amount: ; day: Tuesday.", "Amount: 75; day: Tuesday; day: Friday.", "Amount: 75; day: Tuesday!", "Other: 75; day: Tuesday."] {
        assert!(!usableMeaning(&inferFacetMeaning(&s.matter.nodes, &s.matter.sources, text.into(), "amount".into()).unwrap()), "{text}");
    }
    let s = accepted(annotate(&s, 3, Role::Client, "client".into(), Reference { id: 1, revision: 2 }, "amount".into(), "not confirmed".into()).unwrap());
    assert!(!usableMeaning(&inferFacetMeaning(&s.matter.nodes, &s.matter.sources, "Amount: 75; day: Tuesday.".into(), "amount".into()).unwrap()));
    let s = accepted(ingest(&initial("Overlap".into()), 0, Role::Client, "client".into(), "Receipt".into(), b"Amount: 50 USD; day: Monday.".to_vec()).unwrap());
    let s = accepted(review(&s, 1, Role::Client, "client".into(), Reference { id: 1, revision: 1 }, "amount".into(), "50".into(), true).unwrap());
    let s = accepted(annotate(&s, 2, Role::Client, "client".into(), Reference { id: 1, revision: 2 }, "payment".into(), "50 USD".into()).unwrap());
    let s = accepted(annotate(&s, 3, Role::Client, "client".into(), Reference { id: 1, revision: 2 }, "day".into(), "Monday".into()).unwrap());
    assert!(!usableMeaning(&inferFacetMeaning(&s.matter.nodes, &s.matter.sources, "Amount: 75 EUR; day: Tuesday.".into(), "amount".into()).unwrap()));
}

#[test]
fn joint_templates_do_not_merge_unrelated_source_spans_or_adjacent_slots() {
    let s = accepted(ingest(&initial("Separate records".into()), 0, Role::Client, "client".into(), "Receipt".into(), b"Amount: 50; day: Monday.\nAmount: 50; day: Monday.".to_vec()).unwrap());
    let s = accepted(review(&s, 1, Role::Client, "client".into(), Reference { id: 1, revision: 1 }, "amount".into(), "50".into(), true).unwrap());
    let s = accepted(review(&s, 2, Role::Client, "client".into(), Reference { id: 2, revision: 1 }, "day".into(), "Monday".into(), true).unwrap());
    assert!(!usableMeaning(&inferFacetMeaning(&s.matter.nodes, &s.matter.sources, "Amount: 75; day: Tuesday.".into(), "amount".into()).unwrap()));
    let s = accepted(ingest(&initial("Adjacent values".into()), 0, Role::Client, "client".into(), "Record".into(), b"AB!".to_vec()).unwrap());
    let s = accepted(review(&s, 1, Role::Client, "client".into(), Reference { id: 1, revision: 1 }, "left".into(), "A".into(), true).unwrap());
    let s = accepted(annotate(&s, 2, Role::Client, "client".into(), Reference { id: 1, revision: 2 }, "right".into(), "B".into()).unwrap());
    assert!(!usableMeaning(&inferFacetMeaning(&s.matter.nodes, &s.matter.sources, "CD!".into(), "left".into()).unwrap()));
    let s = accepted(ingest(&initial("Unanchored aliases".into()), 0, Role::Client, "client".into(), "Record".into(), b"50".to_vec()).unwrap());
    let s = accepted(review(&s, 1, Role::Client, "client".into(), Reference { id: 1, revision: 1 }, "amount".into(), "50".into(), true).unwrap());
    let s = accepted(annotate(&s, 2, Role::Client, "client".into(), Reference { id: 1, revision: 2 }, "claimed.amount".into(), "50".into()).unwrap());
    assert!(!usableMeaning(&inferFacetMeaning(&s.matter.nodes, &s.matter.sources, "unrelated wording".into(), "amount".into()).unwrap()),
        "multiple facets on the same value do not establish a literal anchor");
}

#[test]
fn renamed_facets_show_both_removed_and_added_rule_connections() {
    let s = reviewed_matter();
    let original_rule = s.rules[0].definition;
    let mut changed = s.rules[0].clone(); changed.definition = Reference { id: 0, revision: 0 };
    changed.premises = vec![Requirement { facet: "communication.receipt".into(), value: "received".into(), question: "Was communication received?".into() }];
    changed.action = "Review the communication".into();
    let s = accepted(commitRule(&s, s.matter.revision, Role::Lawyer, "lawyer".into(), &changed).unwrap());
    let new_rule = s.rules.iter().find(|rule| rule.action == "Review the communication").unwrap().definition;
    let reference = node_ref(&s, "notice.receipt");
    let s = accepted(review(&s, s.matter.revision, Role::Client, "client".into(), reference, "communication.receipt".into(), "received".into(), true).unwrap());
    let impact = latestImpact(&s).unwrap().references;
    assert!(impact.iter().any(|r| r.id == original_rule.id), "removing a formerly relevant facet affects the old condition");
    assert!(impact.iter().any(|r| r.id == new_rule.id), "the new facet also affects its own conditions");
    let s = accepted(review(&s, s.matter.revision, Role::Client, "client".into(), node_ref(&s, "communication.receipt"), "unrelated.receipt".into(), "received".into(), true).unwrap());
    let impact = latestImpact(&s).unwrap().references;
    assert!(impact.iter().any(|r| r.id == new_rule.id));
    assert!(!impact.iter().any(|r| r.id == original_rule.id), "older facet history must not create spurious current impact");
}

fn jointly_reviewed_amounts() -> Session {
    let s = accepted(ingest(&initial("Dated receipts".into()), 0, Role::Client, "client".into(), "Records".into(),
        b"Amount: 50; day: Monday.\nAmount: 75; day: Tuesday.".to_vec()).unwrap());
    let s = assert_fact(&s, "goal", "Understand both fields");
    let s = accepted(review(&s, s.matter.revision, Role::Client, "client".into(), Reference { id: 1, revision: 1 }, "amount".into(), "50".into(), true).unwrap());
    let s = accepted(annotate(&s, s.matter.revision, Role::Client, "client".into(), node_ref(&s, "amount"), "day".into(), "Monday".into()).unwrap());
    accepted(review(&s, s.matter.revision, Role::Client, "client".into(), Reference { id: 2, revision: 1 }, "amount".into(), "75".into(), true).unwrap())
}

#[test]
fn reviewing_one_facet_keeps_other_learned_facets_in_the_journey() {
    let s = jointly_reviewed_amounts();
    let before = s.clone();
    let view = overview(&s, Role::Client).unwrap();
    assert_eq!(view.stage, "additional-interpretation");
    assert_eq!(view.node, 2); assert_eq!(view.suggestion, "day");
    assert!(view.context.iter().any(|text| text == "Records · line 2"));
    assert!(view.context.iter().any(|text| text.contains("Tuesday")));
    assert!(view.context.iter().any(|text| text == "Amount: 75; day: Tuesday."));
    let prepared = nextStep(&s, Role::Client, &view).unwrap();
    assert!(prepared.starts_with("review\u{1f}")); assert!(prepared.contains("Tuesday"));
    assert_eq!(s, before, "preparing the review does not accept an interpretation");
    let s = accepted(annotate(&s, s.matter.revision, Role::Client, "client".into(), Reference { id: 2, revision: 2 }, "day".into(), "Tuesday".into()).unwrap());
    assert!(nextAdditionalReview(&s).unwrap().node.is_none());
    assert_eq!(overview(&s, Role::Client).unwrap().stage, "jurisdiction");
    let added = s.matter.nodes.iter().find(|n| n.facet == "day" && n.value == "Tuesday").unwrap();
    let s = accepted(withdraw(&s, s.matter.revision, Role::Client, "client".into(), nodeReference(added)).unwrap());
    assert!(nextAdditionalReview(&s).unwrap().node.is_none(), "withdrawal must not create a review loop");
}

#[test]
fn additional_review_retracts_when_its_training_is_withdrawn() {
    let s = jointly_reviewed_amounts();
    assert_eq!(nextAdditionalReview(&s).unwrap().meaning.value, "Tuesday");
    let training = s.matter.nodes.iter().find(|n| n.facet == "day").unwrap();
    let s = accepted(withdraw(&s, s.matter.revision, Role::Client, "client".into(), nodeReference(training)).unwrap());
    assert!(nextAdditionalReview(&s).unwrap().node.is_none());
}

#[test]
fn additional_review_keeps_equal_values_on_separate_passages_distinct() {
    let s = jointly_reviewed_amounts();
    let s = accepted(ingest(&s, s.matter.revision, Role::Client, "client".into(), "Records".into(), b"Amount: 75; day: Tuesday.".to_vec()).unwrap());
    let next = s.matter.nodes.iter().max_by_key(|n| n.id).unwrap();
    let s = accepted(review(&s, s.matter.revision, Role::Client, "client".into(), nodeReference(next), "amount".into(), "75".into(), true).unwrap());
    let focused = nextAdditionalReview(&s).unwrap();
    assert_eq!(focused.node.as_ref().unwrap().id, 2);
    assert!(overview(&s, Role::Client).unwrap().context.iter().any(|text| text == "Records · resource 1 · line 2"));
    let chosen = focused.node.unwrap();
    let s = accepted(annotate(&s, s.matter.revision, Role::Client, "client".into(), nodeReference(&chosen), "day".into(), focused.meaning.value).unwrap());
    let following = nextAdditionalReview(&s).unwrap();
    assert_ne!(following.node.as_ref().unwrap().id, chosen.id);
    assert_eq!(following.node.as_ref().unwrap().citations[0].source, 2);
    assert_eq!(following.meaning.value, "Tuesday");
    assert!(overview(&s, Role::Client).unwrap().context.iter().any(|text| text == "Records · resource 2 · line 1"));
}

#[test]
fn additional_review_preserves_ambiguity_instead_of_prefilling_an_answer() {
    let s = jointly_reviewed_amounts();
    let s = accepted(ingest(&s, s.matter.revision, Role::Client, "client".into(), "Competing record".into(), b"Amount: 75; day: Tuesday.".to_vec()).unwrap());
    let latest = s.matter.nodes.iter().max_by_key(|n| n.id).unwrap();
    let reference = Reference { id: latest.id, revision: latest.revision + 1 };
    let s = accepted(review(&s, s.matter.revision, Role::Client, "client".into(), nodeReference(latest), "day".into(), "Tuesday".into(), true).unwrap());
    let s = accepted(annotate(&s, s.matter.revision, Role::Client, "client".into(), reference, "day".into(), "not established".into()).unwrap());
    let extra = nextAdditionalReview(&s).unwrap();
    assert_eq!(extra.node.unwrap().id, 2); assert_eq!(extra.meaning.facet, "day");
    assert!(extra.meaning.ambiguous);
    let view = overview(&s, Role::Client).unwrap();
    assert!(view.context.iter().any(|text| text.contains("Reviewed examples disagree")));
    assert!(nextStep(&s, Role::Client, &view).unwrap().ends_with("3:day0:0:"), "disagreement requires an editable empty meaning");
}

#[test]
fn additional_review_respects_privileged_facets_and_reader_workflows() {
    let s = jointly_reviewed_amounts();
    let s = accepted(annotate(&s, s.matter.revision, Role::Lawyer, "lawyer".into(), Reference { id: 1, revision: 2 }, "authority".into(), "Monday".into()).unwrap());
    assert_eq!(nextAdditionalReview(&s).unwrap().meaning.facet, "authority");
    let client = overview(&s, Role::Client).unwrap();
    let lawyer = overview(&s, Role::Lawyer).unwrap();
    assert_eq!(client.node, lawyer.node, "changing role must not change the reviewed passage");
    assert_eq!(client.suggestion, lawyer.suggestion);
    assert_eq!(client.heading, "Lawyer review: another aspect");
    assert_eq!(nextStep(&s, Role::Client, &client).unwrap(), "");
    assert!(nextStep(&s, Role::Lawyer, &lawyer).unwrap().starts_with("review\u{1f}"));
    let view = overview(&s, Role::Reader).unwrap();
    assert_eq!(view.stage, "additional-interpretation");
    assert_eq!(nextStep(&s, Role::Reader, &view).unwrap(), "", "reader views must not prepare a mutating workflow");
}

#[test]
fn review_locations_follow_utf8_bytes_and_crlf_without_exposing_internal_ids() {
    let s = accepted(ingest(&initial("Source locations".into()), 0, Role::Client, "client".into(), "Records".into(), "Zoë\r\nSecond passage".as_bytes().to_vec()).unwrap());
    let view = select(&s, Role::Client, 2, 0).unwrap();
    assert_eq!(view.explanation, "Second passage");
    assert!(view.context.iter().any(|text| text == "Records · line 2"));
    assert!(!view.context.iter().any(|text| text.contains("bytes")));
}

#[test]
fn additional_facet_attention_prioritizes_unresolved_rule_conditions() {
    let s = jointly_reviewed_amounts();
    let s = assert_fact(&s, "jurisdiction", "Reviewed jurisdiction");
    let s = accepted(ingest(&s, s.matter.revision, Role::Lawyer, "lawyer".into(), "Governing provision".into(), b"Review the receipt date before acting.".to_vec()).unwrap());
    let latest = s.matter.nodes.iter().max_by_key(|n| n.id).unwrap();
    let s = accepted(review(&s, s.matter.revision, Role::Lawyer, "lawyer".into(), nodeReference(latest), "authority".into(), "Reviewed date provision".into(), true).unwrap());
    let s = accepted(annotate(&s, s.matter.revision, Role::Client, "client".into(), Reference { id: 1, revision: 2 }, "claimed.amount".into(), "50".into()).unwrap());
    let rule = Rule { definition: Reference { id: 0, revision: 0 }, authority: node_ref(&s,"authority"), jurisdiction: node_ref(&s,"jurisdiction"), goal: node_ref(&s,"goal"),
        premises: vec![Requirement { facet: "day".into(), value: "Tuesday".into(), question: "Confirm the receipt day".into() }], exceptions: vec![],
        conclusionFacet: "receipt.review".into(), conclusionValue: "dated receipt reviewed".into(), action: "Review the dated receipt".into() };
    let s = accepted(commitRule(&s, s.matter.revision, Role::Lawyer, "lawyer".into(), &rule).unwrap());
    assert_eq!(nextAdditionalReview(&s).unwrap().meaning.facet, "day");
    let s=accepted(ingest(&s,s.matter.revision,Role::Client,"client".into(),"Other".into(),b"Understand both fields".to_vec()).unwrap());
    let focused=nextAttention(&s).unwrap();assert!(focused.additional,"unresolved rule conditions outrank mere goal vocabulary");assert_eq!(focused.meaning.facet,"day");
}

fn repeated_reviewed_journal() -> String {
    let title = "Separate receipts".to_string();
    let start = initialJournal(title);
    let s = replay(start.clone()).unwrap().session;
    let imported = commit(start, &s, "ingest".into(), "client".into(), &vec!["Records".into(), "Zoë: 75\r\nZoë: 75".into()]).unwrap();
    assert_eq!(imported.code, "");
    let first = reviewNext(imported.journal, &imported.session, "client".into(), "amount".into(), "75".into()).unwrap();
    assert_eq!(first.code, "");
    let second = reviewNext(first.journal, &first.session, "client".into(), "amount".into(), "75".into()).unwrap();
    assert_eq!(second.code, "");
    second.journal
}

#[test]
fn located_changes_preserve_the_other_passage_and_replay_exactly() {
    let journal = repeated_reviewed_journal();
    let s = replay(journal.clone()).unwrap().session;
    assert!(uniqueLocatedNode(&s, "amount".into(), "75".into(), "".into()).unwrap().is_none());
    let refused = editLocatedValue(journal.clone(), &s, "client".into(), "amount".into(), "75".into(), "80".into(), "Records · line 3".into()).unwrap();
    assert_eq!(refused.journal, journal); assert_eq!(refused.session, s); assert!(!refused.code.is_empty());
    let corrected = editLocatedValue(journal, &s, "client".into(), "amount".into(), "75".into(), "80".into(), "Records · line 2".into()).unwrap();
    assert_eq!(corrected.code, "");
    assert_eq!(findNode(&corrected.session.matter.nodes, 1).unwrap().value, "75");
    assert_eq!(findNode(&corrected.session.matter.nodes, 2).unwrap().value, "80");
    assert_eq!(corrected.session.matter.sources, s.matter.sources);
    assert_eq!(findNode(&corrected.session.matter.nodes, 2).unwrap().citations, findNode(&s.matter.nodes, 2).unwrap().citations);
    let fields = vec![corrected.journal.clone(), "client".into(), "amount".into(), "80".into(), "disputed.amount".into(), "80".into(), "Records · line 2".into()];
    let annotated = changeFields("annotate".into(), &fields, corrected.journal, &corrected.session, "client".into()).unwrap();
    assert_eq!(annotated.code, "");
    let fields = vec![annotated.journal.clone(), "client".into(), "amount".into(), "75".into(), "Records · line 1".into()];
    let withdrawn = changeFields("withdraw".into(), &fields, annotated.journal, &annotated.session, "client".into()).unwrap();
    assert_eq!(withdrawn.code, "");
    assert!(!findNode(&withdrawn.session.matter.nodes, 1).unwrap().accepted);
    assert!(findNode(&withdrawn.session.matter.nodes, 2).unwrap().accepted);
    assert!(withdrawn.session.matter.nodes.iter().find(|n| n.facet == "disputed.amount").unwrap().accepted);
    assert_eq!(replay(withdrawn.journal).unwrap().session, withdrawn.session);
}

#[test]
fn source_qualifiers_handle_duplicate_names_and_never_bypass_permissions() {
    let mut s = replay(repeated_reviewed_journal()).unwrap().session;
    s = accepted(ingest(&s, s.matter.revision, Role::Lawyer, "lawyer".into(), "Records".into(), b"Provision".to_vec()).unwrap());
    let id = s.matter.nodes.iter().max_by_key(|n| n.id).unwrap().id;
    s = accepted(review(&s, s.matter.revision, Role::Lawyer, "lawyer".into(), Reference {id, revision:1}, "authority".into(), "Reviewed provision".into(), true).unwrap());
    assert!(uniqueLocatedNode(&s, "amount".into(), "75".into(), "Records · line 1".into()).unwrap().is_none());
    assert_eq!(uniqueLocatedNode(&s, "amount".into(), "75".into(), "Records · resource 1 · line 1".into()).unwrap().unwrap().id, 1);
    let chosen = uniqueLocatedNode(&s, "authority".into(), "Reviewed provision".into(), "Records · resource 2 · line 1".into()).unwrap().unwrap();
    let refused = review(&s, s.matter.revision, Role::Client, "client".into(), nodeReference(&chosen), "authority".into(), "Unreviewed replacement".into(), true).unwrap();
    assert_eq!(refused.code, "lawyer-review-required"); assert_eq!(refused.session, s);
}

#[test]
fn visually_equal_source_locations_remain_ambiguous_instead_of_choosing_a_passage() {
    let mut s = initial("Visible ambiguity".into());
    for title in ["Records\tfile", "Records file"] {
        s = accepted(ingest(&s, s.matter.revision, Role::Client, "client".into(), title.into(), b"75".to_vec()).unwrap());
        let node = nextReview(&s).unwrap().unwrap();
        s = accepted(review(&s, s.matter.revision, Role::Client, "client".into(), nodeReference(&node), "amount".into(), "75".into(), true).unwrap());
    }
    assert!(uniqueLocatedNode(&s, "amount".into(), "75".into(), "Records file · line 1".into()).unwrap().is_none());
    let previous = s.clone();
    let stale = s.matter.sources[0].clone();
    s = accepted(reviseSource(&s, s.matter.revision, Role::Client, "client".into(), Reference{id:stale.id, revision:stale.revision}, b"80".to_vec()).unwrap());
    let selected = uniqueLocatedNode(&s, "amount".into(), "75".into(), "Records file · line 1".into()).unwrap().unwrap();
    assert_ne!(selected.citations[0].source, stale.id);
    assert_eq!(previous.matter.sources.len(), s.matter.sources.len());
}

#[test]
fn inspection_locations_use_the_cited_historical_bytes_after_source_replacement() {
    let mut s = replay(repeated_reviewed_journal()).unwrap().session;
    let old = findNode(&s.matter.nodes, 2).unwrap();
    s = accepted(reviseSource(&s, s.matter.revision, Role::Client, "client".into(), Reference{id:1, revision:1}, b"Completely changed first line\n75".to_vec()).unwrap());
    assert_eq!(interpretationLocation(&s, &old).unwrap(), "Records · earlier version 1 · line 2");
    assert!(uniqueLocatedNode(&s, "amount".into(), "75".into(), "Records · earlier version 1 · line 2".into()).unwrap().is_none());
    let new = s.matter.nodes.iter().max_by_key(|n|n.id).unwrap();
    assert_eq!(interpretationLocation(&s, new).unwrap(), "Records · line 2");
}

#[test]
fn chronology_uses_valid_civil_dates_without_guessing_formats_or_missing_parts() {
    for (text,key) in [("0001-01-01",10101),("2024-02-29",20240229),("2000-02-29",20000229),("9999-12-31",99991231)] {
        assert_eq!(calendarDateKey(text.into()).unwrap(),Some(key),"{text}");
    }
    for text in ["1900-02-29","2023-02-29","2024-04-31","2024-06-31","2024-00-01","2024-13-01","2024-01-00","0000-01-01","2024-1-01","24-01-01","2024/01/01","2024-01-01 ","2024-01-01T00:00:00Z","early March","２０２４-01-01",""] {
        assert_eq!(calendarDateKey(text.into()).unwrap(),None,"{text}");
    }
}

#[test]
fn chronology_reorders_corrections_and_retains_ambiguous_dates_for_review() {
    let s=accepted(ingest(&initial("Dates".into()),0,Role::Client,"client".into(),"Notices".into(),
        b"Later: 2024-03-01.\nEarlier: 2024-02-29.\nUncertain: early March.".to_vec()).unwrap());
    let mut s=s;
    for (id,value) in [(1,"2024-03-01"),(2,"2024-02-29"),(3,"early March")] {
        s=accepted(review(&s,s.matter.revision,Role::Client,"client".into(),Reference{id,revision:1},"notice.date".into(),value.into(),true).unwrap());
    }
    let result=reviewed_chronology(&s,&["notice.date"]);
    assert_eq!(result.dated.iter().map(|e|e.node.id).collect::<Vec<_>>(),vec![2,1]);
    assert_eq!(result.unresolved.iter().map(|n|n.id).collect::<Vec<_>>(),vec![3]);
    assert_eq!(result.dated[0].node.citations,findNode(&s.matter.nodes,2).unwrap().citations);
    s=accepted(review(&s,s.matter.revision,Role::Client,"client".into(),Reference{id:1,revision:2},"notice.date".into(),"2024-02-28".into(),true).unwrap());
    assert_eq!(reviewed_chronology(&s,&["notice.date"]).dated.iter().map(|e|e.node.id).collect::<Vec<_>>(),vec![1,2]);
    s=accepted(annotate(&s,s.matter.revision,Role::Client,"client".into(),Reference{id:2,revision:2},"notice.date".into(),"2024-03-02".into()).unwrap());
    let result=reviewed_chronology(&s,&["notice.date"]);
    assert_eq!(result.dated.len(),1);assert_eq!(result.unresolved.len(),3);
    let competing=s.matter.nodes.iter().find(|n|n.value=="2024-03-02").unwrap();
    s=accepted(withdraw(&s,s.matter.revision,Role::Client,"client".into(),nodeReference(competing)).unwrap());
    assert_eq!(reviewed_chronology(&s,&["notice.date"]).dated.len(),2);
    s=accepted(reviseSource(&s,s.matter.revision,Role::Client,"client".into(),Reference{id:1,revision:1},b"Replacement notice".to_vec()).unwrap());
    let result=reviewed_chronology(&s,&["notice.date"]);
    assert!(result.dated.is_empty());assert!(result.unresolved.is_empty());
}

#[test]
fn chronology_keeps_independent_equal_dates_and_excludes_unreviewed_or_withdrawn_values() {
    let mut s=accepted(ingest(&initial("Equal dates".into()),0,Role::Client,"client".into(),"Notices".into(),b"First: 2024-02-29.\nSecond: 2024-02-29.\nUnreviewed: 2024-01-01.".to_vec()).unwrap());
    for id in [2,1] {
        s=accepted(review(&s,s.matter.revision,Role::Client,"client".into(),Reference{id,revision:1},"date".into(),"2024-02-29".into(),true).unwrap());
    }
    assert_eq!(reviewed_chronology(&s,&["date"]).dated.iter().map(|e|e.node.id).collect::<Vec<_>>(),vec![1,2]);
    s=accepted(withdraw(&s,s.matter.revision,Role::Client,"client".into(),Reference{id:1,revision:2}).unwrap());
    let result=reviewed_chronology(&s,&["date"]);assert_eq!(result.dated.len(),1);assert_eq!(result.dated[0].node.id,2);
    assert!(reviewed_chronology(&s,&["unknown.aspect"]).dated.is_empty());
}

fn reviewed_chronology(session: &Session, facets: &[&str]) -> Chronology {
    chronology(session, &current(&session.matter.nodes,&session.matter.sources).unwrap().references, &facets.iter().map(|s|s.to_string()).collect::<Vec<_>>()).unwrap()
}

#[test]
fn chronology_combines_only_the_selected_date_aspects_without_duplicate_entries() {
    let mut s=initial("Related dates".into());
    for (facet,value) in [("notice.date","2024-03-01"),("response.date","2024-03-02"),("hearing.date","2024-04-01")] {
        s=assert_fact(&s,facet,value);
    }
    let result=reviewed_chronology(&s,&["response.date","notice.date","notice.date"]);
    assert_eq!(result.dated.iter().map(|e|e.node.facet.as_str()).collect::<Vec<_>>(),vec!["notice.date","response.date"]);
    assert!(result.unresolved.is_empty());
}

fn repeated_resource_journal() -> String {
    let mut journal=initialJournal("Resource revisions".into());
    for content in ["First resource\nSecond line", "Second resource"] {
        let session=replay(journal.clone()).unwrap().session;
        let result=commit(journal,&session,"ingest".into(),"client".into(),&["Records".into(),content.into()]).unwrap();
        assert_eq!(result.code,"");journal=result.journal;
    }
    journal
}

#[test]
fn resource_location_replaces_only_the_intended_equal_named_source() {
    let journal=repeated_resource_journal();let s=replay(journal.clone()).unwrap().session;
    let ambiguous=replaceResource(journal.clone(),&s,"client".into(),"Records".into(),"Replacement".into(),"".into()).unwrap();
    assert!(!ambiguous.code.is_empty());assert_eq!(ambiguous.journal,journal);assert_eq!(ambiguous.session,s);
    let replacement=replaceResource(journal,&s,"client".into(),"Records".into(),"Replacement".into(),"Records · resource 2 · line 1".into()).unwrap();
    assert_eq!(replacement.code,"");
    let first=s.matter.sources.iter().find(|r|r.id==1).unwrap();
    assert_eq!(replacement.session.matter.sources.iter().find(|r|r.id==1).unwrap(),first);
    let changed=replacement.session.matter.sources.iter().find(|r|r.id==2).unwrap();
    assert_eq!(changed.revision,2);assert_eq!(changed.content,b"Replacement");
    assert_eq!(replacement.session.sourceHistory,vec![s.matter.sources.iter().find(|r|r.id==2).unwrap().clone()]);
    assert_eq!(replay(replacement.journal).unwrap().session,replacement.session);
}

#[test]
fn invalid_historical_or_unauthorized_resource_selection_preserves_everything() {
    let journal=repeated_resource_journal();let s=replay(journal.clone()).unwrap().session;
    for (role,title,location) in [("client","Records","Records · resource 2 · line 9"),("client","Other","Records · resource 2 · line 1"),("reader","Records","Records · resource 2 · line 1")] {
        let refused=replaceResource(journal.clone(),&s,role.into(),title.into(),"Replacement".into(),location.into()).unwrap();
        assert!(!refused.code.is_empty());assert_eq!(refused.session,s);assert_eq!(refused.journal,journal);
    }
    let replaced=replaceResource(journal,&s,"client".into(),"".into(),"Replacement".into(),"Records · resource 2 · line 1".into()).unwrap();assert_eq!(replaced.code,"");
    let refused=replaceResource(replaced.journal.clone(),&replaced.session,"client".into(),"Records".into(),"Another".into(),"Records · resource 2 · earlier version 1 · line 1".into()).unwrap();
    assert!(!refused.code.is_empty());assert_eq!(refused.session,replaced.session);assert_eq!(refused.journal,replaced.journal);
}

#[test]
fn resource_selection_remains_available_after_its_interpretations_are_withdrawn() {
    let journal=repeated_resource_journal();let s=replay(journal.clone()).unwrap().session;
    let reviewed=commit(journal,&s,"review".into(),"client".into(),&["3".into(),"1".into(),"fact".into(),"Reviewed resource".into(),"true".into()]).unwrap();assert_eq!(reviewed.code,"");
    let withdrawn=commit(reviewed.journal,&reviewed.session,"withdraw".into(),"client".into(),&["3".into(),"2".into()]).unwrap();assert_eq!(withdrawn.code,"");
    let replaced=replaceResource(withdrawn.journal,&withdrawn.session,"client".into(),"".into(),"Corrected resource".into(),"Records · resource 2 · line 1".into()).unwrap();
    assert_eq!(replaced.code,"");assert_eq!(replaced.session.matter.sources.iter().find(|r|r.id==2).unwrap().content,b"Corrected resource");
}

#[test]
fn csv_cells_decode_quoting_without_losing_original_evidence_or_accepting_facts() {
    let bytes = "\u{feff}person,notes,amount\r\nZoë,\"said \"\"yes\"\", then\r\nleft\",50\r\n李,,75\r\n".as_bytes().to_vec();
    let s = accepted(ingestCsv(&initial("Table".into()),0,Role::Client,"client".into(),"Records".into(),bytes.clone()).unwrap());
    assert_eq!(s.labels[0].format,"csv");assert_eq!(s.matter.sources[0].content,bytes);
    let values:Vec<_>=s.matter.nodes.iter().map(|n|(n.facet.as_str(),n.value.as_str())).collect();
    assert_eq!(values,vec![("person","Zoë"),("notes","said \"yes\", then\r\nleft"),("amount","50"),("person","李"),("amount","75")]);
    for n in &s.matter.nodes {
        assert!(!n.accepted);assert!(n.dependencies.is_empty());assert_eq!(n.citations.len(),1);
        let c=&n.citations[0];assert_eq!(c.quote,bytes[c.start as usize..(c.start+c.size)as usize]);
        assert!(citationsCurrent(&s.matter.sources,&n.citations));
    }
    assert_eq!(String::from_utf8(s.matter.nodes[1].citations[0].quote.clone()).unwrap(),"\"said \"\"yes\"\", then\r\nleft\"");
    assert_eq!(interpretationLocation(&s,&s.matter.nodes[1]).unwrap(),"Records · row 2 · column 2");
    assert_eq!(interpretationLocation(&s,&s.matter.nodes[4]).unwrap(),"Records · row 3 · column 3");
    assert!(current(&s.matter.nodes,&s.matter.sources).unwrap().references.is_empty());
}

#[test]
fn csv_malformed_or_over_bound_input_refuses_the_entire_transaction() {
    let s=assert_fact(&initial("Table".into()),"goal","Understand the records");
    for text in ["", "a,a\n1,2", ",a\n1,2", "a,b\n1", "a,b\n1,2,3", "a\n\"unclosed", "a\n\"closed\"junk", "a\nba\"re", "a\r1", "a,b\n1,2\n\n", "a,b\n1,2\rX", "a\n\"\"\""] {
        let outcome=ingestCsv(&s,s.matter.revision,Role::Client,"client".into(),"Table".into(),text.as_bytes().to_vec()).unwrap();
        assert!(!outcome.code.is_empty(),"must reject {text:?}");assert_eq!(outcome.session,s);
    }
    for bytes in [vec![255],vec![b'x';8193],format!("{}\n1","x".repeat(129)).into_bytes(),format!("a\n{}","1\n".repeat(64)).into_bytes(),format!("a\n{}","x,".repeat(1024)).into_bytes()] {
        let outcome=ingestCsv(&s,s.matter.revision,Role::Client,"client".into(),"Table".into(),bytes).unwrap();
        assert!(!outcome.code.is_empty());assert_eq!(outcome.session,s);
    }
}

#[test]
fn csv_empty_cells_are_not_assertions_and_final_newlines_do_not_create_rows() {
    for text in ["a,b\n,yes", "a,b\n\"\",yes\n", "a,b\r\n,\"yes\"\r\n"] {
        let s=accepted(ingestCsv(&initial("Table".into()),0,Role::Client,"client".into(),"Records".into(),text.as_bytes().to_vec()).unwrap());
        assert_eq!(s.matter.nodes.len(),1);assert_eq!(s.matter.nodes[0].facet,"b");assert_eq!(s.matter.nodes[0].value,"yes");
    }
    for text in ["a,b", "a,b\n", "a,b\n,", "a,b\n\"\",\"\""] {
        let s=initial("Table".into());let refused=ingestCsv(&s,0,Role::Client,"client".into(),"Records".into(),text.as_bytes().to_vec()).unwrap();
        assert_eq!(refused.code,"source-empty-or-node-limit");assert_eq!(refused.session,s);
    }
}

fn csv_journal(text:&str)->JournalResult {
    let journal=initialJournal("Table".into());let s=replay(journal.clone()).unwrap().session;
    let imported=commit(journal,&s,"ingest-csv".into(),"client".into(),&vec!["Records".into(),text.into()]).unwrap();
    assert_eq!(imported.code,"");imported
}

#[test]
fn csv_review_uses_the_cell_and_heading_instead_of_transferring_another_cells_meaning() {
    let imported=csv_journal("amount,person\n50,50\n75,50");
    let a=reviewNext(imported.journal,&imported.session,"client".into(),"".into(),"fifty".into()).unwrap();assert_eq!(a.code,"");
    let view=reviewView(&a.session,&nextReview(&a.session).unwrap().unwrap(),Role::Client).unwrap();
    assert_eq!(view.suggestion,"person");assert_eq!(view.explanation,"50");
    let b=reviewNext(a.journal,&a.session,"client".into(),"".into(),"".into()).unwrap();assert_eq!(b.code,"");
    assert!(b.session.matter.nodes.iter().any(|n|n.accepted&&n.facet=="person"&&n.value=="50"));
    assert_eq!(replay(b.journal.clone()).unwrap().session,b.session);
    let c=reviewNext(b.journal,&b.session,"client".into(),"payment.amount".into(),"".into()).unwrap();assert_eq!(c.code,"");
    assert!(c.session.matter.nodes.iter().any(|n|n.accepted&&n.facet=="payment.amount"&&n.value=="75"));
}

#[test]
fn csv_replacement_retains_format_and_history_and_invalidates_reviewed_dates() {
    let imported=csv_journal("date\n2024-03-01\n2024-02-29");
    let first=reviewNext(imported.journal,&imported.session,"client".into(),"".into(),"".into()).unwrap();
    let second=reviewNext(first.journal,&first.session,"client".into(),"".into(),"".into()).unwrap();assert_eq!(second.code,"");
    assert_eq!(reviewed_chronology(&second.session,&["date"]).dated.len(),2);
    let original=second.session.matter.sources[0].clone();
    let changed=replaceResource(second.journal.clone(),&second.session,"client".into(),"Records".into(),"date\n2024-03-02".into(),"Records · row 2 · column 1".into()).unwrap();assert_eq!(changed.code,"");
    assert_eq!(changed.session.sourceHistory,vec![original]);assert!(reviewed_chronology(&changed.session,&["date"]).dated.is_empty());
    assert_eq!(interpretationLocation(&changed.session,&changed.session.matter.nodes[0]).unwrap(),"Records · earlier version 1 · row 2 · column 1");
    assert_eq!(nextReview(&changed.session).unwrap().unwrap().value,"2024-03-02");
    assert_eq!(replay(changed.journal.clone()).unwrap().session,changed.session);
    let failed=replaceResource(changed.journal.clone(),&changed.session,"client".into(),"Records".into(),"date,other\n1".into(),"".into()).unwrap();assert_eq!(failed.code,"csv-format-or-limit");assert_eq!(failed.session,changed.session);assert_eq!(failed.journal,changed.journal);
}

#[test]
fn csv_import_and_privileged_review_follow_existing_permissions() {
    let s=initial("Table".into());let refused=ingestCsv(&s,0,Role::Reader,"reader".into(),"Records".into(),b"a\n1".to_vec()).unwrap();assert_eq!(refused.session,s);assert!(!refused.code.is_empty());
    let imported=csv_journal("authority\nA source provision.");
    let view=reviewView(&imported.session,&nextReview(&imported.session).unwrap().unwrap(),Role::Client).unwrap();
    assert_eq!(nextStep(&imported.session,Role::Client,&view).unwrap(),"");
    assert_eq!(nextStep(&imported.session,Role::Reader,&view).unwrap(),"");
    let refused=reviewNext(imported.journal.clone(),&imported.session,"client".into(),"".into(),"".into()).unwrap();assert_eq!(refused.code,"lawyer-review-required");assert_eq!(refused.session,imported.session);assert_eq!(refused.journal,imported.journal);
    let accepted=reviewNext(imported.journal,&imported.session,"lawyer".into(),"".into(),"".into()).unwrap();assert_eq!(accepted.code,"");assert!(accepted.session.matter.nodes[0].accepted);
}

#[test]
fn csv_reviewed_exception_retracts_a_previously_accepted_strategy() {
    let s=reviewed_matter();let rule=s.rules[0].clone();
    let s=accepted(propose(&s,s.matter.revision,Role::Lawyer,"lawyer".into(),rule.definition).unwrap());
    let conclusion=s.matter.nodes.iter().max_by_key(|n|n.id).unwrap().clone();
    let s=accepted(review(&s,s.matter.revision,Role::Lawyer,"lawyer".into(),nodeReference(&conclusion),conclusion.facet,conclusion.value,true).unwrap());
    let s=accepted(ingestCsv(&s,s.matter.revision,Role::Client,"client".into(),"Withdrawal register".into(),b"notice.withdrawal\nwithdrawn".to_vec()).unwrap());
    assert_eq!(assess(&s.rules[0],&s.matter.nodes,&s.matter.sources).unwrap().status,ReasoningStatus::Supported);
    let cell=s.matter.nodes.iter().max_by_key(|n|n.id).unwrap().clone();
    let s=accepted(review(&s,s.matter.revision,Role::Client,"client".into(),nodeReference(&cell),cell.facet,cell.value,true).unwrap());
    assert_eq!(assess(&s.rules[0],&s.matter.nodes,&s.matter.sources).unwrap().status,ReasoningStatus::Excepted);
    assert!(!s.matter.nodes.iter().find(|n|n.id==conclusion.id).unwrap().accepted);
}

#[test]
fn csv_rows_do_not_share_header_citations_that_invent_conflicts_between_records() {
    let imported=csv_journal("amount\n50\n75");
    let first=reviewNext(imported.journal,&imported.session,"client".into(),"".into(),"".into()).unwrap();
    let second=reviewNext(first.journal,&first.session,"client".into(),"".into(),"".into()).unwrap();assert_eq!(second.code,"");
    let nodes=&second.session.matter.nodes;let admitted=current(nodes,&second.session.matter.sources).unwrap();
    for node in nodes {assert!(!competingMeaning(nodes,&admitted.references,node));}
    assert_ne!(nodes[0].citations,nodes[1].citations);
}

#[test]
fn csv_resource_and_cell_limits_accept_the_boundary_and_refuse_the_next_cell() {
    let s=initial("Bounded table".into());
    let at_bytes=format!("a\n{}","x".repeat(8190));assert_eq!(at_bytes.len(),8192);
    let imported=accepted(ingestCsv(&s,0,Role::Client,"client".into(),"Bytes".into(),at_bytes.into_bytes()).unwrap());assert_eq!(imported.matter.nodes[0].value.len(),8190);
    assert_eq!(nextAttention(&imported).unwrap().node.unwrap().value.len(),8190);
    let headers=(0..512).map(|i|format!("a{i}")).collect::<Vec<_>>().join(",");
    let values=vec!["x";512].join(",");let table=format!("{headers}\n{values}");
    let imported=accepted(ingestCsv(&s,0,Role::Client,"client".into(),"Cells".into(),table.into_bytes()).unwrap());assert_eq!(imported.matter.nodes.len(),512);
    let refused=ingestCsv(&s,0,Role::Client,"client".into(),"Cells".into(),format!("{headers},extra\n{values},x").into_bytes()).unwrap();assert_eq!(refused.code,"csv-format-or-limit");assert_eq!(refused.session,s);
    let headers=(0..16).map(|i|format!("a{i}")).collect::<Vec<_>>().join(",");
    let rows=vec![vec!["x";16].join(",");63].join("\n");
    let dense=accepted(ingestCsv(&s,0,Role::Client,"client".into(),"Rows".into(),format!("{headers}\n{rows}").into_bytes()).unwrap());assert_eq!(dense.matter.nodes.len(),1008);
    let with_rule=reviewed_matter();
    let combined=accepted(ingestCsv(&with_rule,with_rule.matter.revision,Role::Client,"client".into(),"Rows".into(),format!("{headers}\n{rows}").into_bytes()).unwrap());
    assert!(combined.matter.nodes.len()>1008);assert_eq!(assess(&combined.rules[0],&combined.matter.nodes,&combined.matter.sources).unwrap().status,ReasoningStatus::Supported);
    assert_eq!(nextAttention(&combined).unwrap().node.unwrap().value,"notice disputed");
    assert_eq!(overview(&combined,Role::Client).unwrap().stage,"review");
}

#[test]
fn csv_additional_learning_preserves_column_context_for_equal_cell_values() {
    let imported=csv_journal("amount,person\n50,50\n50,50");
    let mut result=imported;
    for _ in 0..4 {result=reviewNext(result.journal,&result.session,"client".into(),"".into(),"".into()).unwrap();assert_eq!(result.code,"");}
    assert!(nextAdditionalReview(&result.session).unwrap().node.is_none(),"equal bare values in another column must not invent an additional aspect");
    let fields=vec![result.journal.clone(),"client".into(),"amount".into(),"50".into(),"claimed.amount".into(),"50".into(),"Records · row 2 · column 1".into()];
    let result=changeFields("annotate".into(),&fields,result.journal.clone(),&result.session,"client".into()).unwrap();
    assert_eq!(result.code,"");let additional=nextAdditionalReview(&result.session).unwrap();
    assert_eq!(additional.meaning.facet,"claimed.amount");
    assert_eq!(interpretationLocation(&result.session,&additional.node.unwrap()).unwrap(),"Records · row 3 · column 1");
}

#[test]
fn source_context_shows_the_whole_csv_record_including_empty_cells() {
    let imported=csv_journal("person,notes,date\r\nZoë,\"first\r\nsecond\",2024-02-29\r\n李,,2024-03-01");
    let s=&imported.session;let source=&s.matter.sources[0];
    let selected=matchingSourceVersions(&s.matter.sources,s,"Records".into(),"Records · row 2 · column 2".into()).unwrap();assert_eq!(selected.count,1);
    let context=resourceContent(source,true,selected.citation).unwrap().unwrap();
    assert_eq!(context.scope,"CSV source · row 2");assert_eq!(context.focusIndex,1);assert_eq!(context.items.len(),3);
    assert_eq!(context.items.iter().map(|i|(i.heading.as_str(),i.value.as_str())).collect::<Vec<_>>(),vec![("person","Zoë"),("notes","first\r\nsecond"),("date","2024-02-29")]);
    let selected=matchingSourceVersions(&s.matter.sources,s,"".into(),"Records · row 3 · column 3".into()).unwrap();
    let context=resourceContent(source,true,selected.citation).unwrap().unwrap();
    assert_eq!(context.items.len(),3);assert_eq!(context.items[1].value,"");assert_eq!(context.items[2].value,"2024-03-01");
    assert!(s.matter.nodes.iter().all(|n|!n.accepted));
}

#[test]
fn text_source_context_opens_the_page_containing_the_original_utf8_passage() {
    let text=(1..=24).map(|i|format!("Zoë line {i}\r")).collect::<Vec<_>>().join("\n");
    let s=accepted(ingest(&initial("Text".into()),0,Role::Client,"client".into(),"Records".into(),text.as_bytes().to_vec()).unwrap());
    let selected=matchingSourceVersions(&s.matter.sources,&s,"Records".into(),"Records · line 20".into()).unwrap();assert_eq!(selected.count,1);
    let context=resourceContent(&s.matter.sources[0],false,selected.citation).unwrap().unwrap();
    assert_eq!(context.focusIndex,19);assert_eq!(resourcePageNumber("".into(),context.focusIndex).unwrap(),Some(3));
    let page=sourceItemPage(&context.items,16,8).unwrap();assert_eq!(page.values.len(),8);assert!(page.values[0].starts_with("line 17 — Zoë line 17"));assert!(page.values[3].contains("Zoë line 20"));
    assert_eq!(s.matter.sources[0].content,text.as_bytes());
}

#[test]
fn source_context_resolves_retained_versions_without_mixing_new_rows_or_headings() {
    let imported=csv_journal("person,notes,date\nZoë,original,2024-02-29");
    let changed=replaceResource(imported.journal,&imported.session,"client".into(),"Records".into(),"person,date\n李,2024-03-01".into(),"".into()).unwrap();assert_eq!(changed.code,"");
    let s=&changed.session;let versions=[s.matter.sources.clone(),s.sourceHistory.clone()].concat();
    let selected=matchingSourceVersions(&versions,s,"".into(),"Records · earlier version 1 · row 2 · column 2".into()).unwrap();assert_eq!(selected.count,1);
    let source=selected.source.unwrap();assert_eq!(source.revision,1);
    let content=resourceContent(&source,true,selected.citation).unwrap().unwrap();assert_eq!(content.items.len(),3);assert_eq!(content.items[1].heading,"notes");assert_eq!(content.items[1].value,"original");
    let current=matchingSourceVersions(&versions,s,"".into(),"Records · row 2 · column 2".into()).unwrap();assert_eq!(current.count,1);
    let content=resourceContent(&current.source.unwrap(),true,current.citation).unwrap().unwrap();assert_eq!(content.items.len(),2);assert_eq!(content.items[1].heading,"date");assert_eq!(content.items[1].value,"2024-03-01");
    assert_eq!(replay(changed.journal).unwrap().session,*s);
}

#[test]
fn source_context_browses_duplicate_names_and_refuses_inconsistent_selection() {
    let journal=repeated_resource_journal();let s=replay(journal.clone()).unwrap().session;
    assert_eq!(matchingSourceVersions(&s.matter.sources,&s,"Records".into(),"".into()).unwrap().count,2);
    let catalogue=sourceCatalogueItems(&s.matter.sources,&s).unwrap();assert_eq!(catalogue.values.len(),2);assert!(catalogue.values.iter().any(|v|v=="Records · resource 1 · line 1"));assert!(catalogue.values.iter().any(|v|v=="Records · resource 2 · line 1"));
    for (title,location) in [("Missing","Records · resource 1 · line 1"),("Records","Records · line 1"),("Records","Records · resource 9 · line 1")] {
        assert_eq!(matchingSourceVersions(&s.matter.sources,&s,title.into(),location.into()).unwrap().count,0);
    }
    let selected=matchingSourceVersions(&s.matter.sources,&s,"".into(),"Records · resource 2 · line 1".into()).unwrap();assert_eq!(selected.count,1);assert_eq!(selected.source.unwrap().content,b"Second resource");
    assert_eq!(replay(journal).unwrap().session,s);
}

#[test]
fn source_context_paginates_wide_rows_around_the_selected_cell_with_no_missing_cells() {
    let headers=(0..512).map(|i|format!("a{i}")).collect::<Vec<_>>().join(",");let values=(0..512).map(|i|i.to_string()).collect::<Vec<_>>().join(",");
    let s=accepted(ingestCsv(&initial("Table".into()),0,Role::Client,"client".into(),"Records".into(),format!("{headers}\n{values}").into_bytes()).unwrap());
    let focus=s.matter.nodes[500].citations[0].clone();let content=resourceContent(&s.matter.sources[0],true,Some(focus)).unwrap().unwrap();assert_eq!(content.items.len(),512);assert_eq!(content.focusIndex,500);
    assert_eq!(resourcePageNumber("".into(),500).unwrap(),Some(63));
    let page=sourceItemPage(&content.items,496,8).unwrap();assert_eq!(page.values.len(),8);assert!(page.values[4].contains("column 501 — a500: 500"));
    let last=sourceItemPage(&content.items,504,8).unwrap();assert_eq!(last.values.len(),8);assert!(last.values[7].contains("a511: 511"));
    for page in ["0","129","-1","1x","01"] {assert_eq!(resourcePageNumber(page.into(),0).unwrap(),None);}
}

#[test]
fn selected_pending_passage_review_preserves_other_sources_and_replays_exactly() {
    let journal=repeated_resource_journal();let s=replay(journal.clone()).unwrap().session;
    let selected=reviewLocated(journal,&s,"client".into(),"record.kind".into(),"second".into(),"Records · resource 2 · line 1".into()).unwrap();
    assert_eq!(selected.code,"");
    let node=selected.session.matter.nodes.iter().find(|n|n.accepted).unwrap();
    assert_eq!(node.citations[0].source,2);assert_eq!(node.value,"second");
    assert!(selected.session.matter.nodes.iter().filter(|n|n.citations[0].source==1).all(|n|!n.accepted));
    assert_eq!(replay(selected.journal.clone()).unwrap().session,selected.session);
    let following=reviewLocated(selected.journal,&selected.session,"client".into(),"record.kind".into(),"first".into(),"".into()).unwrap();
    assert_eq!(following.code,"");assert!(following.session.matter.nodes.iter().any(|n|n.accepted&&n.value=="first"&&n.citations[0].source==1));
}

#[test]
fn selected_review_refuses_accepted_withdrawn_historical_and_unknown_locations() {
    let journal=repeated_resource_journal();let s=replay(journal.clone()).unwrap().session;
    for (role,location) in [("client","Records · line 1"),("client","Records · resource 2 · line 9"),("reader","Records · resource 2 · line 1")] {
        let denied=reviewLocated(journal.clone(),&s,role.into(),"kind".into(),"second".into(),location.into()).unwrap();
        assert!(!denied.code.is_empty());assert_eq!(denied.journal,journal);assert_eq!(denied.session,s);
    }
    let accepted=reviewLocated(journal,&s,"client".into(),"kind".into(),"second".into(),"Records · resource 2 · line 1".into()).unwrap();assert_eq!(accepted.code,"");
    let denied=reviewLocated(accepted.journal.clone(),&accepted.session,"client".into(),"kind".into(),"rewritten".into(),"Records · resource 2 · line 1".into()).unwrap();assert_eq!(denied.code,"select-passage");assert_eq!(denied.session,accepted.session);
    let withdrawn=alterInterpretation(accepted.journal,&accepted.session,"withdraw".into(),"client".into(),&["".into(),"client".into(),"kind".into(),"second".into(),"Records · resource 2 · line 1".into()]).unwrap();assert_eq!(withdrawn.code,"");
    let denied=reviewLocated(withdrawn.journal.clone(),&withdrawn.session,"client".into(),"kind".into(),"second".into(),"Records · resource 2 · line 1".into()).unwrap();assert_eq!(denied.code,"select-passage");assert_eq!(denied.journal,withdrawn.journal);
    let replaced=replaceResource(withdrawn.journal,&withdrawn.session,"client".into(),"Records".into(),"Replacement".into(),"Records · resource 2 · line 1".into()).unwrap();assert_eq!(replaced.code,"");
    let denied=reviewLocated(replaced.journal.clone(),&replaced.session,"client".into(),"kind".into(),"old".into(),"Records · resource 2 · earlier version 1 · line 1".into()).unwrap();assert_eq!(denied.code,"select-passage");assert_eq!(denied.journal,replaced.journal);
}

#[test]
fn source_context_review_form_is_bound_to_current_pending_location_and_role() {
    let imported=csv_journal("person,authority\nZoë,Reviewed provision");
    let cell=imported.session.matter.nodes.iter().find(|n|n.facet=="authority").unwrap();let citation=cell.citations[0].clone();
    assert_eq!(sourceReviewStep(&imported.session,Role::Client,Some(citation.clone())).unwrap(),"");
    assert_eq!(sourceReviewStep(&imported.session,Role::Reader,Some(citation.clone())).unwrap(),"");
    let prepared=sourceReviewStep(&imported.session,Role::Lawyer,Some(citation.clone())).unwrap();
    assert!(prepared.starts_with("review\u{1f}"));assert!(prepared.contains("Records · row 2 · column 2"));
    let reviewed=reviewLocated(imported.journal,&imported.session,"lawyer".into(),"".into(),"".into(),"Records · row 2 · column 2".into()).unwrap();assert_eq!(reviewed.code,"");
    assert_eq!(sourceReviewStep(&reviewed.session,Role::Lawyer,Some(citation)).unwrap(),"");
    assert!(!reviewed.session.matter.nodes.iter().find(|n|n.facet=="person").unwrap().accepted);
}

#[test]
fn selected_csv_review_uses_the_selected_decoded_cell_and_preserves_raw_citation() {
    let imported=csv_journal("person,notes\nZoë,\"said \"\"yes\"\", then\nleft\"");
    let raw=imported.session.matter.nodes.iter().find(|n|n.facet=="notes").unwrap().citations.clone();
    let reviewed=reviewLocated(imported.journal,&imported.session,"client".into(),"".into(),"".into(),"Records · row 2 · column 2".into()).unwrap();assert_eq!(reviewed.code,"");
    let cell=reviewed.session.matter.nodes.iter().find(|n|n.accepted).unwrap();assert_eq!(cell.facet,"notes");assert_eq!(cell.value,"said \"yes\", then\nleft");assert_eq!(cell.citations,raw);
    assert!(citationsCurrent(&reviewed.session.matter.sources,&cell.citations));
    assert_eq!(replay(reviewed.journal).unwrap().session,reviewed.session);
}

fn strategy_journal() -> JournalResult {
    let journal=initialJournal("Proposal review".into());let s=replay(journal.clone()).unwrap().session;
    let r=commit(journal,&s,"ingest".into(),"client".into(),&["Notice".into(),"notice received".into()]).unwrap();assert_eq!(r.code,"");
    let r=reviewNext(r.journal,&r.session,"client".into(),"notice.receipt".into(),"received".into()).unwrap();assert_eq!(r.code,"");
    let r=setContext(r.journal,&r.session,"client".into(),"goal".into(),"Respond".into()).unwrap();assert_eq!(r.code,"");
    let r=setContext(r.journal,&r.session,"client".into(),"jurisdiction".into(),"Reviewed jurisdiction".into()).unwrap();assert_eq!(r.code,"");
    let r=commit(r.journal,&r.session,"ingest".into(),"lawyer".into(),&["Authority".into(),"A received notice permits a response unless withdrawn.".into()]).unwrap();assert_eq!(r.code,"");
    let r=reviewNext(r.journal,&r.session,"lawyer".into(),"authority".into(),"Reviewed source".into()).unwrap();assert_eq!(r.code,"");
    let r=addRule(r.journal,&r.session,"lawyer".into(),"Reviewed source".into(),"Respond".into(),"notice.receipt = received".into(),"notice.withdrawal = withdrawn".into(),"Prepare a response.".into()).unwrap();assert_eq!(r.code,"");r
}

#[test]
fn proposal_creation_refuses_repeated_support_and_allows_a_fresh_review_after_retraction() {
    let s=reviewed_matter();let rule=s.rules[0].clone();
    assert!(strategyNext(&s,Role::Lawyer,&rule).unwrap().starts_with("propose\u{1f}"));
    let s=accepted(proposeCurrent(&s,s.matter.revision,Role::Lawyer,"lawyer".into(),rule.definition).unwrap());
    let assessment=assess(&rule,&s.matter.nodes,&s.matter.sources).unwrap();let node=currentProposal(&s,&assessment).unwrap().unwrap();assert!(!node.accepted);
    let refused=proposeCurrent(&s,s.matter.revision,Role::Lawyer,"lawyer".into(),rule.definition).unwrap();assert_eq!(refused.code,"proposal-already-current");assert_eq!(refused.session,s);
    let s=accepted(review(&s,s.matter.revision,Role::Lawyer,"lawyer".into(),nodeReference(&node),node.facet.clone(),node.value.clone(),true).unwrap());
    assert!(strategyNext(&s,Role::Lawyer,&rule).unwrap().starts_with("inspect\u{1f}"));
    assert_eq!(proposeCurrent(&s,s.matter.revision,Role::Lawyer,"lawyer".into(),rule.definition).unwrap().session,s);
    let s=assert_fact(&s,"notice.withdrawal","withdrawn");assert!(currentProposal(&s,&assess(&rule,&s.matter.nodes,&s.matter.sources).unwrap()).unwrap().is_none());
    let exception=s.matter.nodes.iter().find(|n|n.facet=="notice.withdrawal").unwrap().clone();
    let s=accepted(withdraw(&s,s.matter.revision,Role::Client,"client".into(),nodeReference(&exception)).unwrap());
    assert!(currentProposal(&s,&assess(&rule,&s.matter.nodes,&s.matter.sources).unwrap()).unwrap().is_none());
    let s=accepted(proposeCurrent(&s,s.matter.revision,Role::Lawyer,"lawyer".into(),rule.definition).unwrap());
    let fresh=currentProposal(&s,&assess(&rule,&s.matter.nodes,&s.matter.sources).unwrap()).unwrap().unwrap();assert_ne!(fresh.id,node.id);assert!(!fresh.accepted);
}

#[test]
fn legacy_duplicate_proposals_replay_but_new_commands_preserve_the_journal_on_repetition() {
    let mut r=strategy_journal();let fields=referenceFields(r.session.rules[0].definition).values;
    for _ in 0..2 {r=commit(r.journal,&r.session,"propose".into(),"lawyer".into(),&fields).unwrap();assert_eq!(r.code,"");}
    assert_eq!(replay(r.journal.clone()).unwrap().session,r.session);
    let rule=r.session.rules[0].clone();let first=currentProposal(&r.session,&assess(&rule,&r.session.matter.nodes,&r.session.matter.sources).unwrap()).unwrap().unwrap();
    assert_eq!(first.id,r.session.matter.nodes.iter().filter(|n|n.origin==Origin::Inferred).map(|n|n.id).min().unwrap());
    let denied=commit(r.journal.clone(),&r.session,"propose-current".into(),"lawyer".into(),&fields).unwrap();assert_eq!(denied.code,"proposal-already-current");assert_eq!(denied.journal,r.journal);assert_eq!(denied.session,r.session);
    let reviewed=reviewStrategyProposal(r.journal,&r.session,"lawyer".into(),"Prepare a response.".into()).unwrap();assert_eq!(reviewed.code,"");
    let selected=currentProposal(&reviewed.session,&assess(&rule,&reviewed.session.matter.nodes,&reviewed.session.matter.sources).unwrap()).unwrap().unwrap();assert!(selected.accepted);assert_eq!(selected.id,first.id);
    assert_eq!(replay(reviewed.journal).unwrap().session,reviewed.session);
}

#[test]
fn strategy_review_selects_its_own_proposal_instead_of_another_pending_rule() {
    let mut r=strategy_journal();
    r=addRule(r.journal,&r.session,"lawyer".into(),"Reviewed source".into(),"Respond".into(),"notice.receipt = received".into(),"notice.withdrawal = withdrawn".into(),"Seek clarification.".into()).unwrap();assert_eq!(r.code,"");
    let first=r.session.rules.iter().find(|x|x.action=="Prepare a response.").unwrap().clone();let second=r.session.rules.iter().find(|x|x.action=="Seek clarification.").unwrap().clone();
    for rule in [&first,&second] {r=commit(r.journal,&r.session,"propose-current".into(),"lawyer".into(),&referenceFields(rule.definition).values).unwrap();assert_eq!(r.code,"");}
    let a=currentProposal(&r.session,&assess(&first,&r.session.matter.nodes,&r.session.matter.sources).unwrap()).unwrap().unwrap();let b=currentProposal(&r.session,&assess(&second,&r.session.matter.nodes,&r.session.matter.sources).unwrap()).unwrap().unwrap();assert_ne!(a.id,b.id);assert_eq!(nextReview(&r.session).unwrap().unwrap().id,b.id);
    assert!(strategyNext(&r.session,Role::Lawyer,&first).unwrap().starts_with("review-proposal\u{1f}"));assert!(strategyNext(&r.session,Role::Lawyer,&first).unwrap().contains("Prepare a response."));assert_eq!(strategyNext(&r.session,Role::Client,&first).unwrap(),"");
    let denied=reviewStrategyProposal(r.journal.clone(),&r.session,"client".into(),first.action.clone()).unwrap();assert_eq!(denied.code,"lawyer-review-required");assert_eq!(denied.journal,r.journal);
    let reviewed=reviewStrategyProposal(r.journal,&r.session,"lawyer".into(),first.action).unwrap();assert_eq!(reviewed.code,"");assert!(reviewed.session.matter.nodes.iter().find(|n|n.id==a.id).unwrap().accepted);assert!(!reviewed.session.matter.nodes.iter().find(|n|n.id==b.id).unwrap().accepted);
    assert_eq!(replay(reviewed.journal).unwrap().session,reviewed.session);
}

#[test]
fn strategy_review_refuses_changed_support_and_never_fills_a_required_fact_value() {
    let r=strategy_journal();let rule=r.session.rules[0].clone();let r=commit(r.journal,&r.session,"propose-current".into(),"lawyer".into(),&referenceFields(rule.definition).values).unwrap();assert_eq!(r.code,"");
    let changed=editLocatedValue(r.journal,&r.session,"client".into(),"notice.receipt".into(),"received".into(),"not received".into(),"Notice · line 1".into()).unwrap();assert_eq!(changed.code,"");
    let denied=reviewStrategyProposal(changed.journal.clone(),&changed.session,"lawyer".into(),rule.action.clone()).unwrap();assert_eq!(denied.code,"no-pending-proposal");assert_eq!(denied.journal,changed.journal);assert_eq!(denied.session,changed.session);
    let next=strategyNext(&changed.session,Role::Lawyer,&rule).unwrap();assert!(next.starts_with("assertion\u{1f}"));assert!(next.ends_with("14:notice.receipt0:"));assert!(!next.contains("received"));
}

#[test]
fn proposal_matching_handles_large_matters_without_duplicate_nodes_or_larger_test_stacks() {
    let s=reviewed_matter();let rule=s.rules[0].clone();
    let table=(0..16).map(|i|format!("column{i}")).collect::<Vec<_>>().join(",")+"\n"+&(0..63).map(|_|vec!["1";16].join(",")).collect::<Vec<_>>().join("\n");
    let s=accepted(ingestCsv(&s,s.matter.revision,Role::Client,"client".into(),"Large table".into(),table.into_bytes()).unwrap());
    let s=accepted(proposeCurrent(&s,s.matter.revision,Role::Lawyer,"lawyer".into(),rule.definition).unwrap());assert!(s.matter.nodes.len()>1008);
    let repeated=proposeCurrent(&s,s.matter.revision,Role::Lawyer,"lawyer".into(),rule.definition).unwrap();assert_eq!(repeated.code,"proposal-already-current");assert_eq!(repeated.session,s);
}

#[test]
fn changing_goal_reorders_attention_without_accepting_source_content() {
    let s=accepted(ingest(&initial("Attention".into()),0,Role::Client,"client".into(),"Records".into(),b"repair invoice\nrent refund".to_vec()).unwrap());
    let s=assert_fact(&s,"goal","rent refund");
    assert_eq!(nextAttention(&s).unwrap().node.unwrap().id,2);
    for role in [Role::Client,Role::Lawyer,Role::Reader] {assert_eq!(overview(&s,role).unwrap().node,2);}
    assert!(s.matter.nodes.iter().filter(|n|!n.citations.is_empty()).all(|n|!n.accepted));
    let s=accepted(review(&s,s.matter.revision,Role::Client,"client".into(),node_ref(&s,"goal"),"goal".into(),"repair invoice".into(),true).unwrap());
    assert_eq!(nextAttention(&s).unwrap().node.unwrap().id,1);
    let s=accepted(withdraw(&s,s.matter.revision,Role::Client,"client".into(),node_ref(&s,"goal")).unwrap());
    assert_eq!(overview(&s,Role::Client).unwrap().stage,"goal");
    assert_eq!(nextAttention(&s).unwrap().node.unwrap().id,1,"without a current goal, preserve source order");
}

#[test]
fn repeated_goal_words_do_not_inflate_attention_and_ties_keep_source_order() {
    let s=accepted(ingest(&initial("Attention".into()),0,Role::Client,"client".into(),"Records".into(),b"rent refund\nrent rent rent rent".to_vec()).unwrap());
    let s=assert_fact(&s,"goal","rent refund");
    assert_eq!(nextAttention(&s).unwrap().node.unwrap().id,1);
    let s=accepted(review(&s,s.matter.revision,Role::Client,"client".into(),node_ref(&s,"goal"),"goal".into(),"rent rent rent rent".into(),true).unwrap());
    assert_eq!(goalFeatureOverlap(&goalContext(&s,&current(&s.matter.nodes,&s.matter.sources).unwrap().references).unwrap(),&features("rent rent rent rent".into()).unwrap().values).unwrap(),2,"one distinct word and one ordered pair");
    let s=accepted(review(&s,s.matter.revision,Role::Client,"client".into(),node_ref(&s,"goal"),"goal".into(),"rent".into(),true).unwrap());
    assert_eq!(nextAttention(&s).unwrap().node.unwrap().id,1,"equal lexical scores preserve earliest passage");
}

#[test]
fn a_learned_missing_aspect_competes_with_unrelated_new_passages() {
    let s=jointly_reviewed_amounts();
    let s=accepted(review(&s,s.matter.revision,Role::Client,"client".into(),node_ref(&s,"goal"),"goal".into(),"Tuesday".into(),true).unwrap());
    let s=accepted(ingest(&s,s.matter.revision,Role::Client,"client".into(),"Other".into(),b"An unrelated item".to_vec()).unwrap());
    let focus=nextAttention(&s).unwrap();assert!(focus.additional);assert_eq!(focus.node.unwrap().id,2);assert_eq!(focus.meaning.value,"Tuesday");
    assert_eq!(overview(&s,Role::Client).unwrap().stage,"additional-interpretation");
    let s=accepted(withdraw(&s,s.matter.revision,Role::Client,"client".into(),node_ref(&s,"day")).unwrap());
    let focus=nextAttention(&s).unwrap();assert!(!focus.additional);assert_eq!(focus.node.unwrap().value,"An unrelated item");
}

#[test]
fn unified_attention_review_commits_the_displayed_additional_aspect_and_replays() {
    let journal=initialJournal("Attention".into());let s=replay(journal.clone()).unwrap().session;
    let r=commit(journal,&s,"ingest".into(),"client".into(),&["Records".into(),"Amount: 50; day: Monday.\nAmount: 75; day: Tuesday.".into()]).unwrap();assert_eq!(r.code,"");
    let r=reviewLocated(r.journal,&r.session,"client".into(),"amount".into(),"50".into(),"Records · line 1".into()).unwrap();assert_eq!(r.code,"");
    let r=commit(r.journal,&r.session,"annotate".into(),"client".into(),&["1".into(),"2".into(),"day".into(),"Monday".into()]).unwrap();assert_eq!(r.code,"");
    let r=reviewLocated(r.journal,&r.session,"client".into(),"amount".into(),"75".into(),"Records · line 2".into()).unwrap();assert_eq!(r.code,"");
    let r=setContext(r.journal,&r.session,"client".into(),"goal".into(),"Tuesday".into()).unwrap();assert_eq!(r.code,"");
    let r=commit(r.journal,&r.session,"ingest".into(),"client".into(),&["Other".into(),"Unrelated item".into()]).unwrap();assert_eq!(r.code,"");
    let view=overview(&r.session,Role::Client).unwrap();assert_eq!(view.stage,"additional-interpretation");assert_eq!(view.node,2);
    let r=reviewNext(r.journal,&r.session,"client".into(),"".into(),"".into()).unwrap();assert_eq!(r.code,"");
    let added=r.session.matter.nodes.iter().find(|n|n.facet=="day"&&n.value=="Tuesday").unwrap();assert!(added.accepted);assert_eq!(added.citations[0].source,1);
    assert!(!r.session.matter.nodes.iter().find(|n|n.value=="Unrelated item").unwrap().accepted);
    assert_eq!(replay(r.journal).unwrap().session,r.session);
}

#[test]
fn goal_attention_selects_between_learned_aspects_of_the_same_passage() {
    let s=jointly_reviewed_amounts();
    let s=accepted(annotate(&s,s.matter.revision,Role::Client,"client".into(),Reference{id:1,revision:2},"claimed.amount".into(),"50".into()).unwrap());
    assert_eq!(nextAdditionalReview(&s).unwrap().meaning.facet,"claimed.amount","preserve prior traversal on a tie");
    let s=accepted(review(&s,s.matter.revision,Role::Client,"client".into(),node_ref(&s,"goal"),"goal".into(),"Tuesday".into(),true).unwrap());
    assert_eq!(nextAdditionalReview(&s).unwrap().meaning.facet,"day");
    let s=accepted(review(&s,s.matter.revision,Role::Client,"client".into(),node_ref(&s,"goal"),"goal".into(),"claimed.amount".into(),true).unwrap());
    assert_eq!(nextAdditionalReview(&s).unwrap().meaning.facet,"claimed.amount");
    assert!(!s.matter.nodes.iter().any(|n|n.facet=="day"&&n.value=="Tuesday"));
}

#[test]
fn attention_finishes_for_a_full_matter_of_reviewed_text_passages() {
    let mut s=initial("Reviewed archive".into());
    for index in 0..16 {
        s=accepted(ingest(&s,s.matter.revision,Role::Client,"client".into(),format!("Record {index}"),vec!["entry";63].join("\n").into_bytes()).unwrap());
    }
    s=assert_fact(&s,"goal","Understand the archive");
    assert_eq!(nextAttention(&s).unwrap().node.unwrap().id,1,"untrained passages retain source order at the matter boundary");
    let references=s.matter.nodes.iter().filter(|n|!n.citations.is_empty()).map(nodeReference).collect::<Vec<_>>();
    for reference in references {s=accepted(review(&s,s.matter.revision,Role::Client,"client".into(),reference,"entry".into(),"entry".into(),true).unwrap());}
    assert_eq!(s.matter.nodes.len(),1009);
    assert!(nextAttention(&s).unwrap().node.is_none());
    assert_eq!(overview(&s,Role::Client).unwrap().stage,"jurisdiction");
}

#[test]
fn attention_reaches_the_last_cell_at_the_intake_bound() {
    let headers=(0..16).map(|i|format!("column{i}")).collect::<Vec<_>>().join(",");
    let rows=(0..63).map(|row|(0..16).map(|column|if row==62&&column==15{"finale"}else{"entry"}).collect::<Vec<_>>().join(",")).collect::<Vec<_>>().join("\n");
    let s=assert_fact(&initial("Last cell".into()),"goal","finale");
    let s=accepted(ingestCsv(&s,s.matter.revision,Role::Client,"client".into(),"Records".into(),format!("{headers}\n{rows}").into_bytes()).unwrap());
    let selected=nextAttention(&s).unwrap().node.unwrap();assert_eq!(selected.value,"finale");assert_eq!(selected.facet,"column15");assert!(!selected.accepted);
    assert_eq!(interpretationLocation(&s,&selected).unwrap(),"Records · row 64 · column 16");
    assert_eq!(overview(&s,Role::Client).unwrap().node,selected.id);
}

#[test]
fn batched_meaning_context_preserves_the_visible_eight_aspect_limit() {
    let mut s=accepted(ingest(&initial("Context".into()),0,Role::Client,"client".into(),"Record".into(),b"Amount: 50".to_vec()).unwrap());
    s=accepted(review(&s,s.matter.revision,Role::Client,"client".into(),Reference{id:1,revision:1},"facet0".into(),"50".into(),true).unwrap());
    for index in 1..8 {s=accepted(annotate(&s,s.matter.revision,Role::Client,"client".into(),Reference{id:1,revision:2},format!("facet{index}"),"50".into()).unwrap());}
    let context=meaningContext(&s.matter.nodes,&s.matter.nodes,&s.matter.sources,"Amount: 50".into(),&[],8).unwrap();
    assert_eq!(context.values.len(),8);assert!(context.values.iter().all(|v|v.ends_with(": 50")));
    s=accepted(annotate(&s,s.matter.revision,Role::Client,"client".into(),Reference{id:1,revision:2},"facet8".into(),"50".into()).unwrap());
    let context=meaningContext(&s.matter.nodes,&s.matter.nodes,&s.matter.sources,"Amount: 50".into(),&[],8).unwrap();
    assert_eq!(context.values.len(),9);assert!(context.values[..8].iter().all(|v|v.ends_with(": 50")));assert_eq!(context.values[8],"Additional facets can be checked by selecting a facet during review.");
    assert!(meaningContext(&[],&s.matter.nodes,&s.matter.sources,"Amount: 50".into(),&[],0).unwrap().values.is_empty());
}

#[test]
fn attention_uses_the_learned_value_that_automatic_review_will_accept() {
    let journal=initialJournal("Amount attention".into());let s=replay(journal.clone()).unwrap().session;
    let r=commit(journal,&s,"ingest".into(),"client".into(),&["Training".into(),"Amount: 50.".into()]).unwrap();assert_eq!(r.code,"");
    let r=reviewNext(r.journal,&r.session,"client".into(),"amount".into(),"50".into()).unwrap();assert_eq!(r.code,"");
    let r=setContext(r.journal,&r.session,"client".into(),"goal".into(),"75".into()).unwrap();assert_eq!(r.code,"");
    let r=commit(r.journal,&r.session,"ingest".into(),"client".into(),&["Update".into(),"Unrelated context\nAmount: 75.".into()]).unwrap();assert_eq!(r.code,"");
    let before=r.session.clone();let view=overview(&r.session,Role::Client).unwrap();assert_eq!(view.suggestion,"amount");assert!(view.context.iter().any(|v|v=="amount: 75"));
    assert!(nextStep(&r.session,Role::Client,&view).unwrap().contains("Update · line 2"));assert_eq!(r.session,before);
    assert!(!r.session.matter.nodes.iter().find(|n|n.value=="Amount: 75.").unwrap().accepted);
    let r=reviewNext(r.journal,&r.session,"client".into(),"".into(),"".into()).unwrap();assert_eq!(r.code,"");
    let selected=r.session.matter.nodes.iter().find(|n|n.facet=="amount"&&n.value=="75").unwrap();assert!(selected.accepted);assert_eq!(interpretationLocation(&r.session,selected).unwrap(),"Update · line 2");
    assert!(!r.session.matter.nodes.iter().find(|n|n.value=="Unrelated context").unwrap().accepted);assert_eq!(replay(r.journal).unwrap().session,r.session);
}

#[test]
fn attention_uses_the_displayed_learned_facet_when_the_classifier_disagrees() {
    let s=reviewed_matter();
    let s=accepted(ingest(&s,s.matter.revision,Role::Client,"client".into(),"Training".into(),b"Amount: 50.".to_vec()).unwrap());
    let training=s.matter.nodes.iter().max_by_key(|n|n.id).unwrap();
    let s=accepted(review(&s,s.matter.revision,Role::Client,"client".into(),nodeReference(training),"amount".into(),"50".into(),true).unwrap());
    let s=assert_fact(&s,"context","Amount: 75.");
    let mut rule=s.rules[0].clone();rule.definition=Reference{id:0,revision:0};rule.premises=vec![Requirement{facet:"amount".into(),value:"75".into(),question:"Confirm the amount".into()}];rule.exceptions=vec![];rule.action="Review the amount".into();
    let s=accepted(commitRule(&s,s.matter.revision,Role::Lawyer,"lawyer".into(),&rule).unwrap());
    let s=accepted(ingest(&s,s.matter.revision,Role::Client,"client".into(),"Update".into(),b"Unrelated context\nAmount: 75.".to_vec()).unwrap());
    assert_eq!(suggestedFacet(&infer(&train(&s.matter.nodes,&s.matter.sources).unwrap(),"Amount: 75.".into()).unwrap()),"context");
    assert_eq!(inferMeaning(&s.matter.nodes,&s.matter.sources,"Amount: 75.".into()).unwrap().facet,"amount");
    assert_eq!(nextAttention(&s).unwrap().node.unwrap().value,"Amount: 75.");assert_eq!(overview(&s,Role::Client).unwrap().suggestion,"amount");
}

#[test]
fn disputed_learned_values_do_not_create_goal_attention_evidence() {
    let s=accepted(ingest(&initial("Disputed attention".into()),0,Role::Client,"client".into(),"Training".into(),b"Amount: 50.".to_vec()).unwrap());
    let s=accepted(review(&s,s.matter.revision,Role::Client,"client".into(),Reference{id:1,revision:1},"amount".into(),"50".into(),true).unwrap());
    let s=assert_fact(&s,"goal","75");
    let s=accepted(annotate(&s,s.matter.revision,Role::Client,"client".into(),Reference{id:1,revision:2},"amount".into(),"unknown".into()).unwrap());
    let s=accepted(ingest(&s,s.matter.revision,Role::Client,"client".into(),"Update".into(),b"Unrelated context\nAmount: 75.".to_vec()).unwrap());
    assert!(inferFacetMeaning(&s.matter.nodes,&s.matter.sources,"Amount: 75.".into(),"amount".into()).unwrap().ambiguous);
    assert_eq!(nextAttention(&s).unwrap().node.unwrap().value,"Unrelated context","an ambiguous extracted value cannot break the literal attention tie");
}

fn compiled_meanings_agree(session: &Session, queries: &[&str], facets: &[&str]) {
    let admitted=current(&session.matter.nodes,&session.matter.sources).unwrap().references;
    let model=compileMeanings(&session.matter.nodes,&session.matter.nodes,&admitted).unwrap();
    for query in queries {
        assert_eq!(inferCompiledMeaning(&model,(*query).into()).unwrap(),inferMeaning(&session.matter.nodes,&session.matter.sources,(*query).into()).unwrap(),"global meaning and complete training provenance for {query}");
        for facet in facets {
            assert_eq!(inferCompiledFacetMeaning(&model,(*query).into(),(*facet).into()).unwrap(),inferFacetMeaning(&session.matter.nodes,&session.matter.sources,(*query).into(),(*facet).into()).unwrap(),"facet {facet} and complete training provenance for {query}");
        }
    }
}

#[test]
fn compiled_training_retains_literal_joint_and_conflicting_meaning_provenance() {
    let mut s=accepted(ingest(&initial("Compiled meanings".into()),0,Role::Client,"client".into(),"Record".into(),b"Amount: 50; day: Monday.\nAmount: 75; day: Tuesday.".to_vec()).unwrap());
    let queries=["Amount: 50; day: Monday.","Amount: 75; day: Tuesday.","Unrelated text","Amount: ; day: Tuesday."];
    let facets=["amount","day","alias","missing",""];
    compiled_meanings_agree(&s,&queries,&facets);
    s=accepted(review(&s,s.matter.revision,Role::Client,"client".into(),Reference{id:1,revision:1},"amount".into(),"50".into(),true).unwrap());
    s=accepted(annotate(&s,s.matter.revision,Role::Client,"client".into(),Reference{id:1,revision:2},"day".into(),"Monday".into()).unwrap());
    s=accepted(annotate(&s,s.matter.revision,Role::Client,"client".into(),Reference{id:1,revision:2},"alias".into(),"50".into()).unwrap());
    compiled_meanings_agree(&s,&queries,&facets);
    s=accepted(annotate(&s,s.matter.revision,Role::Client,"client".into(),Reference{id:1,revision:2},"amount".into(),"unknown".into()).unwrap());
    s=accepted(annotate(&s,s.matter.revision,Role::Client,"client".into(),Reference{id:1,revision:2},"amount".into(),"disputed".into()).unwrap());
    compiled_meanings_agree(&s,&queries,&facets);
    let conflicts=s.matter.nodes.iter().filter(|n|n.value=="unknown"||n.value=="disputed").map(nodeReference).collect::<Vec<_>>();
    for conflict in conflicts {s=accepted(withdraw(&s,s.matter.revision,Role::Client,"client".into(),conflict).unwrap());}
    compiled_meanings_agree(&s,&queries,&facets);
    s=accepted(reviseSource(&s,s.matter.revision,Role::Client,"client".into(),Reference{id:1,revision:1},b"Replaced original".to_vec()).unwrap());
    compiled_meanings_agree(&s,&queries,&facets);
}

#[test]
fn correcting_a_full_intake_preserves_every_other_passage_and_its_order() {
    let mut s=initial("Complete intake".into());
    for index in 0..16 {s=accepted(ingest(&s,s.matter.revision,Role::Client,"client".into(),format!("Record {index}"),vec!["entry";63].join("\n").into_bytes()).unwrap());}
    for identifier in [1,32,33,1008] {
        let before=s.matter.nodes.clone();let selected=before.iter().find(|node|node.id==identifier).unwrap();
        s=accepted(review(&s,s.matter.revision,Role::Client,"client".into(),nodeReference(selected),"entry".into(),format!("Correction {identifier}"),true).unwrap());
        assert_eq!(s.matter.nodes.len(),before.len());
        for (old,current) in before.iter().zip(&s.matter.nodes) {
            assert_eq!(old.id,current.id);
            if old.id==identifier {assert_eq!(current.value,format!("Correction {identifier}"));assert_eq!(current.revision,old.revision+1);assert_eq!(current.citations,old.citations);assert_eq!(current.dependencies,old.dependencies);}
            else {assert_eq!(current,old);}
        }
    }
}

fn journal_fields(values: &[String]) -> String {
    values.iter().map(|value|format!("{}:{value}",value.len())).collect()
}
fn append_journal_command(journal: &mut String, values: Vec<String>) {
    let command=journal_fields(&values);journal.push_str(&format!("{}:{command}",command.len()));
}
fn full_review_journal() -> String {
    let mut journal=initialJournal("Complete archive".into());let mut revision: u64=0;
    for index in 0..16 {
        append_journal_command(&mut journal,vec!["ingest".into(),revision.to_string(),"client".into(),"client".into(),format!("Resource {}",index+1),vec!["entry";63].join("\n")]);revision+=1;
    }
    append_journal_command(&mut journal,vec!["assert".into(),revision.to_string(),"client".into(),"client".into(),"goal".into(),"Understand the archive".into()]);revision+=1;
    for identifier in 1u64..=1008 {
        append_journal_command(&mut journal,vec!["review".into(),revision.to_string(),"client".into(),"client".into(),identifier.to_string(),"1".into(),"entry".into(),"entry".into(),"true".into()]);revision+=1;
    }
    journal
}
fn correction_history(commands: usize) -> String {
    let mut journal=initialJournal("Retained corrections".into());
    append_journal_command(&mut journal,vec!["ingest".into(),"0".into(),"client".into(),"client".into(),"Record".into(),"original".into()]);
    for revision in 1..commands {
        append_journal_command(&mut journal,vec!["review".into(),revision.to_string(),"client".into(),"client".into(),"1".into(),revision.to_string(),"entry".into(),format!("value {revision}"),"true".into()]);
    }
    journal
}

#[test]
fn bounded_field_iteration_keeps_utf8_order_and_refuses_the_first_extra_field() {
    let fields=(0..2050).map(|index|format!("Zoë {index}:\n\0\u{1f}" )).collect::<Vec<_>>();let encoded=journal_fields(&fields);
    for count in [0,1,2,3,31,32,33,511,512,513,1023,1024,1025,2047,2048,2049,2050] {
        let subset=journal_fields(&fields[..count]);
        assert_eq!(decodeJournalFields(subset.clone(),count as u64).unwrap().unwrap().values,&fields[..count]);
        if count>0 {assert!(decodeJournalFields(subset,(count-1) as u64).unwrap().is_none());}
    }
    assert_eq!(decodeJournalFields(encoded.clone(),2050).unwrap().unwrap().values,fields);
    assert!(decodeJournalFields(encoded.clone(),2049).unwrap().is_none());
    assert!(decodeJournalFields(format!("{encoded}1:x"),2050).unwrap().is_none());
    assert!(decodeJournalFields(format!("{encoded}2:x"),2051).unwrap().is_none());
    assert_eq!(decodeJournalFields("".into(),0).unwrap().unwrap().values,Vec::<String>::new());
    assert!(decodeJournalFields("0:".into(),0).unwrap().is_none());
}

#[test]
fn a_full_intake_can_be_reviewed_saved_replayed_and_corrected() {
    let journal=full_review_journal();let s=accepted(replay(journal.clone()).unwrap());
    assert_eq!(s.matter.revision,1025);assert_eq!(s.matter.nodes.len(),1009);assert_eq!(s.matter.changes.len(),1008);assert_eq!(s.audit.len(),1025);
    assert!(s.matter.nodes.iter().all(|node|node.accepted));assert!(nextAttention(&s).unwrap().node.is_none());
    let command=journal_fields(&["review".into(),"1025".into(),"client".into(),"client".into(),"1008".into(),"2".into(),"entry".into(),"corrected last passage".into(),"true".into()]);
    let corrected=transact(journal,command).unwrap();assert_eq!(corrected.code,"");assert_eq!(corrected.session.matter.revision,1026);
    assert_eq!(replay(corrected.journal).unwrap().session,corrected.session);
    assert_eq!(corrected.session.matter.nodes.iter().find(|node|node.id==1008).unwrap().value,"corrected last passage");
}

#[test]
fn the_full_history_budget_preserves_every_correction_and_refuses_atomically() {
    let journal=correction_history(2048);let s=accepted(replay(journal.clone()).unwrap());
    assert_eq!(s.matter.revision,2048);assert_eq!(s.matter.nodes[0].revision,2048);assert_eq!(s.matter.nodes[0].value,"value 2047");assert_eq!(s.matter.changes.len(),2047);assert_eq!(s.audit.len(),2048);
    let command=journal_fields(&["assert".into(),"2048".into(),"client".into(),"client".into(),"goal".into(),"Continue".into()]);
    let refused=transact(journal.clone(),command.clone()).unwrap();assert_eq!(refused.code,"journal-count");assert_eq!(refused.journal,journal);assert_eq!(refused.session,s);
    let extra=format!("{journal}{}:{command}",command.len());assert!(!replay(extra).unwrap().code.is_empty());
    let mut corrupt=correction_history(2047);append_journal_command(&mut corrupt,vec!["assert".into(),"2047".into(),"reader".into(),"reader".into(),"goal".into(),"forged".into()]);
    let failed=replay(corrupt).unwrap();assert!(!failed.code.is_empty());assert_eq!(failed.session,initial("".into()),"late corruption must not expose a partially accepted matter");
    let empty=initial("First refusal".into());
    let later=journal_fields(&["assert".into(),"0".into(),"client".into(),"client".into(),"goal".into(),"must not run".into()]);
    let stopped=replayCommands(&["malformed".into(),later],&empty).unwrap();
    assert_eq!(stopped.code,"command-encoding");assert_eq!(stopped.session,empty,"later valid commands cannot erase the first refusal");
}

#[test]
fn multiple_goals_change_attention_when_a_later_goal_is_edited_or_withdrawn() {
    let s=accepted(ingest(&initial("Several goals".into()),0,Role::Client,"client".into(),"Records".into(),b"repair invoice\nrent refund".to_vec()).unwrap());
    let s=assert_fact(&s,"goal","Understand the dispute");let first=node_ref(&s,"goal");
    let s=assert_fact(&s,"goal","rent refund");let later=node_ref(&s,"goal");
    let s=assert_fact(&s,"goal","Keep records");
    assert_eq!(nextAttention(&s).unwrap().node.unwrap().id,2,"a later goal must contribute relevance");
    for role in [Role::Client,Role::Lawyer,Role::Reader] {assert_eq!(overview(&s,role).unwrap().node,2);}
    assert!(s.matter.nodes.iter().filter(|n|!n.citations.is_empty()).all(|n|!n.accepted));
    let s=accepted(review(&s,s.matter.revision,Role::Client,"client".into(),later,"goal".into(),"repair invoice".into(),true).unwrap());
    assert_eq!(nextAttention(&s).unwrap().node.unwrap().id,1);
    assert_eq!(nodeReference(s.matter.nodes.iter().find(|n|n.id==first.id).unwrap()),first);
    let s=accepted(withdraw(&s,s.matter.revision,Role::Client,"client".into(),Reference{id:later.id,revision:2}).unwrap());
    assert_eq!(nextAttention(&s).unwrap().node.unwrap().id,1,"with no goal overlap retain source order");
}

#[test]
fn multiple_goals_do_not_count_repeated_vocabulary_more_than_once() {
    let s=accepted(ingest(&initial("Distinct goals".into()),0,Role::Client,"client".into(),"Records".into(),b"rent\nrepair".to_vec()).unwrap());
    let s=assert_fact(&s,"goal","repair");assert_eq!(nextAttention(&s).unwrap().node.unwrap().id,2);
    let s=assert_fact(&s,"goal","rent");assert_eq!(nextAttention(&s).unwrap().node.unwrap().id,1,"equal support from separate goals retains source order");
    let s=assert_fact(&s,"goal","repair");let s=assert_fact(&s,"goal","repair repair repair");
    assert_eq!(nextAttention(&s).unwrap().node.unwrap().id,1,"duplicating a goal cannot outvote another goal");
}

#[test]
fn multiple_goals_guide_missing_aspects_and_withdrawal_restores_pending_precedence() {
    let s=jointly_reviewed_amounts();
    let s=accepted(ingest(&s,s.matter.revision,Role::Client,"client".into(),"Other".into(),b"Unrelated item".to_vec()).unwrap());
    assert!(!nextAttention(&s).unwrap().additional);
    let s=assert_fact(&s,"goal","Tuesday");let later=node_ref(&s,"goal");
    let s=assert_fact(&s,"goal","Keep records");
    let focused=nextAttention(&s).unwrap();assert!(focused.additional);assert_eq!(focused.meaning.facet,"day");assert_eq!(focused.meaning.value,"Tuesday");
    assert_eq!(overview(&s,Role::Client).unwrap().node,focused.node.unwrap().id);
    let s=accepted(withdraw(&s,s.matter.revision,Role::Client,"client".into(),later).unwrap());
    assert!(!nextAttention(&s).unwrap().additional);
}

fn goal_overlap_for(session: &Session, text: &str) -> u64 {
    let admitted=current(&session.matter.nodes,&session.matter.sources).unwrap().references;
    goalFeatureOverlap(&goalContext(session,&admitted).unwrap(),&features(text.into()).unwrap().values).unwrap()
}

#[test]
fn goal_context_preserves_goal_boundaries_and_counts_each_query_feature_once() {
    let s=assert_fact(&assert_fact(&initial("Goal boundaries".into()),"goal","rent"),"goal","repair");
    let s=assert_fact(&s,"goal","repair repair repair");
    assert_eq!(goal_overlap_for(&s,"rent repair"),2,"separate goals do not supply the intervening ordered pair");
    let mut permuted=s.clone();permuted.matter.nodes.reverse();assert_eq!(goal_overlap_for(&permuted,"rent repair"),2);
    let s=assert_fact(&s,"goal","rent repair");assert_eq!(goal_overlap_for(&s,"rent repair"),3,"a pair must occur within a goal");
    let context=goalContext(&s,&current(&s.matter.nodes,&s.matter.sources).unwrap().references).unwrap();
    let mut query=features("rent repair".into()).unwrap().values;query.extend(query.clone());assert_eq!(goalFeatureOverlap(&context,&query).unwrap(),3);
}

#[test]
fn goal_context_excludes_unreviewed_conflicted_withdrawn_and_replaced_source_meanings() {
    let s=accepted(ingest(&initial("Source goals".into()),0,Role::Client,"client".into(),"Instructions".into(),b"rent refund".to_vec()).unwrap());
    let s=assert_fact(&s,"goal","Understand");assert_eq!(goal_overlap_for(&s,"rent refund"),0);
    let s=accepted(review(&s,s.matter.revision,Role::Client,"client".into(),Reference{id:1,revision:1},"goal".into(),"rent refund".into(),true).unwrap());
    assert_eq!(goal_overlap_for(&s,"rent refund"),3);
    let s=accepted(annotate(&s,s.matter.revision,Role::Client,"client".into(),Reference{id:1,revision:2},"goal".into(),"repair invoice".into()).unwrap());
    assert_eq!(goal_overlap_for(&s,"rent refund repair invoice"),0,"conflicting meanings of the same instructions cannot guide attention");
    let conflict=nodeReference(s.matter.nodes.iter().max_by_key(|n|n.id).unwrap());
    let s=accepted(withdraw(&s,s.matter.revision,Role::Client,"client".into(),conflict).unwrap());assert_eq!(goal_overlap_for(&s,"rent refund"),3);
    let s=accepted(reviseSource(&s,s.matter.revision,Role::Client,"client".into(),Reference{id:1,revision:1},b"Different instructions".to_vec()).unwrap());
    assert_eq!(goal_overlap_for(&s,"rent refund"),0);
}

#[test]
fn goal_context_reaches_the_last_goal_at_full_matter_capacity() {
    let mut s=initial("Full goal context".into());
    for index in 0..1024 {s=assert_fact(&s,"goal",&format!("goal {index}"));}
    assert_eq!(s.matter.nodes.len(),1024);
    for index in [0,31,32,511,512,1023] {assert_eq!(goal_overlap_for(&s,&format!("goal {index}")),3);}
    assert_eq!(goal_overlap_for(&s,"goal missing"),1);
    assert!(nextAttention(&s).unwrap().node.is_none());
}

#[test]
fn adding_an_outcome_preserves_rule_goal_binding_and_selected_corrections() {
    let original=strategy_journal();let binding=original.session.rules[0].goal.clone();
    let fields=vec![original.journal.clone(),"client".into(),"Recover the rent".into()];
    let added=changeFields("add-goal".into(),&fields,original.journal.clone(),&original.session,"client".into()).unwrap();
    assert_eq!(added.code,"");assert_eq!(added.session.rules[0].goal,binding);
    assert_eq!(goal_overlap_for(&added.session,"Recover the rent"),5);
    assert!(current(&added.session.matter.nodes,&added.session.matter.sources).unwrap().references.contains(&binding));
    let ambiguous=setContext(added.journal.clone(),&added.session,"client".into(),"goal".into(),"Choose for me".into()).unwrap();
    assert!(!ambiguous.code.is_empty());assert_eq!(ambiguous.journal,added.journal);assert_eq!(ambiguous.session,added.session);
    let edited=editLocatedValue(added.journal,&added.session,"client".into(),"goal".into(),"Recover the rent".into(),"Repair the home".into(),"".into()).unwrap();
    assert_eq!(edited.code,"");assert!(current(&edited.session.matter.nodes,&edited.session.matter.sources).unwrap().references.contains(&binding));
    assert_eq!(replay(edited.journal.clone()).unwrap().session,edited.session);
    let changed=editLocatedValue(edited.journal,&edited.session,"client".into(),"goal".into(),"Respond".into(),"Negotiate".into(),"".into()).unwrap();
    assert_eq!(changed.code,"");assert!(!current(&changed.session.matter.nodes,&changed.session.matter.sources).unwrap().references.contains(&binding));
    assert_eq!(assess(&changed.session.rules[0],&changed.session.matter.nodes,&changed.session.matter.sources).unwrap().status,ReasoningStatus::Inactive);
    assert_eq!(replay(changed.journal).unwrap().session,changed.session);
    let denied=changeFields("add-goal".into(),&fields,original.journal.clone(),&original.session,"reader".into()).unwrap();
    assert!(!denied.code.is_empty());assert_eq!(denied.journal,original.journal);assert_eq!(denied.session,original.session);
}

#[test]
fn grouped_synapse_updates_preserve_weights_order_and_first_match() {
    for count in [0,1,31,32,33,63,64,65,511,1024,2048] {
        let original=(0..count).map(|i|Synapse{feature:format!("feature {i}"),weight:(i+1) as u64}).collect::<Vec<_>>();
        for feature in ["feature 0","feature 31","feature 32","feature 511","feature 2047","new feature"] {
            let mut expected=original.clone();
            if let Some(existing)=expected.iter_mut().find(|s|s.feature==feature) { existing.weight+=1; }
            else { expected.push(Synapse{feature:feature.into(),weight:1}); }
            assert_eq!(strengthen(&original,feature.into()).unwrap().values,expected);
        }
    }
    let original=vec![Synapse{feature:"same".into(),weight:2},Synapse{feature:"same".into(),weight:7}];
    let updated=strengthen(&original,"same".into()).unwrap().values;
    assert_eq!(updated[0].weight,3);assert_eq!(updated[1].weight,7);assert_eq!(original[0].weight,2);
    let mut boundary=(0..65).map(|i|Synapse{feature:format!("feature {i}"),weight:1}).collect::<Vec<_>>();
    boundary[31].feature="shared".into();boundary[32].feature="shared".into();
    let updated=strengthen(&boundary,"shared".into()).unwrap().values;
    assert_eq!(updated[31].weight,2);assert_eq!(updated[32].weight,1);
}

#[test]
fn identical_direct_goals_can_be_selected_without_changing_the_other_binding() {
    let original=strategy_journal();let bound=original.session.rules[0].goal.clone();
    let added=commit(original.journal,&original.session,"assert".into(),"client".into(),&["goal".into(),"Respond".into()]).unwrap();
    assert_eq!(added.code,"");
    let duplicate=added.session.matter.nodes.iter().max_by_key(|n|n.id).unwrap().clone();
    let location=interpretationLocation(&added.session,&duplicate).unwrap();
    assert_eq!(location,format!("Recorded directly · entry {}",duplicate.id));
    let bound_node=findNode(&added.session.matter.nodes,bound.id).unwrap();
    assert_eq!(interpretationLocation(&added.session,&bound_node).unwrap(),format!("Recorded directly · entry {}",bound.id));
    for qualifier in ["", "Recorded directly", "Recorded directly · entry 9999"] {
        let refused=editLocatedValue(added.journal.clone(),&added.session,"client".into(),"goal".into(),"Respond".into(),"Negotiate".into(),qualifier.into()).unwrap();
        assert!(!refused.code.is_empty());assert_eq!(refused.session,added.session);assert_eq!(refused.journal,added.journal);
    }
    let corrected=editLocatedValue(added.journal,&added.session,"client".into(),"goal".into(),"Respond".into(),"Negotiate".into(),location.clone()).unwrap();
    assert_eq!(corrected.code,"");
    assert_eq!(findNode(&corrected.session.matter.nodes,bound.id).unwrap(),bound_node);
    assert_eq!(corrected.session.rules[0].goal,bound);
    assert_eq!(assess(&corrected.session.rules[0],&corrected.session.matter.nodes,&corrected.session.matter.sources).unwrap().status,ReasoningStatus::Supported);
    assert_eq!(replay(corrected.journal.clone()).unwrap().session,corrected.session);
    // A copied entry location remains usable after its wording becomes unique.
    let fields=vec![corrected.journal.clone(),"client".into(),"goal".into(),"Negotiate".into(),location];
    let withdrawn=changeFields("withdraw".into(),&fields,corrected.journal,&corrected.session,"client".into()).unwrap();
    assert_eq!(withdrawn.code,"");assert!(!findNode(&withdrawn.session.matter.nodes,duplicate.id).unwrap().accepted);
    assert_eq!(findNode(&withdrawn.session.matter.nodes,bound.id).unwrap(),bound_node);
    assert_eq!(replay(withdrawn.journal).unwrap().session,withdrawn.session);
}

#[test]
fn direct_entry_locations_preserve_roles_facets_and_cited_provenance() {
    let original=strategy_journal();let goal=original.session.rules[0].goal.clone();
    let location=format!("Recorded directly · entry {}",goal.id);
    let denied=editLocatedValue(original.journal.clone(),&original.session,"reader".into(),"goal".into(),"Respond".into(),"Altered".into(),location.clone()).unwrap();
    assert!(!denied.code.is_empty());assert_eq!(denied.session,original.session);assert_eq!(denied.journal,original.journal);
    assert!(uniqueLocatedNode(&original.session,"jurisdiction".into(),"".into(),location).unwrap().is_none());
    let authority=&original.session.rules[0].authority;
    assert!(uniqueLocatedNode(&original.session,"authority".into(),"".into(),format!("Recorded directly · entry {}",authority.id)).unwrap().is_none());
    assert_eq!(interpretationLocation(&original.session,&findNode(&original.session.matter.nodes,goal.id).unwrap()).unwrap(),"Recorded directly");
    let changed=editLocatedValue(original.journal,&original.session,"client".into(),"goal".into(),"Respond".into(),"Negotiate".into(),"Recorded directly".into()).unwrap();
    assert_eq!(changed.code,"");assert_eq!(assess(&changed.session.rules[0],&changed.session.matter.nodes,&changed.session.matter.sources).unwrap().status,ReasoningStatus::Inactive);
}

#[test]
fn direct_entry_disambiguation_reaches_the_full_matter_boundary() {
    let mut s=initial("Repeated entries".into());
    for index in 0..1024 {s=assert_fact(&s,"goal",if index==0||index==1023 {"Repeated outcome"} else {"Other outcome"});}
    for id in [1,1024] {
        let node=findNode(&s.matter.nodes,id).unwrap();let location=interpretationLocation(&s,&node).unwrap();
        assert_eq!(location,format!("Recorded directly · entry {id}"));
        assert_eq!(uniqueLocatedNode(&s,"goal".into(),"Repeated outcome".into(),location).unwrap().unwrap(),node);
    }
    assert!(uniqueLocatedNode(&s,"goal".into(),"Repeated outcome".into(),"Recorded directly".into()).unwrap().is_none());
    let admitted=current(&s.matter.nodes,&s.matter.sources).unwrap().references;
    for (value,count,first_id) in [("Repeated outcome",2,1024),("Other outcome",1022,1023),("",1024,1024)] {
        let selected=matchingLocatedNodes(&s.matter.nodes,&s,&admitted,"goal".into(),value.into(),"Recorded directly".into()).unwrap();
        assert_eq!(selected.count,count);assert_eq!(selected.node.unwrap().id,first_id);
    }
}

#[test]
fn direct_entry_inspection_reaches_the_last_page_without_expanding_the_stack() {
    let mut s=initial("Repeated entries".into());
    for index in 0..1024 {s=assert_fact(&s,"goal",if index==0||index==1023 {"Repeated outcome"} else {"Other outcome"});}
    let admitted=current(&s.matter.nodes,&s.matter.sources).unwrap().references;
    let rows=facetPage(&s.matter.nodes,&s,&s.matter.nodes,&s.audit,&admitted,"goal".into(),Role::Client,1016,8).unwrap().values;
    assert_eq!(rows.len(),8);
    for (row,id) in rows.iter().zip((1..=8).rev()) {assert!(row.ends_with(&format!("Recorded directly · entry {id}")));}
    assert!(rows[7].starts_with("Current interpretation: Repeated outcome"));
    assert!(facetPage(&s.matter.nodes,&s,&s.matter.nodes,&s.audit,&admitted,"missing".into(),Role::Client,0,8).unwrap().values.is_empty());
}

#[test]
fn full_capacity_goal_vocabulary_replays_and_focuses_the_oldest_relevant_goal() {
    let mut journal=initialJournal("All current goals".into());
    append_journal_command(&mut journal,vec!["ingest".into(),"0".into(),"client".into(),"client".into(),"Records".into(),"ordinary passage\ntarget agreement".into()]);
    for index in 0..1022 {
        append_journal_command(&mut journal,vec!["assert".into(),(index+1).to_string(),"client".into(),"client".into(),"goal".into(),if index==0 {"target agreement".into()} else {format!("another outcome {index}")}]);
    }
    let restored=replay(journal).unwrap();assert_eq!(restored.code,"");
    assert_eq!(restored.session.matter.nodes.len(),1024);
    assert_eq!(overview(&restored.session,Role::Client).unwrap().node,2);
    assert_eq!(restored.session.matter.nodes.iter().filter(|n|!n.accepted).count(),2);
}
