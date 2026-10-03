import importlib.util,tempfile,pathlib,subprocess,os,json
spec=importlib.util.spec_from_file_location('archive_local',pathlib.Path(__file__).resolve().parent/'archive-local.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def git(p,*args):
 r=subprocess.run(['git','-C',str(p),*args],capture_output=True,text=True,check=True);return r.stdout.strip()
with tempfile.TemporaryDirectory(prefix='mbp-archive-check-') as tmp:
 root=pathlib.Path(tmp);source=root/'source';source.mkdir();remote=root/'remote.git';meta=root/'metadata';meta.mkdir()
 git(source,'init','-b','main');git(source,'config','user.name','Archive test');git(source,'config','user.email','test@example.invalid');git(source,'config','commit.gpgsign','false')
 (source/'file.txt').write_text('base\n');git(source,'add','file.txt');git(source,'commit','-m','base');base=git(source,'rev-parse','HEAD')
 subprocess.run(['git','init','--bare',str(remote)],capture_output=True,check=True);git(source,'remote','add','origin',str(remote));git(source,'push','origin','main')
 git(source,'update-ref','refs/backup-audit/test/heads/main',base)
 (source/'file.txt').write_text('local commit\n');git(source,'commit','-am','local');local=git(source,'rev-parse','HEAD')
 (source/'stash.txt').write_text('saved untracked work\n');git(source,'stash','push','--include-untracked','-m','save local work')
 (source/'file.txt').write_text('staged version\n');git(source,'add','file.txt');(source/'file.txt').write_text('unstaged version\n')
 (source/'.env').write_text('EXAMPLE=value\n');(source/'node_modules').mkdir();(source/'node_modules/dep').write_text('dependency')
 os.symlink('file.txt',source/'linked.txt')
 found,skips=m.walk_files(source);assert not any('node_modules' in p.parts for p in found);assert '.env' in [p.name for p in found];assert source/'linked.txt' in found
 st=(source/'.env').stat();f={'bytes':st.st_size,'mtime_ns':st.st_mtime_ns};m.copy_file(source/'.env',root/'overlay/.env',f);assert f['verified']
 item={'head':local,'remote_refs':['refs/backup-audit/test/heads/main']};m.history(source,meta,item)
 assert item['local_history_commits']>=2
 clone=root/'restored';subprocess.run(['git','clone','--branch','main',str(remote),str(clone)],capture_output=True,check=True)
 git(clone,'bundle','verify',str(meta/'local-history.bundle'));git(clone,'fetch',str(meta/'local-history.bundle'),'refs/heads/main:refs/heads/recovered')
 git(clone,'checkout','recovered');assert git(clone,'rev-parse','HEAD')==local
 git(clone,'apply','--index',str(meta/'staged.patch'));git(clone,'apply',str(meta/'unstaged.patch'));assert (clone/'file.txt').read_text()=='unstaged version\n'
 git(clone,'fetch',str(meta/'local-history.bundle'),'refs/stash:refs/archive/stash');stash=git(clone,'rev-parse','refs/archive/stash');git(clone,'stash','store','-m','restored',stash);assert git(clone,'stash','list')
 full=root/'full-metadata';full.mkdir();m.history(source,full,{'head':local,'remote_refs':[]})
 subprocess.run(['git','clone','--branch','main',str(full/'local-history.bundle'),str(root/'full-restored')],capture_output=True,check=True)
 assert git(root/'full-restored','rev-parse','HEAD')==local
 git(source,'reset','--hard',base);git(source,'update-ref','-d','refs/stash')
 reflog_only=root/'reflog-only';reflog_only.mkdir();reflog_item={'head':base,'remote_refs':['refs/backup-audit/test/heads/main']};m.history(source,reflog_only,reflog_item)
 assert reflog_item['local_history_commits']>0
 heads=git(source,'bundle','list-heads',str(reflog_only/'local-history.bundle'));assert 'archive-reflog/'+local in heads
 git(clone,'fetch',str(reflog_only/'local-history.bundle'),'refs/heads/archive-reflog/'+local+':refs/heads/restored-reflog');assert git(clone,'rev-parse','restored-reflog')==local
 print('PASS: reflog-only history bundle and recovery; full standalone bundle clone; local commit and stash recovered from incremental bundle; staged and unstaged versions restored; .env copy hash verified; dependency cache skipped; symlink detected.')
