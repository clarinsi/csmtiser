import config
import os
import sys

pth=sys.argv[1]

if config.tokenise:
  sys.stdout.write('Tokenising\n')
  os.system(config.moses_scripts+'/tokenizer/tokenizer.perl < '+pth+' > '+pth+'.tok')
  pth+='.tok'

if config.truecase:
  sys.stdout.write('Truecasing\n') 
  os.system(config.moses_scripts+'/recaser/truecase.perl --model '+config.working_dir+'/truecase.model < '+pth+' > '+pth+'.true')
  pth+='.true'

if config.lowercase:
  sys.stdout.write('Lowercasing '+pth+'\n')
  os.system(config.moses_scripts+'/tokenizer/lowercase.perl < '+pth+' > '+pth+'.lower')
  pth+='.lower'

sys.stdout.write('Preprocessing the data\n')
def preprocess(input,output):
  out=open(output,'w')
  for line in open(input):
    out.write('_ '+' '.join(line.decode(config.encoding).strip().replace(' ','_')).encode(config.encoding)+' _\n')
  out.close()
preprocess(pth,pth+'.proc')
pth+='.proc'

sys.stdout.write('Normalising the data\n')
os.system('rm -f '+config.working_dir+'/norm.log')
os.system(config.moses+'/moses -dl 0 -threads '+str(config.num_cores)+' -f '+config.working_dir+'/mert-work/moses.ini < '+pth+' 2> '+config.working_dir+'/norm.log 1> '+pth+'.norm')
pth+='.norm'

sys.stdout.write('Postprocessing the data\n')
def postprocess(input,output):
  out=open(output,'w')
  for line in open(input):
    out.write(line.strip().strip(' _').replace(' ','').replace('_',' ')+'\n')
  out.close()
postprocess(pth,pth+'.deproc')
pth+='.deproc'

if config.truecase:
  sys.stdout.write('Detruecasing\n')
  os.system(config.moses_scripts+'/recaser/detruecase.perl < '+pth+' > '+pth+'.detrue')
  pth+='.detrue'

if config.tokenise:
  os.system(config.moses_scripts+'/tokenizer/detokenizer.perl < '+pth+' > '+pth+'.detok')
  pth+='.detok'

os.system('mv '+pth+' '+sys.argv[1]+'.norm')
