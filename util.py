def strToTuple(strTuple):
    ret = strTuple.split(",")
    first = int(ret[0])
    second = int(ret[1])
    return (first, second)

def tupleToStr(tpl):
    return str(tpl[0]) + "," + str(tpl[1])
