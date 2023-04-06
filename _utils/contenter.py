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
with codecs.open("test.txt", "w", "utf-8") as fout:
    for line in lines:
        flag, x = check(line)
        if flag:
            print(x, file = fout)
    