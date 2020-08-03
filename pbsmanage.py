import os,argparse,time,sys,re,subprocess

def runsubprocess(pbsfile):
    pidnumber=subprocess.check_output(["qsub",pbsfile])
    sys.stdout.write("Task %s was submited.\n"%str(pidnumber).strip("b'\\\\n"))
    return str(pidnumber).strip("b'\\\\n")

def pbsmanage(pbscontent,processnumber=100):
    pidcontent=[]
    while True:
        try:
            pidcontent.append(runsubprocess(next(pbscontent)))
            while len(pidcontent)==processnumber:
                [pidcontent.remove(i) for i in pidcontent if not re.findall("\n%s\s.+?\s[QR]\s.+" % (i), subprocess.getoutput("qstat"))]
        except:
            break
    while pidcontent:
        [pidcontent.remove(i) for i in pidcontent if not re.findall("\n%s\s.+?\s[QR]\s.+"%(i),subprocess.getoutput("qstat"))]

if __name__ == "__main__":
    btm=time.time()
    parser = argparse.ArgumentParser(description="To Manage pbs scripts.")
    parser.add_argument("-d", "--diret", required=True, type=str,help="The directory name where the pbsfiles save in")
    parser.add_argument("-p","--process",type=int,help="The process number.",default=100)
    Args=parser.parse_args()
    full_dir=os.path.abspath(Args.diret)
    pbscontent=("/".join([full_dir,i]) for i in os.listdir(full_dir))
    pbsmanage(pbscontent=pbscontent,processnumber=Args.process)
    etm=time.time()
    sys.stdout.write("%.3f hours used totally.\n"%round((etm-btm)/3600,3))
