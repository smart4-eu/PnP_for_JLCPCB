#! /usr/bin/env python3

import csv
import sys
import argparse
import pathlib


def CreateBOM(pnp, bom):
    for row in pnp:    
        find=0     
        for d in bom:
            if row[1].lower() == d[0].lower():
                find=1
                d[1]=d[1]+","+row[0]
                d[2]=str(int(d[2])+1)
        if find==0:    
            bom.append([row[1],row[0],"1",row[3],row[7],""])

def ModifyPnP(file,pnp):
    with open(file, newline='') as csvfile:
        # Tento blok hledá začátek csv v souboru vygenerovaném altiem - na začátku souboru je komentář
        row=0
        for num, line in enumerate(csvfile, 1):
            if '\"Designator\"' in line:
                row=num
                break
        csvfile.seek(0,0);
        if row > 0:
            for i in range(row-1):
                csvfile.readline()
        # odstranění duplikátních názvů
        data = csv.DictReader(csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
        for row in data:    
            find=0     
            for d in pnp:
                if row["Designator"].lower() == d[0].lower().split("_")[0]:
                    find=find+1
            if find==0:    
                pnp.append([row["Designator"],row["Comment"],row["Layer"],row["Footprint"],row["Center-X(mm)"],row["Center-Y(mm)"],row["Rotation"],row["Description"]])
            else:
                pnp.append([row["Designator"]+"_"+str(find),row["Comment"],row["Layer"],row["Footprint"],row["Center-X(mm)"],row["Center-Y(mm)"],row["Rotation"],row["Description"]])

def LCSCCorrection(file,bom):
    with open(file, newline='') as csvfile:
        data = csv.DictReader(csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
        for row in data:       
            for d in bom:
                if row["Comment"].lower() == d[0].lower():
                    d[5]=row["LCSC Part #"]
                
def RotationCorrection(file,pnp):
    with open(file, newline='') as csvfile:
        data = csv.DictReader(csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
        for row in data:       
            for d in pnp:
                if row["Footprint"].lower() == d[3].lower():
                    rc=int(row["Correction"])
                    if (rc>-180) and (rc<180):
                        rc=int(d[6])+rc
                        if rc>=360:
                            rc=rc-360
                        if rc<0:
                            rc=rc+360
                        d[6]=str(rc)
                        
                        

                
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input",
        help="Input CSV PnP file - Altium csv format",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-b", "--bom",
        help="Input CSV BOM file - Altium BOM csv format, LCSC Part # needed",
        type=str,
        required=False,
    )
    parser.add_argument(
        "-o", "--output",
        help="Outuput name",
        type=str,
        required=False,
    )
    parser.add_argument(
        "-r", "--rotation",
        help="Rotation correction for components",
        type=str,
        required=False,
    )
    
    args = parser.parse_args()

    if args.input is not None:
        #Create PnP 
        pnp=[]
        ModifyPnP(args.input,pnp)
        
        #Create BOM
        bom=[]
        CreateBOM(pnp, bom)
        
        if args.bom != None:
            LCSCCorrection(args.bom,bom)
            
        if args.rotation != None:
            RotationCorrection(args.rotation,pnp)
        
        if args.output != None:
            pnp_filename=args.output+"_PnP.csv"
            bom_filename=args.output+"_BOM.csv"
        else:
            pnp_filename="JLCPCB_PnP.csv"
            bom_filename="JLCPCB_BOM.csv" 
                  
        with open(pnp_filename,"w",newline='') as out:
            csv_out=csv.writer(out, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
            csv_out.writerow(['Designator','Comment','Layer','Footprint','Center-X(mm)','Center-Y(mm)','Rotation','Description'])
            for row in pnp:
                csv_out.writerow(row) 
                
        with open(bom_filename,"w",newline='') as out:
            csv_out=csv.writer(out, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
            csv_out.writerow(['Comment','Designator','Quantity','Footprint','Description','LCSC Part #'])
            for row in bom:
                csv_out.writerow(row) 
