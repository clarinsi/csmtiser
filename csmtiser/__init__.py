from csmtiser.config import normalizer_config, load_config_file
import os
import re
import string
import sys
import uuid

class Csmtiser:
    def __init__(self, yml_conf):
        self.config=normalizer_config(yml_conf)

    def preprocess(self,input, output):
        SEP = self.config.tokenseparator #.decode(self.config.encoding)

        out = open(output, 'w')
        for line in open(input):
            line = line.decode(self.config.encoding)
            if SEP in line:
                print("The token separator ({}) occurs in the test data. Output may not look as expected.".format(SEP))
            replace_expr = ur'{0} ([^{0}]*\d[^{0}]*|[{1}]) {0}'.format(re.escape(SEP), "".join(
                [re.escape(x) for x in string.punctuation if x != SEP]))
            replacement = ur'{0} <np translation="\1">\1</np> {0}'.format(SEP)
            modline = SEP + ' ' + ' '.join(line.strip().replace(' ', SEP)) + ' ' + SEP + '\n'
            outline = re.sub(replace_expr, replacement, modline)  # .encode(self.config.encoding))
            out.write(outline.encode(self.config.encoding))
            # out.write(re.sub(r'_ ([^_]*\d[^_]*|[-.:,;!?]) _',r'_ <np translation="\1">\1</np> _','_ '+' '.join(line.decode(self.config.encoding).strip().replace(' ','_')).encode(self.config.encoding)+' _\n'))
        out.close()

    def normalise(self,pth):
        if self.config.tokenise:
            sys.stdout.write('Tokenising\n')
            os.system(self.config.moses_scripts + '/tokenizer/tokenizer.perl < ' + pth + ' > ' + pth + '.tok')
            pth += '.tok'

        if self.config.truecase:
            sys.stdout.write('Truecasing\n')
            os.system(
                self.config.moses_scripts + '/recaser/truecase.perl --model ' + self.config.working_dir + '/truecase.model < ' + pth + ' > ' + pth + '.true')
            pth += '.true'

        if self.config.lowercase:
            sys.stdout.write('Lowercasing ' + pth + '\n')
            os.system(self.config.moses_scripts + '/tokenizer/lowercase.perl < ' + pth + ' > ' + pth + '.lower')
            pth += '.lower'

        sys.stdout.write('Preprocessing the data\n')
        SEP = self.config.tokenseparator #.decode(self.config.encoding)



        self.preprocess(pth, pth + '.proc')

        pth += '.proc'


        sys.stdout.write('Normalising the data\n')
        os.system('rm -f ' + self.config.working_dir + '/norm.log')
        align = ''
        if self.config.align:
            align = '-t '
        os.system(self.config.moses + '/moses -xml-input exclusive -dl 0 ' + align + '-threads ' + str(
            self.config.num_cores) + ' -f ' + self.config.working_dir + '/mert-work/moses.ini < ' + pth + ' 2> ' + self.config.working_dir + '/norm.log 1> ' + pth + '.norm')
        pth += '.norm'

        if self.config.align:
            from alignment import retokenize

            if self.config.lowercase:
                retokenize(pth[:-5], pth, pth + '.align', True, SEP=SEP)
            else:
                retokenize(pth[:-5], pth, pth + '.align', False, SEP=SEP)
            pth += '.align'
        else:
            sys.stdout.write('Postprocessing the data\n')


            def postprocess(input, output):
                out = open(output, 'w')
                for line in open(input):
                    out.write((line.decode(self.config.encoding).strip().strip(' ' + SEP).replace(' ', '').replace(SEP,
                                                                                                              ' ') + '\n').encode(
                        self.config.encoding))
                out.close()


            postprocess(pth, pth + '.deproc')
            pth += '.deproc'

            if self.config.truecase:
                sys.stdout.write('Detruecasing\n')
                os.system(self.config.moses_scripts + '/recaser/detruecase.perl < ' + pth + ' > ' + pth + '.detrue')
                pth += '.detrue'

            if self.config.tokenise:
                os.system(self.config.moses_scripts + '/tokenizer/detokenizer.perl < ' + pth + ' > ' + pth + '.detok')
                pth += '.detok'
        return pth

    def normalise_to_string(self,txt):
        if self.config.align==False:
            raise Exception("Invalid align mode for this operation") #check if in proper config mode

        unique_filename = str(uuid.uuid4())
        path=self.config.working_dir+'/'+unique_filename

        with open(path,'w') as f:
            f.write(txt)
        new_path=self.normalise(path)

        with open(new_path,'r') as f:
            res=f.read(txt)
        os.system("rm "+path+"*")

        return res


    def normalise_tokens(self,tokens):
        if self.config.align!=False:
            raise Exception("Invalid align mode for this operation") #check if in proper config mode

        unique_filename = str(uuid.uuid4())
        path=self.config.working_dir+'/'+unique_filename

        with open(path,'w') as f:
            for token in tokens:
                f.write(token+"\n")
        new_path=self.normalise(path)

        with open(new_path,'r') as f:
            normalized_tokens=[t.rstrip() for t in f.readlines()]
        os.system("rm "+path+"*")

        return dict(zip(tokens,normalized_tokens))

