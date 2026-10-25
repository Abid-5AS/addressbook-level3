"""Export only submission material and verify every ZIP member against SHA-256."""
from pathlib import Path
from datetime import datetime
import hashlib,json,shutil,tempfile,zipfile

root=Path(__file__).resolve().parents[2]
maintenance=root/'maintenance'
out=maintenance/'submission'
out.mkdir(exist_ok=True)
files=set()

def add_file(rel):
    p=root/rel
    if not p.is_file():raise FileNotFoundError(p)
    files.add(p)

def add_tree(rel):
    p=root/rel
    if not p.is_dir():raise FileNotFoundError(p)
    for f in p.rglob('*'):
        if not f.is_file():continue
        relative=f.relative_to(root)
        if f.name=='.DS_Store' or '__pycache__' in relative.parts or 'sandbox' in relative.parts:continue
        if f.suffix in {'.pyc','.jfr'}:continue
        files.add(f)

for name in ['.gitattributes','.gitignore','LICENSE','copyright.txt','README.md','START-HERE.md',
             'build.gradle','gradle.properties','gradlew','gradlew.bat']:
    add_file(name)
for rel in ['src','config','gradle','.run']:
    add_tree(rel)
for name in ['README.md','REPORT.md','AddressBook_Maintenance_Report.pdf','20-ACTIVITY-MATRIX.md','TOOL-EVIDENCE.md']:
    add_file('maintenance/'+name)
for rel in ['changes','diagrams','assets']:
    add_tree('maintenance/'+rel)
for name in ['verify.sh','run-demo.sh','analyze.sh','Doxyfile','AstDump.java','build-report.py','package-submission.py']:
    add_file('maintenance/tools/'+name)
for name in ['00-baseline-build.txt','01-adaptive-tests.txt','02-corrective-before.txt',
             '03-clones-before.txt','04-corrective-after.txt','05-clones-50tokens.txt',
             '06-preventive-tests.txt','12-find-parser-ast.txt','16-jdk27-fresh.txt',
             '20-jfr-summary.txt','doxygen-warnings.txt','summary.json','upstream-commit.txt','publication-history.txt',
             'commit-index.txt','original-source.zip','ui-tag-search.png','ui-invalid-tag.png','ui-list-restored.txt']:
    add_file('maintenance/evidence/'+name)
for rel in ['final-tests','final-coverage','final-checkstyle','patches','reproduced']:
    add_tree('maintenance/evidence/'+rel)
for p in (maintenance/'evidence/final-test-results').glob('TEST-*.xml'):files.add(p)
for name in ['01-find-usages.png','01-find-usages.txt','02-data-flow.png','02-data-flow-export.txt',
             '03-debug-null.png','03-debug-null.txt','04-debug-exception-line.png',
             '05-debug-test-result.png','05-debug-test-result.txt','06-refactor-selected-block.png',
             '07-extract-method.png','08-extract-method.patch',
             '10-refactor-fresh-verification.txt','11-main-launcher-configuration.txt']:
    add_file('maintenance/evidence/intellij/'+name)
add_tree('maintenance/generated/doxygen')
add_file('build/libs/addressbook.jar')
add_file('docs/images/Ui.png')

# Reject private material before any export, including future accidental additions.
for p in files:
    rel=p.relative_to(root)
    assert 'preparation' not in rel.parts and '.git' not in rel.parts,rel
    assert not any(x in p.name for x in ['VIVA-','STUDY','HANDOFF','UNDERSTANDING-GUIDE','CHECKLIST']),rel

manifest={'format':2,'root':'AddressBook-Maintenance','scope':'Submission source, report and selected evidence',
 'files':{str(p.relative_to(root)):{'bytes':p.stat().st_size,
 'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(files)}}
manifest_path=maintenance/'evidence/package-manifest.json'
manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
files.add(manifest_path)

with tempfile.TemporaryDirectory(prefix='assemble-',dir=out) as temp:
    temp=Path(temp);export=temp/'AddressBook-Maintenance';export.mkdir()
    for p in sorted(files):
        target=export/p.relative_to(root);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
    archive=temp/'AddressBook_Maintenance_Submission.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(export.rglob('*')):
            if p.is_file():z.write(p,str(p.relative_to(temp)))
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for name,meta in manifest['files'].items():
            data=z.read('AddressBook-Maintenance/'+name)
            assert len(data)==meta['bytes'] and hashlib.sha256(data).hexdigest()==meta['sha256'],name
        assert not any('/preparation/' in n or '/.git/' in n for n in z.namelist())
    final=out/export.name
    if final.exists():
        backups=maintenance/'generated/previous-submission-exports';backups.mkdir(exist_ok=True)
        shutil.move(final,backups/datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
    shutil.move(export,final)
    shutil.move(archive,out/archive.name)
shutil.copy2(maintenance/'AddressBook_Maintenance_Report.pdf',out/'AddressBook_Maintenance_Report.pdf')
(out/'README.md').write_text('# Ready to Submit\n\nAddressBook_Maintenance_Submission.zip contains source, report and selected supporting evidence. AddressBook-Maintenance/ is the same clean export for repository publishing. The PDF is also copied here for a separate report upload. Personal notes, viva scripts, setup-only CPG files and local Git history are excluded.\n')
archive=out/'AddressBook_Maintenance_Submission.zip'
print(json.dumps({'archive':str(archive),'export':str(final),'verified_files':len(manifest['files']),
 'archive_bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
 'personal_preparation_included':False},indent=2))
