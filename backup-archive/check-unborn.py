import importlib.util,pathlib,tempfile,subprocess,json,copy
base=pathlib.Path(__file__).resolve().parent;spec=importlib.util.spec_from_file_location('archive',base/'archive-local.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def git(repo,*args):return m.textgit(repo,*args).strip()
with tempfile.TemporaryDirectory(prefix='archive-unborn-check-') as tmp:
 root=pathlib.Path(tmp);repo=root/'source';repo.mkdir();git(repo,'init');(repo/'file.txt').write_text('staged content\n');git(repo,'add','file.txt');(repo/'file.txt').write_text('unstaged content\n')
 meta=root/'metadata';meta.mkdir();item={'head':None,'remote_refs':[]};m.history(repo,meta,item)
 assert item['local_history_commits']==0;assert not (meta/'local-history.bundle').exists()
 restore=root/'restored';restore.mkdir();git(restore,'init');git(restore,'apply','--index',str(meta/'staged.patch'));git(restore,'apply',str(meta/'unstaged.patch'));assert (restore/'file.txt').read_text()=='unstaged content\n'
 assert git(restore,'show',':file.txt')=='staged content'
 git(repo,'config','user.name','Archive test');git(repo,'config','user.email','test@example.invalid');git(repo,'config','commit.gpgsign','false');git(repo,'commit','-m','initial')
 # A repository can have commits but no reflog. Its named history must still bundle.
 import shutil
 shutil.rmtree(repo/'.git/logs');meta2=root/'metadata2';meta2.mkdir();item2={'head':git(repo,'rev-parse','HEAD'),'remote_refs':[]};m.history(repo,meta2,item2);assert item2['local_history_commits']==1;assert (meta2/'local-history.bundle').is_file()
 print('PASS: unborn repository with staged/unstaged work recovered; committed repository with no reflog bundles correctly.')
