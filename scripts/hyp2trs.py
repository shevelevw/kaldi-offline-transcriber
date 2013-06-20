'''
Created on Aug 11, 2010

FIXME: topic segmentation broken

@author: tanel
'''
import sys
import re
import datetime
import locale


topicseg_file = ""

def option_handler_t(name):
    """Specify the topicseg file.
    """
    topicseg_file = name
    return

def print_header(filename):
    now = datetime.datetime.now()
    print '<?xml version="1.0" encoding="UTF-8"?>'
    print '<!DOCTYPE Trans SYSTEM "trans-14.dtd">'
    print '<Trans scribe="est-speech2txt" audio_filename="'+ filename+ '" version="1" version_date="' + now.strftime("%y%m%d") + '">'
    
    
def print_footer():
    print '</Episode>'
    print '</Trans>'
    
def print_speakers(speakers):
    print "<Speakers>"
    i = 1
    for v in sorted(speakers.values()):
        print '<Speaker id="%s" name="K%d" check="no" dialect="native" accent="" scope="local" type="male"/>' % (v, i)
        i += 1
    print "</Speakers>"
    print '<Episode>'
        
        
def print_sections(sections, topics):
    
    for i in xrange(len(sections)):
        turns = sections[i]
        topic = None
        if len(topics) > 0:
            topic = topics[i]
        starttime = turns[0][1][0][0]
        endtime = turns[-1][1][-1][1]
        print '<Section type="report" startTime="%s" endTime="%s"' % (starttime, endtime),
        if (topic is not None):
            print 'topic="to%d"' % topic,
        print '>'
        for (speaker, turn) in turns:
            print '<Turn speaker="%s" startTime="%s" endTime="%s">' % (speaker, turn[0][0], turn[-1][1])
            for line in turn:
                #print line[2]
                print '<Sync time="%s"/>' % line[0]
                print line[2]
            print '</Turn>' 
        print '</Section>'
          
def print_topics(topic_last_lines):
    print "<Topics>"
    i = 0
    for t in topic_last_lines:
        print '<Topic id="to%d" desc="Teema %d"/>' % (i, i)            
        i += 1
    print "</Topics>"
    
if __name__ == '__main__':
    
    lines = []
    for l in sys.stdin:
        m = re.match("^(.*) \((.*)_(\d+\.\d+)[_-](\d+\.\d+)_(\S+)(\s+\S+)?\)$", l)
        if m:
            content = m.group(1)
            filename = m.group(2)
            starttime = float(m.group(3))
            endtime = float(m.group(4))
            speaker =m.group(5)
            lines.append((content, filename, starttime, endtime, speaker))
        else:
            raise Exception("cannot process line: " + l)
    speakers = {}
    num_speakers = 0
    for line in lines:
        speaker = line[4]
        if not speakers.has_key(speaker):
            speakers[speaker] = "S%d" % (num_speakers + 1)
            num_speakers += 1
    print_header(lines[0][1])
    topic_last_lines = []
    if topicseg_file != "":
        topic_last_lines = [int(s) for s in open(topicseg_file).readline()[1:-2].split(",")]
        print_topics(topic_last_lines)
        
    print_speakers(speakers)  
    
    
    
    last_speaker = ""
    
    last_endtime = -1
    
    sections = []
    topics = []
    line_no = 0
    for line in lines:
        line_no += 1
        speaker = speakers[line[4]]
        starttime = line[2]
        endtime = line[3]
        content = line[0]
        if starttime != last_endtime or (line_no - 1 in topic_last_lines):
            turns = []
            sections.append(turns)
            if (len(topic_last_lines) > 0):
                topic_index = 0
                
                while topic_last_lines[topic_index] < line_no:
                    topic_index += 1
                topics.append(topic_index)
                
            turn = []
            turns.append((speaker, turn))
        elif speaker != last_speaker :
            turn = []
            turns.append((speaker, turn))
            
        
        turn.append((starttime, endtime, content))
        last_endtime = endtime
        last_speaker = speaker
        
     
        
    print_sections(sections, topics)
        
    print_footer()  
    
            
                
    
         
            
    
          
