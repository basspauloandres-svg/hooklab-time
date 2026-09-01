from bimmuda_t1_crosswalk_builder import build

def test_presence_does_not_promote():
    q={'candidates':[{'title':'Umbrella','artist':'Rihanna'}]}
    m=[{'Title':'Umbrella','Artist':'Rihanna featuring Jay-Z','Year':'2007','Position':'2'}]
    out=build(q,m,'AUDIT_REQUIRED')
    r=out['rows'][0]
    assert r['present_in_bimmuda'] is True
    assert r['bimmuda_id']=='2007_02'
    assert r['scientific_eligibility']=='BLOCKED_LICENSE_AUDIT'
    assert out['counts']['scientifically_promoted_rows']==0

def test_absent_song_not_covered():
    q={'candidates':[{'title':'Unknown Song','artist':'Unknown'}]}
    out=build(q,[],'AUDIT_REQUIRED')
    assert out['rows'][0]['present_in_bimmuda'] is False
    assert out['rows'][0]['scientific_eligibility']=='NOT_COVERED'
