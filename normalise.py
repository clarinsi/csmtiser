import config
import os
import sys
import re
import string

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
SEP=config.tokenseparator.decode(config.encoding)
warn=False
def preprocess(input,output):
  out=open(output,'w')
  for line in open(input):
    line=line.decode(config.encoding)
    if SEP in line:
      warn=True
    replace_expr = ur'{0} ([^{0}]*\d[^{0}]*|[{1}]) {0}'.format(re.escape(SEP), "".join([re.escape(x) for x in string.punctuation if x != SEP]))
    replacement = ur'{0} <np translation="\1">\1</np> {0}'.format(SEP)
    modline = SEP+' '+' '.join(line.strip().replace(' ',SEP))+' '+SEP+'\n'
    outline = re.sub(replace_expr, replacement, modline)#.encode(config.encoding))
    out.write(outline.encode(config.encoding))
    #out.write(re.sub(r'_ ([^_]*\d[^_]*|[-.:,;!?]) _',r'_ <np translation="\1">\1</np> _','_ '+' '.join(line.decode(config.encoding).strip().replace(' ','_')).encode(config.encoding)+' _\n'))
  out.close()
preprocess(pth,pth+'.proc')
pth+='.proc'
if warn:
  print("The token separator ({}) occurs in the test data. Output may not look as expected.".format(SEP))

sys.stdout.write('Normalising the data\n')
os.system('rm -f '+config.working_dir+'/norm.log')
align=''
if config.align:
  align='-t '
os.system(config.moses+'/moses -xml-input exclusive -dl 0 '+align+'-threads '+str(config.num_cores)+' -f '+config.working_dir+'/mert-work/moses.ini < '+pth+' 2> '+config.working_dir+'/norm.log 1> '+pth+'.norm')
pth+='.norm'

if config.align:
  from alignment import retokenize
  if config.lowercase:
    retokenize(pth[:-5],pth,pth+'.align',True,SEP=SEP)
  else:
    retokenize(pth[:-5],pth,pth+'.align',False,SEP=SEP)
  pth+='.align'
else:
  sys.stdout.write('Postprocessing the data\n')
  def postprocess(input,output):
    out=open(output,'w')
    for line in open(input):
      out.write((line.decode(config.encoding).strip().strip(' '+SEP).replace(' ','').replace(SEP,' ')+'\n').encode(config.encoding))
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
