from milestone_300_sampling_frame_builder import build

def rows():
 out=[]
 for y in range(2006,2026):
  for r in range(1,101): out.append({'chart_year':str(y),'rank':str(r),'title':f'S{y}-{r}','artist':'A','playcount':'100000000','duration_ms':'200000','spotify_uri':'spotify:track:x'})
 return out

def test_exact_300_frame():
 out=build(rows());assert out['frame_complete'];assert out['candidate_count']==300;assert all(v==15 for v in out['year_counts'].values())

def test_does_not_promote_discovery_rows():
 out=build(rows());assert all(x['scientific_promotion'] is False for x in out['candidates']);assert all(x['genre_style']=='PENDING' for x in out['candidates'])

def test_incomplete_year_blocks_frame():
 r=[x for x in rows() if not (x['chart_year']=='2015' and x['rank']=='15')];out=build(r);assert not out['frame_complete'];assert out['status']=='FRAME_INCOMPLETE'
