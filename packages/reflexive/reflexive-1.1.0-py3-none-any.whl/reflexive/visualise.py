from reflexive import session
from reflexive import cfg

class Display:
    aws:session.AWS = None
    config:cfg.Config = None
    
    defaults = {
        "priority_tags": [
            "VR_ER",
            "AR",
            "RR",
            "EP_EV",
            "AF_CN",
            "EO",
            "EA"
        ],
        "colours": {
            "VR_ER": "#ff6644",
            "AR": "#00cc00",
            "RR": "#6699ff",
            "EP_EV": "#aacc33",
            "AF_CN": "#dd44cc",
            "EO":"#f7f7d4",
            "EA":"#d9f2f2"
        }
    }
    
    # "VR_ER": "#ff6644", #Orange
	# 	"AR": "#00cc00", #Green
	# 	"RR": "#6699ff", #Blue
	# 	"EP_EV": "#aacc33", #Lime
	# 	"AF_CN": "#dd44cc", #magenta
	# 	"EO":"#f7f7d4", #light yellow 
	# 	"EA":"#d9f2f2" #light Cyan
    # {
    #     "priority_tags": ["VR_ER","AR","RR","EP_EV","AF_CN","KP"],
    #     "colours": {"VR_EV_CN": "#ff6644","ER_AF": "#dd44cc","AR": "#00cc00","EP": "#aacc33","RR": "#00aaff","KP":"#aaaacc"}}
    
    def __init__(self,aws):
        self.aws = aws
        self.aws = aws
        self.config = self.aws.config
        self.set_default_parameters()
    
    def set_default_parameters(self):
        priority_tags = self.defaults['priority_tags']
        colours = self.defaults['colours']
        options = {"ents": list(colours.keys()), "colors": colours}
        self.config.set_display_parameters(priority_tags,colours,options)
       
     
    def add_reflexive_offsets(self,df):
        temp_df = df.copy()
        temp_df['reflexive_offsets'] = temp_df.ReflexiveResults.apply(self.collect_reflexive_offsets)
        return temp_df
        
    def add_keyphrase_offsets(self,df):
        temp_df = df.copy()
        temp_df['keyphrase_offsets'] = temp_df.KeyPhraseResults.apply(self.collect_keyphrase_offsets)
        return temp_df
    
    def add_syntax_offsets(self,df):
        temp_df = df.copy()
        temp_df['syntax_offsets'] = temp_df.SyntaxResults.apply(self.collect_syntax_offsets)
        return temp_df
    
    def add_offsets(self,df):
        df = self.add_reflexive_offsets(df)
        df = self.add_keyphrase_offsets(df)
        return self.add_syntax_offsets(df)
    
    def create_displacy(self,df):
        all_ents = list(df.apply(self.render_record,axis=1))
        #html_out = displacy.render(all_ents,manual=True,style="ent", options=options,page=True,jupyter=False)
        # with open(f"{path}{prefix}annotated_reflections{postfix}.html","w") as fp:
        #     fp.write(html_out)
        #displacy.render(all_ents,manual=True,style="ent", options=options)
        return all_ents
            
    def render_record(self,record,title="----"):
        #timestamp = record['timestamp'].split('T')[0]
        #pseudonym = record['pseudonym']
        #point_round = record['point_round']
        #title = f"{pseudonym} ({point_round}) - {timestamp}"
        title = f"Idx_{record.name}"
        tags = self.config.display_priority_tags
        text = record['text']
        reflexive_offsets = record['reflexive_offsets']
        keyphrase_offsets = record['keyphrase_offsets']
        syntax_offsets = record['syntax_offsets']
        ents = []
        taken = []
        offsets = []
        for tag in tags:
            if tag in reflexive_offsets:
                offsets = reflexive_offsets[tag]
            elif tag in syntax_offsets:
                offsets = syntax_offsets[tag]
            elif tag in keyphrase_offsets:
                offsets = keyphrase_offsets[tag]
            
            for off in offsets:
                new_ent = {}
                if off[0] in taken:
                    # the start offset is taken
                    x = None
                elif off[1] in taken:
                    # the end offset is taken
                    x = None
                else:
                    # both start and end is available
                    for t in range(off[0],(off[1]+1)):
                        taken.append(t)
                    #print(taken)
                    new_ent["start"] = off[0]
                    new_ent["end"] = off[1]
                    new_ent["label"] = tag
                    ents.append(new_ent)

        text_ents = {
            "text": text, #.replace('\r\n','\n'),
            "ents": ents,
            "title": title
        }

        return text_ents
    
    def collect_keyphrase_offsets(self,krs):
        new_krs = {}
        for kr in krs:
            if kr['Score']>0.98:
                new_krs.setdefault("KP",[]).append((kr['BeginOffset'],kr['EndOffset']))
        return new_krs

    def collect_reflexive_offsets(self,rrs):
        new_rrs = {}
        for rr in rrs:
            if rr['Score']>0.5:
                ent_type = rr['Type']
                if ent_type in ['VR','ER']:
                    label = "NR"
                elif ent_type in ['EP','EV']:
                    label = "EP"
                elif ent_type in ['CN','AF']:
                    label = "AF"
                else:
                    label = ent_type
                new_rrs.setdefault(label,[]).append((rr['BeginOffset'],rr['EndOffset']))
        return new_rrs
    
    def collect_syntax_offsets(self,syntax_results):
        offsets = {}
        for sr in syntax_results:
            pos = sr['PartOfSpeech']
            if pos['Score']>0.99:
                if pos['Tag'] in ['NOUN','ADJ']: # TE - Topic Entity
                    offsets.setdefault("TE",[]).append((sr['BeginOffset'],sr['EndOffset']))
                # if pos['Tag'] in ['ADV','VERB']:
                #     offsets.setdefault("EA",[]).append((sr['BeginOffset'],sr['EndOffset']))
        return self.concatenate_offsets(offsets)
    
    def concatenate_offsets(self,offsets:dict):
        new_offsets = {}
        for k in offsets.keys():
            #print("TAG:",k)
            #print("Offsets:",len(offsets[k]))
            b,e = offsets[k][0] # set to first tag
            for v in offsets[k]:
                #print("b,e",b,e)
                #print("offset:",v)
                if v[0] <= (e+1): # this tag extends a previous tag
                    e = v[1]
                    #print("extending")
                    #print("new_offset:",(b,e))
                else:   # this tag starts a new tag
                    #print("new tag")
                    new_offsets.setdefault(k,[]).append((b,e))
                    b = v[0]
                    e = v[1]
            #print("New offsets:",len(new_offsets[k]))
        return new_offsets