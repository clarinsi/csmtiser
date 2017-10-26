from config import load_config_file
config=load_config_file()

import os
import sys


train_orig=config.train_orig
train_norm=config.train_norm
train=[config.train_orig,config.train_norm]
lms=config.lms[:]

if config.tokenise:
  os.system(config.moses_scripts+'/tokenizer/tokenizer.perl < '+config.train_orig+' > '+config.train_orig+'.tok')
  config.train_orig+='.tok'
  os.system(config.moses_scripts+'/tokenizer/tokenizer.perl < '+config.train_norm+' > '+config.train_norm+'.tok')
  config.train_norm+='.tok'

if config.truecase:
  if config.truecase_model==None:
    # learn a truecasing model either on the given dataset or on training data
    if config.truecase_dataset==None:
      # prepare the training data for learning the truecase model
      sys.stdout.write('Concatenating training data for truecasing learning\n')
      os.system('cat '+config.train_orig+' '+config.train_norm+' > '+config.train_orig+'.tmp')
      config.truecase_dataset=config.train_orig+'.tmp'
    sys.stdout.write('Learning the truecaser\n')
    os.system(config.moses_scripts+'/recaser/train-truecaser.perl --model '+config.working_dir+'/truecase.model --corpus '+config.truecase_dataset)
    if config.truecase_dataset==config.train_orig+'.tmp':
      os.system('rm '+config.train_orig+'.tmp')
    config.truecase_model=config.working_dir+'/truecase.model'
  sys.stdout.write('Truecasing train, dev, lm\n') 
  os.system(config.moses_scripts+'/recaser/truecase.perl --model '+config.truecase_model+' < '+config.train_orig+' > '+config.train_orig+'.true')
  config.train_orig+='.true'
  os.system(config.moses_scripts+'/recaser/truecase.perl --model '+config.truecase_model+' < '+config.train_norm+' > '+config.train_norm+'.true')
  config.train_norm+='.true'
  if config.dev_orig!=None:
    os.system(config.moses_scripts+'/recaser/truecase.perl --model '+config.truecase_model+' < '+config.dev_orig+' > '+config.dev_orig+'.true')
    config.dev_orig+='.true'
    os.system(config.moses_scripts+'/recaser/truecase.perl --model '+config.truecase_model+' < '+config.dev_norm+' > '+config.dev_norm+'.true')
    config.dev_norm+='.true'
  for index,pth in enumerate(config.lms):
    sys.stdout.write('Truecasing '+pth+'\n')
    os.system(config.moses_scripts+'/recaser/truecase.perl --model '+config.truecase_model+' < '+pth+' > '+pth+'.true')
    config.lms[index]+='.true'

if config.lowercase:
  sys.stdout.write('Lowercasing training, dev, lm\n')
  os.system(config.moses_scripts+'/tokenizer/lowercase.perl < '+config.train_orig+' > '+config.train_orig+'.lower')
  config.train_orig+='.lower'
  os.system(config.moses_scripts+'/tokenizer/lowercase.perl < '+config.train_norm+' > '+config.train_norm+'.lower')
  config.train_norm+='.lower'
  if config.dev_orig!=None:
    os.system(config.moses_scripts+'/tokenizer/lowercase.perl < '+config.dev_orig+' > '+config.dev_orig+'.lower')
    config.dev_orig+='.lower'
    os.system(config.moses_scripts+'/tokenizer/lowercase.perl < '+config.dev_norm+' > '+config.dev_norm+'.lower')
    config.dev_norm+='.lower'
  for index,pth in enumerate(config.lms):
    sys.stdout.write('Lowercasing '+pth+'\n')
    os.system(config.moses_scripts+'/tokenizer/lowercase.perl < '+pth+' > '+pth+'.lower')
    config.lms[index]+='.lower'

if config.dev_orig==None:
  from random import shuffle
  sys.stdout.write('Reading data for splitting into train and dev\n')
  data=zip(open(config.train_orig),open(config.train_norm))
  shuffle(data)
  train_size=round((1-float(config.dev_perc))*len(data))
  origf=open(config.train_orig+'.train','w')
  normf=open(config.train_norm+'.train','w')
  sys.stdout.write('Splitting the data\n')
  for index,(orig,norm) in enumerate(data):    
    origf.write(orig)
    normf.write(norm)
    if index+1==train_size:
      origf.close()
      normf.close()
      origf=open(config.train_orig+'.dev','w')
      normf=open(config.train_norm+'.dev','w')
  origf.close()
  normf.close()
  config.dev_orig=config.train_orig+'.dev'
  config.dev_norm=config.train_norm+'.dev'
  config.train_orig+='.train'
  config.train_norm+='.train'

sys.stdout.write('Preparing the data for learning the models\n')
SEP=config.tokenseparator#.decode('utf-8')
warn=False
def preprocess(input,output):
  out=open(output,'w')
  for line in open(input):
    if SEP in line.decode(config.encoding):
      warn=True
    out.write((SEP+' '+' '.join(line.decode(config.encoding).strip().replace(' ',SEP))+' '+SEP+'\n').encode(config.encoding))
  out.close()
preprocess(config.train_orig,config.working_dir+'/train.orig')
preprocess(config.train_norm,config.working_dir+'/train.norm')
preprocess(config.dev_orig,config.working_dir+'/dev.orig')
preprocess(config.dev_norm,config.working_dir+'/dev.norm')
for index,pth in enumerate(config.lms):
  preprocess(pth,'lm_'+str(index)+'.proc')
if warn:
  print("You have chosen a token separator ({}) that occurs in the data! Consider choosing another separator in config.py.".format(SEP))
