import lxml.etree as ET
import sys

#fitx = "Batch2a_en_v1.8.NAF"
#tree = ET.parse(inp_naf)
#root = tree.getroot()
inp_naf = sys.stdin.read()

root = ET.fromstring(inp_naf.encode('utf-8'))
sentence_id = "0"
out_xml = ET.Element('corpus')
node_dict = {}
for wf in root.findall('./text/wf'):
    #print(wf.text)
    if wf.attrib["sent"] != sentence_id:
        if sentence_id != '0':
            for d_to,node in node_dict.items():
                dep = root.find('./deps/dep[@to="'+d_to+'"]')
                if dep != None:
                    node.set('si',dep.attrib['rfunc'])
                    parent = node_dict[dep.attrib['from']]
                    parent.append(node)
                else:
                    node.set('si','root')
                    sent.append(node)
        sentence_id = wf.attrib["sent"]
        sent = ET.SubElement(out_xml,'SENTENCE',{'ord':sentence_id,'alloc':'0'})
        w_id_sen = 1
        node_dict = {}
    node = ET.Element('NODE')
    w_id =  wf.attrib['id']#[1:]
    node.set('ord',str(w_id_sen))
    node.set('alloc','0')
    node.set('form',wf.text)
    #term = root.find('./terms/term[@id="t'+w_id+'"]')
    term = root.find('./terms/term/span/target[@id="'+w_id+'"]').getparent().getparent()
    t_id = term.attrib['id']
    node.set('lem',term.attrib['lemma'])
    case = term.attrib['case']
    if '@' in case:
        case = case[:case.index('@')-1]
    node.set('mi','|'+case.replace(' ','|'))
    node_dict[t_id]=node
    w_id_sen += 1
for d_to,node in node_dict.items():
    dep = root.find('./deps/dep[@to="'+d_to+'"]')
    if dep != None:
        node.set('si',dep.attrib['rfunc'])
        parent = node_dict[dep.attrib['from']]
        parent.append(node)
    else:
        node.set('si','root')
        sent.append(node)

print(ET.tostring(out_xml,pretty_print=True,encoding='unicode'))
