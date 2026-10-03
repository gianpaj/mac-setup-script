#!/usr/bin/env python3
"""Preserve local Git work and files; never fetch, push, pull, or delete sources."""
import argparse,datetime,hashlib,json,os,pathlib,shutil,stat,subprocess,sys,tempfile,time
HOME=pathlib.Path.home()
BASE=pathlib.Path(os.environ.get('MBP_ARCHIVE_STATE_DIR',str(HOME/'backup-repo-audit'))).expanduser()
CACHE_DIRS={'node_modules','.venv','venv','__pycache__','.next','.nuxt','.svelte-kit','.turbo','.parcel-cache','.pytest_cache','.mypy_cache','.ruff_cache','.gradle','.cache','.pnpm-store'}
CACHE_FILES={'.DS_Store'}
EXCLUDED_ROOTS=[HOME/'projects-old/onova',HOME/'freelance/clark']
FORCE_FULL_ROOTS=[HOME/'github/twinfoundation/ui',HOME/'github/Thinkful-Ed',HOME/'github/gianpaj/tts-api-bench']
DOWNLOAD_NAMES=['old mac','books','Audiobooks','Tutorials : Courses','Documentaries','Movies','TV_Shows','Music Downloads','Podcasts','youtube','Backup 2TB big1 HDD ( to move to Media 2tb hdd)']
def under(path,roots):return any(path==r or r in path.parents for r in roots)
ENV=dict(os.environ,GIT_OPTIONAL_LOCKS='0',GIT_TERMINAL_PROMPT='0',GIT_LFS_SKIP_SMUDGE='1')

def git(repo,*args,input=None,check=True):
 p=subprocess.run(['git','-c','gc.auto=0','-c','maintenance.auto=false','-C',str(repo),*args],input=input,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=ENV,timeout=300)
 if check and p.returncode:raise RuntimeError('git '+args[0]+': '+p.stderr.decode(errors='replace')[:800])
 return p

def paths(data):return [os.fsdecode(x) for x in data.split(b'\0') if x]
def textgit(repo,*args):return git(repo,*args).stdout.decode(errors='replace')
def cached(path):return any(p in CACHE_DIRS for p in path.parts) or path.name in CACHE_FILES

def walk_files(root,nested=()):
 skipped=[];found=[]
 for base,dirs,files in os.walk(root,followlinks=False):
  here=pathlib.Path(base)
  for d in list(dirs):
   p=here/d
   if d=='.git' or p in nested or d in CACHE_DIRS:
    dirs.remove(d)
    if d!='.git' and p not in nested:skipped.append(str(p.relative_to(root)))
   elif p.is_symlink():dirs.remove(d);found.append(p)
  for name in files:
   p=here/name
   if name=='.git':continue
   if cached(p.relative_to(root)):skipped.append(str(p.relative_to(root)));continue
   found.append(p)
 return found,skipped

def hashfile(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def portable_path(relative):
 parts=[]
 for part in pathlib.Path(relative).parts:
  name=''.join('%%%02X'%ord(c) if c in '%<>:"\\|?*' or ord(c)<32 or (i==len(part)-1 and c in '. ') else c for i,c in enumerate(part))
  if len(name.encode('utf-16-le'))>400:name=name[:160]+'~'+hashlib.sha256(part.encode()).hexdigest()[:16]
  parts.append(name)
 return pathlib.Path(*parts)

def downloads_plan():
 items=[];total=0
 def fail(error):raise error
 for name in DOWNLOAD_NAMES:
  root=HOME/'Downloads'/name
  if not root.is_dir():raise RuntimeError('Requested Downloads folder is missing: '+str(root))
  files=[];links=[];directories=['']
  for base,dirs,names in os.walk(root,followlinks=False,onerror=fail):
   here=pathlib.Path(base)
   for d in list(dirs):
    p=here/d;rel=str(p.relative_to(root))
    if p.is_symlink():links.append({'path':rel,'target':os.readlink(p)});dirs.remove(d)
    else:directories.append(rel)
   for n in names:
    p=here/n;rel=str(p.relative_to(root));st=p.lstat()
    if stat.S_ISLNK(st.st_mode):links.append({'path':rel,'target':os.readlink(p)})
    elif stat.S_ISREG(st.st_mode):files.append({'path':rel,'bytes':st.st_size,'mtime_ns':st.st_mtime_ns});total+=st.st_size
    else:raise RuntimeError('Special file needs review: '+str(p))
  items.append({'source':str(root),'relative_path':str(root.relative_to(HOME)),'kind':'downloads folder','files':files,'symlinks':links,'directories':directories,'skipped_caches':[]})
 return {'created_at':datetime.datetime.now().isoformat(),'source_home':str(HOME),'file_bytes':total,'items':items}

def plan():
 repos=[pathlib.Path(x) for x in json.load(open(BASE/'inventory.json'))]
 fetched=json.load(open(BASE/'fetch-results.json'))
 audit={x['path']:x for x in json.load(open(BASE/'results.json'))}
 items=[];total=0
 for repo in repos:
  if under(repo,EXCLUDED_ROOTS):continue
  rr=audit.get(str(repo),{})
  fresh=[]
  for x in fetched:
   if x['path']==str(repo) and x['exit_code']==0:
    fresh+=textgit(repo,'for-each-ref','--format=%(refname)','refs/backup-audit/20261003-confirm/'+str(x['i'])+'/').splitlines()
  verified=bool(fresh)
  forced=under(repo,FORCE_FULL_ROOTS)
  tracked=set(paths(git(repo,'ls-files','-z').stdout))
  head=git(repo,'rev-parse','--verify','HEAD',check=False)
  changed=set(paths(git(repo,'diff','--no-ext-diff','--name-only','-z','HEAD').stdout)) if head.returncode==0 else tracked
  flags=textgit(repo,'ls-files','-v').splitlines()
  changed.update(x[2:] for x in flags if x[0].islower() or x[0]=='S')
  files,skips=walk_files(repo,{p for p in repos if repo in p.parents})
  selected=[];links=[]
  for p in files:
   rel=str(p.relative_to(repo))
   if verified and not forced and rel in tracked and rel not in changed:continue
   st=p.lstat()
   if stat.S_ISLNK(st.st_mode):links.append({'path':rel,'target':os.readlink(p)})
   elif stat.S_ISREG(st.st_mode):selected.append({'path':rel,'bytes':st.st_size,'mtime_ns':st.st_mtime_ns});total+=st.st_size
   else:raise RuntimeError('Special file needs review: '+str(p))
  deleted=[p for p in sorted(changed) if not os.path.lexists(repo/p)]
  items.append({'source':str(repo),'relative_path':str(repo.relative_to(HOME)),'kind':'repository','remote_verified':verified,'full_copy_requested':forced,'verification_note':'Fresh remote refs available' if verified else 'Remote unavailable/empty/missing: source and local history preserved conservatively','remote_refs':[] if forced else fresh,'files':selected,'symlinks':links,'deleted_paths':deleted,'skipped_caches':skips,'head':head.stdout.decode().strip() if head.returncode==0 else None,'remotes':textgit(repo,'remote','-v').splitlines(),'branches':textgit(repo,'for-each-ref','--format=%(refname) %(objectname)','refs/heads/').splitlines(),'status':textgit(repo,'status','--porcelain=v1','--untracked-files=normal')})
 for raw in json.load(open(BASE/'outside-repositories.json')):
  p=pathlib.Path(raw)
  if under(p,EXCLUDED_ROOTS) or not os.path.lexists(p) or cached(p.relative_to(HOME)):continue
  files,skips=walk_files(p) if p.is_dir() and not p.is_symlink() else ([p],[])
  selected=[];links=[]
  for f in files:
   rel=str(f.relative_to(p)) if f!=p else ''
   st=f.lstat()
   if stat.S_ISLNK(st.st_mode):links.append({'path':rel,'target':os.readlink(f)})
   elif stat.S_ISREG(st.st_mode):selected.append({'path':rel,'bytes':st.st_size,'mtime_ns':st.st_mtime_ns});total+=st.st_size
   else:raise RuntimeError('Special file needs review: '+str(f))
  items.append({'source':str(p),'relative_path':str(p.relative_to(HOME)),'kind':'loose files','files':selected,'symlinks':links,'skipped_caches':skips})
 return {'created_at':datetime.datetime.now().isoformat(),'source_home':str(HOME),'excluded_roots':[str(x) for x in EXCLUDED_ROOTS],'full_copy_roots':[str(x) for x in FORCE_FULL_ROOTS],'skipped_cache_names':sorted(CACHE_DIRS),'file_bytes':total,'items':items}

def copy_file(src,dest,item):
 dest.parent.mkdir(parents=True,exist_ok=True)
 if dest.exists() and item.get('verified') and item.get('sha256'):
  if hashfile(dest)!=item['sha256']:raise RuntimeError('Previously verified archive file changed: '+str(dest))
  return
 for attempt in range(5):
  before=src.stat()
  if dest.exists() and hashfile(src)==hashfile(dest):
   digest=hashfile(dest);after=src.stat()
   if (before.st_size,before.st_mtime_ns)==(after.st_size,after.st_mtime_ns):break
  handle,tmp=tempfile.mkstemp(prefix='.archive-copy-',dir=dest.parent);os.close(handle)
  try:
   shutil.copyfile(src,tmp)
   digest=hashfile(tmp);source_digest=hashfile(src);after=src.stat()
   if digest==source_digest and (before.st_size,before.st_mtime_ns)==(after.st_size,after.st_mtime_ns):
    os.replace(tmp,dest);break
  finally:
   if os.path.exists(tmp):os.unlink(tmp)
  time.sleep(0.2)
 else:raise RuntimeError('File keeps changing; close the app and resume: '+str(src))
 if (item['bytes'],item['mtime_ns'])!=(before.st_size,before.st_mtime_ns):item['changed_since_plan']=True
 item.update(bytes=before.st_size,mtime_ns=before.st_mtime_ns,sha256=digest,mode=stat.S_IMODE(before.st_mode),verified=True)
 try:shutil.copystat(src,dest)
 except OSError:pass

def verify_item(dest,item,fast=False):
 out=dest/item.get('archive_relative_path',item['relative_path'])
 for f in item['files']:
  target=out/f.get('archive_path',f['path']) if f['path'] else out
  if not f.get('sha256') or not target.is_file() or target.stat().st_size!=f['bytes']:raise RuntimeError('Archived file verification failed: '+str(target))
  if not fast and hashfile(target)!=f['sha256']:raise RuntimeError('Archived file verification failed: '+str(target))
 if item.get('bundle_sha256'):
  bundle=dest/'_archive'/item.get('archive_relative_path',item['relative_path'])/'local-history.bundle'
  if hashfile(bundle)!=item['bundle_sha256']:raise RuntimeError('Archived bundle verification failed: '+str(bundle))

def save_manifest(dest,p):
 target=dest/'archive-manifest.json';tmp=dest/'archive-manifest.json.tmp'
 tmp.write_text(json.dumps(p,indent=2));os.replace(tmp,target)

def history(repo,meta,item):
 refs=[x for x in textgit(repo,'for-each-ref','--format=%(refname)').splitlines() if not x.startswith('refs/backup-audit/')]
 if item['head']:refs.append('HEAD')
 # An unborn repository has no revision for `rev-list --reflog` to walk.
 # Read reflog tips first; an empty list is a valid repository state.
 reflog=list(dict.fromkeys(textgit(repo,'reflog','show','--all','--format=%H').splitlines()));refs+=reflog
 refs=list(dict.fromkeys(refs))
 revs=''.join(x+'\n' for x in refs)+''.join('^'+x+'\n' for x in item['remote_refs'])
 count=git(repo,'rev-list','--count','--stdin',input=revs.encode()).stdout.decode().strip() if refs else '0'
 item['local_history_commits']=int(count)
 if int(count):
  dest=meta/'local-history.bundle'
  # Bundle tips must have names. Reflog-only commit IDs need synthetic refs;
  # create those in an isolated bare repository, leaving source refs untouched.
  negative=''.join('^'+x+'\n' for x in item['remote_refs'])
  reflog_revs=''.join(x+'\n' for x in reflog)+negative
  local_reflog=git(repo,'rev-list','--stdin',input=reflog_revs.encode()).stdout.decode().splitlines() if reflog else []
  objects=pathlib.Path(textgit(repo,'rev-parse','--path-format=absolute','--git-common-dir').strip())/'objects'
  source_refs=textgit(repo,'for-each-ref','--format=%(objectname) %(refname)').splitlines()
  with tempfile.TemporaryDirectory(prefix='archive-bundle-',dir=BASE) as tmp:
   scratch=pathlib.Path(tmp);git(repo,'init','--bare',str(scratch))
   (scratch/'objects/info/alternates').write_text(str(objects)+'\n')
   tips=[];by_name={}
   for line in source_refs:
    oid,ref=line.split(' ',1);by_name[ref]=oid
    if ref.startswith('refs/backup-audit/'):continue
    path=scratch/ref;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(oid+'\n');tips.append(ref)
   for oid in local_reflog:
    ref='refs/heads/archive-reflog/'+oid;path=scratch/ref;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(oid+'\n');tips.append(ref)
   if item['head']:(scratch/'HEAD').write_text(item['head']+'\n');tips.append('HEAD')
   bundle_revs=''.join(x+'\n' for x in tips)+''.join('^'+by_name[x]+'\n' for x in item['remote_refs'])
   git(scratch,'bundle','create',str(dest),'--stdin',input=bundle_revs.encode())
  git(repo,'bundle','verify',str(dest))
  item['bundle_sha256']=hashfile(dest)
  (meta/'bundle-heads.txt').write_bytes(git(repo,'bundle','list-heads',str(dest)).stdout)
 # Git can compare an unborn index with the empty tree, preserving staged
 # content even before the first commit exists.
 for name,args in [('staged.patch',['diff','--no-ext-diff','--binary','--cached']+(['HEAD'] if item['head'] else [])),('unstaged.patch',['diff','--no-ext-diff','--binary'])]:
  data=git(repo,*args).stdout
  if data:(meta/name).write_bytes(data)
 # Save original local config, hooks and ignore rules separately from the checkout.
 item['stashes']=textgit(repo,'stash','list','--format=%gd%x09%H%x09%gs').splitlines()
 (meta/'reflog.txt').write_bytes(git(repo,'reflog','show','--all','--format=%H %gD %gs').stdout)
 gd=pathlib.Path(textgit(repo,'rev-parse','--absolute-git-dir').strip())
 common=pathlib.Path(textgit(repo,'rev-parse','--path-format=absolute','--git-common-dir').strip())
 for root,label in ([(gd,'git-dir')] if gd==common else [(gd,'git-dir'),(common,'git-common-dir')]):
  for name in ['config','config.worktree','info/exclude']:
   src=root/name
   if src.is_file():
    dest=meta/label/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
  for name in ['hooks','lfs/objects']:
   src=root/name
   if src.is_dir():
    for base,dirs,files in os.walk(src):
     for filename in files:
      f=pathlib.Path(base)/filename
      if filename.endswith('.sample'):continue
      dest=meta/label/f.relative_to(root);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,dest)
 # Preserve loose unreachable objects, including the blob found in FlaskReactold.
 fsck=git(repo,'fsck','--full','--no-reflogs','--unreachable',check=False)
 if fsck.returncode:raise RuntimeError('Git object verification failed in '+str(repo)+': '+fsck.stderr.decode(errors='replace')[:500])
 (meta/'object-check.txt').write_bytes(fsck.stdout+fsck.stderr)
 for line in fsck.stdout.decode().splitlines():
  fields=line.split()
  if len(fields)==3 and fields[0]=='unreachable':
   kind,oid=fields[1:];data=git(repo,'cat-file',kind,oid).stdout
   dest=meta/'unreachable-objects'/oid;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
   with open(meta/'unreachable-objects.jsonl','a') as f:f.write(json.dumps({'oid':oid,'type':kind,'bytes':len(data),'sha256':hashfile(dest)})+'\n')
 # Save tag objects even when their commits are already on a remote.
 for line in textgit(repo,'for-each-ref','--format=%(objecttype) %(objectname) %(refname)','refs/tags/').splitlines():
  kind,oid,ref=line.split(' ',2)
  if kind=='tag':
   dest=meta/'annotated-tags'/oid;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(git(repo,'cat-file','tag',oid).stdout)

RESTORE='''This is an incremental archive, not a complete checkout.\nClone the project's verified remote, then use local-history.bundle to fetch saved branches/history.\nThe bundle may require commits from that remote; keep the remote URLs in each repository manifest.
To restore stashes, fetch the saved bundle refs into temporary refs, then use git stash store with the saved stash commit IDs (oldest first).\nCopy archived working files over the checkout. Apply deleted_paths and recreate symlinks from the manifest.\nStaged/unstaged patches preserve both versions of partially staged changes. Git config and hooks are saved separately.\nFor unverified/missing remotes, the bundle includes full local history and working files are copied conservatively.\nUnreachable objects can be restored with git hash-object -w -t TYPE FILE; compare the returned object ID with the manifest.\nOriginal names and encoded archive paths are recorded in each manifest; use them when restoring filenames.\nDo not delete original repositories until the HDD archive is complete and its files/bundles have been verified.\n'''

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--plan-only',action='store_true');ap.add_argument('--downloads-only',action='store_true');ap.add_argument('--resume',type=pathlib.Path);ap.add_argument('--fast-resume',action='store_true');ap.add_argument('--destination',default='/Volumes/WD_BLACK/mbp-archive');args=ap.parse_args()
 if args.fast_resume and not args.resume:ap.error('--fast-resume requires --resume')
 if args.resume and (args.downloads_only or args.plan_only):ap.error('--resume uses the saved archive plan; do not combine it with other modes')
 if args.resume:
  dest=args.resume.resolve();p=json.loads((dest/'archive-manifest.json').read_text())
  print('Resuming:',dest,flush=True)
 else:
  downloads=downloads_plan();p=downloads if args.downloads_only else plan()
  if not args.downloads_only:p['items']+=downloads['items'];p['file_bytes']+=downloads['file_bytes']
 (BASE/('downloads-plan.json' if args.downloads_only else 'archive-plan.json')).write_text(json.dumps(p,indent=2))
 print('Plan:',len(p['items']),'items;',sum(len(x['files']) for x in p['items']),'files;',round(p['file_bytes']/1024**3,2),'GiB before Git bundles',flush=True)
 if args.plan_only:return
 if not args.resume:
  parent=pathlib.Path(args.destination)
  if not parent.is_dir():raise RuntimeError('Destination must already exist: '+str(parent))
  dest=parent/(('downloads-' if args.downloads_only else 'local-only-')+datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S'));dest.mkdir()
 free=shutil.disk_usage(dest).free
 if free<p['file_bytes']+5*1024**3:raise RuntimeError('Insufficient free space for files and history')
 p['destination']=str(dest);p['complete']=False;save_manifest(dest,p);(dest/'RESTORE.txt').write_text(RESTORE)
 for n,item in enumerate(p['items'],1):
  if item.get('complete'):
   verify_item(dest,item,fast=args.fast_resume);print(str(n)+'/'+str(len(p['items']))+(' prior verification reused ' if args.fast_resume else ' already verified ')+item['relative_path'],flush=True);continue
  repo=pathlib.Path(item['source']);item['archive_relative_path']=str(portable_path(item['relative_path']));out=dest/item['archive_relative_path'];meta=dest/'_archive'/item['archive_relative_path'];meta.mkdir(parents=True,exist_ok=True)
  for directory in item.get('directories',[]):(out/portable_path(directory)).mkdir(parents=True,exist_ok=True)
  for f in item['files']:
   f['archive_path']=f.get('archive_path',str(portable_path(f['path'])) if f['path'] else '')
   if args.resume and f['path'] and (out/f['path']).exists() and not (out/f['archive_path']).exists():f['archive_path']=f['path']
   src=repo/f['path'] if f['path'] else repo;target=out/f['archive_path'] if f['path'] else out
   try:copy_file(src,target,f)
   except Exception:
    save_manifest(dest,p);raise
  if item['kind']=='repository':
   current=git(repo,'rev-parse','--verify','HEAD',check=False)
   current_head=current.stdout.decode().strip() if current.returncode==0 else None
   if current_head!=item['head'] or textgit(repo,'status','--porcelain=v1','--untracked-files=normal')!=item['status']:raise RuntimeError('Repository changed after plan: '+str(repo))
   try:history(repo,meta,item)
   except Exception:
    save_manifest(dest,p);raise
  (meta/'manifest.json').write_text(json.dumps(item,indent=2));item['complete']=True
  print(str(n)+'/'+str(len(p['items']))+' verified '+item['relative_path'],flush=True)
  save_manifest(dest,p)
 p['complete']=True;p['finished_at']=datetime.datetime.now().isoformat();save_manifest(dest,p);print('Archive complete:',dest,flush=True)
if __name__=='__main__':main()
