import codecs

readme_fname = "../readme.md"

def check(s):
    k = 0
    while s[k] == '#':
        k += 1
    
    if k > 0:
        while s[k] in '#.0123456789':
            k += 1
            
        flag = False
        
        s_a = '<a name="'
        s_b = '"></a>'
        
        a = s.find(s_a)
        b = s.find(s_b) 
        href = ''
        if a > 0 and b > 0 and k > 0:
            href = s[a + len(s_a):b]
            flag = True
        
        title = s[k+1:a-1]
        titles = title.split()
        x = f"{titles[0]} [{title[len(titles[0])+1:]}](#{href})"
        return flag, x
        
    return False, ''

lines = codecs.open(readme_fname, "r", "utf-8").readlines()
menu = []
for line in lines:
    flag, x = check(line)
    if flag:
        menu.append(x)
            
s_a = "# Table of Contents"
s_b = "### Table of contents finishes"

content = codecs.open(readme_fname, "r", "utf-8").read()
header = content[:content.find(s_a)+len(s_a)]
footer = content[content.find(s_b):]

with codecs.open(readme_fname, "w", "utf-8") as fout:
    print(header, file=fout)
    print(file=fout)
    print("\n".join(menu), file= fout)
    print(file=fout)
    print(footer, file=fout)