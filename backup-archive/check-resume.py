import importlib.util,pathlib,tempfile,json,os,sys,hashlib
spec=importlib.util.spec_from_file_location('archive',pathlib.Path(__file__).resolve().parent/'archive-local.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
with tempfile.TemporaryDirectory(prefix='archive-resume-check-') as tmp:
 root=pathlib.Path(tmp);src=root/'source';src.mkdir();dest=root/'archive';dest.mkdir();m.BASE=root
 a=src/'a';a.write_text('first snapshot');b=src/'b';b.write_text('planned value')
 def item(p):
  s=p.stat();return {'path':'','bytes':s.st_size,'mtime_ns':s.st_mtime_ns}
 fa=item(a);m.copy_file(a,dest/'saved-a',fa)
 first={'source':str(a),'relative_path':'saved-a','kind':'loose files','files':[fa],'complete':True}
 fb=item(b);second={'source':str(b),'relative_path':'saved-b','kind':'loose files','files':[fb]}
 (dest/'saved-b').write_text('incomplete old copy');a.write_text('changed since completed snapshot');b.write_text('latest stable contents')
 (dest/'archive-manifest.json').write_text(json.dumps({'file_bytes':fa['bytes']+fb['bytes'],'items':[first,second],'complete':False}))
 sys.argv=['archive-local.py','--resume',str(dest)];m.main()
 manifest=json.loads((dest/'archive-manifest.json').read_text());assert manifest['complete'];assert len(manifest['items'])==2
 assert (dest/'saved-a').read_text()=='first snapshot';assert (dest/'saved-b').read_text()=='latest stable contents';assert manifest['items'][1]['files'][0]['changed_since_plan']
 original_hash=m.hashfile
 def no_rehash(path):
  if pathlib.Path(path).name in {'saved-a','saved-b'}:raise AssertionError('fast-resume rehashed completed data')
  return original_hash(path)
 m.hashfile=no_rehash;sys.argv=['archive-local.py','--resume',str(dest),'--fast-resume'];m.main();m.hashfile=original_hash
 # A source mutation during the first attempt requires a verified retry.
 c=src/'changing';c.write_text('before');fc=item(c);original=m.shutil.copyfile;attempts=[]
 def mutate(source,target):
  result=original(source,target);attempts.append(1)
  if len(attempts)==1:pathlib.Path(source).write_text('after modification')
  return result
 m.shutil.copyfile=mutate;m.copy_file(c,dest/'retry',fc);m.shutil.copyfile=original
 assert len(attempts)==2;assert (dest/'retry').read_text()=='after modification';assert fc['verified']
 assert not list(dest.glob('.archive-copy-*'))
 print('PASS: existing archive resumes; completed snapshots preserved; stale-plan file accepted after verification; partial copy replaced; mid-copy mutation retried; no duplicate archive or leftover temporary files.')
