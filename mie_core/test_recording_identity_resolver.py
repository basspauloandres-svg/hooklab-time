from recording_identity_resolver import score

def rec(title='Firework',artist='Katy Perry',length=228000,date='2010-10-26'):
    return {'title':title,'artist-credit':[{'name':artist,'joinphrase':''}],'length':length,'first-release-date':date}

def test_exact_identity_scores_strongly():
    target={'title':'Firework','artist':'Katy Perry','duration_ms':228000,'release_year':2010}
    s,reasons=score(target,rec())
    assert s==100
    assert 'TITLE_EXACT' in reasons and 'ARTIST_EXACT' in reasons

def test_wrong_artist_is_not_strong_identity():
    target={'title':'Firework','artist':'Katy Perry','duration_ms':228000,'release_year':2010}
    s,_=score(target,rec(artist='Other Artist'))
    assert s<80

def test_large_duration_mismatch_penalizes_version():
    target={'title':'Firework','artist':'Katy Perry','duration_ms':228000,'release_year':2010}
    s,reasons=score(target,rec(length=174000))
    assert s<80
    assert 'DURATION_DELTA_MS=54000' in reasons
