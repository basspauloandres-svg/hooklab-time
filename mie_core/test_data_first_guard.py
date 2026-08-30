from data_first_guard import DecisionEvidence, DataFirstViolation, authorize, assert_no_manual_success_weights

def test_corpus_decision_is_authorized():
    e=DecisionEvidence('D1','CORPUS_EMPIRICAL','Observed corpus relation',statistic='effect estimate')
    assert authorize(e)['authorized']

def test_human_prior_cannot_control_inference():
    e=DecisionEvidence('D2','HUMAN_PRIOR','Repetition seems commercially useful')
    try: authorize(e)
    except DataFirstViolation: return
    raise AssertionError('Human prior entered inferential mode')

def test_literature_prior_can_remain_exploratory():
    e=DecisionEvidence('D3','LITERATURE_PRIOR','Prior literature hypothesis',provisional=True)
    assert authorize(e,'EXPLORATORY')['authorized']

def test_manual_success_score_is_rejected():
    try: assert_no_manual_success_weights({'success_score':0.8})
    except DataFirstViolation: return
    raise AssertionError('Manual success score accepted')
