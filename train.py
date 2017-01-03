import config
import os
import sys

sys.stdout.write('Deleting old models in the working directory\n')
os.system('rm -rf '+config.working_dir+'/corpus')
os.system('rm -rf '+config.working_dir+'/model')
os.system('rm -rf '+config.working_dir+'/giza.norm-orig')
os.system('rm -rf '+config.working_dir+'/giza.orig-norm')
os.system('rm -rf '+config.working_dir+'/train.log')
os.system('rm -rf '+config.working_dir+'/mert-work/')

lms=config.lms[:]
config.lms.insert(0,config.working_dir+'/train.norm')
for index,pth in enumerate(config.lms):
  sys.stdout.write('Building a LM from '+pth+'\n')
  if index>0:
    pth2=config.working_dir+'/lm_'+str(index-1)+'.proc'
  else:
    pth2=pth
  os.system(config.kenlm+'/lmplz -o '+str(config.lm_order)+' --discount_fallback < '+pth+' 1> '+pth2+'.arpa 2>> '+config.working_dir+'/train.log')
  os.system(config.kenlm+'/build_binary '+pth2+'.arpa '+pth2+'.blm >> '+config.working_dir+'/train.log 2>&1')

sys.stdout.write('Building the untuned system\n')
sys.stdout.flush()
os.system(config.moses_scripts+'/training/train-model.perl -root-dir '+config.working_dir+' -corpus '+config.working_dir+'/train -f orig -e norm -alignment grow-diag-final-and -lm 0:'+str(config.lm_order)+':'+config.working_dir+'/train.norm.blm:8 -cores '+str(config.num_cores)+' --mgiza -mgiza-cpus '+str(config.num_cores)+' -external-bin-dir '+config.mgiza+' >> '+config.working_dir+'/train.log 2>&1')

sys.stdout.write('Updating the moses.ini file\n')
ini=open(config.working_dir+'/model/moses.ini').read().replace('[distortion-limit]\n6','[distortion-limit]\n0')
modini=open(config.working_dir+'/model/moses.mod.ini','w')
for line in ini.strip().split('\n'):
  if line.startswith('Distortion') or line.startswith('LexicalReordering'):
    continue
  else:
    modini.write(line+'\n')
  if line.startswith('KENLM'):
    for index in range(1,len(config.lms)):
      modini.write('KENLM lazyken=0 name=LM'+str(index)+' factor=0 path='+config.working_dir+'/lm_'+str(index-1)+'.proc.blm order='+str(config.lm_order)+'\n')
for index in range(1,len(config.lms)):
  modini.write('LM'+str(index)+'= 0.5\n')
modini.close()
sys.stdout.write('Tuning the system\n')
sys.stdout.flush()
os.system(config.moses_scripts+'training/mert-moses.pl '+config.working_dir+'/dev.orig '+config.working_dir+'/dev.norm '+config.moses+'/moses '+config.working_dir+'/model/moses.mod.ini --mertdir '+config.moses+' --working-dir '+config.working_dir+'/mert-work/ --mertargs="--sctype WER" --decoder-flags="-threads '+str(config.num_cores)+'" >> '+config.working_dir+'/train.log 2>&1')
sys.stdout.write('Finished\n')
sys.stdout.flush()
