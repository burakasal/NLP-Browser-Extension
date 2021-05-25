
def lexiconCheck(text, list, mytxt):

        mfile = open(mytxt, "r", encoding="utf8")
        f=[]
        for l in mfile:
            if len(l)>1:
                f.append(l.strip())
        for line in text:
            for ele in range(0, len(f)):
                if f[ele] in line:
                    list.append(f[ele])
        return list